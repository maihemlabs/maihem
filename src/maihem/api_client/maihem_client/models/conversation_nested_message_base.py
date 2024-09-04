from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_type import AgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_sentence_base import ConversationNestedSentenceBase
    from ..models.conversation_nested_test_result_metric_base import ConversationNestedTestResultMetricBase


T = TypeVar("T", bound="ConversationNestedMessageBase")


@_attrs_define
class ConversationNestedMessageBase:
    """
    Attributes:
        agent_type (AgentType):
        content (str):
        id (Union[None, Unset, str]):
        test_result_metrics (Union[Unset, List['ConversationNestedTestResultMetricBase']]):
        conversation_sentences (Union[Unset, List['ConversationNestedSentenceBase']]):
        end_code (Union[None, Unset, str]):
    """

    agent_type: AgentType
    content: str
    id: Union[None, Unset, str] = UNSET
    test_result_metrics: Union[Unset, List["ConversationNestedTestResultMetricBase"]] = UNSET
    conversation_sentences: Union[Unset, List["ConversationNestedSentenceBase"]] = UNSET
    end_code: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        agent_type = self.agent_type.value

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

        conversation_sentences: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conversation_sentences, Unset):
            conversation_sentences = []
            for conversation_sentences_item_data in self.conversation_sentences:
                conversation_sentences_item = conversation_sentences_item_data.to_dict()
                conversation_sentences.append(conversation_sentences_item)

        end_code: Union[None, Unset, str]
        if isinstance(self.end_code, Unset):
            end_code = UNSET
        else:
            end_code = self.end_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_type": agent_type,
                "content": content,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if test_result_metrics is not UNSET:
            field_dict["test_result_metrics"] = test_result_metrics
        if conversation_sentences is not UNSET:
            field_dict["conversation_sentences"] = conversation_sentences
        if end_code is not UNSET:
            field_dict["end_code"] = end_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_sentence_base import ConversationNestedSentenceBase
        from ..models.conversation_nested_test_result_metric_base import ConversationNestedTestResultMetricBase

        d = src_dict.copy()
        agent_type = AgentType(d.pop("agent_type"))

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

        conversation_sentences = []
        _conversation_sentences = d.pop("conversation_sentences", UNSET)
        for conversation_sentences_item_data in _conversation_sentences or []:
            conversation_sentences_item = ConversationNestedSentenceBase.from_dict(conversation_sentences_item_data)

            conversation_sentences.append(conversation_sentences_item)

        def _parse_end_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end_code = _parse_end_code(d.pop("end_code", UNSET))

        conversation_nested_message_base = cls(
            agent_type=agent_type,
            content=content,
            id=id,
            test_result_metrics=test_result_metrics,
            conversation_sentences=conversation_sentences,
            end_code=end_code,
        )

        conversation_nested_message_base.additional_properties = d
        return conversation_nested_message_base

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
