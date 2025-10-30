from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)

if TYPE_CHECKING:
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AbstractAppOutputHandler(HasSnakeShortClassNameClassMixin, BaseClass):
    """Base class for app output handlers.
    
    Output handlers are responsible for processing and displaying AbstractResponse objects.
    Different implementations can write to stdout, files, buffers, or other destinations.
    """

    @abstract_method
    def print(self, response: AbstractResponse) -> str | None:
        """Print or process the response.
        
        Args:
            response: The AbstractResponse to print or process
            
        Returns:
            The printed/processed string, or None if nothing was output
        """
        self._raise_not_implemented_error()

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "OutputHandler"