from abc import abstractmethod

from wexample_helpers_app.utils.abstract_kernel_child import AbsractKernelChild


class AbstractCommandResolver(AbsractKernelChild):
    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass
