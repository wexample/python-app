from typing import Any, List

from pydantic import BaseModel, Field

from wexample_app.const.globals import ENV_VAR_NAME_APP_ENV
from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin
from wexample_filestate.mixins.with_workdir_mixin import WithWorkdirMixin
from wexample_helpers.classes.mixin.has_env_keys import HasEnvKeys
from wexample_prompt.mixins.with_prompt_context import WithPromptContext


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

    def model_post_init(self, __context: Any) -> None:
        self._init_io_manager()
        self._init_workdir(self.entrypoint_path, self.io_manager)
        self._load_env_file(f"{self.workdir.get_resolved()}{self._get_dotenv_file_name()}")
