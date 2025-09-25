"""
Stock locations (distribution centers) loader for Wake API
"""

from typing import List, Dict, Any
from ..api import wake_client


class StockLocationsLoader:
    """Service to load stock locations/distribution centers from Wake API"""
    
    def __init__(self, client=None):
        self.client = client or wake_client
    
    async def load_distribution_centers(self) -> List[Dict[str, Any]]:
        """
        Load all distribution centers
        
        Returns:
            List of distribution centers with id, name, zip code and default flag
            
        Example response:
            [
                {
                    "id": 25,
                    "nome": "CD Padrão",
                    "cep": 30140170,
                    "padrao": true
                }
            ]
        """
        result = await self.client.get("/centrosdistribuicao")
        return result if result is not None else []
    
    async def get_default_distribution_center(self) -> Dict[str, Any] | None:
        """
        Get the default distribution center
        
        Returns:
            Default distribution center or None if not found
        """
        centers = await self.load_distribution_centers()
        
        for center in centers:
            if center.get("padrao", False):
                return center
        
        return None
    
    async def get_distribution_center_by_id(self, center_id: int) -> Dict[str, Any] | None:
        """
        Get a specific distribution center by ID
        
        Args:
            center_id: Distribution center ID
            
        Returns:
            Distribution center data or None if not found
        """
        centers = await self.load_distribution_centers()
        
        for center in centers:
            if center.get("id") == center_id:
                return center
        
        return None