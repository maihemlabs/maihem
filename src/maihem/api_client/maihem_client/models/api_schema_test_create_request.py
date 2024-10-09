from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_type import AgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_schema_test_create_request_metrics_config import APISchemaTestCreateRequestMetricsConfig


T = TypeVar("T", bound="APISchemaTestCreateRequest")


@_attrs_define
class APISchemaTestCreateRequest:
    """
    Attributes:
        identifier (str):
        agent_target_id (str):
        metrics_config (APISchemaTestCreateRequestMetricsConfig):
        name (Union[None, Unset, str]):
        initiating_agent (Union[Unset, AgentType]):  Default: AgentType.MAIHEM.
        conversation_turns_max (Union[None, Unset, int]):
        agent_maihem_behavior_prompt (Union[None, Unset, str]):
        is_dev_mode (Union[None, Unset, bool]):  Default: False.
    """

    identifier: str
    agent_target_id: str
    metrics_config: "APISchemaTestCreateRequestMetricsConfig"
    name: Union[None, Unset, str] = UNSET
    initiating_agent: Union[Unset, AgentType] = AgentType.MAIHEM
    conversation_turns_max: Union[None, Unset, int] = UNSET
    agent_maihem_behavior_prompt: Union[None, Unset, str] = UNSET
    is_dev_mode: Union[None, Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier

        agent_target_id = self.agent_target_id

        metrics_config = self.metrics_config.to_dict()

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        initiating_agent: Union[Unset, str] = UNSET
        if not isinstance(self.initiating_agent, Unset):
            initiating_agent = self.initiating_agent.value

        conversation_turns_max: Union[None, Unset, int]
        if isinstance(self.conversation_turns_max, Unset):
            conversation_turns_max = UNSET
        else:
            conversation_turns_max = self.conversation_turns_max

        agent_maihem_behavior_prompt: Union[None, Unset, str]
        if isinstance(self.agent_maihem_behavior_prompt, Unset):
            agent_maihem_behavior_prompt = UNSET
        else:
            agent_maihem_behavior_prompt = self.agent_maihem_behavior_prompt

        is_dev_mode: Union[None, Unset, bool]
        if isinstance(self.is_dev_mode, Unset):
            is_dev_mode = UNSET
        else:
            is_dev_mode = self.is_dev_mode

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identifier": identifier,
                "agent_target_id": agent_target_id,
                "metrics_config": metrics_config,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if initiating_agent is not UNSET:
            field_dict["initiating_agent"] = initiating_agent
        if conversation_turns_max is not UNSET:
            field_dict["conversation_turns_max"] = conversation_turns_max
        if agent_maihem_behavior_prompt is not UNSET:
            field_dict["agent_maihem_behavior_prompt"] = agent_maihem_behavior_prompt
        if is_dev_mode is not UNSET:
            field_dict["is_dev_mode"] = is_dev_mode

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_schema_test_create_request_metrics_config import APISchemaTestCreateRequestMetricsConfig

        d = src_dict.copy()
        identifier = d.pop("identifier")

        agent_target_id = d.pop("agent_target_id")

        metrics_config = APISchemaTestCreateRequestMetricsConfig.from_dict(d.pop("metrics_config"))

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

        def _parse_conversation_turns_max(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        conversation_turns_max = _parse_conversation_turns_max(d.pop("conversation_turns_max", UNSET))

        def _parse_agent_maihem_behavior_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_maihem_behavior_prompt = _parse_agent_maihem_behavior_prompt(d.pop("agent_maihem_behavior_prompt", UNSET))

        def _parse_is_dev_mode(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_dev_mode = _parse_is_dev_mode(d.pop("is_dev_mode", UNSET))

        api_schema_test_create_request = cls(
            identifier=identifier,
            agent_target_id=agent_target_id,
            metrics_config=metrics_config,
            name=name,
            initiating_agent=initiating_agent,
            conversation_turns_max=conversation_turns_max,
            agent_maihem_behavior_prompt=agent_maihem_behavior_prompt,
            is_dev_mode=is_dev_mode,
        )

        api_schema_test_create_request.additional_properties = d
        return api_schema_test_create_request

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
