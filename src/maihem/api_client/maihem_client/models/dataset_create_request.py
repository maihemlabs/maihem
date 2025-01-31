from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_create_request_dataset_target import DatasetCreateRequestDatasetTarget
from ..models.dataset_create_request_source_type import DatasetCreateRequestSourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCreateRequest")


@_attrs_define
class DatasetCreateRequest:
    """
    Attributes:
        name (str):
        label (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        source_type (Union[Unset, DatasetCreateRequestSourceType]):  Default: DatasetCreateRequestSourceType.FILE.
        source_reference (Union[None, Unset, str]):
        dataset_target (Union[Unset, DatasetCreateRequestDatasetTarget]):  Default:
            DatasetCreateRequestDatasetTarget.CONVERSATION.
        workflow_step_id (Union[None, Unset, str]):
        external_id (Union[None, Unset, str]):
    """

    name: str
    label: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    source_type: Union[Unset, DatasetCreateRequestSourceType] = DatasetCreateRequestSourceType.FILE
    source_reference: Union[None, Unset, str] = UNSET
    dataset_target: Union[Unset, DatasetCreateRequestDatasetTarget] = DatasetCreateRequestDatasetTarget.CONVERSATION
    workflow_step_id: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        source_type: Union[Unset, str] = UNSET
        if not isinstance(self.source_type, Unset):
            source_type = self.source_type.value

        source_reference: Union[None, Unset, str]
        if isinstance(self.source_reference, Unset):
            source_reference = UNSET
        else:
            source_reference = self.source_reference

        dataset_target: Union[Unset, str] = UNSET
        if not isinstance(self.dataset_target, Unset):
            dataset_target = self.dataset_target.value

        workflow_step_id: Union[None, Unset, str]
        if isinstance(self.workflow_step_id, Unset):
            workflow_step_id = UNSET
        else:
            workflow_step_id = self.workflow_step_id

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if description is not UNSET:
            field_dict["description"] = description
        if source_type is not UNSET:
            field_dict["source_type"] = source_type
        if source_reference is not UNSET:
            field_dict["source_reference"] = source_reference
        if dataset_target is not UNSET:
            field_dict["dataset_target"] = dataset_target
        if workflow_step_id is not UNSET:
            field_dict["workflow_step_id"] = workflow_step_id
        if external_id is not UNSET:
            field_dict["external_id"] = external_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _source_type = d.pop("source_type", UNSET)
        source_type: Union[Unset, DatasetCreateRequestSourceType]
        if isinstance(_source_type, Unset):
            source_type = UNSET
        else:
            source_type = DatasetCreateRequestSourceType(_source_type)

        def _parse_source_reference(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_reference = _parse_source_reference(d.pop("source_reference", UNSET))

        _dataset_target = d.pop("dataset_target", UNSET)
        dataset_target: Union[Unset, DatasetCreateRequestDatasetTarget]
        if isinstance(_dataset_target, Unset):
            dataset_target = UNSET
        else:
            dataset_target = DatasetCreateRequestDatasetTarget(_dataset_target)

        def _parse_workflow_step_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workflow_step_id = _parse_workflow_step_id(d.pop("workflow_step_id", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        dataset_create_request = cls(
            name=name,
            label=label,
            description=description,
            source_type=source_type,
            source_reference=source_reference,
            dataset_target=dataset_target,
            workflow_step_id=workflow_step_id,
            external_id=external_id,
        )

        dataset_create_request.additional_properties = d
        return dataset_create_request

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
