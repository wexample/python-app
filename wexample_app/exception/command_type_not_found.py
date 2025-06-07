from wexample_app.exception.abstract_exception import AbstractException


class CommandTypeNotFound(AbstractException):
    def __init__(self, command_name: str):
        self.command_name = command_name
        super().__init__(message=f"Unable to determine command type for: {command_name}")
