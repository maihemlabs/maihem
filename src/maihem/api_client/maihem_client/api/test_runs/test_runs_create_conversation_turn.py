from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_schema_conversation_turn_create_request import APISchemaConversationTurnCreateRequest
from ...models.api_schema_conversation_turn_create_response import APISchemaConversationTurnCreateResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_run_id: str,
    conversation_id: str,
    *,
    body: APISchemaConversationTurnCreateRequest,
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
) -> Optional[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = APISchemaConversationTurnCreateResponse.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]:
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
    body: APISchemaConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]
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
    body: APISchemaConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]
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
    body: APISchemaConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]
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
    body: APISchemaConversationTurnCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]]:
    """Create a conversation turn

     Create a new turn in a specified conversation

    Args:
        test_run_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):
        body (APISchemaConversationTurnCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APISchemaConversationTurnCreateResponse, HTTPValidationError]
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
