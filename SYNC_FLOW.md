# Wake API Sync Flow

## What We're Syncing

### 1. **Distribution Centers** (Centros de Distribuição)
- **Table**: `distribution_centers`
- **Data**: Warehouse locations where products are stored
- **Fields**: ID, name, ZIP code, is_default flag
- **Example**: "CD Padrão", "Storage SP", "Camys São Paulo"

### 2. **Categories** (Categorias)
- **Table**: `categories`
- **Data**: Product categories in a hierarchical structure
- **Fields**: ID, name, parent_category_id, path, is_active
- **Example**: "FEMININO > CAMISETA"

### 3. **Products** (Produtos)
- **Table**: `products`
- **Data**: Parent product groupings
- **Fields**: ID, parent_product_id, manufacturer, created_at, updated_at
- **Note**: In Wake API, products are grouped - one product can have multiple variants

### 4. **Product Variants** (Variantes)
- **Table**: `product_variants`
- **Data**: Individual SKUs (actual sellable items)
- **Fields**: ID, SKU, name, EAN, dimensions (weight, height, length, width), is_valid, show_on_site
- **Example**: "Camiseta Lisa Queen M PRETO" (SKU: 73607)

### 5. **Pricing** (Preços)
- **Table**: `variant_pricing`
- **Data**: Current prices for each variant
- **Fields**: cost_price, original_price (precoDe), sale_price (precoPor)
- **Example**: Original R$ 296, Sale R$ 88.80

### 6. **Stock** (Estoque)
- **Table**: `variant_stock`
- **Data**: Inventory levels per variant per distribution center
- **Fields**: physical_stock, reserved_stock, is_available
- **Example**: SKU 146293 has 6 units in "CD Padrão"

## Sync Process Flow

```
1. DISTRIBUTION CENTERS SYNC
   └─> GET /centrosdistribuicao
       └─> Store all DCs in database

2. CATEGORIES SYNC
   └─> GET /categorias
       └─> Store all categories with hierarchy

3. PRODUCTS SYNC (Main Process)
   └─> GET /produtos?pagina=X&quantidadeRegistros=50
       │
       └─> For each product in response:
           │
           ├─> Create/Update PRODUCT record
           │   └─> Extract: produtoId, parentId, manufacturer, dates
           │
           ├─> Create/Update VARIANT record
           │   └─> Extract: SKU, name, dimensions, flags
           │
           ├─> Create/Update PRICING record
           │   └─> Extract: precoCusto, precoDe, precoPor
           │
           └─> For each Distribution Center:
               └─> GET /produtos/{sku}/estoque
                   └─> Extract stock from listProdutoVarianteCentroDistribuicaoEstoque
                   └─> Create/Update STOCK record for this DC
```

## API Response Structure

The Wake API returns products as a flat list where each item is actually a variant with embedded product info:

```json
{
  "produtoVarianteId": 256680,  // Variant ID
  "produtoId": 70139,           // Product ID
  "sku": "73607",               // Unique SKU
  "nome": "Camiseta Lisa Queen M PRETO",
  "nomeProdutoPai": "Camiseta Lisa em Algodão...",
  "precoDe": 296,
  "precoPor": 88.8,
  // ... dimensions and other fields
}
```

Stock response structure:
```json
{
  "estoqueFisico": 6,  // Total stock
  "estoqueReservado": 0,
  "listProdutoVarianteCentroDistribuicaoEstoque": [
    {
      "centroDistribuicaoId": 25,
      "nome": "CD Padrão",
      "estoqueFisico": 6,
      "estoqueReservado": 0
    }
  ]
}
```

## Sync Options

### Option 1: Resume Sync
- Finds where the last sync stopped (by checking existing SKUs)
- Continues from that page
- Faster for adding new products

### Option 2: Full Resync
- Starts from page 1
- Updates ALL existing products with latest data
- Ensures stock, prices, and product info are current
- Takes longer but guarantees data freshness

## Rate Limiting

- API limit: 120 requests per minute per endpoint group
- Sync respects this limit automatically
- If rate limited, waits for the specified retry time
- Shows visual countdown during rate limit waits

## Performance

For ~6,000 products:
- Initial sync: ~2.5 hours (due to stock API calls)
- Resync: Similar time (updates existing data)
- Bottleneck: Stock requires 3 API calls per product (one per DC)