from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Set, ClassVar

from pointr_cloud_common.dto.v8.base_dto import BaseDTO, BaseV8ResponseDTO
from pointr_cloud_common.dto.v8.validation import ValidationError, validate_type

@dataclass
class SdkConfigurationDTO(BaseDTO):
    configurationKey: str
    configurationValue: str
    configurationValueType: str
    
    # Class variables (not dataclass fields)
    VALID_VALUE_TYPES: ClassVar[Set[str]] = {"Float", "Double", "Integer", "Boolean", "String"}
    MAX_VALUE_LENGTH: ClassVar[int] = 5000

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SdkConfigurationDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SdkConfigurationDTO")
        
        # Handle V8 API response format - extract from 'result' if present
        if "result" in data:
            data = data["result"]
        
        # Required fields
        config_key = data.get("configurationKey")
        if not config_key:
            raise ValidationError("Missing required field 'configurationKey'", "configurationKey", None)
        
        config_value = data.get("configurationValue")
        if config_value is None:  # Allow empty string but not None
            raise ValidationError("Missing required field 'configurationValue'", "configurationValue", None)
        
        config_value_type = data.get("configurationValueType")
        if not config_value_type:
            raise ValidationError("Missing required field 'configurationValueType'", "configurationValueType", None)
        
        validate_type(config_key, str, "configurationKey")
        validate_type(config_value, str, "configurationValue")
        validate_type(config_value_type, str, "configurationValueType")
        
        return SdkConfigurationDTO(
            configurationKey=config_key,
            configurationValue=config_value,
            configurationValueType=config_value_type
        )

    def to_api_json(self) -> Dict[str, Any]:
        """Convert the DTO to a dictionary for API requests."""
        return {
            "configurationKey": self.configurationKey,
            "configurationValue": self.configurationValue,
            "configurationValueType": self.configurationValueType
        }
    
    def validate(self) -> bool:
        """Validate the DTO according to API requirements."""
        if not self.configurationKey:
            raise ValidationError("configurationKey cannot be empty", "configurationKey", self.configurationKey)
            
        if self.configurationValue is None:  # Allow empty string but not None
            raise ValidationError("configurationValue cannot be None", "configurationValue", self.configurationValue)
            
        if len(self.configurationValue) > self.MAX_VALUE_LENGTH:
            raise ValidationError(
                f"configurationValue exceeds maximum length of {self.MAX_VALUE_LENGTH} characters", 
                "configurationValue", 
                f"{len(self.configurationValue)} characters"
            )
            
        if not self.configurationValueType:
            raise ValidationError("configurationValueType cannot be empty", "configurationValueType", self.configurationValueType)
            
        if self.configurationValueType not in self.VALID_VALUE_TYPES:
            raise ValidationError(
                f"configurationValueType must be one of {', '.join(self.VALID_VALUE_TYPES)}", 
                "configurationValueType", 
                self.configurationValueType
            )
            
        return True

    @staticmethod
    def list_from_api_json(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List["SdkConfigurationDTO"]:
        if isinstance(data, list):
            return [SdkConfigurationDTO.from_api_json(item) for item in data]
        
        # Handle V8 API response format
        if isinstance(data, dict):
            # Extract from 'results' field if present
            if "results" in data:
                results = data["results"]
                if isinstance(results, list):
                    return [SdkConfigurationDTO.from_api_json(item) for item in results]
            
            # Handle nested configurations
            if "configurations" in data and isinstance(data["configurations"], list):
                return [SdkConfigurationDTO.from_api_json(item) for item in data["configurations"]]
        
        return []

@dataclass
class SdkConfigurationResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for SDK configurations."""
    result: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SdkConfigurationResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SdkConfigurationResponseDTO")
        
        return SdkConfigurationResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            result=data.get("result")
        )

    def get_sdk_configurations(self) -> List[SdkConfigurationDTO]:
        """Extract SDK configurations from the result."""
        if not self.result:
            return []
        
        # Handle single configuration object
        if isinstance(self.result, dict) and "configurationKey" in self.result:
            return [SdkConfigurationDTO.from_api_json(self.result)]
        
        # Handle list of configurations
        if isinstance(self.result, list):
            return SdkConfigurationDTO.list_from_api_json(self.result)
        
        # Handle nested structure
        if isinstance(self.result, dict):
            configs = self.result.get("configurations", [])
            if isinstance(configs, list):
                return SdkConfigurationDTO.list_from_api_json(configs)
            elif isinstance(configs, dict) and "configurationKey" in configs:
                return [SdkConfigurationDTO.from_api_json(configs)]
        
        return []

@dataclass
class SdkTypedConfigResponseDTO(BaseV8ResponseDTO):
    """V8 API response wrapper for typed SDK configurations."""
    results: Optional[List[Dict[str, Any]]] = None

    @staticmethod
    def from_api_json(data: Dict[str, Any]) -> "SdkTypedConfigResponseDTO":
        if not isinstance(data, dict):
            raise ValidationError("Expected dictionary for SdkTypedConfigResponseDTO")
        
        return SdkTypedConfigResponseDTO(
            createdTimestampUtcEpochSeconds=data.get("createdTimestampUtcEpochSeconds"),
            endpoint=data.get("endpoint"),
            results=data.get("results")
        )

    def get_sdk_configurations(self) -> List[SdkConfigurationDTO]:
        """Extract SDK configurations from the results array."""
        if not self.results:
            return []
        return SdkConfigurationDTO.list_from_api_json(self.results)
