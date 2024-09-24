from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_schema_test_result_metric_feedback import APISchemaTestResultMetricFeedback
from ...models.api_schema_test_result_metric_feedback_create_request import (
    APISchemaTestResultMetricFeedbackCreateRequest,
)
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    trm_id: str,
    *,
    body: APISchemaTestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/test-result-metrics/{trm_id}/feedback",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = APISchemaTestResultMetricFeedback.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.GATEWAY_TIMEOUT:
        response_504 = ErrorResponse.from_dict(response.json())

        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    trm_id: str,
    *,
    client: AuthenticatedClient,
    body: APISchemaTestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        trm_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaTestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        trm_id=trm_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    trm_id: str,
    *,
    client: AuthenticatedClient,
    body: APISchemaTestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        trm_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaTestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APISchemaTestResultMetricFeedback, ErrorResponse]
    """

    return sync_detailed(
        trm_id=trm_id,
        client=client,
        body=body,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    trm_id: str,
    *,
    client: AuthenticatedClient,
    body: APISchemaTestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        trm_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaTestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        trm_id=trm_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    trm_id: str,
    *,
    client: AuthenticatedClient,
    body: APISchemaTestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[APISchemaTestResultMetricFeedback, ErrorResponse]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        trm_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaTestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APISchemaTestResultMetricFeedback, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            trm_id=trm_id,
            client=client,
            body=body,
            x_api_key=x_api_key,
        )
    ).parsed
