from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConversationNestedTokenCostBase")


@_attrs_define
class ConversationNestedTokenCostBase:
    """
    Attributes:
        input_tokens (int):
        output_tokens (int):
        cost_amount (int):
        cost_currency (str):
        id (Union[None, Unset, str]):
    """

    input_tokens: int
    output_tokens: int
    cost_amount: int
    cost_currency: str
    id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        cost_amount = self.cost_amount

        cost_currency = self.cost_currency

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_amount": cost_amount,
                "cost_currency": cost_currency,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_tokens = d.pop("input_tokens")

        output_tokens = d.pop("output_tokens")

        cost_amount = d.pop("cost_amount")

        cost_currency = d.pop("cost_currency")

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        conversation_nested_token_cost_base = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_amount=cost_amount,
            cost_currency=cost_currency,
            id=id,
        )

        conversation_nested_token_cost_base.additional_properties = d
        return conversation_nested_token_cost_base

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
