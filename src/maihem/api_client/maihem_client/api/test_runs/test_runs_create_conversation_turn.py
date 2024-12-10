from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.conversation_turn_create_request import ConversationTurnCreateRequest
from ...models.conversation_turn_create_response import ConversationTurnCreateResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_run_id: str,
    conversation_id: str,
    *,
    body: ConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/test-runs/{test_run_id}/conversations/{conversation_id}/turns",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ConversationTurnCreateResponse, ErrorResponse]]:
    if response.status_code == 201:
        response_201 = ConversationTurnCreateResponse.from_dict(response.json())

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
) -> Response[Union[ConversationTurnCreateResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_run_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    body: ConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ConversationTurnCreateResponse, ErrorResponse]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (ConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConversationTurnCreateResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        conversation_id=conversation_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_run_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    body: ConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ConversationTurnCreateResponse, ErrorResponse]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (ConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConversationTurnCreateResponse, ErrorResponse]
    """

    return sync_detailed(
        test_run_id=test_run_id,
        conversation_id=conversation_id,
        client=client,
        body=body,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    test_run_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    body: ConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ConversationTurnCreateResponse, ErrorResponse]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (ConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConversationTurnCreateResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        conversation_id=conversation_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_run_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    body: ConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ConversationTurnCreateResponse, ErrorResponse]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (ConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConversationTurnCreateResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            test_run_id=test_run_id,
            conversation_id=conversation_id,
            client=client,
            body=body,
            x_api_key=x_api_key,
        )
    ).parsed
