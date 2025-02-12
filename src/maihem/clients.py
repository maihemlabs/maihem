import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from typing import Dict, Literal, Optional, List, Callable
from pydantic import ValidationError
import random
from tqdm import tqdm
from yaspin import yaspin
from yaspin.spinners import Spinners

from maihem.utils.modules_map import map_module_list_to_metrics
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
from maihem.api_client.maihem_client.models.test_dataset_create_request import (
    TestDatasetCreateRequest,
)
from maihem.api_client.maihem_client.models.test_create_request_entity_type import (
    TestCreateRequestEntityType,
)
from maihem.api_client.maihem_client.models.create_test_run_request import (
    CreateTestRunRequest,
)
from maihem.api_client.maihem_client.models.test_run_workflow_trace_i_ds import (
    TestRunWorkflowTraceIDs,
)
from maihem.api_client.maihem_client.models.workflow_step_span_create_response import (
    WorkflowStepSpanCreateResponse,
)
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)
from maihem.api_client.maihem_client.models.conversation_nested_message import (
    ConversationNestedMessage,
)
from maihem.api_client.maihem_client.models.dataset_item_create_item_request import (
    DatasetItemCreateItemRequest,
)
from maihem.api_client.maihem_client.models.dataset_items_create_request import (
    DatasetItemsCreateRequest,
)
from maihem.api_client.maihem_client.models.dataset_items_create_response import (
    DatasetItemsCreateResponse,
)
from maihem.api_client.maihem_client.models.dataset_create_request import (
    DatasetCreateRequest,
)
import maihem.errors as errors
from maihem.api import MaihemHTTPClientSync
from maihem.schemas.tests import TestStatusEnum
from maihem.utils.documents import TextSplitter, extract_text, parse_documents
from maihem.logger import get_logger


