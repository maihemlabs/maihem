from typing import Dict, List, Optional, Callable
import json

from maihem.api_client.maihem_client.client import Client as MaihemHTTPClient
from maihem.api_client.maihem_client.types import Response
from maihem.api_client.maihem_client.models.agent_target_create_request import (
    AgentTargetCreateRequest,
)
from maihem.api_client.maihem_client.models.agent_target import (
    AgentTarget,
)
from maihem.api_client.maihem_client.models.agent_target_revision import (
    AgentTargetRevision,
)
from maihem.api_client.maihem_client.models.agent_target_revision_create_request import (
    AgentTargetRevisionCreateRequest,
)
from maihem.api_client.maihem_client.models.dataset_create_request import (
    DatasetCreateRequest,
)
from maihem.api_client.maihem_client.models.dataset import Dataset
from maihem.api_client.maihem_client.models.dataset_item_create_item_request import (
    DatasetItemCreateItemRequest,
)
from maihem.api_client.maihem_client.models.dataset_items_create_response import (
    DatasetItemsCreateResponse,
)
from maihem.api_client.maihem_client.models.test_dataset_create_request import (
    TestDatasetCreateRequest,
)
from maihem.api_client.maihem_client.models.test_create_request import (
    TestCreateRequest,
)
from maihem.api_client.maihem_client.models.test import (
    Test,
)
from maihem.api_client.maihem_client.models.test_run import (
    TestRun,
)
from maihem.api_client.maihem_client.models.test_run_workflow_trace_i_ds import (
    TestRunWorkflowTraceIDs,
)
from maihem.api_client.maihem_client.models.test_run_results_conversations import (
    TestRunResultsConversations,
)
from maihem.api_client.maihem_client.api.tests import tests_create_test
from maihem.api_client.maihem_client.api.datasets import (
    datasets_create_dataset,
    datasets_create_dataset_item,
    datasets_get_datasets,
)
from maihem.api_client.maihem_client.api.tests import (
    tests_create_test_run,
    tests_get_tests,
    tests_get_test_test_runs,
    tests_add_dataset_to_test,
)
from maihem.api_client.maihem_client.api.agents import (
    agents_create_agent_target,
    agents_get_agent_targets,
    agents_get_agent_target,
    agents_get_target_agent_workflows,
    agents_create_agent_target_revision,
    agents_get_agent_target_revisions,
)
from maihem.api_client.maihem_client.models.v_workflow import VWorkflow
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)
from maihem.api_client.maihem_client.models.conversation_turn_create_request import (
    ConversationTurnCreateRequest,
)
from maihem.api_client.maihem_client.models.conversation_turn_create_response import (
    ConversationTurnCreateResponse,
)
from maihem.api_client.maihem_client.api.test_runs import (
    test_runs_get_test_run,
    test_runs_get_test_run_conversations,
    test_runs_create_conversation_turn,
    test_runs_update_test_run_status,
    test_runs_get_test_run_result_with_conversations,
    test_runs_get_test_run_workflow_traces,
)
from maihem.api_client.maihem_client.models.create_test_run_request import (
    CreateTestRunRequest,
)
from maihem.api_client.maihem_client.api.test_runs import (
    test_runs_create_workflow_step_span,
)
from maihem.api_client.maihem_client.models.test_run_status_update_request import (
    TestRunStatusUpdateRequest,
)
from maihem.api_client.maihem_client.api.conversations import (
    conversations_get_conversation,
)
from maihem.api_client.maihem_client.api.whoami import whoami_who_am_i

from maihem.shared.lib.errors import handle_http_errors, ErrorResponse
from maihem.schemas.tests import TestStatusEnum
from maihem.shared.lib.logger import get_logger


class MaihemHTTPClientBase:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self._logger = get_logger()


