from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_schema_agent_target_create_request import APISchemaAgentTargetCreateRequest
from ...models.api_schema_agent_target_create_response import APISchemaAgentTargetCreateResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: APISchemaAgentTargetCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/agents/target",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = APISchemaAgentTargetCreateResponse.from_dict(response.json())

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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: APISchemaAgentTargetCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]:
    """Connect target agent

     Add a new target agent for Maihem to test

    Args:
        x_api_key (Union[None, Unset, str]):
        body (APISchemaAgentTargetCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]
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
    body: APISchemaAgentTargetCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]:
    """Connect target agent

     Add a new target agent for Maihem to test

    Args:
        x_api_key (Union[None, Unset, str]):
        body (APISchemaAgentTargetCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APISchemaAgentTargetCreateResponse, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: APISchemaAgentTargetCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]:
    """Connect target agent

     Add a new target agent for Maihem to test

    Args:
        x_api_key (Union[None, Unset, str]):
        body (APISchemaAgentTargetCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]
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
    body: APISchemaAgentTargetCreateRequest,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[APISchemaAgentTargetCreateResponse, ErrorResponse]]:
    """Connect target agent

     Add a new target agent for Maihem to test

    Args:
        x_api_key (Union[None, Unset, str]):
        body (APISchemaAgentTargetCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APISchemaAgentTargetCreateResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_api_key=x_api_key,
        )
    ).parsed
