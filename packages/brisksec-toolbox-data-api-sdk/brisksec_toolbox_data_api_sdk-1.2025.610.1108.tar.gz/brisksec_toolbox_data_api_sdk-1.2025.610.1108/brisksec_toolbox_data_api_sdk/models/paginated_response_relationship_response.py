from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relationship_response import RelationshipResponse


T = TypeVar("T", bound="PaginatedResponseRelationshipResponse")


@_attrs_define
class PaginatedResponseRelationshipResponse:
    """
    Attributes:
        items (list['RelationshipResponse']): List of items in the current page
        total (int): Total number of items across all pages
        page (int): Current page number (1-based)
        size (int): Number of items per page
    """

    items: list["RelationshipResponse"]
    total: int
    page: int
    size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        total = self.total

        page = self.page

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "total": total,
                "page": page,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relationship_response import RelationshipResponse

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RelationshipResponse.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        page = d.pop("page")

        size = d.pop("size")

        paginated_response_relationship_response = cls(
            items=items,
            total=total,
            page=page,
            size=size,
        )

        paginated_response_relationship_response.additional_properties = d
        return paginated_response_relationship_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
