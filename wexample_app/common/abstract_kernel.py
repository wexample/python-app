from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Type

from pydantic import BaseModel, Field
from wexample_app.const.globals import ENV_VAR_NAME_APP_ENV
from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin
from wexample_filestate.mixins.with_workdir_mixin import WithWorkdirMixin
from wexample_helpers.classes.mixin.has_env_keys_file import HasEnvKeysFile
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.response.abstract_response import AbstractResponse


class AbstractKernel(
    ServiceContainerMixin,
    HasEnvKeysFile,
    WithWorkdirMixin,
    WithIoMethods,
    PrintableMixin,
    BaseModel,
):
    entrypoint_path: str = Field(
        description="The main file placed at application root directory"
    )
    root_request: Any | None = None

    def __init__(self, **kwargs) -> None:
        BaseModel.__init__(self, **kwargs)
        HasEnvKeysFile.__init__(self)

    def get_expected_env_keys(self) -> list[str]:
        return [ENV_VAR_NAME_APP_ENV]

    def setup(self) -> AbstractKernel:
        import os
        from pathlib import Path

        from wexample_helpers.const.globals import FILE_NAME_ENV, FILE_NAME_ENV_YAML

        self._init_io_manager()
        workdir_resolved = f"{Path(self.entrypoint_path).parent}{os.sep}"
        self._init_env_file(f"{workdir_resolved}{FILE_NAME_ENV}")
        self._init_env_file_yaml(f"{workdir_resolved}{FILE_NAME_ENV_YAML}")
        self._init_workdir(entrypoint_path=self.entrypoint_path, io_manager=self.io)

        return self

    def _get_command_request_class(self) -> type[CommandRequest]:
        from wexample_app.common.command_request import CommandRequest

        return CommandRequest

    def execute_kernel_command(self, request: CommandRequest) -> AbstractResponse:
        # Save unique root request
        self.root_request = self.root_request if self.root_request else request

        return request.execute()

    def execute_kernel_command_and_print(self, request: CommandRequest) -> None:
        self.execute_kernel_command(request=request)
