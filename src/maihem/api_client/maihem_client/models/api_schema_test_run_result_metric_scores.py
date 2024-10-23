from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_enum import TestResultEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaTestRunResultMetricScores")


@_attrs_define
class APISchemaTestRunResultMetricScores:
    """
    Attributes:
        total_conversations (int):
        result_passed (int):
        result_failed (int):
        status_completed (int):
        status_error (int):
        status_running (int):
        status_pending (int):
        status_paused (int):
        result (Union[None, TestResultEnum, Unset]):
        total_score (Union[None, Unset, float]):
    """

    total_conversations: int
    result_passed: int
    result_failed: int
    status_completed: int
    status_error: int
    status_running: int
    status_pending: int
    status_paused: int
    result: Union[None, TestResultEnum, Unset] = UNSET
    total_score: Union[None, Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_conversations = self.total_conversations

        result_passed = self.result_passed

        result_failed = self.result_failed

        status_completed = self.status_completed

        status_error = self.status_error

        status_running = self.status_running

        status_pending = self.status_pending

        status_paused = self.status_paused

        result: Union[None, Unset, str]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, TestResultEnum):
            result = self.result.value
        else:
            result = self.result

        total_score: Union[None, Unset, float]
        if isinstance(self.total_score, Unset):
            total_score = UNSET
        else:
            total_score = self.total_score

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_conversations": total_conversations,
                "result_passed": result_passed,
                "result_failed": result_failed,
                "status_completed": status_completed,
                "status_error": status_error,
                "status_running": status_running,
                "status_pending": status_pending,
                "status_paused": status_paused,
            }
        )
        if result is not UNSET:
            field_dict["result"] = result
        if total_score is not UNSET:
            field_dict["total_score"] = total_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_conversations = d.pop("total_conversations")

        result_passed = d.pop("result_passed")

        result_failed = d.pop("result_failed")

        status_completed = d.pop("status_completed")

        status_error = d.pop("status_error")

        status_running = d.pop("status_running")

        status_pending = d.pop("status_pending")

        status_paused = d.pop("status_paused")

        def _parse_result(data: object) -> Union[None, TestResultEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_type_0 = TestResultEnum(data)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TestResultEnum, Unset], data)

        result = _parse_result(d.pop("result", UNSET))

        def _parse_total_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_score = _parse_total_score(d.pop("total_score", UNSET))

        api_schema_test_run_result_metric_scores = cls(
            total_conversations=total_conversations,
            result_passed=result_passed,
            result_failed=result_failed,
            status_completed=status_completed,
            status_error=status_error,
            status_running=status_running,
            status_pending=status_pending,
            status_paused=status_paused,
            result=result,
            total_score=total_score,
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
