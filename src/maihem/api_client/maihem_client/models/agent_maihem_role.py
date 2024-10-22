from enum import Enum


class AgentMaihemRole(str, Enum):
    QA = "qa"
    SAFETY = "safety"
    SEC = "sec"

    def __str__(self) -> str:
        return str(self.value)
