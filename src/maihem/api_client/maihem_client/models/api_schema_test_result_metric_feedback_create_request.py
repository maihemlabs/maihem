from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_schema_test_result_metric_feedback_create_request_feedback import (
    APISchemaTestResultMetricFeedbackCreateRequestFeedback,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaTestResultMetricFeedbackCreateRequest")


@_attrs_define
class APISchemaTestResultMetricFeedbackCreateRequest:
    """
    Attributes:
        feedback (Union[Unset, APISchemaTestResultMetricFeedbackCreateRequestFeedback]):  Default:
            APISchemaTestResultMetricFeedbackCreateRequestFeedback.POSITIVE.
        comments (Union[None, Unset, str]):
    """

    feedback: Union[Unset, APISchemaTestResultMetricFeedbackCreateRequestFeedback] = (
        APISchemaTestResultMetricFeedbackCreateRequestFeedback.POSITIVE
    )
    comments: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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
        field_dict.update({})
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _feedback = d.pop("feedback", UNSET)
        feedback: Union[Unset, APISchemaTestResultMetricFeedbackCreateRequestFeedback]
        if isinstance(_feedback, Unset):
            feedback = UNSET
        else:
            feedback = APISchemaTestResultMetricFeedbackCreateRequestFeedback(_feedback)

        def _parse_comments(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comments = _parse_comments(d.pop("comments", UNSET))

        api_schema_test_result_metric_feedback_create_request = cls(
            feedback=feedback,
            comments=comments,
        )

        api_schema_test_result_metric_feedback_create_request.additional_properties = d
        return api_schema_test_result_metric_feedback_create_request

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
