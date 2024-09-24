import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_result_enum import TestResultEnum
from ..models.test_status_enum import TestStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
    from ..models.conversation_nested_turn import ConversationNestedTurn


T = TypeVar("T", bound="ConversationNested")


@_attrs_define
class ConversationNested:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        status (TestStatusEnum):
        result (TestResultEnum):
        started_at (Union[None, Unset, datetime.datetime]):
        completed_at (Union[None, Unset, datetime.datetime]):
        evaluations (Union[Unset, List['ConversationNestedEvaluation']]):
        conversation_turns (Union[Unset, List['ConversationNestedTurn']]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: TestStatusEnum
    result: TestResultEnum
    started_at: Union[None, Unset, datetime.datetime] = UNSET
    completed_at: Union[None, Unset, datetime.datetime] = UNSET
    evaluations: Union[Unset, List["ConversationNestedEvaluation"]] = UNSET
    conversation_turns: Union[Unset, List["ConversationNestedTurn"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status = self.status.value

        result = self.result.value

        started_at: Union[None, Unset, str]
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: Union[None, Unset, str]
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        evaluations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.evaluations, Unset):
            evaluations = []
            for evaluations_item_data in self.evaluations:
                evaluations_item = evaluations_item_data.to_dict()
                evaluations.append(evaluations_item)

        conversation_turns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conversation_turns, Unset):
            conversation_turns = []
            for conversation_turns_item_data in self.conversation_turns:
                conversation_turns_item = conversation_turns_item_data.to_dict()
                conversation_turns.append(conversation_turns_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "status": status,
                "result": result,
            }
        )
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if evaluations is not UNSET:
            field_dict["evaluations"] = evaluations
        if conversation_turns is not UNSET:
            field_dict["conversation_turns"] = conversation_turns

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_nested_evaluation import ConversationNestedEvaluation
        from ..models.conversation_nested_turn import ConversationNestedTurn

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        status = TestStatusEnum(d.pop("status"))

        result = TestResultEnum(d.pop("result"))

        def _parse_started_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))

        def _parse_completed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        evaluations = []
        _evaluations = d.pop("evaluations", UNSET)
        for evaluations_item_data in _evaluations or []:
            evaluations_item = ConversationNestedEvaluation.from_dict(evaluations_item_data)

            evaluations.append(evaluations_item)

        conversation_turns = []
        _conversation_turns = d.pop("conversation_turns", UNSET)
        for conversation_turns_item_data in _conversation_turns or []:
            conversation_turns_item = ConversationNestedTurn.from_dict(conversation_turns_item_data)

            conversation_turns.append(conversation_turns_item)

        conversation_nested = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            result=result,
            started_at=started_at,
            completed_at=completed_at,
            evaluations=evaluations,
            conversation_turns=conversation_turns,
        )

        conversation_nested.additional_properties = d
        return conversation_nested

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
