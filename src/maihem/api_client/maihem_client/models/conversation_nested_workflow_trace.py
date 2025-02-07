import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_workflow_span import ConversationNestedWorkflowSpan


T = TypeVar("T", bound="ConversationNestedWorkflowTrace")


@_attrs_define
class ConversationNestedWorkflowTrace:
    """
    Attributes:
        id (str):
        workflow_id (str):
        started_at (datetime.datetime):
        completed_at (datetime.datetime):
        created_at (Union[None, Unset, datetime.datetime]):
        updated_at (Union[None, Unset, datetime.datetime]):
        workflow_spans (Union[Unset, list['ConversationNestedWorkflowSpan']]):
    """

    id: str
    workflow_id: str
    started_at: datetime.datetime
    completed_at: datetime.datetime
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    workflow_spans: Union[Unset, list["ConversationNestedWorkflowSpan"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        workflow_id = self.workflow_id

        started_at = self.started_at.isoformat()

        completed_at = self.completed_at.isoformat()

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        workflow_spans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_spans, Unset):
            workflow_spans = []
            for workflow_spans_item_data in self.workflow_spans:
                workflow_spans_item = workflow_spans_item_data.to_dict()
                workflow_spans.append(workflow_spans_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workflow_id": workflow_id,
                "started_at": started_at,
                "completed_at": completed_at,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if workflow_spans is not UNSET:
            field_dict["workflow_spans"] = workflow_spans

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.conversation_nested_workflow_span import ConversationNestedWorkflowSpan

        d = src_dict.copy()
        id = d.pop("id")

        workflow_id = d.pop("workflow_id")

        started_at = isoparse(d.pop("started_at"))

        completed_at = isoparse(d.pop("completed_at"))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        workflow_spans = []
        _workflow_spans = d.pop("workflow_spans", UNSET)
        for workflow_spans_item_data in _workflow_spans or []:
            workflow_spans_item = ConversationNestedWorkflowSpan.from_dict(workflow_spans_item_data)

            workflow_spans.append(workflow_spans_item)

        conversation_nested_workflow_trace = cls(
            id=id,
            workflow_id=workflow_id,
            started_at=started_at,
            completed_at=completed_at,
            created_at=created_at,
            updated_at=updated_at,
            workflow_spans=workflow_spans,
        )

        conversation_nested_workflow_trace.additional_properties = d
        return conversation_nested_workflow_trace

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
