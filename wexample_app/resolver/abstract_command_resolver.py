from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.common.service.service_mixin import ServiceMixin
from wexample_helpers.const.types import StringsMatch, StringsList

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.common.abstract_kernel import AbstractKernel


class AbstractCommandResolver(AbstractKernelChild, ServiceMixin, BaseModel):
    def __init__(self, kernel: "AbstractKernel", **kwargs):
        BaseModel.__init__(self, **kwargs)
        AbstractKernelChild.__init__(self, kernel=kernel)

    @classmethod
    def get_class_name_suffix(cls) -> Optional[str]:
        return 'CommandResolver'

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass

    @classmethod
    def build_match(cls, command: str) -> Optional[StringsMatch]:
        import re
        return re.match(cls.get_pattern(), command) if command else None

    def build_command_path(self, request: "CommandRequest") -> Optional[str]:
        return None

    def build_command_function_name(self, request: "CommandRequest") -> None:
        return None

    def supports(self, request: "CommandRequest") -> Optional[StringsMatch]:
        match = self.build_match(request.name)

        if match:
            return match

        return None

    def get_function_name_parts(self, parts: StringsList) -> StringsList:
        return [
            parts[0],
            parts[1],
            parts[2],
        ]