import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_result_enum import TestResultEnum
from ..models.test_status_enum import TestStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_schema_links import APISchemaLinks


T = TypeVar("T", bound="APISchemaTestRunConversations")


@_attrs_define
class APISchemaTestRunConversations:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        test_id (str):
        status (TestStatusEnum):
        result (TestResultEnum):
        started_at (Union[None, Unset, datetime.datetime]):
        completed_at (Union[None, Unset, datetime.datetime]):
        result_score (Union[None, Unset, float]):
        links (Union['APISchemaLinks', None, Unset]):
        conversation_ids (Union[Unset, List[str]]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    test_id: str
    status: TestStatusEnum
    result: TestResultEnum
    started_at: Union[None, Unset, datetime.datetime] = UNSET
    completed_at: Union[None, Unset, datetime.datetime] = UNSET
    result_score: Union[None, Unset, float] = UNSET
    links: Union["APISchemaLinks", None, Unset] = UNSET
    conversation_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.api_schema_links import APISchemaLinks

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        test_id = self.test_id

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

        result_score: Union[None, Unset, float]
        if isinstance(self.result_score, Unset):
            result_score = UNSET
        else:
            result_score = self.result_score

        links: Union[Dict[str, Any], None, Unset]
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, APISchemaLinks):
            links = self.links.to_dict()
        else:
            links = self.links

        conversation_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.conversation_ids, Unset):
            conversation_ids = self.conversation_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "test_id": test_id,
                "status": status,
                "result": result,
            }
        )
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if result_score is not UNSET:
            field_dict["result_score"] = result_score
        if links is not UNSET:
            field_dict["links"] = links
        if conversation_ids is not UNSET:
            field_dict["conversation_ids"] = conversation_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_schema_links import APISchemaLinks

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        test_id = d.pop("test_id")

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

        def _parse_result_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        result_score = _parse_result_score(d.pop("result_score", UNSET))

        def _parse_links(data: object) -> Union["APISchemaLinks", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = APISchemaLinks.from_dict(data)

                return links_type_0
            except:  # noqa: E722
                pass
            return cast(Union["APISchemaLinks", None, Unset], data)

        links = _parse_links(d.pop("links", UNSET))

        conversation_ids = cast(List[str], d.pop("conversation_ids", UNSET))

        api_schema_test_run_conversations = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            test_id=test_id,
            status=status,
            result=result,
            started_at=started_at,
            completed_at=completed_at,
            result_score=result_score,
            links=links,
            conversation_ids=conversation_ids,
        )

        api_schema_test_run_conversations.additional_properties = d
        return api_schema_test_run_conversations

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
