import mlflow
import numpy as np
import optuna
from optuna.trial import Trial
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


def load_data(test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    data = np.load("../../data/processed.npy")
    X = data[:, :-1]
    y = data[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)
    return X_train, X_test, y_train, y_test


def objective(trial: Trial) -> float:
    # Load iris dataset
    X_train, X_test, y_train, y_test = load_data()

    # Define hyperparameters for Logistic Regression
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 1, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.001, 1),
        "gamma": trial.suggest_float("gamma", 0, 20),
        "subsample": trial.suggest_float("subsample", 0.8, 1),
    }
    model = XGBClassifier(**params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")

    # Log metrics to MLflow
    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1", f1)

    return f1


def main():
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30, n_jobs=-1)

    trial = study.best_trial
    print(f"Best parameters set found on development set: {trial.params}")

    with mlflow.start_run(run_name="XGB best") as run:
        X_train, X_test, y_train, y_test = load_data()

        clf = XGBClassifier(**trial.params)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        f1 = f1_score(y_test, y_pred, average="macro")
        mlflow.log_metric("f1", f1)
        mlflow.sklearn.log_model(clf, "model")
        accuracy = accuracy_score(y_test, y_pred)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_params(trial.params)


if __name__ == "__main__":
    main()
