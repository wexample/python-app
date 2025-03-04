from typing import Any, cast
from typing import List, Optional, Union, TYPE_CHECKING

from pydantic import BaseModel, Field, PrivateAttr

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.runner.abstract_command_runner import AbstractCommandRunner

if TYPE_CHECKING:
    from wexample_wex_core.common.kernel import Kernel
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver


class CommandRequest(
    AbstractKernelChild,
    BaseModel
):
    name: str
    arguments: List[Union[str, int]] = Field(default_factory=list)
    path: Optional[str] = None
    type: Optional[str] = None
    _resolver: Optional["AbstractCommandResolver"] = PrivateAttr(default=None)
    _runner: Optional["AbstractCommandRunner"] = PrivateAttr(default=None)

    def __init__(self, kernel: "Kernel", **kwargs):
        BaseModel.__init__(self, **kwargs)
        AbstractKernelChild.__init__(self, kernel=kernel)

        self.type = self.guess_type()
        self.resolver = self.get_resolver()
        self.path = self.resolver.build_command_path(request=self)
        self.runner = self.guess_runner()

    @property
    def resolver(self) -> "AbstractCommandResolver":
        return self._resolver

    @resolver.setter
    def resolver(self, value: "AbstractCommandResolver"):
        self._resolver = value

    @property
    def runner(self) -> "AbstractCommandRunner":
        return self._runner

    @runner.setter
    def runner(self, value: "AbstractCommandRunner"):
        self._runner = value

    @property
    def kernel(self) -> Union["AbstractKernel", "CommandRunnerKernel"]:
        # Enforce typing
        return cast("CommandRunnerKernel", super().kernel)

    def execute(self) -> Any:
        if self.runner is None:
            return None

        command = self.runner.build_command(request=self)

        return command.execute(self.arguments) if command is not None else None

    def get_resolver(self) -> Optional["AbstractCommandResolver"]:
        return self.kernel.get_resolver(self.type)

    def guess_runner(self) -> Optional["AbstractCommandRunner"]:
        for runner in self.kernel.get_runners().values():
            if runner.will_run(self):
                return runner
        return None

    def guess_type(self) -> Optional[str]:
        for resolver in self.kernel.get_resolvers().values():
            if resolver.supports(request=self):
                return resolver.get_type()
        return None
