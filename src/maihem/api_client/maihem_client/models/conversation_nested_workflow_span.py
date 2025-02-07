import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_evaluation_base import ConversationNestedEvaluationBase
    from ..models.conversation_nested_workflow_span_input_payload import ConversationNestedWorkflowSpanInputPayload
    from ..models.conversation_nested_workflow_span_output_payload import ConversationNestedWorkflowSpanOutputPayload


T = TypeVar("T", bound="ConversationNestedWorkflowSpan")


@_attrs_define
class ConversationNestedWorkflowSpan:
    """
    Attributes:
        id (str):
        name (str):
        input_payload (ConversationNestedWorkflowSpanInputPayload):
        output_payload (ConversationNestedWorkflowSpanOutputPayload):
        started_at (datetime.datetime):
        completed_at (datetime.datetime):
        evaluators (Union[Unset, list[str]]):
        parent_span_id (Union[None, Unset, str]):
        evaluations (Union[Unset, list['ConversationNestedEvaluationBase']]):
    """

    id: str
    name: str
    input_payload: "ConversationNestedWorkflowSpanInputPayload"
    output_payload: "ConversationNestedWorkflowSpanOutputPayload"
    started_at: datetime.datetime
    completed_at: datetime.datetime
    evaluators: Union[Unset, list[str]] = UNSET
    parent_span_id: Union[None, Unset, str] = UNSET
    evaluations: Union[Unset, list["ConversationNestedEvaluationBase"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        input_payload = self.input_payload.to_dict()

        output_payload = self.output_payload.to_dict()

        started_at = self.started_at.isoformat()

        completed_at = self.completed_at.isoformat()

        evaluators: Union[Unset, list[str]] = UNSET
        if not isinstance(self.evaluators, Unset):
            evaluators = self.evaluators

        parent_span_id: Union[None, Unset, str]
        if isinstance(self.parent_span_id, Unset):
            parent_span_id = UNSET
        else:
            parent_span_id = self.parent_span_id

        evaluations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.evaluations, Unset):
            evaluations = []
            for evaluations_item_data in self.evaluations:
                evaluations_item = evaluations_item_data.to_dict()
                evaluations.append(evaluations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "input_payload": input_payload,
                "output_payload": output_payload,
                "started_at": started_at,
                "completed_at": completed_at,
            }
        )
        if evaluators is not UNSET:
            field_dict["evaluators"] = evaluators
        if parent_span_id is not UNSET:
            field_dict["parent_span_id"] = parent_span_id
        if evaluations is not UNSET:
            field_dict["evaluations"] = evaluations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.conversation_nested_evaluation_base import ConversationNestedEvaluationBase
        from ..models.conversation_nested_workflow_span_input_payload import ConversationNestedWorkflowSpanInputPayload
        from ..models.conversation_nested_workflow_span_output_payload import (
            ConversationNestedWorkflowSpanOutputPayload,
        )

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        input_payload = ConversationNestedWorkflowSpanInputPayload.from_dict(d.pop("input_payload"))

        output_payload = ConversationNestedWorkflowSpanOutputPayload.from_dict(d.pop("output_payload"))

        started_at = isoparse(d.pop("started_at"))

        completed_at = isoparse(d.pop("completed_at"))

        evaluators = cast(list[str], d.pop("evaluators", UNSET))

        def _parse_parent_span_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_span_id = _parse_parent_span_id(d.pop("parent_span_id", UNSET))

        evaluations = []
        _evaluations = d.pop("evaluations", UNSET)
        for evaluations_item_data in _evaluations or []:
            evaluations_item = ConversationNestedEvaluationBase.from_dict(evaluations_item_data)

            evaluations.append(evaluations_item)

        conversation_nested_workflow_span = cls(
            id=id,
            name=name,
            input_payload=input_payload,
            output_payload=output_payload,
            started_at=started_at,
            completed_at=completed_at,
            evaluators=evaluators,
            parent_span_id=parent_span_id,
            evaluations=evaluations,
        )

        conversation_nested_workflow_span.additional_properties = d
        return conversation_nested_workflow_span

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
