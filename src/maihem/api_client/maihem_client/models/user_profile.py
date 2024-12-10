from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.org import Org
    from ..models.user import User


T = TypeVar("T", bound="UserProfile")


@_attrs_define
class UserProfile:
    """
    Attributes:
        user (User):
        active_org_id (str):
        orgs (List['Org']):
    """

    user: "User"
    active_org_id: str
    orgs: List["Org"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user = self.user.to_dict()

        active_org_id = self.active_org_id

        orgs = []
        for orgs_item_data in self.orgs:
            orgs_item = orgs_item_data.to_dict()
            orgs.append(orgs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "active_org_id": active_org_id,
                "orgs": orgs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.org import Org
        from ..models.user import User

        d = src_dict.copy()
        user = User.from_dict(d.pop("user"))

        active_org_id = d.pop("active_org_id")

        orgs = []
        _orgs = d.pop("orgs")
        for orgs_item_data in _orgs:
            orgs_item = Org.from_dict(orgs_item_data)

            orgs.append(orgs_item)

        user_profile = cls(
            user=user,
            active_org_id=active_org_id,
            orgs=orgs,
        )

        user_profile.additional_properties = d
        return user_profile

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
