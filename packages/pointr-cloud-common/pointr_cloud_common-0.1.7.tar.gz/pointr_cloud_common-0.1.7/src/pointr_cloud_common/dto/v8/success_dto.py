from dataclasses import dataclass
from typing import Dict, Any, Optional

from pointr_cloud_common.dto.v8.base_dto import BaseDTO, BaseV8ResponseDTO
from pointr_cloud_common.dto.v8.validation import ValidationError

@dataclass
class SuccessResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for success responses."""
    result: Optional[Dict[str, Any]] = None
    isSuccess: Optional[bool] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SuccessResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SuccessResponseDTO")
        
        return SuccessResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            result=data.get("result"),
            isSuccess=data.get("isSuccess")
        )

    def is_successful(self) -> bool:
        """Check if the operation was successful."""
        if self.isSuccess is not None:
            return self.isSuccess
        
        # If no explicit success field, assume success if we have a result
        return self.result is not None

@dataclass
class EmptyResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for empty responses (like DELETE operations)."""
    
    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "EmptyResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for EmptyResponseDTO")
        
        return EmptyResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint")
        )
