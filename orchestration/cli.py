"""CLI interface for the Prefect orchestrator"""

import argparse
import os
import sys
from typing import Sequence

from .prefect_flows import dvc_pipeline_flow
from .prefect_server_utils import PrefectServerConfig, is_prefect_server_up


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prefect walkthrough entrypoints.")
    parser.add_argument("--fail-once", action="store_true", help="Fail once to show retries.")
    parser.add_argument("--show_metrics", action="store_true", help="Skip metrics summary task.")
    return parser.parse_args(argv)


def _main(argv: Sequence[str]) -> int:
    args = _parse_args(argv)
    if not is_prefect_server_up(PrefectServerConfig()):
        print("Prefect server unavailable!")
        return os.EX_SOFTWARE

    dvc_pipeline_flow(fail_once=args.fail_once, show_metrics=args.show_metrics)
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
