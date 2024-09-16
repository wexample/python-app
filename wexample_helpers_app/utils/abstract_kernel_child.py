from typing import Any

from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers_app.utils.abstract_kernel import AbstractKernel


class AbsractKernelChild(BaseModel):
    kernel: "AbstractKernel"

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)