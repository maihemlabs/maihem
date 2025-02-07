from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminEvaluationReviewEditRequest")


@_attrs_define
class AdminEvaluationReviewEditRequest:
    """
    Attributes:
        result (str):
        entity_id (str):
        entity_type (str):
        evaluation_id (Union[None, Unset, str]):
        score (Union[None, Unset, int]):
        explanation (Union[None, Unset, str]):
    """

    result: str
    entity_id: str
    entity_type: str
    evaluation_id: Union[None, Unset, str] = UNSET
    score: Union[None, Unset, int] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = self.result

        entity_id = self.entity_id

        entity_type = self.entity_type

        evaluation_id: Union[None, Unset, str]
        if isinstance(self.evaluation_id, Unset):
            evaluation_id = UNSET
        else:
            evaluation_id = self.evaluation_id

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "entity_id": entity_id,
                "entity_type": entity_type,
            }
        )
        if evaluation_id is not UNSET:
            field_dict["evaluation_id"] = evaluation_id
        if score is not UNSET:
            field_dict["score"] = score
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        result = d.pop("result")

        entity_id = d.pop("entity_id")

        entity_type = d.pop("entity_type")

        def _parse_evaluation_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        evaluation_id = _parse_evaluation_id(d.pop("evaluation_id", UNSET))

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

        admin_evaluation_review_edit_request = cls(
            result=result,
            entity_id=entity_id,
            entity_type=entity_type,
            evaluation_id=evaluation_id,
            score=score,
            explanation=explanation,
        )

        admin_evaluation_review_edit_request.additional_properties = d
        return admin_evaluation_review_edit_request

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
