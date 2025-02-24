from abc import ABC, abstractmethod, ABCMeta
from typing import (
    Any,
    Dict,
    Optional,
    Mapping,
    ClassVar,
    Set,
    Callable,
    get_type_hints,
    Type,
)
from pydantic import BaseModel  # Install via: pip install pydantic
import textwrap


# Optional: define a custom exception for InputMapping errors
class InputMappingError(TypeError):
    """Exception raised when InputMapping validation fails."""

    pass


# Use Pydantic for robust input mapping validation.
class InputMapping(BaseModel):
    """
    Maps standard input names to your function's parameter names.
    The attribute names represent the standard interface, and the values
    are your function's parameter names.

    Pydantic automatically validates the types based on the annotations.
    """

    def to_dict(self) -> Dict[str, str]:
        """
        Returns a mapping from your function's parameter names to the standard names.
        The reverse mapping is defined as: the value stored in the instance (i.e. your
        function parameter) maps to the field name (i.e. the standardized input).
        """
        # Use model_fields instead of __fields__ (deprecated in recent Pydantic versions)
        return {getattr(self, field): field for field in self.model_fields}

    class Config:
        # Disallow extra fields so that only annotated fields are allowed.
        extra = "forbid"


# Global registry for storing Evaluator classes
EVALUATOR_REGISTRY: Dict[str, Type["MaihemEvaluator"]] = {}


class EvaluatorMeta(ABCMeta):
    """
    Metaclass for MaihemEvaluator that automatically sets the
    EXPECTED_INPUTS from the inner Inputs class annotations.
    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        inputs_cls = getattr(cls, "Inputs", None)
        if inputs_cls:
            # Using get_type_hints ensures that forward references and other niceties are handled.
            cls.EXPECTED_INPUTS = set(get_type_hints(inputs_cls).keys())
        else:
            cls.EXPECTED_INPUTS = set()
        # Register evaluator classes with a non-empty NAME
        if cls.NAME:
            if cls.NAME in EVALUATOR_REGISTRY:
                raise ValueError(f"Duplicate evaluator name: {cls.NAME}")
            EVALUATOR_REGISTRY[cls.NAME] = cls


class MaihemEvaluator(ABC, metaclass=EvaluatorMeta):
    # Connector name for identification must be defined in each subclass.
    NAME: ClassVar[str] = ""
    EXPECTED_INPUTS: Set[str] = set()  # Default for static type-checking

    def __init__(
        self,
        inputs: Optional[InputMapping] = None,
        output_fn: Optional[Callable[[Any], Any]] = None,
    ) -> None:
        """
        Initialize connector with optional input mapping and output transformation.

        Args:
            inputs: Maps your function's parameter names to our standard names. Use
                get_expected_inputs() to see what standard inputs are needed.
            output_fn: Optional function to transform the decorated function's output
                before standard output mapping.
        """
        if not self.NAME:
            raise ValueError(f"Connector {self.__class__.__name__} must define NAME")

        self.input_mapping: Dict[str, str] = inputs.to_dict() if inputs else {}
        self.output_fn = output_fn
        self._validate_mappings()

    def _validate_mappings(self) -> None:
        """
        Validates that all provided input mappings are among the expected inputs.
        """
        if self.input_mapping:
            # The mapping's values are the standard input names.
            mapped_inputs = set(self.input_mapping.values())
            invalid_inputs = mapped_inputs - self.EXPECTED_INPUTS
            if invalid_inputs:
                raise ValueError(
                    f"Invalid input mappings: {invalid_inputs}. "
                    f"Expected inputs are: {self.EXPECTED_INPUTS}"
                )

    @classmethod
    def get_expected_inputs(cls) -> Set[str]:
        """
        Returns the set of standard input names that this connector expects.
        """
        return cls.EXPECTED_INPUTS

    @classmethod
    def create_with_mapping_help(cls) -> None:
        """
        Prints help text showing what mappings this connector needs.
        """
        print(f"\nConnector: {cls.__name__}\n")
        print("Expected Inputs:")
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

    def map_inputs(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Map function inputs to standardized names using the provided input mapping.
        Only inputs with an explicit mapping are included.
        """
        return {
            self.input_mapping[k]: v
            for k, v in kwargs.items()
            if k in self.input_mapping
        }

    def map_outputs(self, result: Any) -> Dict[str, Any]:
        """
        Transform the function output to a standardized format.
        Optionally applies the defined output transformation.
        """
        if self.output_fn:
            result = self.output_fn(result)
        return self._transform_output(result)

    @abstractmethod
    def _transform_output(self, result: Any) -> Dict[str, Any]:
        """
        Transform the return value to a standardized format. Must be implemented
        by subclasses.
        """
        pass

    def _generate_function_wrapper(self, function_name: str) -> str:
        """
        Generate a wrapper code snippet for the connector function.
        (In practice, you might return a callable or write this to a file.)
        """
        # Get type hints from the inner Inputs class.
        inputs_hints = get_type_hints(self.Inputs)
        args_str = ", ".join(
            f"{k}: {v.__name__ if hasattr(v, '__name__') else str(v)}"
            for k, v in inputs_hints.items()
        )
        required_inputs = "\n\t".join(
            f"- {k}: {v.__name__ if hasattr(v, '__name__') else str(v)}"
            for k, v in inputs_hints.items()
        )
        params = ", ".join(inputs_hints.keys())

        wrapper_code = textwrap.dedent(
            f"""\
            ###### {self.NAME} Wrapper ######
            
            # Add imports here
            # import my_{self.NAME}
            
            
            def {function_name}_wrapper({args_str}):
                \"\"\"Wrapper for {self.NAME} step.
                
                Required Inputs:
                {required_inputs}
                \"\"\"
                
                ##### YOUR CODE HERE #####
                # my_{self.NAME}({params})
            """
        )
        return wrapper_code


