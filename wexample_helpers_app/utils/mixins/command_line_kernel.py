from __future__ import annotations

from typing import Type

from wexample_helpers.helpers.args_helper import args_shift_one
from wexample_helpers_app.const.types import CommandLineArgumentsList
from wexample_helpers_app.utils.command_request import CommandRequest


class CommandLineKernel:
    _sys_argv: list[str]
    _sys_argv_start_index: int | None = 1
    _sys_argv_end_index: int | None = None
    _core_argv: list[str]

    def _init_command_line_kernel(self):
        import sys

        self._sys_argv: list[str] = sys.argv.copy()

        self._handle_core_args()

    def _get_core_args(self):
        return {}

    def _handle_core_args(self):
        for arg_config in self._get_core_args():
            if args_shift_one(self._sys_argv, arg_config["arg"], True) is not None:
                setattr(self, arg_config["attr"], arg_config["value"])

    def exec_argv(self):
        """
        Main entrypoint from command line calls.
        May not be called by an internal script.
        """

        command_requests = self._build_command_requests_from_arguments(
            self._sys_argv[self._sys_argv_start_index:self._sys_argv_end_index]
        )

        for command_request in command_requests:
            self.execute_kernel_command(command_request)

    def _build_command_requests_from_arguments(self, arguments: CommandLineArgumentsList) -> list[CommandRequest]:
        return []

    def _build_single_command_request_from_arguments(self, arguments: CommandLineArgumentsList):
        return [
            (self._get_command_request_class())(
                kernel=self,
                name=arguments[0],
                arguments=arguments[1:])
        ]
