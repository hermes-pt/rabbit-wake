"""
Products sync service
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from wake.api import WakeAPIClient
from wake.loaders import ProductsLoader
from wake.db import SessionLocal, Product, ProductVariant, VariantPricing, VariantStock, DistributionCenter, VariantAttribute, ProductInfo


class ProductSync:
    """Service to sync products from Wake API to database"""
    
    def __init__(self, api_client: WakeAPIClient = None, sync_prices: bool = True, sync_stock: bool = True):
        self.api_client = api_client
        self.loader = ProductsLoader(api_client) if api_client else None
        self.sync_prices = sync_prices
        self.sync_stock = sync_stock
    
    async def sync_all(self, limit: int = 100) -> int:
        """
        Sync products from API to database
        
        Args:
            limit: Maximum number of products to sync
            
        Returns:
            Number of products synced
        """
        # Initialize loader
        if self.api_client:
            self.loader = ProductsLoader(self.api_client)
        else:
            async with WakeAPIClient() as client:
                self.loader = ProductsLoader(client)
                return await self._perform_sync(limit)
        
        return await self._perform_sync(limit)
    
    async def _perform_sync(self, limit: int) -> int:
        """Perform the actual sync operation"""
        # Load products from API
        products = await self.loader.load_products(quantity=limit)
        
        # Get distribution centers for stock sync
        distribution_centers = []
        with SessionLocal() as db:
            distribution_centers = db.query(DistributionCenter).all()
            dc_ids = [dc.id for dc in distribution_centers]
        
        count = 0
        
        # Process each product
        for product_data in products:
            await self._sync_product(product_data, dc_ids)
            count += 1
        
        return count
    
    async def _sync_product(self, product_data: Dict, dc_ids: List[int]):
        """Sync a single product and its variants"""
        with SessionLocal() as db:
            # Each item in the products list is actually a variant
            # Extract product info from variant data
            product_id = product_data["produtoId"]
            
            # Create or update product
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                product = Product(id=product_id)
            
            product.parent_product_id = product_data.get("parentId")
            product.parent_name = product_data.get("nomeProdutoPai")
            product.manufacturer = product_data.get("fabricante")
            product.created_at = self._parse_datetime(product_data.get("dataCriacao"))
            product.updated_at = self._parse_datetime(product_data.get("dataAtualizacao"))
            
            db.add(product)
            db.flush()
            
            # Sync product information (descriptions, specs, etc.)
            if product_data.get("informacoes"):
                # Remove existing info for this product
                db.query(ProductInfo).filter_by(product_id=product.id).delete()
                
                # Add new info
                for info_data in product_data["informacoes"]:
                    info = ProductInfo(
                        product_id=product.id,
                        info_id=info_data.get("informacaoId", 0),
                        title=info_data.get("titulo", ""),
                        text=info_data.get("texto", ""),
                        info_type=info_data.get("tipoInformacao", ""),
                        show_on_site=info_data.get("exibirSite", True)
                    )
                    db.add(info)
            
            # The product data IS the variant data in this API
            await self._sync_variant(db, product.id, product_data, dc_ids)
            
            db.commit()
    
    async def _sync_variant(self, db: Session, product_id: int, variant_data: Dict, dc_ids: List[int]):
        """Sync a single product variant"""
        # Create or update variant - check by ID first, then by SKU
        variant = db.query(ProductVariant).filter_by(id=variant_data["produtoVarianteId"]).first()
        if not variant:
            # Check if SKU already exists
            variant = db.query(ProductVariant).filter_by(sku=variant_data["sku"]).first()
            if not variant:
                variant = ProductVariant(id=variant_data["produtoVarianteId"])
            else:
                # Update the ID if SKU exists but with different ID
                variant.id = variant_data["produtoVarianteId"]
        
        variant.product_id = product_id
        variant.sku = variant_data["sku"]
        variant.name = variant_data["nome"]
        variant.ean = variant_data.get("ean")
        variant.weight = variant_data.get("peso")
        variant.height = variant_data.get("altura")
        variant.length = variant_data.get("comprimento")
        variant.width = variant_data.get("largura")
        variant.is_valid = variant_data.get("valido", True)
        variant.show_on_site = variant_data.get("exibirSite", True)
        variant.created_at = self._parse_datetime(variant_data.get("dataCriacao"))
        variant.updated_at = self._parse_datetime(variant_data.get("dataAtualizacao"))
        
        db.add(variant)
        db.flush()
        
        # Sync pricing (if enabled)
        if self.sync_prices:
            pricing = db.query(VariantPricing).filter_by(variant_id=variant.id).first()
            if not pricing:
                pricing = VariantPricing(variant_id=variant.id)
            
            pricing.cost_price = variant_data.get("precoCusto")
            pricing.original_price = variant_data.get("precoDe")
            pricing.sale_price = variant_data.get("precoPor")
            pricing.updated_at = datetime.now()
            
            db.add(pricing)
        
        # Sync attributes (size, color, etc.)
        if variant_data.get("atributos"):
            # Remove existing attributes for this variant
            db.query(VariantAttribute).filter_by(variant_id=variant.id).delete()
            
            # Add new attributes
            for attr_data in variant_data["atributos"]:
                attribute = VariantAttribute(
                    variant_id=variant.id,
                    attribute_type=attr_data.get("tipoAtributo", ""),
                    name=attr_data.get("nome", ""),
                    value=attr_data.get("valor", ""),
                    is_filter=attr_data.get("isFiltro", False),
                    display=attr_data.get("exibir", True)
                )
                db.add(attribute)
        
        # Sync stock for each distribution center (if enabled)
        if self.sync_stock:
            for dc_id in dc_ids:
                # Get stock data from API
                stock_data = await self._get_stock_for_variant(variant.sku, dc_id)
                
                stock = db.query(VariantStock).filter_by(
                    variant_id=variant.id,
                    distribution_center_id=dc_id
                ).first()
                
                if not stock:
                    stock = VariantStock(
                        variant_id=variant.id,
                        distribution_center_id=dc_id
                    )
                
                if stock_data:
                    stock.physical_stock = stock_data.get("estoqueFisico", 0)
                    stock.reserved_stock = stock_data.get("estoqueReservado", 0)
                    # Calculate availability based on physical stock
                    stock.is_available = stock.physical_stock > 0
                else:
                    stock.physical_stock = 0
                    stock.reserved_stock = 0
                    stock.is_available = False
                
                stock.updated_at = datetime.now()
                db.add(stock)
    
    async def _get_stock_for_variant(self, sku: str, dc_id: int) -> Optional[Dict]:
        """Get stock data for a specific variant and distribution center"""
        try:
            stock_data = await self.loader.load_product_stock(sku)
            if stock_data:
                # Get the list of stock by distribution center
                dc_stock_list = stock_data.get("listProdutoVarianteCentroDistribuicaoEstoque", [])
                for stock in dc_stock_list:
                    if stock.get("centroDistribuicaoId") == dc_id:
                        return stock
        except:
            pass
        return None
    
    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """Parse datetime string from API"""
        if not date_str:
            return None
        try:
            # Handle format: "2023-11-29T15:42:22.84"
            if "T" in date_str:
                date_str = date_str.split(".")[0]  # Remove milliseconds
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            return None
        except:
            return None