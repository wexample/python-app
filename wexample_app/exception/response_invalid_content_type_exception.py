from typing import Any, Optional, List, Type

from wexample_app.exception.abstract_exception import AbstractException, ExceptionData


class ResponseInvalidContentData(ExceptionData):
    """Data model for ResponseInvalidContent exception."""
    content_type: str
    content_value: str


class ResponseInvalidContentTypeException(AbstractException):
    """Exception raised when a response contains invalid content that cannot be properly processed."""
    error_code: str = "RESPONSE_INVALID_CONTENT"

    def __init__(
            self,
            content: Any,
            allowed_content_types: List[Type],
            cause: Optional[Exception] = None,
            previous: Optional[Exception] = None,
    ):
        # Create structured data using Pydantic model
        content_type = type(content).__name__
        # Convert to string but limit length to avoid huge error messages
        content_str = str(content)
        if len(content_str) > 100:
            content_str = content_str[:97] + "..."

        data_model = ResponseInvalidContentData(
            content_type=content_type,
            content_value=content_str
        )

        # Store content info as instance attributes
        self.content_type = content_type
        self.content_value = content_str
        
        # Format the allowed types for the error message
        allowed_types_str = ", ".join([t.__name__ for t in allowed_content_types])

        super().__init__(
            message=f"Response contains invalid content of type '{content_type}'. Expected one of: {allowed_types_str}.",
            data=data_model.model_dump(),
            cause=cause,
            previous=previous
        )
