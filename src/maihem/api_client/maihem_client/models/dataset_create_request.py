from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_create_request_target_type import DatasetCreateRequestTargetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCreateRequest")


@_attrs_define
class DatasetCreateRequest:
    """
    Attributes:
        name (str):
        label (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        source_type (Union[Literal['file'], Unset]):  Default: 'file'.
        source_reference (Union[None, Unset, str]):
        target_type (Union[Unset, DatasetCreateRequestTargetType]):  Default: DatasetCreateRequestTargetType.WORKFLOW.
        target_id (Union[None, Unset, str]):
        external_id (Union[None, Unset, str]):
    """

    name: str
    label: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    source_type: Union[Literal["file"], Unset] = "file"
    source_reference: Union[None, Unset, str] = UNSET
    target_type: Union[Unset, DatasetCreateRequestTargetType] = DatasetCreateRequestTargetType.WORKFLOW
    target_id: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        source_type = self.source_type

        source_reference: Union[None, Unset, str]
        if isinstance(self.source_reference, Unset):
            source_reference = UNSET
        else:
            source_reference = self.source_reference

        target_type: Union[Unset, str] = UNSET
        if not isinstance(self.target_type, Unset):
            target_type = self.target_type.value

        target_id: Union[None, Unset, str]
        if isinstance(self.target_id, Unset):
            target_id = UNSET
        else:
            target_id = self.target_id

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        field_dict: dict[str, Any] = {}
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
        if target_type is not UNSET:
            field_dict["target_type"] = target_type
        if target_id is not UNSET:
            field_dict["target_id"] = target_id
        if external_id is not UNSET:
            field_dict["external_id"] = external_id

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

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        source_type = cast(Union[Literal["file"], Unset], d.pop("source_type", UNSET))
        if source_type != "file" and not isinstance(source_type, Unset):
            raise ValueError(f"source_type must match const 'file', got '{source_type}'")

        def _parse_source_reference(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_reference = _parse_source_reference(d.pop("source_reference", UNSET))

        _target_type = d.pop("target_type", UNSET)
        target_type: Union[Unset, DatasetCreateRequestTargetType]
        if isinstance(_target_type, Unset):
            target_type = UNSET
        else:
            target_type = DatasetCreateRequestTargetType(_target_type)

        def _parse_target_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        target_id = _parse_target_id(d.pop("target_id", UNSET))

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
            target_type=target_type,
            target_id=target_id,
            external_id=external_id,
        )

        dataset_create_request.additional_properties = d
        return dataset_create_request

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
