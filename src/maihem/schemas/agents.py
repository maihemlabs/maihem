import asyncio
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import os
from pydantic_extra_types.language_code import LanguageAlpha2
from typing import Optional, Tuple, List, Dict, Coroutine
import json
import importlib

from maihem.otel_client import Tracer
import maihem.shared.lib.errors as errors
from maihem.shared.lib.logger import get_logger

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

    _wrapper_function: Optional[Coroutine] = None
    _wrapped_function_name: Optional[str] = None
    _workflow_name: Optional[str] = None
    document_paths: List[str] = []

    def set_wrapper_function(
        self,
        function_name: str,
        test_name: str,
        workflow_name: Optional[str] = None,
    ) -> None:
        """Dynamically imports and sets the wrapper function based on workflow name"""
        try:
            # Import the wrappers module
            wrappers = importlib.import_module(f"test_{test_name}.wrapper_functions")

            # Get the wrapper function name by prepending 'wrapper_' to workflow name
            wrapper_func_name = f"{function_name}_wrapper"

            # Get the function from the module
            if hasattr(wrappers, wrapper_func_name):
                self._wrapper_function = getattr(wrappers, wrapper_func_name)
                self._wrapped_function_name = function_name
                self._workflow_name = workflow_name
                logger.info(f"Wrapper function '{wrapper_func_name}' set successfully")
            else:
                raise AttributeError(
                    f"Wrapper function '{wrapper_func_name}' not found in wrappers.py"
                )

        except ImportError as e:
            raise ImportError(f"Could not import wrappers module: {str(e)}")
        except Exception as e:
            raise Exception(f"Error setting wrapper function: {str(e)}")

    def _test_wrapper_function(self, wrapper_function: Coroutine) -> bool:
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
                logger=logger,
                message=f"Error testing target agent wrapper function: {e}",
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

    def _call_workflow(
        self,
        conversation_id: str,
        conversation_message_id: str,
        message: Optional[str] = "",
        conversation_history: Dict = {},
        test_run_id: Optional[str] = None,
        target_agent_revision_id: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> Tuple[str, List[str]]:
        if not self._wrapper_function:
            errors.raise_wrapper_function_error(
                logger=logger, message="Target agent wrapper function not set"
            )
        for retry in range(3):
            try:
                data = {
                    "query": message,
                    "maihem_ids": {
                        "conversation_id": conversation_id,
                        "conversation_message_id": conversation_message_id,
                        "test_run_id": test_run_id,
                        "agent_target_revision_id": target_agent_revision_id,
                        "environment": environment,
                    },
                }
                message_with_ids = json.dumps(data)

                kwargs = {
                    "conversation_id": conversation_id,
                    "user_input": message_with_ids or message,
                    "conversation_history": conversation_history,
                }

                response = asyncio.run(self._wrapper_function(**kwargs))
                return response
            except Exception as e:
                if retry < 2:
                    logger.warning(
                        f"Error sending message to target agent, retrying ({retry + 1}). Error: {str(e)}"
                    )
                else:
                    errors.raise_wrapper_function_error(
                        logger=logger,
                        message=f"Error sending message to target agent after 3 retries. Error: {str(e)}",
                    )

    def _call_step(
        self,
        interaction_id: str,
        target_agent_id: str,
        test_run_id: str,
        kwargs: Dict,
        target_agent_revision_id: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> Tuple[str, List[str]]:
        if not self._wrapper_function:
            errors.raise_wrapper_function_error(
                logger=logger, message="Target agent wrapper function not set"
            )
        for retry in range(3):
            try:

                tracer = Tracer.get_instance().tracer
                # span_name = self._wrapped_function_name
                with tracer.start_as_current_span(self._workflow_name) as span:
                    span.set_attribute("workflow_trace_id", interaction_id)
                    span.set_attribute("test_run_id", test_run_id)
                    span.set_attribute("agent_target_id", target_agent_id)
                    span.set_attribute("workflow_name", self._workflow_name)
                    span.set_attribute("workflow_step_name", self._workflow_name)
                    if target_agent_revision_id:
                        span.set_attribute(
                            "agent_target_revision_id", target_agent_revision_id
                        )
                    if environment:
                        span.set_attribute("environment", environment)

                    # Call the step wrapper function
                    response = asyncio.run(self._wrapper_function(**kwargs))
                tracer.span_processor.force_flush()
                return response
            except Exception as e:
                if retry < 2:
                    logger.warning(
                        f"Error sending message to target agent, retrying ({retry + 1}). Error: {str(e)}"
                    )
                else:
                    errors.raise_wrapper_function_error(
                        logger=logger,
                        message=f"Error sending message to target agent after 3 retries. Error: {str(e)}",
                    )
