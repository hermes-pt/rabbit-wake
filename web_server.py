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
from src.wake.loaders.products import ProductsLoader
from src.wake.loaders.categories import CategoriesLoader
from src.wake.loaders.stock_locations import StockLocationsLoader
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
async def get_products(page: int = 1, quantity: int = 50):
    """Get products from Wake API"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductsLoader(client)
            products = await loader.load_products(page=page, quantity=min(quantity, 50))
            return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_identifier}")
async def get_product(product_identifier: str):
    """Get a specific product by SKU or ID"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductsLoader(client)
            product = await loader.get_product(product_identifier)
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
            loader = CategoriesLoader(client)
            categories = await loader.load_categories()
            return {"categories": categories, "count": len(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/distribution-centers")
async def get_distribution_centers():
    """Get all distribution centers"""
    try:
        async with WakeAPIClient() as client:
            loader = StockLocationsLoader(client)
            centers = await loader.load_distribution_centers()
            return {"distribution_centers": centers, "count": len(centers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_identifier}/stock")
async def get_product_stock(product_identifier: str):
    """Get stock information for a product"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductsLoader(client)
            stock = await loader.load_product_stock(product_identifier)
            return {"product_identifier": product_identifier, "stock": stock}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_identifier}/prices")
async def get_product_prices(product_identifier: str):
    """Get price information for a product"""
    try:
        async with WakeAPIClient() as client:
            loader = ProductsLoader(client)
            prices = await loader.load_product_prices(product_identifier)
            return {"product_identifier": product_identifier, "prices": prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)