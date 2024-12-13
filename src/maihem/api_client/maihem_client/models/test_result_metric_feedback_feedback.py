from enum import Enum


class TestResultMetricFeedbackFeedback(str, Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive"

    def __str__(self) -> str:
        return str(self.value)
