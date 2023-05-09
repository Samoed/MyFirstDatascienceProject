import mlflow
import numpy as np
import optuna
from optuna.trial import Trial
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def load_data(test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    data = np.load("../../data/processed.npy")
    X = data[:, :-1]
    y = data[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)
    return X_train, X_test, y_train, y_test


def objective(trial: Trial) -> float:
    X_train, X_test, y_train, y_test = load_data()

    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 5000),
        'max_depth': trial.suggest_int('max_depth', 1, 10),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2']),
        "criterion": trial.suggest_categorical("criterion", ["gini", "entropy"]),
    }

    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')

    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1", f1)

    return f1


def main():
    mlflow.sklearn.autolog(max_tuning_runs=15)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30, n_jobs=-1)

    trial = study.best_trial
    print(f"Best parameters set found on development set: {trial.params}")

    with mlflow.start_run(run_name="Forest best") as run:
        X_train, X_test, y_train, y_test = load_data()

        clf = RandomForestClassifier(**trial.params)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        f1 = f1_score(y_test, y_pred, average='macro')
        mlflow.log_metric("f1", f1)
        mlflow.sklearn.log_model(clf, "model")
        accuracy = accuracy_score(y_test, y_pred)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_params(trial.params)


if __name__ == "__main__":
    main()
