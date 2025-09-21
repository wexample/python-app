from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.const.types import CommandLineArgumentsList
    from wexample_filestate.utils.file_state_manager import FileStateManager


@base_class
class CommandLineKernel(BaseClass):
    _call_workdir: FileStateManager = private_field(
        description="The directory path from where the call has been run"
    )
    _core_argv: list[str] = private_field(
        factory=list, description="Core command arguments processed by the kernel"
    )
    _sys_argv: list[str] = private_field(
        factory=list, description="System command line arguments from sys.argv"
    )
    _sys_argv_end_index: int | None = private_field(
        default=None, description="End index for processing sys.argv slice"
    )
    _sys_argv_start_index: int = private_field(
        default=1, description="Start index for processing sys.argv slice"
    )

    @property
    def call_workdir(self) -> FileStateManager:
        # Getter is non-optional and always returns a conformant type
        return self._call_workdir

    def exec_argv(self: AbstractKernel) -> None:
        """
        Main entrypoint from command line calls.
        May not be called by an internal script.
        """
        try:
            command_requests = self._build_command_requests_from_arguments(
                self._sys_argv[self._sys_argv_start_index : self._sys_argv_end_index]
            )
        except Exception as e:
            self.io.error(exception=e, fatal=True)

            return

        for command_request in command_requests:
            self.execute_kernel_command_and_print(command_request)

    def _build_command_requests_from_arguments(
        self: AbstractKernel, arguments: CommandLineArgumentsList
    ) -> list[CommandRequest]:
        # By default, allow one request per execution call.
        return self._build_single_command_request_from_arguments(arguments)

    def _build_single_command_request_from_arguments(
        self: AbstractKernel, arguments: CommandLineArgumentsList
    ):
        return [
            self._get_command_request_class()(
                kernel=self, name=arguments[0], arguments=arguments[1:]
            )
        ]

    def _get_core_args(self: AbstractKernel) -> list[dict[str, Any]]:
        return []

    def _handle_core_args(self: AbstractKernel) -> None:
        from wexample_helpers.helpers.args import args_shift_one

        for arg_config in self._get_core_args():
            if args_shift_one(self._sys_argv, arg_config["arg"], True) is not None:
                setattr(self, f"_config_arg_{arg_config['attr']}", arg_config["value"])

    def _init_command_line_kernel(self: AbstractKernel) -> None:
        import os
        import sys

        from wexample_filestate.utils.file_state_manager import FileStateManager

        self._sys_argv = sys.argv.copy()
        self._call_workdir = FileStateManager.create_from_path(
            path=os.getcwd(), config={}, io=self.io
        )

        self._handle_core_args()
