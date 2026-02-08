"""Prefect Tasks and Flow (Option B) where Prefect takes ownership of the Pipeline DAG"""

import tempfile
from pathlib import Path

from mltoy.config import load_params
from mltoy.pipeline import stage_evaluate, stage_prepare, stage_train

from .prefect_server_utils import PrefectServerConfig, set_project_prefect_env
from .utils import repo_root

# NOTE: See prefect_server_setup module doc for why set_project_prefect_env
#       should be called before importing prefect
set_project_prefect_env(PrefectServerConfig())
from prefect import flow, task  # pylint: disable=wrong-import-position, wrong-import-order


@task(name="prepare")
def prepare_task(params_path: Path = Path("params.yaml")) -> None:
    """Prepare train/test splits (Python-native stage)."""
    params = load_params(repo_root() / params_path)
    stage_prepare(
        raw_csv=repo_root() / "data/raw/iris.csv",
        train_csv=repo_root() / "data/processed/train.csv",
        test_csv=repo_root() / "data/processed/test.csv",
        params=params,
    )


@task(name="train", retries=1, retry_delay_seconds=2)
def train_task(*, params_path: Path = Path("params.yaml"), fail_once: bool = False) -> None:
    """Train model (Python-native stage)."""
    if fail_once:
        marker = Path(tempfile.gettempdir()) / "prefect_demo_train_fail_once.marker"
        if not marker.exists():
            marker.write_text("fail once\n", encoding="utf-8")
            raise RuntimeError("Intentional one-time failure to demonstrate retries.")

    params = load_params(repo_root() / params_path)
    stage_train(
        train_csv=repo_root() / "data/processed/train.csv",
        model_path=repo_root() / "models/model.joblib",
        params=params,
    )


@task(name="evaluate")
def evaluate_task(params_path: Path = Path("params.yaml")) -> None:
    """Evaluate model (Python-native stage)."""
    params = load_params(repo_root() / params_path)
    stage_evaluate(
        test_csv=repo_root() / "data/processed/test.csv",
        model_path=repo_root() / "models/model.joblib",
        metrics_path=repo_root() / "reports/metrics.json",
        params=params,
    )


@flow(name="Prefect owned stage DAG")
def pipeline_flow(
    *, params_path: Path = Path("params.yaml"), fail_train_once: bool = False
) -> None:
    """Run prepare -> train -> evaluate as Prefect tasks."""
    prepare_task(params_path=params_path)
    train_task(params_path=params_path, fail_once=fail_train_once)
    evaluate_task(params_path=params_path)