class MaihemHTTPClientSync(MaihemHTTPClientBase):
    def whoami(self) -> Dict[str, str]:
        logger = get_logger()
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response = self._retry(whoami_who_am_i.sync_detailed)(
                client=client, x_api_key=self.token
            )
        if response.status_code != 200:
            handle_http_errors(logger=logger, error_resp=response.parsed)
        return response.parsed

    def _retry(self, function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            retries = 3
            for r in range(1, retries + 1):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    if r == retries:
                        self._logger.error(
                            f"An error occurred in {function.__name__} after {retries} retries. Error: {e}"
                        )
                        raise e

            return None

        return wrapper

    def _return_validated_response(self, response: Response):
        logger = get_logger()
        if response.status_code != 200 and response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(logger=logger, error_resp=ErrorResponse(**error_dict))
        return response.parsed

    def create_agent_target(self, req: AgentTargetCreateRequest) -> AgentTarget:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[AgentTarget] = self._retry(
                agents_create_agent_target.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                body=req,
            )

        return self._return_validated_response(response)

    def get_agent_targets_by_name(self, name: str) -> List[AgentTarget]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[AgentTarget]] = self._retry(
                agents_get_agent_targets.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                name=name,
            )

        return self._return_validated_response(response)

    def get_agent_target(self, agent_target_id: str) -> AgentTarget:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[AgentTarget] = self._retry(
                agents_get_agent_target.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                agent_target_id=agent_target_id,
            )

        return self._return_validated_response(response)

    def create_agent_target_revision(
        self, req: AgentTargetRevisionCreateRequest
    ) -> AgentTargetRevision:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[AgentTargetRevision] = self._retry(
                agents_create_agent_target_revision.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                body=req,
                agent_target_id=req.agent_target_id,
            )

        return self._return_validated_response(response)

    def create_test(self, req: TestCreateRequest) -> Test:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[Test] = self._retry(tests_create_test.sync_detailed)(
                client=client,
                x_api_key=self.token,
                body=req,
            )

        return self._return_validated_response(response)

    def get_tests_by_name(self, name: str) -> Test:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[Test]] = self._retry(tests_get_tests.sync_detailed)(
                client=client,
                x_api_key=self.token,
                name=name,
            )

        return self._return_validated_response(response)

    def create_test_run(self, test_id: str, req: CreateTestRunRequest) -> TestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRun] = self._retry(
                tests_create_test_run.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_id=test_id,
                body=req,
            )

        return self._return_validated_response(response)

    def update_test_run_status(
        self, test_run_id: str, status: TestStatusEnum
    ) -> TestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRun] = self._retry(
                test_runs_update_test_run_status.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_run_id=test_run_id,
                body=TestRunStatusUpdateRequest(status=status),
            )

        return self._return_validated_response(response)

    def create_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        target_agent_message: Optional[str] = None,
        contexts: Optional[List[str]] = None,
    ) -> ConversationTurnCreateResponse:
        with MaihemHTTPClient(base_url=self.base_url) as client:

            req: ConversationTurnCreateRequest = ConversationTurnCreateRequest(
                message=target_agent_message,
                contexts=contexts,
            )

            response: Response[ConversationTurnCreateResponse] = self._retry(
                test_runs_create_conversation_turn.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_run_id=test_run_id,
                conversation_id=conversation_id,
                body=req,
            )

        return self._return_validated_response(response)

    def get_conversation(self, conversation_id: str) -> ConversationNested:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[ConversationNested] = self._retry(
                conversations_get_conversation.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                conversation_id=conversation_id,
            )

        return self._return_validated_response(response)

    def get_workflow_span(
        self, test_run_id: str, workflow_trace_id: str
    ) -> ConversationNested:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[ConversationNested] = self._retry(
                test_runs_create_workflow_step_span.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_run_id=test_run_id,
                workflow_trace_id=workflow_trace_id,
            )

        return self._return_validated_response(response)

    def get_test_run(self, test_run_id: str) -> TestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRun] = self._retry(
                test_runs_get_test_run.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        return self._return_validated_response(response)

    def get_test_test_runs(self, test_id: str, test_run_name: str) -> List[TestRun]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[TestRun]] = self._retry(
                tests_get_test_test_runs.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_id=test_id,
                name=test_run_name,
            )

        return self._return_validated_response(response)

    def get_test_run_conversations(
        self, test_run_id: str
    ) -> TestRunResultsConversations:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRunResultsConversations] = self._retry(
                test_runs_get_test_run_conversations.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        return self._return_validated_response(response)

    def get_test_run_workflow_traces(self, test_run_id: str) -> TestRunWorkflowTraceIDs:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRunWorkflowTraceIDs] = self._retry(
                test_runs_get_test_run_workflow_traces.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        return self._return_validated_response(response)

    def get_test_run_result(self, test_run_id: str) -> TestRunResultsConversations:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRunResultsConversations] = self._retry(
                test_runs_get_test_run_result_with_conversations.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        return self._return_validated_response(response)

    def create_dataset(self, req: DatasetCreateRequest) -> Dataset:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[Dataset] = self._retry(
                datasets_create_dataset.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                body=req,
            )

        return self._return_validated_response(response)

    def create_dataset_items(
        self, req: DatasetItemCreateItemRequest, dataset_id: str
    ) -> DatasetItemsCreateResponse:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[DatasetItemsCreateResponse] = self._retry(
                datasets_create_dataset_item.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                dataset_id=dataset_id,
                body=req,
            )

        return self._return_validated_response(response)

    def assign_dataset_to_test(
        self, test_id: str, req: TestDatasetCreateRequest
    ) -> DatasetItemsCreateResponse:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[DatasetItemsCreateResponse] = self._retry(
                tests_add_dataset_to_test.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_id=test_id,
                body=req,
            )

        return self._return_validated_response(response)

    def get_datasets(self, name: str) -> List[Dataset]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[Dataset]] = self._retry(
                datasets_get_datasets.sync_detailed
            )(client=client, x_api_key=self.token, name=name)

        return self._return_validated_response(response)

    def get_workflows(self, agent_target_id: str) -> List[VWorkflow]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[VWorkflow]] = self._retry(
                agents_get_target_agent_workflows.sync_detailed
            )(client=client, x_api_key=self.token, agent_target_id=agent_target_id)

        return self._return_validated_response(response)

    def get_target_agent_revisions(
        self, agent_target_id: str
    ) -> List[AgentTargetRevision]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[AgentTargetRevision]] = self._retry(
                agents_get_agent_target_revisions.sync_detailed
            )(client=client, x_api_key=self.token, agent_target_id=agent_target_id)

        return self._return_validated_response(response)
