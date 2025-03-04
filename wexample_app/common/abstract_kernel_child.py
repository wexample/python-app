from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel


class AbstractKernelChild:
    _kernel: "AbstractKernel" = None

    @property
    def kernel(self) -> "AbstractKernel":
        assert self._kernel is AbstractKernel

        return self._kernel

    @kernel.setter
    def kernel(self, value: "AbstractKernel"):
        self._kernel = value
