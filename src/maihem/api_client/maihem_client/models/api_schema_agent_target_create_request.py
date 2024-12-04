from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaAgentTargetCreateRequest")


@_attrs_define
class APISchemaAgentTargetCreateRequest:
    """
    Attributes:
        name (str):
        description (str):
        label (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        industry (Union[None, Unset, str]):
        language (Union[None, Unset, str]):  Default: 'en'.
        url (Union[None, Unset, str]):
    """

    name: str
    description: str
    label: Union[None, Unset, str] = UNSET
    role: Union[None, Unset, str] = UNSET
    industry: Union[None, Unset, str] = UNSET
    language: Union[None, Unset, str] = "en"
    url: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description

        label: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            label = UNSET
        else:
            label = self.label

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        industry: Union[None, Unset, str]
        if isinstance(self.industry, Unset):
            industry = UNSET
        else:
            industry = self.industry

        language: Union[None, Unset, str]
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if role is not UNSET:
            field_dict["role"] = role
        if industry is not UNSET:
            field_dict["industry"] = industry
        if language is not UNSET:
            field_dict["language"] = language
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")
        description = d.pop("description")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_industry(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        industry = _parse_industry(d.pop("industry", UNSET))

        def _parse_language(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        api_schema_agent_target_create_request = cls(
            name=name,
            description=description,
            label=label,
            role=role,
            industry=industry,
            language=language,
            url=url,
        )

        api_schema_agent_target_create_request.additional_properties = d
        return api_schema_agent_target_create_request

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
