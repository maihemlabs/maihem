from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_metric_feedback_create_request_feedback import TestResultMetricFeedbackCreateRequestFeedback
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestResultMetricFeedbackCreateRequest")


@_attrs_define
class TestResultMetricFeedbackCreateRequest:
    """
    Attributes:
        entity_id (str):
        entity_type (str):
        test_result_metric_id (Union[None, Unset, str]):
        feedback (Union[Unset, TestResultMetricFeedbackCreateRequestFeedback]):  Default:
            TestResultMetricFeedbackCreateRequestFeedback.POSITIVE.
        comments (Union[None, Unset, str]):
    """

    entity_id: str
    entity_type: str
    test_result_metric_id: Union[None, Unset, str] = UNSET
    feedback: Union[Unset, TestResultMetricFeedbackCreateRequestFeedback] = (
        TestResultMetricFeedbackCreateRequestFeedback.POSITIVE
    )
    comments: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id

        entity_type = self.entity_type

        test_result_metric_id: Union[None, Unset, str]
        if isinstance(self.test_result_metric_id, Unset):
            test_result_metric_id = UNSET
        else:
            test_result_metric_id = self.test_result_metric_id

        feedback: Union[Unset, str] = UNSET
        if not isinstance(self.feedback, Unset):
            feedback = self.feedback.value

        comments: Union[None, Unset, str]
        if isinstance(self.comments, Unset):
            comments = UNSET
        else:
            comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
            }
        )
        if test_result_metric_id is not UNSET:
            field_dict["test_result_metric_id"] = test_result_metric_id
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entity_id")

        entity_type = d.pop("entity_type")

        def _parse_test_result_metric_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_result_metric_id = _parse_test_result_metric_id(d.pop("test_result_metric_id", UNSET))

        _feedback = d.pop("feedback", UNSET)
        feedback: Union[Unset, TestResultMetricFeedbackCreateRequestFeedback]
        if isinstance(_feedback, Unset):
            feedback = UNSET
        else:
            feedback = TestResultMetricFeedbackCreateRequestFeedback(_feedback)

        def _parse_comments(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comments = _parse_comments(d.pop("comments", UNSET))

        test_result_metric_feedback_create_request = cls(
            entity_id=entity_id,
            entity_type=entity_type,
            test_result_metric_id=test_result_metric_id,
            feedback=feedback,
            comments=comments,
        )

        test_result_metric_feedback_create_request.additional_properties = d
        return test_result_metric_feedback_create_request

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
