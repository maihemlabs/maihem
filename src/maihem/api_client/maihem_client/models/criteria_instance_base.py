from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CriteriaInstanceBase")


@_attrs_define
class CriteriaInstanceBase:
    """
    Attributes:
        instances (int):
        conversations (int):
        score_impact (Union[None, Unset, float]):
    """

    instances: int
    conversations: int
    score_impact: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instances = self.instances

        conversations = self.conversations

        score_impact: Union[None, Unset, float]
        if isinstance(self.score_impact, Unset):
            score_impact = UNSET
        else:
            score_impact = self.score_impact

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instances": instances,
                "conversations": conversations,
            }
        )
        if score_impact is not UNSET:
            field_dict["score_impact"] = score_impact

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        instances = d.pop("instances")

        conversations = d.pop("conversations")

        def _parse_score_impact(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        score_impact = _parse_score_impact(d.pop("score_impact", UNSET))

        criteria_instance_base = cls(
            instances=instances,
            conversations=conversations,
            score_impact=score_impact,
        )

        criteria_instance_base.additional_properties = d
        return criteria_instance_base

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
