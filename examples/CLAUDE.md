# Working with Wake API Examples

## How to Use These Examples

When working with the Wake API examples in this directory, follow these guidelines:

### 1. Always Check Both Files

For each endpoint, there are two files:
- `.md` file - Contains the API endpoint documentation (method, URL, parameters)
- `.json` file - Contains actual response examples from the API

**IMPORTANT**: Always read the `.json` file to understand the exact response structure. Do not guess field names.

### 2. Response Structure Validation

Before implementing any endpoint:
1. Read the `.md` file to understand the endpoint URL and parameters
2. Read the `.json` file to see the exact field names and structure
3. Use the exact field names from the JSON examples, not assumed names

### 3. Common Mistakes to Avoid

❌ **Wrong**: Assuming field names
```python
stock.get('estoqueTotal')  # This field doesn't exist
stock.get('estoquePorCentroDistribuicao')  # Wrong field name
```

✅ **Correct**: Using exact field names from examples
```python
stock.get('estoqueFisico')  # From product_stock.json
stock.get('listProdutoVarianteCentroDistribuicaoEstoque')  # Exact field name
```

### 4. Handling Different Response Types

- **Lists**: Some endpoints return arrays directly (e.g., products, images)
- **Objects**: Some endpoints return single objects (e.g., stock, prices)
- **Null/None**: Some endpoints return `null` when no data exists (e.g., images for products without photos)

Always check the example to know what to expect.

### 5. Testing with Example Data

Use the exact identifiers from the examples when testing:
- SKU `146293` has images and stock (good for testing)
- SKU `73563` might not have images (good for testing empty responses)

### 6. Parameter Names

Check the `.md` files for exact parameter names:
- `tipoIdentificador` not `tipo_identificador`
- `pagina` not `page`
- `quantidadeRegistros` not `quantidade` or `limit`

### 7. Before Implementing

Checklist:
- [ ] Read the `.md` file for endpoint details
- [ ] Read the `.json` file for response structure
- [ ] Note exact field names and types
- [ ] Check if response can be null
- [ ] Use exact parameter names from documentation