import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type import AgentType
from ..models.test_result_enum import TestResultEnum
from ..models.test_status_enum import TestStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_documents_type_0 import TestDocumentsType0
    from ..models.test_metrics_config import TestMetricsConfig


T = TypeVar("T", bound="Test")


@_attrs_define
class Test:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str):
        initiating_agent (AgentType):
        agent_target_id (str):
        agent_target_name (str):
        metrics_config (TestMetricsConfig):
        label (Union[None, Unset, str]):
        agent_target_label (Union[None, Unset, str]):
        conversation_turns_max (Union[None, Unset, int]):
        agent_maihem_behavior_prompt (Union[None, Unset, str]):
        agent_maihem_goal_prompt (Union[None, Unset, str]):
        agent_maihem_population_prompt (Union[None, Unset, str]):
        documents (Union['TestDocumentsType0', None, Unset]):
        last_test_run_id (Union[None, Unset, str]):
        last_test_run_started_at (Union[None, Unset, datetime.datetime]):
        last_test_run_completed_at (Union[None, Unset, datetime.datetime]):
        last_test_run_status (Union[None, TestStatusEnum, Unset]):
        last_test_run_result (Union[None, TestResultEnum, Unset]):
        last_test_run_result_score (Union[None, Unset, float]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    initiating_agent: AgentType
    agent_target_id: str
    agent_target_name: str
    metrics_config: "TestMetricsConfig"
    label: Union[None, Unset, str] = UNSET
    agent_target_label: Union[None, Unset, str] = UNSET
    conversation_turns_max: Union[None, Unset, int] = UNSET
    agent_maihem_behavior_prompt: Union[None, Unset, str] = UNSET
    agent_maihem_goal_prompt: Union[None, Unset, str] = UNSET
    agent_maihem_population_prompt: Union[None, Unset, str] = UNSET
    documents: Union["TestDocumentsType0", None, Unset] = UNSET
    last_test_run_id: Union[None, Unset, str] = UNSET
    last_test_run_started_at: Union[None, Unset, datetime.datetime] = UNSET
    last_test_run_completed_at: Union[None, Unset, datetime.datetime] = UNSET
    last_test_run_status: Union[None, TestStatusEnum, Unset] = UNSET
    last_test_run_result: Union[None, TestResultEnum, Unset] = UNSET
    last_test_run_result_score: Union[None, Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.test_documents_type_0 import TestDocumentsType0

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        initiating_agent = self.initiating_agent.value

        agent_target_id = self.agent_target_id

        agent_target_name = self.agent_target_name

        metrics_config = self.metrics_config.to_dict()

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        agent_target_label: Union[None, Unset, str]
        if isinstance(self.agent_target_label, Unset):
            agent_target_label = UNSET
        else:
            agent_target_label = self.agent_target_label

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

        documents: Union[Dict[str, Any], None, Unset]
        if isinstance(self.documents, Unset):
            documents = UNSET
        elif isinstance(self.documents, TestDocumentsType0):
            documents = self.documents.to_dict()
        else:
            documents = self.documents

        last_test_run_id: Union[None, Unset, str]
        if isinstance(self.last_test_run_id, Unset):
            last_test_run_id = UNSET
        else:
            last_test_run_id = self.last_test_run_id

        last_test_run_started_at: Union[None, Unset, str]
        if isinstance(self.last_test_run_started_at, Unset):
            last_test_run_started_at = UNSET
        elif isinstance(self.last_test_run_started_at, datetime.datetime):
            last_test_run_started_at = self.last_test_run_started_at.isoformat()
        else:
            last_test_run_started_at = self.last_test_run_started_at

        last_test_run_completed_at: Union[None, Unset, str]
        if isinstance(self.last_test_run_completed_at, Unset):
            last_test_run_completed_at = UNSET
        elif isinstance(self.last_test_run_completed_at, datetime.datetime):
            last_test_run_completed_at = self.last_test_run_completed_at.isoformat()
        else:
            last_test_run_completed_at = self.last_test_run_completed_at

        last_test_run_status: Union[None, Unset, str]
        if isinstance(self.last_test_run_status, Unset):
            last_test_run_status = UNSET
        elif isinstance(self.last_test_run_status, TestStatusEnum):
            last_test_run_status = self.last_test_run_status.value
        else:
            last_test_run_status = self.last_test_run_status

        last_test_run_result: Union[None, Unset, str]
        if isinstance(self.last_test_run_result, Unset):
            last_test_run_result = UNSET
        elif isinstance(self.last_test_run_result, TestResultEnum):
            last_test_run_result = self.last_test_run_result.value
        else:
            last_test_run_result = self.last_test_run_result

        last_test_run_result_score: Union[None, Unset, float]
        if isinstance(self.last_test_run_result_score, Unset):
            last_test_run_result_score = UNSET
        else:
            last_test_run_result_score = self.last_test_run_result_score

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "name": name,
                "initiating_agent": initiating_agent,
                "agent_target_id": agent_target_id,
                "agent_target_name": agent_target_name,
                "metrics_config": metrics_config,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if agent_target_label is not UNSET:
            field_dict["agent_target_label"] = agent_target_label
        if conversation_turns_max is not UNSET:
            field_dict["conversation_turns_max"] = conversation_turns_max
        if agent_maihem_behavior_prompt is not UNSET:
            field_dict["agent_maihem_behavior_prompt"] = agent_maihem_behavior_prompt
        if agent_maihem_goal_prompt is not UNSET:
            field_dict["agent_maihem_goal_prompt"] = agent_maihem_goal_prompt
        if agent_maihem_population_prompt is not UNSET:
            field_dict["agent_maihem_population_prompt"] = agent_maihem_population_prompt
        if documents is not UNSET:
            field_dict["documents"] = documents
        if last_test_run_id is not UNSET:
            field_dict["last_test_run_id"] = last_test_run_id
        if last_test_run_started_at is not UNSET:
            field_dict["last_test_run_started_at"] = last_test_run_started_at
        if last_test_run_completed_at is not UNSET:
            field_dict["last_test_run_completed_at"] = last_test_run_completed_at
        if last_test_run_status is not UNSET:
            field_dict["last_test_run_status"] = last_test_run_status
        if last_test_run_result is not UNSET:
            field_dict["last_test_run_result"] = last_test_run_result
        if last_test_run_result_score is not UNSET:
            field_dict["last_test_run_result_score"] = last_test_run_result_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_documents_type_0 import TestDocumentsType0
        from ..models.test_metrics_config import TestMetricsConfig

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        name = d.pop("name")

        initiating_agent = AgentType(d.pop("initiating_agent"))

        agent_target_id = d.pop("agent_target_id")

        agent_target_name = d.pop("agent_target_name")

        metrics_config = TestMetricsConfig.from_dict(d.pop("metrics_config"))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_agent_target_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_target_label = _parse_agent_target_label(d.pop("agent_target_label", UNSET))

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

        def _parse_documents(data: object) -> Union["TestDocumentsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                documents_type_0 = TestDocumentsType0.from_dict(data)

                return documents_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestDocumentsType0", None, Unset], data)

        documents = _parse_documents(d.pop("documents", UNSET))

        def _parse_last_test_run_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_test_run_id = _parse_last_test_run_id(d.pop("last_test_run_id", UNSET))

        def _parse_last_test_run_started_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_test_run_started_at_type_0 = isoparse(data)

                return last_test_run_started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_test_run_started_at = _parse_last_test_run_started_at(d.pop("last_test_run_started_at", UNSET))

        def _parse_last_test_run_completed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_test_run_completed_at_type_0 = isoparse(data)

                return last_test_run_completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_test_run_completed_at = _parse_last_test_run_completed_at(d.pop("last_test_run_completed_at", UNSET))

        def _parse_last_test_run_status(data: object) -> Union[None, TestStatusEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_test_run_status_type_0 = TestStatusEnum(data)

                return last_test_run_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TestStatusEnum, Unset], data)

        last_test_run_status = _parse_last_test_run_status(d.pop("last_test_run_status", UNSET))

        def _parse_last_test_run_result(data: object) -> Union[None, TestResultEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_test_run_result_type_0 = TestResultEnum(data)

                return last_test_run_result_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TestResultEnum, Unset], data)

        last_test_run_result = _parse_last_test_run_result(d.pop("last_test_run_result", UNSET))

        def _parse_last_test_run_result_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        last_test_run_result_score = _parse_last_test_run_result_score(d.pop("last_test_run_result_score", UNSET))

        test = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            initiating_agent=initiating_agent,
            agent_target_id=agent_target_id,
            agent_target_name=agent_target_name,
            metrics_config=metrics_config,
            label=label,
            agent_target_label=agent_target_label,
            conversation_turns_max=conversation_turns_max,
            agent_maihem_behavior_prompt=agent_maihem_behavior_prompt,
            agent_maihem_goal_prompt=agent_maihem_goal_prompt,
            agent_maihem_population_prompt=agent_maihem_population_prompt,
            documents=documents,
            last_test_run_id=last_test_run_id,
            last_test_run_started_at=last_test_run_started_at,
            last_test_run_completed_at=last_test_run_completed_at,
            last_test_run_status=last_test_run_status,
            last_test_run_result=last_test_run_result,
            last_test_run_result_score=last_test_run_result_score,
        )

        test.additional_properties = d
        return test

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
