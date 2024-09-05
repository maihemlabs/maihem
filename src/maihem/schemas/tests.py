from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from maihem.schemas.agents import AgentType
from enum import Enum


class TestStatusEnum(str, Enum):
    PAUSED = "paused"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TestResultEnum(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    ERRORED = "errored"
    CANCELLED = "cancelled"


class APISchemaLinks(BaseModel):
    test_result: Optional[str] = None
    test_result_conversations: Optional[str] = None

    class Config:
        exclude_none = True


class Test(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    identifier: str
    name: Optional[str] = None
    agent_target_id: str
    initiating_agent: AgentType = AgentType.MAIHEM
    agent_maihem_behavior_prompt: Optional[str] = None
    metrics: List[str]
    conversations_per_metric: Optional[int] = 5


class TestRun(BaseModel):
    test_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TestStatusEnum
    result: TestResultEnum
    conversation_ids: List[str] = []
    links: Optional[APISchemaLinks] = None


class TestRunResults:
    def __init__(self):
        pass
