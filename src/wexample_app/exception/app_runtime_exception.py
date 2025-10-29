from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class AppRuntimeException(UndefinedException):
    """Base exception for expected runtime errors in the application.
    
    This exception class is used for errors that are part of normal application
    flow and should not display a full traceback. These are business logic errors
    that should be handled gracefully and displayed to the user in a friendly way.
    
    Examples include:
    - Command not found
    - Invalid configuration
    - Missing required resources
    
    Subclasses of this exception can be caught specifically to provide
    custom error handling without showing technical stack traces.
    """

    error_code: str = "APP_RUNTIME_ERROR"
