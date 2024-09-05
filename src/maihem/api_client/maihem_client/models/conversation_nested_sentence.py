import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_test_result_metric import ConversationNestedTestResultMetric


T = TypeVar("T", bound="ConversationNestedSentence")


@_attrs_define
class ConversationNestedSentence:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        content (str):
        test_result_metrics (Union[Unset, List['ConversationNestedTestResultMetric']]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    content: str
    test_result_metrics: Union[Unset, List["ConversationNestedTestResultMetric"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        content = self.content

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
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "content": content,
            }
        )
        if test_result_metrics is not UNSET:
            field_dict["test_result_metrics"] = test_result_metrics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_test_result_metric import ConversationNestedTestResultMetric

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        content = d.pop("content")

        test_result_metrics = []
        _test_result_metrics = d.pop("test_result_metrics", UNSET)
        for test_result_metrics_item_data in _test_result_metrics or []:
            test_result_metrics_item = ConversationNestedTestResultMetric.from_dict(test_result_metrics_item_data)

            test_result_metrics.append(test_result_metrics_item)

        conversation_nested_sentence = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            content=content,
            test_result_metrics=test_result_metrics,
        )

        conversation_nested_sentence.additional_properties = d
        return conversation_nested_sentence

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
