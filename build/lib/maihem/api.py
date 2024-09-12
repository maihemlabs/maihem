from typing import Dict, List, Optional
import json
from maihem.api_client.maihem_client.client import Client as MaihemHTTPClient
from maihem.api_client.maihem_client.types import Response
from maihem.api_client.maihem_client.models.api_schema_agent_target_create_request import (
    APISchemaAgentTargetCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_agent_target_create_response import (
    APISchemaAgentTargetCreateResponse,
)
from maihem.api_client.maihem_client.models.api_schema_test_create_request import (
    APISchemaTestCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_test_run_create_request import (
    APISchemaTestRunCreateRequest,
)
from maihem.api_client.maihem_client.models.api_schema_test import (
    APISchemaTest,
)
from maihem.api_client.maihem_client.models.api_schema_test_run import (
    APISchemaTestRun,
)
from maihem.api_client.maihem_client.models.api_schema_test_run_with_conversations_nested import (
    APISchemaTestRunWithConversationsNested,
)
from maihem.api_client.maihem_client.models.api_schema_agent_target_get_response import (
    APISchemaAgentTargetGetResponse,
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
from maihem.api_client.maihem_client.models.api_schema_conversation_turn_create_response import (
    APISchemaConversationTurnCreateResponse,
)
from maihem.api_client.maihem_client.api.test_runs import (
    test_runs_get_test_run,
    test_runs_get_test_run_with_conversations,
    test_runs_create_conversation_turn,
)
from maihem.api_client.maihem_client.api.conversations import (
    conversations_get_conversation,
)
from maihem.api_client.maihem_client.api.whoami import whoami_who_am_i
from maihem.api_client.maihem_client.api.agents import agents_create_agent_target
from maihem.api_client.maihem_client.api.agents import (
    agents_get_agent_targets,
)

from maihem.errors import handle_http_errors, ErrorResponse


class MaihemHTTPClientBase:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token


class MaihemHTTPClientSync(MaihemHTTPClientBase):
    def whoami(self) -> Dict[str, str]:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response = whoami_who_am_i.sync_detailed(
                client=client, x_api_key=self.token
            )

        if response.status_code != 200:
            handle_http_errors(error_resp=response.parsed)
        return response.parsed

    def create_agent_target(
        self, req: APISchemaAgentTargetCreateRequest
    ) -> APISchemaAgentTargetCreateResponse:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaAgentTargetCreateResponse] = (
                agents_create_agent_target.sync_detailed(
                    client=client,
                    x_api_key=self.token,
                    body=req,
                )
            )

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_agent_target_by_identifier(
        self, identifier: str
    ) -> APISchemaAgentTargetGetResponse:

        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[List[APISchemaAgentTargetGetResponse]] = (
                agents_get_agent_targets.sync_detailed(
                    client=client,
                    x_api_key=self.token,
                    identifier=identifier,
                )
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed[0]

    def create_test(self, req: APISchemaTestCreateRequest) -> APISchemaTest:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTest] = tests_create_test.sync_detailed(
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
            response: Response[List[APISchemaTest]] = tests_get_tests.sync_detailed(
                client=client,
                x_api_key=self.token,
                identifier=identifier,
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))

        return response.parsed[0]

    def create_test_run(self, test_id: str, agent_target_id: str) -> APISchemaTestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRun] = tests_create_test_run.sync_detailed(
                client=client,
                x_api_key=self.token,
                test_id=test_id,
                body=APISchemaTestRunCreateRequest(agent_target_id=agent_target_id),
            )

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def create_conversation_turn(
        self,
        test_run_id: str,
        conversation_id: str,
        target_agent_message: Optional[str] = None,
        contexts: Optional[List[str]] = None,
    ) -> APISchemaConversationTurnCreateResponse:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            req: APISchemaConversationTurnCreateRequest = (
                APISchemaConversationTurnCreateRequest(
                    message=target_agent_message, contexts=contexts
                )
            )

            response: Response[APISchemaConversationTurnCreateResponse] = (
                test_runs_create_conversation_turn.sync_detailed(
                    client=client,
                    x_api_key=self.token,
                    test_run_id=test_run_id,
                    conversation_id=conversation_id,
                    body=req,
                )
            )

        if response.status_code != 201:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run(self, test_run_id: str) -> APISchemaTestRun:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRun] = test_runs_get_test_run.sync_detailed(
                client=client, x_api_key=self.token, test_run_id=test_run_id
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_conversation(self, conversation_id: str) -> ConversationNested:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[ConversationNested] = (
                conversations_get_conversation.sync_detailed(
                    client=client,
                    x_api_key=self.token,
                    conversation_id=conversation_id,
                )
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed

    def get_test_run_with_conversations(
        self, test_run_id: str
    ) -> APISchemaTestRunWithConversationsNested:
        with MaihemHTTPClient(base_url=self.base_url) as client:
            response: Response[APISchemaTestRunWithConversationsNested] = (
                test_runs_get_test_run_with_conversations.sync_detailed(
                    client=client, x_api_key=self.token, test_run_id=test_run_id
                )
            )

        if response.status_code != 200:
            error_dict = json.loads(response.content)
            handle_http_errors(error_resp=ErrorResponse.from_dict(error_dict))
        return response.parsed
