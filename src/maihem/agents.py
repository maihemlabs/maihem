from typing import Callable


class AgentTarget:
    
    def __init__(self):
        self.chat_function = None
    
    def set_chat_function(self, chat_function: Callable) -> None:
        self.chat_function = chat_function