"""Provide a tiny CLI for running the pipeline."""

import argparse
from pathlib import Path
from typing import Callable

from mltoy.config import load_params
from mltoy.pipeline import run_all, stage_evaluate, stage_prepare, stage_train


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--params",
        type=Path,
        default=Path("params.yaml"),
        help="Path to params.yaml",
    )


def _cmd_prepare(args: argparse.Namespace) -> None:
    params = load_params(args.params)
    stage_prepare(
        raw_csv=args.raw,
        train_csv=args.train,
        test_csv=args.test,
        params=params,
    )


def _cmd_train(args: argparse.Namespace) -> None:
    params = load_params(args.params)
    stage_train(
        train_csv=args.train,
        model_path=args.model,
        params=params,
    )


def _cmd_evaluate(args: argparse.Namespace) -> None:
    params = load_params(args.params)
    stage_evaluate(
        test_csv=args.test,
        model_path=args.model,
        metrics_path=args.metrics,
        params=params,
    )


def _cmd_run_all(args: argparse.Namespace) -> None:
    params = load_params(args.params)
    run_all(
        raw_csv=args.raw,
        train_csv=args.train,
        test_csv=args.test,
        model_path=args.model,
        metrics_path=args.metrics,
        params=params,
    )


def build_parser() -> argparse.ArgumentParser:
    """Build argparse parser."""

    parser = argparse.ArgumentParser(prog="mltoy")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prepare = sub.add_parser("prepare", help="Prepare train/test splits.")
    _add_common_args(p_prepare)
    p_prepare.add_argument("--raw", type=Path, default=Path("data/raw/iris.csv"))
    p_prepare.add_argument("--train", type=Path, default=Path("data/processed/train.csv"))
    p_prepare.add_argument("--test", type=Path, default=Path("data/processed/test.csv"))
    p_prepare.set_defaults(func=_cmd_prepare)

    p_train = sub.add_parser("train", help="Train model.")
    _add_common_args(p_train)
    p_train.add_argument("--train", type=Path, default=Path("data/processed/train.csv"))
    p_train.add_argument("--model", type=Path, default=Path("models/model.joblib"))
    p_train.set_defaults(func=_cmd_train)

    p_eval = sub.add_parser("evaluate", help="Evaluate model.")
    _add_common_args(p_eval)
    p_eval.add_argument("--test", type=Path, default=Path("data/processed/test.csv"))
    p_eval.add_argument("--model", type=Path, default=Path("models/model.joblib"))
    p_eval.add_argument("--metrics", type=Path, default=Path("reports/metrics.json"))
    p_eval.set_defaults(func=_cmd_evaluate)

    p_run = sub.add_parser("run-all", help="Run prepare --> train --> evaluate.")
    _add_common_args(p_run)
    p_run.add_argument("--raw", type=Path, default=Path("data/raw/iris.csv"))
    p_run.add_argument("--train", type=Path, default=Path("data/processed/train.csv"))
    p_run.add_argument("--test", type=Path, default=Path("data/processed/test.csv"))
    p_run.add_argument("--model", type=Path, default=Path("models/model.joblib"))
    p_run.add_argument("--metrics", type=Path, default=Path("reports/metrics.json"))
    p_run.set_defaults(func=_cmd_run_all)

    return parser


def main(argv: list[str] | None = None) -> None:
    """Run CLI entrypoint."""

    parser = build_parser()
    args = parser.parse_args(argv)
    func: Callable[[argparse.Namespace], None] = args.func
    func(args)


if __name__ == "__main__":
    main()
