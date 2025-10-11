# API Reference

Complete reference for all MCP features provided by the TrackHS MCP Connector.

## Tools

### search_reservations

**Description**: Advanced reservation search with comprehensive filtering options

**Parameters**:
- `date_from` (string, optional): Start date for search (YYYY-MM-DD)
- `date_to` (string, optional): End date for search (YYYY-MM-DD)
- `booked_from` (string, optional): Booking date start (YYYY-MM-DD)
- `booked_to` (string, optional): Booking date end (YYYY-MM-DD)
- `arrival_from` (string, optional): Arrival date start (YYYY-MM-DD)
- `arrival_to` (string, optional): Arrival date end (YYYY-MM-DD)
- `departure_from` (string, optional): Departure date start (YYYY-MM-DD)
- `departure_to` (string, optional): Departure date end (YYYY-MM-DD)
- `node_ids` (string, optional): Comma-separated node IDs
- `unit_ids` (string, optional): Comma-separated unit IDs
- `contact_ids` (string, optional): Comma-separated contact IDs
- `folio_ids` (string, optional): Comma-separated folio IDs
- `reservation_ids` (string, optional): Comma-separated reservation IDs
- `text` (string, optional): Text search across reservation fields
- `status` (string, optional): Reservation status filter
- `tags` (string, optional): Comma-separated tags
- `in_house_today` (boolean, optional): Filter for in-house today
- `sort_by` (string, optional): Sort field (default: "created_at")
- `sort_order` (string, optional): Sort order ("asc" or "desc")
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 50)
- `scroll_id` (string, optional): Elasticsearch scroll ID for pagination

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

## Resources

### trackhs://schema/reservations

**Description**: Complete schema for Track HS reservations

**Content**: JSON schema defining reservation structure, fields, and validation rules

**Usage**: Access via MCP resource system for understanding data structure

### trackhs://api/v2/endpoints

**Description**: Available API endpoints in Track HS V2

**Content**: List of all available endpoints with descriptions and parameters

**Usage**: Reference for API integration and development

### trackhs://api/v2/parameters

**Description**: API parameters documentation

**Content**: Detailed parameter descriptions, types, and validation rules

**Usage**: Understanding parameter requirements and constraints

### trackhs://api/v2/examples

**Description**: Usage examples for Track HS API V2

**Content**: Code examples and usage patterns

**Usage**: Learning how to use the API effectively

### trackhs://status/system

**Description**: System status and connectivity information

**Content**: Current system status, API connectivity, and health metrics

**Usage**: Monitoring system health and connectivity

### trackhs://docs/api

**Description**: Complete API documentation

**Content**: Comprehensive API documentation with examples

**Usage**: Full reference for API usage and integration

## Prompts

### check-today-reservations

**Description**: Check reservations for today using API V2

**Arguments**:
- `node_id` (string, optional): Specific node to check
- `include_departures` (boolean, optional): Include departing guests
- `include_arrivals` (boolean, optional): Include arriving guests

**Example**:
```
Use the check-today-reservations prompt to see today's reservations for node 123.
```

### advanced-reservation-search

**Description**: Advanced reservation search with multiple filters

**Arguments**:
- `date_range` (string, optional): Date range for search
- `filters` (object, optional): Additional search filters
- `sort_options` (object, optional): Sorting preferences

**Example**:
```
Use advanced-reservation-search to find all confirmed reservations for next month, sorted by arrival date.
```

### reservation-analytics

**Description**: Generate analytics and insights from reservation data

**Arguments**:
- `date_range` (string, optional): Analysis period
- `metrics` (array, optional): Specific metrics to calculate
- `group_by` (string, optional): Grouping criteria

**Example**:
```
Use reservation-analytics to analyze occupancy rates for the past quarter, grouped by property.
```

### guest-experience-analysis

**Description**: Analyze guest experience and satisfaction

**Arguments**:
- `reservation_ids` (array, optional): Specific reservations to analyze
- `time_period` (string, optional): Analysis time period
- `focus_areas` (array, optional): Specific areas to focus on

**Example**:
```
Use guest-experience-analysis to understand guest satisfaction trends over the past year.
```

### financial-analysis

**Description**: Perform financial analysis on reservation data

**Arguments**:
- `date_range` (string, optional): Analysis period
- `revenue_metrics` (array, optional): Specific revenue metrics
- `cost_analysis` (boolean, optional): Include cost analysis

**Example**:
```
Use financial-analysis to calculate revenue per available room (RevPAR) for the current month.
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
