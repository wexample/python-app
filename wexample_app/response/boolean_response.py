from wexample_app.const.types import ResponsePrintable
from wexample_app.response.abstract_response import AbstractResponse


class BooleanResponse(AbstractResponse):
    content: bool

    def get_printable(self) -> ResponsePrintable:
        return 'True' if self.content is True else 'False'
