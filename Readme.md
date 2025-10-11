# TrackHS MCP Connector

A production-ready MCP (Model Context Protocol) server for Track HS API integration, demonstrating Clean Architecture principles and comprehensive MCP protocol features.

## What is this?

This repository provides a complete implementation of an MCP server that:
- Integrates with Track HS API V2 for reservation management
- Demonstrates Clean Architecture with dependency injection
- Implements all MCP protocol features (tools, resources, prompts)
- Serves as a learning resource and starting template for your own MCP servers

The [Model Context Protocol](https://modelcontextprotocol.io) is an open standard that enables seamless integration between AI applications and external data sources, tools, and services.

## Table of Contents

- [Getting Started](#getting-started)
  - [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Testing](#testing)
  - [Common Issues & Solutions](#common-issues--solutions)
- [Understanding the System](#understanding-the-system)
  - [Features](#features)
  - [Repository Structure](#repository-structure)
  - [Configuration](#configuration)
  - [Customizing for Your Use Case](#customizing-for-your-use-case)
- [Development & Operations](#development--operations)
  - [Development](#development)
  - [Testing & Quality](#testing--quality)
  - [Monitoring & Debugging](#monitoring--debugging)
- [Reference](#reference)
  - [API Reference](#api-reference)
  - [Technical Details](#technical-details)
  - [Security](#security)
  - [External Resources](#external-resources)
- [Contributing](#contributing)
  - [License](#license)

---

# Getting Started

## Quick Start

*For detailed installation instructions, see [Installation](#installation) below.*

Get the server running in 5 minutes:

```bash
# 1. Prerequisites
python --version  # Ensure Python 3.8+

# 2. Setup
git clone <repository-url>
cd MCPtrackhsConnector
pip install -r requirements.txt

# 3. Configuration
cp .env.example .env
# Edit .env with your Track HS credentials

# 4. Start server
python -m src.trackhs_mcp

# 5. Test with MCP Inspector
npx -y @modelcontextprotocol/inspector
# Connect to stdio transport
```

## Installation

### Prerequisites
- Python 3.8+
- pip or uv
- Track HS API credentials

### Step 1: Clone and Install Dependencies
```bash
git clone <repository-url>
cd MCPtrackhsConnector
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Step 2: Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
# TRACKHS_API_URL=https://api.trackhs.com/api
# TRACKHS_USERNAME=your_username
# TRACKHS_PASSWORD=your_password
```

### Step 3: Start the Server
```bash
# Development mode
python -m src.trackhs_mcp

# Or with environment variables
TRACKHS_USERNAME=user TRACKHS_PASSWORD=pass python -m src.trackhs_mcp
```

## Testing

### With MCP Inspector (Recommended)

The easiest way to test the server:

```bash
# 1. Ensure server is running (python -m src.trackhs_mcp)

# 2. Launch Inspector
npx -y @modelcontextprotocol/inspector

# 3. Connect using stdio transport
# 4. Test tools, resources, and prompts interactively
```

### With Example Scripts

The `examples/` directory contains runnable code demonstrating MCP interactions:

- **`basic_usage.py`**: Complete Python example with MCP operations
- **`examples/README.md`**: Detailed usage instructions

See [examples/README.md](examples/README.md) for detailed usage.

## Common Issues & Solutions

### "Authentication failed"
- **Cause**: Invalid credentials or API URL
- **Solution**:
  - Verify credentials in `.env` file
  - Check API URL is correct
  - Ensure API is accessible

### "Cannot connect to MCP server" or "Connection Error"
- **Cause**: Server not running or incorrect configuration
- **Solution**:
  - Ensure server is running (`python -m src.trackhs_mcp`)
  - Check environment variables are set
  - Verify Python path and dependencies

### "Module not found" errors
- **Cause**: Missing dependencies or incorrect Python path
- **Solution**:
  - Install dependencies: `pip install -r requirements.txt`
  - Check Python version: `python --version`
  - Verify virtual environment is activated

### "API request failed"
- **Cause**: Network issues or API problems
- **Solution**:
  - Check internet connectivity
  - Verify API URL is accessible
  - Check API credentials are valid

---

# Understanding the System

## Features

### MCP Protocol Features
- **[Tools](https://modelcontextprotocol.io/docs/concepts/tools)**: Two focused reservation search tools (V1 and V2)
- **[Resources](https://modelcontextprotocol.io/docs/concepts/resources)**: Essential API schema and documentation
- **[Prompts](https://modelcontextprotocol.io/docs/concepts/prompts)**: Three specialized prompts for reservation search scenarios
- **Completions**: Auto-completion support for prompt arguments
- **Logging**: Multi-level logging with configurable verbosity
- **Error Handling**: Comprehensive error handling and validation

### Clean Architecture Features
- **Domain Layer**: Business entities and value objects
- **Application Layer**: Use cases and ports (interfaces)
- **Infrastructure Layer**: External adapters and utilities
- **Dependency Injection**: Easy testing and maintenance
- **Separation of Concerns**: Clear layer boundaries

### Track HS API Integration
- **Search Reservations V2**: Primary tool with comprehensive filtering capabilities
- **Search Reservations V1**: Legacy compatibility tool for existing integrations
- **Advanced Filtering**: Date ranges, IDs, text search, status filters
- **Pagination**: Standard pagination and Elasticsearch scroll
- **Error Handling**: Robust error handling and retry logic
- **Authentication**: Secure credential management

## Repository Structure

This repository demonstrates a focused MCP server following best practices with Clean Architecture:

```
src/trackhs_mcp/              # Main application code
├── domain/                   # Business logic and entities
├── application/              # Use cases and interfaces
└── infrastructure/           # External adapters and utilities

docs/                         # Documentation organized by topic
scripts/                      # Development and testing scripts
examples/                    # Example code and usage patterns
tests/                       # Comprehensive test suite
```

The architecture separates business logic from infrastructure concerns, allowing easy testing and maintenance.

## Configuration

The server uses environment variables for configuration:

**`.env` file:**
```bash
TRACKHS_API_URL=https://api.trackhs.com/api  # API base URL
TRACKHS_USERNAME=your_username               # API username
TRACKHS_PASSWORD=your_password               # API password
TRACKHS_TIMEOUT=30                          # Request timeout
```

## Customizing for Your Use Case

This is a reference implementation with Track HS integration. To adapt it for production:
- **Replace API integration:** See [Customization Guide](docs/customization-guide.md) for adapting to your API
- **Extend functionality:** See [Architecture Guide](docs/architecture.md) for adding new features

---

# Development & Operations

## Development

```bash
# Start development server
python -m src.trackhs_mcp

# Run tests
pytest tests/ -v

# Run linting
flake8 src/
black src/
isort src/
```

### Build & Production
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python -m src.trackhs_mcp
```

### Testing & Quality
```bash
pytest tests/ -v                    # All tests
pytest tests/ --cov=src/trackhs_mcp # With coverage
flake8 src/                         # Linting
black src/                          # Code formatting
isort src/                          # Import sorting
```

### Automated Testing

The test suite verifies all MCP features and Clean Architecture:

```bash
pytest tests/ -v
```

The tests cover:
- Unit tests for each layer (domain, application, infrastructure)
- Integration tests for API interactions
- End-to-end tests for complete workflows
- Error handling and edge cases

## Monitoring & Debugging

### Logging
Structured logging with configurable levels:
- HTTP request/response logging
- API interaction events
- Error tracking and debugging
- Performance monitoring

### Debug Tools
- MCP Inspector for interactive debugging
- Comprehensive test suite
- Development mode with hot-reload
- Source maps for debugging

---

# Reference

## API Reference

This MCP server provides a focused set of features:

### Tools (2)
- `search_reservations` - Primary reservation search using API V2
- `search_reservations_v1` - Legacy compatibility using API V1

### Prompts (3)
- `search-reservations-by-dates` - Search reservations by date range
- `search-reservations-by-guest` - Search reservations by guest information
- `search-reservations-advanced` - Advanced search with multiple filters

### Resources (2)
- `trackhs://schema/reservations` - Complete reservation data schema
- `trackhs://api/documentation` - API V2 documentation and examples

For detailed information, see [docs/api-reference.md](docs/api-reference.md).

## Technical Details

### Clean Architecture Implementation

The server implements Clean Architecture with clear separation of concerns:

#### Domain Layer
- **Entities**: Business objects (Reservation, Contact, Unit, etc.)
- **Value Objects**: Immutable objects (Config, RequestOptions, etc.)
- **Exceptions**: Domain-specific exceptions

#### Application Layer
- **Use Cases**: Business logic (SearchReservations)
- **Ports**: Interfaces for external dependencies

#### Infrastructure Layer
- **Adapters**: External service implementations
- **MCP**: Protocol implementation
- **Utils**: Cross-cutting concerns

### Design Patterns
- **Dependency Injection**: Easy testing and maintenance
- **Repository Pattern**: Data access abstraction
- **Strategy Pattern**: Pluggable implementations
- **Factory Pattern**: Object creation

## Security

### Implemented Security Measures
- **Input Validation**: Pydantic schemas for all inputs
- **Error Handling**: Sanitized error responses
- **Credential Management**: Secure environment variable handling
- **Request Validation**: Comprehensive parameter validation

### Security Best Practices
1. Never commit credentials to version control
2. Use environment variables for sensitive data
3. Validate all inputs
4. Implement proper error handling
5. Use HTTPS for API communications
6. Monitor and log security events

## External Resources

### MCP Documentation
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [MCP Concepts](https://modelcontextprotocol.io/docs/concepts)
  - [Tools](https://modelcontextprotocol.io/docs/concepts/tools)
  - [Resources](https://modelcontextprotocol.io/docs/concepts/resources)
  - [Prompts](https://modelcontextprotocol.io/docs/concepts/prompts)
  - [Transports](https://modelcontextprotocol.io/docs/concepts/transports)

### Python Resources
- [FastMCP Documentation](https://gofastmcp.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [HTTPX Documentation](https://www.python-httpx.org)

---

# Contributing

We welcome contributions!

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Run linting and fix issues
7. Submit a pull request

### Code Style
- Python with type hints
- Black code formatting
- Flake8 linting
- Comprehensive test coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
