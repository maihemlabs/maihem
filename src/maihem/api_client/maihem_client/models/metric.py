from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.criteria import Criteria


T = TypeVar("T", bound="Metric")


@_attrs_define
class Metric:
    """
    Attributes:
        id (str):
        metric_group (str):
        metric_group_label (str):
        metric_sub_group (str):
        metric_sub_group_label (str):
        metric (str):
        metric_label (str):
        metric_description (Union[None, Unset, str]):
        criteria (Union[Unset, List['Criteria']]):
    """

    id: str
    metric_group: str
    metric_group_label: str
    metric_sub_group: str
    metric_sub_group_label: str
    metric: str
    metric_label: str
    metric_description: Union[None, Unset, str] = UNSET
    criteria: Union[Unset, List["Criteria"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        metric_group = self.metric_group

        metric_group_label = self.metric_group_label

        metric_sub_group = self.metric_sub_group

        metric_sub_group_label = self.metric_sub_group_label

        metric = self.metric

        metric_label = self.metric_label

        metric_description: Union[None, Unset, str]
        if isinstance(self.metric_description, Unset):
            metric_description = UNSET
        else:
            metric_description = self.metric_description

        criteria: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.criteria, Unset):
            criteria = []
            for criteria_item_data in self.criteria:
                criteria_item = criteria_item_data.to_dict()
                criteria.append(criteria_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "metric_group": metric_group,
                "metric_group_label": metric_group_label,
                "metric_sub_group": metric_sub_group,
                "metric_sub_group_label": metric_sub_group_label,
                "metric": metric,
                "metric_label": metric_label,
            }
        )
        if metric_description is not UNSET:
            field_dict["metric_description"] = metric_description
        if criteria is not UNSET:
            field_dict["criteria"] = criteria

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.criteria import Criteria

        d = src_dict.copy()
        id = d.pop("id")

        metric_group = d.pop("metric_group")

        metric_group_label = d.pop("metric_group_label")

        metric_sub_group = d.pop("metric_sub_group")

        metric_sub_group_label = d.pop("metric_sub_group_label")

        metric = d.pop("metric")

        metric_label = d.pop("metric_label")

        def _parse_metric_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_description = _parse_metric_description(d.pop("metric_description", UNSET))

        criteria = []
        _criteria = d.pop("criteria", UNSET)
        for criteria_item_data in _criteria or []:
            criteria_item = Criteria.from_dict(criteria_item_data)

            criteria.append(criteria_item)

        metric = cls(
            id=id,
            metric_group=metric_group,
            metric_group_label=metric_group_label,
            metric_sub_group=metric_sub_group,
            metric_sub_group_label=metric_sub_group_label,
            metric=metric,
            metric_label=metric_label,
            metric_description=metric_description,
            criteria=criteria,
        )

        metric.additional_properties = d
        return metric

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
