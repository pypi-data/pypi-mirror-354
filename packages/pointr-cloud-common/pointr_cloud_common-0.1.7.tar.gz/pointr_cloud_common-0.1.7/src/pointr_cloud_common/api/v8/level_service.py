from typing import Dict, Any, List, Optional
import logging
from pointr_cloud_common.dto.v8.level_dto import LevelDTO
from pointr_cloud_common.dto.v8.create_response_dto import CreateResponseDTO
from pointr_cloud_common.api.v8.base_service import BaseApiService, V8ApiError

class LevelApiService(BaseApiService):
    """Service for level-related API operations."""
    
    def __init__(self, api_service):
        super().__init__(api_service)
        self.logger = logging.getLogger(__name__)
    
    def get_levels(self, site_fid: str, building_fid: str) -> List[LevelDTO]:
        """Get all levels for a building."""
        endpoint = f"{self.base_url}/sites/{site_fid}/buildings/{building_fid}/levels"
        response = self.session.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        levels = []
        for level_data in data:
            try:
                level = LevelDTO.from_api_json(level_data)
                level.sid = site_fid
                level.bid = building_fid
                levels.append(level)
            except Exception as e:
                self.logger.error(f"Failed to parse level data: {e}")
                continue
        
        self.logger.info(f"Retrieved {len(levels)} levels for building {building_fid}")
        return levels

    def get_draft_levels(self, site_fid: str, building_fid: str) -> List[LevelDTO]:
        """Get all draft levels for a building."""
        endpoint = f"{self.base_url}/sites/{site_fid}/buildings/{building_fid}/draft/levels"
        response = self.session.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        levels = []
        for level_data in data:
            try:
                level = LevelDTO.from_api_json(level_data)
                level.sid = site_fid
                level.bid = building_fid
                levels.append(level)
            except Exception as e:
                self.logger.error(f"Failed to parse draft level data: {e}")
                continue
        
        self.logger.info(f"Retrieved {len(levels)} draft levels for building {building_fid}")
        return levels

    def get_level_by_index(self, building_fid: str, level_index: int) -> LevelDTO:
        """
        Get a level by its index.

        Args:
            building_fid: The building FID
            level_index: The level index

        Returns:
            A LevelDTO object
        """
        # First get all levels
        all_levels = self.get_levels(building_fid, building_fid)
        
        # Find the level with the matching index
        for level in all_levels:
            if level.levelIndex == level_index:
                return level
 
        raise V8ApiError(f"No level found with index {level_index}")

    def create_level(self, building_fid: str, level_index: int, level: Dict[str, Any]) -> str:
        """
        Create a level in a building.

        Args:
            building_fid: The building FID
            level_index: The level index
            level: The level data

        Returns:
            The FID of the created level
        """
        endpoint = f"api/v8/buildings/{building_fid}/levels/{level_index}"
        data = self._make_request("POST", endpoint, level)
        try:
            # V8 API returns created level in 'result' object
            if "result" in data:
                return CreateResponseDTO.from_api_json(data).fid
            else:
                return CreateResponseDTO.from_api_json(data).fid
        except Exception as e:
            self.logger.error(f"Failed to parse create response: {str(e)}")
            raise V8ApiError(f"Failed to parse create response: {str(e)}")

    def update_level(self, building_fid: str, level_index: int, level: Dict[str, Any]) -> str:
        """
        Update a level in a building.

        Args:
            building_fid: The building FID
            level_index: The level index
            level: The level data
        
        Returns:
            The FID of the updated level
        """
        endpoint = f"api/v8/buildings/{building_fid}/levels/{level_index}"
        data = self._make_request("PATCH", endpoint, level)
        try:
            # V8 API returns updated level in 'result' object
            if "result" in data:
                return CreateResponseDTO.from_api_json(data).fid
            else:
                return CreateResponseDTO.from_api_json(data).fid
        except Exception as e:
            self.logger.error(f"Failed to parse update response: {str(e)}")
            raise V8ApiError(f"Failed to parse update response: {str(e)}")

    def delete_level(self, building_fid: str, level_index: int) -> bool:
        """
        Delete a level from a building.
        
        Args:
            building_fid: The building FID
            level_index: The level index
        
        Returns:
            True if the level was deleted successfully
        """
        endpoint = f"api/v8/buildings/{building_fid}/levels/{level_index}"
        self._make_request("DELETE", endpoint)
        return True
