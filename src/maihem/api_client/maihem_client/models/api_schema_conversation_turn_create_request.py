from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_schema_conversation_turn_create_request_document_type_0 import (
        APISchemaConversationTurnCreateRequestDocumentType0,
    )


T = TypeVar("T", bound="APISchemaConversationTurnCreateRequest")


@_attrs_define
class APISchemaConversationTurnCreateRequest:
    """
    Attributes:
        message (Union[None, Unset, str]):
        contexts (Union[List[str], None, Unset]):
        document (Union['APISchemaConversationTurnCreateRequestDocumentType0', None, Unset]):
    """

    message: Union[None, Unset, str] = UNSET
    contexts: Union[List[str], None, Unset] = UNSET
    document: Union["APISchemaConversationTurnCreateRequestDocumentType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.api_schema_conversation_turn_create_request_document_type_0 import (
            APISchemaConversationTurnCreateRequestDocumentType0,
        )

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        contexts: Union[List[str], None, Unset]
        if isinstance(self.contexts, Unset):
            contexts = UNSET
        elif isinstance(self.contexts, list):
            contexts = self.contexts

        else:
            contexts = self.contexts

        document: Union[Dict[str, Any], None, Unset]
        if isinstance(self.document, Unset):
            document = UNSET
        elif isinstance(self.document, APISchemaConversationTurnCreateRequestDocumentType0):
            document = self.document.to_dict()
        else:
            document = self.document

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if contexts is not UNSET:
            field_dict["contexts"] = contexts
        if document is not UNSET:
            field_dict["document"] = document

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_schema_conversation_turn_create_request_document_type_0 import (
            APISchemaConversationTurnCreateRequestDocumentType0,
        )

        d = src_dict.copy()

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_contexts(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                contexts_type_0 = cast(List[str], data)

                return contexts_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        contexts = _parse_contexts(d.pop("contexts", UNSET))

        def _parse_document(data: object) -> Union["APISchemaConversationTurnCreateRequestDocumentType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                document_type_0 = APISchemaConversationTurnCreateRequestDocumentType0.from_dict(data)

                return document_type_0
            except:  # noqa: E722
                pass
            return cast(Union["APISchemaConversationTurnCreateRequestDocumentType0", None, Unset], data)

        document = _parse_document(d.pop("document", UNSET))

        api_schema_conversation_turn_create_request = cls(
            message=message,
            contexts=contexts,
            document=document,
        )

        api_schema_conversation_turn_create_request.additional_properties = d
        return api_schema_conversation_turn_create_request

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
