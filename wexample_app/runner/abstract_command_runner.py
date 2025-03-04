from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.common.service.service_mixin import ServiceMixin

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command_request import CommandRequest


class AbstractCommandRunner(AbstractKernelChild, ServiceMixin, BaseModel):
    def __init__(self, kernel: "AbstractKernel", **kwargs):
        BaseModel.__init__(self, **kwargs)
        AbstractKernelChild.__init__(self, kernel=kernel)

    @abstractmethod
    def build_command(self, request: "CommandRequest") -> Optional["Command"]:
        pass

    def will_run(self, request: "CommandRequest") -> bool:
        return False
