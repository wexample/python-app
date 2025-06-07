import os.path
from typing import Optional
from typing import TYPE_CHECKING
from types import ModuleType

from wexample_app.exception.command_file_not_found import CommandFileNotFound
from wexample_app.exception.command_module_load_error import CommandModuleLoadError
from wexample_app.exception.command_function_name_missing import CommandFunctionNameMissing
from wexample_app.exception.command_function_not_found import CommandFunctionNotFound
from wexample_app.runner.abstract_command_runner import AbstractCommandRunner
from wexample_helpers.const.types import AnyCallable

if TYPE_CHECKING:
    from wexample_app.common.command import Command
    from wexample_app.common.command_request import CommandRequest


class PythonCommandRunner(AbstractCommandRunner):
    def will_run(self, request: "CommandRequest") -> bool:
        from pathlib import Path
        from wexample_helpers.const.globals import FILE_EXTENSION_PYTHON

        path = request.resolver.build_command_path(request)
        if path is None:
            return False

        file_path = Path(path)
        file_extension = file_path.suffix.lower()

        return file_extension == f".{FILE_EXTENSION_PYTHON}"

    def _load_command_python_module(self, request: "CommandRequest") -> ModuleType:
        import importlib.util

        path = request.resolver.build_command_path(request)
        if not os.path.exists(path):
            raise CommandFileNotFound(file_path=path)

        # Import module and load function.
        spec = importlib.util.spec_from_file_location(path, path)
        if not spec or not spec.loader:
            raise CommandModuleLoadError(file_path=path)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    def _load_command_python_function(self, request: "CommandRequest") -> AnyCallable:
        function_name = request.resolver.build_command_function_name(request)

        if not function_name:
            raise CommandFunctionNameMissing(command_name=request.command_name)

        module = self._load_command_python_module(request=request)
        return getattr(module, function_name, None)


    def build_runnable_command(self, request: "CommandRequest") -> Optional["Command"]:
        function = self._load_command_python_function(request=request)

        if not function:
            path = request.resolver.build_command_path(request)
            function_name = request.resolver.build_command_function_name(request)
            raise CommandFunctionNotFound(function_name=function_name, module_path=path)

        return request.resolver.get_command_class_type()(
            kernel=self.kernel,
            function=function
        ) if function is not None else None
