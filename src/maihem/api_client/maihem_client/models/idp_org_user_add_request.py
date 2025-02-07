from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IDPOrgUserAddRequest")


@_attrs_define
class IDPOrgUserAddRequest:
    """
    Attributes:
        event_type (str):
        org_id (str):
        role (str):
        user_id (str):
    """

    event_type: str
    org_id: str
    role: str
    user_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        org_id = self.org_id

        role = self.role

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
                "org_id": org_id,
                "role": role,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        event_type = d.pop("event_type")

        org_id = d.pop("org_id")

        role = d.pop("role")

        user_id = d.pop("user_id")

        idp_org_user_add_request = cls(
            event_type=event_type,
            org_id=org_id,
            role=role,
            user_id=user_id,
        )

        idp_org_user_add_request.additional_properties = d
        return idp_org_user_add_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
