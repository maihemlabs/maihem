from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Mapping, ClassVar, Set, Callable
from dataclasses import dataclass


@dataclass
class InputMapping:
    """Maps standard input names to your function's parameter names.
    The attribute names are our standard interface, values are your function's parameter names.
    """

    def __init__(self, **kwargs: str):
        """
        Initialize with standard_name=your_param_name pairs.
        Example: InputMapping(query='user_input') means standard 'query' maps to your 'user_input' parameter
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._mapping = {v: k for k, v in kwargs.items()}  # Reverse the mapping

    def to_dict(self) -> Dict[str, str]:
        """Returns mapping from function param names to standard names."""
        return self._mapping


class MaihemEvaluator(ABC):
    # Class attributes defining the standard names expected by this connector
    EXPECTED_INPUTS: ClassVar[Set[str]] = set()
    NAME: ClassVar[str] = ""  # Connector name for identification

    def __init__(
        self,
        inputs: Optional[InputMapping] = None,
        output_fn: Optional[Callable[[Any], Any]] = None,
    ):
        """
        Initialize connector with optional input mappings and output transformation.

        Args:
            inputs: Maps your function's parameter names to our standard names.
                Use get_expected_inputs() to see what standard names are needed.
            output_fn: Optional function to transform the decorated function's output
                before standard output mapping. Useful when your function returns
                data in a different format than expected.
        """
        if not self.NAME:
            raise ValueError(f"Connector {self.__class__.__name__} must define NAME")

        self.input_mapping = inputs.to_dict() if inputs else {}
        self.output_fn = output_fn
        self._validate_mappings()

    def _validate_mappings(self) -> None:
        """Validates that all required mappings are provided and map to expected names."""
        if self.input_mapping:
            mapped_inputs = set(self.input_mapping.values())
            invalid_inputs = mapped_inputs - self.EXPECTED_INPUTS
            if invalid_inputs:
                raise ValueError(
                    f"Invalid input mappings: {invalid_inputs}. "
                    f"Expected inputs are: {self.EXPECTED_INPUTS}"
                )

    @classmethod
    def get_expected_inputs(cls) -> Set[str]:
        """Returns the set of standard input names this connector expects."""
        return cls.EXPECTED_INPUTS

    @classmethod
    def create_with_mapping_help(cls) -> None:
        """Prints help text showing what mappings this connector needs."""
        print(f"\nConnector: {cls.__name__}")
        print("\nExpected Inputs:")
        for input_name in sorted(cls.EXPECTED_INPUTS):
            print(f"  - {input_name}")
        print("\nExample usage:")
        example_inputs = {f"your_{name}": name for name in sorted(cls.EXPECTED_INPUTS)}
        print(
            f"""
@maihem(
    connector={cls.__name__}(
        inputs=InputMapping(
            {", ".join(f"{k}='{v}'" for k, v in example_inputs.items())}
        )
    )
)
"""
        )

    def _map_key(self, key: str, mapping: Mapping[str, str]) -> str:
        """Maps a key using the provided mapping, returns original if no mapping exists."""
        return mapping.get(key, key)

    def map_inputs(self, **kwargs) -> Dict[str, Any]:
        """Map function inputs to standardized names using input_mapping."""
        return {self._map_key(k, self.input_mapping): v for k, v in kwargs.items()}

    def map_outputs(self, result: Any) -> Dict[str, Any]:
        """Transform the function output to a standardized format."""
        if self.output_fn:
            result = self.output_fn(result)
        return self._transform_output(result)

    @abstractmethod
    def _transform_output(self, result: Any) -> Dict[str, Any]:
        """Transform the return value to a standardized format."""
        pass


class MaihemQA(MaihemEvaluator):
    """Question answering connector.

    Required Inputs:
        - query: str  # The question to answer

    Output Format:
        answer: str  # The answer to the question
    """

    NAME = "question_answering"
    EXPECTED_INPUTS = {"query", "documents"}

    class Inputs(InputMapping):
        query: str
        documents: list[str]

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"answer": result}


class MaihemIntent(MaihemEvaluator):
    """Intent recognition connector.

    Required Inputs:
        - query: str  # The text to classify intent from

    Output Format:
        intent: str  # The classified intent

    Example:
        @maihem(
            evaluator=MaihemIntent(
                inputs=InputMapping(query='user_input'),
                output_fn=lambda x: x['intent']  # Extract intent from dict
            )
        )
        async def my_intent(user_input: str) -> dict:
            return {"intent": "some_intent", "confidence": 0.9}
    """

    NAME = "intent_recognition"
    EXPECTED_INPUTS = {"query"}

    class Inputs(InputMapping):
        query: str

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"intent": result}


class MaihemNER(MaihemEvaluator):
    """Named Entity Recognition connector.

    Required Inputs:
        - query: str  # The text to extract entities from

    Output Format:
        entities: list[str]  # List of extracted entities
    """

    NAME = "name_entity_recognition"
    EXPECTED_INPUTS = {"query"}

    class Inputs(InputMapping):
        query: str

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"entities": result}


class MaihemRephrasing(MaihemEvaluator):
    """Query rephrasing connector.

    Required Inputs:
        - query: str  # The text to rephrase

    Output Format:
        rephrased_query: str  # The rephrased query
    """

    NAME = "query_rephrasing"
    EXPECTED_INPUTS = {"query"}

    class Inputs(InputMapping):
        query: str

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"rephrased_query": result}


class MaihemRetrieval(MaihemEvaluator):
    """Document retrieval connector.

    Required Inputs:
        - query: str  # The search query
        - entities: list[str]  # List of entities to use for retrieval

    Output Format:
        documents: list[str]  # Retrieved text chunks

    Example:
        @maihem(
            evaluator=MaihemRetrieval(
                inputs=InputMapping(
                    query='search_query',
                    entities='named_entities'
                ),
                output_fn=lambda x: x['documents']  # Extract documents from response
            )
        )
        async def my_retrieval(search_query: str, named_entities: list[str]) -> dict:
            return {
                "documents": ["doc1", "doc2"],
                "scores": [0.9, 0.8]
            }
    """

    NAME = "document_retrieval"
    EXPECTED_INPUTS = {"query", "entities"}

    class Inputs(InputMapping):
        query: str
        entities: list[str]

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"documents": result}


class MaihemReranking(MaihemEvaluator):
    """Document reranking connector.

    Required Inputs:
        - documents: list[str]  # List of documents to rerank

    Output Format:
        reranked_chunks: list[str]  # Reranked documents
    """

    NAME = "document_reranking"
    EXPECTED_INPUTS = {"documents"}

    class Inputs(InputMapping):
        documents: list[str]

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"reranked_chunks": result}


class MaihemFiltering(MaihemEvaluator):
    """Document filtering connector.

    Required Inputs:
        - documents: list[str]  # List of documents to filter

    Output Format:
        filtered_chunks: list[str]  # Filtered documents
    """

    NAME = "document_filtering"
    EXPECTED_INPUTS = {"documents"}

    class Inputs(InputMapping):
        documents: list[str]

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"filtered_chunks": result}


class MaihemFinalAnswer(MaihemEvaluator):
    """Final answer generation connector.

    Required Inputs:
        - query: str  # The original question
        - documents: list[str]  # The filtered documents to use for answering

    Output Format:
        answer: str  # The final answer
    """

    NAME = "answer_generation"
    EXPECTED_INPUTS = {"query", "documents"}

    class Inputs(InputMapping):
        query: str
        documents: list[str]

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"answer": result}
