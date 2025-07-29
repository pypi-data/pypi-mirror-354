import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.domain_update_business_criticality import DomainUpdateBusinessCriticality
from ..models.domain_update_category import DomainUpdateCategory
from ..models.domain_update_classification import DomainUpdateClassification
from ..models.domain_update_domain_status import DomainUpdateDomainStatus
from ..models.domain_update_environment import DomainUpdateEnvironment
from ..models.domain_update_lifecycle_stage import DomainUpdateLifecycleStage
from ..models.domain_update_sensitivity import DomainUpdateSensitivity
from ..models.domain_update_status import DomainUpdateStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.domain_update_geographic_location import DomainUpdateGeographicLocation
    from ..models.domain_update_labels import DomainUpdateLabels


T = TypeVar("T", bound="DomainUpdate")


@_attrs_define
class DomainUpdate:
    """Schema for updating domain fields (all optional for partial updates)

    Attributes:
        registrar (Union[None, Unset, str]): Domain registrar company
        expiration_date (Union[None, Unset, datetime.datetime]): Domain expiration date
        domain_status (Union[Unset, DomainUpdateDomainStatus]): Current status of the domain Default:
            DomainUpdateDomainStatus.ACTIVE.
        nameservers (Union[Unset, list[str]]): List of nameservers for this domain
        classification (Union[Unset, DomainUpdateClassification]): Classification level of the asset Default:
            DomainUpdateClassification.UNKNOWN.
        sensitivity (Union[Unset, DomainUpdateSensitivity]): Sensitivity level of the asset Default:
            DomainUpdateSensitivity.UNKNOWN.
        category (Union[Unset, DomainUpdateCategory]): Category of the asset Default: DomainUpdateCategory.UNKNOWN.
        tags (Union[Unset, list[str]]): List of tags for categorizing the asset
        labels (Union[Unset, DomainUpdateLabels]): Key-value pairs for additional metadata
        owner (Union[None, Unset, str]): Primary owner of the asset
        owner_department (Union[None, Unset, str]): Department that owns the asset
        custodian (Union[None, Unset, str]): Person or team responsible for maintaining the asset
        business_unit (Union[None, Unset, str]): Business unit associated with the asset
        cost_center (Union[None, Unset, str]): Cost center for financial tracking
        status (Union[Unset, DomainUpdateStatus]): Current status of the asset Default: DomainUpdateStatus.UNKNOWN.
        lifecycle_stage (Union[Unset, DomainUpdateLifecycleStage]): Current lifecycle stage of the asset Default:
            DomainUpdateLifecycleStage.UNKNOWN.
        creation_date (Union[None, Unset, datetime.datetime]): Date when the asset was created
        last_review_date (Union[None, Unset, datetime.datetime]): Date when the asset was last reviewed
        next_review_date (Union[None, Unset, datetime.datetime]): Scheduled date for next review
        retirement_date (Union[None, Unset, datetime.datetime]): Planned retirement date for the asset
        purpose (Union[None, Unset, str]): Purpose or function of the asset
        environment (Union[Unset, DomainUpdateEnvironment]): Environment where the asset is deployed Default:
            DomainUpdateEnvironment.UNKNOWN.
        business_criticality (Union[Unset, DomainUpdateBusinessCriticality]): How critical the asset is to business
            operations Default: DomainUpdateBusinessCriticality.UNKNOWN.
        notes (Union[None, Unset, str]): Additional notes about the asset
        public_facing (Union[None, Unset, bool]):  Default: False.
        external_access_points (Union[Unset, list[str]]):
        discovery_sources (Union[Unset, list[str]]):
        geographic_location (Union[Unset, DomainUpdateGeographicLocation]):
        jurisdiction (Union[None, Unset, str]):
        technology_fingerprint (Union[Unset, list[str]]):
        external_references (Union[Unset, list[str]]):
        social_media_presence (Union[Unset, list[str]]):
        third_party_dependencies (Union[Unset, list[str]]):
        vendor_relationships (Union[Unset, list[str]]):
        supply_chain_risk_level (Union[None, Unset, str]):  Default: 'unknown'.
        threat_exposure_level (Union[None, Unset, str]):  Default: 'unknown'.
        intelligence_sources (Union[Unset, list[str]]):
        observable_indicators (Union[Unset, list[str]]):
        monitoring_frequency (Union[None, Unset, str]):  Default: 'daily'.
        last_osint_scan (Union[None, Unset, datetime.datetime]):
        intelligence_priority (Union[None, Unset, str]):  Default: 'medium'.
        known_threat_actors (Union[Unset, list[str]]):
        attack_surface_score (Union[None, Unset, float]):  Default: 0.0.
        external_exposure_score (Union[None, Unset, float]):  Default: 0.0.
        source (Union[None, Unset, str]):
        confidence (Union[None, Unset, float]):
        name (Union[None, Unset, str]):
    """

    registrar: Union[None, Unset, str] = UNSET
    expiration_date: Union[None, Unset, datetime.datetime] = UNSET
    domain_status: Union[Unset, DomainUpdateDomainStatus] = DomainUpdateDomainStatus.ACTIVE
    nameservers: Union[Unset, list[str]] = UNSET
    classification: Union[Unset, DomainUpdateClassification] = DomainUpdateClassification.UNKNOWN
    sensitivity: Union[Unset, DomainUpdateSensitivity] = DomainUpdateSensitivity.UNKNOWN
    category: Union[Unset, DomainUpdateCategory] = DomainUpdateCategory.UNKNOWN
    tags: Union[Unset, list[str]] = UNSET
    labels: Union[Unset, "DomainUpdateLabels"] = UNSET
    owner: Union[None, Unset, str] = UNSET
    owner_department: Union[None, Unset, str] = UNSET
    custodian: Union[None, Unset, str] = UNSET
    business_unit: Union[None, Unset, str] = UNSET
    cost_center: Union[None, Unset, str] = UNSET
    status: Union[Unset, DomainUpdateStatus] = DomainUpdateStatus.UNKNOWN
    lifecycle_stage: Union[Unset, DomainUpdateLifecycleStage] = DomainUpdateLifecycleStage.UNKNOWN
    creation_date: Union[None, Unset, datetime.datetime] = UNSET
    last_review_date: Union[None, Unset, datetime.datetime] = UNSET
    next_review_date: Union[None, Unset, datetime.datetime] = UNSET
    retirement_date: Union[None, Unset, datetime.datetime] = UNSET
    purpose: Union[None, Unset, str] = UNSET
    environment: Union[Unset, DomainUpdateEnvironment] = DomainUpdateEnvironment.UNKNOWN
    business_criticality: Union[Unset, DomainUpdateBusinessCriticality] = DomainUpdateBusinessCriticality.UNKNOWN
    notes: Union[None, Unset, str] = UNSET
    public_facing: Union[None, Unset, bool] = False
    external_access_points: Union[Unset, list[str]] = UNSET
    discovery_sources: Union[Unset, list[str]] = UNSET
    geographic_location: Union[Unset, "DomainUpdateGeographicLocation"] = UNSET
    jurisdiction: Union[None, Unset, str] = UNSET
    technology_fingerprint: Union[Unset, list[str]] = UNSET
    external_references: Union[Unset, list[str]] = UNSET
    social_media_presence: Union[Unset, list[str]] = UNSET
    third_party_dependencies: Union[Unset, list[str]] = UNSET
    vendor_relationships: Union[Unset, list[str]] = UNSET
    supply_chain_risk_level: Union[None, Unset, str] = "unknown"
    threat_exposure_level: Union[None, Unset, str] = "unknown"
    intelligence_sources: Union[Unset, list[str]] = UNSET
    observable_indicators: Union[Unset, list[str]] = UNSET
    monitoring_frequency: Union[None, Unset, str] = "daily"
    last_osint_scan: Union[None, Unset, datetime.datetime] = UNSET
    intelligence_priority: Union[None, Unset, str] = "medium"
    known_threat_actors: Union[Unset, list[str]] = UNSET
    attack_surface_score: Union[None, Unset, float] = 0.0
    external_exposure_score: Union[None, Unset, float] = 0.0
    source: Union[None, Unset, str] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        registrar: Union[None, Unset, str]
        if isinstance(self.registrar, Unset):
            registrar = UNSET
        else:
            registrar = self.registrar

        expiration_date: Union[None, Unset, str]
        if isinstance(self.expiration_date, Unset):
            expiration_date = UNSET
        elif isinstance(self.expiration_date, datetime.datetime):
            expiration_date = self.expiration_date.isoformat()
        else:
            expiration_date = self.expiration_date

        domain_status: Union[Unset, str] = UNSET
        if not isinstance(self.domain_status, Unset):
            domain_status = self.domain_status.value

        nameservers: Union[Unset, list[str]] = UNSET
        if not isinstance(self.nameservers, Unset):
            nameservers = self.nameservers

        classification: Union[Unset, str] = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification.value

        sensitivity: Union[Unset, str] = UNSET
        if not isinstance(self.sensitivity, Unset):
            sensitivity = self.sensitivity.value

        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        labels: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        owner: Union[None, Unset, str]
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        owner_department: Union[None, Unset, str]
        if isinstance(self.owner_department, Unset):
            owner_department = UNSET
        else:
            owner_department = self.owner_department

        custodian: Union[None, Unset, str]
        if isinstance(self.custodian, Unset):
            custodian = UNSET
        else:
            custodian = self.custodian

        business_unit: Union[None, Unset, str]
        if isinstance(self.business_unit, Unset):
            business_unit = UNSET
        else:
            business_unit = self.business_unit

        cost_center: Union[None, Unset, str]
        if isinstance(self.cost_center, Unset):
            cost_center = UNSET
        else:
            cost_center = self.cost_center

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        lifecycle_stage: Union[Unset, str] = UNSET
        if not isinstance(self.lifecycle_stage, Unset):
            lifecycle_stage = self.lifecycle_stage.value

        creation_date: Union[None, Unset, str]
        if isinstance(self.creation_date, Unset):
            creation_date = UNSET
        elif isinstance(self.creation_date, datetime.datetime):
            creation_date = self.creation_date.isoformat()
        else:
            creation_date = self.creation_date

        last_review_date: Union[None, Unset, str]
        if isinstance(self.last_review_date, Unset):
            last_review_date = UNSET
        elif isinstance(self.last_review_date, datetime.datetime):
            last_review_date = self.last_review_date.isoformat()
        else:
            last_review_date = self.last_review_date

        next_review_date: Union[None, Unset, str]
        if isinstance(self.next_review_date, Unset):
            next_review_date = UNSET
        elif isinstance(self.next_review_date, datetime.datetime):
            next_review_date = self.next_review_date.isoformat()
        else:
            next_review_date = self.next_review_date

        retirement_date: Union[None, Unset, str]
        if isinstance(self.retirement_date, Unset):
            retirement_date = UNSET
        elif isinstance(self.retirement_date, datetime.datetime):
            retirement_date = self.retirement_date.isoformat()
        else:
            retirement_date = self.retirement_date

        purpose: Union[None, Unset, str]
        if isinstance(self.purpose, Unset):
            purpose = UNSET
        else:
            purpose = self.purpose

        environment: Union[Unset, str] = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.value

        business_criticality: Union[Unset, str] = UNSET
        if not isinstance(self.business_criticality, Unset):
            business_criticality = self.business_criticality.value

        notes: Union[None, Unset, str]
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        public_facing: Union[None, Unset, bool]
        if isinstance(self.public_facing, Unset):
            public_facing = UNSET
        else:
            public_facing = self.public_facing

        external_access_points: Union[Unset, list[str]] = UNSET
        if not isinstance(self.external_access_points, Unset):
            external_access_points = self.external_access_points

        discovery_sources: Union[Unset, list[str]] = UNSET
        if not isinstance(self.discovery_sources, Unset):
            discovery_sources = self.discovery_sources

        geographic_location: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.geographic_location, Unset):
            geographic_location = self.geographic_location.to_dict()

        jurisdiction: Union[None, Unset, str]
        if isinstance(self.jurisdiction, Unset):
            jurisdiction = UNSET
        else:
            jurisdiction = self.jurisdiction

        technology_fingerprint: Union[Unset, list[str]] = UNSET
        if not isinstance(self.technology_fingerprint, Unset):
            technology_fingerprint = self.technology_fingerprint

        external_references: Union[Unset, list[str]] = UNSET
        if not isinstance(self.external_references, Unset):
            external_references = self.external_references

        social_media_presence: Union[Unset, list[str]] = UNSET
        if not isinstance(self.social_media_presence, Unset):
            social_media_presence = self.social_media_presence

        third_party_dependencies: Union[Unset, list[str]] = UNSET
        if not isinstance(self.third_party_dependencies, Unset):
            third_party_dependencies = self.third_party_dependencies

        vendor_relationships: Union[Unset, list[str]] = UNSET
        if not isinstance(self.vendor_relationships, Unset):
            vendor_relationships = self.vendor_relationships

        supply_chain_risk_level: Union[None, Unset, str]
        if isinstance(self.supply_chain_risk_level, Unset):
            supply_chain_risk_level = UNSET
        else:
            supply_chain_risk_level = self.supply_chain_risk_level

        threat_exposure_level: Union[None, Unset, str]
        if isinstance(self.threat_exposure_level, Unset):
            threat_exposure_level = UNSET
        else:
            threat_exposure_level = self.threat_exposure_level

        intelligence_sources: Union[Unset, list[str]] = UNSET
        if not isinstance(self.intelligence_sources, Unset):
            intelligence_sources = self.intelligence_sources

        observable_indicators: Union[Unset, list[str]] = UNSET
        if not isinstance(self.observable_indicators, Unset):
            observable_indicators = self.observable_indicators

        monitoring_frequency: Union[None, Unset, str]
        if isinstance(self.monitoring_frequency, Unset):
            monitoring_frequency = UNSET
        else:
            monitoring_frequency = self.monitoring_frequency

        last_osint_scan: Union[None, Unset, str]
        if isinstance(self.last_osint_scan, Unset):
            last_osint_scan = UNSET
        elif isinstance(self.last_osint_scan, datetime.datetime):
            last_osint_scan = self.last_osint_scan.isoformat()
        else:
            last_osint_scan = self.last_osint_scan

        intelligence_priority: Union[None, Unset, str]
        if isinstance(self.intelligence_priority, Unset):
            intelligence_priority = UNSET
        else:
            intelligence_priority = self.intelligence_priority

        known_threat_actors: Union[Unset, list[str]] = UNSET
        if not isinstance(self.known_threat_actors, Unset):
            known_threat_actors = self.known_threat_actors

        attack_surface_score: Union[None, Unset, float]
        if isinstance(self.attack_surface_score, Unset):
            attack_surface_score = UNSET
        else:
            attack_surface_score = self.attack_surface_score

        external_exposure_score: Union[None, Unset, float]
        if isinstance(self.external_exposure_score, Unset):
            external_exposure_score = UNSET
        else:
            external_exposure_score = self.external_exposure_score

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if registrar is not UNSET:
            field_dict["registrar"] = registrar
        if expiration_date is not UNSET:
            field_dict["expiration_date"] = expiration_date
        if domain_status is not UNSET:
            field_dict["domain_status"] = domain_status
        if nameservers is not UNSET:
            field_dict["nameservers"] = nameservers
        if classification is not UNSET:
            field_dict["classification"] = classification
        if sensitivity is not UNSET:
            field_dict["sensitivity"] = sensitivity
        if category is not UNSET:
            field_dict["category"] = category
        if tags is not UNSET:
            field_dict["tags"] = tags
        if labels is not UNSET:
            field_dict["labels"] = labels
        if owner is not UNSET:
            field_dict["owner"] = owner
        if owner_department is not UNSET:
            field_dict["owner_department"] = owner_department
        if custodian is not UNSET:
            field_dict["custodian"] = custodian
        if business_unit is not UNSET:
            field_dict["business_unit"] = business_unit
        if cost_center is not UNSET:
            field_dict["cost_center"] = cost_center
        if status is not UNSET:
            field_dict["status"] = status
        if lifecycle_stage is not UNSET:
            field_dict["lifecycle_stage"] = lifecycle_stage
        if creation_date is not UNSET:
            field_dict["creation_date"] = creation_date
        if last_review_date is not UNSET:
            field_dict["last_review_date"] = last_review_date
        if next_review_date is not UNSET:
            field_dict["next_review_date"] = next_review_date
        if retirement_date is not UNSET:
            field_dict["retirement_date"] = retirement_date
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if environment is not UNSET:
            field_dict["environment"] = environment
        if business_criticality is not UNSET:
            field_dict["business_criticality"] = business_criticality
        if notes is not UNSET:
            field_dict["notes"] = notes
        if public_facing is not UNSET:
            field_dict["public_facing"] = public_facing
        if external_access_points is not UNSET:
            field_dict["external_access_points"] = external_access_points
        if discovery_sources is not UNSET:
            field_dict["discovery_sources"] = discovery_sources
        if geographic_location is not UNSET:
            field_dict["geographic_location"] = geographic_location
        if jurisdiction is not UNSET:
            field_dict["jurisdiction"] = jurisdiction
        if technology_fingerprint is not UNSET:
            field_dict["technology_fingerprint"] = technology_fingerprint
        if external_references is not UNSET:
            field_dict["external_references"] = external_references
        if social_media_presence is not UNSET:
            field_dict["social_media_presence"] = social_media_presence
        if third_party_dependencies is not UNSET:
            field_dict["third_party_dependencies"] = third_party_dependencies
        if vendor_relationships is not UNSET:
            field_dict["vendor_relationships"] = vendor_relationships
        if supply_chain_risk_level is not UNSET:
            field_dict["supply_chain_risk_level"] = supply_chain_risk_level
        if threat_exposure_level is not UNSET:
            field_dict["threat_exposure_level"] = threat_exposure_level
        if intelligence_sources is not UNSET:
            field_dict["intelligence_sources"] = intelligence_sources
        if observable_indicators is not UNSET:
            field_dict["observable_indicators"] = observable_indicators
        if monitoring_frequency is not UNSET:
            field_dict["monitoring_frequency"] = monitoring_frequency
        if last_osint_scan is not UNSET:
            field_dict["last_osint_scan"] = last_osint_scan
        if intelligence_priority is not UNSET:
            field_dict["intelligence_priority"] = intelligence_priority
        if known_threat_actors is not UNSET:
            field_dict["known_threat_actors"] = known_threat_actors
        if attack_surface_score is not UNSET:
            field_dict["attack_surface_score"] = attack_surface_score
        if external_exposure_score is not UNSET:
            field_dict["external_exposure_score"] = external_exposure_score
        if source is not UNSET:
            field_dict["source"] = source
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.domain_update_geographic_location import DomainUpdateGeographicLocation
        from ..models.domain_update_labels import DomainUpdateLabels

        d = dict(src_dict)

        def _parse_registrar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        registrar = _parse_registrar(d.pop("registrar", UNSET))

        def _parse_expiration_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_date_type_0 = isoparse(data)

                return expiration_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expiration_date = _parse_expiration_date(d.pop("expiration_date", UNSET))

        _domain_status = d.pop("domain_status", UNSET)
        domain_status: Union[Unset, DomainUpdateDomainStatus]
        if isinstance(_domain_status, Unset):
            domain_status = UNSET
        else:
            domain_status = DomainUpdateDomainStatus(_domain_status)

        nameservers = cast(list[str], d.pop("nameservers", UNSET))

        _classification = d.pop("classification", UNSET)
        classification: Union[Unset, DomainUpdateClassification]
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = DomainUpdateClassification(_classification)

        _sensitivity = d.pop("sensitivity", UNSET)
        sensitivity: Union[Unset, DomainUpdateSensitivity]
        if isinstance(_sensitivity, Unset):
            sensitivity = UNSET
        else:
            sensitivity = DomainUpdateSensitivity(_sensitivity)

        _category = d.pop("category", UNSET)
        category: Union[Unset, DomainUpdateCategory]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = DomainUpdateCategory(_category)

        tags = cast(list[str], d.pop("tags", UNSET))

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, DomainUpdateLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = DomainUpdateLabels.from_dict(_labels)

        def _parse_owner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_owner_department(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner_department = _parse_owner_department(d.pop("owner_department", UNSET))

        def _parse_custodian(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        custodian = _parse_custodian(d.pop("custodian", UNSET))

        def _parse_business_unit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        business_unit = _parse_business_unit(d.pop("business_unit", UNSET))

        def _parse_cost_center(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cost_center = _parse_cost_center(d.pop("cost_center", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, DomainUpdateStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DomainUpdateStatus(_status)

        _lifecycle_stage = d.pop("lifecycle_stage", UNSET)
        lifecycle_stage: Union[Unset, DomainUpdateLifecycleStage]
        if isinstance(_lifecycle_stage, Unset):
            lifecycle_stage = UNSET
        else:
            lifecycle_stage = DomainUpdateLifecycleStage(_lifecycle_stage)

        def _parse_creation_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                creation_date_type_0 = isoparse(data)

                return creation_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        creation_date = _parse_creation_date(d.pop("creation_date", UNSET))

        def _parse_last_review_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_review_date_type_0 = isoparse(data)

                return last_review_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_review_date = _parse_last_review_date(d.pop("last_review_date", UNSET))

        def _parse_next_review_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_review_date_type_0 = isoparse(data)

                return next_review_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        next_review_date = _parse_next_review_date(d.pop("next_review_date", UNSET))

        def _parse_retirement_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                retirement_date_type_0 = isoparse(data)

                return retirement_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        retirement_date = _parse_retirement_date(d.pop("retirement_date", UNSET))

        def _parse_purpose(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        purpose = _parse_purpose(d.pop("purpose", UNSET))

        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, DomainUpdateEnvironment]
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = DomainUpdateEnvironment(_environment)

        _business_criticality = d.pop("business_criticality", UNSET)
        business_criticality: Union[Unset, DomainUpdateBusinessCriticality]
        if isinstance(_business_criticality, Unset):
            business_criticality = UNSET
        else:
            business_criticality = DomainUpdateBusinessCriticality(_business_criticality)

        def _parse_notes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_public_facing(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        public_facing = _parse_public_facing(d.pop("public_facing", UNSET))

        external_access_points = cast(list[str], d.pop("external_access_points", UNSET))

        discovery_sources = cast(list[str], d.pop("discovery_sources", UNSET))

        _geographic_location = d.pop("geographic_location", UNSET)
        geographic_location: Union[Unset, DomainUpdateGeographicLocation]
        if isinstance(_geographic_location, Unset):
            geographic_location = UNSET
        else:
            geographic_location = DomainUpdateGeographicLocation.from_dict(_geographic_location)

        def _parse_jurisdiction(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        jurisdiction = _parse_jurisdiction(d.pop("jurisdiction", UNSET))

        technology_fingerprint = cast(list[str], d.pop("technology_fingerprint", UNSET))

        external_references = cast(list[str], d.pop("external_references", UNSET))

        social_media_presence = cast(list[str], d.pop("social_media_presence", UNSET))

        third_party_dependencies = cast(list[str], d.pop("third_party_dependencies", UNSET))

        vendor_relationships = cast(list[str], d.pop("vendor_relationships", UNSET))

        def _parse_supply_chain_risk_level(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        supply_chain_risk_level = _parse_supply_chain_risk_level(d.pop("supply_chain_risk_level", UNSET))

        def _parse_threat_exposure_level(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        threat_exposure_level = _parse_threat_exposure_level(d.pop("threat_exposure_level", UNSET))

        intelligence_sources = cast(list[str], d.pop("intelligence_sources", UNSET))

        observable_indicators = cast(list[str], d.pop("observable_indicators", UNSET))

        def _parse_monitoring_frequency(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        monitoring_frequency = _parse_monitoring_frequency(d.pop("monitoring_frequency", UNSET))

        def _parse_last_osint_scan(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_osint_scan_type_0 = isoparse(data)

                return last_osint_scan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_osint_scan = _parse_last_osint_scan(d.pop("last_osint_scan", UNSET))

        def _parse_intelligence_priority(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        intelligence_priority = _parse_intelligence_priority(d.pop("intelligence_priority", UNSET))

        known_threat_actors = cast(list[str], d.pop("known_threat_actors", UNSET))

        def _parse_attack_surface_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        attack_surface_score = _parse_attack_surface_score(d.pop("attack_surface_score", UNSET))

        def _parse_external_exposure_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        external_exposure_score = _parse_external_exposure_score(d.pop("external_exposure_score", UNSET))

        def _parse_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        domain_update = cls(
            registrar=registrar,
            expiration_date=expiration_date,
            domain_status=domain_status,
            nameservers=nameservers,
            classification=classification,
            sensitivity=sensitivity,
            category=category,
            tags=tags,
            labels=labels,
            owner=owner,
            owner_department=owner_department,
            custodian=custodian,
            business_unit=business_unit,
            cost_center=cost_center,
            status=status,
            lifecycle_stage=lifecycle_stage,
            creation_date=creation_date,
            last_review_date=last_review_date,
            next_review_date=next_review_date,
            retirement_date=retirement_date,
            purpose=purpose,
            environment=environment,
            business_criticality=business_criticality,
            notes=notes,
            public_facing=public_facing,
            external_access_points=external_access_points,
            discovery_sources=discovery_sources,
            geographic_location=geographic_location,
            jurisdiction=jurisdiction,
            technology_fingerprint=technology_fingerprint,
            external_references=external_references,
            social_media_presence=social_media_presence,
            third_party_dependencies=third_party_dependencies,
            vendor_relationships=vendor_relationships,
            supply_chain_risk_level=supply_chain_risk_level,
            threat_exposure_level=threat_exposure_level,
            intelligence_sources=intelligence_sources,
            observable_indicators=observable_indicators,
            monitoring_frequency=monitoring_frequency,
            last_osint_scan=last_osint_scan,
            intelligence_priority=intelligence_priority,
            known_threat_actors=known_threat_actors,
            attack_surface_score=attack_surface_score,
            external_exposure_score=external_exposure_score,
            source=source,
            confidence=confidence,
            name=name,
        )

        domain_update.additional_properties = d
        return domain_update

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
