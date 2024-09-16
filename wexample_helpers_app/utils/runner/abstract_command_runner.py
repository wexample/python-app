from abc import abstractmethod
from typing import Optional

from wexample_helpers_app.utils.abstract_kernel_child import AbsractKernelChild

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers_app.utils.command import Command
    from wexample_helpers_app.utils.command_request import CommandRequest


class AbstractCommandRunner(AbsractKernelChild):
    @classmethod
    @abstractmethod
    def get_runner_name(cls) -> str:
        pass

    @abstractmethod
    def build_command(self, request: "CommandRequest") -> Optional["Command"]:
        pass

    def will_run(self, request: "CommandRequest") -> bool:
        return False