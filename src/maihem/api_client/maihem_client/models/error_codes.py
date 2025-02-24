from enum import Enum


class ErrorCodes(str, Enum):
    ERR_AUTHENTICATION_FAILED = "err_authentication_failed"
    ERR_CONFIG_FILE = "err_config_file"
    ERR_DATA_INTEGRITY = "err_data_integrity"
    ERR_INTERNAL_SERVER = "err_internal_server"
    ERR_NOT_FOUND = "err_not_found"
    ERR_NOT_IMPLEMENTED = "err_not_implemented"
    ERR_REQUEST_TIMEOUT = "err_request_timeout"
    ERR_REQUEST_VALIDATION = "err_request_validation"
    ERR_SCHEMA_VALIDATION = "err_schema_validation"
    ERR_WORKFLOW_PROCESSING = "err_workflow_processing"
    ERR_WRAPPER_FUNCTION = "err_wrapper_function"

    def __str__(self) -> str:
        return str(self.value)
