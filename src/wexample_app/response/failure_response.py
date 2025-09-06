from __future__ import annotations

from typing import TYPE_CHECKING, Any
from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    pass
    from wexample_app.const.types import ResponsePrintable


class FailureResponse(AbstractResponse):
    exception: Any | None = None
    message: str | None = None

    def get_printable(self) -> ResponsePrintable:
        # Build a string representation from exception and/or message
        if self.exception and self.message:
            return f"{self.message}: {str(self.exception)}"
        elif self.exception:
            return str(self.exception)
        elif self.message:
            return self.message
        else:
            return "Unknown failure"
