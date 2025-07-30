from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union

from pointr_cloud_common.dto.v8.base_dto import BaseDTO, BaseV8ResponseDTO
from pointr_cloud_common.dto.v8.validation import ValidationError, validate_required_field, validate_type, ensure_dict
from pointr_cloud_common.dto.v8.building_dto import GeometryPolygonModel

@dataclass
class SiteDTO(BaseDTO):
    fid: str
    name: str
    sid: Optional[str] = None
    eid: Optional[str] = None
    extraData: Dict[str, Any] = field(default_factory=dict)
    geometry: Optional[GeometryPolygonModel] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SiteDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SiteDTO")
        
        # Handle V8 API response format - extract from 'result' if present
        if "result" in data:
            data = data["result"]
        
        # Required fields
        site_internal_id = data.get("siteInternalIdentifier")
        if site_internal_id is None:
            raise ValidationError("Missing required field 'siteInternalIdentifier'", "siteInternalIdentifier", None)
        
        site_title = data.get("siteTitle")
        if not site_title:
            raise ValidationError("Missing required field 'siteTitle'", "siteTitle", None)
        
        # Optional fields
        site_external_id = data.get("siteExternalIdentifier")
        site_extra_data = ensure_dict(data.get("siteExtraData"), "siteExtraData")
        sid = str(site_internal_id)
        
        # Geometry
        geometry = None
        if "geometry" in data:
            geometry = GeometryPolygonModel.from_api_json(data["geometry"])
        
        return SiteDTO(
            fid=str(site_internal_id),
            name=site_title,
            sid=sid,
            eid=site_external_id,
            extraData=site_extra_data,
            geometry=geometry
        )

    def to_api_json(self) -> Dict[str, Any]:
        result = {
            "siteInternalIdentifier": int(self.fid),
            "siteTitle": self.name,
            "siteExtraData": self.extraData
        }
        
        if self.eid is not None:
            result["siteExternalIdentifier"] = self.eid
            
        if self.geometry is not None:
            result["geometry"] = self.geometry.to_api_json()
            
        if self.sid is not None:
            result["sid"] = self.sid
            
        return result
    
    def validate(self) -> bool:
        """Validate the DTO."""
        if not self.fid:
            raise ValidationError("fid cannot be empty", "fid", self.fid)
        if not self.name:
            raise ValidationError("name cannot be empty", "name", self.name)
        return True

    @staticmethod
    def list_from_api_json(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List["SiteDTO"]:
        if isinstance(data, list):
            return [SiteDTO.from_api_json(item) for item in data]
        
        # Handle V8 API response format
        if isinstance(data, dict):
            # Extract from 'results' field if present
            if "results" in data:
                results = data["results"]
                if isinstance(results, list):
                    return [SiteDTO.from_api_json(item) for item in results]
            
            # Handle FeatureCollection format
            if data.get("type") == "FeatureCollection" and "features" in data:
                return [SiteDTO.from_api_json(feature.get("properties", feature)) 
                       for feature in data["features"]]
            # Handle direct object format
            elif "items" in data and isinstance(data["items"], list):
                return [SiteDTO.from_api_json(item) for item in data["items"]]
        
        return []

@dataclass
class CreateSiteResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for site creation."""
    result: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "CreateSiteResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for CreateSiteResponseDTO")
        
        return CreateSiteResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            result=data.get("result")
        )

    def get_site(self) -> Optional[SiteDTO]:
        """Extract created site from the result."""
        if not self.result:
            return None
        return SiteDTO.from_api_json(self.result)

@dataclass
class SiteResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for single site."""
    result: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SiteResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SiteResponseDTO")
        
        return SiteResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            result=data.get("result")
        )

    def get_site(self) -> Optional[SiteDTO]:
        """Extract site from the result."""
        if not self.result:
            return None
        return SiteDTO.from_api_json(self.result)

@dataclass
class SitesResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for multiple sites."""
    results: Optional[List[Dict[str, Any]]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SitesResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SitesResponseDTO")
        
        return SitesResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            results=data.get("results")
        )

    def get_sites(self) -> List[SiteDTO]:
        """Extract sites from the results array."""
        if not self.results:
            return []
        return [SiteDTO.from_api_json(item) for item in self.results]
