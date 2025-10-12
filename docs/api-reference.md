# API Reference

Complete reference for the focused MCP features provided by the TrackHS MCP Connector.

This server follows MCP best practices by providing a focused set of tools, prompts, and resources specifically for reservation and folio management functionality.

## Tools

### search_reservations (V2 - Primary)

**Description**: Advanced reservation search using TrackHS API V2 with comprehensive filtering options

**Parameters**:
- `page` (integer, optional): Page number (default: 1)
- `size` (integer, optional): Page size (default: 10, max: 1000)
- `sort_column` (string, optional): Sort field (name, status, checkin, etc.)
- `sort_direction` (string, optional): Sort order (asc/desc)
- `search` (string, optional): Text search in names/descriptions
- `node_id` (string, optional): Node ID(s) - single int, comma-separated, or array
- `unit_id` (string, optional): Unit ID(s) - single int, comma-separated, or array
- `contact_id` (string, optional): Contact ID(s) - single int, comma-separated, or array
- `status` (string|array, optional): Reservation status(es)
- `arrival_start` (string, optional): Arrival date start (ISO 8601)
- `arrival_end` (string, optional): Arrival date end (ISO 8601)
- `departure_start` (string, optional): Departure date start (ISO 8601)
- `departure_end` (string, optional): Departure date end (ISO 8601)
- `booked_start` (string, optional): Booking date start (ISO 8601)
- `booked_end` (string, optional): Booking date end (ISO 8601)
- `scroll` (integer|string, optional): Elasticsearch scroll (1 to start)
- `in_house_today` (integer, optional): Filter by in-house today (0/1)

### search_reservations_v1 (V1 - Legacy)

**Description**: Legacy reservation search using TrackHS API V1 for compatibility

**Parameters**: Same as search_reservations but uses V1 endpoint

**Example Usage**:
```json
{
  "name": "search_reservations",
  "arguments": {
    "date_from": "2024-01-01",
    "date_to": "2024-12-31",
    "node_ids": "123,456,789",
    "status": "confirmed",
    "sort_by": "arrival_date",
    "sort_order": "asc"
  }
}
```

**Response**:
```json
{
  "reservations": [
    {
      "id": "12345",
      "arrival_date": "2024-01-15",
      "departure_date": "2024-01-20",
      "guest_name": "John Doe",
      "status": "confirmed",
      "total_amount": 500.00
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 500,
    "per_page": 50
  }
}
```

## Tools (Additional)

### get_folio

**Description**: Get a specific folio by ID with complete financial information

**Parameters**:
- `folio_id` (string, required): Unique folio ID

**Features**:
- Supports guest and master folio types
- Includes financial data (balances, commissions, revenue)
- Embedded contact, company, and travel agent information
- Master folio rules and exception handling

**Example Usage**:
```json
{
  "name": "get_folio",
  "arguments": {
    "folio_id": "12345"
  }
}
```

**Response**:
```json
{
  "id": 12345,
  "status": "open",
  "type": "guest",
  "currentBalance": 150.00,
  "realizedBalance": 100.00,
  "contactId": 1,
  "companyId": 1,
  "reservationId": 37165851,
  "travelAgentId": 1,
  "name": "Guest Folio - John Doe",
  "agentCommission": 10.00,
  "ownerCommission": 5.00,
  "ownerRevenue": 500.00,
  "checkInDate": "2024-01-15",
  "checkOutDate": "2024-01-20",
  "_embedded": {
    "contact": {
      "id": 1,
      "firstName": "John",
      "lastName": "Doe",
      "primaryEmail": "john@example.com"
    },
    "travelAgent": {
      "id": 1,
      "type": "agent",
      "name": "Travel Agency Inc"
    },
    "company": {
      "id": 1,
      "type": "company",
      "name": "Property Management Co"
    }
  }
}
```

## Resources

### trackhs://schema/reservations

**Description**: Complete schema for TrackHS reservations V2

**Content**: JSON schema defining reservation structure, fields, and validation rules

**Usage**: Access via MCP resource system for understanding data structure

### trackhs://api/documentation

**Description**: Complete API V2 documentation and examples

**Content**: Comprehensive API documentation with examples and usage patterns

**Usage**: Full reference for API usage and integration

## Prompts

### search-reservations-by-dates

**Description**: Search reservations by date range using API V2

**Arguments**:
- `start_date` (string, required): Start date (YYYY-MM-DD)
- `end_date` (string, required): End date (YYYY-MM-DD)
- `date_type` (string, optional): Type of date filter (arrival, departure, booked)

