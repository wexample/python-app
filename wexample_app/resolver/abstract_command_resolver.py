from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.common.service.service_mixin import ServiceMixin

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.common.abstract_kernel import AbstractKernel


class AbstractCommandResolver(AbstractKernelChild, ServiceMixin, BaseModel):
    @classmethod
    def get_class_name_suffix(cls) -> Optional[str]:
        return 'CommandResolver'

    def __init__(self, kernel: "AbstractKernel", **kwargs):
        BaseModel.__init__(self, **kwargs)
        AbstractKernelChild.__init__(self, kernel=kernel)

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass

    def supports(self, request: "CommandRequest") -> bool:
        # By default, resolver match with every command.
        return True

    def build_command_path(self, request: "CommandRequest") -> Optional[str]:
        return None

    def build_command_function_name(self, request: "CommandRequest") -> None:
        return None
