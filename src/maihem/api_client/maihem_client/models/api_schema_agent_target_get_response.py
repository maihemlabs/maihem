import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaAgentTargetGetResponse")


@_attrs_define
class APISchemaAgentTargetGetResponse:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        identifer (str):
        role (str):
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        industry (Union[None, Unset, str]):
        behaviour_prompt (Union[None, Unset, str]):
        language (Union[None, Unset, str]):  Default: 'en'.
        url (Union[None, Unset, str]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    identifer: str
    role: str
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    industry: Union[None, Unset, str] = UNSET
    behaviour_prompt: Union[None, Unset, str] = UNSET
    language: Union[None, Unset, str] = "en"
    url: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        identifer = self.identifer

        role = self.role

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        industry: Union[None, Unset, str]
        if isinstance(self.industry, Unset):
            industry = UNSET
        else:
            industry = self.industry

        behaviour_prompt: Union[None, Unset, str]
        if isinstance(self.behaviour_prompt, Unset):
            behaviour_prompt = UNSET
        else:
            behaviour_prompt = self.behaviour_prompt

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
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "identifer": identifer,
                "role": role,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if industry is not UNSET:
            field_dict["industry"] = industry
        if behaviour_prompt is not UNSET:
            field_dict["behaviour_prompt"] = behaviour_prompt
        if language is not UNSET:
            field_dict["language"] = language
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        identifer = d.pop("identifer")

        role = d.pop("role")

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_industry(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        industry = _parse_industry(d.pop("industry", UNSET))

        def _parse_behaviour_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        behaviour_prompt = _parse_behaviour_prompt(d.pop("behaviour_prompt", UNSET))

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

        api_schema_agent_target_get_response = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            identifer=identifer,
            role=role,
            name=name,
            description=description,
            industry=industry,
            behaviour_prompt=behaviour_prompt,
            language=language,
            url=url,
        )

        api_schema_agent_target_get_response.additional_properties = d
        return api_schema_agent_target_get_response

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
