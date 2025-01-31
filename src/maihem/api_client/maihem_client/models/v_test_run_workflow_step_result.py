import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="VTestRunWorkflowStepResult")


@_attrs_define
class VTestRunWorkflowStepResult:
    """
    Attributes:
        org_id (str):
        test_run_id (str):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        workflow_id (str):
        name (str):
        label (Union[None, str]):
        score (Union[Any, None]):
        result (Union[Any, None]):
    """

    org_id: str
    test_run_id: str
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    workflow_id: str
    name: str
    label: Union[None, str]
    score: Union[Any, None]
    result: Union[Any, None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org_id = self.org_id

        test_run_id = self.test_run_id

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        workflow_id = self.workflow_id

        name = self.name

        label: Union[None, str]
        label = self.label

        score: Union[Any, None]
        score = self.score

        result: Union[Any, None]
        result = self.result

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org_id": org_id,
                "test_run_id": test_run_id,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "workflow_id": workflow_id,
                "name": name,
                "label": label,
                "score": score,
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org_id = d.pop("org_id")

        test_run_id = d.pop("test_run_id")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        workflow_id = d.pop("workflow_id")

        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        label = _parse_label(d.pop("label"))

        def _parse_score(data: object) -> Union[Any, None]:
            if data is None:
                return data
            return cast(Union[Any, None], data)

        score = _parse_score(d.pop("score"))

        def _parse_result(data: object) -> Union[Any, None]:
            if data is None:
                return data
            return cast(Union[Any, None], data)

        result = _parse_result(d.pop("result"))

        v_test_run_workflow_step_result = cls(
            org_id=org_id,
            test_run_id=test_run_id,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            workflow_id=workflow_id,
            name=name,
            label=label,
            score=score,
            result=result,
        )

        v_test_run_workflow_step_result.additional_properties = d
        return v_test_run_workflow_step_result

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
