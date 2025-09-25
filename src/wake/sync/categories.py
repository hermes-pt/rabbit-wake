"""
Categories sync service
"""

from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from wake.api import WakeAPIClient
from wake.loaders.categories import CategoriesLoader
from wake.db import SessionLocal, Category


class CategorySync:
    """Service to sync categories from Wake API to database"""
    
    def __init__(self, api_client: WakeAPIClient = None):
        self.api_client = api_client
        self.loader = None
    
    async def sync_all(self) -> int:
        """
        Sync all categories from API to database
        
        Returns:
            Number of categories synced
        """
        # Initialize loader
        if self.api_client:
            self.loader = CategoriesLoader(self.api_client)
        else:
            async with WakeAPIClient() as client:
                self.loader = CategoriesLoader(client)
                return await self._perform_sync()
        
        return await self._perform_sync()
    
    async def _perform_sync(self) -> int:
        """Perform the actual sync operation"""
        # Load categories from API
        categories = await self.loader.load_categories()
        
        # Sync to database
        with SessionLocal() as db:
            # Clear existing data
            db.query(Category).delete()
            
            # Insert new data
            for cat in categories:
                db_category = Category(
                    id=cat["id"],
                    parent_category_id=cat.get("categoriaPaiId"),
                    name=cat["nome"],
                    path=cat.get("caminhoHierarquia", ""),
                    is_active=cat.get("ativo", True)
                )
                db.add(db_category)
            
            db.commit()
            
        return len(categories)