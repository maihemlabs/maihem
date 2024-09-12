from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested import ConversationNested


T = TypeVar("T", bound="APISchemaConversationTurnCreateResponse")


@_attrs_define
class APISchemaConversationTurnCreateResponse:
    """
    Attributes:
        conversation (ConversationNested):
        turn_id (Union[None, Unset, str]):
    """

    conversation: "ConversationNested"
    turn_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conversation = self.conversation.to_dict()

        turn_id: Union[None, Unset, str]
        if isinstance(self.turn_id, Unset):
            turn_id = UNSET
        else:
            turn_id = self.turn_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation": conversation,
            }
        )
        if turn_id is not UNSET:
            field_dict["turn_id"] = turn_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested import ConversationNested

        d = src_dict.copy()
        conversation = ConversationNested.from_dict(d.pop("conversation"))

        def _parse_turn_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        turn_id = _parse_turn_id(d.pop("turn_id", UNSET))

        api_schema_conversation_turn_create_response = cls(
            conversation=conversation,
            turn_id=turn_id,
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
