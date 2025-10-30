from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_app.response.abstract_response import AbstractResponse
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


@base_class
class DictResponse(AbstractResponse):
    """Response containing structured dictionary data."""

    content: dict[str, Any] = public_field(
        description="Dictionary containing structured response data"
    )

    def __attrs_post_init__(self) -> None:
        from wexample_app.exception.response_invalid_content_type_exception import (
            ResponseInvalidContentTypeException,
        )

        self._execute_super_attrs_post_init_if_exists()

        if not isinstance(self.content, dict):
            raise ResponseInvalidContentTypeException(
                content=self.content, allowed_content_types=[dict]
            )

    def get_printable(self) -> ResponsePrintable:
        return str(self.content)
