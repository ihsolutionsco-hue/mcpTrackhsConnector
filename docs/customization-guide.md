# Customization Guide

This guide explains how to customize and extend the TrackHS MCP Connector for your specific needs.

## Adding New Tools

### 1. Create Use Case

First, create a new use case in the application layer:

```python
# src/trackhs_mcp/application/use_cases/new_tool.py
from typing import Dict, Any, Optional
from ...domain.value_objects.request import RequestOptions
from ...application.ports.api_client_port import ApiClientPort

class NewToolUseCase:
    def __init__(self, api_client: ApiClientPort):
        self.api_client = api_client

    async def execute(self, param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
        """Execute the new tool logic"""
        # Implement your business logic here
        result = await self.api_client.get(f"/api/endpoint", {"param1": param1})
        return result
```

### 2. Create MCP Tool

Create the MCP tool implementation:

```python
# src/trackhs_mcp/infrastructure/mcp/new_tool.py
from typing import Dict, Any
from fastmcp import FastMCP
from ...application.use_cases.new_tool import NewToolUseCase

def register_new_tool(mcp: FastMCP, api_client):
    """Register the new tool with MCP"""

    @mcp.tool()
    async def new_tool(param1: str, param2: int = None) -> str:
        """
        Description of your new tool.

        Args:
            param1: First parameter description
            param2: Second parameter description (optional)
        """
        use_case = NewToolUseCase(api_client)
        result = await use_case.execute(param1, param2)
        return f"Tool executed successfully: {result}"
```

### 3. Register Tool

Add the tool to the main tools registry:

```python
# src/trackhs_mcp/infrastructure/mcp/all_tools.py
from .new_tool import register_new_tool

def register_all_tools(mcp: FastMCP, api_client):
    """Register all tools with MCP"""
    # Existing tools...
    register_new_tool(mcp, api_client)
```

## Adding New Resources

### 1. Create Resource Handler

```python
# src/trackhs_mcp/infrastructure/mcp/new_resource.py
from typing import Dict, Any
from fastmcp import FastMCP

def register_new_resource(mcp: FastMCP, api_client):
    """Register new resource with MCP"""

    @mcp.resource("trackhs://new-resource")
    async def get_new_resource() -> Dict[str, Any]:
        """Get new resource data"""
        # Fetch data from API or generate content
        data = await api_client.get("/api/new-resource")
        return {
            "uri": "trackhs://new-resource",
            "mimeType": "application/json",
            "text": str(data)
        }
```

### 2. Register Resource

```python
# src/trackhs_mcp/infrastructure/mcp/resources.py
from .new_resource import register_new_resource

def register_all_resources(mcp: FastMCP, api_client):
    """Register all resources with MCP"""
    # Existing resources...
    register_new_resource(mcp, api_client)
```

## Adding New Prompts

### 1. Create Prompt Handler

```python
# src/trackhs_mcp/infrastructure/mcp/new_prompt.py
from typing import Dict, Any, Optional
from fastmcp import FastMCP

def register_new_prompt(mcp: FastMCP, api_client):
    """Register new prompt with MCP"""

    @mcp.prompt()
    async def new_prompt(context: str = "", options: Optional[Dict[str, Any]] = None) -> str:
        """
        Description of your new prompt.

        Args:
            context: Additional context for the prompt
            options: Optional configuration options
        """
        # Generate prompt based on context and options
        prompt_text = f"""
        Based on the context: {context}

        Generate a response that:
        1. Analyzes the provided information
        2. Provides actionable insights
        3. Suggests next steps

        Options: {options or {}}
        """
        return prompt_text
```

### 2. Register Prompt

```python
# src/trackhs_mcp/infrastructure/mcp/prompts.py
from .new_prompt import register_new_prompt

def register_all_prompts(mcp: FastMCP, api_client):
    """Register all prompts with MCP"""
    # Existing prompts...
    register_new_prompt(mcp, api_client)
```

## Extending Entities

### 1. Add New Domain Entity

```python
# src/trackhs_mcp/domain/entities/new_entity.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class NewEntity(BaseModel):
    """New domain entity"""

    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Entity name")
    description: Optional[str] = Field(None, description="Entity description")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### 2. Add Value Objects

```python
# src/trackhs_mcp/domain/value_objects/new_value_object.py
from pydantic import BaseModel, Field, validator
from typing import Optional

