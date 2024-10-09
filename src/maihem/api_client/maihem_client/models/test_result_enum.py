from enum import Enum


class TestResultEnum(str, Enum):
    CANCELED = "canceled"
    ERRORED = "errored"
    FAILED = "failed"
    PASSED = "passed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
