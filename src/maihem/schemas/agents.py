from datetime import datetime
from pydantic import BaseModel
from typing import Callable, Optional, Tuple, List
import maihem.errors as errors

from enum import Enum
from maihem.logger import get_logger

from pydantic_extra_types.language_code import LanguageAlpha2


class AgentTarget(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    identifier: str
    name: Optional[str] = None
    role: str
    description: Optional[str] = None
    industry: Optional[str] = None
    language: Optional[LanguageAlpha2] = "en"

    _chat_function: Optional[Callable] = None

    def set_chat_function(self, chat_function: Callable) -> None:
        logger = get_logger()
        is_test_success = self.test_chat_function(chat_function)

        if is_test_success:
            self._chat_function = chat_function
            logger.info("Chat function tested and added successfully!")

    def test_chat_function(self, chat_function: Callable) -> bool:
        logger = get_logger()
        test_message = "Hi, it's the Maihem agent. Ready for testing?"
        logger.info("Testing chat function...")
        logger.info(f"Sending chatbot message: {test_message}")
        try:
            message, contexts = chat_function(
                str(datetime.now()),
                test_message,
            )
            assert isinstance(message, str), "Response message must be a string"
            assert isinstance(contexts, list), "Contexts must be a list"
            for context in contexts:
                assert isinstance(
                    context, str
                ), "Each context in the list must be a string"

            return True
        except Exception as e:
            errors.raise_chat_function_error(
                f"Error testing target agent chat function: {e}"
            )

    def _send_message(
        self, conversation_id: str, message: str
    ) -> Tuple[str, List[str]]:
        if not self._chat_function:
            errors.raise_chat_function_error("Target agent chat function not set")
        response, contexts = self._chat_function(conversation_id, message)
        return response, contexts


class AgentType(str, Enum):
    MAIHEM = "maihem"
    TARGET = "target"
