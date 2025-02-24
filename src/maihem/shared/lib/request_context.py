from contextvars import ContextVar

request_id_context: ContextVar[str] = ContextVar("request_id", default="")
conversation_id_context: ContextVar[str] = ContextVar("conversation_id", default="")
test_run_id_context: ContextVar[str] = ContextVar("test_run_id", default="")
workflow_trace_raw_id_context: ContextVar[str] = ContextVar(
    "workflow_trace_raw_id", default=""
)
workflow_trace_id_context: ContextVar[str] = ContextVar("workflow_trace_id", default="")
workflow_span_id_context: ContextVar[str] = ContextVar("workflow_span_id", default="")
workflow_step_id_context: ContextVar[str] = ContextVar("workflow_step_id", default="")


def get_request_id() -> str:
    return request_id_context.get()


def set_request_id(request_id: str):
    request_id_context.set(request_id)


def get_conversation_id() -> str:
    return conversation_id_context.get()


def set_conversation_id(conversation_id: str):
    conversation_id_context.set(conversation_id)


def get_test_run_id() -> str:
    return test_run_id_context.get()


def set_test_run_id(test_id: str):
    test_run_id_context.set(test_id)


def get_workflow_trace_raw_id() -> str:
    return workflow_trace_raw_id_context.get()


def set_workflow_trace_raw_id(workflow_trace_raw_id: str):
    workflow_trace_raw_id_context.set(workflow_trace_raw_id)


def get_workflow_trace_id() -> str:
    return workflow_trace_id_context.get()


def set_workflow_trace_id(workflow_trace_id: str):
    workflow_trace_id_context.set(workflow_trace_id)


def get_workflow_span_id() -> str:
    return workflow_span_id_context.get()


def set_workflow_span_id(workflow_span_id: str):
    workflow_span_id_context.set(workflow_span_id)


def get_workflow_step_id() -> str:
    return workflow_step_id_context.get()


def set_workflow_step_id(workflow_step_id: str):
    workflow_step_id_context.set(workflow_step_id)
