import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type import AgentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaTestCreateResponse")


@_attrs_define
class APISchemaTestCreateResponse:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        identifier (str):
        agent_target_id (str):
        metrics (List[str]):
        name (Union[None, Unset, str]):
        initiating_agent (Union[Unset, AgentType]):  Default: AgentType.MAIHEM.
        conversations_per_metric (Union[None, Unset, int]):  Default: 5.
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    identifier: str
    agent_target_id: str
    metrics: List[str]
    name: Union[None, Unset, str] = UNSET
    initiating_agent: Union[Unset, AgentType] = AgentType.MAIHEM
    conversations_per_metric: Union[None, Unset, int] = 5
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        identifier = self.identifier

        agent_target_id = self.agent_target_id

        metrics = self.metrics

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        initiating_agent: Union[Unset, str] = UNSET
        if not isinstance(self.initiating_agent, Unset):
            initiating_agent = self.initiating_agent.value

        conversations_per_metric: Union[None, Unset, int]
        if isinstance(self.conversations_per_metric, Unset):
            conversations_per_metric = UNSET
        else:
            conversations_per_metric = self.conversations_per_metric

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "identifier": identifier,
                "agent_target_id": agent_target_id,
                "metrics": metrics,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if initiating_agent is not UNSET:
            field_dict["initiating_agent"] = initiating_agent
        if conversations_per_metric is not UNSET:
            field_dict["conversations_per_metric"] = conversations_per_metric

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        identifier = d.pop("identifier")

        agent_target_id = d.pop("agent_target_id")

        metrics = cast(List[str], d.pop("metrics"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        _initiating_agent = d.pop("initiating_agent", UNSET)
        initiating_agent: Union[Unset, AgentType]
        if isinstance(_initiating_agent, Unset):
            initiating_agent = UNSET
        else:
            initiating_agent = AgentType(_initiating_agent)

        def _parse_conversations_per_metric(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        conversations_per_metric = _parse_conversations_per_metric(d.pop("conversations_per_metric", UNSET))

        api_schema_test_create_response = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            identifier=identifier,
            agent_target_id=agent_target_id,
            metrics=metrics,
            name=name,
            initiating_agent=initiating_agent,
            conversations_per_metric=conversations_per_metric,
        )

        api_schema_test_create_response.additional_properties = d
        return api_schema_test_create_response

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
