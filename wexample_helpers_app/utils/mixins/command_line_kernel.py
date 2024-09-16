from __future__ import annotations


class CommandLineKernel:
    _sys_argv: list[str]

    def _init_command_line_kernel(self):
        import sys

        self._sys_argv: list[str] = sys.argv.copy()

    def exec_argv(self):
        pass
