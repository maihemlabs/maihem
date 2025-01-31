from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VTestRunWorkflowResult")


@_attrs_define
class VTestRunWorkflowResult:
    """
    Attributes:
        org_id (str):
        test_id (str):
        test_run_id (str):
        workflow_id (str):
        score (Union[Any, None]):
        result (Union[Any, None]):
        total_conversations (int):
        total_messages (int):
        total_failures (int):
        avg_duration_ms (str):
    """

    org_id: str
    test_id: str
    test_run_id: str
    workflow_id: str
    score: Union[Any, None]
    result: Union[Any, None]
    total_conversations: int
    total_messages: int
    total_failures: int
    avg_duration_ms: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org_id = self.org_id

        test_id = self.test_id

        test_run_id = self.test_run_id

        workflow_id = self.workflow_id

        score: Union[Any, None]
        score = self.score

        result: Union[Any, None]
        result = self.result

        total_conversations = self.total_conversations

        total_messages = self.total_messages

        total_failures = self.total_failures

        avg_duration_ms = self.avg_duration_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org_id": org_id,
                "test_id": test_id,
                "test_run_id": test_run_id,
                "workflow_id": workflow_id,
                "score": score,
                "result": result,
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "total_failures": total_failures,
                "avg_duration_ms": avg_duration_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org_id = d.pop("org_id")

        test_id = d.pop("test_id")

        test_run_id = d.pop("test_run_id")

        workflow_id = d.pop("workflow_id")

        def _parse_score(data: object) -> Union[Any, None]:
            if data is None:
                return data
            return cast(Union[Any, None], data)

        score = _parse_score(d.pop("score"))

        def _parse_result(data: object) -> Union[Any, None]:
            if data is None:
                return data
            return cast(Union[Any, None], data)

        result = _parse_result(d.pop("result"))

        total_conversations = d.pop("total_conversations")

        total_messages = d.pop("total_messages")

        total_failures = d.pop("total_failures")

        avg_duration_ms = d.pop("avg_duration_ms")

        v_test_run_workflow_result = cls(
            org_id=org_id,
            test_id=test_id,
            test_run_id=test_run_id,
            workflow_id=workflow_id,
            score=score,
            result=result,
            total_conversations=total_conversations,
            total_messages=total_messages,
            total_failures=total_failures,
            avg_duration_ms=avg_duration_ms,
        )

        v_test_run_workflow_result.additional_properties = d
        return v_test_run_workflow_result

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
