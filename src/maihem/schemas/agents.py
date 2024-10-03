from datetime import datetime
from pydantic import BaseModel

from enum import Enum
import os
from pydantic_extra_types.language_code import LanguageAlpha2
from typing import Callable, Optional, Tuple, List, Dict

import maihem.errors as errors
from maihem.logger import get_logger
from maihem.utils import extract_text


class AgentType(str, Enum):
    MAIHEM = "maihem"
    TARGET = "target"


class TargetAgent(BaseModel):
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
    document_paths: List[str] = []

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

    def add_documents(self, documents: List[str]) -> None:
        logger = get_logger()
        for doc_path in documents:
            if not os.path.exists(doc_path):
                logger.warning(f"Document not found: {doc_path}")
                continue

            if not os.path.isfile(doc_path):
                logger.warning(f"Path is not a file: {doc_path}")
                continue

            file_size = os.path.getsize(doc_path)
            if file_size == 0:
                logger.warning(f"File is empty: {doc_path}")
                continue

            if file_size > 10 * 1024 * 1024:  # 10 MB limit
                logger.warning(f"File is too large (>10MB): {doc_path}")
                continue

            try:
                self.document_paths.append(doc_path)
                logger.info(f"Added document: {doc_path}")
            except Exception as e:
                logger.error(f"Error processing document {doc_path}: {str(e)}")

    def _send_message(
        self, conversation_id: str, message: Optional[str] = ""
    ) -> Tuple[str, List[str]]:
        if not self._chat_function:
            errors.raise_chat_function_error("Target agent chat function not set")
        response, contexts = self._chat_function(conversation_id, message)
        return response, contexts
