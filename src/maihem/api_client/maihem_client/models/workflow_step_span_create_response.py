from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_step_span_create_response_input_payload_type_0 import (
        WorkflowStepSpanCreateResponseInputPayloadType0,
    )


T = TypeVar("T", bound="WorkflowStepSpanCreateResponse")


@_attrs_define
class WorkflowStepSpanCreateResponse:
    """
    Attributes:
        input_payload (Union['WorkflowStepSpanCreateResponseInputPayloadType0', None, Unset]):
    """

    input_payload: Union["WorkflowStepSpanCreateResponseInputPayloadType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workflow_step_span_create_response_input_payload_type_0 import (
            WorkflowStepSpanCreateResponseInputPayloadType0,
        )

        input_payload: Union[None, Unset, dict[str, Any]]
        if isinstance(self.input_payload, Unset):
            input_payload = UNSET
        elif isinstance(self.input_payload, WorkflowStepSpanCreateResponseInputPayloadType0):
            input_payload = self.input_payload.to_dict()
        else:
            input_payload = self.input_payload

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_payload is not UNSET:
            field_dict["input_payload"] = input_payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.workflow_step_span_create_response_input_payload_type_0 import (
            WorkflowStepSpanCreateResponseInputPayloadType0,
        )

        d = src_dict.copy()

        def _parse_input_payload(data: object) -> Union["WorkflowStepSpanCreateResponseInputPayloadType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_payload_type_0 = WorkflowStepSpanCreateResponseInputPayloadType0.from_dict(data)

                return input_payload_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WorkflowStepSpanCreateResponseInputPayloadType0", None, Unset], data)

        input_payload = _parse_input_payload(d.pop("input_payload", UNSET))

        workflow_step_span_create_response = cls(
            input_payload=input_payload,
        )

        workflow_step_span_create_response.additional_properties = d
        return workflow_step_span_create_response

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
