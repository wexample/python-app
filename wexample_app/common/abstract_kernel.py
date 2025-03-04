from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin
from wexample_filestate.mixins.with_workdir_mixin import WithWorkdirMixin
from wexample_prompt.mixins.with_prompt_context import WithPromptContext

if TYPE_CHECKING:
    pass


class AbstractKernel(
    ServiceContainerMixin,
    WithWorkdirMixin,
    WithPromptContext,
    BaseModel
):
    entrypoint_path: str = Field(description="The main file placed at application root directory")

    def model_post_init(self, __context: Any) -> None:
        self._init_io_manager()
        self._init_workdir(
            self.entrypoint_path,
            self.io_manager
        )
