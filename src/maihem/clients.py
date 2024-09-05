from typing import Dict, Literal

from maihem.schemas.agents import AgentTarget
from maihem.schemas.tests import Test, TestRun, TestRunResults


class Client:

    def __init__(self) -> None:
        pass

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        company: str,
        industry: str,
        description: str,
        workflow: Dict = None,
        rag_params: Dict = None,
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
        # dynamic_mode: Literal["static", "dynamic"],
        concurrent_conversations: int,
    ) -> TestRun:
        raise NotImplementedError("Method not implemented")

    def get_test_run_results(test_run_identifier: str) -> TestRunResults:
        raise NotImplementedError("Method not implemented")


class Maihem(Client):

    def __init__(self) -> None:
        self.type = "sync"

    def create_target_agent(
        self,
        identifier: str,
        role: str,
        company: str,
        industry: str,
        description: str,
        workflow: Dict = None,
        rag_params: Dict = None,
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
        workflow: Dict = None,
        rag_params: Dict = None,
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
