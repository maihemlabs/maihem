from typing import Dict, List, Optional

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


class MaihemHTTPClientBase:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token


class MaihemHTTPClientSync(MaihemHTTPClientBase):
    def whoami(self) -> Dict[str, str]:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response = whoami_who_am_i.sync_detailed(
                    client=client, x_api_key=self.token
                )
        except Exception as e:
            return {"error": str(e)}

        if response.status_code != 200:
            return response.content.decode("utf-8")
        return response.parsed

    def create_agent_target(
        self, req: APISchemaAgentTargetCreateRequest
    ) -> APISchemaAgentTargetCreateResponse:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaAgentTargetCreateResponse] = (
                    agents_create_agent_target.sync_detailed(
                        client=client,
                        x_api_key=self.token,
                        body=req,
                    )
                )
        except Exception as e:
            return {"error": str(e)}

        if response.status_code != 201:
            raise Exception(response.content.decode("utf-8"))
        return response.parsed

    def get_agent_target_by_identifier(
        self, identifier: str
    ) -> APISchemaAgentTargetGetResponse:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[List[APISchemaAgentTargetGetResponse]] = (
                    agents_get_agent_targets.sync_detailed(
                        client=client,
                        x_api_key=self.token,
                        identifier=identifier,
                    )
                )
        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 200:
            raise Exception(response.content.decode("utf-8"))

        return response.parsed[0]

    def create_test(self, req: APISchemaTestCreateRequest) -> APISchemaTest:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTest] = tests_create_test.sync_detailed(
                    client=client,
                    x_api_key=self.token,
                    body=req,
                )
        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 201:
            raise Exception(response.content.decode("utf-8"))
        return response.parsed

    def get_test_by_identifier(self, identifier: str) -> APISchemaTest:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[List[APISchemaTest]] = tests_get_tests.sync_detailed(
                    client=client,
                    x_api_key=self.token,
                    identifier=identifier,
                )
        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 200:
            raise Exception(response.content.decode("utf-8"))

        return response.parsed[0]

    def create_test_run(self, test_id: str) -> APISchemaTestRun:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTestRun] = (
                    tests_create_test_run.sync_detailed(
                        client=client, x_api_key=self.token, test_id=test_id
                    )
                )

        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 201:
            return response.content.decode("utf-8")
        return response.parsed

    def create_conversation_turns(
        self,
        test_run_id: str,
        conversation_id: str,
        target_agent_message: Optional[str] = None,
        contexts: Optional[List[str]] = None,
    ) -> APISchemaConversationTurnCreateResponse:
        try:
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
        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 201:
            return response.content.decode("utf-8")
        return response.parsed

    def get_test_run(self, test_run_id: str) -> APISchemaTestRun:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTestRun] = (
                    test_runs_get_test_run.sync_detailed(
                        client=client, x_api_key=self.token, test_run_id=test_run_id
                    )
                )

        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 200:
            return response.content.decode("utf-8")
        return response.parsed

    def get_conversation(self, conversation_id: str) -> ConversationNested:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[ConversationNested] = (
                    conversations_get_conversation.sync_detailed(
                        client=client,
                        x_api_key=self.token,
                        conversation_id=conversation_id,
                    )
                )

        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 200:
            return response.content.decode("utf-8")
        return response.parsed

    def get_test_run_with_conversations(
        self, test_run_id: str
    ) -> APISchemaTestRunWithConversationsNested:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTestRunWithConversationsNested] = (
                    test_runs_get_test_run_with_conversations.sync_detailed(
                        client=client, x_api_key=self.token, test_run_id=test_run_id
                    )
                )

        except Exception as e:
            print({"error": str(e)})
            raise

        if response.status_code != 200:
            return response.content.decode("utf-8")
        return response.parsed
