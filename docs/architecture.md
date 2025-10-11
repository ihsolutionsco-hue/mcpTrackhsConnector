# Architecture Guide

This guide explains the Clean Architecture implementation in the TrackHS MCP Connector.

## Overview

The TrackHS MCP Connector follows Clean Architecture principles to ensure maintainability, testability, and separation of concerns. The architecture is organized into three main layers:

- **Domain Layer**: Business logic and entities
- **Application Layer**: Use cases and interfaces
- **Infrastructure Layer**: External adapters and utilities

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   MCP Adapter   │  │   API Adapter   │  │   Utils      │ │
│  │                 │  │                 │  │              │ │
│  │ • Tools         │  │ • HTTP Client   │  │ • Auth       │ │
│  │ • Resources     │  │ • Config        │  │ • Logging    │ │
│  │ • Prompts       │  │ • Error Handling│  │ • Pagination │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Use Cases     │  │     Ports       │  │   Services   │ │
│  │                 │  │                 │  │              │ │
│  │ • Search        │  │ • API Client    │  │ • Validation │ │
│  │ • Validation    │  │ • Repository    │  │ • Processing │ │
│  │ • Processing    │  │ • Notifications │  │ • Analytics  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │    Entities     │  │  Value Objects  │  │ Exceptions  │ │
│  │                 │  │                 │  │              │ │
│  │ • Reservation   │  │ • Config        │  │ • API Error │ │
│  │ • Contact        │  │ • Request       │  │ • Validation│ │
│  │ • Unit           │  │ • Response      │  │ • Network   │ │
│  │ • Node           │  │ • Pagination    │  │ • Timeout   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### Domain Layer

The domain layer contains the core business logic and is independent of external frameworks.

#### Entities

Business objects that represent the core concepts:

```python
# src/trackhs_mcp/domain/entities/reservation.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Reservation(BaseModel):
    """Reservation entity representing a booking"""
    
    id: str = Field(..., description="Unique reservation identifier")
    guest_name: str = Field(..., description="Guest name")
    arrival_date: datetime = Field(..., description="Arrival date")
    departure_date: datetime = Field(..., description="Departure date")
    status: str = Field(..., description="Reservation status")
    total_amount: float = Field(..., description="Total amount")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### Value Objects

Immutable objects that represent concepts:

```python
# src/trackhs_mcp/domain/value_objects/config.py
from pydantic import BaseModel, Field, validator
from typing import Optional

