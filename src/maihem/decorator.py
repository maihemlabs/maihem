from maihem.evaluators import MaihemEvaluator
from maihem.otel_client import Tracer, trace
from maihem.utils.utils import validate_attributes_testing, extract_ids_from_query
from maihem.clients import Maihem
from maihem.utils.registry import register_function
from typing import Optional, Callable, Any, Tuple, Dict
import inspect
from functools import wraps, lru_cache
import orjson as json
import os
import logging


@lru_cache(maxsize=128)  # Increased cache size since it's now shared
def get_agent_target_id(
    agent_name: str, api_key: Optional[str] = None
) -> Optional[str]:
    """
    Retrieve the agent's target id (cached for performance).

    If api_key is not provided, picks it from the environment variable.
    """
    if not agent_name:
        return None
    if not api_key:
        api_key = os.getenv("MAIHEM_API_KEY")
    client = Maihem(env="local")  # TODO: change env to prod
    try:
        agent = client.get_target_agent(name=agent_name)
        return agent.id
    except Exception:
        return None


def _process_args_and_set_inputs(
    sig: inspect.Signature,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    evaluator: Optional[MaihemEvaluator],
    span: Any,
) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    """
    Bind and process the function arguments and update the span with the input payload.

    This function:
    - Binds the passed arguments using the cached signature.
    - Removes 'self' from the bound arguments.
    - Maps the inputs if an evaluator is provided.
    - Processes the 'query' parameter by extracting ids and converting
      the query to a "clean" version.
    - Sets the JSON-dumped representations of the payload on the span.

    Returns:
        Possibly modified (args, kwargs) after processing.
    """
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    filtered_arguments = {k: v for k, v in bound_args.arguments.items() if k != "self"}

    # Use evaluator to map inputs if available.
    input_payload = (
        evaluator.map_inputs(**filtered_arguments) if evaluator else filtered_arguments
    )

    # If a "query" parameter exists, process it.
    if "query" in input_payload:
        clean_query, ids = extract_ids_from_query(input_payload["query"])
        for key, value in ids.items():
            span.set_attribute(key, value)

        # Replace query in args and kwargs if found.
        args = tuple(
            clean_query if arg == input_payload["query"] else arg for arg in args
        )
        if evaluator:
            arg_name = next(
                (k for k, v in evaluator.input_mapping.items() if v == "query"), None
            )
            if arg_name and arg_name in kwargs:
                kwargs[arg_name] = clean_query
        input_payload["query"] = clean_query

    span.set_attribute("input_payload", json.dumps(input_payload))
    span.set_attribute("input_payload_raw", json.dumps(filtered_arguments))
    return args, kwargs


def _set_output_attributes(
    span: Any, result: Any, evaluator: Optional[MaihemEvaluator]
) -> Any:
    """
    Map (if applicable) and set the output payload on the span.

    Returns:
        The mapped output.
    """
    output_payload = evaluator.map_outputs(result) if evaluator else result
    span.set_attribute("output_payload", json.dumps(output_payload))
    span.set_attribute("output_payload_raw", json.dumps(result))
    return output_payload


def workflow(
    name: Optional[str] = None,
    agent_target: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
    api_key: Optional[str] = None,
) -> Callable:
    """
    Decorator that defines a workflow by creating a parent span.

    It caches agent target ids if provided and sets the relevant attributes on
    the span (workflow name, evaluator name, etc.).

    Raises:
        ValueError: If the workflow is called within another workflow (nested workflows
                   are not allowed).
    """

    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)
        cached_agent_id = (
            get_agent_target_id(agent_target, api_key) if agent_target else None
        )

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Check for parent span
                parent_span = trace.get_current_span()
                if parent_span.get_span_context().is_valid:
                    raise ValueError(
                        "Nested workflows are not allowed. The workflow decorator cannot "
                        "be used within another workflow."
                    )

                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name) as span:
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)
                    span.set_attribute("workflow_name", span_name)
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )

                    args, kwargs = _process_args_and_set_inputs(
                        sig, args, kwargs, evaluator, span
                    )
                    result = await func(*args, **kwargs)
                    _set_output_attributes(span, result, evaluator)
                    return result

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Check for parent span
                parent_span = trace.get_current_span()
                if parent_span.get_span_context().is_valid:
                    raise ValueError(
                        "Nested workflows are not allowed. The workflow decorator cannot "
                        "be used within another workflow."
                    )

                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name) as span:
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)
                    span.set_attribute("workflow_name", span_name)
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )

                    args, kwargs = _process_args_and_set_inputs(
                        sig, args, kwargs, evaluator, span
                    )
                    result = func(*args, **kwargs)
                    _set_output_attributes(span, result, evaluator)
                    return result

            return sync_wrapper

    return decorator


def workflow_step(
    name: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
) -> Callable:
    """
    Decorator that defines a step in a workflow, establishing a child/span within
    an existing workflow span.

    Note: It must be executed within a workflow (i.e. there must be an active parent span)
          and the parent span must not already be a child (nested too deeply).
    """

    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                parent_span = trace.get_current_span()
                if not parent_span.get_span_context().is_valid:
                    raise ValueError(
                        "workflow_step must be executed within a workflow decorated "
                        "function (no active parent span found)."
                    )
                # Check if the parent span already has a parent to avoid too deep nesting.
                parent_of_parent = getattr(parent_span, "parent", None)
                if parent_of_parent and parent_of_parent.is_valid:
                    raise ValueError(
                        "workflow_step cannot be nested more than one level; "
                        "the parent span already has a parent."
                    )

                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )

                    args, kwargs = _process_args_and_set_inputs(
                        sig, args, kwargs, evaluator, span
                    )
                    result = await func(*args, **kwargs)
                    _set_output_attributes(span, result, evaluator)
                    return result

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                parent_span = trace.get_current_span()
                if not parent_span.get_span_context().is_valid:
                    raise ValueError(
                        "workflow_step must be executed within a workflow decorated "
                        "function (no active parent span found)."
                    )
                # Check if the parent span already has a parent to avoid too deep nesting.
                parent_of_parent = getattr(parent_span, "parent", None)
                if parent_of_parent and parent_of_parent.get_span_context().is_valid:
                    raise ValueError(
                        "workflow_step cannot be nested more than one level; "
                        "the parent span already has a parent."
                    )

                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )

                    args, kwargs = _process_args_and_set_inputs(
                        sig, args, kwargs, evaluator, span
                    )
                    result = func(*args, **kwargs)
                    _set_output_attributes(span, result, evaluator)
                    return result

            return sync_wrapper

    return decorator
