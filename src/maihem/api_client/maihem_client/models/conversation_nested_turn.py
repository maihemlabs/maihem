import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
    from ..models.conversation_nested_message import ConversationNestedMessage


T = TypeVar("T", bound="ConversationNestedTurn")


@_attrs_define
class ConversationNestedTurn:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        evaluations (Union[Unset, List['ConversationNestedEvaluation']]):
        conversation_messages (Union[Unset, List['ConversationNestedMessage']]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    evaluations: Union[Unset, List["ConversationNestedEvaluation"]] = UNSET
    conversation_messages: Union[Unset, List["ConversationNestedMessage"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        evaluations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.evaluations, Unset):
            evaluations = []
            for evaluations_item_data in self.evaluations:
                evaluations_item = evaluations_item_data.to_dict()
                evaluations.append(evaluations_item)

        conversation_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conversation_messages, Unset):
            conversation_messages = []
            for conversation_messages_item_data in self.conversation_messages:
                conversation_messages_item = conversation_messages_item_data.to_dict()
                conversation_messages.append(conversation_messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if evaluations is not UNSET:
            field_dict["evaluations"] = evaluations
        if conversation_messages is not UNSET:
            field_dict["conversation_messages"] = conversation_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
        from ..models.conversation_nested_message import ConversationNestedMessage

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        evaluations = []
        _evaluations = d.pop("evaluations", UNSET)
        for evaluations_item_data in _evaluations or []:
            evaluations_item = ConversationNestedEvaluation.from_dict(evaluations_item_data)

            evaluations.append(evaluations_item)

        conversation_messages = []
        _conversation_messages = d.pop("conversation_messages", UNSET)
        for conversation_messages_item_data in _conversation_messages or []:
            conversation_messages_item = ConversationNestedMessage.from_dict(conversation_messages_item_data)

            conversation_messages.append(conversation_messages_item)

        conversation_nested_turn = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            evaluations=evaluations,
            conversation_messages=conversation_messages,
        )

        conversation_nested_turn.additional_properties = d
        return conversation_nested_turn

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
