from __future__ import annotations

from typing import List, Type, TYPE_CHECKING

from pydantic import BaseModel, Field

from wexample_app.const.globals import ENV_VAR_NAME_APP_ENV
from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin
from wexample_filestate.mixins.with_workdir_mixin import WithWorkdirMixin
from wexample_helpers.classes.mixin.has_env_keys import HasEnvKeys
from wexample_prompt.mixins.with_prompt_context import WithPromptContext
from wexample_prompt.responses.base_prompt_response import BasePromptResponse

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.common.abstract_addon_manager import AbstractAddonManager


class AbstractKernel(
    ServiceContainerMixin,
    HasEnvKeys,
    WithWorkdirMixin,
    WithPromptContext,
    BaseModel
):
    entrypoint_path: str = Field(description="The main file placed at application root directory")

    def get_expected_env_keys(self) -> List[str]:
        return [
            ENV_VAR_NAME_APP_ENV
        ]

    def setup(self, addons: List[Type["AbstractAddonManager"]]) -> "AbstractKernel":
        self._init_io_manager()
        self._init_workdir(self.entrypoint_path, self.io_manager)
        self._load_env_file(f"{self.workdir.get_resolved()}{self._get_dotenv_file_name()}")
        self.register_items("addons", addons)
        return self

    def _get_command_request_class(self) -> Type["CommandRequest"]:
        from wexample_app.common.command_request import CommandRequest
        return CommandRequest

    def execute_kernel_command(self, request: "CommandRequest") -> BasePromptResponse:
        return request.execute()
