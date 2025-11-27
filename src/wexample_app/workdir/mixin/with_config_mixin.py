from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.workdir.mixin.with_yaml_files import WithYamlFiles
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue
    from wexample_filestate.item.file.yaml_file import YamlFile
    from wexample_helpers.const.types import FileStringOrPath

@base_class
class WithConfigMixin(WithYamlFiles):
    def get_config_file(self) -> YamlFile:
        from wexample_app.const.globals import WORKDIR_SETUP_DIR, APP_FILE_APP_CONFIG

        # We don't search into the target item tree as this is a low level information.
        return self.get_yaml_file_from_path(
            path=self.get_path() / WORKDIR_SETUP_DIR / APP_FILE_APP_CONFIG
        )

    @classmethod
    def get_config_from_path(cls, path: FileStringOrPath) -> YamlFile | None:
        from pathlib import Path

        from wexample_filestate.item.file.yaml_file import YamlFile
        from wexample_app.const.globals import WORKDIR_SETUP_DIR, APP_FILE_APP_CONFIG

        setup_config_path = Path(path) / WORKDIR_SETUP_DIR / APP_FILE_APP_CONFIG

        if setup_config_path.exists():
            return YamlFile.create_from_path(
                path=setup_config_path,
            )

        return None

    def get_config(self) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue

        config_file = self.get_config_file()
        if config_file:
            return config_file.read_config()

        return NestedConfigValue(raw={})
