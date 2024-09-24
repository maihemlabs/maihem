from typing import List, Optional, Dict
import json
from pydantic import BaseModel
from datetime import datetime
from maihem.schemas.agents import AgentType
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)
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
    test_conversations: Optional[str] = None
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
    initiating_agent: AgentType = AgentType.MAIHEM
    conversation_turns_max: Optional[int] = None
    agent_maihem_behavior_prompt: Optional[str] = None
    metrics_config: Dict[str, int] = {}


class TestRun(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    test_id: str
    agent_target_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TestStatusEnum
    result: TestResultEnum
    links: Optional[APISchemaLinks] = None

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class TestRunConversations(TestRun):
    conversation_ids: List[str] = []

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class TestRunResultMetricScore(BaseModel):
    total: int
    passed: int
    failed: int
    errored: int


class ConversationCounts(BaseModel):
    total_conversations: int
    result_passed: int
    result_failed: int
    result_errored: int
    result_pending: int
    result_cancelled: int
    status_completed: int
    status_failed: int
    status_running: int
    status_pending: int
    status_paused: int
    total_score: Optional[float] = None


class TestRunResultMetrics(TestRun):
    conversation_counts: ConversationCounts
    metric_scores: Dict[str, TestRunResultMetricScore] = {}


class TestRunResultConversations(TestRun):
    conversations: List[ConversationNested] = []

    def __str__(self):
        test_run_dict = self.model_dump()
        conversation_jsons = [
            conversation.to_dict() for conversation in self.conversations
        ]
        test_run_dict["conversations"] = conversation_jsons

        return json.dumps(test_run_dict, default=str, indent=4)

    def to_json(self):
        return self.__str__()

    def to_dict(self):
        test_run_dict = self.model_dump()
        conversation_jsons = [
            conversation.to_dict() for conversation in self.conversations
        ]
        test_run_dict["conversations"] = conversation_jsons

        return test_run_dict

    class Config:
        arbitrary_types_allowed = True
