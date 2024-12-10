from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.test_result_metric_feedback import TestResultMetricFeedback
from ...models.test_result_metric_feedback_create_request import TestResultMetricFeedbackCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: TestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/test-result-metrics/feedback",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TestResultMetricFeedback]]:
    if response.status_code == 201:
        response_201 = TestResultMetricFeedback.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == 504:
        response_504 = ErrorResponse.from_dict(response.json())

        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, TestResultMetricFeedback]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestResultMetricFeedback]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        x_api_key (Union[None, Unset, str]):
        body (TestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestResultMetricFeedback]]
    """

    kwargs = _get_kwargs(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: TestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestResultMetricFeedback]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        x_api_key (Union[None, Unset, str]):
        body (TestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestResultMetricFeedback]
    """

    return sync_detailed(
        client=client,
        body=body,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestResultMetricFeedback]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        x_api_key (Union[None, Unset, str]):
        body (TestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestResultMetricFeedback]]
    """

    kwargs = _get_kwargs(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TestResultMetricFeedbackCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestResultMetricFeedback]]:
    """Add test result metric feedback

     Add feedback to a test result metric

    Args:
        x_api_key (Union[None, Unset, str]):
        body (TestResultMetricFeedbackCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestResultMetricFeedback]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_api_key=x_api_key,
        )
    ).parsed
