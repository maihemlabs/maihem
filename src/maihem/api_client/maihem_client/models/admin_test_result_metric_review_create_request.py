from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminTestResultMetricReviewCreateRequest")


@_attrs_define
class AdminTestResultMetricReviewCreateRequest:
    """
    Attributes:
        entity_id (str):
        entity_type (str):
        action (str):
        test_result_metric_id (Union[None, Unset, str]):
        event (Union[Unset, str]):  Default: 'added'.
        content (Union[None, Unset, str]):
    """

    entity_id: str
    entity_type: str
    action: str
    test_result_metric_id: Union[None, Unset, str] = UNSET
    event: Union[Unset, str] = "added"
    content: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id

        entity_type = self.entity_type

        action = self.action

        test_result_metric_id: Union[None, Unset, str]
        if isinstance(self.test_result_metric_id, Unset):
            test_result_metric_id = UNSET
        else:
            test_result_metric_id = self.test_result_metric_id

        event = self.event

        content: Union[None, Unset, str]
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "action": action,
            }
        )
        if test_result_metric_id is not UNSET:
            field_dict["test_result_metric_id"] = test_result_metric_id
        if event is not UNSET:
            field_dict["event"] = event
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entity_id")

        entity_type = d.pop("entity_type")

        action = d.pop("action")

        def _parse_test_result_metric_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_result_metric_id = _parse_test_result_metric_id(d.pop("test_result_metric_id", UNSET))

        event = d.pop("event", UNSET)

        def _parse_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        admin_test_result_metric_review_create_request = cls(
            entity_id=entity_id,
            entity_type=entity_type,
            action=action,
            test_result_metric_id=test_result_metric_id,
            event=event,
            content=content,
        )

        admin_test_result_metric_review_create_request.additional_properties = d
        return admin_test_result_metric_review_create_request

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
