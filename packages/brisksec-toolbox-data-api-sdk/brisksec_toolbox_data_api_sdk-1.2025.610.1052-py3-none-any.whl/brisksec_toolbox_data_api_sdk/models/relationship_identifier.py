from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RelationshipIdentifier")


@_attrs_define
class RelationshipIdentifier:
    """Schema for identifying a relationship

    Attributes:
        source_type (str): Type of the source entity (e.g., 'Organization')
        source_id (str): ID of the source entity
        target_type (str): Type of the target entity (e.g., 'Domain')
        target_id (str): ID of the target entity
        type_ (str): Type of relationship (e.g., 'OWNS', 'RESOLVES_TO')
    """

    source_type: str
    source_id: str
    target_type: str
    target_id: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_type = self.source_type

        source_id = self.source_id

        target_type = self.target_type

        target_id = self.target_id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_type": source_type,
                "source_id": source_id,
                "target_type": target_type,
                "target_id": target_id,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_type = d.pop("source_type")

        source_id = d.pop("source_id")

        target_type = d.pop("target_type")

        target_id = d.pop("target_id")

        type_ = d.pop("type")

        relationship_identifier = cls(
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            type_=type_,
        )

        relationship_identifier.additional_properties = d
        return relationship_identifier

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
