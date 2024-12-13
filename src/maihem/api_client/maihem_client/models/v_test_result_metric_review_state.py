import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="VTestResultMetricReviewState")


@_attrs_define
class VTestResultMetricReviewState:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        test_result_metric_id (str):
        is_result_reviewed (bool):
        is_flagged_internal (bool):
        is_flagged_customer (bool):
        result_reviewed_by (Union[None, str]):
        flagged_internal_by (Union[None, str]):
        flagged_customer_by (Union[None, str]):
        trm_entity_type (str):
        trm_entity_id (str):
        result_reviewed_by_first_name (Union[None, str]):
        result_reviewed_by_last_name (Union[None, str]):
        flagged_internal_by_first_name (Union[None, str]):
        flagged_internal_by_last_name (Union[None, str]):
        flagged_customer_by_first_name (Union[None, str]):
        flagged_customer_by_last_name (Union[None, str]):
        org_id (str):
        test_run_id (str):
        metric_id (str):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    test_result_metric_id: str
    is_result_reviewed: bool
    is_flagged_internal: bool
    is_flagged_customer: bool
    result_reviewed_by: Union[None, str]
    flagged_internal_by: Union[None, str]
    flagged_customer_by: Union[None, str]
    trm_entity_type: str
    trm_entity_id: str
    result_reviewed_by_first_name: Union[None, str]
    result_reviewed_by_last_name: Union[None, str]
    flagged_internal_by_first_name: Union[None, str]
    flagged_internal_by_last_name: Union[None, str]
    flagged_customer_by_first_name: Union[None, str]
    flagged_customer_by_last_name: Union[None, str]
    org_id: str
    test_run_id: str
    metric_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        test_result_metric_id = self.test_result_metric_id

        is_result_reviewed = self.is_result_reviewed

        is_flagged_internal = self.is_flagged_internal

        is_flagged_customer = self.is_flagged_customer

        result_reviewed_by: Union[None, str]
        result_reviewed_by = self.result_reviewed_by

        flagged_internal_by: Union[None, str]
        flagged_internal_by = self.flagged_internal_by

        flagged_customer_by: Union[None, str]
        flagged_customer_by = self.flagged_customer_by

        trm_entity_type = self.trm_entity_type

        trm_entity_id = self.trm_entity_id

        result_reviewed_by_first_name: Union[None, str]
        result_reviewed_by_first_name = self.result_reviewed_by_first_name

        result_reviewed_by_last_name: Union[None, str]
        result_reviewed_by_last_name = self.result_reviewed_by_last_name

        flagged_internal_by_first_name: Union[None, str]
        flagged_internal_by_first_name = self.flagged_internal_by_first_name

        flagged_internal_by_last_name: Union[None, str]
        flagged_internal_by_last_name = self.flagged_internal_by_last_name

        flagged_customer_by_first_name: Union[None, str]
        flagged_customer_by_first_name = self.flagged_customer_by_first_name

        flagged_customer_by_last_name: Union[None, str]
        flagged_customer_by_last_name = self.flagged_customer_by_last_name

        org_id = self.org_id

        test_run_id = self.test_run_id

        metric_id = self.metric_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "test_result_metric_id": test_result_metric_id,
                "is_result_reviewed": is_result_reviewed,
                "is_flagged_internal": is_flagged_internal,
                "is_flagged_customer": is_flagged_customer,
                "result_reviewed_by": result_reviewed_by,
                "flagged_internal_by": flagged_internal_by,
                "flagged_customer_by": flagged_customer_by,
                "trm_entity_type": trm_entity_type,
                "trm_entity_id": trm_entity_id,
                "result_reviewed_by_first_name": result_reviewed_by_first_name,
                "result_reviewed_by_last_name": result_reviewed_by_last_name,
                "flagged_internal_by_first_name": flagged_internal_by_first_name,
                "flagged_internal_by_last_name": flagged_internal_by_last_name,
                "flagged_customer_by_first_name": flagged_customer_by_first_name,
                "flagged_customer_by_last_name": flagged_customer_by_last_name,
                "org_id": org_id,
                "test_run_id": test_run_id,
                "metric_id": metric_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        test_result_metric_id = d.pop("test_result_metric_id")

        is_result_reviewed = d.pop("is_result_reviewed")

        is_flagged_internal = d.pop("is_flagged_internal")

        is_flagged_customer = d.pop("is_flagged_customer")

        def _parse_result_reviewed_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        result_reviewed_by = _parse_result_reviewed_by(d.pop("result_reviewed_by"))

        def _parse_flagged_internal_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        flagged_internal_by = _parse_flagged_internal_by(d.pop("flagged_internal_by"))

        def _parse_flagged_customer_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        flagged_customer_by = _parse_flagged_customer_by(d.pop("flagged_customer_by"))

        trm_entity_type = d.pop("trm_entity_type")

        trm_entity_id = d.pop("trm_entity_id")

        def _parse_result_reviewed_by_first_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        result_reviewed_by_first_name = _parse_result_reviewed_by_first_name(d.pop("result_reviewed_by_first_name"))

        def _parse_result_reviewed_by_last_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        result_reviewed_by_last_name = _parse_result_reviewed_by_last_name(d.pop("result_reviewed_by_last_name"))

        def _parse_flagged_internal_by_first_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        flagged_internal_by_first_name = _parse_flagged_internal_by_first_name(d.pop("flagged_internal_by_first_name"))

        def _parse_flagged_internal_by_last_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        flagged_internal_by_last_name = _parse_flagged_internal_by_last_name(d.pop("flagged_internal_by_last_name"))

        def _parse_flagged_customer_by_first_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        flagged_customer_by_first_name = _parse_flagged_customer_by_first_name(d.pop("flagged_customer_by_first_name"))

        def _parse_flagged_customer_by_last_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        flagged_customer_by_last_name = _parse_flagged_customer_by_last_name(d.pop("flagged_customer_by_last_name"))

        org_id = d.pop("org_id")

        test_run_id = d.pop("test_run_id")

        metric_id = d.pop("metric_id")

        v_test_result_metric_review_state = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            test_result_metric_id=test_result_metric_id,
            is_result_reviewed=is_result_reviewed,
            is_flagged_internal=is_flagged_internal,
            is_flagged_customer=is_flagged_customer,
            result_reviewed_by=result_reviewed_by,
            flagged_internal_by=flagged_internal_by,
            flagged_customer_by=flagged_customer_by,
            trm_entity_type=trm_entity_type,
            trm_entity_id=trm_entity_id,
            result_reviewed_by_first_name=result_reviewed_by_first_name,
            result_reviewed_by_last_name=result_reviewed_by_last_name,
            flagged_internal_by_first_name=flagged_internal_by_first_name,
            flagged_internal_by_last_name=flagged_internal_by_last_name,
            flagged_customer_by_first_name=flagged_customer_by_first_name,
            flagged_customer_by_last_name=flagged_customer_by_last_name,
            org_id=org_id,
            test_run_id=test_run_id,
            metric_id=metric_id,
        )

        v_test_result_metric_review_state.additional_properties = d
        return v_test_result_metric_review_state

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
