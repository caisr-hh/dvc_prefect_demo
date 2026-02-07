"""Train and evaluate a simple sklearn model."""

from dataclasses import dataclass
from pathlib import Path
from typing import cast

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class FitArtifacts:
    """Return trained artifacts."""

    model: LogisticRegression
    scaler: StandardScaler | None


def fit_logreg(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    C: float,
    max_iter: int,
    standardize: bool,
) -> FitArtifacts:
    """Fit logistic regression."""

    scaler: StandardScaler | None = None
    x_arr = x_train.to_numpy()

    if standardize:
        scaler = StandardScaler()
        x_arr = scaler.fit_transform(x_arr)

    model = LogisticRegression(C=C, max_iter=max_iter, solver="lbfgs")
    model.fit(x_arr, y_train.to_numpy())

    return FitArtifacts(model=model, scaler=scaler)


def predict(artifacts: FitArtifacts, x: pd.DataFrame, *, standardize: bool) -> np.ndarray:
    """Predict labels."""

    x_arr = x.to_numpy()
    if standardize and artifacts.scaler is not None:
        x_arr = artifacts.scaler.transform(x_arr)
    return cast(np.ndarray, artifacts.model.predict(x_arr))


def save_artifacts(artifacts: FitArtifacts, path: Path) -> None:
    """Save model artifacts."""

    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifacts, path)


def load_artifacts(path: Path) -> FitArtifacts:
    """Load model artifacts."""

    return cast(FitArtifacts, joblib.load(path))


def compute_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    """Compute simple classification metrics."""

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
    }