**Example**:
```
Use search-reservations-by-dates to find all reservations arriving between 2024-01-01 and 2024-01-31.
```

### search-reservations-by-guest

**Description**: Search reservations by guest information using API V2

**Arguments**:
- `guest_name` (string, optional): Guest name to search
- `contact_id` (string, optional): Specific contact ID
- `email` (string, optional): Guest email
- `phone` (string, optional): Guest phone number

**Example**:
```
Use search-reservations-by-guest to find all reservations for John Doe or contact ID 12345.
```

### search-reservations-advanced

**Description**: Advanced reservation search with multiple filters using API V2

**Arguments**:
- `search_term` (string, optional): Text search term
- `status` (string, optional): Reservation status filter
- `node_id` (string, optional): Node ID filter
- `unit_type_id` (string, optional): Unit type ID filter
- `include_financials` (boolean, optional): Include financial data
- `scroll_mode` (boolean, optional): Use scroll mode for large datasets

**Example**:
```
Use search-reservations-advanced to find all confirmed reservations in node 123 with financial details.
```

## Request/Response Examples

### Tool Request Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_reservations",
    "arguments": {
      "date_from": "2024-01-01",
      "date_to": "2024-01-31",
      "status": "confirmed",
      "sort_by": "arrival_date"
    }
  }
}
```

### Tool Response Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 25 confirmed reservations for January 2024"
      }
    ],
    "isError": false
  }
}
```

### Resource Request Example

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "trackhs://schema/reservations"
  }
}
```

### Resource Response Example

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "contents": [
      {
        "uri": "trackhs://schema/reservations",
        "mimeType": "application/json",
        "text": "{\"type\": \"object\", \"properties\": {...}}"
      }
    ]
  }
}
```

### Prompt Request Example

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "prompts/get",
  "params": {
    "name": "check-today-reservations",
    "arguments": {
      "node_id": "123"
    }
  }
}
```

### Prompt Response Example

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "description": "Check reservations for today using API V2",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Show me today's reservations for node 123, including arrivals and departures."
        }
      }
    ]
  }
}
```

## Error Handling

### Common Error Types

#### Authentication Errors

```json
{
  "error": {
    "code": -32000,
    "message": "Authentication failed",
    "data": {
      "type": "AuthenticationError",
      "details": "Invalid credentials provided"
    }
  }
}
```

#### Validation Errors

```json
{
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "type": "ValidationError",
      "details": "Invalid date format. Expected YYYY-MM-DD",
      "field": "date_from"
    }
  }
}
```

#### API Errors

```json
{
  "error": {
    "code": -32001,
    "message": "API request failed",
    "data": {
      "type": "ApiError",
      "details": "Track HS API returned 500 Internal Server Error",
      "status_code": 500
    }
  }
}
```

### Error Response Format

All errors follow the JSON-RPC 2.0 error format:

```json
{
  "jsonrpc": "2.0",
  "id": <request_id>,
  "error": {
    "code": <error_code>,
    "message": "<error_message>",
    "data": {
      "type": "<error_type>",
      "details": "<detailed_error_info>",
      "field": "<field_name_if_applicable>"
    }
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32000 | Authentication error |
| -32001 | API error |
| -32002 | Validation error |
| -32003 | Network error |
| -32004 | Timeout error |

## Rate Limiting

The server implements rate limiting to prevent abuse:

- **Requests per minute**: 100 (configurable)
- **Burst allowance**: 20 requests
- **Rate limit headers**: Included in responses

### Rate Limit Response

```json
{
  "error": {
    "code": -32005,
    "message": "Rate limit exceeded",
    "data": {
      "type": "RateLimitError",
      "retry_after": 60,
      "limit": 100,
      "remaining": 0
    }
  }
}
```

## Security

### Authentication

- **Bearer token authentication** for API requests
- **Credential validation** on startup
- **Secure credential storage** via environment variables

### Input Validation

- **Parameter validation** using Pydantic schemas
- **Type checking** for all inputs
- **Range validation** for numeric parameters
- **Format validation** for date strings

### Error Sanitization

- **Sensitive data removal** from error messages
- **Stack trace filtering** in production
- **Log sanitization** for security

## Performance

### Response Times

- **Tool calls**: < 2 seconds average
- **Resource access**: < 1 second average
- **Prompt generation**: < 500ms average

### Caching

- **Schema caching** for resources
- **Configuration caching** for settings
- **Response caching** for repeated requests

### Optimization

- **Connection pooling** for API requests
- **Async processing** for concurrent operations
- **Memory optimization** for large datasets
