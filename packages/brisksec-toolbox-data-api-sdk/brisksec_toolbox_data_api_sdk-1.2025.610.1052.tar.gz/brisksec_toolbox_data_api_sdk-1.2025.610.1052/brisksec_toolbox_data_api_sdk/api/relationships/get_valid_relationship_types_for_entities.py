from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_responsestr import PaginatedResponsestr
from ...types import Response


def _get_kwargs(
    source_type: str,
    target_type: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/relationships/types/{source_type}/{target_type}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponsestr]]:
    if response.status_code == 200:
        response_200 = PaginatedResponsestr.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponsestr]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    source_type: str,
    target_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, PaginatedResponsestr]]:
    """Get Valid Relationship Types For Entities

     Get valid relationship types between two entity types.

    This endpoint returns a list of relationship types that are valid
    between the given source and target entity types.

    Args:
        source_type (str): Source entity type
        target_type (str): Target entity type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponsestr]]
    """

    kwargs = _get_kwargs(
        source_type=source_type,
        target_type=target_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    source_type: str,
    target_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, PaginatedResponsestr]]:
    """Get Valid Relationship Types For Entities

     Get valid relationship types between two entity types.

    This endpoint returns a list of relationship types that are valid
    between the given source and target entity types.

    Args:
        source_type (str): Source entity type
        target_type (str): Target entity type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponsestr]
    """

    return sync_detailed(
        source_type=source_type,
        target_type=target_type,
        client=client,
    ).parsed


async def asyncio_detailed(
    source_type: str,
    target_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, PaginatedResponsestr]]:
    """Get Valid Relationship Types For Entities

     Get valid relationship types between two entity types.

    This endpoint returns a list of relationship types that are valid
    between the given source and target entity types.

    Args:
        source_type (str): Source entity type
        target_type (str): Target entity type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponsestr]]
    """

    kwargs = _get_kwargs(
        source_type=source_type,
        target_type=target_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    source_type: str,
    target_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, PaginatedResponsestr]]:
    """Get Valid Relationship Types For Entities

     Get valid relationship types between two entity types.

    This endpoint returns a list of relationship types that are valid
    between the given source and target entity types.

    Args:
        source_type (str): Source entity type
        target_type (str): Target entity type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponsestr]
    """

    return (
        await asyncio_detailed(
            source_type=source_type,
            target_type=target_type,
            client=client,
        )
    ).parsed
