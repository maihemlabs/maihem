from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestRunConversationScores")


@_attrs_define
class TestRunConversationScores:
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

        status_canceled = self.status_canceled

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
            }
        )

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

        status_canceled = d.pop("status_canceled")

        test_run_conversation_scores = cls(
            total_conversations=total_conversations,
            result_passed=result_passed,
            result_failed=result_failed,
            status_completed=status_completed,
            status_error=status_error,
            status_running=status_running,
            status_pending=status_pending,
            status_paused=status_paused,
            status_canceled=status_canceled,
        )

        test_run_conversation_scores.additional_properties = d
        return test_run_conversation_scores

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
