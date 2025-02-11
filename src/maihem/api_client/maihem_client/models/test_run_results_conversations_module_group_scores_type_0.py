from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.test_run_metric_scores import TestRunMetricScores


T = TypeVar("T", bound="TestRunResultsConversationsModuleGroupScoresType0")


@_attrs_define
class TestRunResultsConversationsModuleGroupScoresType0:
    """ """

    additional_properties: Dict[str, "TestRunMetricScores"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_metric_scores import TestRunMetricScores

        d = src_dict.copy()
        test_run_results_conversations_module_group_scores_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = TestRunMetricScores.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        test_run_results_conversations_module_group_scores_type_0.additional_properties = additional_properties
        return test_run_results_conversations_module_group_scores_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "TestRunMetricScores":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "TestRunMetricScores") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
