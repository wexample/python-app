from typing import Optional

from wexample_app.exception.abstract_exception import AbstractException, ExceptionData


class CommandFileNotFoundData(ExceptionData):
    """Data model for CommandFileNotFound exception."""
    file_path: str


class CommandFileNotFoundException(AbstractException):
    """Exception raised when a command file cannot be found at the specified path."""
    error_code: str = "COMMAND_FILE_NOT_FOUND"

    def __init__(self, file_path: str, cause: Optional[Exception] = None):
        # Create structured data using Pydantic model
        data_model = CommandFileNotFoundData(file_path=file_path)

        # Store file_path as instance attribute for backward compatibility
        self.file_path = file_path

        super().__init__(
            message=f"Command file not found at path: {file_path}",
            data=data_model.model_dump(),
            cause=cause
        )
