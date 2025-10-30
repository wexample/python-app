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
        """Get the file path for output.
        
        Can be overridden by subclasses to compute path dynamically.
        
        Args:
            request: The command request
            
        Returns:
            The file path to write to
        """
        return self.file_path

    def get_target_name(self) -> str:
        """Get the target name for this handler.
        
        Returns:
            'file'
        """
        from wexample_app.const.output import OUTPUT_TARGET_FILE

        return OUTPUT_TARGET_FILE

    def print(self, request: CommandRequest, response: AbstractResponse) -> str | None:
        """Write the response to a file.
        
        Overrides parent to use _get_file_path() for dynamic path building.
        
        Args:
            request: The command request containing output format
            response: The AbstractResponse to write
            
        Returns:
            The written string, or None if nothing was written
        """
        from wexample_app.response.null_response import NullResponse

        # Skip null responses
        if isinstance(response, NullResponse):
            return None

        # Get the output format from request
        output_format = request.output_format
        
        # Get formatted output
        formatted = response.get_formatted(output_format=output_format)
        
        # Write to file if there's content
        if formatted:
            return self._write_output(request=request, content=formatted)
        
        return None

    def _write_output(self, request: CommandRequest, content: str) -> str | None:
        """Write the formatted content to a file.
        
        Args:
            request: The command request (for dynamic path building)
            content: The formatted content to write
            
        Returns:
            The written string
        """
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        file_path = self._get_file_path(request)
        file_path.write_text(content, encoding="utf-8")
        self.kernel.io.log(f"Output saved to: {cli_make_clickable_path(file_path)}")
        return content
