import mlflow
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, KFold


def main():
    mlflow.sklearn.autolog(max_tuning_runs=15)

    data = np.load("../../data/processed.npy")
    X = data[:, :-1]
    y = data[:, -1]
    cv = KFold(n_splits=3, random_state=42, shuffle=True)
    scoring = {"acc": "accuracy", "f1": "f1_macro"}  # roc_auc_ovr

    parameters = {
        "penalty": ["l1", "l2"],
        "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        "solver": ["liblinear", "saga"],
        "max_iter": [100, 1000, 2500, 5000],
    }
    logreg = LogisticRegression(random_state=42)
    clf = GridSearchCV(logreg, parameters, cv=cv, n_jobs=-1, scoring=scoring, verbose=1, refit="f1")

    clf.fit(X, y)
    run_id = mlflow.last_active_run().info.run_id

    # show data logged in the child runs
    filter_child_runs = "tags.mlflow.parentRunId = '{}'".format(run_id)
    runs = mlflow.search_runs(filter_string=filter_child_runs)

    with mlflow.start_run(run_name="logreg best") as run:
        print(f"Best parameters set found on development set: {clf.best_params_} with score {clf.best_score_}")
        mlflow.log_params(clf.best_params_)
        mlflow.log_metric("f1", clf.best_score_)
        mlflow.sklearn.log_model(clf, "model")
        mlflow.sklearn.log_model(clf.best_estimator_, "best_estimator")


if __name__ == "__main__":
    main()
