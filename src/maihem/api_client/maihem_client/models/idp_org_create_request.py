from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IDPOrgCreateRequest")


@_attrs_define
class IDPOrgCreateRequest:
    """
    Attributes:
        event_type (str):
        org_id (str):
        name (str):
    """

    event_type: str
    org_id: str
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        org_id = self.org_id

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
                "org_id": org_id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        event_type = d.pop("event_type")

        org_id = d.pop("org_id")

        name = d.pop("name")

        idp_org_create_request = cls(
            event_type=event_type,
            org_id=org_id,
            name=name,
        )

        idp_org_create_request.additional_properties = d
        return idp_org_create_request

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
