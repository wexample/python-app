from pydantic import PrivateAttr


class CommandLineKernel:
    _sys_argv: list[str] = PrivateAttr(default_factory=list)

    def _init_command_line_kernel(self):
        import sys

        self._sys_argv = sys.argv.copy()

    def exec_argv(self):
        """
        Main entrypoint from command line calls.
        May not be called by an internal script.
        """
        pass
