# Examples

This directory contains practical examples of using the TrackHS MCP Connector.

## Basic Usage

### basic_usage.py

Demonstrates basic MCP operations with the TrackHS connector:

```python
# Example: Search reservations using MCP
# Demonstrates basic usage patterns

import asyncio
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.application.use_cases.search_reservations import SearchReservationsUseCase

async def main():
    """Basic usage example"""

    # 1. Configure the client
    config = TrackHSConfig.from_env()
    api_client = TrackHSApiClient(config)

    # 2. Create use case
    search_use_case = SearchReservationsUseCase(api_client)

    # 3. Search reservations
    filters = {
        'date_from': '2024-01-01',
        'date_to': '2024-01-31',
        'status': 'confirmed'
    }

    result = await search_use_case.execute(filters)

    print(f"Found {result['total']} reservations")
    for reservation in result['reservations']:
        print(f"- {reservation.guest_name}: {reservation.arrival_date} to {reservation.departure_date}")

    # 4. Clean up
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Running Examples

### Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Basic Usage Example

```bash
# Run the basic usage example
python examples/basic_usage.py
```

### Expected Output

```
Found 25 reservations
- John Doe: 2024-01-15 to 2024-01-20
- Jane Smith: 2024-01-18 to 2024-01-22
- Bob Johnson: 2024-01-20 to 2024-01-25
...
```

## Advanced Examples

### Custom Filters

```python
# Advanced filtering example
filters = {
    'date_from': '2024-01-01',
    'date_to': '2024-12-31',
    'node_ids': '123,456,789',
    'status': 'confirmed',
    'text': 'luxury',
    'sort_by': 'arrival_date',
    'sort_order': 'asc',
    'page': 1,
    'per_page': 50
}
```

### Error Handling

```python
# Error handling example
try:
    result = await search_use_case.execute(filters)
except ValidationError as e:
    print(f"Validation error: {e}")
except ApiError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Pagination

```python
# Pagination example
page = 1
per_page = 10

while True:
    filters = {
        'page': page,
        'per_page': per_page
    }

    result = await search_use_case.execute(filters)

    if not result['reservations']:
        break

    print(f"Page {page}: {len(result['reservations'])} reservations")

    for reservation in result['reservations']:
        print(f"  - {reservation.guest_name}")

    page += 1
```

## MCP Integration Examples

### Using with Claude Desktop

1. Configure Claude Desktop:
```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "src.trackhs_mcp"],
      "cwd": "/path/to/MCPtrackhsConnector",
      "env": {
        "TRACKHS_API_URL": "https://ihmvacations.trackhs.com/api",
        "TRACKHS_USERNAME": "your_username",
        "TRACKHS_PASSWORD": "your_password"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. Use in Claude:
```
Search for all confirmed reservations for next month
```

### Using with MCP Inspector

1. Start the server:
```bash
python -m src.trackhs_mcp
```

2. Open MCP Inspector:
```bash
npx -y @modelcontextprotocol/inspector
```

3. Connect using stdio transport

4. Test tools, resources, and prompts interactively

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're in the project root directory
2. **Configuration Errors**: Verify .env file is configured correctly
3. **API Errors**: Check your Track HS credentials and API access
4. **Network Errors**: Verify internet connectivity and firewall settings

### Debug Mode

Run examples with debug logging:

```bash
DEBUG=true python examples/basic_usage.py
```

### Testing Connectivity

```python
# Test API connectivity
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig

config = TrackHSConfig.from_env()
client = TrackHSApiClient(config)

# Test connection
try:
    result = await client.get("/api/health")
    print("API connection successful")
except Exception as e:
    print(f"API connection failed: {e}")
```

## Contributing Examples

To add new examples:

1. Create a new Python file in this directory
2. Follow the naming convention: `example_name.py`
3. Include comprehensive docstrings
4. Add error handling
5. Update this README with usage instructions

Example template:

```python
"""
Example: [Description]

This example demonstrates [what it does].
"""

import asyncio
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient

async def main():
    """Main example function"""
    # Your example code here
    pass

if __name__ == "__main__":
    asyncio.run(main())
```
