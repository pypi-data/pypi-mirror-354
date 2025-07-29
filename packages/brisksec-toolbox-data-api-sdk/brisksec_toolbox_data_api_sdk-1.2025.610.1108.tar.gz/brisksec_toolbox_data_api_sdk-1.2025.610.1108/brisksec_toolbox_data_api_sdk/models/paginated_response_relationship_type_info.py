from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relationship_type_info import RelationshipTypeInfo


T = TypeVar("T", bound="PaginatedResponseRelationshipTypeInfo")


@_attrs_define
class PaginatedResponseRelationshipTypeInfo:
    """
    Attributes:
        items (list['RelationshipTypeInfo']): List of items in the current page
        total (int): Total number of items across all pages
        page (int): Current page number (1-based)
        size (int): Number of items per page
    """

    items: list["RelationshipTypeInfo"]
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
        from ..models.relationship_type_info import RelationshipTypeInfo

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RelationshipTypeInfo.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        page = d.pop("page")

        size = d.pop("size")

        paginated_response_relationship_type_info = cls(
            items=items,
            total=total,
            page=page,
            size=size,
        )

        paginated_response_relationship_type_info.additional_properties = d
        return paginated_response_relationship_type_info

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
