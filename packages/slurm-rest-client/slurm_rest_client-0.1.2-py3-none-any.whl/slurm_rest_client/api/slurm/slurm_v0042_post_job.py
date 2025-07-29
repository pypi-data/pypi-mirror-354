from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0042_job_desc_msg import V0042JobDescMsg
from ...models.v0042_openapi_job_post_response import V0042OpenapiJobPostResponse
from ...types import Response


def _get_kwargs(
    job_id: str,
    *,
    body: V0042JobDescMsg,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/slurm/v0.0.42/job/{job_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0042OpenapiJobPostResponse]:
    if response.status_code == 200:
        response_200 = V0042OpenapiJobPostResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0042OpenapiJobPostResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042JobDescMsg,
) -> Response[V0042OpenapiJobPostResponse]:
    """update job

    Args:
        job_id (str):
        body (V0042JobDescMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0042OpenapiJobPostResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042JobDescMsg,
) -> Optional[V0042OpenapiJobPostResponse]:
    """update job

    Args:
        job_id (str):
        body (V0042JobDescMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0042OpenapiJobPostResponse
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042JobDescMsg,
) -> Response[V0042OpenapiJobPostResponse]:
    """update job

    Args:
        job_id (str):
        body (V0042JobDescMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0042OpenapiJobPostResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0042JobDescMsg,
) -> Optional[V0042OpenapiJobPostResponse]:
    """update job

    Args:
        job_id (str):
        body (V0042JobDescMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0042OpenapiJobPostResponse
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            body=body,
        )
    ).parsed