class TrackHSConfig(BaseModel):
    """Configuration value object"""
    
    base_url: str = Field(..., description="API base URL")
    username: str = Field(..., description="API username")
    password: str = Field(..., description="API password")
    timeout: int = Field(30, description="Request timeout")
    
    @validator('base_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('Timeout must be positive')
        return v
```

#### Exceptions

Domain-specific exceptions:

```python
# src/trackhs_mcp/domain/exceptions/api_exceptions.py
class TrackHSException(Exception):
    """Base exception for Track HS operations"""
    pass

class AuthenticationError(TrackHSException):
    """Authentication failed"""
    pass

class ValidationError(TrackHSException):
    """Data validation failed"""
    pass

class ApiError(TrackHSException):
    """API request failed"""
    pass
```

### Application Layer

The application layer contains use cases and interfaces (ports).

#### Use Cases

Business logic implementation:

```python
# src/trackhs_mcp/application/use_cases/search_reservations.py
from typing import Dict, Any, Optional
from ...domain.entities.reservation import Reservation
from ...application.ports.api_client_port import ApiClientPort

class SearchReservationsUseCase:
    """Use case for searching reservations"""
    
    def __init__(self, api_client: ApiClientPort):
        self.api_client = api_client
    
    async def execute(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute reservation search"""
        # Validate filters
        self._validate_filters(filters)
        
        # Call API
        response = await self.api_client.get("/api/reservations", filters)
        
        # Process response
        reservations = [Reservation(**item) for item in response.get('data', [])]
        
        return {
            'reservations': reservations,
            'pagination': response.get('pagination', {}),
            'total': response.get('total', 0)
        }
    
    def _validate_filters(self, filters: Dict[str, Any]) -> None:
        """Validate search filters"""
        # Implementation details...
        pass
```

#### Ports (Interfaces)

Abstractions for external dependencies:

```python
# src/trackhs_mcp/application/ports/api_client_port.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ApiClientPort(ABC):
    """Port for API client operations"""
    
    @abstractmethod
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform GET request"""
        pass
    
    @abstractmethod
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform POST request"""
        pass
    
    @abstractmethod
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform PUT request"""
        pass
    
    @abstractmethod
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Perform DELETE request"""
        pass
```

### Infrastructure Layer

The infrastructure layer contains external adapters and utilities.

#### Adapters

Implementations of ports:

```python
# src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py
import httpx
from typing import Dict, Any, Optional
from ...application.ports.api_client_port import ApiClientPort
from ...domain.value_objects.config import TrackHSConfig

class TrackHSApiClient(ApiClientPort):
    """Track HS API client implementation"""
    
    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout
        )
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform GET request"""
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform POST request"""
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()
    
    # Additional methods...
```

#### MCP Adapter

MCP protocol implementation:

```python
# src/trackhs_mcp/infrastructure/mcp/tools.py
from fastmcp import FastMCP
from ...application.use_cases.search_reservations import SearchReservationsUseCase

def register_search_reservations_tool(mcp: FastMCP, api_client):
    """Register search reservations tool"""
    
    @mcp.tool()
    async def search_reservations(
        date_from: str = None,
        date_to: str = None,
        status: str = None
    ) -> str:
        """
        Search reservations with filters.
        
        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            status: Reservation status
        """
        use_case = SearchReservationsUseCase(api_client)
        filters = {
            'date_from': date_from,
            'date_to': date_to,
            'status': status
        }
        result = await use_case.execute(filters)
        return f"Found {result['total']} reservations"
```

## Dependency Injection

The architecture uses dependency injection to decouple components and enable testing.

### Main Entry Point

```python
# src/trackhs_mcp/__main__.py
from fastmcp import FastMCP
from .infrastructure.adapters.config import TrackHSConfig
from .infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from .infrastructure.mcp.server import register_all_components

def main():
    """Main entry point with dependency injection"""
    # Create dependencies
    config = TrackHSConfig.from_env()
    api_client = TrackHSApiClient(config)
    
    # Create MCP server
    mcp = FastMCP("TrackHS MCP Server")
    
    # Register components with dependencies
    register_all_components(mcp, api_client)
    
    # Run server
    mcp.run()

if __name__ == "__main__":
    main()
```

### Component Registration

```python
# src/trackhs_mcp/infrastructure/mcp/server.py
from .tools import register_all_tools
from .resources import register_all_resources
from .prompts import register_all_prompts

def register_all_components(mcp: FastMCP, api_client):
    """Register all components with dependency injection"""
    register_all_tools(mcp, api_client)
    register_all_resources(mcp, api_client)
    register_all_prompts(mcp, api_client)
```

## Design Patterns

### 1. Repository Pattern

Abstraction for data access:

```python
# src/trackhs_mcp/application/ports/repository_port.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.entities.reservation import Reservation

class ReservationRepositoryPort(ABC):
    """Repository port for reservation data"""
    
    @abstractmethod
    async def find_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """Find reservation by ID"""
        pass
    
    @abstractmethod
    async def search(self, filters: Dict[str, Any]) -> List[Reservation]:
        """Search reservations with filters"""
        pass
```

### 2. Strategy Pattern

Pluggable implementations:

```python
# src/trackhs_mcp/application/ports/notification_port.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class NotificationPort(ABC):
    """Port for notifications"""
    
    @abstractmethod
    async def send(self, message: str, data: Dict[str, Any]) -> bool:
        """Send notification"""
        pass

class EmailNotificationAdapter(NotificationPort):
    """Email notification implementation"""
    
    async def send(self, message: str, data: Dict[str, Any]) -> bool:
        # Email implementation
        pass

class SlackNotificationAdapter(NotificationPort):
    """Slack notification implementation"""
    
    async def send(self, message: str, data: Dict[str, Any]) -> bool:
        # Slack implementation
        pass
```

### 3. Factory Pattern

Object creation:

```python
# src/trackhs_mcp/infrastructure/factories/api_client_factory.py
from typing import Type
from ...application.ports.api_client_port import ApiClientPort
from ...infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from ...infrastructure.adapters.mock_api_client import MockApiClient

class ApiClientFactory:
    """Factory for creating API clients"""
    
    @staticmethod
    def create(environment: str = "production") -> ApiClientPort:
        """Create API client based on environment"""
        if environment == "test":
            return MockApiClient()
        else:
            return TrackHSApiClient()
```

## Testing Strategy

### Unit Tests

Test individual components in isolation:

```python
# tests/unit/application/use_cases/test_search_reservations.py
import pytest
from unittest.mock import AsyncMock
from src.trackhs_mcp.application.use_cases.search_reservations import SearchReservationsUseCase

class TestSearchReservationsUseCase:
    @pytest.fixture
    def mock_api_client(self):
        return AsyncMock()
    
    @pytest.fixture
    def use_case(self, mock_api_client):
        return SearchReservationsUseCase(mock_api_client)
    
    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_api_client):
        """Test successful execution"""
        mock_api_client.get.return_value = {
            'data': [{'id': '1', 'guest_name': 'John Doe'}],
            'total': 1
        }
        
        result = await use_case.execute({'status': 'confirmed'})
        
        assert result['total'] == 1
        assert len(result['reservations']) == 1
```

### Integration Tests

Test component interactions:

```python
# tests/integration/test_api_integration.py
import pytest
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig

class TestApiIntegration:
    @pytest.fixture
    def config(self):
        return TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="test",
            password="test"
        )
    
    @pytest.fixture
    def api_client(self, config):
        return TrackHSApiClient(config)
    
    @pytest.mark.asyncio
    async def test_api_connection(self, api_client):
        """Test API connection"""
        # Test actual API connection
        pass
```

### End-to-End Tests

Test complete workflows:

```python
# tests/e2e/test_mcp_integration.py
import pytest
from fastmcp import FastMCP
from src.trackhs_mcp.infrastructure.mcp.server import register_all_components

class TestMCPIntegration:
    @pytest.fixture
    def mcp_server(self):
        mcp = FastMCP("Test Server")
        # Register components
        return mcp
    
    @pytest.mark.asyncio
    async def test_tool_execution(self, mcp_server):
        """Test tool execution through MCP"""
        # Test complete MCP workflow
        pass
```

## Benefits of Clean Architecture

### 1. Maintainability

- Clear separation of concerns
- Easy to understand and modify
- Reduced coupling between components

### 2. Testability

- Easy to mock dependencies
- Unit tests for each layer
- Integration tests for workflows

### 3. Flexibility

- Easy to swap implementations
- Support for multiple environments
- Pluggable components

### 4. Scalability

- Horizontal scaling support
- Performance optimization
- Resource management

## Best Practices

### 1. Layer Dependencies

- Domain layer has no dependencies
- Application layer depends only on domain
- Infrastructure layer depends on application and domain

### 2. Interface Segregation

- Small, focused interfaces
- Single responsibility principle
- Easy to implement and test

### 3. Dependency Inversion

- Depend on abstractions, not concretions
- Use dependency injection
- Easy to swap implementations

### 4. Error Handling

- Domain-specific exceptions
- Proper error propagation
- Graceful degradation

## Common Pitfalls

### 1. Anemic Domain Model

- Avoid entities with only getters/setters
- Include business logic in entities
- Use value objects for complex data

### 2. Leaky Abstractions

- Keep interfaces focused
- Avoid exposing implementation details
- Use proper abstraction levels

### 3. Circular Dependencies

- Avoid circular imports
- Use dependency injection
- Keep layers independent

### 4. Over-Engineering

- Start simple and evolve
- Don't create unnecessary abstractions
- Focus on business value

## Conclusion

The Clean Architecture implementation in the TrackHS MCP Connector provides:

- **Maintainable code** with clear separation of concerns
- **Testable components** with dependency injection
- **Flexible design** that supports multiple environments
- **Scalable architecture** for future growth

This architecture ensures the codebase remains maintainable and extensible as requirements evolve.
