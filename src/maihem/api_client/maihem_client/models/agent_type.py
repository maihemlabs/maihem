from enum import Enum


class AgentType(str, Enum):
    MAIHEM = "maihem"
    TARGET = "target"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
