from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from wexample_prompt.mixins.with_prompt_context import WithPromptContext
from wexample_prompt.common.io_manager import IoManager

if TYPE_CHECKING:
    pass


class AbstractKernel(
    WithPromptContext,
    BaseModel
):
    entrypoint_path: str = Field(description="The main file placed at application root directory")

    def model_post_init(self, __context: Any) -> None:
        self.io = IoManager()
        self.io.log('OK')