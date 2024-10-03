from enum import Enum
from maihem.api_client.maihem_client.models.error_response import (
    ErrorResponse,
)
from maihem.api_client.maihem_client.models.error_response_error import (
    ErrorResponseError,
)
from maihem.api_client.maihem_client.models.error_codes import (
    ErrorCodes as ErrorCodesAPI,
)
from pydantic_core import ValidationError
from maihem.logger import get_logger


class ErrorCodes(str, Enum):
    ERR_CHAT_FUNCTION = "err_chat_function"
    ERR_CONFIG_FILE = "err_config_file"
    ERR_INTERNAL_SERVER = ErrorCodesAPI.ERR_INTERNAL_SERVER
    ERR_NOT_FOUND = ErrorCodesAPI.ERR_NOT_FOUND
    ERR_REQUEST_VALIDATION = ErrorCodesAPI.ERR_REQUEST_VALIDATION
    ERR_SCHEMA_VALIDATION = ErrorCodesAPI.ERR_SCHEMA_VALIDATION
    ERR_DATA_INTEGRITY = ErrorCodesAPI.ERR_DATA_INTEGRITY
    ERR_AUTHENTICATION_FAILED = ErrorCodesAPI.ERR_AUTHENTICATION_FAILED


class ErrorBase(Exception):
    message: str

    def __init__(self, error_resp: ErrorResponse) -> None:
        self.message = error_resp.error.message

    def __str__(self) -> str:
        return self.message


class AuthenticationFailedError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


class InternalServerError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


class NotFoundError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


class RequestValidationError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


class SchemaValidationError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


class DataIntegrityError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


class ChatFunctionError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)
        
class ConfigFileError(ErrorBase):
    def __init__(self, error_resp: ErrorResponse) -> None:
        super().__init__(error_resp)


def handle_http_errors(error_resp: ErrorResponse):
    if not error_resp:
        return

    if error_resp.error.code == ErrorCodes.ERR_INTERNAL_SERVER:
        raise InternalServerError(error_resp)
    elif error_resp.error.code == ErrorCodes.ERR_NOT_FOUND:
        raise NotFoundError(error_resp)
    elif error_resp.error.code == ErrorCodes.ERR_REQUEST_VALIDATION:
        raise RequestValidationError(error_resp)
    elif error_resp.error.code == ErrorCodes.ERR_SCHEMA_VALIDATION:
        raise SchemaValidationError(error_resp)
    elif error_resp.error.code == ErrorCodes.ERR_DATA_INTEGRITY:
        raise DataIntegrityError(error_resp)
    elif error_resp.error.code == ErrorCodes.ERR_AUTHENTICATION_FAILED:
        raise AuthenticationFailedError(error_resp)
    else:
        raise ErrorBase(error_resp)


def handle_base_error(exception: ErrorBase):
    get_logger().error(exception.message)
    raise exception


def handle_schema_validation_error(exception: ValidationError):
    raise SchemaValidationError(
        ErrorResponse(
            error=ErrorResponseError(
                code=ErrorCodes.ERR_SCHEMA_VALIDATION,
                message=str(exception.errors()),
                detail=None,
            )
        )
    ) from exception


def raise_request_validation_error(message: str):
    raise RequestValidationError(
        ErrorResponse(
            error=ErrorResponseError(
                code=ErrorCodes.ERR_REQUEST_VALIDATION, message=message, detail=None
            ),
            request_id=None,
        )
    )


def raise_not_found_error(message: str):
    raise NotFoundError(
        ErrorResponse(
            error=ErrorResponseError(
                code=ErrorCodes.ERR_NOT_FOUND, message=message, detail=None
            ),
            request_id=None,
        )
    )


def raise_chat_function_error(message: str):
    raise ChatFunctionError(
        ErrorResponse(
            error=ErrorResponseError(
                code=ErrorCodes.ERR_CHAT_FUNCTION, message=message, detail=None
            ),
            request_id=None,
        )
    )
    
    
def raise_config_file_error(message: str):
    raise ConfigFileError(
        ErrorResponse(
            error=ErrorResponseError(
                code=ErrorCodes.ERR_CONFIG_FILE, message=message, detail=None
            ),
            request_id=None,
        )
    )
