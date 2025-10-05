from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel_child import AbstractKernelChild

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.const.types import ResponsePrintable


@base_class
class AbstractResponse(AbstractKernelChild, BaseClass):
    kernel: AbstractKernel = public_field(
        description="The kernel that produced the response"
    )

    @abstract_method
    def get_printable(self) -> ResponsePrintable:
        pass

    def get_wrapped_printable(self) -> str:
        printable = self.get_printable()

        if printable is None:
            return ""

        return printable
