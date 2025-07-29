from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relationship_identifier import RelationshipIdentifier
    from ..models.relationship_update import RelationshipUpdate


T = TypeVar("T", bound="BodyUpdateRelationship")


@_attrs_define
class BodyUpdateRelationship:
    """
    Attributes:
        rel_identifier (RelationshipIdentifier): Schema for identifying a relationship
        relationship_data (RelationshipUpdate): Schema for updating an existing relationship
    """

    rel_identifier: "RelationshipIdentifier"
    relationship_data: "RelationshipUpdate"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rel_identifier = self.rel_identifier.to_dict()

        relationship_data = self.relationship_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rel_identifier": rel_identifier,
                "relationship_data": relationship_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relationship_identifier import RelationshipIdentifier
        from ..models.relationship_update import RelationshipUpdate

        d = dict(src_dict)
        rel_identifier = RelationshipIdentifier.from_dict(d.pop("rel_identifier"))

        relationship_data = RelationshipUpdate.from_dict(d.pop("relationship_data"))

        body_update_relationship = cls(
            rel_identifier=rel_identifier,
            relationship_data=relationship_data,
        )

        body_update_relationship.additional_properties = d
        return body_update_relationship

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
