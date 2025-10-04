from __future__ import annotations

from wexample_wex_addon_dev_python.workdir.python_workdir import PythonWorkdir
from wexample_wex_core.workdir.project_workdir import ProjectWorkdir


class AppWorkdir(PythonWorkdir):
    @classmethod
    def create_from_config(cls, **kwargs) -> ProjectWorkdir:
        print('OK!')
        exit()
