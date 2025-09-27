from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class CommandTypeNotFoundException(UndefinedException):
    """Exception raised when the system cannot determine the type of a command."""

    error_code: str = "COMMAND_TYPE_NOT_FOUND"

    def __init__(
        self,
        command_name: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        # Store command_name as instance attribute
        self.command_name = command_name

        super().__init__(
            message=f"Unable to determine command type for: {command_name}",
            data={"command_name": command_name},
            cause=cause,
            previous=previous,
        )
