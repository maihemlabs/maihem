from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.test_run_conversation_i_ds import TestRunConversationIDs
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_run_id: str,
    *,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/test-runs/{test_run_id}/conversations",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TestRunConversationIDs]]:
    if response.status_code == 200:
        response_200 = TestRunConversationIDs.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, TestRunConversationIDs]]:
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
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestRunConversationIDs]]:
    """Get test run conversations

     Get a test run including conversations to be run

    Args:
        test_run_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRunConversationIDs]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
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
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestRunConversationIDs]]:
    """Get test run conversations

     Get a test run including conversations to be run

    Args:
        test_run_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRunConversationIDs]
    """

    return sync_detailed(
        test_run_id=test_run_id,
        client=client,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    test_run_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TestRunConversationIDs]]:
    """Get test run conversations

     Get a test run including conversations to be run

    Args:
        test_run_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRunConversationIDs]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_run_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TestRunConversationIDs]]:
    """Get test run conversations

     Get a test run including conversations to be run

    Args:
        test_run_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRunConversationIDs]
    """

    return (
        await asyncio_detailed(
            test_run_id=test_run_id,
            client=client,
            x_api_key=x_api_key,
        )
    ).parsed
