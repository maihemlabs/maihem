from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConversationNestedTokenCost")


@_attrs_define
class ConversationNestedTokenCost:
    """
    Attributes:
        id (str):
        input_tokens (int):
        output_tokens (int):
        cost_amount (int):
        cost_currency (str):
    """

    id: str
    input_tokens: int
    output_tokens: int
    cost_amount: int
    cost_currency: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        cost_amount = self.cost_amount

        cost_currency = self.cost_currency

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_amount": cost_amount,
                "cost_currency": cost_currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        input_tokens = d.pop("input_tokens")

        output_tokens = d.pop("output_tokens")

        cost_amount = d.pop("cost_amount")

        cost_currency = d.pop("cost_currency")

        conversation_nested_token_cost = cls(
            id=id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_amount=cost_amount,
            cost_currency=cost_currency,
        )

        conversation_nested_token_cost.additional_properties = d
        return conversation_nested_token_cost

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
