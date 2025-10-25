from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_app.command.option import Option
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.utils.file_state_manager import FileStateManager

    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.const.types import CommandLineArgumentsList


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

    def _get_core_args(self: AbstractKernel) -> list[Option]:
        return []

    def _handle_core_args(self: AbstractKernel) -> None:
        """Parse and handle core arguments, removing them from _sys_argv."""
        from wexample_wex_core.helpers.argument_parser import parse_arguments

        core_options = self._get_core_args()
        
        if not core_options:
            return

        # Parse core arguments from sys_argv
        try:
            parsed_core_args = parse_arguments(
                arguments=self._sys_argv[1:],  # Skip program name
                options=core_options,
                allowed_option_names=[opt.name for opt in core_options],
            )
        except Exception:
            # If parsing fails, silently continue (core args are optional)
            return

        # Apply parsed values to kernel attributes
        for option in core_options:
            if option.name in parsed_core_args:
                # Use the option's value field if set, otherwise use parsed value
                value = option.value if option.value is not None else parsed_core_args[option.name]
                setattr(self, f"_config_arg_{option.name}", value)

        # Remove core arguments from _sys_argv to prevent them from being passed to commands
        self._remove_core_args_from_sys_argv(core_options)

    def _remove_core_args_from_sys_argv(self: AbstractKernel, core_options: list[Option]) -> None:
        """Remove core arguments from _sys_argv."""
        i = 1  # Skip program name
        while i < len(self._sys_argv):
            arg = self._sys_argv[i]
            removed = False

            # Check for long option (--option)
            if arg.startswith("--"):
                option_name = arg[2:]
                for option in core_options:
                    if option.kebab_name == option_name:
                        del self._sys_argv[i]
                        # If not a flag, also remove the next argument (the value)
                        if not option.is_flag and i < len(self._sys_argv) and not self._sys_argv[i].startswith("-"):
                            del self._sys_argv[i]
                        removed = True
                        break

            # Check for short option (-o)
            elif arg.startswith("-") and len(arg) > 1:
                short_name = arg[1:]
                for option in core_options:
                    if option.short_name == short_name:
                        del self._sys_argv[i]
                        # If not a flag, also remove the next argument (the value)
                        if not option.is_flag and i < len(self._sys_argv) and not self._sys_argv[i].startswith("-"):
                            del self._sys_argv[i]
                        removed = True
                        break

            if not removed:
                i += 1

    def _init_command_line_kernel(self: AbstractKernel) -> None:
        import os
        import sys

        from wexample_filestate.utils.file_state_manager import FileStateManager

        self._sys_argv = sys.argv.copy()
        self._call_workdir = FileStateManager.create_from_path(
            path=os.getcwd(), config={}, io=self.io
        )

        self._handle_core_args()
