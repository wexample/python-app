from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AppStdoutOutputHandler(BaseClass):
    """Output handler for app responses that writes to stdout.
    
    This handler is specifically designed for AbstractResponse objects from the app package.
    It calls get_wrapped_printable() to obtain a string representation and writes it to stdout.
    
    Unlike PromptStdoutOutputHandler which handles complex rendering and erasure for interactive
    prompts, this handler simply outputs the response content.
    """

    def print(self, response: AbstractResponse) -> str | None:
        """Print the response to stdout.
        
        Args:
            response: The AbstractResponse to print
            
        Returns:
            The printed string, or None if nothing was printed
        """
        printable = response.get_wrapped_printable()
        
        if printable:
            sys.stdout.write(printable + "\n")
            sys.stdout.flush()
            return printable
        
        return None
