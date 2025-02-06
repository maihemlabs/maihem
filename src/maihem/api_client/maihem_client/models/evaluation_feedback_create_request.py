from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.evaluation_feedback_create_request_feedback import EvaluationFeedbackCreateRequestFeedback
from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluationFeedbackCreateRequest")


@_attrs_define
class EvaluationFeedbackCreateRequest:
    """
    Attributes:
        entity_id (str):
        entity_type (str):
        evaluation_id (Union[None, Unset, str]):
        feedback (Union[Unset, EvaluationFeedbackCreateRequestFeedback]):  Default:
            EvaluationFeedbackCreateRequestFeedback.POSITIVE.
        comments (Union[None, Unset, str]):
    """

    entity_id: str
    entity_type: str
    evaluation_id: Union[None, Unset, str] = UNSET
    feedback: Union[Unset, EvaluationFeedbackCreateRequestFeedback] = EvaluationFeedbackCreateRequestFeedback.POSITIVE
    comments: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity_id = self.entity_id

        entity_type = self.entity_type

        evaluation_id: Union[None, Unset, str]
        if isinstance(self.evaluation_id, Unset):
            evaluation_id = UNSET
        else:
            evaluation_id = self.evaluation_id

        feedback: Union[Unset, str] = UNSET
        if not isinstance(self.feedback, Unset):
            feedback = self.feedback.value

        comments: Union[None, Unset, str]
        if isinstance(self.comments, Unset):
            comments = UNSET
        else:
            comments = self.comments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
            }
        )
        if evaluation_id is not UNSET:
            field_dict["evaluation_id"] = evaluation_id
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entity_id")

        entity_type = d.pop("entity_type")

        def _parse_evaluation_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        evaluation_id = _parse_evaluation_id(d.pop("evaluation_id", UNSET))

        _feedback = d.pop("feedback", UNSET)
        feedback: Union[Unset, EvaluationFeedbackCreateRequestFeedback]
        if isinstance(_feedback, Unset):
            feedback = UNSET
        else:
            feedback = EvaluationFeedbackCreateRequestFeedback(_feedback)

        def _parse_comments(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comments = _parse_comments(d.pop("comments", UNSET))

        evaluation_feedback_create_request = cls(
            entity_id=entity_id,
            entity_type=entity_type,
            evaluation_id=evaluation_id,
            feedback=feedback,
            comments=comments,
        )

        evaluation_feedback_create_request.additional_properties = d
        return evaluation_feedback_create_request

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
