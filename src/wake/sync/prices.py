"""
Price sync service - updates only pricing data for existing products
"""

from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from wake.api import WakeAPIClient
from wake.loaders import ProductsLoader
from wake.db import SessionLocal, ProductVariant, VariantPricing


class PriceSync:
    """Service to sync only prices for existing products"""
    
    def __init__(self, api_client: WakeAPIClient = None):
        self.api_client = api_client
        self.loader = ProductsLoader(api_client) if api_client else None
    
    async def sync_all_prices(self, batch_size: int = 50) -> int:
        """
        Sync prices for all existing products
        
        Args:
            batch_size: Number of products per page
            
        Returns:
            Number of prices updated
        """
        if self.api_client:
            return await self._perform_sync(batch_size)
        else:
            async with WakeAPIClient() as client:
                self.api_client = client
                self.loader = ProductsLoader(client)
                return await self._perform_sync(batch_size)
    
    async def _perform_sync(self, batch_size: int) -> int:
        """Perform the actual price sync"""
        page = 1
        total_updated = 0
        
        while True:
            # Get products from API
            products = await self.loader.load_products(
                page=page,
                quantity=batch_size
            )
            
            if not products:
                break
            
            # Update prices for each product
            with SessionLocal() as db:
                for product_data in products:
                    variant_id = product_data["produtoVarianteId"]
                    
                    # Check if variant exists
                    variant = db.query(ProductVariant).filter_by(id=variant_id).first()
                    if not variant:
                        continue  # Skip if product doesn't exist
                    
                    # Update pricing
                    pricing = db.query(VariantPricing).filter_by(variant_id=variant_id).first()
                    if not pricing:
                        pricing = VariantPricing(variant_id=variant_id)
                    
                    pricing.cost_price = product_data.get("precoCusto")
                    pricing.original_price = product_data.get("precoDe")
                    pricing.sale_price = product_data.get("precoPor")
                    pricing.updated_at = datetime.now()
                    
                    db.add(pricing)
                    total_updated += 1
                
                db.commit()
            
            page += 1
        
        return total_updated
    
    async def sync_price_changes(self, changed_since: str = None) -> int:
        """
        Sync only products with price changes
        
        Args:
            changed_since: Date string (yyyy-mm-dd hh:mm:ss)
            
        Returns:
            Number of prices updated
        """
        if not self.loader:
            async with WakeAPIClient() as client:
                self.loader = ProductsLoader(client)
                return await self._sync_changes(changed_since)
        
        return await self._sync_changes(changed_since)
    
    async def _sync_changes(self, changed_since: str) -> int:
        """Sync products with changes"""
        page = 1
        total_updated = 0
        
        while True:
            # Get changed products
            products = await self.loader.load_product_updates(
                page=page,
                quantity=50,
                changed_since=changed_since
            )
            
            if not products:
                break
            
            with SessionLocal() as db:
                for product_data in products:
                    # The updates endpoint returns full product data with embedded prices
                    variant_id = product_data.get("produtoVarianteId")
                    sku = product_data.get("sku")
                    
                    if not variant_id or not sku:
                        continue
                    
                    # Find variant by ID
                    variant = db.query(ProductVariant).filter_by(id=variant_id).first()
                    if not variant:
                        continue
                    
                    # Update pricing - the response includes current prices
                    pricing = db.query(VariantPricing).filter_by(variant_id=variant_id).first()
                    if not pricing:
                        pricing = VariantPricing(variant_id=variant_id)
                    
                    # Prices are directly in the response
                    pricing.original_price = product_data.get("precoDe")
                    pricing.sale_price = product_data.get("precoPor")
                    # Note: updates endpoint doesn't include cost price (precoCusto)
                    pricing.updated_at = datetime.now()
                    
                    db.add(pricing)
                    total_updated += 1
                
                db.commit()
            
            page += 1
        
        return total_updated