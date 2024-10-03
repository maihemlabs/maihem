from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaTestRunConversationCounts")


@_attrs_define
class APISchemaTestRunConversationCounts:
    """
    Attributes:
        total_conversations (int):
        result_passed (int):
        result_failed (int):
        result_errored (int):
        result_pending (int):
        result_canceled (int):
        status_completed (int):
        status_failed (int):
        status_running (int):
        status_pending (int):
        status_paused (int):
        total_score (Union[None, Unset, float]):
    """

    total_conversations: int
    result_passed: int
    result_failed: int
    result_errored: int
    result_pending: int
    result_canceled: int
    status_completed: int
    status_failed: int
    status_running: int
    status_pending: int
    status_paused: int
    total_score: Union[None, Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_conversations = self.total_conversations

        result_passed = self.result_passed

        result_failed = self.result_failed

        result_errored = self.result_errored

        result_pending = self.result_pending

        result_canceled = self.result_canceled

        status_completed = self.status_completed

        status_failed = self.status_failed

        status_running = self.status_running

        status_pending = self.status_pending

        status_paused = self.status_paused

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
                "result_errored": result_errored,
                "result_pending": result_pending,
                "result_canceled": result_canceled,
                "status_completed": status_completed,
                "status_failed": status_failed,
                "status_running": status_running,
                "status_pending": status_pending,
                "status_paused": status_paused,
            }
        )
        if total_score is not UNSET:
            field_dict["total_score"] = total_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_conversations = d.pop("total_conversations")

        result_passed = d.pop("result_passed")

        result_failed = d.pop("result_failed")

        result_errored = d.pop("result_errored")

        result_pending = d.pop("result_pending")

        result_canceled = d.pop("result_canceled")

        status_completed = d.pop("status_completed")

        status_failed = d.pop("status_failed")

        status_running = d.pop("status_running")

        status_pending = d.pop("status_pending")

        status_paused = d.pop("status_paused")

        def _parse_total_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_score = _parse_total_score(d.pop("total_score", UNSET))

        api_schema_test_run_conversation_counts = cls(
            total_conversations=total_conversations,
            result_passed=result_passed,
            result_failed=result_failed,
            result_errored=result_errored,
            result_pending=result_pending,
            result_canceled=result_canceled,
            status_completed=status_completed,
            status_failed=status_failed,
            status_running=status_running,
            status_pending=status_pending,
            status_paused=status_paused,
            total_score=total_score,
        )

        api_schema_test_run_conversation_counts.additional_properties = d
        return api_schema_test_run_conversation_counts

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
