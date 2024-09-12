from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaLinks")


@_attrs_define
class APISchemaLinks:
    """
    Attributes:
        test_conversations (Union[None, Unset, str]):
        test_result (Union[None, Unset, str]):
        test_result_conversations (Union[None, Unset, str]):
    """

    test_conversations: Union[None, Unset, str] = UNSET
    test_result: Union[None, Unset, str] = UNSET
    test_result_conversations: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_conversations: Union[None, Unset, str]
        if isinstance(self.test_conversations, Unset):
            test_conversations = UNSET
        else:
            test_conversations = self.test_conversations

        test_result: Union[None, Unset, str]
        if isinstance(self.test_result, Unset):
            test_result = UNSET
        else:
            test_result = self.test_result

        test_result_conversations: Union[None, Unset, str]
        if isinstance(self.test_result_conversations, Unset):
            test_result_conversations = UNSET
        else:
            test_result_conversations = self.test_result_conversations

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if test_conversations is not UNSET:
            field_dict["test_conversations"] = test_conversations
        if test_result is not UNSET:
            field_dict["test_result"] = test_result
        if test_result_conversations is not UNSET:
            field_dict["test_result_conversations"] = test_result_conversations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_test_conversations(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_conversations = _parse_test_conversations(d.pop("test_conversations", UNSET))

        def _parse_test_result(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_result = _parse_test_result(d.pop("test_result", UNSET))

        def _parse_test_result_conversations(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_result_conversations = _parse_test_result_conversations(d.pop("test_result_conversations", UNSET))

        api_schema_links = cls(
            test_conversations=test_conversations,
            test_result=test_result,
            test_result_conversations=test_result_conversations,
        )

        api_schema_links.additional_properties = d
        return api_schema_links

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
