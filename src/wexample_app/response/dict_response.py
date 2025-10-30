from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_app.response.abstract_response import AbstractResponse
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


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

    def get_formatted(self, output_format: str) -> str:
        """Get the formatted dict response according to the specified format.
        
        Args:
            output_format: The desired output format (str, json, yaml, etc.)
            
        Returns:
            The formatted response as a string
        """
        from wexample_app.const.output import (
            OUTPUT_FORMAT_JSON,
            OUTPUT_FORMAT_STR,
            OUTPUT_FORMAT_YAML,
        )

        if output_format == OUTPUT_FORMAT_JSON:
            import json
            return json.dumps(self.content, indent=2)
        
        elif output_format == OUTPUT_FORMAT_YAML:
            import yaml
            return yaml.dump(self.content, default_flow_style=False)
        
        elif output_format == OUTPUT_FORMAT_STR:
            # Use io.properties() for structured display, then capture the output
            from wexample_prompt.responses.data.properties_prompt_response import (
                PropertiesPromptResponse,
            )
            
            prompt_response = PropertiesPromptResponse.create_properties(
                properties=self.content,
                title="Response",
            )
            
            # Print via kernel io and return empty string (io already printed)
            if self.kernel and self.kernel.io:
                self.kernel.io.print_response(response=prompt_response)
                return ""
            
            # Fallback if no kernel
            return str(self.content)
        
        else:
            # Unknown format, fallback to string representation
            return str(self.content)
