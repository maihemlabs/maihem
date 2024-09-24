from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IDPUserCreateRequest")


@_attrs_define
class IDPUserCreateRequest:
    """
    Attributes:
        email (str):
        email_confirmed (bool):
        event_type (str):
        first_name (str):
        last_name (str):
        user_id (str):
        picture_url (Union[None, Unset, str]):
        username (Union[None, Unset, str]):
    """

    email: str
    email_confirmed: bool
    event_type: str
    first_name: str
    last_name: str
    user_id: str
    picture_url: Union[None, Unset, str] = UNSET
    username: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        email_confirmed = self.email_confirmed

        event_type = self.event_type

        first_name = self.first_name

        last_name = self.last_name

        user_id = self.user_id

        picture_url: Union[None, Unset, str]
        if isinstance(self.picture_url, Unset):
            picture_url = UNSET
        else:
            picture_url = self.picture_url

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "email_confirmed": email_confirmed,
                "event_type": event_type,
                "first_name": first_name,
                "last_name": last_name,
                "user_id": user_id,
            }
        )
        if picture_url is not UNSET:
            field_dict["picture_url"] = picture_url
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        email_confirmed = d.pop("email_confirmed")

        event_type = d.pop("event_type")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        user_id = d.pop("user_id")

        def _parse_picture_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        picture_url = _parse_picture_url(d.pop("picture_url", UNSET))

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        idp_user_create_request = cls(
            email=email,
            email_confirmed=email_confirmed,
            event_type=event_type,
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            picture_url=picture_url,
            username=username,
        )

        idp_user_create_request.additional_properties = d
        return idp_user_create_request

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
