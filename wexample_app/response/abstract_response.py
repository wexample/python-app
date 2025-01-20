from abc import abstractmethod

from wexample_app.utils.abstract_kernel_child import AbstractKernelChild


class AbstractResponse(AbstractKernelChild):
    @abstractmethod
    def print(self) -> str:
        # For now, simple placeholder.
        pass
