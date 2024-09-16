from typing import Any, Optional, Dict, Type

from pydantic import BaseModel, Field
from wexample_helpers.const.types import StringsList
from wexample_prompt.io_manager import IOManager
from wexample_filestate.file_state_manager import FileStateManager
from wexample_helpers_app.utils.command_request import CommandRequest

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers_app.utils.abstract_command_resolver import AbstractCommandResolver


class AbstractKernel(BaseModel):
    io: Optional[IOManager] = None
    directory: Optional[FileStateManager] = None
    entrypoint_path: str = Field(description="The main file placed at application root directory")
    root_path: Optional[str] = None
    resolvers: Dict[str, "AbstractCommandResolver"] = None
    env_config: Dict[str, Optional[str]] = None
    expected_env_items: Optional[StringsList] = [
        "APP_ENV"
    ]
    workdir: FileStateManager = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

        self.io = IOManager()

        self._init_workdir()
        self._init_env_values()
        self._init_command_resolvers()

        # Validate configuration.
        self._check_env_values()

    def _init_env_values(self):
        from dotenv import dotenv_values

        self.env_config = dotenv_values(f"{self.workdir.get_resolved()}{self._get_dotenv_file_name()}")

    def _get_dotenv_file_name(self) -> str:
        from wexample_helpers.const.globals import DOTENV_FILE_NAME
        return DOTENV_FILE_NAME

    def _init_workdir(self):
        self.workdir = (self._get_workdir_state_manager_class()).create_from_path(
            path=self.entrypoint_path,
            config={}
        )

    def _init_command_resolvers(self):
        self.resolvers: Dict[str, Type["AbstractCommandResolver"]] = {
            class_definition.get_type(): class_definition(kernel=self)
            for class_definition in self._get_command_resolvers()
        }


    def _get_workdir_state_manager_class(self) -> Type[FileStateManager]:
        return FileStateManager

    def _get_command_request_class(self) -> Type[CommandRequest]:
        return CommandRequest

    def _check_env_values(self):
        from wexample_helpers.helpers.dict_helper import dict_get_first_missing_key
        first_missing_key = dict_get_first_missing_key(self.env_config, self.expected_env_items)
        if first_missing_key:
            # TODO Use logger
            print('ERROR: Missing .env configuration ' + first_missing_key)
            exit()

    def _get_core_args(self) -> list[dict[str, Any]]:
        return []

    def _get_command_resolvers(self) -> list["AbstractCommandResolver"]:
        return []

    def execute_kernel_command(self, request: CommandRequest):
        print(request.name)
