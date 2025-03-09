from __future__ import annotations

from typing import List, Type, TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from wexample_app.const.globals import ENV_VAR_NAME_APP_ENV
from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin
from wexample_filestate.mixins.with_workdir_mixin import WithWorkdirMixin
from wexample_helpers.classes.mixin.has_env_keys_file import HasEnvKeysFile
from wexample_prompt.mixins.with_prompt_context import WithPromptContext
from wexample_prompt.responses.base_prompt_response import BasePromptResponse

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest


class AbstractKernel(
    ServiceContainerMixin,
    HasEnvKeysFile,
    WithWorkdirMixin,
    WithPromptContext,
    BaseModel
):
    entrypoint_path: str = Field(description="The main file placed at application root directory")

    def __init__(self, **kwargs) -> None:
        BaseModel.__init__(self, **kwargs)
        HasEnvKeysFile.__init__(self)

    def get_expected_env_keys(self) -> List[str]:
        return [
            ENV_VAR_NAME_APP_ENV
        ]

    def setup(self) -> "AbstractKernel":
        from wexample_helpers.const.globals import FILE_NAME_ENV, FILE_NAME_ENV_YAML

        self._init_io_manager()
        self._init_workdir(entrypoint_path=self.entrypoint_path, io_manager=self.io)
        workdir_resolved = self.workdir.get_resolved()
        self._init_env_file(f"{workdir_resolved}{FILE_NAME_ENV}")
        self._init_env_file_yaml(f"{workdir_resolved}{FILE_NAME_ENV_YAML}")

        return self

    def _get_command_request_class(self) -> Type["CommandRequest"]:
        from wexample_app.common.command_request import CommandRequest
        return CommandRequest

    def execute_kernel_command(self, request: "CommandRequest") -> BasePromptResponse:
        return request.execute()
