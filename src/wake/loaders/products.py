"""
Products loader service for Wake API
"""

from typing import Dict, Any, Optional, List, AsyncGenerator
from ..api import wake_client


class ProductsLoader:
    """Service to load products data from Wake API"""
    
    def __init__(self, client=None):
        self.client = client or wake_client
    
    async def load_products(
        self,
        page: int = 1,
        quantity: int = 50,
        categories: Optional[List[int]] = None,
        manufacturers: Optional[List[int]] = None,
        distribution_centers: Optional[List[int]] = None,
        changed_since: Optional[str] = None,
        only_valid: bool = True,
        additional_fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Load products from Wake API
        
        Args:
            page: Page number (default: 1)
            quantity: Number of records per page (max: 50)
            categories: List of category IDs to filter
            manufacturers: List of manufacturer IDs to filter
            distribution_centers: List of distribution center IDs to filter
            changed_since: Return only products changed after date (format: yyyy-mm-dd hh:mm:ss)
            only_valid: Return only valid products
            additional_fields: Additional fields to include (Atacado, Estoque, Atributo, Informacao, TabelaPreco)
        """
        params = {
            "pagina": page,
            "quantidadeRegistros": min(quantity, 50),  # Max 50
            "somenteValidos": only_valid
        }
        
        if categories:
            params["categorias"] = ",".join(str(c) for c in categories)
        
        if manufacturers:
            params["fabricantes"] = ",".join(str(m) for m in manufacturers)
        
        if distribution_centers:
            params["centrosDistribuicao"] = ",".join(str(dc) for dc in distribution_centers)
        
        if changed_since:
            params["alteradosPartirDe"] = changed_since
        
        if additional_fields:
            params["camposAdicionais"] = additional_fields
        else:
            # Always include attributes and info by default
            params["camposAdicionais"] = ["Atributo", "Informacao"]
        
        result = await self.client.get("/produtos", params=params)
        return result if result is not None else []
    
    
    async def load_product_stock(
        self,
        identifier: str,
        identifier_type: str = "Sku"
    ) -> Dict[str, Any]:
        """
        Load product stock information
        
        Args:
            identifier: Product identifier
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
        
        Returns:
            Dictionary with total stock and stock by distribution center
        """
        params = {"tipoIdentificador": identifier_type}
        return await self.client.get(f"/produtos/{identifier}/estoque", params=params)
    
    async def load_product_prices(
        self,
        identifier: str,
        identifier_type: str = "Sku"
    ) -> Dict[str, Any]:
        """
        Load product prices including price table prices
        
        Args:
            identifier: Product identifier
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
        
        Returns:
            Dictionary with all product prices
        """
        params = {"tipoIdentificador": identifier_type}
        return await self.client.get(f"/produtos/{identifier}/precos", params=params)
    
    async def load_product_images(
        self,
        identifier: str,
        identifier_type: str = "Sku",
        include_siblings: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Load product images
        
        Args:
            identifier: Product identifier
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
            include_siblings: Include sibling products' images
        
        Returns:
            List of product images
        """
        params = {
            "tipoIdentificador": identifier_type,
            "produtosIrmaos": include_siblings
        }
        result = await self.client.get(f"/produtos/{identifier}/imagens", params=params)
        return result if result is not None else []
    
    async def load_related_products(
        self,
        identifier: str,
        identifier_type: str = "Sku"
    ) -> List[Dict[str, Any]]:
        """
        Load related products
        
        Args:
            identifier: Product identifier
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
        
        Returns:
            List of related product identifiers
        """
        params = {"tipoIdentificador": identifier_type}
        result = await self.client.get(f"/produtos/{identifier}/relacionados", params=params)
        return result if result is not None else []
    
    async def load_product_categories(
        self,
        identifier: str,
        identifier_type: str = "Sku",
        page: int = 1,
        quantity: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Load product categories
        
        Args:
            identifier: Product identifier
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
            page: Page number (default: 1)
            quantity: Number of records per page (max: 50)
        
        Returns:
            List of product categories
        """
        params = {
            "tipoIdentificador": identifier_type,
            "pagina": page,
            "quantidadRegistros": min(quantity, 50)
        }
        result = await self.client.get(f"/produtos/{identifier}/categorias", params=params)
        return result if result is not None else []
    
    async def load_product_updates(
        self,
        page: int = 1,
        quantity: int = 50,
        changed_since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Load products that have been updated (price or stock changes)
        
        Args:
            page: Page number (default: 1)
            quantity: Number of records per page (max: 50)
            changed_since: Return only products changed after date (format: yyyy-mm-dd hh:mm:ss, max 48h)
        
        Returns:
            List of products with price and stock changes
        """
        params = {
            "pagina": page,
            "quantidadeRegistros": min(quantity, 50)
        }
        
        if changed_since:
            params["alteradosPartirDe"] = changed_since
        
        result = await self.client.get("/produtos/alteracoes", params=params)
        return result if result is not None else []
    
    async def load_product_info(
        self,
        identifier: str,
        identifier_type: str = "Sku"
    ) -> List[Dict[str, Any]]:
        """
        Load product information (descriptions, specifications, etc.)
        
        Args:
            identifier: Product identifier (SKU, product variant ID, or product ID)
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
            
        Returns:
            List of product information entries
        """
        params = {"tipoIdentificador": identifier_type}
        result = await self.client.get(f"/produtos/{identifier}/informacoes", params=params)
        return result if result is not None else []
    
    async def load_related_products(
        self,
        identifier: str,
        identifier_type: str = "ProdutoId"
    ) -> List[Dict[str, Any]]:
        """
        Load related products from the Wake API
        
        Args:
            identifier: Product identifier (SKU, product variant ID, or product ID)
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
            
        Returns:
            List of related product identifiers (produtoId, sku, etc.)
        """
        params = {"tipoIdentificador": identifier_type}
        result = await self.client.get(f"/produtos/{identifier}/relacionados", params=params)
        return result if result is not None else []
    
    async def load_product_images(
        self,
        identifier: str,
        identifier_type: str = "Sku",
        include_siblings: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Load product images from the Wake API
        
        Args:
            identifier: Product identifier (SKU, product variant ID, or product ID)
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
            include_siblings: Include images from sibling products (produtosIrmaos)
            
        Returns:
            List of product images with URLs
        """
        params = {
            "tipoIdentificador": identifier_type,
            "produtosIrmaos": include_siblings
        }
        result = await self.client.get(f"/produtos/{identifier}/imagens", params=params)
        return result if result is not None else []
    
    async def load_all_products(
        self,
        batch_size: int = 50,
        only_valid: bool = True,
        additional_fields: Optional[List[str]] = None
    ) -> AsyncGenerator[List[Dict[str, Any]], None]:
        """
        Generator to load all products in batches
        
        Args:
            batch_size: Number of products per batch (max: 50)
            only_valid: Return only valid products
            additional_fields: Additional fields to include
        """
        page = 1
        
        while True:
            result = await self.load_products(
                page=page,
                quantity=batch_size,
                only_valid=only_valid,
                additional_fields=additional_fields
            )
            
            if not result:
                break
            
            yield result
            page += 1
    
    async def get_product(
        self,
        identifier: str,
        identifier_type: str = "Sku",
        additional_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get a single product by its identifier
        
        Args:
            identifier: Product identifier (SKU, product variant ID, or product ID)
            identifier_type: Type of identifier (Sku, ProdutoVarianteId, ProdutoId)
            additional_fields: Additional fields to include (Atacado, Estoque, Atributo, Informacao, TabelaPreco)
            
        Returns:
            Product details or empty dict if not found
        """
        params = {"tipoIdentificador": identifier_type}
        
        if additional_fields:
            params["camposAdicionais"] = additional_fields
        else:
            # Always include attributes and info by default
            params["camposAdicionais"] = ["Atributo", "Informacao", "Estoque"]
        
        result = await self.client.get(f"/produtos/{identifier}", params=params)
        return result if result is not None else {}