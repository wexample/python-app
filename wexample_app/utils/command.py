from typing import Callable, Any

from wexample_app.utils.abstract_kernel_child import AbsractKernelChild


class Command(AbsractKernelChild):
    function: Callable[..., Any] = None

    def execute(self):
        return self.function(
            kernel=self.kernel
        )
