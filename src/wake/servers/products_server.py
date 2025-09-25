#!/usr/bin/env python3
"""
Wake Products MCP Server

Provides tools to search and interact with Wake e-commerce products locally.
"""

from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, func

from src.wake.db import SessionLocal, Product, ProductVariant, VariantPricing, VariantStock, DistributionCenter, VariantAttribute, ProductInfo
from src.wake.api import WakeAPIClient
from src.wake.loaders import ProductsLoader


# Create MCP server
mcp = FastMCP("Wake Products Server")


@mcp.tool()
async def search_products(
    query: str,
    limit: int = 10,
    include_pricing: bool = True,
    include_out_of_stock: bool = False,
    include_images: bool = True
) -> List[Dict[str, Any]]:
    """
    Search for products by name, SKU, or other attributes
    
    Args:
        query: Search query (searches in product name, variant name, SKU)
        limit: Maximum number of results to return (default: 10)
        include_pricing: Include pricing information in results (default: True)
        include_out_of_stock: Include products with no stock (default: False - only shows in-stock items)
        include_images: Include product images from API (default: True)
    
    Returns:
        List of matching products with details (always includes stock information)
    """
    # Create API client for image loading if needed
    api_client = None
    loader = None
    if include_images:
        api_client = WakeAPIClient()
        await api_client.__aenter__()
        loader = ProductsLoader(api_client)
    
    try:
        with SessionLocal() as db:
            # Build base query
            query_obj = db.query(ProductVariant).join(Product)
            
            # Add search filters
            # Try to convert query to integer for ID searches
            try:
                query_as_int = int(query)
                search_filter = or_(
                    ProductVariant.name.ilike(f"%{query}%"),
                    ProductVariant.sku.ilike(f"%{query}%"),
                    Product.parent_name.ilike(f"%{query}%"),
                    Product.manufacturer.ilike(f"%{query}%"),
                    Product.id == query_as_int,  # Search by product ID
                    Product.parent_product_id == query_as_int  # Search by parent product ID
                )
            except ValueError:
                # Query is not a number, search only text fields
                search_filter = or_(
                    ProductVariant.name.ilike(f"%{query}%"),
                    ProductVariant.sku.ilike(f"%{query}%"),
                    Product.parent_name.ilike(f"%{query}%"),
                    Product.manufacturer.ilike(f"%{query}%")
                )
            query_obj = query_obj.filter(search_filter)
            
            # Join with stock table to enable sorting by stock
            query_obj = query_obj.outerjoin(VariantStock)
            
            # Filter out out-of-stock items by default
            if not include_out_of_stock:
                query_obj = query_obj.filter(
                    VariantStock.physical_stock > 0
                )
            
            # Sort by total stock (sum of all distribution centers) in descending order
            query_obj = query_obj.group_by(ProductVariant.id, Product.id).order_by(
                func.coalesce(func.sum(VariantStock.physical_stock), 0).desc()
            )
            
            # Get results
            variants = query_obj.limit(limit).all()
            
            results = []
            for variant in variants:
                result = {
                    "product_id": variant.product.id,
                    "variant_id": variant.id,
                    "sku": variant.sku,
                    "name": variant.name,
                    "parent_name": variant.product.parent_name,
                    "manufacturer": variant.product.manufacturer,
                    "ean": variant.ean
                }
                
                # Add pricing if requested
                if include_pricing:
                    pricing = db.query(VariantPricing).filter_by(variant_id=variant.id).first()
                    if pricing:
                        result["pricing"] = {
                            "original_price": pricing.original_price,
                            "sale_price": pricing.sale_price
                        }
                
                # Always add stock information
                stock_records = db.query(VariantStock).join(DistributionCenter).filter(
                    VariantStock.variant_id == variant.id
                ).all()
                
                total_stock = 0
                stock_by_dc = []
                
                for stock in stock_records:
                    total_stock += stock.physical_stock
                    stock_by_dc.append({
                        "distribution_center": stock.distribution_center.name,
                        "available": stock.physical_stock
                    })
                
                result["stock"] = {
                    "total_available": total_stock,
                    "by_location": stock_by_dc
                }
                
                # Add attributes (size, color, etc.) - simplified to just name->value
                attributes = db.query(VariantAttribute).filter_by(variant_id=variant.id).all()
                result["attributes"] = {}
                for attr in attributes:
                    result["attributes"][attr.name] = attr.value
                
                # Add product information (descriptions, specs, etc.)
                product_info = db.query(ProductInfo).filter_by(product_id=variant.product_id).all()
                result["product_info"] = {}
                for info in product_info:
                    # Group by info type, but just store the text content
                    if info.info_type not in result["product_info"]:
                        result["product_info"][info.info_type] = []
                    result["product_info"][info.info_type].append({
                        "title": info.title,
                        "text": info.text
                    })
                
                # Add product images from API
                if include_images and loader:
                    try:
                        images = await loader.load_product_images(variant.sku, "Sku", include_siblings=True)
                        if images:
                            result["images"] = [
                                {
                                    "url": img.get("url"),
                                    "ordem": img.get("ordem"),
                                    "nome": img.get("nomeArquivo")
                                }
                                for img in images
                                if img.get("url")
                            ]
                    except Exception:
                        # If image loading fails, continue without images
                        pass
                
                results.append(result)
        
        return results
    finally:
        # Clean up API client if created
        if api_client:
            await api_client.__aexit__(None, None, None)


@mcp.tool()
async def get_related_products(
    product_id: int,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Get related products for a given product ID
    
    Args:
        product_id: The product ID to find related products for
        limit: Maximum number of related products to return (default: 10)
    
    Returns:
        List of related products with details
    """
    # Always fetch from Wake API
    async with WakeAPIClient() as client:
        loader = ProductsLoader(client)
        # Get related products from API
        related_ids = await loader.load_related_products(str(product_id), "ProdutoId")
        
        if not related_ids:
            return []
        
        # Get details for each related product from local DB
        results = []
        with SessionLocal() as db:
            for related in related_ids[:limit]:
                variant = db.query(ProductVariant).filter_by(
                    sku=related.get('sku')
                ).first()
                
                if variant:
                    result = {
                        "product_id": variant.product_id,
                        "variant_id": variant.id,
                        "sku": variant.sku,
                        "name": variant.name,
                        "parent_name": variant.product.parent_name,
                        "manufacturer": variant.product.manufacturer
                    }
                    
                    # Add attributes
                    attributes = db.query(VariantAttribute).filter_by(
                        variant_id=variant.id
                    ).all()
                    result["attributes"] = {}
                    for attr in attributes:
                        result["attributes"][attr.name] = attr.value
                    
                    # Add pricing
                    pricing = db.query(VariantPricing).filter_by(
                        variant_id=variant.id
                    ).first()
                    if pricing:
                        result["pricing"] = {
                            "original_price": pricing.original_price,
                            "sale_price": pricing.sale_price
                        }
                    
                    # Add stock info
                    total_stock = db.query(func.sum(VariantStock.physical_stock)).filter_by(
                        variant_id=variant.id
                    ).scalar() or 0
                    result["stock_available"] = total_stock
                    
                    # Add product images
                    try:
                        images = await loader.load_product_images(variant.sku, "Sku", include_siblings=True)
                        if images:
                            result["images"] = [
                                {
                                    "url": img.get("url"),
                                    "ordem": img.get("ordem"),
                                    "nome": img.get("nomeArquivo")
                                }
                                for img in images
                                if img.get("url")
                            ]
                    except Exception:
                        # If image loading fails, continue without images
                        pass
                    
                    results.append(result)
        
        return results


if __name__ == "__main__":
    mcp.run()