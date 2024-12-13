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
    ERROR = "error"
    CANCELED = "canceled"


class TestResultEnum(str, Enum):
    PASSED = "passed"
    FAILED = "failed"


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
    name: str
    agent_target_id: str
    label: Optional[str] = None
    initiating_agent: AgentType = AgentType.MAIHEM
    conversation_turns_max: Optional[int] = None
    agent_maihem_behavior_prompt: Optional[str] = None
    agent_maihem_goal_prompt: Optional[str] = None
    agent_maihem_population_prompt: Optional[str] = None
    metrics_config: Dict[str, int] = {}


class TestRun(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    test_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TestStatusEnum
    result: Optional[TestResultEnum] = None
    links: Optional[APISchemaLinks] = None

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class TestRunConversations(TestRun):
    conversation_ids: List[str] = []

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class ConversationScores(BaseModel):
    total_conversations: int
    total_score: Optional[float] = None
    result_passed: int
    result_failed: int
    status_completed: int
    status_error: int
    status_running: int
    status_pending: int
    status_paused: int


class TestRunResultMetricScore(ConversationScores):
    result: Optional[TestResultEnum] = None
    status: TestStatusEnum


class TestRunResultMetrics(TestRun):
    conversation_scores: ConversationScores
    metric_scores: Dict[str, TestRunResultMetricScore]


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


class ResultEvaluation(BaseModel):
    criteria: str
    is_failure: bool
    explanation: Optional[str] = None

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class ResultConversationMessage(BaseModel):
    role: str
    content: str
    failed_evaluations: Optional[List[ResultEvaluation]] = None

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class ResultConversation(BaseModel):
    messages: List[ResultConversationMessage]
    failed_evaluations: Optional[List[ResultEvaluation]] = None

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)


class ResultTestRun(BaseModel):
    result: Optional[TestResultEnum] = None
    score: Optional[float] = None
    conversations: Optional[List[ResultConversation]] = None
    id: Optional[str] = None

    def __str__(self):
        return json.dumps(self.model_dump(), default=str, indent=4)

    def __init__(self, test_run_api: TestRunResultConversations):
        super().__init__()

        conversations = []
        for conv in test_run_api.conversations:
            messages = []
            for turn in conv.conversation_turns:
                for msg in turn.conversation_messages:
                    evaluations_msg = []
                    for evl in msg.evaluations:
                        is_failure = evl.result.value == "failed"
                        if is_failure:
                            evaluation_msg = ResultEvaluation(
                                criteria=evl.criteria,
                                is_failure=is_failure,
                                explanation=evl.explanation,
                            )
                            evaluations_msg.append(evaluation_msg)

                    message = ResultConversationMessage(
                        role=msg.agent_type.value,
                        content=msg.content,
                        failed_evaluations=evaluations_msg,
                    )
                    messages.append(message)

            evaluations = []
            for evl in conv.evaluations:
                is_failure = evl.result.value == "failed"
                if is_failure:
                    evaluation = ResultEvaluation(
                        criteria=evl.criteria,
                        is_failure=is_failure,
                        explanation=evl.explanation,
                    )
                    evaluations.append(evaluation)

            conversation = ResultConversation(
                messages=messages, failed_evaluations=evaluations
            )
            conversations.append(conversation)

        self.id = test_run_api.id
        self.result = test_run_api.result
        self.score = test_run_api.result_score
        self.conversations = conversations


# class SimulatedConversation:
#     """
#     Class with the response messages and evaluation from a simulated conversation

#     messages: List[Dict[str, str]] - List of messages from the conversation
#     evaluation: str - Explanation of the evaluation of the conversation
#     """

#     def __init__(self, conversation: TestRunResultConversations, conv_num: int = 0):
#         self.conv_num = conv_num
#         try:
#             self.messages = self._convert_conv_to_message_list(conversation)
#         except Exception as e:
#             self.messages = None
#         try:
#             self.evaluation = (
#                 conversation.conversations[conv_num].evaluations[0].explanation
#             )
#         except Exception as e:
#             self.evaluation = None

#     def _convert_conv_to_message_list(self, conversation: TestRunResultConversations):
#         conv = conversation.conversations[self.conv_num]
#         message_list = []

#         for turn in conv.conversation_turns:
#             for message in turn.conversation_messages:
#                 message_list.append({message.agent_type.value: message.content})

#         return message_list
