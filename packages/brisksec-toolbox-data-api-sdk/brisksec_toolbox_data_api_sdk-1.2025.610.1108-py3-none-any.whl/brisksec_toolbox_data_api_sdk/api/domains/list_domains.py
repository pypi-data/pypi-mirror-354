from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_domain_response import PaginatedResponseDomainResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    search: Union[None, Unset, str] = UNSET,
    registrar: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    json_size: Union[None, Unset, int]
    if isinstance(size, Unset):
        json_size = UNSET
    else:
        json_size = size
    params["size"] = json_size

    json_search: Union[None, Unset, str]
    if isinstance(search, Unset):
        json_search = UNSET
    else:
        json_search = search
    params["search"] = json_search

    params["registrar"] = registrar

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/domains/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseDomainResponse]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseDomainResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseDomainResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    search: Union[None, Unset, str] = UNSET,
    registrar: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseDomainResponse]]:
    """List Entities

     List all entities with optional search and filtering.

            ## Search
            - **Available search fields**: name
            - Use the 'search' parameter to search across these fields

            ## Filtering
            - **Available filter fields**: registrar
            - Add query parameters matching these field names to filter results
            - Example: ?name=example&status=active

    Args:
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        search (Union[None, Unset, str]): Search term (searches in fields: name)
        registrar (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseDomainResponse]]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        search=search,
        registrar=registrar,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    search: Union[None, Unset, str] = UNSET,
    registrar: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseDomainResponse]]:
    """List Entities

     List all entities with optional search and filtering.

            ## Search
            - **Available search fields**: name
            - Use the 'search' parameter to search across these fields

            ## Filtering
            - **Available filter fields**: registrar
            - Add query parameters matching these field names to filter results
            - Example: ?name=example&status=active

    Args:
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        search (Union[None, Unset, str]): Search term (searches in fields: name)
        registrar (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseDomainResponse]
    """

    return sync_detailed(
        client=client,
        page=page,
        size=size,
        search=search,
        registrar=registrar,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    search: Union[None, Unset, str] = UNSET,
    registrar: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseDomainResponse]]:
    """List Entities

     List all entities with optional search and filtering.

            ## Search
            - **Available search fields**: name
            - Use the 'search' parameter to search across these fields

            ## Filtering
            - **Available filter fields**: registrar
            - Add query parameters matching these field names to filter results
            - Example: ?name=example&status=active

    Args:
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        search (Union[None, Unset, str]): Search term (searches in fields: name)
        registrar (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseDomainResponse]]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        search=search,
        registrar=registrar,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    size: Union[None, Unset, int] = UNSET,
    search: Union[None, Unset, str] = UNSET,
    registrar: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseDomainResponse]]:
    """List Entities

     List all entities with optional search and filtering.

            ## Search
            - **Available search fields**: name
            - Use the 'search' parameter to search across these fields

            ## Filtering
            - **Available filter fields**: registrar
            - Add query parameters matching these field names to filter results
            - Example: ?name=example&status=active

    Args:
        page (Union[Unset, int]): Page number Default: 1.
        size (Union[None, Unset, int]): Page size
        search (Union[None, Unset, str]): Search term (searches in fields: name)
        registrar (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseDomainResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            size=size,
            search=search,
            registrar=registrar,
        )
    ).parsed
