from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_enum import TestResultEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_token_cost import ConversationNestedTokenCost


T = TypeVar("T", bound="ConversationNestedEvaluation")


@_attrs_define
class ConversationNestedEvaluation:
    """
    Attributes:
        id (str):
        result (TestResultEnum):
        metric_slug (str):
        score (Union[None, Unset, float]):
        confidence (Union[None, Unset, float]):
        explanation (Union[None, Unset, str]):
        classification (Union[None, Unset, str]):
        token_cost (Union['ConversationNestedTokenCost', None, Unset]):
    """

    id: str
    result: TestResultEnum
    metric_slug: str
    score: Union[None, Unset, float] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    classification: Union[None, Unset, str] = UNSET
    token_cost: Union["ConversationNestedTokenCost", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.conversation_nested_token_cost import ConversationNestedTokenCost

        id = self.id

        result = self.result.value

        metric_slug = self.metric_slug

        score: Union[None, Unset, float]
        if isinstance(self.score, Unset):
            score = UNSET
        else:
            score = self.score

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        classification: Union[None, Unset, str]
        if isinstance(self.classification, Unset):
            classification = UNSET
        else:
            classification = self.classification

        token_cost: Union[Dict[str, Any], None, Unset]
        if isinstance(self.token_cost, Unset):
            token_cost = UNSET
        elif isinstance(self.token_cost, ConversationNestedTokenCost):
            token_cost = self.token_cost.to_dict()
        else:
            token_cost = self.token_cost

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "result": result,
                "metric_slug": metric_slug,
            }
        )
        if score is not UNSET:
            field_dict["score"] = score
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if classification is not UNSET:
            field_dict["classification"] = classification
        if token_cost is not UNSET:
            field_dict["token_cost"] = token_cost

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_token_cost import ConversationNestedTokenCost

        d = src_dict.copy()
        id = d.pop("id")

        result = TestResultEnum(d.pop("result"))

        metric_slug = d.pop("metric_slug")

        def _parse_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        score = _parse_score(d.pop("score", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        def _parse_classification(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        classification = _parse_classification(d.pop("classification", UNSET))

        def _parse_token_cost(data: object) -> Union["ConversationNestedTokenCost", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                token_cost_type_0 = ConversationNestedTokenCost.from_dict(data)

                return token_cost_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ConversationNestedTokenCost", None, Unset], data)

        token_cost = _parse_token_cost(d.pop("token_cost", UNSET))

        conversation_nested_evaluation = cls(
            id=id,
            result=result,
            metric_slug=metric_slug,
            score=score,
            confidence=confidence,
            explanation=explanation,
            classification=classification,
            token_cost=token_cost,
        )

        conversation_nested_evaluation.additional_properties = d
        return conversation_nested_evaluation

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
