from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import attrs
from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_helpers.classes.base_class import BaseClass

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.const.types import ResponsePrintable


@attrs.define(kw_only=True)
class AbstractResponse(AbstractKernelChild, BaseClass):
    kernel: AbstractKernel = attrs.field()

    def __attrs_post_init__(self) -> None:
        AbstractKernelChild.__init__(self, kernel=self.kernel)

    @abstractmethod
    def get_printable(self) -> ResponsePrintable:
        pass

    def get_wrapped_printable(self) -> str:
        printable = self.get_printable()

        if printable is None:
            return ""

        return printable
