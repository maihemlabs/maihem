from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminTestResultMetricReviewEditRequest")


@_attrs_define
class AdminTestResultMetricReviewEditRequest:
    """
    Attributes:
        result (str):
        entity_id (str):
        entity_type (str):
        test_result_metric_id (Union[None, Unset, str]):
        score (Union[None, Unset, int]):
        explanation (Union[None, Unset, str]):
    """

    result: str
    entity_id: str
    entity_type: str
    test_result_metric_id: Union[None, Unset, str] = UNSET
    score: Union[None, Unset, int] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = self.result

        entity_id = self.entity_id

        entity_type = self.entity_type

        test_result_metric_id: Union[None, Unset, str]
        if isinstance(self.test_result_metric_id, Unset):
            test_result_metric_id = UNSET
        else:
            test_result_metric_id = self.test_result_metric_id

        score: Union[None, Unset, int]
        if isinstance(self.score, Unset):
            score = UNSET
        else:
            score = self.score

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "entity_id": entity_id,
                "entity_type": entity_type,
            }
        )
        if test_result_metric_id is not UNSET:
            field_dict["test_result_metric_id"] = test_result_metric_id
        if score is not UNSET:
            field_dict["score"] = score
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        result = d.pop("result")

        entity_id = d.pop("entity_id")

        entity_type = d.pop("entity_type")

        def _parse_test_result_metric_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_result_metric_id = _parse_test_result_metric_id(d.pop("test_result_metric_id", UNSET))

        def _parse_score(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        score = _parse_score(d.pop("score", UNSET))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        admin_test_result_metric_review_edit_request = cls(
            result=result,
            entity_id=entity_id,
            entity_type=entity_type,
            test_result_metric_id=test_result_metric_id,
            score=score,
            explanation=explanation,
        )

        admin_test_result_metric_review_edit_request.additional_properties = d
        return admin_test_result_metric_review_edit_request

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
