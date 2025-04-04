from typing import Any

from wexample_app.response.abstract_response import AbstractResponse


class DefaultResponse(AbstractResponse):
    content: Any

    def print(self) -> str:
        # For now consider every output as a string
        return str(self.content)
