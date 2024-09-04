from typing import Dict, Literal

from agents import AgentTarget
from test_objects import Test, TestRun, TestRunResults


class Client:
    
    def __init__(self):
        pass
    
    def create_target_agent(
        self,
        identifier: str,
        role: str,
        company: str,
        industry: str,
        description: str,
        workflow: Dict = {},
        rag_params: Dict = {}
    ) -> None:
        pass
    
    def get_target_agent(self, identifier: str) -> AgentTarget:
        pass
    
    def create_test(
        self,
        test_identifier: str,
        initiating_agent: Literal["maihem", "target"],
        agent_maihem_behavior_prompt: str = None,
        conversation_turns_max: int = 10,
        metrics_config: Dict = {}
    ) -> Test:
        pass

    def run_test(
        self,
        identifier: str,
        test_identifier: str,
        agent_target: AgentTarget,
        dynamic_mode: Literal["static", "dynamic"],              
        concurrent_conversations: int      
    ) -> TestRun:
        pass

    def get_test_run_results(test_run_identifier: str) -> TestRunResults:
        pass




class Maihem(Client):
    
    def __init__(self):
        pass
    
    
    
class MaihemAsync(Client):
    
    def __init__(self):
        pass