class Client:

    _api_key: str = None
    _base_url: str = "https://api.maihem.ai"
    _base_url_ui: str = "https://cause.maihem.ai"
    _staging_url: str = "https://api.staging.maihem.ai"
    _staging_url_ui: str = "https://cause.staging.maihem.ai"
    _local_url: str = "http://localhost:8000"
    _local_url_ui: str = "http://localhost:3000"

    _maihem_api_client = MaihemHTTPClientSync

    def __init__(
        self,
        env: Optional[Literal["production", "staging", "local"]] = "production",
        api_key: Optional[str] = None,
    ) -> None:
        self._logger = get_logger()

        # Initialize the API client based on the environment
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

    def run_workflow_test(
        self,
        name: str,
        test_name: str,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def run_step_test(
        self,
        name: str,
        test_name: str,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def add_target_agent(
        self,
        name: str,
        role: str,
        description: str,
        label: Optional[str] = None,
        language: Optional[str] = "en",
    ) -> TargetAgent:
        self._logger.info(f"Creating target agent '{name}'...")

        # Create target agent
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

        # Validate response
        agent_target = None
        try:
            agent_target = TargetAgent.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        self._logger.info(f"Successfully created target agent '{name}'")
        return agent_target

    def get_target_agent(self, name: str) -> TargetAgent:
        # Get target agent
        try:
            target_agents = self._maihem_api_client.get_agent_targets_by_name(name=name)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        # Validate response
        if not target_agents or len(target_agents) == 0:
            raise errors.raise_not_found_error(f"Target agent '{name}' not found")

        target_agent = None
        try:
            target_agent = TargetAgent.model_validate(target_agents[0].to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return target_agent

    def upload_workflow_dataset(
        self,
        name: str,
        data: Dict,
        label: Optional[str] = None,
    ) -> None:
        self._upload_dataset(
            name=name,
            data=data,
            label=label,
            entity_type=TestCreateRequestEntityType.WORKFLOW,
        )

    def upload_step_dataset(
        self,
        name: str,
        data: Dict,
        target_agent_name: str,
        step_name: str,
        label: Optional[str] = None,
    ) -> None:
        # Get entity id for workflow step
        entity_id = self._get_workflow_entity_id(
            target_agent_name=target_agent_name,
            entity_type=TestCreateRequestEntityType.WORKFLOW_STEP,
            step_name=step_name,
        )

        self._upload_dataset(
            name=name,
            data=data,
            label=label,
            entity_type=TestCreateRequestEntityType.WORKFLOW_STEP,
            entity_id=entity_id,
        )

    def _upload_dataset(
        self,
        name: str,
        data: Dict,
        entity_type: TestCreateRequestEntityType = TestCreateRequestEntityType.WORKFLOW,
        entity_id: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        self._logger.info(f"Uploading dataset '{name}'...")

        # Create dataset
        resp = None
        try:
            # Create dataset and get dataset id
            resp = self._maihem_api_client.create_dataset(
                req=DatasetCreateRequest(
                    name=name,
                    label=label,
                    target_type=entity_type,
                    target_id=entity_id,
                )
            )

            # Create dataset items for each item in data
            dataset_items = []
            for item in data:
                dataset_item = DatasetItemCreateItemRequest(
                    input_payload=json.dumps(item["input_payload"]),
                    output_payload_expected=json.dumps(item["output_payload_expected"]),
                )
                dataset_items.append(dataset_item)

            # Create dataset from dataset items and pass dataset id
            resp = self._maihem_api_client.create_dataset_items(
                req=DatasetItemsCreateRequest(
                    items=dataset_items,
                ),
                dataset_id=resp.id,
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        # Validate response
        try:
            dataset = DatasetItemsCreateResponse.from_dict(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        self._logger.info(f"Successfully uploaded dataset '{name}'")

    def autogenerate_workflow_test(
        self,
        name: str,
        target_agent_name: str,
        initiating_agent: Optional[AgentType] = AgentType.MAIHEM,
        label: Optional[str] = None,
        maihem_behavior_prompt: Optional[str] = None,
        maihem_goal_prompt: Optional[str] = None,
        maihem_population_prompt: Optional[str] = None,
        conversation_turns_max: Optional[int] = 4,
        number_conversations: Optional[int] = 10,
        documents_path: Optional[str] = None,
        modules: Optional[List[str]] = None,
        metrics_config: Optional[Dict] = None,
    ) -> Test:
        self._logger.info(f"Creating test '{name}'...")

        # Get metrics_config from modules if not provided
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

        return self._create_test(
            name=name,
            target_agent_name=target_agent_name,
            entity_type=TestCreateRequestEntityType.WORKFLOW,
            initiating_agent=initiating_agent,
            label=label,
            maihem_behavior_prompt=maihem_behavior_prompt,
            maihem_goal_prompt=maihem_goal_prompt,
            maihem_population_prompt=maihem_population_prompt,
            conversation_turns_max=conversation_turns_max,
            number_conversations=number_conversations,
            documents_path=documents_path,
            metrics_config=metrics_config,
        )

    def create_workflow_test(
        self,
        name: str,
        target_agent_name: str,
        dataset_name: str,
        initiating_agent: Optional[AgentType] = AgentType.MAIHEM,
        label: Optional[str] = None,
    ) -> Test:

        # First create the test
        test = self._create_test(
            name,
            label=label,
            target_agent_name=target_agent_name,
            entity_type=TestCreateRequestEntityType.WORKFLOW,
            step_name=None,
            initiating_agent=initiating_agent,
            metrics_config={"qa_cx_helpfulness": 1},  # TODO: change to not needed
        )

        # Get dataset id from dataset name
        dataset = self._maihem_api_client.get_datasets(name=dataset_name)
        if not dataset or len(dataset) == 0:
            raise errors.raise_not_found_error(
                f"Dataset '{dataset_name}' does not exist"
            )

        # Assign dataset to test
        self._maihem_api_client.assign_dataset_to_test(
            test_id=test.id, req=TestDatasetCreateRequest(dataset_id=dataset[0].id)
        )

        return test

    def create_step_test(
        self,
        name: str,
        target_agent_name: str,
        dataset_name: str,
        step_name: str,
        initiating_agent: Optional[AgentType] = AgentType.MAIHEM,
        label: Optional[str] = None,
    ) -> Test:
        # First create the test
        test = self._create_test(
            name,
            label=label,
            target_agent_name=target_agent_name,
            entity_type=TestCreateRequestEntityType.WORKFLOW_STEP,
            step_name=step_name,
            initiating_agent=initiating_agent,
            metrics_config={"qa_cx_helpfulness": 1},  # TODO: change to not needed
        )

        # Get dataset id from dataset name
        dataset = self._maihem_api_client.get_datasets(name=dataset_name)
        if not dataset or len(dataset) == 0:
            raise errors.raise_not_found_error(
                f"Dataset '{dataset_name}' does not exist"
            )

        # Assign dataset to test
        self._maihem_api_client.assign_dataset_to_test(
            test_id=test.id, req=TestDatasetCreateRequest(dataset_id=dataset[0].id)
        )

        return test

    def _create_test(
        self,
        name: str,
        target_agent_name: str,
        entity_type: TestCreateRequestEntityType,
        step_name: Optional[str] = None,
        initiating_agent: Optional[AgentType] = AgentType.MAIHEM,
        label: Optional[str] = None,
        maihem_behavior_prompt: Optional[str] = None,
        maihem_goal_prompt: Optional[str] = None,
        maihem_population_prompt: Optional[str] = None,
        conversation_turns_max: Optional[int] = 4,
        documents_path: Optional[str] = None,
        metrics_config: Optional[Dict] = None,
    ) -> Test:

        # Convert string initiating_agent to enum if needed
        if isinstance(initiating_agent, str):
            try:
                initiating_agent = AgentType[initiating_agent.upper()]
            except KeyError:
                raise errors.raise_request_validation_error(
                    f"Invalid agent type: {initiating_agent}"
                )

        try:
            # Create test
            with yaspin(
                Spinners.arc,
                text="Creating test, this might take a minute...",
            ) as _:

                # Parse documents
                documents = parse_documents(documents_path) if documents_path else None
                documents = documents if documents else None

                # Get target agent
                target_agent = self.get_target_agent(name=target_agent_name)

                # Get entity id (workflow id)
                entity_id = self._get_workflow_entity_id(
                    target_agent_name=target_agent_name,
                    entity_type=entity_type,
                    step_name=step_name,
                )

                metrics_config_req = TestCreateRequestMetricsConfig.from_dict(
                    metrics_config
                )
                resp = self._maihem_api_client.create_test(
                    req=TestCreateRequest(
                        entity_type=entity_type,
                        entity_id=entity_id,
                        name=name,
                        label=label,
                        initiating_agent=initiating_agent,
                        conversation_turns_max=conversation_turns_max,
                        agent_target_id=target_agent.id,
                        agent_maihem_behavior_prompt=maihem_behavior_prompt,
                        agent_maihem_goal_prompt=maihem_goal_prompt,
                        agent_maihem_population_prompt=maihem_population_prompt,
                        metrics_config=metrics_config_req,
                        documents=documents,
                    )
                )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        # Validate response
        test = None
        try:
            test = Test.model_validate(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        self._logger.info(f"Successfully created test '{name}'")
        return test

    def get_test(self, name: str) -> Test:
        # Get test
        resp = None
        try:
            resp = self._maihem_api_client.get_tests_by_name(name=name)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        if not resp or len(resp) == 0:
            raise errors.raise_not_found_error(f"Test '{name}' not found")

        # Validate response
        test = None
        try:
            test = Test.model_validate(resp[0].to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test

    def get_test_run_result(self, test_name: str, test_run_name: str) -> ResultTestRun:
        # Get test
        try:
            test = self.get_test(test_name)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        # Get test runs
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

        # Get test run result
        test_run = None
        try:
            test_run_api = self._maihem_api_client.get_test_run_result(
                test_run_id=test_runs[0].id
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        # Validate response
        try:
            test_run = ResultTestRun(test_run_api=test_run_api)
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test_run

    def _get_workflow(self, target_agent: TargetAgent):
        workflows = self._maihem_api_client.get_workflows(
            agent_target_id=target_agent.id
        )
        if not workflows or len(workflows) == 0:
            raise errors.raise_not_found_error(
                f"Workflows for target agent '{target_agent.name}' not found. Please initialize a workflow for this target agent."
            )
        workflow = workflows[len(workflows) - 1]
        return workflow

    def _get_workflow_entity_id(
        self,
        target_agent_name: str,
        entity_type: TestCreateRequestEntityType,
        step_name: Optional[str] = None,
    ) -> str:

        # Get target agent id
        target_agent = self.get_target_agent(name=target_agent_name)

        # Get workflows
        workflow = self._get_workflow(target_agent=target_agent)

        # Get entity id for workflow or workflow step
        entity_id = None
        if entity_type == TestCreateRequestEntityType.WORKFLOW_STEP:
            for step in workflow.workflow_steps:
                if step["name"] == step_name:
                    entity_id = step["id"]
                    break
        else:
            entity_id = workflow.id

        if not entity_id:
            raise errors.raise_not_found_error(
                f"Entity '{entity_type}' with name '{step_name}' not found"
            )

        return entity_id


class Maihem(Client):

    def run_step_test(
        self,
        name: str,
        test_name: str,
        step_name: str,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> ResultTestRun:
        return self._run_test(
            name=name,
            test_name=test_name,
            entity_type=TestCreateRequestEntityType.WORKFLOW_STEP,
            step_name=step_name,
            label=label,
            concurrent_conversations=concurrent_conversations,
        )

    def run_workflow_test(
        self,
        name: str,
        test_name: str,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> ResultTestRun:
        return self._run_test(
            name=name,
            test_name=test_name,
            entity_type=TestCreateRequestEntityType.WORKFLOW,
            label=label,
            concurrent_conversations=concurrent_conversations,
        )

    """
    How test run works:
    def _run_test():
      set_wrapper_function() [workflow or step]
      _maihem_api_client.create_test_run()
      _get_test_run_conversations() -> _maihem_api_client.get_test_run_conversations()
      for conversation in conversations (concurrently):
        _run_conversation() -> while conversation is active:
          _run_conversation_turn()
              _get_conversation() -> _maihem_api_client.get_conversation()
              _call_workflow()/_call_step() [call wrapper function] -> target_agent._call_workflow()/_call_step()
              _get_conversation_turn() -> _maihem_api_client.get_conversation_turn()
      _get_test_run_result() -> _maihem_api_client.get_test_run_result()
    """

    def run_workflow_test(
        self,
        name: str,
        test_name: str,
        label: Optional[str] = None,
        concurrent_conversations: int = 10,
    ) -> ResultTestRun:

        test_run = None
        try:
            with yaspin(
                Spinners.arc,
                text=f"Preparing test run '{test_name}...",
            ) as _:
                # Get all necessary information and objects
                test = self.get_test(test_name)
                target_agent_api = self._maihem_api_client.get_agent_target(
                    agent_target_id=test.agent_target_id
                )
                target_agent = self.get_target_agent(name=target_agent_api.name)
                workflow = self._get_workflow(target_agent=target_agent)

                # Set wrapper function to be called
                target_agent.set_wrapper_function(
                    function_name=workflow.name, workflow_name=workflow.name
                )

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

            test_run_conversations = self._get_test_run_conversations(test_run.id)
            conversation_ids = test_run_conversations.conversation_ids

            self._logger.info(f"Starting test run '{test.name}'")
            print("\n" + "-" * 50 + "\n")
            self._logger.info(
                f"Running test run with {len(conversation_ids)} conversations (up to {concurrent_conversations} concurrently)..."
            )
            self._logger.info(f"Test run ID: {test_run.id}")
            self._logger.info(
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
                            self._logger.error(
                                f"Error running conversation ({conversation_id}): {e.message}"
                            )
                            progress.colour = "red"
                        finally:
                            progress.update()

            print("\n" + "-" * 50 + "\n")
            self._logger.info(f"Test run '{name}' completed")

            url_results = f"https://cause.maihem.ai/evaluate/test-runs/{test_run.id}"
            self._logger.info(f"See test run results: {url_results}")

            return self.get_test_run_result(test_name=test_name, test_run_name=name)

        except KeyboardInterrupt:
            self._logger.info("Keyboard interrupt detected. Canceling test...")
            if test_run is not None and test_run.id is not None:
                self._maihem_api_client.update_test_run_status(
                    test_run_id=test_run.id, status=TestStatusEnum.CANCELED
                )
            self._logger.info("Test run canceled!")
        except errors.ErrorBase as e:
            errors.handle_base_error(e)
        except Exception as e:
            self._logger.error(f"Error: {e}. Ending test...")
            if test_run is not None and test_run.id is not None:
                self._maihem_api_client.update_test_run_status(
                    test_run_id=test_run.id, status=TestStatusEnum.ERROR
                )

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
        pending_target_message_id = None
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
                pending_target_message_id=pending_target_message_id,
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
            pending_target_message_id = turn_resp.pending_target_message_id

        return conversation_id

    def _run_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        test: Test,
        target_agent: TargetAgent,
        conversation_history: Dict,
        previous_turn_id: Optional[str] = None,
        pending_target_message_id: Optional[str] = None,
    ) -> ConversationTurnCreateResponse:
        agent_maihem_message = None

        turn_resp = None

        conversation = self._get_conversation(conversation_id)

        document_key = None
        text = None

        # Document loading and chunking (for RAG)
        # if target_agent.document_paths:
        #     max_attempts = 10
        #     attempts = 0
        #     while attempts < max_attempts:
        #         if not target_agent.document_paths:
        #             break
        #         document_path = random.choice(list(target_agent.document_paths))
        #         document_key = os.path.basename(document_path)
        #         try:
        #             document = extract_text(document_path)
        #             if len(document) > 10000:
        #                 chunks = TextSplitter(
        #                     chunk_size=5000, chunk_overlap=200
        #                 ).split_text(document)
        #                 text = random.choice(chunks)
        #             else:
        #                 text = document
        #             if text.strip():
        #                 break
        #         except Exception as e:
        #             self._logger.warning(
        #                 f"Error processing document {document_key}: {str(e)}"
        #             )
        #         attempts += 1

        #     if attempts == max_attempts:
        #         self._logger.warning(
        #             "Max attempts reached while trying to select a valid document chunk."
        #         )
        if (
            test.initiating_agent == AgentType.MAIHEM
            and len(conversation.conversation_turns) == 0
        ):  # If Maihem starts and no conversation turns exist yet
            turn_resp = self._generate_conversation_turn(
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                target_agent_message=None,
                contexts=[],
            )

            pending_target_message_id = turn_resp.pending_target_message_id

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

            target_agent_message = target_agent._call_workflow(
                conversation_id=conversation_id,
                conversation_message_id=pending_target_message_id,
                message=agent_maihem_message,
                conversation_history=conversation_history,
                test_run_id=test_run_id,
            )

            contexts = []  # TODO: remove contexts from all sequence

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
                pending_target_message_id=resp.pending_target_message_id,
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

    def _get_test_run_conversations(self, test_run_id: str) -> TestRunConversations:
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

    def _get_conversation(self, conversation_id: str) -> ConversationNested:
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

    def run_step_test(
        self,
        name: str,
        test_name: str,
        step_name: str,
        label: Optional[str] = None,
        concurrent_interactions: int = 10,
    ) -> ResultTestRun:

        test_run = None
        try:
            with yaspin(
                Spinners.arc,
                text=f"Preparing test run '{test_name}...",
            ) as _:
                # Get all necessary information and objects
                test = self.get_test(test_name)
                target_agent_api = self._maihem_api_client.get_agent_target(
                    agent_target_id=test.agent_target_id
                )
                target_agent = self.get_target_agent(name=target_agent_api.name)
                workflow = self._get_workflow(target_agent=target_agent)

                # Check step name is in workflow steps
                is_valid_step_name = False
                for step in workflow.workflow_steps:
                    if step["name"] == step_name:
                        is_valid_step_name = True
                        break
                if is_valid_step_name:
                    # Set wrapper function to be called
                    target_agent.set_wrapper_function(
                        function_name=step_name,
                        workflow_name=workflow.name,
                    )
                else:
                    raise errors.raise_not_found_error(
                        f"Step '{step_name}' not found in workflow '{workflow.name}'"
                    )
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

            test_run_traces = self._get_test_run_workflow_traces(test_run.id)
            traces_ids = test_run_traces.workflow_trace_ids

            self._logger.info(f"Starting test run '{test.name}'")
            print("\n" + "-" * 50 + "\n")
            self._logger.info(
                f"Running test run with {len(traces_ids)} interactions (up to {concurrent_interactions} concurrently)..."
            )
            self._logger.info(f"Test run ID: {test_run.id}")
            self._logger.info(
                f"Test run results (UI): {self._base_url_ui}/evaluate/test-runs/{test_run.id}"
            )

            print("\n" + "-" * 50 + "\n")

            with tqdm(
                len(traces_ids),
                total=len(traces_ids),
                unit="interaction",
                colour="green",
                desc=f"Test run ({test_run.id})",
                position=0,
            ) as progress:
                with ThreadPoolExecutor(
                    max_workers=concurrent_interactions
                ) as executor:
                    future_to_trace_id = {
                        executor.submit(
                            self._run_step_interaction,
                            test_run.id,
                            trace_id,
                            test,
                            target_agent,
                            progress_bar_position=i + 1,
                        ): trace_id
                        for i, trace_id in enumerate(traces_ids)
                    }

                    for future in as_completed(future_to_trace_id):
                        trace_id = future_to_trace_id[future]
                        try:
                            future.result()
                        except errors.ErrorBase as e:
                            self._logger.error(
                                f"Error running interaction ({trace_id}): {e.message}"
                            )
                            progress.colour = "red"
                        finally:
                            progress.update()

            print("\n" + "-" * 50 + "\n")
            self._logger.info(f"Test run '{name}' completed")

            url_results = f"https://cause.maihem.ai/evaluate/test-runs/{test_run.id}"
            self._logger.info(f"See test run results: {url_results}")

            return self.get_test_run_result(test_name=test_name, test_run_name=name)

        except KeyboardInterrupt:
            self._logger.info("Keyboard interrupt detected. Canceling test...")
            if test_run is not None and test_run.id is not None:
                self._maihem_api_client.update_test_run_status(
                    test_run_id=test_run.id, status=TestStatusEnum.CANCELED
                )
            self._logger.info("Test run canceled!")
        except errors.ErrorBase as e:
            errors.handle_base_error(e)
        except Exception as e:
            self._logger.error(f"Error: {e}. Ending test...")
            if test_run is not None and test_run.id is not None:
                self._maihem_api_client.update_test_run_status(
                    test_run_id=test_run.id, status=TestStatusEnum.ERROR
                )

    def _run_step_interaction(
        self,
        test_run_id: str,
        interaction_id: str,
        test: Test,
        target_agent: TargetAgent,
        progress_bar_position: int,
    ) -> str:

        # Print progress bar
        progress = tqdm(
            total=test.conversation_turns_max,
            desc=f"Interaction ({interaction_id})",
            position=progress_bar_position,
            leave=False,
        )
        progress.update()

        span = self._get_workflow_span(
            test_run_id=test_run_id, workflow_trace_id=interaction_id
        )
        try:
            result = target_agent._call_step(
                interaction_id=interaction_id,
                target_agent_id=target_agent.id,
                test_run_id=test_run_id,
                kwargs=span.input_payload.additional_properties,
            )

        except Exception as e:
            errors.raise_wrapper_function_error(
                f"Error sending data to target agent: {e}"
            )

        return interaction_id

    def _get_test_run_workflow_traces(
        self, test_run_id: str
    ) -> TestRunWorkflowTraceIDs:
        resp = None
        try:
            resp = self._maihem_api_client.get_test_run_workflow_traces(test_run_id)
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        test_run_traces = None
        try:
            test_run_traces = TestRunWorkflowTraceIDs.from_dict(resp.to_dict())
        except ValidationError as e:
            errors.handle_schema_validation_error(e)

        return test_run_traces

    def _get_workflow_span(
        self, test_run_id: str, workflow_trace_id: str
    ) -> WorkflowStepSpanCreateResponse:
        resp = None
        try:
            resp = self._maihem_api_client.get_workflow_span(
                test_run_id=test_run_id, workflow_trace_id=workflow_trace_id
            )
        except errors.ErrorBase as e:
            errors.handle_base_error(e)

        try:
            workflow_span = WorkflowStepSpanCreateResponse.from_dict(resp.to_dict())
            return workflow_span
        except ValidationError as e:
            errors.handle_schema_validation_error(e)
