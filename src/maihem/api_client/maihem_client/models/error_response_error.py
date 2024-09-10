from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_codes import ErrorCodes

if TYPE_CHECKING:
    from ..models.error_response_error_detail_type_0 import ErrorResponseErrorDetailType0


T = TypeVar("T", bound="ErrorResponseError")


@_attrs_define
class ErrorResponseError:
    """
    Attributes:
        code (ErrorCodes):
        message (str):
        detail (Union['ErrorResponseErrorDetailType0', None]):
    """

    code: ErrorCodes
    message: str
    detail: Union["ErrorResponseErrorDetailType0", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.error_response_error_detail_type_0 import ErrorResponseErrorDetailType0

        code = self.code.value

        message = self.message

        detail: Union[Dict[str, Any], None]
        if isinstance(self.detail, ErrorResponseErrorDetailType0):
            detail = self.detail.to_dict()
        else:
            detail = self.detail

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
        from ..models.error_response_error_detail_type_0 import ErrorResponseErrorDetailType0

        d = src_dict.copy()
        code = ErrorCodes(d.pop("code"))

        message = d.pop("message")

        def _parse_detail(data: object) -> Union["ErrorResponseErrorDetailType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                detail_type_0 = ErrorResponseErrorDetailType0.from_dict(data)

                return detail_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ErrorResponseErrorDetailType0", None], data)

        detail = _parse_detail(d.pop("detail"))

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
