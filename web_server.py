#!/usr/bin/env python3
"""
Wake HTTP Server for Render deployment

HTTP wrapper around the Wake MCP server for web deployment.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any
import asyncio
import json

# Import the Wake components
from src.wake.loaders.products import ProductLoader
from src.wake.loaders.categories import CategoryLoader
from src.wake.loaders.stock_locations import StockLocationLoader
from src.wake.api.base import WakeAPIClient

app = FastAPI(
    title="Wake E-commerce API",
    description="HTTP API for Wake E-commerce integration",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Wake E-commerce API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "wake-api"}

@app.get("/products")
async def get_products(limit: int = 100, offset: int = 0):
    """Get products from Wake API"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductLoader(client)
            products = await loader.load_products(limit=limit, offset=offset)
            return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductLoader(client)
            product = await loader.load_product_by_id(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
async def get_categories():
    """Get all categories"""
    try:
        async with WakeAPIClient() as client:
            loader = CategoryLoader(client)
            categories = await loader.load_all_categories()
            return {"categories": categories, "count": len(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock-locations")
async def get_stock_locations():
    """Get all stock locations"""
    try:
        async with WakeAPIClient() as client:
            loader = StockLocationLoader(client)
            locations = await loader.load_stock_locations()
            return {"stock_locations": locations, "count": len(locations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}/stock")
async def get_product_stock(product_id: int):
    """Get stock information for a product"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductLoader(client)
            stock = await loader.load_product_stock(product_id)
            return {"product_id": product_id, "stock": stock}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}/prices")
async def get_product_prices(product_id: int):
    """Get price information for a product"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductLoader(client)
            prices = await loader.load_product_prices(product_id)
            return {"product_id": product_id, "prices": prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)