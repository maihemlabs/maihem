from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.environment import Environment
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTestRunRequest")


@_attrs_define
class CreateTestRunRequest:
    """
    Attributes:
        name (str):
        label (Union[None, Unset, str]):
        environment (Union[Environment, None, Unset]):
        agent_target_revision_id (Union[None, Unset, str]):
    """

    name: str
    label: Union[None, Unset, str] = UNSET
    environment: Union[Environment, None, Unset] = UNSET
    agent_target_revision_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        environment: Union[None, Unset, str]
        if isinstance(self.environment, Unset):
            environment = UNSET
        elif isinstance(self.environment, Environment):
            environment = self.environment.value
        else:
            environment = self.environment

        agent_target_revision_id: Union[None, Unset, str]
        if isinstance(self.agent_target_revision_id, Unset):
            agent_target_revision_id = UNSET
        else:
            agent_target_revision_id = self.agent_target_revision_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if environment is not UNSET:
            field_dict["environment"] = environment
        if agent_target_revision_id is not UNSET:
            field_dict["agent_target_revision_id"] = agent_target_revision_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_environment(data: object) -> Union[Environment, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_type_0 = Environment(data)

                return environment_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Environment, None, Unset], data)

        environment = _parse_environment(d.pop("environment", UNSET))

        def _parse_agent_target_revision_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_target_revision_id = _parse_agent_target_revision_id(d.pop("agent_target_revision_id", UNSET))

        create_test_run_request = cls(
            name=name,
            label=label,
            environment=environment,
            agent_target_revision_id=agent_target_revision_id,
        )

        create_test_run_request.additional_properties = d
        return create_test_run_request

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
