# Wake E-commerce Sync Architecture

## Overview

Architecture for synchronizing Wake e-commerce data to a local SQLite database using Alembic migrations, uv package manager, and MCP servers.

## Components

### 1. Database Layer
- **SQLite Database**: Local storage for synced data
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration management

### 2. Sync Service Layer
- **WakeSyncService**: Core synchronization logic
  - Fetches data from Wake API
  - Handles sync operations
  - Manages sync state
  
### 3. MCP Server Layer
- **wake_sync_server.py**: MCP server exposing sync operations
  - Start sync operations
  - Check sync status
  - View sync history

### 4. Wake API Integration
- Reuses existing `wake_api_base.py` client
- Read-only operations

## Directory Structure

```
wake-mcp/
├── alembic/
│   ├── versions/          # Migration files
│   └── alembic.ini        # Alembic configuration
├── sync/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # Database connection/session
│   └── service.py         # WakeSyncService
├── wake_sync_server.py    # MCP server for sync operations
├── wake_api_base.py       # Existing Wake API client
├── wake_types.py          # Existing Wake types
└── wake_sync.db           # SQLite database (generated)
```

## Environment Variables
```env
# Wake API
WAKE_API_BASE_URL=https://api.fbits.net
WAKE_API_TOKEN=your_token_here

# Database
DATABASE_URL=sqlite+aiosqlite:///wake_sync.db
```

## Implementation Steps

1. **Setup Project**
   - Initialize uv project
   - Install dependencies
   - Create directory structure

2. **Database Setup**
   - Create SQLAlchemy models
   - Initialize Alembic
   - Create migrations

3. **Sync Service**
   - Implement WakeSyncService
   - Connect to Wake API

4. **MCP Server**
   - Create wake_sync_server.py
   - Implement sync tools

5. **Testing**
   - Unit tests
   - Integration tests