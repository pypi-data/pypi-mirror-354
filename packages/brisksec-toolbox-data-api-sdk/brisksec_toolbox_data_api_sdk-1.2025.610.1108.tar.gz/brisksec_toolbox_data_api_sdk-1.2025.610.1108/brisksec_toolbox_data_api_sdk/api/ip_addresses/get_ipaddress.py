from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.ip_address_response import IPAddressResponse
from ...types import Response


def _get_kwargs(
    entity_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/ip-addresses/{entity_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, IPAddressResponse]]:
    if response.status_code == 200:
        response_200 = IPAddressResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, IPAddressResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, IPAddressResponse]]:
    """Get Entity

     Get an entity by ID

    Args:
        entity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, IPAddressResponse]]
    """

    kwargs = _get_kwargs(
        entity_id=entity_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, IPAddressResponse]]:
    """Get Entity

     Get an entity by ID

    Args:
        entity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, IPAddressResponse]
    """

    return sync_detailed(
        entity_id=entity_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, IPAddressResponse]]:
    """Get Entity

     Get an entity by ID

    Args:
        entity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, IPAddressResponse]]
    """

    kwargs = _get_kwargs(
        entity_id=entity_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, IPAddressResponse]]:
    """Get Entity

     Get an entity by ID

    Args:
        entity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, IPAddressResponse]
    """

    return (
        await asyncio_detailed(
            entity_id=entity_id,
            client=client,
        )
    ).parsed
