from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union

from pointr_cloud_common.dto.v8.base_dto import BaseDTO, BaseV8ResponseDTO
from pointr_cloud_common.dto.v8.validation import ValidationError, validate_required_field, validate_type, ensure_dict
from pointr_cloud_common.dto.v8.building_dto import GeometryPolygonModel

@dataclass
class LevelDTO(BaseDTO):
    fid: str  # This will be derived from levelIndex
    name: str  # This will be levelLongTitle
    shortName: Optional[str] = None  # This will be levelShortTitle
    sid: Optional[str] = None
    bid: Optional[str] = None
    eid: Optional[str] = None
    levelNumber: Optional[int] = None  # This will be levelIndex
    extraData: Dict[str, Any] = field(default_factory=dict)
    geometry: Optional[GeometryPolygonModel] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "LevelDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for LevelDTO")
        
        # Handle V8 API response format - extract from 'result' if present
        if "result" in data:
            data = data["result"]
        
        # Required fields
        level_index = data.get("levelIndex")
        if level_index is None:
            raise ValidationError("Missing required field 'levelIndex'", "levelIndex", None)
        
        level_long_title = data.get("levelLongTitle")
        if not level_long_title:
            raise ValidationError("Missing required field 'levelLongTitle'", "levelLongTitle", None)
        
        # Optional fields
        level_short_title = data.get("levelShortTitle")
        level_extra_data = ensure_dict(data.get("levelExtraData"), "levelExtraData")
        
        # Geometry
        geometry = None
        if "geometry" in data:
            geometry = GeometryPolygonModel.from_api_json(data["geometry"])
        
        return LevelDTO(
            fid=str(level_index),  # Use levelIndex as the fid
            name=level_long_title,
            shortName=level_short_title,
            levelNumber=level_index,
            extraData=level_extra_data,
            geometry=geometry
        )

    def to_api_json(self) -> Dict[str, Any]:
        result = {
            "levelIndex": self.levelNumber,
            "levelLongTitle": self.name,
            "levelExtraData": self.extraData
        }
        
        if self.shortName is not None:
            result["levelShortTitle"] = self.shortName
            
        if self.geometry is not None:
            result["geometry"] = self.geometry.to_api_json()
            
        if self.sid is not None:
            result["sid"] = self.sid
            
        if self.bid is not None:
            result["bid"] = self.bid
            
        return result
    
    @property
    def floorNumber(self) -> Optional[int]:
        """Alias for levelNumber for backward compatibility."""
        return self.levelNumber
    
    def validate(self) -> bool:
        """Validate the DTO."""
        if not self.fid:
            raise ValidationError("fid cannot be empty", "fid", self.fid)
        if not self.name:
            raise ValidationError("name cannot be empty", "name", self.name)
        if not self.bid:
            raise ValidationError("bid cannot be empty", "bid", self.bid)
        if not self.sid:
            raise ValidationError("sid cannot be empty", "sid", self.sid)
        return True

    @staticmethod
    def list_from_api_json(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List["LevelDTO"]:
        if isinstance(data, list):
            return [LevelDTO.from_api_json(item) for item in data]
        
        # Handle V8 API response format
        if isinstance(data, dict):
            # Extract from 'results' field if present
            if "results" in data:
                results = data["results"]
                if isinstance(results, list):
                    return [LevelDTO.from_api_json(item) for item in results]
            
            # Handle FeatureCollection format
            if data.get("type") == "FeatureCollection" and "features" in data:
                return [LevelDTO.from_api_json(feature.get("properties", feature)) 
                       for feature in data["features"]]
            # Handle direct array format
            elif "items" in data and isinstance(data["items"], list):
                return [LevelDTO.from_api_json(item) for item in data["items"]]
        
        return []

@dataclass
class BuildingLevelsResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for building levels."""
    results: Optional[List[Dict[str, Any]]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "BuildingLevelsResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for BuildingLevelsResponseDTO")
        
        return BuildingLevelsResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            results=data.get("results")
        )

    def get_levels(self) -> List[LevelDTO]:
        """Extract levels from the results array."""
        if not self.results:
            return []
        return LevelDTO.list_from_api_json(self.results)
