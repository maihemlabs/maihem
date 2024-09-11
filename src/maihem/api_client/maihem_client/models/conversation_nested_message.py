import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type import AgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
    from ..models.conversation_nested_sentence import ConversationNestedSentence


T = TypeVar("T", bound="ConversationNestedMessage")


@_attrs_define
class ConversationNestedMessage:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        agent_type (AgentType):
        content (str):
        end_code (Union[None, Unset, str]):
        evaluations (Union[Unset, List['ConversationNestedEvaluation']]):
        conversation_sentences (Union[Unset, List['ConversationNestedSentence']]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    agent_type: AgentType
    content: str
    end_code: Union[None, Unset, str] = UNSET
    evaluations: Union[Unset, List["ConversationNestedEvaluation"]] = UNSET
    conversation_sentences: Union[Unset, List["ConversationNestedSentence"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        agent_type = self.agent_type.value

        content = self.content

        end_code: Union[None, Unset, str]
        if isinstance(self.end_code, Unset):
            end_code = UNSET
        else:
            end_code = self.end_code

        evaluations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.evaluations, Unset):
            evaluations = []
            for evaluations_item_data in self.evaluations:
                evaluations_item = evaluations_item_data.to_dict()
                evaluations.append(evaluations_item)

        conversation_sentences: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conversation_sentences, Unset):
            conversation_sentences = []
            for conversation_sentences_item_data in self.conversation_sentences:
                conversation_sentences_item = conversation_sentences_item_data.to_dict()
                conversation_sentences.append(conversation_sentences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "agent_type": agent_type,
                "content": content,
            }
        )
        if end_code is not UNSET:
            field_dict["end_code"] = end_code
        if evaluations is not UNSET:
            field_dict["evaluations"] = evaluations
        if conversation_sentences is not UNSET:
            field_dict["conversation_sentences"] = conversation_sentences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
        from ..models.conversation_nested_sentence import ConversationNestedSentence

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        agent_type = AgentType(d.pop("agent_type"))

        content = d.pop("content")

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

        conversation_nested_message = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            agent_type=agent_type,
            content=content,
            end_code=end_code,
            evaluations=evaluations,
            conversation_sentences=conversation_sentences,
        )

        conversation_nested_message.additional_properties = d
        return conversation_nested_message

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
