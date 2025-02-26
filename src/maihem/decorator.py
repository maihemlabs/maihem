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


def safe_serialize_input(data: Any) -> str:
    """
    Try to JSON-serialize the input.

    If JSON serialization fails and the data is a dict, try to iterate through each key/value:
    if an individual value fails, use its repr. For non-dict data fall back to repr.
    """
    try:
        return json.dumps(data)
    except Exception:
        if isinstance(data, dict):
            safe_data = {}
            for key, value in data.items():
                try:
                    # Try to safely serialize each value
                    safe_data[key] = json.loads(json.dumps(value))
                except Exception:
                    safe_data[key] = repr(value)
            try:
                return json.dumps(safe_data)
            except Exception:
                return repr(safe_data)
        return repr(data)


def safe_serialize_output(data: Any) -> str:
    """
    Try to JSON-serialize the output.

    If serialization fails, simply return a repr of the data.
    """
    try:
        return json.dumps(data)
    except Exception:
        return repr(data)


@lru_cache(maxsize=128)  # Increased cache size since it's now shared
def get_agent_target_id(
    target_agent_name: str, api_key: Optional[str] = None
) -> Optional[str]:
    """
    Retrieve the agent's target id (cached for performance).

    If api_key is not provided, picks it from the environment variable.
    """
    if not target_agent_name:
        return None
    if not api_key:
        api_key = os.getenv("MAIHEM_API_KEY")
    client = Maihem(env="local")  # TODO: change env to prod
    try:
        agent = client.get_target_agent(name=target_agent_name)
        return agent.id
    except Exception:
        return None


@lru_cache(maxsize=128)
def get_agent_target_revision_id(
    target_agent_name: str, target_agent_revision_name: str
) -> Optional[str]:
    """
    Retrieve the agent's target id (cached for performance).

    """
    if not target_agent_revision_name:
        return None
    client = Maihem(env="local")  # TODO: change env to prod
    try:
        revision_id = client._get_target_agent_revision_id(
            target_agent_id=get_agent_target_id(target_agent_name),
            revision_name=target_agent_revision_name,
        )
        return revision_id
    except Exception:
        return None


def _process_args_and_set_inputs(
    sig: inspect.Signature,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    evaluator: Optional[MaihemEvaluator],
    span: Any,
    span_name: str,
    is_parent_span: bool = True,
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

    span.set_attribute("workflow_step_name", span_name)
    span.set_attribute("evaluator_name", evaluator.NAME if evaluator else None)
    span.set_attribute("input_payload", safe_serialize_input(input_payload))
    span.set_attribute("input_payload_raw", safe_serialize_input(filtered_arguments))

    if is_parent_span:
        span.set_attribute("workflow_name", span_name)

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
                    (k for k, v in evaluator.input_mapping.items() if v == "query"),
                    None,
                )
                if arg_name and arg_name in kwargs:
                    kwargs[arg_name] = clean_query
            input_payload["query"] = clean_query
    else:
        span.set_attribute("entity_type", "workflow_step")

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
    span.set_attribute("output_payload", safe_serialize_output(output_payload))
    span.set_attribute("output_payload_raw", safe_serialize_output(result))
    return output_payload


def workflow_step(
    name: Optional[str] = None,
    target_agent_name: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
    api_key: Optional[str] = None,
) -> Callable:
    """
    Merged decorator that behaves as a workflow or a workflow step depending on context.

    - If no active parent span is present, it creates a top-level workflow span and (if provided)
      sets the agent_target_id attribute.
    - If an active parent span exists, it creates a child span (workflow step).
      It raises an error if the active span already has a parent (i.e. nested too deeply).

    Supports both asynchronous and synchronous functions.
    """

    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                parent_span = trace.get_current_span()
                if parent_span.get_span_context().is_valid:
                    # Active span present so treat this as a workflow step
                    is_parent_span = False
                    cached_agent_id = None
                    cached_agent_target_revision_id = None
                    environment = None
                else:
                    # No active span; create a top-level workflow
                    is_parent_span = True
                    cached_agent_id = (
                        get_agent_target_id(target_agent_name, api_key)
                        if target_agent_name
                        else None
                    )
                    environment = os.getenv("MAIHEM_ENVIRONMENT")
                    revision_name = os.getenv("MAIHEM_TARGET_AGENT_REVISION")
                    cached_agent_target_revision_id = get_agent_target_revision_id(
                        target_agent_name, revision_name
                    )

                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name) as span:
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)
                    if environment:
                        span.set_attribute("environment", environment)
                    if cached_agent_target_revision_id:
                        span.set_attribute(
                            "agent_target_revision_id", cached_agent_target_revision_id
                        )

                    new_args, new_kwargs = _process_args_and_set_inputs(
                        sig,
                        args,
                        kwargs,
                        evaluator,
                        span,
                        span_name,
                        is_parent_span,
                    )
                    result = await func(*new_args, **new_kwargs)
                    _set_output_attributes(span, result, evaluator)
                if not parent_span.get_span_context().is_valid:
                    tracer.span_processor.force_flush()
                return result

            return async_wrapper
        else:

            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                parent_span = trace.get_current_span()
                if parent_span.get_span_context().is_valid:
                    # Active span present so treat this as a workflow step
                    is_parent_span = False
                    cached_agent_id = None
                else:
                    # No active span; create a top-level workflow
                    is_parent_span = True
                    cached_agent_id = (
                        get_agent_target_id(target_agent_name, api_key)
                        if target_agent_name
                        else None
                    )

                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name) as span:
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)
                    new_args, new_kwargs = _process_args_and_set_inputs(
                        sig,
                        args,
                        kwargs,
                        evaluator,
                        span,
                        span_name,
                        is_parent_span,
                    )
                    result = func(*new_args, **new_kwargs)
                    _set_output_attributes(span, result, evaluator)
                    if not parent_span.get_span_context().is_valid:
                        tracer.span_processor.force_flush()
                    return result

            return sync_wrapper

    return decorator
