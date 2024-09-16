from wexample_helpers_app.utils.abstract_kernel_child import AbsractKernelChild
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_prompt.utils.prompt_response import PromptResponse


class CommandRequest(AbsractKernelChild):
    name: str
    arguments: list[str] = []

    def execute(self) -> "PromptResponse":
        from wexample_prompt.utils.prompt_response import PromptResponse

        return PromptResponse.from_message(self.name)
