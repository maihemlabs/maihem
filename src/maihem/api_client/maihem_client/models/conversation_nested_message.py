import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type import AgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
    from ..models.conversation_nested_sentence import ConversationNestedSentence
    from ..models.conversation_nested_workflow_trace import ConversationNestedWorkflowTrace


T = TypeVar("T", bound="ConversationNestedMessage")


@_attrs_define
class ConversationNestedMessage:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        agent_type (AgentType):
        content (Union[None, Unset, str]):
        end_code (Union[None, Unset, str]):
        evaluations (Union[Unset, list['ConversationNestedEvaluation']]):
        conversation_sentences (Union[Unset, list['ConversationNestedSentence']]):
        workflow_trace (Union['ConversationNestedWorkflowTrace', None, Unset]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    agent_type: AgentType
    content: Union[None, Unset, str] = UNSET
    end_code: Union[None, Unset, str] = UNSET
    evaluations: Union[Unset, list["ConversationNestedEvaluation"]] = UNSET
    conversation_sentences: Union[Unset, list["ConversationNestedSentence"]] = UNSET
    workflow_trace: Union["ConversationNestedWorkflowTrace", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conversation_nested_workflow_trace import ConversationNestedWorkflowTrace

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        agent_type = self.agent_type.value

        content: Union[None, Unset, str]
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        end_code: Union[None, Unset, str]
        if isinstance(self.end_code, Unset):
            end_code = UNSET
        else:
            end_code = self.end_code

        evaluations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.evaluations, Unset):
            evaluations = []
            for evaluations_item_data in self.evaluations:
                evaluations_item = evaluations_item_data.to_dict()
                evaluations.append(evaluations_item)

        conversation_sentences: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.conversation_sentences, Unset):
            conversation_sentences = []
            for conversation_sentences_item_data in self.conversation_sentences:
                conversation_sentences_item = conversation_sentences_item_data.to_dict()
                conversation_sentences.append(conversation_sentences_item)

        workflow_trace: Union[None, Unset, dict[str, Any]]
        if isinstance(self.workflow_trace, Unset):
            workflow_trace = UNSET
        elif isinstance(self.workflow_trace, ConversationNestedWorkflowTrace):
            workflow_trace = self.workflow_trace.to_dict()
        else:
            workflow_trace = self.workflow_trace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "agent_type": agent_type,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if end_code is not UNSET:
            field_dict["end_code"] = end_code
        if evaluations is not UNSET:
            field_dict["evaluations"] = evaluations
        if conversation_sentences is not UNSET:
            field_dict["conversation_sentences"] = conversation_sentences
        if workflow_trace is not UNSET:
            field_dict["workflow_trace"] = workflow_trace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
        from ..models.conversation_nested_sentence import ConversationNestedSentence
        from ..models.conversation_nested_workflow_trace import ConversationNestedWorkflowTrace

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        agent_type = AgentType(d.pop("agent_type"))

        def _parse_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_end_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end_code = _parse_end_code(d.pop("end_code", UNSET))

        evaluations = []
        _evaluations = d.pop("evaluations", UNSET)
        for evaluations_item_data in _evaluations or []:
            evaluations_item = ConversationNestedEvaluation.from_dict(evaluations_item_data)

            evaluations.append(evaluations_item)

        conversation_sentences = []
        _conversation_sentences = d.pop("conversation_sentences", UNSET)
        for conversation_sentences_item_data in _conversation_sentences or []:
            conversation_sentences_item = ConversationNestedSentence.from_dict(conversation_sentences_item_data)

            conversation_sentences.append(conversation_sentences_item)

        def _parse_workflow_trace(data: object) -> Union["ConversationNestedWorkflowTrace", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                workflow_trace_type_0 = ConversationNestedWorkflowTrace.from_dict(data)

                return workflow_trace_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ConversationNestedWorkflowTrace", None, Unset], data)

        workflow_trace = _parse_workflow_trace(d.pop("workflow_trace", UNSET))

        conversation_nested_message = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            agent_type=agent_type,
            content=content,
            end_code=end_code,
            evaluations=evaluations,
            conversation_sentences=conversation_sentences,
            workflow_trace=workflow_trace,
        )

        conversation_nested_message.additional_properties = d
        return conversation_nested_message

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
