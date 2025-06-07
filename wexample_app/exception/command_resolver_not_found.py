from wexample_app.exception.abstract_exception import AbstractException


class CommandResolverNotFound(AbstractException):
    def __init__(self, command_type: str):
        self.command_type = command_type
        super().__init__(message=f"No resolver found for command type: {command_type}")
