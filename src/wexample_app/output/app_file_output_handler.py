from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AppFileOutputHandler(AbstractAppOutputHandler):
    """Output handler for app responses that writes to a file.
    
    This handler writes the response content to a specified file path.
    """

    file_path: Path = public_field(
        description="Path to the output file"
    )

    def print(self, response: AbstractResponse) -> str | None:
        """Write the response to a file.
        
        Args:
            response: The AbstractResponse to write
            
        Returns:
            The written string, or None if nothing was written
        """
        printable = response.get_wrapped_printable()
        
        if printable:
            self.file_path.write_text(printable, encoding="utf-8")
            return printable
        
        return None
