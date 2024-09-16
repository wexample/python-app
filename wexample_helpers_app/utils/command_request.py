from wexample_helpers_app.utils.abstract_kernel_child import AbsractKernelChild


class CommandRequest(AbsractKernelChild):
    name: str
    arguments: list[str] = []

    def execute(self) -> None:
        # Tmp
        self.kernel.io.print(self.name)
