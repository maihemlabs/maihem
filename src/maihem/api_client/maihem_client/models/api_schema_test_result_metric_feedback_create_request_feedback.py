from enum import Enum


class APISchemaTestResultMetricFeedbackCreateRequestFeedback(str, Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive"

    def __str__(self) -> str:
        return str(self.value)
