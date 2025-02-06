from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetItemCreateItemRequest")


@_attrs_define
class DatasetItemCreateItemRequest:
    """
    Attributes:
        input_payload (str):
        external_id (Union[None, Unset, str]):
        output_payload_expected (Union[None, Unset, str]):
        conversation_history (Union[None, Unset, str]):
    """

    input_payload: str
    external_id: Union[None, Unset, str] = UNSET
    output_payload_expected: Union[None, Unset, str] = UNSET
    conversation_history: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_payload = self.input_payload

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        output_payload_expected: Union[None, Unset, str]
        if isinstance(self.output_payload_expected, Unset):
            output_payload_expected = UNSET
        else:
            output_payload_expected = self.output_payload_expected

        conversation_history: Union[None, Unset, str]
        if isinstance(self.conversation_history, Unset):
            conversation_history = UNSET
        else:
            conversation_history = self.conversation_history

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_payload": input_payload,
            }
        )
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if output_payload_expected is not UNSET:
            field_dict["output_payload_expected"] = output_payload_expected
        if conversation_history is not UNSET:
            field_dict["conversation_history"] = conversation_history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        input_payload = d.pop("input_payload")

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_output_payload_expected(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_payload_expected = _parse_output_payload_expected(d.pop("output_payload_expected", UNSET))

        def _parse_conversation_history(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        conversation_history = _parse_conversation_history(d.pop("conversation_history", UNSET))

        dataset_item_create_item_request = cls(
            input_payload=input_payload,
            external_id=external_id,
            output_payload_expected=output_payload_expected,
            conversation_history=conversation_history,
        )

        dataset_item_create_item_request.additional_properties = d
        return dataset_item_create_item_request

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
