from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.test_run_results_conversations import TestRunResultsConversations
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_run_id: str,
    *,
    metric_id: Union[None, Unset, str] = UNSET,
    metric_result: Union[None, Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    params: Dict[str, Any] = {}

    json_metric_id: Union[None, Unset, str]
    if isinstance(metric_id, Unset):
        json_metric_id = UNSET
    else:
        json_metric_id = metric_id
    params["metric_id"] = json_metric_id

    json_metric_result: Union[None, Unset, str]
    if isinstance(metric_result, Unset):
        json_metric_result = UNSET
    else:
        json_metric_result = metric_result
    params["metric_result"] = json_metric_result

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/test-runs/{test_run_id}/results/conversations",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TestRunResultsConversations]]:
    if response.status_code == 200:
        response_200 = TestRunResultsConversations.from_dict(response.json())

        return response_200
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
) -> Response[Union[ErrorResponse, TestRunResultsConversations]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_run_id: str,
    *,
    client: AuthenticatedClient,
    metric_id: Union[None, Unset, str] = UNSET,
    metric_result: Union[None, Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestRunResultsConversations]]:
    """Get test run result with conversations

     Get a test run result including agent conversations

    Args:
        test_run_id (str):
        metric_id (Union[None, Unset, str]):
        metric_result (Union[None, Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRunResultsConversations]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        metric_id=metric_id,
        metric_result=metric_result,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_run_id: str,
    *,
    client: AuthenticatedClient,
    metric_id: Union[None, Unset, str] = UNSET,
    metric_result: Union[None, Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestRunResultsConversations]]:
    """Get test run result with conversations

     Get a test run result including agent conversations

    Args:
        test_run_id (str):
        metric_id (Union[None, Unset, str]):
        metric_result (Union[None, Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRunResultsConversations]
    """

    return sync_detailed(
        test_run_id=test_run_id,
        client=client,
        metric_id=metric_id,
        metric_result=metric_result,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    test_run_id: str,
    *,
    client: AuthenticatedClient,
    metric_id: Union[None, Unset, str] = UNSET,
    metric_result: Union[None, Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestRunResultsConversations]]:
    """Get test run result with conversations

     Get a test run result including agent conversations

    Args:
        test_run_id (str):
        metric_id (Union[None, Unset, str]):
        metric_result (Union[None, Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRunResultsConversations]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        metric_id=metric_id,
        metric_result=metric_result,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_run_id: str,
    *,
    client: AuthenticatedClient,
    metric_id: Union[None, Unset, str] = UNSET,
    metric_result: Union[None, Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestRunResultsConversations]]:
    """Get test run result with conversations

     Get a test run result including agent conversations

    Args:
        test_run_id (str):
        metric_id (Union[None, Unset, str]):
        metric_result (Union[None, Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRunResultsConversations]
    """

    return (
        await asyncio_detailed(
            test_run_id=test_run_id,
            client=client,
            metric_id=metric_id,
            metric_result=metric_result,
            x_api_key=x_api_key,
        )
    ).parsed
