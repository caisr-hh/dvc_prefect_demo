"""Utility functions for the project."""

from functools import lru_cache
from pathlib import Path

from git import Repo as GitRepo


@lru_cache(maxsize=1)
def repo_root() -> Path:
    """Return path to the git repo of the project"""
    if not (path := GitRepo(__file__, search_parent_directories=True).working_tree_dir):
        raise RuntimeError("Not inside a Git repository.")
    return Path(path)
