from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.relationship_create import RelationshipCreate
from ...models.relationship_response import RelationshipResponse
from ...types import Response


def _get_kwargs(
    *,
    body: RelationshipCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/relationships/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, RelationshipResponse]]:
    if response.status_code == 201:
        response_201 = RelationshipResponse.from_dict(response.json())

        return response_201
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, RelationshipResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipCreate,
) -> Response[Union[HTTPValidationError, RelationshipResponse]]:
    """Create Relationship

     Create a new relationship between two entities.

    This endpoint allows creating a relationship of any valid type between any two entities.
    The relationship type must be valid for the given source and target entity types.

    Args:
        body (RelationshipCreate): Schema for creating a new relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RelationshipResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipCreate,
) -> Optional[Union[HTTPValidationError, RelationshipResponse]]:
    """Create Relationship

     Create a new relationship between two entities.

    This endpoint allows creating a relationship of any valid type between any two entities.
    The relationship type must be valid for the given source and target entity types.

    Args:
        body (RelationshipCreate): Schema for creating a new relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RelationshipResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipCreate,
) -> Response[Union[HTTPValidationError, RelationshipResponse]]:
    """Create Relationship

     Create a new relationship between two entities.

    This endpoint allows creating a relationship of any valid type between any two entities.
    The relationship type must be valid for the given source and target entity types.

    Args:
        body (RelationshipCreate): Schema for creating a new relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RelationshipResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipCreate,
) -> Optional[Union[HTTPValidationError, RelationshipResponse]]:
    """Create Relationship

     Create a new relationship between two entities.

    This endpoint allows creating a relationship of any valid type between any two entities.
    The relationship type must be valid for the given source and target entity types.

    Args:
        body (RelationshipCreate): Schema for creating a new relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RelationshipResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
