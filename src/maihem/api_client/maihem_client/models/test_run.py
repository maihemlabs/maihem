import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_result_enum import TestResultEnum
from ..models.test_status_enum import TestStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.links import Links


T = TypeVar("T", bound="TestRun")


@_attrs_define
class TestRun:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str):
        test_id (str):
        test_name (str):
        agent_target_id (str):
        agent_target_name (str):
        status (TestStatusEnum):
        label (Union[None, Unset, str]):
        test_label (Union[None, Unset, str]):
        agent_target_label (Union[None, Unset, str]):
        started_at (Union[None, Unset, datetime.datetime]):
        completed_at (Union[None, Unset, datetime.datetime]):
        result (Union[None, TestResultEnum, Unset]):
        result_score (Union[None, Unset, float]):
        result_score_change (Union[None, Unset, float]):
        links (Union['Links', None, Unset]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    test_id: str
    test_name: str
    agent_target_id: str
    agent_target_name: str
    status: TestStatusEnum
    label: Union[None, Unset, str] = UNSET
    test_label: Union[None, Unset, str] = UNSET
    agent_target_label: Union[None, Unset, str] = UNSET
    started_at: Union[None, Unset, datetime.datetime] = UNSET
    completed_at: Union[None, Unset, datetime.datetime] = UNSET
    result: Union[None, TestResultEnum, Unset] = UNSET
    result_score: Union[None, Unset, float] = UNSET
    result_score_change: Union[None, Unset, float] = UNSET
    links: Union["Links", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.links import Links

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        test_id = self.test_id

        test_name = self.test_name

        agent_target_id = self.agent_target_id

        agent_target_name = self.agent_target_name

        status = self.status.value

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        test_label: Union[None, Unset, str]
        if isinstance(self.test_label, Unset):
            test_label = UNSET
        else:
            test_label = self.test_label

        agent_target_label: Union[None, Unset, str]
        if isinstance(self.agent_target_label, Unset):
            agent_target_label = UNSET
        else:
            agent_target_label = self.agent_target_label

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

        result: Union[None, Unset, str]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, TestResultEnum):
            result = self.result.value
        else:
            result = self.result

        result_score: Union[None, Unset, float]
        if isinstance(self.result_score, Unset):
            result_score = UNSET
        else:
            result_score = self.result_score

        result_score_change: Union[None, Unset, float]
        if isinstance(self.result_score_change, Unset):
            result_score_change = UNSET
        else:
            result_score_change = self.result_score_change

        links: Union[Dict[str, Any], None, Unset]
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, Links):
            links = self.links.to_dict()
        else:
            links = self.links

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "name": name,
                "test_id": test_id,
                "test_name": test_name,
                "agent_target_id": agent_target_id,
                "agent_target_name": agent_target_name,
                "status": status,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if test_label is not UNSET:
            field_dict["test_label"] = test_label
        if agent_target_label is not UNSET:
            field_dict["agent_target_label"] = agent_target_label
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if result is not UNSET:
            field_dict["result"] = result
        if result_score is not UNSET:
            field_dict["result_score"] = result_score
        if result_score_change is not UNSET:
            field_dict["result_score_change"] = result_score_change
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.links import Links

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        name = d.pop("name")

        test_id = d.pop("test_id")

        test_name = d.pop("test_name")

        agent_target_id = d.pop("agent_target_id")

        agent_target_name = d.pop("agent_target_name")

        status = TestStatusEnum(d.pop("status"))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_test_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_label = _parse_test_label(d.pop("test_label", UNSET))

        def _parse_agent_target_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_target_label = _parse_agent_target_label(d.pop("agent_target_label", UNSET))

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

        def _parse_result(data: object) -> Union[None, TestResultEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_type_0 = TestResultEnum(data)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TestResultEnum, Unset], data)

        result = _parse_result(d.pop("result", UNSET))

        def _parse_result_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        result_score = _parse_result_score(d.pop("result_score", UNSET))

        def _parse_result_score_change(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        result_score_change = _parse_result_score_change(d.pop("result_score_change", UNSET))

        def _parse_links(data: object) -> Union["Links", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = Links.from_dict(data)

                return links_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Links", None, Unset], data)

        links = _parse_links(d.pop("links", UNSET))

        test_run = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            test_id=test_id,
            test_name=test_name,
            agent_target_id=agent_target_id,
            agent_target_name=agent_target_name,
            status=status,
            label=label,
            test_label=test_label,
            agent_target_label=agent_target_label,
            started_at=started_at,
            completed_at=completed_at,
            result=result,
            result_score=result_score,
            result_score_change=result_score_change,
            links=links,
        )

        test_run.additional_properties = d
        return test_run

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
