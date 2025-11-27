from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_app.const.globals import WORKDIR_SETUP_DIR
from wexample_helpers.classes.mixin.has_env_keys import HasEnvKeys
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


@base_class
class WithEnvParametersMixin(HasEnvKeys):
    @classmethod
    def get_env_parameters_from_path(cls, path: Path) -> NestedConfigValue:
        from wexample_filestate.item.file.env_file import EnvFile

        env_path = path / WORKDIR_SETUP_DIR / EnvFile.EXTENSION_DOT_ENV

        if env_path.exists():
            dot_env = EnvFile.create_from_path(
                path=env_path,
            )
            return dot_env.read_config()

        return NestedConfigValue(raw={})

    def get_env_parameters(self) -> NestedConfigValue:
        return self.get_env_parameters_from_path(
            path=self.get_path(),
        )

    def get_env_parameter(self, key: str, default: str | None = None) -> str | None:
        # Search in .env.
        value = (
            self.get_env_parameters()
            .get_config_item(key=key, default=default)
            .get_str_or_none()
        )

        if value is None:
            return super().get_env_parameter(
                key=key,
                default=default,
            )

        return value
