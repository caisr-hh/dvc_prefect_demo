"""Load and store data for the demo pipeline."""

from pathlib import Path

import pandas as pd

FEATURE_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]
LABEL_COLUMN = "label"


def load_raw_csv(path: Path) -> pd.DataFrame:
    """Load raw CSV as a DataFrame."""

    return pd.read_csv(path)


def save_csv(df: pd.DataFrame, path: Path) -> None:
    """Save DataFrame as CSV."""

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def load_csv(path: Path) -> pd.DataFrame:
    """Load CSV as a DataFrame."""

    return pd.read_csv(path)
