from pydantic import BaseModel


class KernelCommandRequest(BaseModel):
    name: str
    arguments: list[str] = []
