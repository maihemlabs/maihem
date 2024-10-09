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
    CANCELED = "canceled"


class TestResultEnum(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    ERRORED = "errored"
    CANCELED = "canceled"


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
    agent_target_id: str
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


class SimulatedConversation:
    """
    Class with the response messages and evaluation from a simulated conversation
    """
    
    def __init__(self, conversation: TestRunResultConversations, conv_num: int = 0):
        self.conv_num = conv_num
        try:
            self.messages = self._convert_conv_to_message_list(conversation)
        except Exception as e:
            self.messages = None
        try:
            self.evaluation = conversation.conversations[conv_num].evaluations[0].explanation
        except Exception as e:
            self.evaluation = None
    
    def _convert_conv_to_message_list(self, conversation: TestRunResultConversations):
        conv = conversation.conversations[self.conv_num]
        message_list = []

        for turn in conv.conversation_turns:
            for message in turn.conversation_messages:
                message_list.append({message.agent_type.value: message.content})

        return message_list
