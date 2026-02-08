"""Project-scoped Prefect server Utils

This module adopts a single Prefect API server bound to a project-local state
directory, so all flows share one backend without spawning a temporary server
per stage. It sets PREFECT_HOME, local storage, and the API database file under
`prefect/`, avoids writes to `~/.prefect`, and exports PREFECT_API_URL for
clients.

The `set_project_prefect_env` function sets all the required ENV variables,
should be called prior to importing Prefect or calling `is_prefect_server_up`.
"""

import os
from pathlib import Path
from urllib.request import urlopen

from pydantic import BaseModel

from .utils import repo_root


class PrefectServerConfig(BaseModel):
    """Prefect server config"""

    project_dir: Path = repo_root()
    prefect_dir_name: str = "prefect"
    prefect_db_filename: str = "prefect.db"
    host: str = "127.0.0.1"
    port: int = 4200

    @property
    def api_url(self) -> str:
        """Build the Prefect API URL for health checks and client config."""
        return f"http://{self.host}:{self.port}/api"

    @property
    def prefect_home(self) -> str:
        """Return path to prefect home directory"""
        path = self.project_dir / self.prefect_dir_name
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    @property
    def storage_path(self) -> str:
        """Return path to prefect home directory"""
        path = Path(self.prefect_home) / "storage"
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    @property
    def db_connection_url(self) -> str:
        """Return url to prefect db connection"""
        return f"sqlite+aiosqlite:///{self.prefect_home}/{self.prefect_db_filename}"

    @property
    def health_url(self) -> str:
        """Return url prefect server's health"""
        return f"{self.api_url}/health"


def set_project_prefect_env(config: PrefectServerConfig) -> None:
    """Set project-scoped Prefect environment variables (DB, storage, home)."""
    os.environ["PREFECT_RESULTS_PERSIST_BY_DEFAULT"] = "true"
    os.environ["PREFECT_HOME"] = config.prefect_home
    os.environ["PREFECT_LOCAL_STORAGE_PATH"] = config.storage_path
    os.environ["PREFECT_API_DATABASE_CONNECTION_URL"] = config.db_connection_url
    os.environ["PREFECT_API_URL"] = config.api_url


def is_prefect_server_up(config: PrefectServerConfig, timeout_s: float = 1.5) -> bool:
    """Return True if a Prefect server responds on the given API URL."""
    set_project_prefect_env(config)
    try:
        with urlopen(config.health_url, timeout=timeout_s):
            return True
    except Exception:  # pylint: disable=broad-exception-caught
        return False
