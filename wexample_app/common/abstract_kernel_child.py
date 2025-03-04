from typing import TYPE_CHECKING, Optional

from pydantic import PrivateAttr

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel


class AbstractKernelChild:
    _kernel: Optional["AbstractKernel"] = PrivateAttr(default=None)

    def __init__(self, kernel: "AbstractKernel"):
        self._kernel = kernel

    @property
    def kernel(self) -> "AbstractKernel":
        from wexample_app.common.abstract_kernel import AbstractKernel
        assert isinstance(self._kernel, AbstractKernel)

        return self._kernel

    @kernel.setter
    def kernel(self, value: "AbstractKernel"):
        self._kernel = value
