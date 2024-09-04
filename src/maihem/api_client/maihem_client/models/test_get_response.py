import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type import AgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_metric_with_conversation_count import TestMetricWithConversationCount


T = TypeVar("T", bound="TestGetResponse")


@_attrs_define
class TestGetResponse:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        identifier (str):
        agent_target_id (str):
        initiating_agent (AgentType):
        name (Union[None, Unset, str]):
        metrics (Union[Unset, List['TestMetricWithConversationCount']]):
        last_run_at (Union[None, Unset, datetime.datetime]):
        last_run_id (Union[None, Unset, str]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    identifier: str
    agent_target_id: str
    initiating_agent: AgentType
    name: Union[None, Unset, str] = UNSET
    metrics: Union[Unset, List["TestMetricWithConversationCount"]] = UNSET
    last_run_at: Union[None, Unset, datetime.datetime] = UNSET
    last_run_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        identifier = self.identifier

        agent_target_id = self.agent_target_id

        initiating_agent = self.initiating_agent.value

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        metrics: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = []
            for metrics_item_data in self.metrics:
                metrics_item = metrics_item_data.to_dict()
                metrics.append(metrics_item)

        last_run_at: Union[None, Unset, str]
        if isinstance(self.last_run_at, Unset):
            last_run_at = UNSET
        elif isinstance(self.last_run_at, datetime.datetime):
            last_run_at = self.last_run_at.isoformat()
        else:
            last_run_at = self.last_run_at

        last_run_id: Union[None, Unset, str]
        if isinstance(self.last_run_id, Unset):
            last_run_id = UNSET
        else:
            last_run_id = self.last_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "identifier": identifier,
                "agent_target_id": agent_target_id,
                "initiating_agent": initiating_agent,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if last_run_at is not UNSET:
            field_dict["last_run_at"] = last_run_at
        if last_run_id is not UNSET:
            field_dict["last_run_id"] = last_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_metric_with_conversation_count import TestMetricWithConversationCount

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        identifier = d.pop("identifier")

        agent_target_id = d.pop("agent_target_id")

        initiating_agent = AgentType(d.pop("initiating_agent"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        metrics = []
        _metrics = d.pop("metrics", UNSET)
        for metrics_item_data in _metrics or []:
            metrics_item = TestMetricWithConversationCount.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        def _parse_last_run_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_run_at_type_0 = isoparse(data)

                return last_run_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_run_at = _parse_last_run_at(d.pop("last_run_at", UNSET))

        def _parse_last_run_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_run_id = _parse_last_run_id(d.pop("last_run_id", UNSET))

        test_get_response = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            identifier=identifier,
            agent_target_id=agent_target_id,
            initiating_agent=initiating_agent,
            name=name,
            metrics=metrics,
            last_run_at=last_run_at,
            last_run_id=last_run_id,
        )

        test_get_response.additional_properties = d
        return test_get_response

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
