from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    source_type: str,
    source_id: str,
    target_type: str,
    target_id: str,
    rel_type: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["source_type"] = source_type

    params["source_id"] = source_id

    params["target_type"] = target_type

    params["target_id"] = target_id

    params["rel_type"] = rel_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/relationships/delete",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    source_type: str,
    source_id: str,
    target_type: str,
    target_id: str,
    rel_type: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Relationship

     Delete a relationship.

    Args:
        source_type (str): Type of the source entity
        source_id (str): ID of the source entity
        target_type (str): Type of the target entity
        target_id (str): ID of the target entity
        rel_type (str): Type of relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        rel_type=rel_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    source_type: str,
    source_id: str,
    target_type: str,
    target_id: str,
    rel_type: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Relationship

     Delete a relationship.

    Args:
        source_type (str): Type of the source entity
        source_id (str): ID of the source entity
        target_type (str): Type of the target entity
        target_id (str): ID of the target entity
        rel_type (str): Type of relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        rel_type=rel_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    source_type: str,
    source_id: str,
    target_type: str,
    target_id: str,
    rel_type: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Relationship

     Delete a relationship.

    Args:
        source_type (str): Type of the source entity
        source_id (str): ID of the source entity
        target_type (str): Type of the target entity
        target_id (str): ID of the target entity
        rel_type (str): Type of relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        rel_type=rel_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    source_type: str,
    source_id: str,
    target_type: str,
    target_id: str,
    rel_type: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Relationship

     Delete a relationship.

    Args:
        source_type (str): Type of the source entity
        source_id (str): ID of the source entity
        target_type (str): Type of the target entity
        target_id (str): ID of the target entity
        rel_type (str): Type of relationship

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            rel_type=rel_type,
        )
    ).parsed
