from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_type import AgentType
from ..models.test_create_request_entity_type import TestCreateRequestEntityType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_create_request_documents_type_0 import TestCreateRequestDocumentsType0
    from ..models.test_create_request_metrics_config_type_0 import TestCreateRequestMetricsConfigType0


T = TypeVar("T", bound="TestCreateRequest")


@_attrs_define
class TestCreateRequest:
    """
    Attributes:
        name (str):
        agent_target_id (str):
        entity_id (str):
        label (Union[None, Unset, str]):
        initiating_agent (Union[Unset, AgentType]):
        conversation_turns_max (Union[None, Unset, int]):
        agent_maihem_behavior_prompt (Union[None, Unset, str]):
        agent_maihem_goal_prompt (Union[None, Unset, str]):
        agent_maihem_population_prompt (Union[None, Unset, str]):
        metrics_config (Union['TestCreateRequestMetricsConfigType0', None, Unset]):
        dataset_id (Union[None, Unset, str]):
        documents (Union['TestCreateRequestDocumentsType0', None, Unset]):
        is_dev_mode (Union[None, Unset, bool]):  Default: False.
        entity_type (Union[Unset, TestCreateRequestEntityType]):  Default: TestCreateRequestEntityType.WORKFLOW.
    """

    name: str
    agent_target_id: str
    entity_id: str
    label: Union[None, Unset, str] = UNSET
    initiating_agent: Union[Unset, AgentType] = UNSET
    conversation_turns_max: Union[None, Unset, int] = UNSET
    agent_maihem_behavior_prompt: Union[None, Unset, str] = UNSET
    agent_maihem_goal_prompt: Union[None, Unset, str] = UNSET
    agent_maihem_population_prompt: Union[None, Unset, str] = UNSET
    metrics_config: Union["TestCreateRequestMetricsConfigType0", None, Unset] = UNSET
    dataset_id: Union[None, Unset, str] = UNSET
    documents: Union["TestCreateRequestDocumentsType0", None, Unset] = UNSET
    is_dev_mode: Union[None, Unset, bool] = False
    entity_type: Union[Unset, TestCreateRequestEntityType] = TestCreateRequestEntityType.WORKFLOW
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_create_request_documents_type_0 import TestCreateRequestDocumentsType0
        from ..models.test_create_request_metrics_config_type_0 import TestCreateRequestMetricsConfigType0

        name = self.name

        agent_target_id = self.agent_target_id

        entity_id = self.entity_id

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

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

        agent_maihem_goal_prompt: Union[None, Unset, str]
        if isinstance(self.agent_maihem_goal_prompt, Unset):
            agent_maihem_goal_prompt = UNSET
        else:
            agent_maihem_goal_prompt = self.agent_maihem_goal_prompt

        agent_maihem_population_prompt: Union[None, Unset, str]
        if isinstance(self.agent_maihem_population_prompt, Unset):
            agent_maihem_population_prompt = UNSET
        else:
            agent_maihem_population_prompt = self.agent_maihem_population_prompt

        metrics_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metrics_config, Unset):
            metrics_config = UNSET
        elif isinstance(self.metrics_config, TestCreateRequestMetricsConfigType0):
            metrics_config = self.metrics_config.to_dict()
        else:
            metrics_config = self.metrics_config

        dataset_id: Union[None, Unset, str]
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        documents: Union[None, Unset, dict[str, Any]]
        if isinstance(self.documents, Unset):
            documents = UNSET
        elif isinstance(self.documents, TestCreateRequestDocumentsType0):
            documents = self.documents.to_dict()
        else:
            documents = self.documents

        is_dev_mode: Union[None, Unset, bool]
        if isinstance(self.is_dev_mode, Unset):
            is_dev_mode = UNSET
        else:
            is_dev_mode = self.is_dev_mode

        entity_type: Union[Unset, str] = UNSET
        if not isinstance(self.entity_type, Unset):
            entity_type = self.entity_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "agent_target_id": agent_target_id,
                "entity_id": entity_id,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if initiating_agent is not UNSET:
            field_dict["initiating_agent"] = initiating_agent
        if conversation_turns_max is not UNSET:
            field_dict["conversation_turns_max"] = conversation_turns_max
        if agent_maihem_behavior_prompt is not UNSET:
            field_dict["agent_maihem_behavior_prompt"] = agent_maihem_behavior_prompt
        if agent_maihem_goal_prompt is not UNSET:
            field_dict["agent_maihem_goal_prompt"] = agent_maihem_goal_prompt
        if agent_maihem_population_prompt is not UNSET:
            field_dict["agent_maihem_population_prompt"] = agent_maihem_population_prompt
        if metrics_config is not UNSET:
            field_dict["metrics_config"] = metrics_config
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if documents is not UNSET:
            field_dict["documents"] = documents
        if is_dev_mode is not UNSET:
            field_dict["is_dev_mode"] = is_dev_mode
        if entity_type is not UNSET:
            field_dict["entity_type"] = entity_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.test_create_request_documents_type_0 import TestCreateRequestDocumentsType0
        from ..models.test_create_request_metrics_config_type_0 import TestCreateRequestMetricsConfigType0

        d = src_dict.copy()
        name = d.pop("name")

        agent_target_id = d.pop("agent_target_id")

        entity_id = d.pop("entity_id")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

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

        def _parse_agent_maihem_goal_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_maihem_goal_prompt = _parse_agent_maihem_goal_prompt(d.pop("agent_maihem_goal_prompt", UNSET))

        def _parse_agent_maihem_population_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_maihem_population_prompt = _parse_agent_maihem_population_prompt(
            d.pop("agent_maihem_population_prompt", UNSET)
        )

        def _parse_metrics_config(data: object) -> Union["TestCreateRequestMetricsConfigType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metrics_config_type_0 = TestCreateRequestMetricsConfigType0.from_dict(data)

                return metrics_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestCreateRequestMetricsConfigType0", None, Unset], data)

        metrics_config = _parse_metrics_config(d.pop("metrics_config", UNSET))

        def _parse_dataset_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_documents(data: object) -> Union["TestCreateRequestDocumentsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                documents_type_0 = TestCreateRequestDocumentsType0.from_dict(data)

                return documents_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestCreateRequestDocumentsType0", None, Unset], data)

        documents = _parse_documents(d.pop("documents", UNSET))

        def _parse_is_dev_mode(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_dev_mode = _parse_is_dev_mode(d.pop("is_dev_mode", UNSET))

        _entity_type = d.pop("entity_type", UNSET)
        entity_type: Union[Unset, TestCreateRequestEntityType]
        if isinstance(_entity_type, Unset):
            entity_type = UNSET
        else:
            entity_type = TestCreateRequestEntityType(_entity_type)

        test_create_request = cls(
            name=name,
            agent_target_id=agent_target_id,
            entity_id=entity_id,
            label=label,
            initiating_agent=initiating_agent,
            conversation_turns_max=conversation_turns_max,
            agent_maihem_behavior_prompt=agent_maihem_behavior_prompt,
            agent_maihem_goal_prompt=agent_maihem_goal_prompt,
            agent_maihem_population_prompt=agent_maihem_population_prompt,
            metrics_config=metrics_config,
            dataset_id=dataset_id,
            documents=documents,
            is_dev_mode=is_dev_mode,
            entity_type=entity_type,
        )

        test_create_request.additional_properties = d
        return test_create_request

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
