from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_enum import TestResultEnum

T = TypeVar("T", bound="APISchemaTestRunResultMetricScores")


@_attrs_define
class APISchemaTestRunResultMetricScores:
    """
    Attributes:
        result (TestResultEnum):
        total (int):
        passed (int):
        failed (int):
        errored (int):
    """

    result: TestResultEnum
    total: int
    passed: int
    failed: int
    errored: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = self.result.value

        total = self.total

        passed = self.passed

        failed = self.failed

        errored = self.errored

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "total": total,
                "passed": passed,
                "failed": failed,
                "errored": errored,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        result = TestResultEnum(d.pop("result"))

        total = d.pop("total")

        passed = d.pop("passed")

        failed = d.pop("failed")

        errored = d.pop("errored")

        api_schema_test_run_result_metric_scores = cls(
            result=result,
            total=total,
            passed=passed,
            failed=failed,
            errored=errored,
        )

        api_schema_test_run_result_metric_scores.additional_properties = d
        return api_schema_test_run_result_metric_scores

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
