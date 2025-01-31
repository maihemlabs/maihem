from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.v_test_run_workflow_trace_result import VTestRunWorkflowTraceResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_run_id: str,
    workflow_id: str,
    conversation_id: str,
    *,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/test-runs/{test_run_id}/workflows/{workflow_id}/conversations/{conversation_id}/results",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List["VTestRunWorkflowTraceResult"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VTestRunWorkflowTraceResult.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[ErrorResponse, List["VTestRunWorkflowTraceResult"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_run_id: str,
    workflow_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, List["VTestRunWorkflowTraceResult"]]]:
    """Get test run workflow step results

     Get test run workflow step results

    Args:
        test_run_id (str):
        workflow_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['VTestRunWorkflowTraceResult']]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        workflow_id=workflow_id,
        conversation_id=conversation_id,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_run_id: str,
    workflow_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, List["VTestRunWorkflowTraceResult"]]]:
    """Get test run workflow step results

     Get test run workflow step results

    Args:
        test_run_id (str):
        workflow_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['VTestRunWorkflowTraceResult']]
    """

    return sync_detailed(
        test_run_id=test_run_id,
        workflow_id=workflow_id,
        conversation_id=conversation_id,
        client=client,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    test_run_id: str,
    workflow_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, List["VTestRunWorkflowTraceResult"]]]:
    """Get test run workflow step results

     Get test run workflow step results

    Args:
        test_run_id (str):
        workflow_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['VTestRunWorkflowTraceResult']]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        workflow_id=workflow_id,
        conversation_id=conversation_id,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_run_id: str,
    workflow_id: str,
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, List["VTestRunWorkflowTraceResult"]]]:
    """Get test run workflow step results

     Get test run workflow step results

    Args:
        test_run_id (str):
        workflow_id (str):
        conversation_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['VTestRunWorkflowTraceResult']]
    """

    return (
        await asyncio_detailed(
            test_run_id=test_run_id,
            workflow_id=workflow_id,
            conversation_id=conversation_id,
            client=client,
            x_api_key=x_api_key,
        )
    ).parsed
