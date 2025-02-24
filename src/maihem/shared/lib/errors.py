from enum import Enum
from typing import Dict, Optional, Any
from pydantic import ValidationError, BaseModel
from .request_context import get_request_id
from .logger import Logger


class ErrorCodes(str, Enum):
    ERR_NOT_FOUND = "err_not_found"
    ERR_WORKFLOW_PROCESSING = "err_workflow_processing"
    ERR_INTERNAL_SERVER = "err_internal_server"
    ERR_REQUEST_VALIDATION = "err_request_validation"
    ERR_SCHEMA_VALIDATION = "err_schema_validation"
    ERR_DATA_INTEGRITY = "err_data_integrity"
    ERR_AUTHENTICATION_FAILED = "err_authentication_failed"
    ERR_REQUEST_TIMEOUT = "err_request_timeout"
    ERR_NOT_IMPLEMENTED = "err_not_implemented"
    ERR_WRAPPER_FUNCTION = "err_wrapper_function"
    ERR_CONFIG_FILE = "err_config_file"


class ErrorResponseError(BaseModel):
    code: ErrorCodes
    message: str
    detail: Optional[Any] = None


class ErrorResponse(BaseModel):
    error: ErrorResponseError
    request_id: Optional[str] = None


error_response_base = {
    400: {"model": ErrorResponse},
    409: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
    504: {"model": ErrorResponse},
}


class BaseError(Exception):
    def __init__(
        self,
        status_code=500,
        code=ErrorCodes.ERR_INTERNAL_SERVER,
        message="Internal server error",
        detail=None,
    ):
        if detail is None:
            detail = {}
        self.status_code = status_code
        self.code = code
        self.message = message
        self.detail = detail
        super().__init__(self.message)

    def to_dict(self) -> Dict:
        error_body = ErrorResponseError(
            code=self.code, message=self.message, detail=self.detail
        )
        error = ErrorResponse(error=error_body, request_id=get_request_id())

        return error.model_dump()


class AuthenticationFailedError(BaseError):
    def __init__(
        self,
        message: str = "Authentication failed",
    ):
        super().__init__(
            status_code=401,
            code=ErrorCodes.ERR_AUTHENTICATION_FAILED,
            message=message,
            detail=None,
        )


class NotFoundError(BaseError):
    def __init__(self, entity_type: str, entity_key: str = None):
        if entity_key:
            message = f"{entity_type} ({entity_key}) not found"
        else:
            message = f"{entity_type} not found"
        super().__init__(
            status_code=404,
            code=ErrorCodes.ERR_NOT_FOUND,
            message=message,
            detail={"entity_type": entity_type, "entity_key": entity_key},
        )


class SchemaValidationError(BaseError):
    def __init__(self, message=None, detail=None):
        super().__init__(
            status_code=400,
            code=ErrorCodes.ERR_SCHEMA_VALIDATION,
            message="Schema validation error" + (f": {message}" if message else ""),
            detail=detail,
        )


class DataIntegrityError(BaseError):
    def __init__(self, entity_type: str, entity_key: str, detail=None):
        super().__init__(
            status_code=409,
            code=ErrorCodes.ERR_DATA_INTEGRITY,
            message=f"{entity_type} ({entity_key}) already exists",
            detail=detail,
        )


class RequestTimeoutError(BaseError):
    def __init__(self, message: str = "Request timeout", detail=None):
        super().__init__(
            status_code=504,
            code=ErrorCodes.ERR_REQUEST_TIMEOUT,
            message=f"{message}",
            detail=detail,
        )


class RequestValidationCustomError(BaseError):
    def __init__(self, message: str = "Request validation error", detail=None):
        super().__init__(
            status_code=400,
            code=ErrorCodes.ERR_REQUEST_VALIDATION,
            message=f"{message}",
            detail=detail,
        )


class WorkflowProcessingError(BaseError):
    def __init__(self, message: str = "Error processing workflow", detail=None):
        super().__init__(
            status_code=500,
            code=ErrorCodes.ERR_WORKFLOW_PROCESSING,
            message=f"Error processing workflow: {message}",
            detail=detail,
        )


class NotImplementError(BaseError):
    def __init__(self, message: str = "Not implemented", detail=None):
        super().__init__(
            status_code=501,
            code=ErrorCodes.ERR_NOT_IMPLEMENTED,
            message=f"{message}",
            detail=detail,
        )


class InternalServerError(BaseError):
    def __init__(self, message: str = "Internal server error", detail=None):
        super().__init__(
            status_code=500,
            code=ErrorCodes.ERR_INTERNAL_SERVER,
            message=f"{message}",
            detail=detail,
        )


class WrapperFunctionError(BaseError):
    def __init__(self, message: str = "Wrapper function error", detail=None):
        super().__init__(
            status_code=500,
            code=ErrorCodes.ERR_WRAPPER_FUNCTION,
            message=f"{message}",
            detail=detail,
        )


