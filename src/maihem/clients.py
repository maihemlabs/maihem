from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from typing import Dict, Literal, Optional, List, Callable
from pydantic import ValidationError
import random
from tqdm import tqdm
from yaspin import yaspin
from yaspin.spinners import Spinners

from maihem.modules_map import map_module_list_to_metrics
from maihem.schemas.agents import TargetAgent, AgentType
from maihem.schemas.tests import (
    Test,
    TestRun,
    TestRunConversations,
    ResultTestRun,
)
from maihem.schemas.conversations import ConversationTurnCreateResponse
from maihem.api_client.maihem_client.models.agent_target_create_request import (
    AgentTargetCreateRequest,
)
from maihem.api_client.maihem_client.models.test_create_request import (
    TestCreateRequest,
)
from maihem.api_client.maihem_client.models.test_create_request_metrics_config import (
    TestCreateRequestMetricsConfig,
)
from maihem.api_client.maihem_client.models.create_test_run_request import (
    CreateTestRunRequest,
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
from maihem.utils.documents import TextSplitter, extract_text, parse_documents


class Client:
    _base_url: str = "https://api.maihem.ai"
    _base_url_ui: str = "https://cause.maihem.ai"
    _api_key: str = None

    _staging_url: str = "https://api.staging.maihem.ai"
    _staging_url_ui: str = "https://cause.staging.maihem.ai"

    _local_url: str = "http://localhost:8000"
    _local_url_ui: str = "http://localhost:3000"

    def create_target_agent(
        self,
        name: str,
        role: str,
        description: str,
        label: str,
        language: str,
    ) -> TargetAgent:
        pass

    def get_target_agent(self, name: str) -> TargetAgent:
        # Add implementation here
        raise NotImplementedError("Method not implemented")

    def create_test(
        self,
        name: str,
        target_agent_name: str,
        initiating_agent: Literal["maihem", "target"],
        label: Optional[str] = None,
        modules: str = None,
        metrics_config: Dict = None,
        maihem_agent_behavior_prompt: str = None,
        maihem_agent_goal_prompt: str = None,
        maihem_agent_population_prompt: str = None,
        conversation_turns_max: int = 10,
        number_conversations: int = 12,
    ) -> Test:
        raise NotImplementedError("Method not implemented")

    def run_test(
        self,
        name: str,
        test_name: str,
        wrapper_function: Callable,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def get_test_run_result(self, test_name: str, test_run_name: str) -> TestRun:
        raise NotImplementedError("Method not implemented")


class Maihem(Client):
    _maihem_api_client = MaihemHTTPClientSync

    def __init__(
        self,
        env: Optional[Literal["production", "staging", "local"]] = "production",
        api_key: Optional[str] = None,
    ) -> None:
        self._logger = get_logger()

        if env == "production":
            self._api_key = api_key or os.getenv("MAIHEM_API_KEY")
            if not self._api_key:
                raise errors.raise_request_validation_error("API key is missing")
            self._maihem_api_client = MaihemHTTPClientSync(
                self._base_url, self._api_key
            )
        elif env == "staging":
            self._api_key = api_key or os.getenv("MAIHEM_API_KEY_STAGING")
            if not self._api_key:
                raise errors.raise_request_validation_error("Staging API key missing")
            self._override_base_url(self._staging_url)
            self._override_base_url_ui(self._staging_url_ui)
        elif env == "local":
            self._api_key = api_key or os.getenv("MAIHEM_API_KEY_LOCAL")
            if not self._api_key:
                raise errors.raise_request_validation_error("Local API key missing")
            self._override_base_url(self._local_url)
            self._override_base_url_ui(self._local_url_ui)

    def _override_base_url(self, base_url: str) -> None:
        self._base_url = base_url
        self._maihem_api_client = MaihemHTTPClientSync(self._base_url, self._api_key)

    def _override_base_url_ui(self, base_url_ui: str) -> None:
        self._base_url_ui = base_url_ui

    def create_target_agent(
        self,
        name: str,
        role: str,
        description: str,
        label: Optional[str] = None,
        language: Optional[str] = "en",
    ) -> TargetAgent:
        logger = get_logger()
        logger.info(f"Creating target agent '{name}'...")
        resp = None
        try:
            resp = self._maihem_api_client.create_agent_target(
                req=AgentTargetCreateRequest(
                    name=name,
                    role=role,
                    label=label,
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

        logger.info(f"Successfully created target agent '{name}'")
        return agent_target

    def get_target_agent(self, name: str) -> TargetAgent:
        resp = None
        try:
            resp = self._maihem_api_client.get_agent_target_by_name(name=name)
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
        name: str,
        target_agent_name: str,
        initiating_agent: Optional[AgentType] = AgentType.MAIHEM,
        label: Optional[str] = None,
        modules: Optional[List[str]] = None,
        metrics_config: Optional[Dict] = None,
        maihem_behavior_prompt: Optional[str] = None,
        maihem_goal_prompt: Optional[str] = None,
        maihem_population_prompt: Optional[str] = None,
        conversation_turns_max: Optional[int] = 4,
        number_conversations: Optional[int] = 10,
        documents_path: Optional[str] = None,
    ) -> Test:
        logger = get_logger()
        logger.info(f"Creating test '{name}'...")

        # Input validation using pattern matching
        match (modules, metrics_config):
            case (None, None):
                raise ValueError("Either modules or metrics_config must be provided")
            case (list(), dict()):
                raise ValueError("Cannot provide both modules and metrics_config")
            case (list(), None):
                if not modules:
                    raise ValueError("Modules list must not be empty")
                metrics_config = map_module_list_to_metrics(
                    modules, number_conversations
                )
            case (None, dict()):
                if not metrics_config:
                    raise ValueError("Metrics config must not be empty")
                if not all(
                    isinstance(v, int) and v > 0 for v in metrics_config.values()
                ):
                    raise ValueError("Metrics config values must be positive integers")
            case _:
                raise ValueError("Invalid configuration for modules or metrics_config")

        # Convert string initiating_agent to enum if needed
        if isinstance(initiating_agent, str):
            try:
                initiating_agent = AgentType[initiating_agent.upper()]
            except KeyError:
                raise errors.raise_request_validation_error(
                    f"Invalid agent type: {initiating_agent}"
                )

        try:
            target_agent = self._maihem_api_client.get_agent_target_by_name(
                name=target_agent_name
            )

            if not target_agent:
                raise errors.raise_not_found_error(
                    f"Target agent '{target_agent_name}' not found"
                )

            if documents_path:
                documents = parse_documents(documents_path)
            else:
                documents = None

            with yaspin(
                Spinners.arc,
                text="Creating Test, this might take a minute...",
            ) as _:
                metrics_config_req = TestCreateRequestMetricsConfig.from_dict(
                    metrics_config
                )
                resp = self._maihem_api_client.create_test(
                    req=TestCreateRequest(
                        name=name,
                        label=label,
                        initiating_agent=initiating_agent,
                        conversation_turns_max=conversation_turns_max,
                        agent_target_id=target_agent.id,
                        agent_maihem_behavior_prompt=maihem_behavior_prompt,
                        agent_maihem_goal_prompt=maihem_goal_prompt,
                        agent_maihem_population_prompt=maihem_population_prompt,
                        metrics_config=metrics_config_req,
                        documents=documents if documents else None,
                    )
                )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test = None

        try:
            test = Test.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        logger.info(f"Successfully created test '{name}'")
        return test

    def get_test(self, name: str) -> Test:
        resp = None
        try:
            resp = self._maihem_api_client.get_test_by_name(name=name)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test = None

        try:
            test = Test.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test

    def run_test(
        self,
        name: str,
        test_name: str,
        wrapper_function: Callable,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> ResultTestRun:
        logger = get_logger()
        test_run = None
        try:
            with yaspin(
                Spinners.arc,
                text=f"Preparing test run '{test_name}...",
            ) as _:
                test = self._maihem_api_client.get_test_by_name(name=test_name)
                target_agent = self.get_target_agent(name=test.agent_target_name)
                target_agent.set_wrapper_function(wrapper_function=wrapper_function)
                resp = None

            try:
                with yaspin(
                    Spinners.arc,
                    text="Creating Test Run, this might take a minute...",
                ) as _:
                    resp = self._maihem_api_client.create_test_run(
                        test_id=test.id,
                        req=CreateTestRunRequest(name=name, label=label),
                    )
            except errors.ErrorBase as e:
                errors.handle_base_error(e)

            try:
                test_run = TestRun.model_validate(resp.to_dict())
            except ValidationError as e:
                errors.handle_schema_validation_error(e)

            test_run_conversations = self.get_test_run_conversations(test_run.id)
            conversation_ids = test_run_conversations.conversation_ids

            logger.info(f"Starting test run '{test.name}'")
            print("\n" + "-" * 50 + "\n")
            logger.info(
                f"Running test run with {len(conversation_ids)} conversations (up to {concurrent_conversations} concurrently)..."
            )
            logger.info(f"Test run ID: {test_run.id}")
            logger.info(
                f"Test run results (UI): {self._base_url_ui}/evaluate/test-runs/{test_run.id}"
            )

            print("\n" + "-" * 50 + "\n")

            conversation_history = {}

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
                            conversation_history=conversation_history,
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
            logger.info(f"Test run '{name}' completed")

            url_results = f"https://cause.maihem.ai/evaluate/test-runs/{test_run.id}"
            logger.info(f"See test run results: {url_results}")

            return self.get_test_run_result(test_name=test_name, test_run_name=name)

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Canceling test...")
            if test_run is not None and test_run.id is not None:
                self._maihem_api_client.update_test_run_status(
                    test_run_id=test_run.id, status=TestStatusEnum.CANCELED
                )
            logger.info("Test run canceled!")
        except errors.ErrorBase as e:
            errors.handle_base_error(e)
        except Exception as e:
            logger.error(f"Error: {e}. Ending test...")
            if test_run is not None and test_run.id is not None:
                self._maihem_api_client.update_test_run_status(
                    test_run_id=test_run.id, status=TestStatusEnum.ERROR
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

    def get_test_run_result(self, test_name: str, test_run_name: str) -> ResultTestRun:
        try:
            test = self.get_test(test_name)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        try:
            test_runs = self._maihem_api_client.get_test_test_runs(
                test_id=test.id, test_run_name=test_run_name
            )
            if test_runs is None or len(test_runs) == 0:
                errors.raise_not_found_error(
                    f"Test run '{test_run_name}' not found for test '{test_name}'"
                )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run = None

        try:
            test_run_api = self._maihem_api_client.get_test_run_result(
                test_run_id=test_runs[0].id
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        try:
            test_run = ResultTestRun(test_run_api=test_run_api)
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test_run

    # def get_test_run_result_conversations(
    #     self, test_run_id: str
    # ) -> TestRunResultConversations:
    #     resp = None
    #     test_run = None

    #     try:
    #         resp = self._maihem_api_client.get_test_run_result_conversations(
    #             test_run_id
    #         )
    #     except errors.ErrorBase as e:
    #         errors.handle_base_error(e)

    #     try:
    #         resp_conversations = resp.conversations
    #         resp_dict = resp.to_dict()
    #         resp_dict["conversations"] = []

    #         conversation_nesteds: ConversationNested = []
    #         for conv in resp_conversations:
    #             conv_dict = conv.to_dict()
    #             try:
    #                 conv = ConversationNested.from_dict(conv_dict)
    #                 conversation_nesteds.append(conv)
    #             except ValidationError as e:
    #                 errors.handle_schema_validation_error(e)

    #         test_run = TestRunResultConversations.model_validate(resp_dict)
    #         test_run.conversations = conversation_nesteds
    #     except ValidationError as e:
    #         errors.handle_schema_validation_error(e)

    #     return test_run

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
        conversation_history: Dict,
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
                conversation_history=conversation_history,
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
        conversation_history: Dict,
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
            agent_maihem_message = (
                agent_maihem_message.content if agent_maihem_message else None
            )
            target_agent_message, contexts = target_agent._send_message(
                conversation_id, agent_maihem_message, conversation_history
            )
        except Exception as e:
            errors.raise_wrapper_function_error(
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
            resp = self._maihem_api_client.create_conversation_turn(
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
