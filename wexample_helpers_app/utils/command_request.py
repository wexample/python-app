from pydantic import BaseModel


class CommandRequest(BaseModel):
    name: str
    arguments: list[str] = []

    def execute(self) -> None:
        print(self.name)
