from typing import TYPE_CHECKING

from wexample_app.runner.abstract_file_command_runner import AbstractFileCommandRunner
from wexample_helpers.const.types import AnyCallable

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest


class YamlCommandRunner(AbstractFileCommandRunner):
    def _build_command_function(self, request: "CommandRequest") -> AnyCallable:
        def _temp(kernel, arguments):
            # TODO improve
            print('kernel: ' + str(kernel))
            print('arguments: ' + str(arguments))

        return _temp
