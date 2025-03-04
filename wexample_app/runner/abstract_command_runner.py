from pydantic import BaseModel

from wexample_app.common.abstract_kernel_child import AbstractKernelChild


class AbstractCommandRunner(AbstractKernelChild, BaseModel):
    pass
