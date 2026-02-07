"""Define and validate configuration."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class SplitConfig(BaseModel):
    """Describe train/test split behavior."""

    test_size: float = Field(..., ge=0.05, le=0.95)
    random_state: int = Field(..., ge=0)


class PreprocessConfig(BaseModel):
    """Describe preprocessing behavior."""

    standardize: bool = True


class TrainConfig(BaseModel):
    """Describe model training hyperparameters."""

    C: float = Field(..., gt=0.0)
    max_iter: int = Field(..., ge=10)


class Params(BaseModel):
    """Hold all demo parameters."""

    split: SplitConfig
    preprocess: PreprocessConfig
    train: TrainConfig


def load_params(path: Path) -> Params:
    """Load parameters from YAML."""

    raw_text = path.read_text(encoding="utf-8")
    data: Any = yaml.safe_load(raw_text)
    return Params.model_validate(data)
