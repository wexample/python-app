from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_wex_core.common.command_request import CommandRequest

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

    def _get_file_path(self, request: CommandRequest) -> Path:
        return self.file_path

    def get_target_name(self) -> str:
        """Get the target name for this handler.
        
        Returns:
            'file'
        """
        from wexample_app.const.output import OUTPUT_TARGET_FILE

        return OUTPUT_TARGET_FILE

    def print(self, request: CommandRequest, response: AbstractResponse) -> str | None:
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        """Write the response to a file.
        
        Args:
            response: The AbstractResponse to write
            
        Returns:
            The written string, or None if nothing was written
        """
        printable = response.get_wrapped_printable()

        if printable:
            file_path = self._get_file_path(
                request
            )

            file_path.write_text(printable, encoding="utf-8")
            self.kernel.log(f"Output saved into: {cli_make_clickable_path(file_path)}")
            return printable

        return None
