from maihem.evaluators import MaihemEvaluator
from maihem.otel_client import Tracer, trace
from maihem.utils.utils import validate_attributes_testing, extract_ids_from_query
from maihem.clients import Maihem
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


def observe(
    name: Optional[str] = None,
    agent_target: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
    api_key: Optional[str] = None,
):
    def decorator(func: Callable) -> Callable:
        # Store the cached id at decorator level
        cached_agent_id = (
            get_agent_target_id(agent_target, api_key) if agent_target else None
        )

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                parent_span = trace.get_current_span()

                with tracer.start_as_current_span(span_name) as span:
                    # Use cached agent_target_id
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)

                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name",
                        evaluator.NAME if evaluator else None,
                    )

                    if parent_span is None or not parent_span.is_recording():
                        try:
                            if getattr(async_wrapper, "testing", False):
                                validate_attributes_testing(async_wrapper)
                        except ValueError as e:
                            span.record_exception(e)
                            span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                            raise

                        monitoring_attrs = {
                            "agent_target_id": getattr(
                                async_wrapper, "agent_target_id", None
                            ),
                            "test_run_id": getattr(async_wrapper, "test_run_id", None),
                            "workflow_name": "workflow_name",
                            "conversation_id": getattr(
                                async_wrapper, "conversation_id", None
                            ),
                            "conversation_message_id": getattr(
                                async_wrapper, "conversation_message_id", None
                            ),
                        }
                        for key, value in monitoring_attrs.items():
                            if value is not None:
                                span.set_attribute(key, value)

                    try:
                        bound_args = inspect.signature(func).bind(*args, **kwargs)
                        bound_args.apply_defaults()

                        # Use connector to map inputs if provided
                        if evaluator:
                            input_payload = evaluator.map_inputs(**bound_args.arguments)
                        else:
                            input_payload = dict(bound_args.arguments)
                        if "query" in input_payload.keys():
                            print(input_payload["query"])
                            clean_query, ids = extract_ids_from_query(
                                input_payload["query"]
                            )
                            print(clean_query, ids)
                            for key, value in ids.items():
                                span.set_attribute(key, value)

                            # Convert args tuple to list for modification
                            args_list = list(args)
                            for i, arg in enumerate(args_list):
                                if arg == input_payload["query"]:
                                    args_list[i] = clean_query

                            # Convert back to tuple
                            args = tuple(args_list)

                            # look for kwarg name in eval mapping
                            arg_name = None
                            for k, v in evaluator.input_mapping.items():
                                if v == "query":
                                    arg_name = k

                            if arg_name and arg_name in kwargs.keys():
                                kwargs[arg_name] = clean_query

                            input_payload["query"] = clean_query

                        span.set_attribute("input_payload", json.dumps(input_payload))

                        result = await func(*args, **kwargs)

                        # Use connector to map outputs if provided
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
                    # Use cached agent_target_id
                    if cached_agent_id:
                        span.set_attribute("agent_target_id", cached_agent_id)

                    span.set_attribute("workflow_step_name", span_name)
                    span.set_attribute(
                        "evaluator_name",
                        evaluator.NAME if evaluator else None,
                    )

                    if parent_span is None or not parent_span.is_recording():
                        try:
                            if getattr(sync_wrapper, "testing", False):
                                validate_attributes_testing(sync_wrapper)
                        except ValueError as e:
                            span.record_exception(e)
                            span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                            raise

                        monitoring_attrs = {
                            "agent_target_id": getattr(
                                sync_wrapper, "agent_target_id", None
                            ),
                            "test_run_id": getattr(sync_wrapper, "test_run_id", None),
                            "workflow_name": "workflow_name",
                            "conversation_id": getattr(
                                sync_wrapper, "conversation_id", None
                            ),
                            "conversation_message_id": getattr(
                                sync_wrapper, "conversation_message_id", None
                            ),
                        }
                        for key, value in monitoring_attrs.items():
                            if value is not None:
                                span.set_attribute(key, value)

                    try:
                        bound_args = inspect.signature(func).bind(*args, **kwargs)
                        bound_args.apply_defaults()

                        # Use connector to map inputs if provided
                        if evaluator:
                            input_payload = evaluator.map_inputs(**bound_args.arguments)
                        else:
                            input_payload = dict(bound_args.arguments)

                        if "query" in input_payload.keys():
                            print(input_payload["query"])
                            clean_query, ids = extract_ids_from_query(
                                input_payload["query"]
                            )
                            print(clean_query, ids)
                            for key, value in ids.items():
                                span.set_attribute(key, value)

                            # Convert args tuple to list for modification
                            args_list = list(args)
                            for i, arg in enumerate(args_list):
                                if arg == input_payload["query"]:
                                    args_list[i] = clean_query

                            # Convert back to tuple
                            args = tuple(args_list)

                            # look for kwarg name in eval mapping
                            arg_name = None
                            for k, v in evaluator.input_mapping.items():
                                if v == "query":
                                    arg_name = k

                            if arg_name and arg_name in kwargs.keys():
                                kwargs[arg_name] = clean_query

                            input_payload["query"] = clean_query

                        span.set_attribute("input_payload", json.dumps(input_payload))

                        result = func(*args, **kwargs)

                        # Use connector to map outputs if provided
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
