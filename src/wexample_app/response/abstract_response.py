from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.const.types import ResponsePrintable

from wexample_helpers.decorator.base_class import base_class


@base_class
class AbstractResponse(AbstractKernelChild, BaseClass):
    kernel: AbstractKernel = public_field(description="The kernel that produced the response")

    @abstractmethod
    def get_printable(self) -> ResponsePrintable:
        pass

    def get_wrapped_printable(self) -> str:
        printable = self.get_printable()

        if printable is None:
            return ""

        return printable
