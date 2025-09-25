# Wake MCP Project Guidelines

## Core Principles

1. **Keep It Simple** - No over-engineering. Clean, readable code.
2. **Read Examples First** - Always check `examples/*.json` for exact field names.
3. **Handle None Gracefully** - Return empty lists/dicts instead of None when possible.
4. **Test Everything** - Create simple test files, run them, then delete them.

## Project Structure

```
src/wake/
├── api/          # API client (base.py, types.py)
├── db/           # Database models and connection
├── loaders/      # Data loaders (products, stock_locations, etc.)
├── servers/      # MCP servers
└── sync/         # Sync services (products, prices, stock)
```

## Development Flow

1. Check examples folder for endpoint docs
2. Read both `.md` (endpoint info) and `.json` (response structure)
3. Implement in appropriate loader
4. Test with real API calls
5. Clean up test files

## Code Style

- Return `Any` from base client
- Return specific types from loaders
- Convert None to empty collections in loaders
- Use exact field names from API responses
- No complex abstractions
- Always include `["Atributo", "Informacao"]` in API calls by default

## Testing

Quick test pattern:
```python
async with WakeAPIClient() as client:
    loader = SomeLoader(client)
    result = await loader.load_something()
    print(result)
```

## Database

- **variant_attributes**: Stores size (Tamanho), color (Cor), etc.
- **product_info**: Stores descriptions, specs, care instructions (HTML)
- **updated_at**: Track when prices/stock were last synced
- Migrations: Use `uv run alembic` for all migration commands

## Sync Features

- Products sync includes attributes and info automatically
- Price sync tracks `updated_at` timestamp
- Stock sync tracks `updated_at` timestamp
- Size mapping: PP, P, M, G, GG, SGG1, SGG2

## Remember

- Session reuse is already implemented
- Boolean params are auto-converted to strings
- POST/PUT/DELETE are disabled for safety
- Always close sessions properly
- Attributes (size/color) come from `camposAdicionais=["Atributo"]`
- Product info comes from `camposAdicionais=["Informacao"]`

Keep it simple, stupid.