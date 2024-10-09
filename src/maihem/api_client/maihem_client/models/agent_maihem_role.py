from enum import Enum


class AgentMaihemRole(str, Enum):
    QA = "qa"
    SEC = "sec"
    SAFETY = "safety"

    def __str__(self) -> str:
        return str(self.value)
