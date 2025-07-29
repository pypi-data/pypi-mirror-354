from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.relationship_batch_create import RelationshipBatchCreate
from ...models.relationship_response import RelationshipResponse
from ...types import Response


def _get_kwargs(
    *,
    body: RelationshipBatchCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/relationships/batch",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["RelationshipResponse"]]]:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = RelationshipResponse.from_dict(response_201_item_data)

            response_201.append(response_201_item)

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
) -> Response[Union[HTTPValidationError, list["RelationshipResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipBatchCreate,
) -> Response[Union[HTTPValidationError, list["RelationshipResponse"]]]:
    """Create Relationships Batch

     Create multiple relationships in a batch.

    This endpoint allows creating multiple relationships in a single request.
    If any relationship creation fails, the entire batch will fail.

    Args:
        body (RelationshipBatchCreate): Schema for creating multiple relationships in a batch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['RelationshipResponse']]]
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
    body: RelationshipBatchCreate,
) -> Optional[Union[HTTPValidationError, list["RelationshipResponse"]]]:
    """Create Relationships Batch

     Create multiple relationships in a batch.

    This endpoint allows creating multiple relationships in a single request.
    If any relationship creation fails, the entire batch will fail.

    Args:
        body (RelationshipBatchCreate): Schema for creating multiple relationships in a batch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['RelationshipResponse']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipBatchCreate,
) -> Response[Union[HTTPValidationError, list["RelationshipResponse"]]]:
    """Create Relationships Batch

     Create multiple relationships in a batch.

    This endpoint allows creating multiple relationships in a single request.
    If any relationship creation fails, the entire batch will fail.

    Args:
        body (RelationshipBatchCreate): Schema for creating multiple relationships in a batch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['RelationshipResponse']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RelationshipBatchCreate,
) -> Optional[Union[HTTPValidationError, list["RelationshipResponse"]]]:
    """Create Relationships Batch

     Create multiple relationships in a batch.

    This endpoint allows creating multiple relationships in a single request.
    If any relationship creation fails, the entire batch will fail.

    Args:
        body (RelationshipBatchCreate): Schema for creating multiple relationships in a batch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['RelationshipResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
