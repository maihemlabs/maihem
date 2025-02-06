from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConversationTurnCreateRequest")


@_attrs_define
class ConversationTurnCreateRequest:
    """
    Attributes:
        message (Union[None, Unset, str]):
        contexts (Union[None, Unset, list[str]]):
    """

    message: Union[None, Unset, str] = UNSET
    contexts: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        contexts: Union[None, Unset, list[str]]
        if isinstance(self.contexts, Unset):
            contexts = UNSET
        elif isinstance(self.contexts, list):
            contexts = self.contexts

        else:
            contexts = self.contexts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if contexts is not UNSET:
            field_dict["contexts"] = contexts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_contexts(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                contexts_type_0 = cast(list[str], data)

                return contexts_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        contexts = _parse_contexts(d.pop("contexts", UNSET))

        conversation_turn_create_request = cls(
            message=message,
            contexts=contexts,
        )

        conversation_turn_create_request.additional_properties = d
        return conversation_turn_create_request

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
