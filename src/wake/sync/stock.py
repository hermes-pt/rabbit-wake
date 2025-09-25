"""
Stock sync service - updates only stock data for existing products
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from wake.api import WakeAPIClient
from wake.loaders import ProductsLoader
from wake.db import SessionLocal, ProductVariant, VariantStock, DistributionCenter


class StockSync:
    """Service to sync only stock levels for existing products"""
    
    def __init__(self, api_client: WakeAPIClient = None):
        self.api_client = api_client
        self.loader = ProductsLoader(api_client) if api_client else None
        self._dc_ids = None
    
    @property
    def dc_ids(self):
        """Get distribution center IDs"""
        if self._dc_ids is None:
            with SessionLocal() as db:
                dcs = db.query(DistributionCenter).all()
                self._dc_ids = [dc.id for dc in dcs]
        return self._dc_ids
    
    async def sync_all_stock(self, batch_size: int = 50) -> int:
        """
        Sync stock for all existing products
        
        Args:
            batch_size: Number of products per batch
            
        Returns:
            Number of stock records updated
        """
        if self.api_client:
            return await self._perform_sync(batch_size)
        else:
            async with WakeAPIClient() as client:
                self.api_client = client
                self.loader = ProductsLoader(client)
                return await self._perform_sync(batch_size)
    
    async def _perform_sync(self, batch_size: int) -> int:
        """Perform the actual stock sync"""
        total_updated = 0
        
        # Get all variants from database
        with SessionLocal() as db:
            # Process in batches
            offset = 0
            
            while True:
                variants = db.query(ProductVariant).offset(offset).limit(batch_size).all()
                
                if not variants:
                    break
                
                for variant in variants:
                    # Sync stock for this variant
                    updated = await self._sync_variant_stock(variant.id, variant.sku)
                    total_updated += updated
                
                offset += batch_size
        
        return total_updated
    
    async def _sync_variant_stock(self, variant_id: int, sku: str) -> int:
        """Sync stock for a single variant"""
        try:
            stock_data = await self.loader.load_product_stock(sku)
            if not stock_data:
                return 0
            
            # Get the list of stock by distribution center
            dc_stock_list = stock_data.get("listProdutoVarianteCentroDistribuicaoEstoque", [])
            
            with SessionLocal() as db:
                updated = 0
                
                for dc_id in self.dc_ids:
                    # Find stock data for this DC
                    dc_stock = None
                    for stock in dc_stock_list:
                        if stock.get("centroDistribuicaoId") == dc_id:
                            dc_stock = stock
                            break
                    
                    # Update or create stock record
                    stock_record = db.query(VariantStock).filter_by(
                        variant_id=variant_id,
                        distribution_center_id=dc_id
                    ).first()
                    
                    if not stock_record:
                        stock_record = VariantStock(
                            variant_id=variant_id,
                            distribution_center_id=dc_id
                        )
                    
                    if dc_stock:
                        stock_record.physical_stock = dc_stock.get("estoqueFisico", 0)
                        stock_record.reserved_stock = dc_stock.get("estoqueReservado", 0)
                        stock_record.is_available = stock_record.physical_stock > 0
                    else:
                        stock_record.physical_stock = 0
                        stock_record.reserved_stock = 0
                        stock_record.is_available = False
                    
                    stock_record.updated_at = datetime.now()
                    db.add(stock_record)
                    updated += 1
                
                db.commit()
                return updated
                
        except Exception as e:
            print(f"Failed to sync stock for SKU {sku}: {e}")
            return 0
    
    async def sync_stock_changes(self, changed_since: str = None) -> int:
        """
        Sync only products with stock changes
        
        Args:
            changed_since: Date string (yyyy-mm-dd hh:mm:ss)
            
        Returns:
            Number of stock records updated
        """
        if self.api_client:
            return await self._sync_changes(changed_since)
        else:
            async with WakeAPIClient() as client:
                self.api_client = client
                self.loader = ProductsLoader(client)
                return await self._sync_changes(changed_since)
    
    async def _sync_changes(self, changed_since: str) -> int:
        """Sync products with stock changes"""
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
                    # Each product has embedded stock data
                    variant_id = product_data.get("produtoVarianteId")
                    sku = product_data.get("sku")
                    stock_data = product_data.get("estoque", [])
                    
                    if not variant_id or not sku:
                        continue
                    
                    # Find variant by ID
                    variant = db.query(ProductVariant).filter_by(id=variant_id).first()
                    if not variant:
                        continue
                    
                    # Update stock for each distribution center
                    for stock_item in stock_data:
                        dc_id = stock_item.get("centroDistribuicaoId")
                        if not dc_id:
                            continue
                        
                        # Get or create stock record
                        stock_record = db.query(VariantStock).filter_by(
                            variant_id=variant_id,
                            distribution_center_id=dc_id
                        ).first()
                        
                        if not stock_record:
                            stock_record = VariantStock(
                                variant_id=variant_id,
                                distribution_center_id=dc_id
                            )
                        
                        # Update stock values
                        stock_record.physical_stock = stock_item.get("estoqueFisico", 0)
                        stock_record.reserved_stock = stock_item.get("estoqueReservado", 0)
                        stock_record.is_available = stock_record.physical_stock > 0
                        stock_record.updated_at = datetime.now()
                        
                        db.add(stock_record)
                        total_updated += 1
                
                db.commit()
            
            page += 1
        
        return total_updated