from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.relationship_update_properties_type_0 import RelationshipUpdatePropertiesType0


T = TypeVar("T", bound="RelationshipUpdate")


@_attrs_define
class RelationshipUpdate:
    """Schema for updating an existing relationship

    Attributes:
        properties (Union['RelationshipUpdatePropertiesType0', None, Unset]): Custom properties for this relationship
        confidence (Union[None, Unset, int]): Confidence score (0-100) Default: 100.
        data_source (Union[None, Unset, str]): Source of this relationship information
        notes (Union[None, Unset, str]): Additional notes about this relationship
    """

    properties: Union["RelationshipUpdatePropertiesType0", None, Unset] = UNSET
    confidence: Union[None, Unset, int] = 100
    data_source: Union[None, Unset, str] = UNSET
    notes: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.relationship_update_properties_type_0 import RelationshipUpdatePropertiesType0

        properties: Union[None, Unset, dict[str, Any]]
        if isinstance(self.properties, Unset):
            properties = UNSET
        elif isinstance(self.properties, RelationshipUpdatePropertiesType0):
            properties = self.properties.to_dict()
        else:
            properties = self.properties

        confidence: Union[None, Unset, int]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        data_source: Union[None, Unset, str]
        if isinstance(self.data_source, Unset):
            data_source = UNSET
        else:
            data_source = self.data_source

        notes: Union[None, Unset, str]
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if properties is not UNSET:
            field_dict["properties"] = properties
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relationship_update_properties_type_0 import RelationshipUpdatePropertiesType0

        d = dict(src_dict)

        def _parse_properties(data: object) -> Union["RelationshipUpdatePropertiesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_0 = RelationshipUpdatePropertiesType0.from_dict(data)

                return properties_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RelationshipUpdatePropertiesType0", None, Unset], data)

        properties = _parse_properties(d.pop("properties", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_data_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        data_source = _parse_data_source(d.pop("data_source", UNSET))

        def _parse_notes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        notes = _parse_notes(d.pop("notes", UNSET))

        relationship_update = cls(
            properties=properties,
            confidence=confidence,
            data_source=data_source,
            notes=notes,
        )

        relationship_update.additional_properties = d
        return relationship_update

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
