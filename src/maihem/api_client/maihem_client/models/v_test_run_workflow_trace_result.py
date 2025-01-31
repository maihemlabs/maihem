import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="VTestRunWorkflowTraceResult")


@_attrs_define
class VTestRunWorkflowTraceResult:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        started_at (datetime.datetime):
        completed_at (datetime.datetime):
        duration_ms (str):
        workflow_id (str):
        name (str):
        label (Union[None, str]):
        result (Union[None, str]):
        org_id (str):
        test_run_id (str):
        conversation_id (str):
        conversation_message_id (str):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    started_at: datetime.datetime
    completed_at: datetime.datetime
    duration_ms: str
    workflow_id: str
    name: str
    label: Union[None, str]
    result: Union[None, str]
    org_id: str
    test_run_id: str
    conversation_id: str
    conversation_message_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        started_at = self.started_at.isoformat()

        completed_at = self.completed_at.isoformat()

        duration_ms = self.duration_ms

        workflow_id = self.workflow_id

        name = self.name

        label: Union[None, str]
        label = self.label

        result: Union[None, str]
        result = self.result

        org_id = self.org_id

        test_run_id = self.test_run_id

        conversation_id = self.conversation_id

        conversation_message_id = self.conversation_message_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "started_at": started_at,
                "completed_at": completed_at,
                "duration_ms": duration_ms,
                "workflow_id": workflow_id,
                "name": name,
                "label": label,
                "result": result,
                "org_id": org_id,
                "test_run_id": test_run_id,
                "conversation_id": conversation_id,
                "conversation_message_id": conversation_message_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        started_at = isoparse(d.pop("started_at"))

        completed_at = isoparse(d.pop("completed_at"))

        duration_ms = d.pop("duration_ms")

        workflow_id = d.pop("workflow_id")

        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        label = _parse_label(d.pop("label"))

        def _parse_result(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        result = _parse_result(d.pop("result"))

        org_id = d.pop("org_id")

        test_run_id = d.pop("test_run_id")

        conversation_id = d.pop("conversation_id")

        conversation_message_id = d.pop("conversation_message_id")

        v_test_run_workflow_trace_result = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            workflow_id=workflow_id,
            name=name,
            label=label,
            result=result,
            org_id=org_id,
            test_run_id=test_run_id,
            conversation_id=conversation_id,
            conversation_message_id=conversation_message_id,
        )

        v_test_run_workflow_trace_result.additional_properties = d
        return v_test_run_workflow_trace_result

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
