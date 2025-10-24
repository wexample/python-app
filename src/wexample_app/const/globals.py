from __future__ import annotations

from pathlib import Path

from wexample_wex_core.const.globals import WORKDIR_SETUP_DIR

# filestate: python-constant-sort
APP_FILE_APP_CONFIG: str = "config.yml"
APP_FILE_APP_MANAGER: Path = Path("app-manager")
APP_PATH_APP_MANAGER: Path = WORKDIR_SETUP_DIR / "python" / "app_manager"
APP_PATH_BIN_APP_MANAGER: Path = WORKDIR_SETUP_DIR / "bin" / APP_FILE_APP_MANAGER

ENV_VAR_NAME_APP_ENV = "APP_ENV"
