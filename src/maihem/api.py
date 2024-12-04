from typing import Dict, List, Optional, Callable
import json

from maihem.api_client.maihem_client.client import Client as MaihemHTTPClient
from maihem.api_client.maihem_client.types import Response
from maihem.api_client.maihem_client.models.api_schema_agent_target_create_request import (
    APISchemaAgentTargetCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_agent_target import (
    APISchemaAgentTarget,
)
from maihem.api_client.maihem_client.models.api_schema_test_create_request import (
    APISchemaTestCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_test import (
    APISchemaTest,
)
from maihem.api_client.maihem_client.models.api_schema_test_run import (
    APISchemaTestRun,
)
from maihem.api_client.maihem_client.models.api_schema_test_run_result_metrics import (
    APISchemaTestRunResultMetrics,
)
from maihem.api_client.maihem_client.models.api_schema_test_run_result_conversations import (
    APISchemaTestRunResultConversations,
)
from maihem.api_client.maihem_client.models.api_schema_test_run_conversations import (
    APISchemaTestRunConversations,
)
from maihem.api_client.maihem_client.api.tests import tests_create_test
from maihem.api_client.maihem_client.api.tests import (
    tests_create_test_run,
    tests_get_tests,
)
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)
from maihem.api_client.maihem_client.models.api_schema_conversation_turn_create_request import (
    APISchemaConversationTurnCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_conversation_turn_create_request_document_type_0 import (
    APISchemaConversationTurnCreateRequestDocumentType0,
)
from maihem.api_client.maihem_client.models.api_schema_conversation_turn_create_response import (
    APISchemaConversationTurnCreateResponse,
)
from maihem.api_client.maihem_client.api.test_runs import (
    test_runs_get_test_run,
    test_runs_get_test_run_conversations,
    test_runs_get_test_run_result_with_conversations,
    test_runs_create_conversation_turn,
    test_runs_get_test_run_result,
    test_runs_update_test_run_status,
)
from maihem.api_client.maihem_client.models.api_schema_test_run_status_update_request import (
    APISchemaTestRunStatusUpdateRequest,
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
                    if r < retries:
                        # self._logger.warning(
                        #     f"An error occurred in {function.__name__}. Retry {r}. Error: {e}"
                        # )
                        pass
                    else:
                        self._logger.error(
                            f"An error occurred in {function.__name__} after {retries} retries. Error: {e}"
                        )
                        raise e

            return None

        return wrapper

    def create_agent_target(
        self, req: APISchemaAgentTargetCreateRequest
    ) -> APISchemaAgentTarget:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaAgentTarget] = self._retry(
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

    def get_agent_target_by_identifier(self, identifier: str) -> APISchemaAgentTarget:

        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[APISchemaAgentTarget]] = self._retry(
                agents_get_agent_targets.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                identifier=identifier,
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed[0]

    def create_test(self, req: APISchemaTestCreateRequest) -> APISchemaTest:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTest] = self._retry(
                tests_create_test.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                body=req,
            )

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed

    def get_test_by_identifier(self, identifier: str) -> APISchemaTest:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[APISchemaTest]] = self._retry(
                tests_get_tests.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                identifier=identifier,
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed[0]

    def create_test_run(self, test_id: str) -> APISchemaTestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRun] = self._retry(
                tests_create_test_run.sync_detailed
            )(client=client, x_api_key=self.token, test_id=test_id)

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def update_test_run_status(
        self, test_run_id: str, status: TestStatusEnum
    ) -> APISchemaTestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRun] = self._retry(
                test_runs_update_test_run_status.sync_detailed
            )(
                client=client,
                x_api_key=self.token,
                test_run_id=test_run_id,
                body=APISchemaTestRunStatusUpdateRequest(status=status),
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
        document: Optional[Dict[str, str]] = None,
    ) -> APISchemaConversationTurnCreateResponse:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            document_req = None

            if document:
                document_req = (
                    APISchemaConversationTurnCreateRequestDocumentType0.from_dict(
                        document
                    )
                )

            req: APISchemaConversationTurnCreateRequest = (
                APISchemaConversationTurnCreateRequest(
                    message=target_agent_message,
                    contexts=contexts,
                    document=document_req if document_req else None,
                )
            )

            response: Response[APISchemaConversationTurnCreateResponse] = self._retry(
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

    def get_test_run(self, test_run_id: str) -> APISchemaTestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRun] = self._retry(
                test_runs_get_test_run.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run_conversations(
        self, test_run_id: str
    ) -> APISchemaTestRunConversations:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRunConversations] = self._retry(
                test_runs_get_test_run_conversations.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run_result(self, test_run_id: str) -> APISchemaTestRunResultMetrics:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRunResultMetrics] = self._retry(
                test_runs_get_test_run_result.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run_result_conversations(
        self, test_run_id: str
    ) -> APISchemaTestRunResultConversations:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRunResultConversations] = self._retry(
                test_runs_get_test_run_result_with_conversations.sync_detailed
            )(client=client, x_api_key=self.token, test_run_id=test_run_id)

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed
