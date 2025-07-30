from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union

from pointr_cloud_common.dto.v8.base_dto import BaseDTO, BaseV8ResponseDTO
from pointr_cloud_common.dto.v8.validation import ValidationError, validate_required_field, validate_type, ensure_dict

@dataclass
class GeometryPolygonModel:
    """GeoJSON Polygon geometry model."""
    type: str = "Polygon"
    coordinates: List[List[List[float]]] = field(default_factory=list)

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "GeometryPolygonModel":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for GeometryPolygonModel")
        
        if data.get("type") != "Polygon":
            raise ValidationError("Expected type 'Polygon'", "type", data.get("type"))
        
        coordinates = data.get("coordinates")
        if not isinstance(coordinates, list):
            raise ValidationError("Expected list for coordinates", "coordinates", coordinates)
        
        return GeometryPolygonModel(
            type="Polygon",
            coordinates=coordinates
        )

    def to_api_json(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "coordinates": self.coordinates
        }

@dataclass
class BuildingDTO(BaseDTO):
    fid: str
    name: str
    sid: Optional[str] = None
    bid: Optional[str] = None
    eid: Optional[str] = None
    extraData: Dict[str, Any] = field(default_factory=dict)
    geometry: Optional[GeometryPolygonModel] = None
    levels: Optional[List["LevelDTO"]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "BuildingDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for BuildingDTO")
        
        # Handle V8 API response format - extract from 'result' if present
        if "result" in data:
            data = data["result"]
        
        # Required fields
        building_internal_id = data.get("buildingInternalIdentifier")
        if building_internal_id is None:
            raise ValidationError("Missing required field 'buildingInternalIdentifier'", "buildingInternalIdentifier", None)
        
        building_title = data.get("buildingTitle")
        if not building_title:
            raise ValidationError("Missing required field 'buildingTitle'", "buildingTitle", None)
        
        # Optional fields
        building_external_id = data.get("buildingExternalIdentifier")
        building_extra_data = ensure_dict(data.get("buildingExtraData"), "buildingExtraData")
        bid = str(building_internal_id)
        
        # Geometry
        geometry = None
        if "geometry" in data:
            geometry = GeometryPolygonModel.from_api_json(data["geometry"])
        
        # Levels
        levels = None
        if "levels" in data and isinstance(data["levels"], list):
            from pointr_cloud_common.dto.v8.level_dto import LevelDTO
            levels = [LevelDTO.from_api_json(level) for level in data["levels"]]
        
        return BuildingDTO(
            fid=str(building_internal_id),
            name=building_title,
            bid=bid,
            eid=building_external_id,
            extraData=building_extra_data,
            geometry=geometry,
            levels=levels
        )

    def to_api_json(self) -> Dict[str, Any]:
        result = {
            "buildingInternalIdentifier": int(self.fid),
            "buildingTitle": self.name,
            "buildingExtraData": self.extraData
        }
        
        if self.eid is not None:
            result["buildingExternalIdentifier"] = self.eid
            
        if self.geometry is not None:
            result["geometry"] = self.geometry.to_api_json()
            
        if self.levels is not None:
            result["levels"] = [level.to_api_json() for level in self.levels]
            
        if self.sid is not None:
            result["sid"] = self.sid
            
        if self.bid is not None:
            result["bid"] = self.bid
            
        return result
    
    def validate(self) -> bool:
        """Validate the DTO."""
        if not self.fid:
            raise ValidationError("fid cannot be empty", "fid", self.fid)
        if not self.name:
            raise ValidationError("name cannot be empty", "name", self.name)
        return True

    @staticmethod
    def list_from_api_json(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List["BuildingDTO"]:
        if isinstance(data, list):
            return [BuildingDTO.from_api_json(item) for item in data]
        
        # Handle V8 API response format
        if isinstance(data, dict):
            # Extract from 'results' field if present
            if "results" in data:
                results = data["results"]
                if isinstance(results, list):
                    return [BuildingDTO.from_api_json(item) for item in results]
            
            # Handle FeatureCollection format
            if data.get("type") == "FeatureCollection" and "features" in data:
                return [BuildingDTO.from_api_json(feature.get("properties", feature)) 
                       for feature in data["features"]]
            # Handle direct array format
            elif "items" in data and isinstance(data["items"], list):
                return [BuildingDTO.from_api_json(item) for item in data["items"]]
        
        return []

@dataclass
class BuildingResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for single building."""
    result: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "BuildingResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for BuildingResponseDTO")
        
        return BuildingResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            result=data.get("result")
        )

    def get_building(self) -> Optional[BuildingDTO]:
        """Extract building from the result."""
        if not self.result:
            return None
        return BuildingDTO.from_api_json(self.result)

@dataclass
class BuildingsResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for multiple buildings."""
    results: Optional[List[Dict[str, Any]]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "BuildingsResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for BuildingsResponseDTO")
        
        return BuildingsResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            results=data.get("results")
        )

    def get_buildings(self) -> List[BuildingDTO]:
        """Extract buildings from the results array."""
        if not self.results:
            return []
        return BuildingDTO.list_from_api_json(self.results)

@dataclass
class CreateBuildingResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for building creation."""
    result: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "CreateBuildingResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for CreateBuildingResponseDTO")
        
        return CreateBuildingResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            result=data.get("result")
        )

    def get_building(self) -> Optional[BuildingDTO]:
        """Extract created building from the result."""
        if not self.result:
            return None
        return BuildingDTO.from_api_json(self.result)