class MaihemQA(MaihemEvaluator):
    """Question answering connector.

    Output Format:
        answer: str  # The answer to the question
    """

    NAME = "question_answering"

    class Inputs(InputMapping):
        """
        Input mapping for the Question Answering connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
        """

        query: str

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"answer": result}


class MaihemIntent(MaihemEvaluator):
    """Intent recognition connector.

    Output Format:
        intent: str  # The classified intent
    """

    NAME = "intent_recognition"

    class Inputs(InputMapping):
        """
        Input mapping for the Intent Recognition connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
        """

        query: str

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"intent": result}


class MaihemNER(MaihemEvaluator):
    """Named Entity Recognition connector.

    Output Format:
        entities: list[str]  # List of extracted entities
    """

    NAME = "name_entity_recognition"

    class Inputs(InputMapping):
        """
        Input mapping for the Named Entity Recognition connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
        """

        query: str

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"entities": result}


class MaihemRephrasing(MaihemEvaluator):
    """Query rephrasing connector.

    Output Format:
        rephrased_query: str  # The rephrased query
    """

    NAME = "query_rephrasing"

    class Inputs(InputMapping):
        """
        Input mapping for the Query Rephrasing connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
        """

        query: str

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"rephrased_query": result}


class MaihemRetrieval(MaihemEvaluator):
    """Document retrieval connector.

    Output Format:
        documents: list[str]  # Retrieved text chunks
    """

    NAME = "document_retrieval"

    class Inputs(InputMapping):
        """
        Input mapping for the Document Retrieval connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
        """

        query: str

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"documents": result}


class MaihemReranking(MaihemEvaluator):
    """Document reranking connector.

    Output Format:
        reranked_documents: list[str]  # Reranked documents
    """

    NAME = "document_reranking"

    class Inputs(InputMapping):
        """
        Input mapping for the Document Reranking connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
            documents (str): The name of the argument that contains the documents as a list of strings.
        """

        query: str
        documents: str

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"reranked_documents": result}


class MaihemFiltering(MaihemEvaluator):
    """Document filtering connector.

    Output Format:
        filtered_documents: list[str]  # Filtered documents
    """

    NAME = "document_filtering"

    class Inputs(InputMapping):
        """
        Input mapping for the Document Filtering connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
            documents (str): The name of the argument that contains the documents as a list of strings.
        """

        query: str
        documents: str

    def _transform_output(self, result: list[str]) -> Dict[str, Any]:
        return {"filtered_documents": result}


class MaihemFinalAnswer(MaihemEvaluator):
    """Final answer generation connector.

    Output Format:
        answer: str  # The final answer
    """

    NAME = "answer_generation"

    class Inputs(InputMapping):
        """
        Input mapping for the Final Answer Generation connector.

        Attributes:
            query (str): The name of the argument that contains the query as a string.
            documents (str): The name of the argument that contains the documents as a list of strings.
        """

        query: str
        documents: str

    def _transform_output(self, result: str) -> Dict[str, Any]:
        return {"answer": result}
