from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from typing import Dict, Literal, Optional, List, Tuple
from pydantic import ValidationError
import random
from tqdm import tqdm
from yaspin import yaspin
from yaspin.spinners import Spinners

from maihem.schemas.agents import TargetAgent, AgentType
from maihem.schemas.tests import (
    Test,
    TestRun,
    TestRunResultConversations,
    TestRunResultMetrics,
    TestRunConversations,
)
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
from maihem.utils import TextSplitter, extract_text


class Client:
    _base_url: str = "https://api.maihem.ai"
    _base_url_ui: str = "https://cause.maihem.ai"
    _api_key: str = None

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        industry: str,
        description: str,
    ) -> TargetAgent:
        pass

    def get_target_agent(self, identifier: str) -> TargetAgent:
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

    def create_test_run(
        self,
        test_identifier: str,
        agent_target: TargetAgent,
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def get_test_run_result(test_run_id: str) -> TestRun:
        raise NotImplementedError("Method not implemented")


class Maihem(Client):
    _maihem_api_client = MaihemHTTPClientSync

    def __init__(self, api_key: Optional[str] = None) -> None:
        self._api_key = api_key or os.getenv("MAIHEM_API_KEY")

        if not self._api_key:
            raise errors.raise_request_validation_error(
                "API key is required to initialize Maihem client"
            )

        self._maihem_api_client = MaihemHTTPClientSync(self._base_url, self._api_key)
        self._logger = get_logger()

    def _override_base_url(self, base_url: str) -> None:
        self._base_url = base_url
        self._maihem_api_client = MaihemHTTPClientSync(self._base_url, self._api_key)

    def _override_base_url_ui(self, base_url_ui: str) -> None:
        self._base_url_ui = base_url_ui

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        industry: str,
        description: str,
        name: Optional[str] = None,
        language: Optional[str] = "en",
    ) -> TargetAgent:
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
                    language=language,
                )
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        agent_target = None

        try:
            agent_target = TargetAgent.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        logger.info(f"Successfully created target agent {identifier}!")
        return agent_target

    def upsert_target_agent(
        self,
        identifier: str,
        role: str,
        industry: str,
        description: str,
        name: Optional[str] = None,
        language: Optional[str] = "en",
    ) -> TargetAgent:
        logger = get_logger()
        logger.info(f"Creating target agent {identifier}...")
        resp = None
        try:
            resp = self._maihem_api_client.upsert_agent_target(
                req=APISchemaAgentTargetCreateRequest(
                    identifier=identifier,
                    name=name,
                    role=role,
                    industry=industry,
                    description=description,
                    language=language,
                )
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        agent_target = None

        try:
            agent_target = TargetAgent.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        logger.info(f"Successfully created target agent {identifier}!")
        return agent_target

    def get_target_agent(self, identifier: str) -> TargetAgent:
        resp = None
        try:
            resp = self._maihem_api_client.get_agent_target_by_identifier(
                identifier=identifier
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        agent_target = None

        try:
            agent_target = TargetAgent.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return agent_target

    def create_test(
        self,
        identifier: str,
        target_agent_identifier: str,
        initiating_agent: AgentType = AgentType.MAIHEM,
        name: Optional[str] = None,
        maihem_agent_behavior_prompt: Optional[str] = None,
        conversation_turns_max: Optional[int] = 10,
        metrics_config: Optional[Dict] = None,
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
            target_agent = self._maihem_api_client.get_agent_target_by_identifier(
                identifier=target_agent_identifier
            )

            if not target_agent:
                raise errors.raise_not_found_error(
                    f"Target agent {target_agent_identifier} not found"
                )

            metrics_config = APISchemaTestCreateRequestMetricsConfig.from_dict(
                metrics_config
            )
            resp = self._maihem_api_client.create_test(
                req=APISchemaTestCreateRequest(
                    identifier=identifier,
                    name=name,
                    initiating_agent=initiating_agent,
                    conversation_turns_max=conversation_turns_max,
                    agent_target_id=target_agent.id,
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

    def upsert_test(
        self,
        identifier: str,
        target_agent_identifier: str,
        initiating_agent: AgentType = AgentType.MAIHEM,
        name: Optional[str] = None,
        maihem_agent_behavior_prompt: Optional[str] = None,
        conversation_turns_max: Optional[int] = 10,
        metrics_config: Optional[Dict] = None,
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
            target_agent = self._maihem_api_client.get_agent_target_by_identifier(
                identifier=target_agent_identifier
            )
            metrics_config = APISchemaTestCreateRequestMetricsConfig.from_dict(
                metrics_config
            )
            resp = self._maihem_api_client.upsert_test(
                req=APISchemaTestCreateRequest(
                    identifier=identifier,
                    name=name,
                    initiating_agent=initiating_agent,
                    conversation_turns_max=conversation_turns_max,
                    agent_target_id=target_agent.id,
                    agent_maihem_behavior_prompt=maihem_agent_behavior_prompt,
                    metrics_config=metrics_config,
                    is_dev_mode=True,
                )
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test = None

        try:
            test = Test.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

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

    def create_test_run(
        self,
        test_identifier: str,
        target_agent: TargetAgent,
        concurrent_conversations: int = 1,
    ) -> TestRun:
        try:
            test = self._maihem_api_client.get_test_by_identifier(test_identifier)

            resp = None

            logger = get_logger()
            logger.info(f"Spawning test run for test {test.identifier}...")

            try:
                with yaspin(
                    Spinners.arc,
                    text="Creating Maihem Agents, this might take a minute...",
                ) as sp:
                    resp = self._maihem_api_client.create_test_run(test_id=test.id)
            except errors.ErrorBase as e:
                errors.handle_base_error(e)

            test_run = None

            try:
                test_run = TestRun.model_validate(resp.to_dict())
            except ValidationError as e:
                errors.handle_schema_validation_error(e)

            test_run_conversations = self.get_test_run_conversations(test_run.id)
            conversation_ids = test_run_conversations.conversation_ids

            logger.info(f"Test run spawned for test {test.identifier}!")
            print("\n" + "-" * 50 + "\n")
            logger.info(
                f"Running test run with {len(conversation_ids)} conversations (up to {concurrent_conversations} concurrently)..."
            )
            logger.info(f"Test run ID: {test_run.id}")
            logger.info(
                f"Test run results (UI): {self._base_url_ui}/evaluations/{test_run.id}"
            )

            print("\n" + "-" * 50 + "\n")

            with tqdm(
                len(conversation_ids),
                total=len(conversation_ids),
                unit="conversation",
                colour="green",
                desc=f"Test run ({test_run.id})",
                position=0,
            ) as progress:
                with ThreadPoolExecutor(
                    max_workers=concurrent_conversations
                ) as executor:
                    future_to_conversation_id = {
                        executor.submit(
                            self._run_conversation,
                            test_run.id,
                            conversation_id,
                            test,
                            target_agent,
                            progress_bar_position=i + 1,
                        ): conversation_id
                        for i, conversation_id in enumerate(conversation_ids)
                    }

                    for future in as_completed(future_to_conversation_id):
                        conversation_id = future_to_conversation_id[future]
                        try:
                            future.result()
                        except errors.ErrorBase as e:
                            logger.error(
                                f"Error running conversation ({conversation_id}): {e.message}"
                            )
                            progress.colour = "red"
                        finally:
                            progress.update()

            print("\n" + "-" * 50 + "\n")
            logger.info(f"Test run ({test_run.id}) completed!")
            return test_run
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Canceling test...")
            self._maihem_api_client.update_test_run_status(
                test_run_id=test_run.id, status=TestStatusEnum.CANCELED
            )
            logger.info("Test run canceled!")
        except Exception as e:
            logger.error(f"Error: {e}. Ending test...")
            self._maihem_api_client.update_test_run_status(
                test_run_id=test_run.id, status=TestStatusEnum.FAILED
            )

    def create_test_run_dev_mode(
        self,
        test_identifier: str,
        target_agent: TargetAgent,
        concurrent_conversations: int = 1,
    ) -> TestRun:
        try:
            if not target_agent._chat_function:
                errors.raise_request_validation_error(
                    "Chat function the target agent must be passed."
                )

            test = self._maihem_api_client.get_test_by_identifier(test_identifier)

            resp = None

            logger = get_logger()

            try:
                with yaspin(
                    Spinners.arc,
                    text="Creating Maihem Agent, this might take a minute...",
                ) as sp:
                    resp = self._maihem_api_client.create_test_run(test_id=test.id)
            except errors.ErrorBase as e:
                errors.handle_base_error(e)

            test_run = None

            try:
                test_run = TestRun.model_validate(resp.to_dict())
            except ValidationError as e:
                errors.handle_schema_validation_error(e)

            test_run_conversations = self.get_test_run_conversations(test_run.id)
            conversation_ids = test_run_conversations.conversation_ids

            # logger.info(
            #     f"Test run results (UI): {self._base_url_ui}/evaluations/{test_run.id}"
            # )

            # with tqdm(
            #     len(conversation_ids),
            #     total=len(conversation_ids),
            #     unit="conversation",
            #     colour="green",
            #     desc=f"Test run ({test_run.id})",
            #     position=0,
            # ) as progress:
            with ThreadPoolExecutor(max_workers=concurrent_conversations) as executor:
                future_to_conversation_id = {
                    executor.submit(
                        self._run_conversation,
                        test_run.id,
                        conversation_id,
                        test,
                        target_agent,
                        progress_bar_position=i + 1,
                    ): conversation_id
                    for i, conversation_id in enumerate(conversation_ids)
                }

                for future in as_completed(future_to_conversation_id):
                    conversation_id = future_to_conversation_id[future]
                    try:
                        future.result()
                    except errors.ErrorBase as e:
                        logger.error(
                            f"Error running conversation ({conversation_id}): {e.message}"
                        )
                        # progress.colour = "red"
                    # finally:
                    # progress.update()

            print("\n" + "-" * 50 + "\n")
            logger.info(f"Conversation ({test_run.id}) completed!")
            return test_run
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Canceling test...")
            self._maihem_api_client.update_test_run_status(
                test_run_id=test_run.id, status=TestStatusEnum.CANCELED
            )
            logger.info("Test run canceled!")
        except Exception as e:
            logger.error(f"Error: {e}. Ending test...")
            self._maihem_api_client.update_test_run_status(
                test_run_id=test_run.id, status=TestStatusEnum.FAILED
            )

    def get_test_run_conversations(self, test_run_id: str) -> TestRunConversations:
        resp = None

        try:
            resp = self._maihem_api_client.get_test_run_conversations(test_run_id)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run = None

        try:
            test_run = TestRunConversations.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test_run

    def get_test_run_result(self, test_run_id: str) -> TestRunResultMetrics:
        resp = None

        try:
            resp = self._maihem_api_client.get_test_run_result(test_run_id)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run = None

        try:
            test_run = TestRunResultMetrics.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test_run

    def get_test_run_result_conversations(
        self, test_run_id: str
    ) -> TestRunResultConversations:
        resp = None

        try:
            resp = self._maihem_api_client.get_test_run_result_conversations(
                test_run_id
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run = None

        try:
            resp_conversations = resp.conversations
            resp_dict = resp.to_dict()
            resp_dict["conversations"] = []

            conversation_nesteds: ConversationNested = []
            for conv in resp_conversations:
                conv_dict = conv.to_dict()
                try:
                    conv = ConversationNested.from_dict(conv_dict)
                    conversation_nesteds.append(conv)
                except ValidationError as e:
                    errors.handle_schema_validation_error(e)

            test_run = TestRunResultConversations.model_validate(resp_dict)
            test_run.conversations = conversation_nesteds
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
        target_agent: TargetAgent,
        progress_bar_position: int,
    ) -> str:
        is_conversation_active = True
        previous_turn_id = None
        turn_cnt = 0

        progress = tqdm(
            total=test.conversation_turns_max,
            desc=f"Conversation ({conversation_id})",
            unit="turn",
            position=progress_bar_position,
            leave=False,
        )
        while is_conversation_active:
            turn_cnt += 1
            progress.update()
            turn_resp = self._run_conversation_turn(
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                test=test,
                target_agent=target_agent,
                previous_turn_id=previous_turn_id,
            )

            if (
                turn_resp.conversation.status != TestStatusEnum.RUNNING
                or not turn_resp.turn_id
            ):
                is_conversation_active = False
                progress.total = turn_cnt
                progress.n = turn_cnt
                progress.refresh()
                progress.close()
                return conversation_id

            previous_turn_id = turn_resp.turn_id

        return conversation_id

    def _run_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        test: Test,
        target_agent: TargetAgent,
        previous_turn_id: Optional[str] = None,
    ) -> ConversationTurnCreateResponse:
        agent_maihem_message = None

        conversation = self.get_conversation(conversation_id)

        document_key = None
        text = None

        logger = get_logger()

        # Document loading and chunking (for RAG)
        if target_agent.document_paths:
            max_attempts = 10
            attempts = 0
            while attempts < max_attempts:
                if not target_agent.document_paths:
                    break
                document_path = random.choice(list(target_agent.document_paths))
                document_key = os.path.basename(document_path)
                try:
                    document = extract_text(document_path)
                    if len(document) > 10000:
                        chunks = TextSplitter(
                            chunk_size=5000, chunk_overlap=200
                        ).split_text(document)
                        text = random.choice(chunks)
                    else:
                        text = document
                    if text.strip():
                        break
                except Exception as e:
                    logger.warning(
                        f"Error processing document {document_key}: {str(e)}"
                    )
                attempts += 1

            if attempts == max_attempts:
                logger.warning(
                    "Max attempts reached while trying to select a valid document chunk."
                )

        if (
            test.initiating_agent == AgentType.MAIHEM
            and len(conversation.conversation_turns) == 0
        ):

            turn_resp = self._generate_conversation_turn(
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                target_agent_message=None,
                contexts=[],
                document={document_key: text} if document_key else None,
            )

            agent_maihem_message = self._get_conversation_message_from_conversation(
                turn_id=turn_resp.turn_id,
                agent_type=AgentType.MAIHEM,
                conversation=turn_resp.conversation,
            )
        elif previous_turn_id is None and len(conversation.conversation_turns) > 0:
            return ConversationTurnCreateResponse(
                turn_id=None, conversation=conversation
            )
        elif previous_turn_id is not None and len(conversation.conversation_turns) > 0:
            agent_maihem_message = self._get_conversation_message_from_conversation(
                turn_id=previous_turn_id,
                agent_type=AgentType.MAIHEM,
                conversation=conversation,
            )

        try:
            target_agent_message, contexts = self._send_target_agent_message(
                target_agent,
                conversation_id,
                agent_maihem_message=(
                    agent_maihem_message.content if agent_maihem_message else None
                ),
            )
        except Exception as e:
            errors.raise_chat_function_error(
                f"Error sending message to target agent: {e}"
            )

        if contexts != []:
            contexts_concat = "\n".join(contexts)
            if len(contexts_concat) > 20000:
                errors.raise_chat_function_error(
                    "Length of all contexts combined should not exceed 20,000 characters"
                )

        turn_resp = self._generate_conversation_turn(
            test_run_id=test_run_id,
            conversation_id=conversation_id,
            target_agent_message=target_agent_message,
            contexts=contexts,
            document={document_key: text} if document_key else None,
        )

        return turn_resp

    def _generate_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        target_agent_message: Optional[str] = None,
        contexts: Optional[List[str]] = None,
        document: Optional[Dict] = None,
    ) -> ConversationTurnCreateResponse:
        try:
            resp = self._maihem_api_client.create_conversation_turn(
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                target_agent_message=target_agent_message,
                contexts=contexts,
                document=document,
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
        target_agent: TargetAgent,
        conversation_id: str,
        agent_maihem_message: Optional[str] = None,
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
    ) -> TargetAgent:
        raise NotImplementedError("Method not implemented")

    def get_target_agent(self, identifier: str) -> TargetAgent:
        raise NotImplementedError("Method not implemented")

    def create_test(
        self,
        test_identifier: str,
        initiating_agent: Literal["maihem", "target"],
        maihem_agent_behavior_prompt: str = None,
        conversation_turns_max: int = 10,
        metrics_config: Dict = None,
    ) -> Test:
        raise NotImplementedError("Method not implemented")

    def create_test_run(
        self,
        identifier: str,
        test_identifier: str,
        target_agent: TargetAgent,
        dynamic_mode: Literal["static", "dynamic"],
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")
