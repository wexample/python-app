from typing import Any, TYPE_CHECKING, List

from wexample_app.const.types import ResponsePrintable
from wexample_app.exception.response_invalid_content_type_exception import ResponseInvalidContentTypeException
from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel


class MultipleResponse(AbstractResponse):
    content: List[Any] = []

    def __init__(self, kernel: "AbstractKernel", **kwargs) -> None:
        super().__init__(kernel, **kwargs)

        if not isinstance(self.content, list):
            raise ResponseInvalidContentTypeException(content=self.content, allowed_content_types=[list])

    def get_printable(self) -> ResponsePrintable:
        # For now consider every output as a string
        return str(self.content)
