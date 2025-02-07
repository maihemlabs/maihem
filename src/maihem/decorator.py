from maihem.evaluators import MaihemEvaluator
from maihem.otel_client import Tracer, trace
from maihem.utils.utils import validate_attributes_testing, extract_ids_from_query
from maihem.clients import Maihem
from maihem.utils.registry import register_function
from typing import Optional, Callable, Any
import inspect
from functools import wraps, lru_cache
import orjson as json
import os


# Move the cached function outside to make it module-level
@lru_cache(maxsize=128)  # Increased cache size since it's now shared
def get_agent_target_id(
    agent_name: str, api_key: Optional[str] = None
) -> Optional[str]:
    if not agent_name:
        return None
    if not api_key:
        api_key = os.getenv("MAIHEM_API_KEY")
    client = Maihem(api_key=api_key, env="local")  # TODO: change env to prod
    try:
        agent = client.get_target_agent(name=agent_name)
        return agent.id
    except Exception:
        return None


# New workflow decorator to create the parent span for a workflow.
def workflow(
    name: Optional[str] = None,
    agent_target: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
    api_key: Optional[str] = None,
):
    def decorator(func: Callable) -> Callable:
        # Cache agent_target id if provided
        cached_agent_id = (
            get_agent_target_id(agent_target, api_key) if agent_target else None
        )

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__

                with tracer.start_as_current_span(span_name) as span:
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)

                    # Set workflow (parent) span attributes
                    span.set_attribute("workflow_name", span_name)
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )
                    try:
                        bound_args = inspect.signature(func).bind(*args, **kwargs)
                        bound_args.apply_defaults()

                        # Exclude 'self' from the arguments if present.
                        filtered_arguments = {
                            k: v for k, v in bound_args.arguments.items() if k != "self"
                        }

                        if evaluator:
                            input_payload = evaluator.map_inputs(**filtered_arguments)
                        else:
                            input_payload = filtered_arguments

                        if "query" in input_payload:
                            clean_query, ids = extract_ids_from_query(
                                input_payload["query"]
                            )

                            for key, value in ids.items():
                                span.set_attribute(key, value)

                            # Convert args tuple to list for modification
                            args_list = list(args)
                            for i, arg in enumerate(args_list):
                                if arg == input_payload["query"]:
                                    args_list[i] = clean_query
                            args = tuple(args_list)

                            # Look for kwarg name in evaluator.input_mapping
                            arg_name = None
                            if evaluator:
                                for k, v in evaluator.input_mapping.items():
                                    if v == "query":
                                        arg_name = k
                                if arg_name and arg_name in kwargs:
                                    kwargs[arg_name] = clean_query

                            input_payload["query"] = clean_query

                        span.set_attribute("input_payload", json.dumps(input_payload))
                        result = await func(*args, **kwargs)

                        if evaluator:
                            output_payload = evaluator.map_outputs(result)
                        else:
                            output_payload = result

                        span.set_attribute("output_payload", json.dumps(output_payload))
                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                        raise

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
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

                    try:
                        bound_args = inspect.signature(func).bind(*args, **kwargs)
                        bound_args.apply_defaults()

                        # Exclude 'self' from the arguments if present.
                        filtered_arguments = {
                            k: v for k, v in bound_args.arguments.items() if k != "self"
                        }

                        if evaluator:
                            input_payload = evaluator.map_inputs(**filtered_arguments)
                        else:
                            input_payload = filtered_arguments

                        if "query" in input_payload:
                            print(input_payload["query"])
                            clean_query, ids = extract_ids_from_query(
                                input_payload["query"]
                            )
                            print(clean_query, ids)

                            for key, value in ids.items():
                                span.set_attribute(key, value)

                            args_list = list(args)
                            for i, arg in enumerate(args_list):
                                if arg == input_payload["query"]:
                                    args_list[i] = clean_query
                            args = tuple(args_list)

                            arg_name = None
                            if evaluator:
                                for k, v in evaluator.input_mapping.items():
                                    if v == "query":
                                        arg_name = k
                                if arg_name and arg_name in kwargs:
                                    kwargs[arg_name] = clean_query

                            input_payload["query"] = clean_query

                        span.set_attribute("input_payload", json.dumps(input_payload))
                        result = func(*args, **kwargs)

                        if evaluator:
                            output_payload = evaluator.map_outputs(result)
                        else:
                            output_payload = result

                        span.set_attribute("output_payload", json.dumps(output_payload))
                        return result

                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                        raise

            return sync_wrapper

    return decorator


# -----------------------------------------------------------------------------
# New workflow_step decorator to create a child span within a workflow.
def workflow_step(
    name: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
):
    def decorator(func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__

                with tracer.start_as_current_span(span_name) as span:
                    # Set the child span attribute for a workflow step.
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )

                    try:
                        bound_args = inspect.signature(func).bind(*args, **kwargs)
                        bound_args.apply_defaults()

                        # Exclude 'self' from the arguments if present.
                        filtered_arguments = {
                            k: v for k, v in bound_args.arguments.items() if k != "self"
                        }

                        if evaluator:
                            input_payload = evaluator.map_inputs(**filtered_arguments)
                        else:
                            input_payload = filtered_arguments

                        span.set_attribute("input_payload", json.dumps(input_payload))
                        result = await func(*args, **kwargs)

                        if evaluator:
                            output_payload = evaluator.map_outputs(result)
                        else:
                            output_payload = result

                        span.set_attribute("output_payload", json.dumps(output_payload))
                        return result

                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                        raise

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                parent_span = trace.get_current_span()

                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name", evaluator.NAME if evaluator else None
                    )

                    try:
                        bound_args = inspect.signature(func).bind(*args, **kwargs)
                        bound_args.apply_defaults()

                        # Exclude 'self' from the arguments if present.
                        filtered_arguments = {
                            k: v for k, v in bound_args.arguments.items() if k != "self"
                        }

                        if evaluator:
                            input_payload = evaluator.map_inputs(**filtered_arguments)
                        else:
                            input_payload = filtered_arguments

                        span.set_attribute("input_payload", json.dumps(input_payload))
                        result = func(*args, **kwargs)

                        if evaluator:
                            output_payload = evaluator.map_outputs(result)
                        else:
                            output_payload = result

                        span.set_attribute("output_payload", json.dumps(output_payload))
                        return result

                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                        raise

            return sync_wrapper

    return decorator
