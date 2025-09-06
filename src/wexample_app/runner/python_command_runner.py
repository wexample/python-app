from __future__ import annotations
from typing import TYPE_CHECKING, Any
from wexample_app.runner.abstract_file_command_runner import AbstractFileCommandRunner

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from typing import Any
    from wexample_helpers.const.types import AnyCallable
    from types import ModuleType


class PythonCommandRunner(AbstractFileCommandRunner):
    def get_file_extension(self) -> str:
        from wexample_helpers.const.globals import FILE_EXTENSION_PYTHON

        return FILE_EXTENSION_PYTHON

    def _load_command_python_module(self, request: CommandRequest) -> ModuleType:
        from wexample_app.exception.command_module_load_error_exception import CommandModuleLoadErrorException
        import importlib.util

        path = self.build_command_path(request)
        path_str = str(path)

        # Import module and load function.
        spec = importlib.util.spec_from_file_location(path_str, path_str)
        if not spec or not spec.loader:
            raise CommandModuleLoadErrorException(file_path=path_str)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    def _load_command_python_function(self, request: CommandRequest) -> AnyCallable:
        from wexample_app.exception.command_function_name_missing_exception import CommandFunctionNameMissingException
        function_name = request.resolver.build_command_function_name(request)

        if not function_name:
            raise CommandFunctionNameMissingException(command_name=request.command_name)

        module = self._load_command_python_module(request=request)
        return getattr(module, function_name, None)

    def _build_command_function(self, request: CommandRequest) -> Any:
        return self._load_command_python_function(request=request)
