import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="VEvaluationReviewAudit")


@_attrs_define
class VEvaluationReviewAudit:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        evaluation_id (str):
        action (str):
        event (str):
        actioned_by (str):
        actioned_at (datetime.datetime):
        content (Union[None, str]):
        evl_entity_type (str):
        evl_entity_id (str):
        actioned_by_first_name (str):
        actioned_by_last_name (str):
        actioned_by_image_url (Union[None, str]):
        org_id (str):
        test_run_id (str):
        metric_id (str):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    evaluation_id: str
    action: str
    event: str
    actioned_by: str
    actioned_at: datetime.datetime
    content: Union[None, str]
    evl_entity_type: str
    evl_entity_id: str
    actioned_by_first_name: str
    actioned_by_last_name: str
    actioned_by_image_url: Union[None, str]
    org_id: str
    test_run_id: str
    metric_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        evaluation_id = self.evaluation_id

        action = self.action

        event = self.event

        actioned_by = self.actioned_by

        actioned_at = self.actioned_at.isoformat()

        content: Union[None, str]
        content = self.content

        evl_entity_type = self.evl_entity_type

        evl_entity_id = self.evl_entity_id

        actioned_by_first_name = self.actioned_by_first_name

        actioned_by_last_name = self.actioned_by_last_name

        actioned_by_image_url: Union[None, str]
        actioned_by_image_url = self.actioned_by_image_url

        org_id = self.org_id

        test_run_id = self.test_run_id

        metric_id = self.metric_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "evaluation_id": evaluation_id,
                "action": action,
                "event": event,
                "actioned_by": actioned_by,
                "actioned_at": actioned_at,
                "content": content,
                "evl_entity_type": evl_entity_type,
                "evl_entity_id": evl_entity_id,
                "actioned_by_first_name": actioned_by_first_name,
                "actioned_by_last_name": actioned_by_last_name,
                "actioned_by_image_url": actioned_by_image_url,
                "org_id": org_id,
                "test_run_id": test_run_id,
                "metric_id": metric_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        evaluation_id = d.pop("evaluation_id")

        action = d.pop("action")

        event = d.pop("event")

        actioned_by = d.pop("actioned_by")

        actioned_at = isoparse(d.pop("actioned_at"))

        def _parse_content(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        content = _parse_content(d.pop("content"))

        evl_entity_type = d.pop("evl_entity_type")

        evl_entity_id = d.pop("evl_entity_id")

        actioned_by_first_name = d.pop("actioned_by_first_name")

        actioned_by_last_name = d.pop("actioned_by_last_name")

        def _parse_actioned_by_image_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        actioned_by_image_url = _parse_actioned_by_image_url(d.pop("actioned_by_image_url"))

        org_id = d.pop("org_id")

        test_run_id = d.pop("test_run_id")

        metric_id = d.pop("metric_id")

        v_evaluation_review_audit = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            evaluation_id=evaluation_id,
            action=action,
            event=event,
            actioned_by=actioned_by,
            actioned_at=actioned_at,
            content=content,
            evl_entity_type=evl_entity_type,
            evl_entity_id=evl_entity_id,
            actioned_by_first_name=actioned_by_first_name,
            actioned_by_last_name=actioned_by_last_name,
            actioned_by_image_url=actioned_by_image_url,
            org_id=org_id,
            test_run_id=test_run_id,
            metric_id=metric_id,
        )

        v_evaluation_review_audit.additional_properties = d
        return v_evaluation_review_audit

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
