from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_test_result_metric_base import ConversationNestedTestResultMetricBase


T = TypeVar("T", bound="ConversationNestedSentenceBase")


@_attrs_define
class ConversationNestedSentenceBase:
    """
    Attributes:
        content (str):
        id (Union[None, Unset, str]):
        test_result_metrics (Union[Unset, List['ConversationNestedTestResultMetricBase']]):
    """

    content: str
    id: Union[None, Unset, str] = UNSET
    test_result_metrics: Union[Unset, List["ConversationNestedTestResultMetricBase"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        test_result_metrics: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.test_result_metrics, Unset):
            test_result_metrics = []
            for test_result_metrics_item_data in self.test_result_metrics:
                test_result_metrics_item = test_result_metrics_item_data.to_dict()
                test_result_metrics.append(test_result_metrics_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if test_result_metrics is not UNSET:
            field_dict["test_result_metrics"] = test_result_metrics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_test_result_metric_base import ConversationNestedTestResultMetricBase

        d = src_dict.copy()
        content = d.pop("content")

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        test_result_metrics = []
        _test_result_metrics = d.pop("test_result_metrics", UNSET)
        for test_result_metrics_item_data in _test_result_metrics or []:
            test_result_metrics_item = ConversationNestedTestResultMetricBase.from_dict(test_result_metrics_item_data)

            test_result_metrics.append(test_result_metrics_item)

        conversation_nested_sentence_base = cls(
            content=content,
            id=id,
            test_result_metrics=test_result_metrics,
        )

        conversation_nested_sentence_base.additional_properties = d
        return conversation_nested_sentence_base

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
