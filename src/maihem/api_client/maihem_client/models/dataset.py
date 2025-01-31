import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Dataset")


@_attrs_define
class Dataset:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        org_id (str):
        name (str):
        label (Union[None, str]):
        description (Union[None, str]):
        source_type (str):
        source_reference (Union[None, str]):
        dataset_target (str):
        workflow_step_id (Union[None, str]):
        external_id (Union[None, str]):
        is_deleted (bool):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    org_id: str
    name: str
    label: Union[None, str]
    description: Union[None, str]
    source_type: str
    source_reference: Union[None, str]
    dataset_target: str
    workflow_step_id: Union[None, str]
    external_id: Union[None, str]
    is_deleted: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        org_id = self.org_id

        name = self.name

        label: Union[None, str]
        label = self.label

        description: Union[None, str]
        description = self.description

        source_type = self.source_type

        source_reference: Union[None, str]
        source_reference = self.source_reference

        dataset_target = self.dataset_target

        workflow_step_id: Union[None, str]
        workflow_step_id = self.workflow_step_id

        external_id: Union[None, str]
        external_id = self.external_id

        is_deleted = self.is_deleted

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "org_id": org_id,
                "name": name,
                "label": label,
                "description": description,
                "source_type": source_type,
                "source_reference": source_reference,
                "dataset_target": dataset_target,
                "workflow_step_id": workflow_step_id,
                "external_id": external_id,
                "is_deleted": is_deleted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        org_id = d.pop("org_id")

        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        label = _parse_label(d.pop("label"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        source_type = d.pop("source_type")

        def _parse_source_reference(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_reference = _parse_source_reference(d.pop("source_reference"))

        dataset_target = d.pop("dataset_target")

        def _parse_workflow_step_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        workflow_step_id = _parse_workflow_step_id(d.pop("workflow_step_id"))

        def _parse_external_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        external_id = _parse_external_id(d.pop("external_id"))

        is_deleted = d.pop("is_deleted")

        dataset = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            org_id=org_id,
            name=name,
            label=label,
            description=description,
            source_type=source_type,
            source_reference=source_reference,
            dataset_target=dataset_target,
            workflow_step_id=workflow_step_id,
            external_id=external_id,
            is_deleted=is_deleted,
        )

        dataset.additional_properties = d
        return dataset

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
