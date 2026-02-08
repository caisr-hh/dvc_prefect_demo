"""Prefect Tasks and Flow

DVC takes ownership of the Pipeline DAG
Prefect wraps DVC operations
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, Sequence

from .prefect_server_utils import PrefectServerConfig, set_project_prefect_env
from .utils import repo_root

# NOTE: See prefect_server_setup module doc for why set_project_prefect_env
#       should be called before importing prefect
set_project_prefect_env(PrefectServerConfig())
from prefect import (  # pylint: disable=wrong-import-position, wrong-import-order
    flow,
    get_run_logger,
    task,
)


def _to_str_cmd(cmd: Sequence[str]) -> str:
    return " ".join(cmd)


def _iter_lines(stream: Iterable[str]) -> Iterable[str]:
    for raw in stream:
        line = raw.rstrip("\n")
        if line:
            yield line


def run_cmd(cmd: Sequence[str], *, cwd: Path) -> None:
    """Run a command and stream stdout/stderr into Prefect logs."""
    logger = get_run_logger()

    logger.info("Running: %s", _to_str_cmd(cmd))
    logger.info("CWD: %s", str(cwd))

    proc = subprocess.Popen(  # pylint: disable=consider-using-with
        list(cmd),
        cwd=str(cwd),
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert proc.stdout is not None

    for line in _iter_lines(proc.stdout):
        logger.info(line)

    returncode = proc.wait()
    if returncode:
        raise RuntimeError(f"Command failed (rc={returncode}): {_to_str_cmd(cmd)}")


@task(name="dvc repro", retries=1, retry_delay_seconds=2)
def dvc_repro_task(*, fail_once: bool) -> None:
    """Run `dvc repro` as a single Prefect task."""
    if fail_once:
        marker = Path(tempfile.gettempdir()) / "prefect_demo_fail_once.marker"
        if not marker.exists():
            marker.write_text("fail once\n", encoding="utf-8")
            raise RuntimeError("Intentional one-time failure to demonstrate retries.")

    run_cmd(["dvc", "repro"], cwd=repo_root())


@task(name="metrics summary")
def metrics_summary_task(metrics_path: Path = Path("reports/metrics.json")) -> None:
    """Load metrics json and log a short summary."""
    logger = get_run_logger()
    full_path = (repo_root() / metrics_path).resolve()
    if not full_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {full_path}")

    metrics = json.loads(full_path.read_text(encoding="utf-8"))
    logger.info("Metrics: %s", json.dumps(metrics, sort_keys=True))


@flow(name="Prefect operates DVC pipeline")
def dvc_pipeline_flow(*, fail_once: bool = False, show_metrics: bool = True) -> None:
    """Operate the DVC pipeline via `dvc repro`."""
    dvc_repro_task(fail_once=fail_once)
    if show_metrics:
        metrics_summary_task()
