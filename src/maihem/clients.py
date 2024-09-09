from typing import Dict, Literal, Optional, List, Tuple
from pydantic import ValidationError
import time

from maihem.schemas.agents import AgentTarget, AgentType
from maihem.schemas.tests import Test, TestRun, TestRunWithConversationsNested
from maihem.schemas.conversations import ConversationTurnCreateResponse
from maihem.api_client.maihem_client.models.api_schema_agent_target_create_request import (
    APISchemaAgentTargetCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_test_create_request import (
    APISchemaTestCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_test_create_request_metrics_config import (
    APISchemaTestCreateRequestMetricsConfig,
)
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)
from maihem.api_client.maihem_client.models.conversation_nested_message import (
    ConversationNestedMessage,
)
import maihem.errors as errors
from maihem.api import MaihemHTTPClientSync
from maihem.schemas.tests import TestStatusEnum
from maihem.logger import get_logger
from alive_progress import alive_bar


class Client:
    def create_target_agent(
        self,
        identifier: str,
        role: str,
        industry: str,
        description: str,
    ) -> AgentTarget:
        pass

    def get_target_agent(self, identifier: str) -> AgentTarget:
        # Add implementation here
        raise NotImplementedError("Method not implemented")

    def create_test(
        self,
        test_identifier: str,
        initiating_agent: Literal["maihem", "target"],
        agent_maihem_behavior_prompt: str = None,
        conversation_turns_max: int = 10,
        metrics_config: Dict = None,
    ) -> Test:
        raise NotImplementedError("Method not implemented")

    def run_test(
        self,
        test_identifier: str,
        agent_target: AgentTarget,
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def get_test_run_results(test_run_identifier: str) -> TestRun:
        raise NotImplementedError("Method not implemented")


class MaihemSync(Client):
    _maihem_api_client = MaihemHTTPClientSync
    _base_url = "http://localhost:8000"

    def __init__(self, api_key: str) -> None:
        self._maihem_api_client = MaihemHTTPClientSync(self._base_url, api_key)
        self._logger = get_logger()

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        industry: str,
        description: str,
        name: Optional[str] = None,
    ) -> AgentTarget:
        logger = get_logger()
        logger.info(f"Creating target agent {identifier}...")
        resp = None
        try:
            resp = self._maihem_api_client.create_agent_target(
                req=APISchemaAgentTargetCreateRequest(
                    identifier=identifier,
                    name=name,
                    role=role,
                    industry=industry,
                    description=description,
                )
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        agent_target = None

        try:
            agent_target = AgentTarget.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        logger.info(f"Successfully created target agent {identifier}!")
        return agent_target

    def get_target_agent(self, identifier: str) -> AgentTarget:
        resp = None
        try:
            resp = self._maihem_api_client.get_agent_target_by_identifier(
                identifier=identifier
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        agent_target = None

        try:
            agent_target = AgentTarget.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return agent_target

    def create_test(
        self,
        identifier: str,
        target_agent: AgentTarget,
        initiating_agent: AgentType = AgentType.MAIHEM,
        name: Optional[str] = None,
        maihem_agent_behavior_prompt: str = None,
        conversation_turns_max: int = 10,
        metrics_config: Dict = None,
    ) -> Test:
        resp = None
        logger = get_logger()
        logger.info(f"Creating test {identifier}...")

        if isinstance(initiating_agent, str):
            try:
                initiating_agent = AgentType[initiating_agent.upper()]
            except KeyError as e:
                raise errors.raise_request_validation_error(
                    f"Invalid agent type: {initiating_agent}"
                ) from e

        try:
            metrics_config = APISchemaTestCreateRequestMetricsConfig.from_dict(
                metrics_config
            )
            resp = self._maihem_api_client.create_test(
                req=APISchemaTestCreateRequest(
                    identifier=identifier,
                    agent_target_id=target_agent.id,
                    name=name,
                    initiating_agent=initiating_agent,
                    conversation_turns_max=conversation_turns_max,
                    agent_maihem_behavior_prompt=maihem_agent_behavior_prompt,
                    metrics_config=metrics_config,
                )
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test = None

        try:
            test = Test.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        logger.info(f"Successfull created test {identifier}!")
        return test

    def get_test(self, identifier: str) -> Test:
        resp = None
        try:
            resp = self._maihem_api_client.get_test_by_identifier(identifier=identifier)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test = None

        try:
            test = Test.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test

    def run_test(
        self, test: Test, target_agent: AgentTarget, concurrent_conversations: int = 1
    ) -> TestRun:
        resp = None

        logger = get_logger()
        logger.info(f"Spawning test run for test {test.identifier}...")

        try:
            resp = self._maihem_api_client.create_test_run(
                test_id=test.id,
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run = None

        try:
            test_run = TestRun.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        conversation_ids = resp.conversation_ids
        logger.info(f"Test run spawned for test {test.identifier}!")
        logger.info(
            f"Running test run ({resp.id}) with {len(conversation_ids)} conversations..."
        )
        logger.info(f"Test results endpoint: {test_run.links.test_result}")

        with alive_bar(
            len(conversation_ids),
            title=f"Test run ({test_run.id})",
            unit="convs",
            enrich_print=True,
        ) as progress:
            for conversation_id in conversation_ids:
                self._run_conversation(
                    test_run.id,
                    conversation_id,
                    test=test,
                    target_agent=target_agent,
                    bar_progress=progress,
                )
                time.sleep(2)
                progress()

        logger.info(f"Test run ({test_run.id}) completed!")
        return test_run

    def get_test_run_with_conversations(
        self, test_run_id: str
    ) -> TestRunWithConversationsNested:
        resp = None

        try:
            resp = self._maihem_api_client.get_test_run_with_conversations(test_run_id)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run = None

        try:
            test_run = TestRunWithConversationsNested.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test_run

    def get_conversation(self, conversation_id: str) -> ConversationNested:
        resp = None

        try:
            resp = self._maihem_api_client.get_conversation(conversation_id)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        try:
            conversation = ConversationNested.from_dict(resp.to_dict())
            return conversation
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

    def _run_conversation(
        self,
        test_run_id: str,
        conversation_id: str,
        test: Test,
        target_agent: AgentTarget,
        bar_progress: alive_bar = None,
    ):
        logger = get_logger()
        is_conversation_active = True
        previous_turn_id = None

        cnt = 0
        bar_progress.text(f"Running conversation {conversation_id}...")
        while is_conversation_active and cnt <= 10:
            time.sleep(0.2)
            cnt += 1

            # turn_resp = self._run_conversation_turn(
            #     test_run_id=test_run_id,
            #     conversation_id=conversation_id,
            #     test=test,
            #     target_agent=target_agent,
            #     previous_turn_id=previous_turn_id,
            # )

            # if (
            #     turn_resp.conversation.status != TestStatusEnum.RUNNING
            #     or not turn_resp.turn_id
            # ):
            #     is_conversation_active = False
            #     return conversation_id

            # previous_turn_id = turn_resp.turn_id
        bar_progress.text(f"Conversation completed {conversation_id}!")

        return conversation_id

    def _run_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        test: Test,
        target_agent: AgentTarget,
        previous_turn_id: Optional[str] = None,
    ) -> ConversationTurnCreateResponse:
        agent_maithem_message = None

        conversation = self.get_conversation(conversation_id)

        if (
            test.initiating_agent == AgentType.MAIHEM
            and len(conversation.conversation_turns) == 0
        ):
            turn_resp = self._generate_conversation_turn(
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                target_agent_message=None,
                contexts=[],
            )

            agent_maithem_message = self._get_conversation_message_from_conversation(
                turn_id=turn_resp.turn_id,
                agent_type=AgentType.MAIHEM,
                conversation=turn_resp.conversation,
            )
        elif previous_turn_id is None:
            return ConversationTurnCreateResponse(
                turn_id=None, conversation=conversation
            )
        else:
            agent_maithem_message = self._get_conversation_message_from_conversation(
                turn_id=previous_turn_id,
                agent_type=AgentType.MAIHEM,
                conversation=conversation,
            )

        target_agent_message, contexts = self._send_target_agent_message(
            target_agent,
            conversation_id,
            agent_maihem_message=(
                agent_maithem_message.content if agent_maithem_message else None
            ),
        )

        turn_resp = self._generate_conversation_turn(
            test_run_id=test_run_id,
            conversation_id=conversation_id,
            target_agent_message=target_agent_message,
            contexts=contexts,
        )

        return turn_resp

    def _generate_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        target_agent_message: Optional[str] = None,
        contexts: Optional[List[str]] = None,
    ) -> ConversationTurnCreateResponse:
        try:
            resp = self._maihem_api_client.create_conversation_turns(
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                target_agent_message=target_agent_message,
                contexts=contexts,
            )

            return ConversationTurnCreateResponse(
                turn_id=resp.turn_id,
                conversation=resp.conversation,
            )
        except ValidationError as e:
            errors.handle_schema_validation_error(e)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

    def _get_conversation_message_from_conversation(
        self,
        turn_id: str,
        agent_type: AgentType,
        conversation: ConversationNested,
    ) -> ConversationNestedMessage:
        for turn in conversation.conversation_turns:

            if turn.id == turn_id:
                for message in turn.conversation_messages:
                    if message.agent_type == agent_type:
                        return message

        errors.raise_not_found_error(f"Could not retrieve {agent_type} agent message")

    def _send_target_agent_message(
        self,
        target_agent: AgentTarget,
        conversation_id: str,
        agent_maihem_message: str,
    ) -> Tuple[str, List[str]]:
        target_agent_message, contexts = target_agent._send_message(
            conversation_id, agent_maihem_message
        )

        return target_agent_message, contexts


class MaihemAsync(Client):

    def __init__(self) -> None:
        self.type = "async"

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        company: str,
        industry: str,
        description: str,
    ) -> AgentTarget:
        raise NotImplementedError("Method not implemented")

    def get_target_agent(self, identifier: str) -> AgentTarget:
        raise NotImplementedError("Method not implemented")

    def create_test(
        self,
        test_identifier: str,
        initiating_agent: Literal["maihem", "target"],
        agent_maihem_behavior_prompt: str = None,
        conversation_turns_max: int = 10,
        metrics_config: Dict = None,
    ) -> Test:
        raise NotImplementedError("Method not implemented")

    def run_test(
        self,
        identifier: str,
        test_identifier: str,
        agent_target: AgentTarget,
        dynamic_mode: Literal["static", "dynamic"],
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")
