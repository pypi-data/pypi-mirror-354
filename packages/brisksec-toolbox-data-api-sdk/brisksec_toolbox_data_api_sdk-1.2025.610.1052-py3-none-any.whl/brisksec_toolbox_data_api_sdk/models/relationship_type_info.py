from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RelationshipTypeInfo")


@_attrs_define
class RelationshipTypeInfo:
    """Schema for relationship type information

    Attributes:
        type_ (str):
        valid_sources (list[str]):
        valid_targets (list[str]):
        properties (list[str]):
        description (str):
    """

    type_: str
    valid_sources: list[str]
    valid_targets: list[str]
    properties: list[str]
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        valid_sources = self.valid_sources

        valid_targets = self.valid_targets

        properties = self.properties

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "valid_sources": valid_sources,
                "valid_targets": valid_targets,
                "properties": properties,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        valid_sources = cast(list[str], d.pop("valid_sources"))

        valid_targets = cast(list[str], d.pop("valid_targets"))

        properties = cast(list[str], d.pop("properties"))

        description = d.pop("description")

        relationship_type_info = cls(
            type_=type_,
            valid_sources=valid_sources,
            valid_targets=valid_targets,
            properties=properties,
            description=description,
        )

        relationship_type_info.additional_properties = d
        return relationship_type_info

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
