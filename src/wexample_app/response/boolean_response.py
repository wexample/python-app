from __future__ import annotations
from wexample_app.response.abstract_response import AbstractResponse
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


class BooleanResponse(AbstractResponse):
    content: bool

    def get_printable(self) -> ResponsePrintable:
        from wexample_helpers.helpers.string import string_render_boolean

        return string_render_boolean(self.content)
