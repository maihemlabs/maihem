from typing import Dict, Literal, Optional
from pydantic import ValidationError

from maihem.schemas.agents import AgentTarget
from maihem.schemas.tests import Test, TestRun, TestRunResults
from maihem.api_client.maihem_client.models.api_schema_agent_target_create_request import (
    APISchemaAgentTargetCreateRequest,
)
import maihem.errors as errors
from maihem.api import MaihemHTTPClientSync


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
        identifier: str,
        test_identifier: str,
        agent_target: AgentTarget,
        # dynamic_mode: Literal["static", "dynamic"],
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def get_test_run_results(test_run_identifier: str) -> TestRunResults:
        raise NotImplementedError("Method not implemented")


class MaihemSync(Client):
    _maihem_api_client = MaihemHTTPClientSync
    _base_url = "http://localhost:8000"

    def __init__(self, api_key: str) -> None:
        self._maihem_api_client = MaihemHTTPClientSync(self._base_url, api_key)

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        industry: str,
        description: str,
        name: Optional[str] = None,
    ) -> AgentTarget:
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
        except Exception as e:
            raise errors.AgentTargetCreateError(str(e))

        agent_target = None

        try:
            agent_target = AgentTarget.model_validate(resp.to_dict())
        except ValidationError as e:
            print(e.json())

        return agent_target

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
        # dynamic_mode: Literal["static", "dynamic"],
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def get_test_run_results(test_run_identifier: str) -> TestRunResults:
        raise NotImplementedError("Method not implemented")


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

    def get_test_run_results(test_run_identifier: str) -> TestRunResults:
        raise NotImplementedError("Method not implemented")
