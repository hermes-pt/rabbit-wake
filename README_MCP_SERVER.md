# Wake Products MCP Server

A Model Context Protocol (MCP) server that provides tools to search and interact with Wake e-commerce products locally.

## Features

- 🔍 **Product Search**: Search products by name, SKU, manufacturer, or parent product name
- 💰 **Pricing Information**: Get current pricing with cost, original, and sale prices
- 📦 **Stock Information**: View stock levels across distribution centers
- 🎯 **Smart Filtering**: Filter by availability, limit results, and include/exclude data types

## Server Location

```
src/wake/servers/products_server.py
```

## Available Tools

### `search_products`

Search for products in the local database.

**Parameters:**
- `query` (str): Search query (searches in product name, variant name, SKU, manufacturer)
- `limit` (int, optional): Maximum results to return (default: 10)
- `include_pricing` (bool, optional): Include pricing information (default: true)
- `include_stock` (bool, optional): Include stock information (default: true)
- `only_available` (bool, optional): Only return products with stock > 0 (default: false)

**Example Usage:**
```json
{
  "tool": "search_products",
  "arguments": {
    "query": "camiseta",
    "limit": 5,
    "only_available": true
  }
}
```

**Response Format:**
```json
[
  {
    "variant_id": 123456,
    "product_id": 67890,
    "sku": "ABC123",
    "name": "Camiseta Básica Azul",
    "parent_name": "Camiseta Básica",
    "manufacturer": "Brand XYZ",
    "ean": "1234567890123",
    "weight": 200.0,
    "dimensions": {
      "height": 30.0,
      "length": 40.0,
      "width": 25.0
    },
    "is_valid": true,
    "show_on_site": true,
    "created_at": "2023-01-01T10:00:00",
    "updated_at": "2023-12-01T15:30:00",
    "pricing": {
      "cost_price": 25.00,
      "original_price": 59.90,
      "sale_price": 39.90,
      "updated_at": "2025-07-04T12:00:00"
    },
    "stock": {
      "total_physical_stock": 45,
      "by_distribution_center": [
        {
          "distribution_center_id": 1,
          "distribution_center_name": "Centro Principal",
          "physical_stock": 30,
          "reserved_stock": 5,
          "is_available": true,
          "updated_at": "2025-07-04T14:30:00"
        },
        {
          "distribution_center_id": 2,
          "distribution_center_name": "Centro Secundário",
          "physical_stock": 15,
          "reserved_stock": 0,
          "is_available": true,
          "updated_at": "2025-07-04T14:30:00"
        }
      ]
    }
  }
]
```

## Running the Server

### Standalone
```bash
uv run python src/wake/servers/products_server.py
```

### MCP Client Integration
Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "wake-products": {
      "command": "uv",
      "args": ["run", "python", "src/wake/servers/products_server.py"],
      "cwd": "/path/to/wake-mcp"
    }
  }
}
```

## Search Examples

1. **Search by SKU**: `query: "126010"`
2. **Search by product name**: `query: "camiseta"`
3. **Search by manufacturer**: `query: "nike"`
4. **Available products only**: `query: "tênis", only_available: true`
5. **Quick search (no pricing/stock)**: `query: "boné", include_pricing: false, include_stock: false`

## Database Requirements

The server requires a synced local database with the following tables:
- `products` - Product information
- `product_variants` - Product variants (SKUs)
- `variant_pricing` - Pricing information
- `variant_stock` - Stock levels by distribution center
- `distribution_centers` - Distribution center information

Use the sync scripts to populate the database:
- `sync_all_safe.py` - Full sync with resume capability
- `sync_products_only.py` - Products without pricing/stock
- `sync_prices.py` - Update pricing only
- `sync_stock.py` - Update stock only

## Performance

- **Local search**: All searches are performed on local SQLite database for fast responses
- **Optimized queries**: Uses database indexes for efficient searching
- **Configurable limits**: Control response size with the `limit` parameter
- **Selective data**: Choose what data to include (pricing, stock) to optimize response size