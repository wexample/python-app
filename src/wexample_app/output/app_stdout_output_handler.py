from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)
from wexample_helpers.decorator.base_class import base_class
from wexample_wex_core.common.command_request import CommandRequest

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

    def get_target_name(self) -> str:
        """Get the target name for this handler.
        
        Returns:
            'stdout'
        """
        from wexample_app.const.output import OUTPUT_TARGET_STDOUT
        
        return OUTPUT_TARGET_STDOUT

    def print(self, request: CommandRequest, response: AbstractResponse) -> str | None:
        """Print the response to stdout with appropriate rendering.
        
        Args:
            response: The AbstractResponse to print
            
        Returns:
            The printed string, or None if nothing was printed
        """
        from wexample_app.response.null_response import NullResponse

        # Skip null responses
        if isinstance(response, NullResponse):
            return None

        from wexample_app.const.output import OUTPUT_FORMAT_STR

        # Get the output format from kernel's root request
        output_format = OUTPUT_FORMAT_STR
        if self.kernel and self.kernel.root_request:
            output_format = self.kernel.root_request.output_format or OUTPUT_FORMAT_STR
        
        # Get formatted output (response handles io.print internally if needed)
        formatted = response.get_formatted(output_format=output_format)
        
        # Write to stdout if there's content
        if formatted:
            sys.stdout.write(formatted + "\n")
            sys.stdout.flush()
            return formatted
        
        return None
