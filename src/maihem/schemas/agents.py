from datetime import datetime
from pydantic import BaseModel
from typing import Callable, Optional

from enum import Enum

from pydantic_extra_types.language_code import LanguageAlpha2
from maihem.errors import ChatFunctionError


class AgentTarget(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    identifer: str
    name: Optional[str] = None
    role: str
    description: Optional[str] = None
    industry: Optional[str] = None
    behaviour_prompt: Optional[str] = None
    language: Optional[LanguageAlpha2] = "en"

    class Config:
        allow_population_by_field_name = True

    chat_function: Optional[Callable] = None

    def set_chat_function(self, chat_function: Callable) -> None:
        self.test_chat_function()
        self.chat_function = chat_function

    def test_chat_function(self) -> None:
        try:
            message, end_code = self.chat_function(
                str(datetime.now()), "Testing target agent function...", None
            )
            assert isinstance(message, str), "Response message must be a string"
            assert isinstance(end_code, str), "End conversation flag must be a string"
        except Exception as e:
            raise ChatFunctionError(f"Chat function test failed: {e}") from e


class AgentType(str, Enum):
    MAIHEM = "maihem"
    TARGET = "target"
