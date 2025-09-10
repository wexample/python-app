from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import attrs
from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.common.service.service_mixin import ServiceMixin
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.const.types import StringsMatch

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command import Command
    from wexample_app.common.command_request import CommandRequest
    from wexample_helpers.const.types import StringsList


from wexample_helpers.decorator.base_class import base_class
@base_class
class AbstractCommandResolver(
    AbstractKernelChild, ServiceMixin, PrintableMixin, BaseClass
):
    kernel: AbstractKernel = public_field(description="The app kernel")

    @classmethod
    def build_match(cls, command: str) -> StringsMatch | None:
        import re

        return re.match(cls.get_pattern(), command) if command else None

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "CommandResolver"

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass

    # @abstractmethod
    def build_command(self, request: CommandRequest) -> Command | None:
        return request.runner.build_runnable_command(request)

    def build_command_function_name(self, request: CommandRequest) -> str | None:
        return None

    def build_command_path(
        self, request: CommandRequest, extension: str
    ) -> Path | None:
        return None

    def get_command_class_type(cls) -> type[Command]:
        from wexample_app.common.command import Command

        return Command

    def get_function_name_parts(self, parts: StringsList) -> StringsList:
        return [
            parts[0],
            parts[1],
            parts[2],
        ]

    def supports(self, request: CommandRequest) -> StringsMatch | None:
        match = self.build_match(request.name)

        if match:
            return match

        return None
