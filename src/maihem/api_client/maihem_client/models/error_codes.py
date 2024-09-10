from enum import Enum


class ErrorCodes(str, Enum):
    ERR_DATA_INTEGRITY = "err_data_integrity"
    ERR_INTERNAL_SERVER = "err_internal_server"
    ERR_NOT_FOUND = "err_not_found"
    ERR_REQUEST_VALIDATION = "err_request_validation"
    ERR_SCHEMA_VALIDATION = "err_schema_validation"

    def __str__(self) -> str:
        return str(self.value)