from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Criteria")


@_attrs_define
class Criteria:
    """
    Attributes:
        id (str):
        scope_type (str):
        scope_id (str):
        criteria (str):
        criteria_label (str):
        criteria_description (Union[None, Unset, str]):
    """

    id: str
    scope_type: str
    scope_id: str
    criteria: str
    criteria_label: str
    criteria_description: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        scope_type = self.scope_type

        scope_id = self.scope_id

        criteria = self.criteria

        criteria_label = self.criteria_label

        criteria_description: Union[None, Unset, str]
        if isinstance(self.criteria_description, Unset):
            criteria_description = UNSET
        else:
            criteria_description = self.criteria_description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scope_type": scope_type,
                "scope_id": scope_id,
                "criteria": criteria,
                "criteria_label": criteria_label,
            }
        )
        if criteria_description is not UNSET:
            field_dict["criteria_description"] = criteria_description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        scope_type = d.pop("scope_type")

        scope_id = d.pop("scope_id")

        criteria = d.pop("criteria")

        criteria_label = d.pop("criteria_label")

        def _parse_criteria_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        criteria_description = _parse_criteria_description(d.pop("criteria_description", UNSET))

        criteria = cls(
            id=id,
            scope_type=scope_type,
            scope_id=scope_id,
            criteria=criteria,
            criteria_label=criteria_label,
            criteria_description=criteria_description,
        )

        criteria.additional_properties = d
        return criteria

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
