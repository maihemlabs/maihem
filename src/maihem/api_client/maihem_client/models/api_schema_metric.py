from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="APISchemaMetric")


@_attrs_define
class APISchemaMetric:
    """
    Attributes:
        id (str):
        metric_group (str):
        metric_group_label (str):
        metric_sub_group (str):
        metric_sub_group_label (str):
        metric (str):
        metric_label (str):
    """

    id: str
    metric_group: str
    metric_group_label: str
    metric_sub_group: str
    metric_sub_group_label: str
    metric: str
    metric_label: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        metric_group = self.metric_group

        metric_group_label = self.metric_group_label

        metric_sub_group = self.metric_sub_group

        metric_sub_group_label = self.metric_sub_group_label

        metric = self.metric

        metric_label = self.metric_label

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        metric_group = d.pop("metric_group")

        metric_group_label = d.pop("metric_group_label")

        metric_sub_group = d.pop("metric_sub_group")

        metric_sub_group_label = d.pop("metric_sub_group_label")

        metric = d.pop("metric")

        metric_label = d.pop("metric_label")

        api_schema_metric = cls(
            id=id,
            metric_group=metric_group,
            metric_group_label=metric_group_label,
            metric_sub_group=metric_sub_group,
            metric_sub_group_label=metric_sub_group_label,
            metric=metric,
            metric_label=metric_label,
        )

        api_schema_metric.additional_properties = d
        return api_schema_metric

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
