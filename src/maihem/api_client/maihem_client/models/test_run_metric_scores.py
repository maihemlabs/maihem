from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_enum import TestResultEnum
from ..models.test_status_enum import TestStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_metric_scores_criteria_failures_type_0 import TestRunMetricScoresCriteriaFailuresType0


T = TypeVar("T", bound="TestRunMetricScores")


@_attrs_define
class TestRunMetricScores:
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
        status_canceled (int):
        status (TestStatusEnum):
        total_score (Union[None, Unset, float]):
        total_score_change (Union[None, Unset, float]):
        result (Union[None, TestResultEnum, Unset]):
        summary (Union[None, Unset, str]):
        criteria_failures (Union['TestRunMetricScoresCriteriaFailuresType0', None, Unset]):
    """

    total_conversations: int
    result_passed: int
    result_failed: int
    status_completed: int
    status_error: int
    status_running: int
    status_pending: int
    status_paused: int
    status_canceled: int
    status: TestStatusEnum
    total_score: Union[None, Unset, float] = UNSET
    total_score_change: Union[None, Unset, float] = UNSET
    result: Union[None, TestResultEnum, Unset] = UNSET
    summary: Union[None, Unset, str] = UNSET
    criteria_failures: Union["TestRunMetricScoresCriteriaFailuresType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.test_run_metric_scores_criteria_failures_type_0 import TestRunMetricScoresCriteriaFailuresType0

        total_conversations = self.total_conversations

        result_passed = self.result_passed

        result_failed = self.result_failed

        status_completed = self.status_completed

        status_error = self.status_error

        status_running = self.status_running

        status_pending = self.status_pending

        status_paused = self.status_paused

        status_canceled = self.status_canceled

        status = self.status.value

        total_score: Union[None, Unset, float]
        if isinstance(self.total_score, Unset):
            total_score = UNSET
        else:
            total_score = self.total_score

        total_score_change: Union[None, Unset, float]
        if isinstance(self.total_score_change, Unset):
            total_score_change = UNSET
        else:
            total_score_change = self.total_score_change

        result: Union[None, Unset, str]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, TestResultEnum):
            result = self.result.value
        else:
            result = self.result

        summary: Union[None, Unset, str]
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        criteria_failures: Union[Dict[str, Any], None, Unset]
        if isinstance(self.criteria_failures, Unset):
            criteria_failures = UNSET
        elif isinstance(self.criteria_failures, TestRunMetricScoresCriteriaFailuresType0):
            criteria_failures = self.criteria_failures.to_dict()
        else:
            criteria_failures = self.criteria_failures

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
                "status_canceled": status_canceled,
                "status": status,
            }
        )
        if total_score is not UNSET:
            field_dict["total_score"] = total_score
        if total_score_change is not UNSET:
            field_dict["total_score_change"] = total_score_change
        if result is not UNSET:
            field_dict["result"] = result
        if summary is not UNSET:
            field_dict["summary"] = summary
        if criteria_failures is not UNSET:
            field_dict["criteria_failures"] = criteria_failures

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_metric_scores_criteria_failures_type_0 import TestRunMetricScoresCriteriaFailuresType0

        d = src_dict.copy()
        total_conversations = d.pop("total_conversations")

        result_passed = d.pop("result_passed")

        result_failed = d.pop("result_failed")

        status_completed = d.pop("status_completed")

        status_error = d.pop("status_error")

        status_running = d.pop("status_running")

        status_pending = d.pop("status_pending")

        status_paused = d.pop("status_paused")

        status_canceled = d.pop("status_canceled")

        status = TestStatusEnum(d.pop("status"))

        def _parse_total_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_score = _parse_total_score(d.pop("total_score", UNSET))

        def _parse_total_score_change(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_score_change = _parse_total_score_change(d.pop("total_score_change", UNSET))

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

        def _parse_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_criteria_failures(data: object) -> Union["TestRunMetricScoresCriteriaFailuresType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                criteria_failures_type_0 = TestRunMetricScoresCriteriaFailuresType0.from_dict(data)

                return criteria_failures_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestRunMetricScoresCriteriaFailuresType0", None, Unset], data)

        criteria_failures = _parse_criteria_failures(d.pop("criteria_failures", UNSET))

        test_run_metric_scores = cls(
            total_conversations=total_conversations,
            result_passed=result_passed,
            result_failed=result_failed,
            status_completed=status_completed,
            status_error=status_error,
            status_running=status_running,
            status_pending=status_pending,
            status_paused=status_paused,
            status_canceled=status_canceled,
            status=status,
            total_score=total_score,
            total_score_change=total_score_change,
            result=result,
            summary=summary,
            criteria_failures=criteria_failures,
        )

        test_run_metric_scores.additional_properties = d
        return test_run_metric_scores

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
