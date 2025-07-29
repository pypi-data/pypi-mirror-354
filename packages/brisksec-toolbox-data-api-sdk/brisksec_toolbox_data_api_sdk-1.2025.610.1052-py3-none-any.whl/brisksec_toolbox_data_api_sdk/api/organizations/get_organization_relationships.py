from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_relationship_response import PaginatedResponseRelationshipResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    entity_id: str,
    *,
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    relationship_types: Union[None, Unset, list[str]] = UNSET,
    target_types: Union[None, Unset, list[str]] = UNSET,
    direction: Union[Unset, str] = "both",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    json_size: Union[None, Unset, int]
    if isinstance(size, Unset):
        json_size = UNSET
    else:
        json_size = size
    params["size"] = json_size

    json_relationship_types: Union[None, Unset, list[str]]
    if isinstance(relationship_types, Unset):
        json_relationship_types = UNSET
    elif isinstance(relationship_types, list):
        json_relationship_types = relationship_types

    else:
        json_relationship_types = relationship_types
    params["relationship_types"] = json_relationship_types

    json_target_types: Union[None, Unset, list[str]]
    if isinstance(target_types, Unset):
        json_target_types = UNSET
    elif isinstance(target_types, list):
        json_target_types = target_types

    else:
        json_target_types = target_types
    params["target_types"] = json_target_types

    params["direction"] = direction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/organizations/{entity_id}/relationships",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseRelationshipResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]:
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
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    relationship_types: Union[None, Unset, list[str]] = UNSET,
    target_types: Union[None, Unset, list[str]] = UNSET,
    direction: Union[Unset, str] = "both",
) -> Response[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]:
    """Get Entity Relationships

     Get all entities related to this entity

    Args:
        entity_id (str):
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        relationship_types (Union[None, Unset, list[str]]): Filter by relationship types
        target_types (Union[None, Unset, list[str]]): Filter by target entity types
        direction (Union[Unset, str]): Relationship direction (outgoing, incoming, both) Default:
            'both'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]
    """

    kwargs = _get_kwargs(
        entity_id=entity_id,
        page=page,
        size=size,
        relationship_types=relationship_types,
        target_types=target_types,
        direction=direction,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    relationship_types: Union[None, Unset, list[str]] = UNSET,
    target_types: Union[None, Unset, list[str]] = UNSET,
    direction: Union[Unset, str] = "both",
) -> Optional[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]:
    """Get Entity Relationships

     Get all entities related to this entity

    Args:
        entity_id (str):
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        relationship_types (Union[None, Unset, list[str]]): Filter by relationship types
        target_types (Union[None, Unset, list[str]]): Filter by target entity types
        direction (Union[Unset, str]): Relationship direction (outgoing, incoming, both) Default:
            'both'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseRelationshipResponse]
    """

    return sync_detailed(
        entity_id=entity_id,
        client=client,
        page=page,
        size=size,
        relationship_types=relationship_types,
        target_types=target_types,
        direction=direction,
    ).parsed


async def asyncio_detailed(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    relationship_types: Union[None, Unset, list[str]] = UNSET,
    target_types: Union[None, Unset, list[str]] = UNSET,
    direction: Union[Unset, str] = "both",
) -> Response[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]:
    """Get Entity Relationships

     Get all entities related to this entity

    Args:
        entity_id (str):
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        relationship_types (Union[None, Unset, list[str]]): Filter by relationship types
        target_types (Union[None, Unset, list[str]]): Filter by target entity types
        direction (Union[Unset, str]): Relationship direction (outgoing, incoming, both) Default:
            'both'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]
    """

    kwargs = _get_kwargs(
        entity_id=entity_id,
        page=page,
        size=size,
        relationship_types=relationship_types,
        target_types=target_types,
        direction=direction,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    relationship_types: Union[None, Unset, list[str]] = UNSET,
    target_types: Union[None, Unset, list[str]] = UNSET,
    direction: Union[Unset, str] = "both",
) -> Optional[Union[HTTPValidationError, PaginatedResponseRelationshipResponse]]:
    """Get Entity Relationships

     Get all entities related to this entity

    Args:
        entity_id (str):
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        relationship_types (Union[None, Unset, list[str]]): Filter by relationship types
        target_types (Union[None, Unset, list[str]]): Filter by target entity types
        direction (Union[Unset, str]): Relationship direction (outgoing, incoming, both) Default:
            'both'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseRelationshipResponse]
    """

    return (
        await asyncio_detailed(
            entity_id=entity_id,
            client=client,
            page=page,
            size=size,
            relationship_types=relationship_types,
            target_types=target_types,
            direction=direction,
        )
    ).parsed
