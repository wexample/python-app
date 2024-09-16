from typing import Optional
from typing import TYPE_CHECKING

from wexample_helpers_app.utils.runner.abstract_command_runner import AbstractCommandRunner

if TYPE_CHECKING:
    from wexample_helpers_app.utils.command import Command
    from wexample_helpers_app.utils.command_request import CommandRequest


class PythonCommandRunner(AbstractCommandRunner):
    @classmethod
    def get_runner_name(cls) -> str:
        return "python"

    def will_run(self, request: "CommandRequest") -> bool:
        from pathlib import Path
        from wexample_helpers.const.globals import FILE_EXTENSION_PYTHON

        file_path = Path(request.resolver.build_command_path(request))
        file_extension = file_path.suffix.lower()

        return file_extension == f".{FILE_EXTENSION_PYTHON}"

    def build_command(self, request: "CommandRequest") -> Optional["Command"]:
        import importlib.util
        from wexample_helpers_app.utils.command import Command

        # request = self.get_request()
        path = request.resolver.build_command_path(request)

        # Import module and load function.
        spec = importlib.util.spec_from_file_location(path, path)

        if not spec or not spec.loader:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        function = getattr(module, request.resolver.build_command_function_name(request), None)

        return Command(
            kernel=self.kernel,
            function=function
        ) if function is not None else None
