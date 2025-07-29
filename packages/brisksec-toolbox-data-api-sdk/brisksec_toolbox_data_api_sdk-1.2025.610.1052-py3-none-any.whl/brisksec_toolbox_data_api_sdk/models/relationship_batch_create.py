from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relationship_create import RelationshipCreate


T = TypeVar("T", bound="RelationshipBatchCreate")


@_attrs_define
class RelationshipBatchCreate:
    """Schema for creating multiple relationships in a batch

    Attributes:
        relationships (list['RelationshipCreate']):
    """

    relationships: list["RelationshipCreate"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        relationships = []
        for relationships_item_data in self.relationships:
            relationships_item = relationships_item_data.to_dict()
            relationships.append(relationships_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "relationships": relationships,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relationship_create import RelationshipCreate

        d = dict(src_dict)
        relationships = []
        _relationships = d.pop("relationships")
        for relationships_item_data in _relationships:
            relationships_item = RelationshipCreate.from_dict(relationships_item_data)

            relationships.append(relationships_item)

        relationship_batch_create = cls(
            relationships=relationships,
        )

        relationship_batch_create.additional_properties = d
        return relationship_batch_create

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
