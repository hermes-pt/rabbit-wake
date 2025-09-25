"""
Distribution centers sync service
"""

from typing import List
from sqlalchemy.orm import Session

from wake.api import WakeAPIClient
from wake.loaders import StockLocationsLoader
from wake.db import SessionLocal, DistributionCenter


class DistributionCenterSync:
    """Service to sync distribution centers from Wake API to database"""
    
    def __init__(self, api_client: WakeAPIClient = None):
        self.api_client = api_client
        self.loader = None
    
    async def sync_all(self) -> int:
        """
        Sync all distribution centers from API to database
        
        Returns:
            Number of distribution centers synced
        """
        # Initialize loader
        if self.api_client:
            self.loader = StockLocationsLoader(self.api_client)
        else:
            async with WakeAPIClient() as client:
                self.loader = StockLocationsLoader(client)
                return await self._perform_sync()
        
        return await self._perform_sync()
    
    async def _perform_sync(self) -> int:
        """Perform the actual sync operation"""
        # Load distribution centers from API
        centers = await self.loader.load_distribution_centers()
        
        # Sync to database
        with SessionLocal() as db:
            # Clear existing data
            db.query(DistributionCenter).delete()
            
            # Insert new data
            for center in centers:
                db_center = DistributionCenter(
                    id=center["id"],
                    name=center["nome"],
                    zip_code=center["cep"],
                    is_default=center["padrao"]
                )
                db.add(db_center)
            
            db.commit()
            
        return len(centers)