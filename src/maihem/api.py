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
from maihem.api_client.maihem_client.models.test_create_request import (
    TestCreateRequest,
)
from maihem.api_client.maihem_client.models.test import (
    Test,
)
from maihem.api_client.maihem_client.models.test_run import (
    TestRun,
)
from maihem.api_client.maihem_client.models.test_run_results_conversations import (
    TestRunResultsConversations,
)
from maihem.api_client.maihem_client.api.tests import tests_create_test
from maihem.api_client.maihem_client.api.tests import (
    tests_create_test_run,
    tests_get_tests,
    tests_get_test_test_runs,
)
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
)
from maihem.api_client.maihem_client.models.create_test_run_request import (
    CreateTestRunRequest,
)
from maihem.api_client.maihem_client.models.test_run_status_update_request import (
    TestRunStatusUpdateRequest,
)
from maihem.api_client.maihem_client.api.conversations import (
    conversations_get_conversation,
)
from maihem.api_client.maihem_client.api.whoami import whoami_who_am_i
from maihem.api_client.maihem_client.api.agents import agents_create_agent_target
from maihem.api_client.maihem_client.api.agents import agents_get_agent_targets

from maihem.errors import handle_http_errors, ErrorResponse
from maihem.schemas.tests import TestStatusEnum
from maihem.logger import get_logger


class MaihemHTTPClientBase:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self._logger = get_logger()


class MaihemHTTPClientSync(MaihemHTTPClientBase):
    def whoami(self) -> Dict[str, str]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response = self._retry(whoami_who_am_i.sync_detailed)(
                client=client, x_api_key=self.token
            )

        if response.status_code != 200:
            handle_http_errors(error_resp=response.parsed)
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

    def create_agent_target(self, req: AgentTargetCreateRequest) -> AgentTarget:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[AgentTarget] = self._retry(
                agents_create_agent_target.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                body=req,
            )

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_agent_target_by_name(self, name: str) -> AgentTarget:

        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[AgentTarget]] = self._retry(
                agents_get_agent_targets.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                name=name,
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed[0]

    def create_test(self, req: TestCreateRequest) -> Test:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[Test] = self._retry(tests_create_test.sync_detailed)(
                client=client,
                x_api_key=self.token,
                body=req,
            )

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed

    def get_test_by_name(self, name: str) -> Test:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[Test]] = self._retry(tests_get_tests.sync_detailed)(
                client=client,
                x_api_key=self.token,
                name=name,
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed[0]

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

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

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

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

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

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_conversation(self, conversation_id: str) -> ConversationNested:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[ConversationNested] = self._retry(
                conversations_get_conversation.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                conversation_id=conversation_id,
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run(self, test_run_id: str) -> TestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRun] = self._retry(
                test_runs_get_test_run.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

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

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run_conversations(
        self, test_run_id: str
    ) -> TestRunResultsConversations:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRunResultsConversations] = self._retry(
                test_runs_get_test_run_conversations.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    # def get_test_run_result(self, name: str) -> TestRunResults:
    #     with MaihemHTTPClient(base_url=self.base_url) as client:
    #         response: Response[TestRunResults] = self._retry(
    #             test_runs_get_test_run_result.sync_detailed
    #         )(client=client, x_api_key=self.token, name=name)

    #     if response.status_code != 200:
    #         error_dict = json.loads(response.content)
    #         handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
    #     return response.parsed

    def get_test_run_result(self, test_run_id: str) -> TestRunResultsConversations:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[TestRunResultsConversations] = self._retry(
                test_runs_get_test_run_result_with_conversations.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed
