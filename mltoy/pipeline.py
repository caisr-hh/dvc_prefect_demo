"""Implement the toy ML pipeline stages."""

import json
from pathlib import Path

from sklearn.model_selection import train_test_split

from mltoy.config import Params
from mltoy.data import FEATURE_COLUMNS, LABEL_COLUMN, load_csv, load_raw_csv, save_csv
from mltoy.modeling import compute_metrics, fit_logreg, load_artifacts, predict, save_artifacts


def stage_prepare(
    *,
    raw_csv: Path,
    train_csv: Path,
    test_csv: Path,
    params: Params,
) -> None:
    """Prepare train/test CSVs."""

    df = load_raw_csv(raw_csv)

    x = df[FEATURE_COLUMNS]
    y = df[LABEL_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=params.split.test_size,
        random_state=params.split.random_state,
        stratify=y,
    )

    train_df = x_train.copy()
    train_df[LABEL_COLUMN] = y_train

    test_df = x_test.copy()
    test_df[LABEL_COLUMN] = y_test

    save_csv(train_df, train_csv)
    save_csv(test_df, test_csv)


def stage_train(
    *,
    train_csv: Path,
    model_path: Path,
    params: Params,
) -> None:
    """Train model and save artifacts."""

    train_df = load_csv(train_csv)
    x_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[LABEL_COLUMN]

    artifacts = fit_logreg(
        x_train,
        y_train,
        C=params.train.C,
        max_iter=params.train.max_iter,
        standardize=params.preprocess.standardize,
    )
    save_artifacts(artifacts, model_path)


def stage_evaluate(
    *,
    test_csv: Path,
    model_path: Path,
    metrics_path: Path,
    params: Params,
) -> dict[str, float]:
    """Evaluate model and write metrics."""

    test_df = load_csv(test_csv)
    x_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[LABEL_COLUMN]

    artifacts = load_artifacts(model_path)
    y_pred = predict(artifacts, x_test, standardize=params.preprocess.standardize)

    metrics = compute_metrics(y_test, y_pred)

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return metrics


def run_all(  # pylint: disable=too-many-arguments
    *,
    raw_csv: Path,
    train_csv: Path,
    test_csv: Path,
    model_path: Path,
    metrics_path: Path,
    params: Params,
) -> dict[str, float]:
    """Run the full pipeline."""

    stage_prepare(raw_csv=raw_csv, train_csv=train_csv, test_csv=test_csv, params=params)
    stage_train(train_csv=train_csv, model_path=model_path, params=params)
    return stage_evaluate(
        test_csv=test_csv,
        model_path=model_path,
        metrics_path=metrics_path,
        params=params,
    )
