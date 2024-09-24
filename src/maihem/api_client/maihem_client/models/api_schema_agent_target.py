import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_result_enum import TestResultEnum
from ..models.test_status_enum import TestStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="APISchemaAgentTarget")


@_attrs_define
class APISchemaAgentTarget:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        identifier (str):
        role (str):
        language (str):
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        industry (Union[None, Unset, str]):
        url (Union[None, Unset, str]):
        last_test_run_id (Union[None, Unset, str]):
        last_test_run_at (Union[None, Unset, datetime.datetime]):
        last_test_run_status (Union[None, TestStatusEnum, Unset]):
        last_test_run_result (Union[None, TestResultEnum, Unset]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    identifier: str
    role: str
    language: str
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    industry: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    last_test_run_id: Union[None, Unset, str] = UNSET
    last_test_run_at: Union[None, Unset, datetime.datetime] = UNSET
    last_test_run_status: Union[None, TestStatusEnum, Unset] = UNSET
    last_test_run_result: Union[None, TestResultEnum, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        identifier = self.identifier

        role = self.role

        language = self.language

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

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        last_test_run_id: Union[None, Unset, str]
        if isinstance(self.last_test_run_id, Unset):
            last_test_run_id = UNSET
        else:
            last_test_run_id = self.last_test_run_id

        last_test_run_at: Union[None, Unset, str]
        if isinstance(self.last_test_run_at, Unset):
            last_test_run_at = UNSET
        elif isinstance(self.last_test_run_at, datetime.datetime):
            last_test_run_at = self.last_test_run_at.isoformat()
        else:
            last_test_run_at = self.last_test_run_at

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "identifier": identifier,
                "role": role,
                "language": language,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if industry is not UNSET:
            field_dict["industry"] = industry
        if url is not UNSET:
            field_dict["url"] = url
        if last_test_run_id is not UNSET:
            field_dict["last_test_run_id"] = last_test_run_id
        if last_test_run_at is not UNSET:
            field_dict["last_test_run_at"] = last_test_run_at
        if last_test_run_status is not UNSET:
            field_dict["last_test_run_status"] = last_test_run_status
        if last_test_run_result is not UNSET:
            field_dict["last_test_run_result"] = last_test_run_result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        identifier = d.pop("identifier")

        role = d.pop("role")

        language = d.pop("language")

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

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_last_test_run_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_test_run_id = _parse_last_test_run_id(d.pop("last_test_run_id", UNSET))

        def _parse_last_test_run_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_test_run_at_type_0 = isoparse(data)

                return last_test_run_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_test_run_at = _parse_last_test_run_at(d.pop("last_test_run_at", UNSET))

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

        api_schema_agent_target = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            identifier=identifier,
            role=role,
            language=language,
            name=name,
            description=description,
            industry=industry,
            url=url,
            last_test_run_id=last_test_run_id,
            last_test_run_at=last_test_run_at,
            last_test_run_status=last_test_run_status,
            last_test_run_result=last_test_run_result,
        )

        api_schema_agent_target.additional_properties = d
        return api_schema_agent_target

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
