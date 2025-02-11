import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_result_metric_feedback_feedback import TestResultMetricFeedbackFeedback
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestResultMetricFeedback")


@_attrs_define
class TestResultMetricFeedback:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        entity_id (str):
        entity_type (str):
        created_by (str):
        feedback (TestResultMetricFeedbackFeedback):
        test_result_metric_id (Union[None, Unset, str]):
        comments (Union[None, Unset, str]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    entity_id: str
    entity_type: str
    created_by: str
    feedback: TestResultMetricFeedbackFeedback
    test_result_metric_id: Union[None, Unset, str] = UNSET
    comments: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        entity_id = self.entity_id

        entity_type = self.entity_type

        created_by = self.created_by

        feedback = self.feedback.value

        test_result_metric_id: Union[None, Unset, str]
        if isinstance(self.test_result_metric_id, Unset):
            test_result_metric_id = UNSET
        else:
            test_result_metric_id = self.test_result_metric_id

        comments: Union[None, Unset, str]
        if isinstance(self.comments, Unset):
            comments = UNSET
        else:
            comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "entity_id": entity_id,
                "entity_type": entity_type,
                "created_by": created_by,
                "feedback": feedback,
            }
        )
        if test_result_metric_id is not UNSET:
            field_dict["test_result_metric_id"] = test_result_metric_id
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        entity_id = d.pop("entity_id")

        entity_type = d.pop("entity_type")

        created_by = d.pop("created_by")

        feedback = TestResultMetricFeedbackFeedback(d.pop("feedback"))

        def _parse_test_result_metric_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_result_metric_id = _parse_test_result_metric_id(d.pop("test_result_metric_id", UNSET))

        def _parse_comments(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comments = _parse_comments(d.pop("comments", UNSET))

        test_result_metric_feedback = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            entity_id=entity_id,
            entity_type=entity_type,
            created_by=created_by,
            feedback=feedback,
            test_result_metric_id=test_result_metric_id,
            comments=comments,
        )

        test_result_metric_feedback.additional_properties = d
        return test_result_metric_feedback

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
