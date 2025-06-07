from typing import Callable, Any, TYPE_CHECKING

from pydantic import BaseModel

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.response.null_response import NullResponse

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.response.abstract_response import AbstractResponse


class Command(AbstractKernelChild, BaseModel):
    function: Callable[..., Any] = None

    def __init__(self, kernel: "AbstractKernel", **kwargs):
        BaseModel.__init__(self, **kwargs)
        AbstractKernelChild.__init__(self, kernel=kernel)

    def execute(self, arguments) -> "AbstractResponse":
        # Basic way to execute command.
        response = self.function(
            kernel=self.kernel,
            arguments=arguments
        )

        if response is None:
            return NullResponse(kernel=self.kernel)

        return response