from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.api_schema_test_run_result_metric_scores import APISchemaTestRunResultMetricScores


T = TypeVar("T", bound="APISchemaTestRunResultConversationsMetricScoresType0")


@_attrs_define
class APISchemaTestRunResultConversationsMetricScoresType0:
    """ """

    additional_properties: Dict[str, "APISchemaTestRunResultMetricScores"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_schema_test_run_result_metric_scores import APISchemaTestRunResultMetricScores

        d = src_dict.copy()
        api_schema_test_run_result_conversations_metric_scores_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = APISchemaTestRunResultMetricScores.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        api_schema_test_run_result_conversations_metric_scores_type_0.additional_properties = additional_properties
        return api_schema_test_run_result_conversations_metric_scores_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "APISchemaTestRunResultMetricScores":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "APISchemaTestRunResultMetricScores") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
