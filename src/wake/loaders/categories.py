"""
Categories loader for Wake API
"""

from typing import List, Dict, Any
from ..api import wake_client


class CategoriesLoader:
    """Service to load categories from Wake API"""
    
    def __init__(self, client=None):
        self.client = client or wake_client
    
    async def load_categories(self) -> List[Dict[str, Any]]:
        """
        Load all categories
        
        Returns:
            List of categories
        """
        result = await self.client.get("/categorias")
        return result if result is not None else []