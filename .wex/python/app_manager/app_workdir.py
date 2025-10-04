from __future__ import annotations

from wexample_wex_addon_app.workdir.mixin.app_workdir_mixin import AppWorkdirMixin
from wexample_wex_addon_dev_python.workdir.python_workdir import PythonWorkdir


class AppWorkdir(PythonWorkdir):
    @classmethod
    def create_from_config(cls, **kwargs) -> AppWorkdirMixin:
        print('OK!')
        exit()
