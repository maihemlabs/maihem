from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_codes import ErrorCodes

if TYPE_CHECKING:
    from ..models.error_response_error_detail import ErrorResponseErrorDetail


T = TypeVar("T", bound="ErrorResponseError")


@_attrs_define
class ErrorResponseError:
    """
    Attributes:
        code (ErrorCodes):
        message (str):
        detail (ErrorResponseErrorDetail):
    """

    code: ErrorCodes
    message: str
    detail: "ErrorResponseErrorDetail"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code.value

        message = self.message

        detail = self.detail.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_response_error_detail import ErrorResponseErrorDetail

        d = src_dict.copy()
        code = ErrorCodes(d.pop("code"))

        message = d.pop("message")

        detail = ErrorResponseErrorDetail.from_dict(d.pop("detail"))

        error_response_error = cls(
            code=code,
            message=message,
            detail=detail,
        )

        error_response_error.additional_properties = d
        return error_response_error

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
