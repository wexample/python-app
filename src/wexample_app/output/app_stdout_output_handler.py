from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AppStdoutOutputHandler(AbstractAppOutputHandler):
    """Output handler for app responses that writes to stdout.
    
    This handler is specifically designed for AbstractResponse objects from the app package.
    It detects the response type and uses appropriate rendering:
    - DictResponse: renders via io.properties() for structured display
    - Other responses: uses get_wrapped_printable() for simple string output
    """

    def print(self, response: AbstractResponse) -> str | None:
        """Print the response to stdout with appropriate rendering.
        
        Args:
            response: The AbstractResponse to print
            
        Returns:
            The printed string, or None if nothing was printed
        """
        from wexample_app.response.dict_response import DictResponse
        from wexample_app.response.null_response import NullResponse

        # Skip null responses
        if isinstance(response, NullResponse):
            return None

        # Special rendering for DictResponse
        if isinstance(response, DictResponse):
            if self.kernel and self.kernel.io:
                self.kernel.io.properties(
                    properties=response.content,
                    title="Response"
                )
                return str(response.content)
        
        # Default: simple string output
        printable = response.get_wrapped_printable()
        
        if printable:
            sys.stdout.write(printable + "\n")
            sys.stdout.flush()
            return printable
        
        return None
