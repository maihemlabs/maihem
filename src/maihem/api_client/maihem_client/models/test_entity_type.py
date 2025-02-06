from enum import Enum


class TestEntityType(str, Enum):
    WORKFLOW = "workflow"
    WORKFLOW_STEP = "workflow_step"

    def __str__(self) -> str:
        return str(self.value)
