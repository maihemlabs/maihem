from enum import Enum


class TestResultEnum(str, Enum):
    FAILED = "failed"
    PASSED = "passed"

    def __str__(self) -> str:
        return str(self.value)
