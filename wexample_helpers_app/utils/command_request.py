from pydantic import BaseModel


class CommandRequest(BaseModel):
    name: str
    arguments: list[str] = []
