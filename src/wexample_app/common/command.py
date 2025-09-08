from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import attrs
from wexample_helpers.classes.base_class import BaseClass
from wexample_app.common.abstract_kernel_child import AbstractKernelChild

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.response.abstract_response import AbstractResponse


class Command(AbstractKernelChild, BaseClass):
    function: Callable[..., Any] = attrs.field(default=None)

    kernel: AbstractKernel = attrs.field()

    def __attrs_post_init__(self) -> None:
        AbstractKernelChild.__init__(self, kernel=self.kernel)

    def execute_request(self, request: CommandRequest) -> Any:
        # Basic way to execute command.
        return self.function(kernel=self.kernel, arguments=request.arguments)

    def execute_request_and_normalize(
        self, request: CommandRequest
    ) -> AbstractResponse:
        from wexample_app.helpers.response import response_normalize

        return response_normalize(
            kernel=self.kernel, response=self.execute_request(request=request)
        )
