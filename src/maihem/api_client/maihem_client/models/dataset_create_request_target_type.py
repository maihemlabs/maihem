from enum import Enum


class DatasetCreateRequestTargetType(str, Enum):
    WORKFLOW = "workflow"
    WORKFLOW_STEP = "workflow_step"

    def __str__(self) -> str:
        return str(self.value)
