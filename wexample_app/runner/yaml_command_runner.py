from typing import TYPE_CHECKING

from wexample_app.runner.abstract_file_command_runner import AbstractFileCommandRunner
from wexample_helpers.const.types import AnyCallable

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest


class YamlCommandRunner(AbstractFileCommandRunner):
    def get_file_extension(self) -> str:
        from wexample_helpers.const.globals import FILE_EXTENSION_YAML
        return FILE_EXTENSION_YAML

    def _build_command_function(self, request: "CommandRequest") -> AnyCallable:
        def _script_command_handler(kernel, arguments):
            print('Executing command: ' + request.name)

        return _script_command_handler