class NewValueObject(BaseModel):
    """New value object"""

    value: str = Field(..., description="Value content")
    type: str = Field(..., description="Value type")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @validator('value')
    def validate_value(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Value cannot be empty")
        return v.strip()
```

## Custom Authentication

### 1. Create Custom Auth Provider

```python
# src/trackhs_mcp/infrastructure/utils/custom_auth.py
from typing import Dict, Any, Optional
from ...domain.value_objects.config import TrackHSConfig

class CustomAuthProvider:
    """Custom authentication provider"""

    def __init__(self, config: TrackHSConfig):
        self.config = config

    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with custom provider"""
        # Implement custom authentication logic
        username = credentials.get('username')
        password = credentials.get('password')

        # Custom authentication logic here
        return await self._validate_credentials(username, password)

    async def _validate_credentials(self, username: str, password: str) -> bool:
        """Validate credentials with custom logic"""
        # Implement your authentication logic
        return True
```

### 2. Update API Client

```python
# src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py
from ..utils.custom_auth import CustomAuthProvider

class TrackHSApiClient(ApiClientPort):
    def __init__(self, config: TrackHSConfig):
        super().__init__(config)
        self.auth_provider = CustomAuthProvider(config)

    async def authenticate(self):
        """Use custom authentication"""
        credentials = {
            'username': self.config.username,
            'password': self.config.password
        }
        return await self.auth_provider.authenticate(credentials)
```

## Configuration Customization

### 1. Add New Configuration Options

```python
# src/trackhs_mcp/domain/value_objects/config.py
from pydantic import BaseModel, Field
from typing import Optional

class TrackHSConfig(BaseModel):
    """Extended configuration with custom options"""

    # Existing fields...
    base_url: str
    username: str
    password: str
    timeout: int = 30

    # New custom fields
    custom_endpoint: Optional[str] = Field(None, description="Custom API endpoint")
    retry_count: int = Field(3, description="Number of retry attempts")
    cache_ttl: int = Field(300, description="Cache TTL in seconds")
    enable_logging: bool = Field(True, description="Enable detailed logging")

    @classmethod
    def from_env(cls) -> "TrackHSConfig":
        """Create configuration from environment variables"""
        import os

        return cls(
            base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
            username=os.getenv("TRACKHS_USERNAME", ""),
            password=os.getenv("TRACKHS_PASSWORD", ""),
            timeout=int(os.getenv("TRACKHS_TIMEOUT", "30")),
            custom_endpoint=os.getenv("TRACKHS_CUSTOM_ENDPOINT"),
            retry_count=int(os.getenv("TRACKHS_RETRY_COUNT", "3")),
            cache_ttl=int(os.getenv("TRACKHS_CACHE_TTL", "300")),
            enable_logging=os.getenv("TRACKHS_ENABLE_LOGGING", "true").lower() == "true"
        )
```

### 2. Environment Variables

Add new environment variables to `.env.example`:

```env
# Existing variables...
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
TRACKHS_TIMEOUT=30

# New custom variables
TRACKHS_CUSTOM_ENDPOINT=/api/custom
TRACKHS_RETRY_COUNT=3
TRACKHS_CACHE_TTL=300
TRACKHS_ENABLE_LOGGING=true
```

## Testing Customizations

### 1. Unit Tests

```python
# tests/unit/application/use_cases/test_new_tool.py
import pytest
from unittest.mock import AsyncMock
from src.trackhs_mcp.application.use_cases.new_tool import NewToolUseCase

class TestNewToolUseCase:
    @pytest.fixture
    def mock_api_client(self):
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_api_client):
        return NewToolUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_api_client):
        """Test successful execution"""
        mock_api_client.get.return_value = {"result": "success"}

        result = await use_case.execute("test_param", 123)

        assert result == {"result": "success"}
        mock_api_client.get.assert_called_once()
```

### 2. Integration Tests

```python
# tests/integration/test_new_tool.py
import pytest
from src.trackhs_mcp.infrastructure.mcp.new_tool import register_new_tool
from fastmcp import FastMCP

class TestNewToolIntegration:
    @pytest.fixture
    def mcp_server(self):
        mcp = FastMCP("Test Server")
        return mcp

    @pytest.mark.asyncio
    async def test_tool_registration(self, mcp_server):
        """Test tool registration"""
        mock_api_client = AsyncMock()
        register_new_tool(mcp_server, mock_api_client)

        # Verify tool is registered
        assert "new_tool" in [tool.name for tool in mcp_server.tools]
```

## Deployment Customizations

### 1. Docker Configuration

```dockerfile
# Dockerfile.custom
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy custom configuration
COPY custom_config.py ./custom_config.py

# Set environment variables
ENV TRACKHS_CUSTOM_ENDPOINT=/api/custom
ENV TRACKHS_RETRY_COUNT=5

# Run with custom configuration
CMD ["python", "-m", "src.trackhs_mcp", "--config", "custom_config.py"]
```

### 2. Kubernetes Configuration

```yaml
# k8s-custom.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trackhs-mcp-connector-custom
spec:
  replicas: 2
  selector:
    matchLabels:
      app: trackhs-mcp-connector-custom
  template:
    metadata:
      labels:
        app: trackhs-mcp-connector-custom
    spec:
      containers:
      - name: mcp-connector
        image: trackhs-mcp-connector:custom
        env:
        - name: TRACKHS_CUSTOM_ENDPOINT
          value: "/api/custom"
        - name: TRACKHS_RETRY_COUNT
          value: "5"
        - name: TRACKHS_CACHE_TTL
          value: "600"
```

## Best Practices

### 1. Code Organization

- Keep customizations in separate modules
- Use dependency injection for testability
- Follow Clean Architecture principles
- Document all customizations

### 2. Testing

- Write unit tests for all custom code
- Include integration tests
- Test error scenarios
- Maintain test coverage

### 3. Configuration

- Use environment variables for configuration
- Provide sensible defaults
- Validate configuration on startup
- Document all configuration options

### 4. Error Handling

- Implement proper error handling
- Provide meaningful error messages
- Log errors appropriately
- Handle edge cases gracefully

### 5. Performance

- Consider performance implications
- Use caching where appropriate
- Implement proper resource management
- Monitor performance metrics

## Troubleshooting Customizations

### Common Issues

1. **Import Errors**: Ensure all custom modules are in the Python path
2. **Configuration Issues**: Verify environment variables are set correctly
3. **Authentication Problems**: Check custom authentication logic
4. **Performance Issues**: Monitor resource usage and optimize as needed

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test custom components
from src.trackhs_mcp.application.use_cases.new_tool import NewToolUseCase
use_case = NewToolUseCase(api_client)
result = await use_case.execute("test")
print(f"Result: {result}")
```

### Support

For customization issues:

1. Check the logs for error messages
2. Verify configuration settings
3. Test components individually
4. Review the Clean Architecture documentation
5. Contact support with detailed error information
