from datetime import datetime
from pydantic import BaseModel

from enum import Enum
import os
from pydantic_extra_types.language_code import LanguageAlpha2
from typing import Callable, Optional, Tuple, List, Dict

import maihem.errors as errors
from maihem.logger import get_logger

logger = get_logger()


class AgentType(str, Enum):
    MAIHEM = "maihem"
    TARGET = "target"


class TargetAgent(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    label: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    language: Optional[LanguageAlpha2] = "en"

    _wrapper_function: Optional[Callable] = None
    document_paths: List[str] = []

    def set_wrapper_function(self, wrapper_function: Callable) -> None:
        is_test_success = self.test_wrapper_function(wrapper_function)

        if is_test_success:
            self._wrapper_function = wrapper_function
            logger.info("Wrapper function tested and added successfully")

    def test_wrapper_function(self, wrapper_function: Callable) -> bool:
        test_message = "Hi, it's the Maihem agent. Ready for testing?"
        logger.info("Testing wrapper function...")
        logger.info(f"Sending message to target agent: {test_message}")
        try:
            message, contexts = wrapper_function(str(datetime.now()), test_message, {})
            assert isinstance(message, str), "Response message must be a string"
            assert isinstance(contexts, list), "Contexts must be a list"
            for context in contexts:
                assert isinstance(
                    context, str
                ), "Each context in the list must be a string"

            return True
        except Exception as e:
            errors.raise_wrapper_function_error(
                f"Error testing target agent wrapper function: {e}"
            )

    def add_documents(self, documents: List[str]) -> None:
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
        self,
        conversation_id: str,
        message: Optional[str] = "",
        conversation_history: Dict = {},
    ) -> Tuple[str, List[str]]:
        if not self._wrapper_function:
            errors.raise_wrapper_function_error("Target agent wrapper function not set")
        for retry in range(3):
            try:
                response, contexts = self._wrapper_function(
                    conversation_id, message, conversation_history
                )
                return response, contexts
            except Exception as e:
                if retry < 2:
                    logger.warning(
                        f"Error sending message to target agent, retrying ({retry + 1}). Error: {str(e)}"
                    )
                else:
                    errors.raise_wrapper_function_error(
                        f"Error sending message to target agent after 3 retries. Error: {str(e)}"
                    )
