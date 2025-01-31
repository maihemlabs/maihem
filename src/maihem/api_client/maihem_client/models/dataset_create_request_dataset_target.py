from enum import Enum


class DatasetCreateRequestDatasetTarget(str, Enum):
    CONVERSATION = "conversation"
    WORKFLOW_STEP = "workflow_step"

    def __str__(self) -> str:
        return str(self.value)
