import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.relationship_response_properties_type_0 import RelationshipResponsePropertiesType0


T = TypeVar("T", bound="RelationshipResponse")


@_attrs_define
class RelationshipResponse:
    """Schema for relationship response

    Attributes:
        name (str): Name of the relationship (typically the relationship type)
        source_type (str): Type of the source entity
        source_id (str): ID of the source entity
        target_type (str): Type of the target entity
        target_id (str): ID of the target entity
        type_ (str): Type of relationship
        properties (Union['RelationshipResponsePropertiesType0', None, Unset]): Custom properties for this relationship
        confidence (Union[None, Unset, int]): Confidence score (0-100) Default: 100.
        data_source (Union[None, Unset, str]): Source of this relationship information
        notes (Union[None, Unset, str]): Additional notes about this relationship
        id (Union[None, Unset, str]): Unique identifier for the relationship
        created_at (Union[None, Unset, datetime.datetime]): When the relationship was created
        updated_at (Union[None, Unset, datetime.datetime]): When the relationship was last updated
    """

    name: str
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    type_: str
    properties: Union["RelationshipResponsePropertiesType0", None, Unset] = UNSET
    confidence: Union[None, Unset, int] = 100
    data_source: Union[None, Unset, str] = UNSET
    notes: Union[None, Unset, str] = UNSET
    id: Union[None, Unset, str] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.relationship_response_properties_type_0 import RelationshipResponsePropertiesType0

        name = self.name

        source_type = self.source_type

        source_id = self.source_id

        target_type = self.target_type

        target_id = self.target_id

        type_ = self.type_

        properties: Union[None, Unset, dict[str, Any]]
        if isinstance(self.properties, Unset):
            properties = UNSET
        elif isinstance(self.properties, RelationshipResponsePropertiesType0):
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

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "source_type": source_type,
                "source_id": source_id,
                "target_type": target_type,
                "target_id": target_id,
                "type": type_,
            }
        )
        if properties is not UNSET:
            field_dict["properties"] = properties
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if notes is not UNSET:
            field_dict["notes"] = notes
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relationship_response_properties_type_0 import RelationshipResponsePropertiesType0

        d = dict(src_dict)
        name = d.pop("name")

        source_type = d.pop("source_type")

        source_id = d.pop("source_id")

        target_type = d.pop("target_type")

        target_id = d.pop("target_id")

        type_ = d.pop("type")

        def _parse_properties(data: object) -> Union["RelationshipResponsePropertiesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_0 = RelationshipResponsePropertiesType0.from_dict(data)

                return properties_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RelationshipResponsePropertiesType0", None, Unset], data)

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

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        relationship_response = cls(
            name=name,
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            type_=type_,
            properties=properties,
            confidence=confidence,
            data_source=data_source,
            notes=notes,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        relationship_response.additional_properties = d
        return relationship_response

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
