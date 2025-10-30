from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.decorator.base_class import base_class
from wexample_wex_core.common.command_request import CommandRequest

if TYPE_CHECKING:
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AbstractAppOutputHandler(AbstractKernelChild):
    """Base class for app output handlers.
    
    Output handlers are responsible for processing and displaying AbstractResponse objects.
    Different implementations can write to stdout, files, buffers, or other destinations.
    """

    @abstract_method
    def get_target_name(self) -> str:
        """Get the name of this output target.
        
        Returns:
            The target name (e.g., 'stdout', 'file')
        """
        self._raise_not_implemented_error()

    @abstract_method
    def print(self, request: CommandRequest, response: AbstractResponse) -> str | None:
        """Print or process the response.
        
        Args:
            response: The AbstractResponse to print or process
            
        Returns:
            The printed/processed string, or None if nothing was output
        """
        self._raise_not_implemented_error()