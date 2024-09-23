from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.conversation_nested import ConversationNested
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    conversation_id: str,
    *,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/conversations/{conversation_id}",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ConversationNested, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConversationNested.from_dict(response.json())

        return response_200
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
) -> Response[Union[ConversationNested, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ConversationNested, ErrorResponse]]:
    """Get a conversation

     Get a conversation by ID

    Args:
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConversationNested, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ConversationNested, ErrorResponse]]:
    """Get a conversation

     Get a conversation by ID

    Args:
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConversationNested, ErrorResponse]
    """

    return sync_detailed(
        conversation_id=conversation_id,
        client=client,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ConversationNested, ErrorResponse]]:
    """Get a conversation

     Get a conversation by ID

    Args:
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConversationNested, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ConversationNested, ErrorResponse]]:
    """Get a conversation

     Get a conversation by ID

    Args:
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConversationNested, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            conversation_id=conversation_id,
            client=client,
            x_api_key=x_api_key,
        )
    ).parsed
