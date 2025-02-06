import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="VWorkflow")


@_attrs_define
class VWorkflow:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str):
        label (Union[None, str]):
        org_id (str):
        agent_target_id (str):
        workflow_steps (Any):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    label: Union[None, str]
    org_id: str
    agent_target_id: str
    workflow_steps: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        label: Union[None, str]
        label = self.label

        org_id = self.org_id

        agent_target_id = self.agent_target_id

        workflow_steps = self.workflow_steps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "name": name,
                "label": label,
                "org_id": org_id,
                "agent_target_id": agent_target_id,
                "workflow_steps": workflow_steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        label = _parse_label(d.pop("label"))

        org_id = d.pop("org_id")

        agent_target_id = d.pop("agent_target_id")

        workflow_steps = d.pop("workflow_steps")

        v_workflow = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            label=label,
            org_id=org_id,
            agent_target_id=agent_target_id,
            workflow_steps=workflow_steps,
        )

        v_workflow.additional_properties = d
        return v_workflow

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
