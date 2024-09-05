from datetime import datetime
from pydantic import BaseModel
from typing import Callable, Dict, Optional

from errors import ExceptionChatFunction


class AgentTarget(BaseModel):
    
    identifier: str
    role: str
    company: str
    industry: str
    description: str
    workflow: Dict
    rag_params: Dict

    chat_function: Optional[Callable] = None
    
    def set_chat_function(self, chat_function: Callable) -> None:
        self.test_chat_function()
        self.chat_function = chat_function
        
        
    def test_chat_function(self) -> None:
        try:
            message, end = self.chat_function(str(datetime.now()), "Testing target agent function...", None)
            assert isinstance(message, str), "Response message must be a string"
            assert isinstance(end, str), "End conversation flag must be a string"
        except Exception as e:
            raise ExceptionChatFunction(f"Error in chat function: {e}")
        
        
        
class AgentMaihem:
    
    
    def __init__(
        self, 
        identifier: str,
        workflow: Dict, 
        behavior_prompt: str, 
        metrics: str,
        agent_target: AgentTarget
    ) -> None:
        self.id = id
        self.workflow = workflow
        self.behavior_prompt = behavior_prompt
        self.metric = metrics
    
    
    agent_maihem = AgentMaihem(
    id="unique_id",                   # Unique ID for the maihem agent
    workflow={},                      # Optional, to describe the workflow of the target agent to test
    behavior_prompt="Clarify cancelation policies", # Prompt to guide behavior of maihem agents in test
    metrics=metrics,                  # Metrics to evaluate the agent
)

agent_maihem.chat(
    id_conversation="unique_id_conversation", # Unique ID for the conversation, to start a new one or to continue an existing one
    target_agent_msg="<msg/None>",    # Message from the target agent
    end=True,                         # True if the conversation should end, False if it should continue
)