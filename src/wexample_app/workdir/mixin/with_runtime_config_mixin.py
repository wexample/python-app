from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.const.path import APP_DIR_NAME_TMP
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.dict import dict_interpolate

from wexample_app.workdir.mixin.with_config_mixin import WithConfigMixin
from wexample_app.workdir.mixin.with_env_parameters_mixin import WithEnvParametersMixin

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue
    from wexample_filestate.item.file.yaml_file import YamlFile


@base_class
class WithRuntimeConfigMixin(WithEnvParametersMixin, WithConfigMixin):
    def build_runtime_config_value(self, reload_config: bool = False) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue
        from wexample_helpers.helpers.dict import dict_merge

        return NestedConfigValue(
            raw=dict_interpolate(
                dict_merge(
                    self.get_config(reload=reload_config).to_dict(),
                    self.get_config(
                        env_name=self.get_app_env(), reload=reload_config
                    ).to_dict_or_none()
                    or {},
                ),
                self.get_env_parameters().to_dict(),
            )
        )

    def get_runtime_config(self, rebuild: bool = False) -> NestedConfigValue:
        runtime_config_file = self.get_runtime_config_file()
        env_name = self.get_app_env()

        if rebuild or self._runtime_config_is_stale(runtime_config_file, env_name):
            runtime_config_file.write_config(
                self.build_runtime_config_value(reload_config=True)
            )

        return runtime_config_file.read_config(reload=rebuild)

    def get_runtime_config_file(self) -> YamlFile:
        from wexample_app.const.globals import (
            APP_FILE_APP_RUNTIME_CONFIG,
            WORKDIR_SETUP_DIR,
        )

        # We don't search into the target item tree as this is a low level information.
        return self.get_yaml_file_from_path(
            path=self.get_path()
            / WORKDIR_SETUP_DIR
            / APP_DIR_NAME_TMP
            / APP_FILE_APP_RUNTIME_CONFIG,
        )

    def write_config_value(self, *args, **kwargs) -> None:
        self.get_config_file().write_config_value(*args, **kwargs)
        self.get_runtime_config(rebuild=True)

    def _runtime_config_is_stale(
        self, runtime_config_file: YamlFile, env_name: str | None
    ) -> bool:
        runtime_path = runtime_config_file.get_path()
        if not runtime_path.exists():
            return True

        # Rebuild if the runtime file is empty or older than source configs.
        runtime_mtime = runtime_path.stat().st_mtime
        if runtime_path.stat().st_size == 0:
            return True

        config_path = self.get_config_file().get_path()
        if config_path.exists() and config_path.stat().st_mtime > runtime_mtime:
            return True

        if env_name:
            env_config_path = self.get_config_file(env_name=env_name).get_path()
            if (
                env_config_path.exists()
                and env_config_path.stat().st_mtime > runtime_mtime
            ):
                return True

        return False
