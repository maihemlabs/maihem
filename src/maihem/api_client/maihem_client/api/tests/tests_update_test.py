from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.test import Test
from ...models.test_create_request import TestCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_id: str,
    *,
    body: TestCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/tests/{test_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, Test]]:
    if response.status_code == 200:
        response_200 = Test.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, Test]]:
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
    body: TestCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, Test]]:
    """Update test

     Update a test configuration

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (TestCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Test]]
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
    body: TestCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, Test]]:
    """Update test

     Update a test configuration

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (TestCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Test]
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
    body: TestCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, Test]]:
    """Update test

     Update a test configuration

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (TestCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Test]]
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
    body: TestCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, Test]]:
    """Update test

     Update a test configuration

    Args:
        test_id (str):
        x_api_key (Union[None, Unset, str]):
        body (TestCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Test]
    """

    return (
        await asyncio_detailed(
            test_id=test_id,
            client=client,
            body=body,
            x_api_key=x_api_key,
        )
    ).parsed
