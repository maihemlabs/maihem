import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Org")


@_attrs_define
class Org:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str):
        idp_org_id (Union[None, Unset, str]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    idp_org_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        idp_org_id: Union[None, Unset, str]
        if isinstance(self.idp_org_id, Unset):
            idp_org_id = UNSET
        else:
            idp_org_id = self.idp_org_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "name": name,
            }
        )
        if idp_org_id is not UNSET:
            field_dict["idp_org_id"] = idp_org_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        name = d.pop("name")

        def _parse_idp_org_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        idp_org_id = _parse_idp_org_id(d.pop("idp_org_id", UNSET))

        org = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            idp_org_id=idp_org_id,
        )

        org.additional_properties = d
        return org

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