class ConfigFileError(BaseError):
    def __init__(self, message: str = "Config file error", detail=None):
        super().__init__(
            status_code=500,
            code=ErrorCodes.ERR_CONFIG_FILE,
            message=f"{message}",
            detail=detail,
        )


def handle_base_error(logger: Logger, exception: BaseError):
    logger.opt(exception=exception).exception(exception.message)
    raise exception


def handle_http_errors(logger: Logger, error_resp: ErrorResponse):
    if not error_resp:
        return
    if error_resp.error.code == ErrorCodes.ERR_INTERNAL_SERVER:
        raise_internal_server_error(logger=logger, message=error_resp.error.message)
    elif error_resp.error.code == ErrorCodes.ERR_NOT_FOUND:
        raise_not_found_error(
            logger=logger,
            entity_type=error_resp.error.detail.get("entity_type"),
            entity_key=error_resp.error.detail.get("entity_key"),
        )
    elif error_resp.error.code == ErrorCodes.ERR_REQUEST_VALIDATION:
        raise_request_validation_error(logger=logger, message=error_resp.error.message)
    elif error_resp.error.code == ErrorCodes.ERR_SCHEMA_VALIDATION:
        raise_schema_validation_error(logger=logger, message=error_resp.error.message)
    elif error_resp.error.code == ErrorCodes.ERR_DATA_INTEGRITY:
        raise_data_integrity_error(
            logger=logger,
            entity_type=error_resp.error.detail.get("entity_type"),
            entity_key=error_resp.error.detail.get("entity_key"),
        )
    elif error_resp.error.code == ErrorCodes.ERR_AUTHENTICATION_FAILED:
        raise_authentication_failed_error(
            logger=logger, message=error_resp.error.message
        )
    else:
        raise BaseError(**error_resp.error)


def handle_schema_validation_error(logger: Logger, exception: ValidationError):
    exc = SchemaValidationError(exception.errors())
    logger.opt(exception=exc).exception(
        f"Schema validation error: {exception.errors()}"
    )
    raise exc from exception


def handle_request_timeout_error(logger: Logger, exception: Exception, detail=None):
    exc = RequestTimeoutError(message="Network request timed out", detail=detail)
    logger.opt(exception=exc).exception(f"Request timeout error: {str(exception)}")
    raise exc from exception


def raise_schema_validation_error(
    logger: Logger, message: Optional[str] = None, detail=None
):

    exception = SchemaValidationError(message=message, detail=detail)
    logger.opt(depth=1).exception(
        f"Schema validation error: {message}", exception=exception
    )
    raise exception


def raise_not_found_error(
    logger: Logger,
    entity_type: str,
    entity_key: str = None,
    reference_entity_type: str = None,
    reference_entity_key: str = None,
    comment: Optional[str] = None,
):
    if entity_type and reference_entity_type and reference_entity_key:
        message = f"{entity_type} not found for {reference_entity_type} ({reference_entity_key})"
    if entity_key:
        message = f"{entity_type} ({entity_key}) not found"
    else:
        message = f"{entity_type} not found"

    if comment:
        message = f"{message} - {comment}"
    exc = NotFoundError(entity_type, entity_key)
    logger.opt(exception=exc).exception(message)
    raise exc


def raise_request_validation_error(logger: Logger, message: Optional[str] = None):
    exc = RequestValidationCustomError(message=message)
    logger.opt(exception=exc).exception(f"{message}")
    raise exc


def raise_workflow_processing_error(logger: Logger, message: Optional[str] = None):
    try:
        raise WorkflowProcessingError(message=message)
    except WorkflowProcessingError:
        logger.exception(f"Error processing workflow: {message}")
        raise


def raise_not_implemented_error(logger: Logger, message: Optional[str] = None):
    try:
        raise NotImplementError(message=message)
    except NotImplementError:
        logger.error(f"Not implemented: {message}")
        raise


def raise_internal_server_error(logger: Logger, message: Optional[str] = None):
    try:
        raise InternalServerError(message=message)
    except InternalServerError:
        logger.error(f"Internal server error: {message}")
        raise


def raise_data_integrity_error(
    logger: Logger,
    entity_type: str,
    entity_key: str,
    detail=None,
):
    exc = DataIntegrityError(
        entity_type,
        entity_key,
        detail=detail or {"entity_type": entity_type, "entity_key": entity_key},
    )
    logger.opt(exception=exc).exception(f"{entity_type} ({entity_key}) already exists")
    raise exc


def raise_authentication_failed_error(logger: Logger, message: Optional[str] = None):
    try:
        raise AuthenticationFailedError(message=message)
    except AuthenticationFailedError:
        logger.error(f"Authentication failed: {message}")
        raise


def raise_wrapper_function_error(logger: Logger, message: Optional[str] = None):
    try:
        raise WrapperFunctionError(message=message)
    except WrapperFunctionError:
        logger.error(f"Wrapper function error: {message}")
        raise


def raise_config_file_error(logger: Logger, message: Optional[str] = None):
    try:
        raise ConfigFileError(message=message)
    except ConfigFileError:
        logger.error(f"Config file error: {message}")
        raise
