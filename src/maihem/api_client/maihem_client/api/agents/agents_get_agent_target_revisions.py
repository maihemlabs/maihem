from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_target_revision import AgentTargetRevision
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    agent_target_id: str,
    *,
    name: Union[Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    params: dict[str, Any] = {}

    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/agents/target/{agent_target_id}/revisions",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, list["AgentTargetRevision"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AgentTargetRevision.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
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
) -> Response[Union[ErrorResponse, list["AgentTargetRevision"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_target_id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, list["AgentTargetRevision"]]]:
    """Get all revisions for a target agent

     Get all revisions for a target agent

    Args:
        agent_target_id (str):
        name (Union[Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['AgentTargetRevision']]]
    """

    kwargs = _get_kwargs(
        agent_target_id=agent_target_id,
        name=name,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_target_id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, list["AgentTargetRevision"]]]:
    """Get all revisions for a target agent

     Get all revisions for a target agent

    Args:
        agent_target_id (str):
        name (Union[Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['AgentTargetRevision']]
    """

    return sync_detailed(
        agent_target_id=agent_target_id,
        client=client,
        name=name,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    agent_target_id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, list["AgentTargetRevision"]]]:
    """Get all revisions for a target agent

     Get all revisions for a target agent

    Args:
        agent_target_id (str):
        name (Union[Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['AgentTargetRevision']]]
    """

    kwargs = _get_kwargs(
        agent_target_id=agent_target_id,
        name=name,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_target_id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, list["AgentTargetRevision"]]]:
    """Get all revisions for a target agent

     Get all revisions for a target agent

    Args:
        agent_target_id (str):
        name (Union[Unset, str]):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['AgentTargetRevision']]
    """

    return (
        await asyncio_detailed(
            agent_target_id=agent_target_id,
            client=client,
            name=name,
            x_api_key=x_api_key,
        )
    ).parsed
