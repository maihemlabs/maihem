from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_test_run_request import CreateTestRunRequest
from ...models.error_response import ErrorResponse
from ...models.test_run import TestRun
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_id: str,
    *,
    body: CreateTestRunRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/tests/{test_id}/test-runs",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TestRun]]:
    if response.status_code == 201:
        response_201 = TestRun.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == 501:
        response_501 = ErrorResponse.from_dict(response.json())

        return response_501
    if response.status_code == 504:
        response_504 = ErrorResponse.from_dict(response.json())

        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, TestRun]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateTestRunRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestRun]]:
    """Run a test

     Create a new run of a specified test

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (CreateTestRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRun]]
    """

    kwargs = _get_kwargs(
        test_id=test_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateTestRunRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestRun]]:
    """Run a test

     Create a new run of a specified test

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (CreateTestRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRun]
    """

    return sync_detailed(
        test_id=test_id,
        client=client,
        body=body,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    test_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateTestRunRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestRun]]:
    """Run a test

     Create a new run of a specified test

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (CreateTestRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRun]]
    """

    kwargs = _get_kwargs(
        test_id=test_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateTestRunRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestRun]]:
    """Run a test

     Create a new run of a specified test

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (CreateTestRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRun]
    """

    return (
        await asyncio_detailed(
            test_id=test_id,
            client=client,
            body=body,
            x_api_key=x_api_key,
        )
    ).parsed
