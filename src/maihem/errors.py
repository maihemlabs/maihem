from maihem.api_client.maihem_client.models.error_response import ErrorResponse
from maihem.api_client.maihem_client.models.error_codes import ErrorCodes


class ErrorBase(Exception):
    def __init__(self, error_resp: ErrorResponse) -> None:
        pass


class InternalServerError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        pass


class NotFoundError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        pass


class RequestValidationError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        pass


class SchemaValidationError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        pass


class DataIntegrityError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        pass


def handle_http_errors(error_resp: ErrorResponse):
    if ErrorCodes.ERR_INTERNAL_SERVER:
        raise InternalServerError(error_resp)
    elif ErrorCodes.ERR_NOT_FOUND:
        raise NotFoundError(error_resp)
    elif ErrorCodes.ERR_REQUEST_VALIDATION:
        raise RequestValidationError(error_resp)
    elif ErrorCodes.ERR_SCHEMA_VALIDATION:
        raise SchemaValidationError(error_resp)
    elif ErrorCodes.ERR_DATA_INTEGRITY:
        raise DataIntegrityError(error_resp)


##############################


class ChatFunctionError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AgentTargetCreateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AgentTargetGetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TestCreateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TestGetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TestRunError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TestRunGetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConversationGetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
