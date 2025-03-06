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
    from wexample_app.common.abstract_addon_manager import AbstractAddonManager


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

    def get_expected_env_keys(self) -> List[str]:
        return [
            ENV_VAR_NAME_APP_ENV
        ]

    def setup(self, addons: Optional[List[Type["AbstractAddonManager"]]] = None) -> "AbstractKernel":
        self._init_io_manager()
        self._init_workdir(entrypoint_path=self.entrypoint_path, io_manager=self.io)
        self._init_env_file(f"{self.workdir.get_resolved()}{self._get_dotenv_file_name()}")
        self._init_addons(addons=addons)

        return self

    def _init_addons(self, addons: Optional[List[Type["AbstractAddonManager"]]] = None):
        from wexample_helpers.service.registry import Registry

        self.set_registry("addon", Registry)
        self.register_items("addon", addons or [])

    def _get_command_request_class(self) -> Type["CommandRequest"]:
        from wexample_app.common.command_request import CommandRequest
        return CommandRequest

    def execute_kernel_command(self, request: "CommandRequest") -> BasePromptResponse:
        return request.execute()
