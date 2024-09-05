from typing import Dict, List

from src.maihem.api_client.maihem_client.client import Client as MaihemHTTPClient
from src.maihem.api_client.maihem_client.types import Response
from src.maihem.api_client.maihem_client.models.api_schema_agent_target_create_request import (
    APISchemaAgentTargetCreateRequest,
)
from src.maihem.api_client.maihem_client.models.api_schema_agent_target_create_response import (
    APISchemaAgentTargetCreateResponse,
)
from src.maihem.api_client.maihem_client.models.api_schema_test_create_request import (
    APISchemaTestCreateRequest,
)
from src.maihem.api_client.maihem_client.models.api_schema_test_create_request_metrics_config import (
    APISchemaTestCreateRequestMetricsConfig,
)
from src.maihem.api_client.maihem_client.models.api_schema_test_create_response import (
    APISchemaTestCreateResponse,
)
from src.maihem.api_client.maihem_client.models.api_schema_test_run import (
    APISchemaTestRun,
)
from src.maihem.api_client.maihem_client.models.api_schema_agent_target_get_response import (
    APISchemaAgentTargetGetResponse,
)
from src.maihem.api_client.maihem_client.api.tests import tests_create_test
from src.maihem.api_client.maihem_client.api.tests import tests_create_test_run
from src.maihem.api_client.maihem_client.api.test_runs import test_runs_get_test_run
from src.maihem.api_client.maihem_client.api.whoami import whoami_who_am_i
from src.maihem.api_client.maihem_client.api.agents import agents_create_agent_target
from src.maihem.api_client.maihem_client.api.agents import (
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
        request = APISchemaAgentTargetCreateRequest(req.to_dict())

        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaAgentTargetCreateResponse] = (
                    agents_create_agent_target.sync_detailed(
                        client=client,
                        x_api_key=self.token,
                        body=request,
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

    def create_test(
        self, req: APISchemaTestCreateRequest
    ) -> APISchemaTestCreateResponse:

        request = APISchemaTestCreateRequest(
            identifier=req.identifier,
            agent_target_id=req.agent_target_id,
            metrics_config=req.metrics_config,
            name=req.name,
            initiating_agent=req.initiating_agent,
            agent_maihem_behavior_prompt=req.agent_maihem_behavior_prompt,
        )

        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTestCreateResponse] = (
                    tests_create_test.sync_detailed(
                        client=client,
                        x_api_key=self.token,
                        body=request,
                    )
                )
        except Exception as e:
            return {"error": str(e)}

        if response.status_code != 200:
            raise Exception(response.content.decode("utf-8"))
        return response.parsed

    def create_test_run(self, test_id: str) -> APISchemaTestRun:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTestRun] = (
                    tests_create_test_run.sync_detailed(
                        client=client, x_api_key=self.token, test_id=test_id
                    )
                )

        except Exception as e:
            return {"error": str(e)}

        if response.status_code != 201:
            return response.content.decode("utf-8")
        return response.parsed

    def get_test_result(self, test_run_id: str) -> APISchemaTestRun:
        try:
            with MaihemHTTPClient(base_url=self.base_url) as client:
                response: Response[APISchemaTestRun] = (
                    test_runs_get_test_run.sync_detailed(
                        client=client, x_api_key=self.token, test_run_id=test_run_id
                    )
                )

        except Exception as e:
            return {"error": str(e)}

        if response.status_code != 201:
            return response.content.decode("utf-8")
        return response.parsed
