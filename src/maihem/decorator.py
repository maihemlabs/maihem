from maihem.evaluators import MaihemEvaluator
from maihem.otel_client import Tracer, trace
from maihem.utils.utils import validate_attributes_testing
from typing import Optional, Callable, Any
import inspect
from functools import wraps
import orjson as json


def observe(
    name: Optional[str] = None,
    workflow_name: Optional[str] = None,
    external_conversation_id: Optional[str] = None,
    external_conversation_message_id: Optional[str] = None,
    evaluator: Optional[MaihemEvaluator] = None,
):
    def decorator(func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                parent_span = trace.get_current_span()

                with tracer.start_as_current_span(span_name) as span:
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
                            "workflow_name": workflow_name,
                            "conversation_id": getattr(
                                async_wrapper, "conversation_id", None
                            ),
                            "conversation_message_id": getattr(
                                async_wrapper, "conversation_message_id", None
                            ),
                            "external_conversation_id": external_conversation_id,
                            "external_conversation_message_id": external_conversation_message_id,
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
                        span.set_attribute(
                            "input_payload", str(json.dumps(input_payload))
                        )

                        result = await func(*args, **kwargs)

                        # Use connector to map outputs if provided
                        if evaluator:
                            output_payload = evaluator.map_outputs(result)
                        else:
                            output_payload = result
                        span.set_attribute(
                            "output_payload", str(json.dumps(output_payload))
                        )

                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                        raise

            return async_wrapper
        else:
            # Implement synchronous wrapper if needed
            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = Tracer.get_instance().tracer
                span_name = name or func.__name__
                parent_span = trace.get_current_span()

                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("workflow_step_name", span_name)

                    span.set_attribute(
                        "evaluator_name",
                        evaluator.NAME if evaluator else None,
                    )

                    if parent_span is None or not parent_span.is_recording():
                        try:
                            if getattr(sync_wrapper, "testing", False):
                                validate_attributes_testing(sync_wrapper)
                            else:
                                if not external_conversation_id:
                                    raise ValueError(
                                        "external_conversation_id is required"
                                    )
                        except ValueError as e:
                            span.record_exception(e)
                            span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                            raise

                        monitoring_attrs = {
                            "agent_target_id": getattr(
                                sync_wrapper, "agent_target_id", None
                            ),
                            "test_run_id": getattr(sync_wrapper, "test_run_id", None),
                            "workflow_name": workflow_name,
                            "conversation_id": getattr(
                                sync_wrapper, "conversation_id", None
                            ),
                            "conversation_message_id": getattr(
                                sync_wrapper, "message_id", None
                            ),
                            "external_conversation_id": external_conversation_id,
                            "external_conversation_message_id": external_conversation_message_id,
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
                        span.set_attribute("input_payload", repr(input_payload))

                        result = func(*args, **kwargs)

                        # Use connector to map outputs if provided
                        if evaluator:
                            output_payload = evaluator.map_outputs(result)
                        else:
                            output_payload = result
                        span.set_attribute("output_payload", repr(output_payload))

                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.status.Status(trace.StatusCode.ERROR))
                        raise

            return sync_wrapper

    return decorator
