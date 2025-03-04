from pydantic import BaseModel

from wexample_app.common.abstract_kernel_child import AbstractKernelChild


class CommandRequest(AbstractKernelChild, BaseModel):
    pass
