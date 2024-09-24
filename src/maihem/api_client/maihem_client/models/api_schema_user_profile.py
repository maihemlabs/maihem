from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.api_schema_org import APISchemaOrg
    from ..models.api_schema_user import APISchemaUser


T = TypeVar("T", bound="APISchemaUserProfile")


@_attrs_define
class APISchemaUserProfile:
    """
    Attributes:
        user (APISchemaUser):
        org (APISchemaOrg):
    """

    user: "APISchemaUser"
    org: "APISchemaOrg"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user = self.user.to_dict()

        org = self.org.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "org": org,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_schema_org import APISchemaOrg
        from ..models.api_schema_user import APISchemaUser

        d = src_dict.copy()
        user = APISchemaUser.from_dict(d.pop("user"))

        org = APISchemaOrg.from_dict(d.pop("org"))

        api_schema_user_profile = cls(
            user=user,
            org=org,
        )

        api_schema_user_profile.additional_properties = d
        return api_schema_user_profile

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
