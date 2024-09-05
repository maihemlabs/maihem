from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.conversation_nested import ConversationNested


T = TypeVar("T", bound="APISchemaConversationTurnCreateResponse")


@_attrs_define
class APISchemaConversationTurnCreateResponse:
    """
    Attributes:
        turn_id (str):
        conversation (ConversationNested):
    """

    turn_id: str
    conversation: "ConversationNested"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        turn_id = self.turn_id

        conversation = self.conversation.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "turn_id": turn_id,
                "conversation": conversation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested import ConversationNested

        d = src_dict.copy()
        turn_id = d.pop("turn_id")

        conversation = ConversationNested.from_dict(d.pop("conversation"))

        api_schema_conversation_turn_create_response = cls(
            turn_id=turn_id,
            conversation=conversation,
        )

        api_schema_conversation_turn_create_response.additional_properties = d
        return api_schema_conversation_turn_create_response

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
