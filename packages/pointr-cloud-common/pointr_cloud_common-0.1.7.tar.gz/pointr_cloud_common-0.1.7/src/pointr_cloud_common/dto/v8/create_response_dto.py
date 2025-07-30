from dataclasses import dataclass
from typing import Dict, Any, Optional

from pointr_cloud_common.dto.v8.base_dto import BaseDTO
from pointr_cloud_common.dto.v8.validation import ValidationError, validate_required_field, validate_type

@dataclass
class CreateResponseDTO(BaseDTO):
    internalIdentifier: int

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "CreateResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for CreateResponseDTO")
        
        # Handle V8 API response format - extract from 'result' if present
        if "result" in data:
            result_data = data["result"]
        else:
            result_data = data
        
        # Get the internal identifier based on the entity type
        internal_id = (result_data.get("siteInternalIdentifier") or 
                      result_data.get("buildingInternalIdentifier") or 
                      result_data.get("levelInternalIdentifier") or 
                      result_data.get("clientInternalIdentifier"))
        
        if internal_id is None:
            raise ValidationError("Missing required field 'internalIdentifier' or equivalent", "internalIdentifier", None)
        
        try:
            internal_id = int(internal_id)
        except (ValueError, TypeError):
            raise ValidationError("internalIdentifier must be convertible to int", "internalIdentifier", internal_id)
        
        return CreateResponseDTO(internalIdentifier=internal_id)

    def to_api_json(self) -> Dict[str, Any]:
        return {"internalIdentifier": self.internalIdentifier}
    
    def validate(self) -> bool:
        """Validate the DTO."""
        if not self.internalIdentifier:
            raise ValidationError("internalIdentifier cannot be empty", "internalIdentifier", self.internalIdentifier)
        return True
