import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.test_run_results import TestRunResults
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_id: str,
    *,
    before_datetime: Union[None, Unset, datetime.datetime] = UNSET,
    limit: Union[None, Unset, int] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    params: Dict[str, Any] = {}

    json_before_datetime: Union[None, Unset, str]
    if isinstance(before_datetime, Unset):
        json_before_datetime = UNSET
    elif isinstance(before_datetime, datetime.datetime):
        json_before_datetime = before_datetime.isoformat()
    else:
        json_before_datetime = before_datetime
    params["before_datetime"] = json_before_datetime

    json_limit: Union[None, Unset, int]
    if isinstance(limit, Unset):
        json_limit = UNSET
    else:
        json_limit = limit
    params["limit"] = json_limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/tests/{test_id}/test-runs/results",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List["TestRunResults"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TestRunResults.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[ErrorResponse, List["TestRunResults"]]]:
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
    before_datetime: Union[None, Unset, datetime.datetime] = UNSET,
    limit: Union[None, Unset, int] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, List["TestRunResults"]]]:
    """Get all test run results for a test

     Get all test test run results for a test

    Args:
        test_id (str):
        before_datetime (Union[None, Unset, datetime.datetime]):
        limit (Union[None, Unset, int]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['TestRunResults']]]
    """

    kwargs = _get_kwargs(
        test_id=test_id,
        before_datetime=before_datetime,
        limit=limit,
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
    before_datetime: Union[None, Unset, datetime.datetime] = UNSET,
    limit: Union[None, Unset, int] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, List["TestRunResults"]]]:
    """Get all test run results for a test

     Get all test test run results for a test

    Args:
        test_id (str):
        before_datetime (Union[None, Unset, datetime.datetime]):
        limit (Union[None, Unset, int]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['TestRunResults']]
    """

    return sync_detailed(
        test_id=test_id,
        client=client,
        before_datetime=before_datetime,
        limit=limit,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    test_id: str,
    *,
    client: AuthenticatedClient,
    before_datetime: Union[None, Unset, datetime.datetime] = UNSET,
    limit: Union[None, Unset, int] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, List["TestRunResults"]]]:
    """Get all test run results for a test

     Get all test test run results for a test

    Args:
        test_id (str):
        before_datetime (Union[None, Unset, datetime.datetime]):
        limit (Union[None, Unset, int]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['TestRunResults']]]
    """

    kwargs = _get_kwargs(
        test_id=test_id,
        before_datetime=before_datetime,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_id: str,
    *,
    client: AuthenticatedClient,
    before_datetime: Union[None, Unset, datetime.datetime] = UNSET,
    limit: Union[None, Unset, int] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, List["TestRunResults"]]]:
    """Get all test run results for a test

     Get all test test run results for a test

    Args:
        test_id (str):
        before_datetime (Union[None, Unset, datetime.datetime]):
        limit (Union[None, Unset, int]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['TestRunResults']]
    """

    return (
        await asyncio_detailed(
            test_id=test_id,
            client=client,
            before_datetime=before_datetime,
            limit=limit,
            x_api_key=x_api_key,
        )
    ).parsed
