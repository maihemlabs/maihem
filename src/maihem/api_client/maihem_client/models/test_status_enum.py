from enum import Enum


class TestStatusEnum(str, Enum):
    CANCELED = "canceled"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
