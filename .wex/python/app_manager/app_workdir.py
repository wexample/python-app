from __future__ import annotations

from wexample_wex_addon_app.workdir.mixin.app_workdir_mixin import AppWorkdirMixin
from wexample_wex_addon_dev_python.workdir.python_package_workdir import PythonPackageWorkdir


class AppWorkdir(PythonPackageWorkdir):
    def get_ordered_readme_files_names(self) -> list[str]:
        return [
            'introduction'
        ]

    @classmethod
    def create_from_config(cls, **kwargs) -> AppWorkdirMixin:
        print('OK!')
        exit()
