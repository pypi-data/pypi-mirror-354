from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0042_openapi_clusters_resp import V0042OpenapiClustersResp
from ...models.v0042_openapi_resp import V0042OpenapiResp
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: V0042OpenapiClustersResp,
    update_time: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["update_time"] = update_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/slurmdb/v0.0.42/clusters/",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0042OpenapiResp]:
    if response.status_code == 200:
        response_200 = V0042OpenapiResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0042OpenapiResp]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042OpenapiClustersResp,
    update_time: Union[Unset, str] = UNSET,
) -> Response[V0042OpenapiResp]:
    """Get cluster list

    Args:
        update_time (Union[Unset, str]):
        body (V0042OpenapiClustersResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0042OpenapiResp]
    """

    kwargs = _get_kwargs(
        body=body,
        update_time=update_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042OpenapiClustersResp,
    update_time: Union[Unset, str] = UNSET,
) -> Optional[V0042OpenapiResp]:
    """Get cluster list

    Args:
        update_time (Union[Unset, str]):
        body (V0042OpenapiClustersResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0042OpenapiResp
    """

    return sync_detailed(
        client=client,
        body=body,
        update_time=update_time,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042OpenapiClustersResp,
    update_time: Union[Unset, str] = UNSET,
) -> Response[V0042OpenapiResp]:
    """Get cluster list

    Args:
        update_time (Union[Unset, str]):
        body (V0042OpenapiClustersResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0042OpenapiResp]
    """

    kwargs = _get_kwargs(
        body=body,
        update_time=update_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042OpenapiClustersResp,
    update_time: Union[Unset, str] = UNSET,
) -> Optional[V0042OpenapiResp]:
    """Get cluster list

    Args:
        update_time (Union[Unset, str]):
        body (V0042OpenapiClustersResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0042OpenapiResp
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            update_time=update_time,
        )
    ).parsed
