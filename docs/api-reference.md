# API Reference

Complete reference for the focused MCP features provided by the TrackHS MCP Connector.

This server follows MCP best practices by providing a focused set of tools, prompts, and resources specifically for reservation and folio management functionality.

## Tools

### search_reservations (V2 - Primary)

**Description**: Advanced reservation search using TrackHS API V2 with comprehensive filtering options

**Parameters**:
- `page` (integer, optional): Page number (default: 1, 1-based pagination)
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

### search_units

**Description**: Search units in Track HS Channel API with comprehensive filtering options

**Parameters**:
- `page` (integer, optional): Page number (default: 1, 1-based pagination)
- `size` (integer, optional): Page size (default: 25, max: 1000)
- `sort_column` (string, optional): Sort field (id, name, nodeName, unitTypeName)
- `sort_direction` (string, optional): Sort order (asc/desc)
- `search` (string, optional): Text search in names/descriptions
- `node_id` (string, optional): Node ID(s) - single int, comma-separated, or array
- `amenity_id` (string, optional): Amenity ID(s) - single int, comma-separated, or array
- `unit_type_id` (string, optional): Unit type ID(s) - single int, comma-separated, or array
- `bedrooms` (integer, optional): Exact number of bedrooms
- `bathrooms` (integer, optional): Exact number of bathrooms
- `pets_friendly` (integer, optional): Pet friendly units (0/1)
- `is_active` (integer, optional): Active units (0/1)
- `is_bookable` (integer, optional): Bookable units (0/1)
- `arrival` (string, optional): Arrival date (ISO 8601)

### search_amenities

**Description**: Search amenities in Track HS Channel API with comprehensive filtering options

**Parameters**:
- `page` (integer, optional): Page number (default: 1, 1-based pagination)
- `size` (integer, optional): Page size (default: 25, max: 1000)
- `sort_column` (string, optional): Sort field (id, order, isPublic, publicSearchable, isFilterable, createdAt)
- `sort_direction` (string, optional): Sort order (asc/desc)
- `search` (string, optional): Text search in id and/or name
- `group_id` (integer, optional): Filter by group ID
- `is_public` (integer, optional): Public amenities (0/1)
- `public_searchable` (integer, optional): Publicly searchable amenities (0/1)
- `is_filterable` (integer, optional): Filterable amenities (0/1)

**Important Notes**:
- **Pagination**: Uses 1-based pagination (page=1 is the first page, not page=0)
- **Parameter Types**: All numeric and boolean parameters accept both integers and strings (automatic conversion)
- **Boolean Values**: Use 0 or 1 (not true/false)
- **Date Format**: All dates must be in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)

**Example Usage**:
```json
{
  "name": "search_amenities",
  "arguments": {
    "is_public": 1,
    "public_searchable": 1,
    "sort_column": "order",
    "sort_direction": "asc"
  }
}
```

**Response**:
```json
{
  "_embedded": {
    "amenities": [
      {
        "id": 1,
        "name": "Swimming Pool",
        "order": 1,
        "isPublic": true,
        "publicSearchable": true,
        "isFilterable": true,
        "groupId": 5
      }
    ]
  },
  "page": 1,
  "page_count": 2,
  "page_size": 25,
  "total_items": 45
}
```

### create_maintenance_work_order

**Description**: Create a new maintenance work order in TrackHS

**Required Parameters**:
- `date_received` (string, required): Date received in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
- `priority` (integer, required): Priority (1=Low, 3=Medium, 5=High)
- `status` (string, required): Work order status (open, not-started, in-progress, completed, etc.)
- `summary` (string, required): Brief summary of the work order
- `estimated_cost` (number, required): Estimated cost (>= 0)
- `estimated_time` (integer, required): Estimated time in minutes (> 0)

**Optional Parameters**:
- `date_scheduled` (string, optional): Scheduled date in ISO 8601 format
- `user_id` (integer, optional): Responsible user ID
- `vendor_id` (integer, optional): Assigned vendor ID
- `unit_id` (integer, optional): Related unit ID
- `reservation_id` (integer, optional): Related reservation ID
- `reference_number` (string, optional): External reference number
- `description` (string, optional): Detailed description
- `work_performed` (string, optional): Work performed description
- `source` (string, optional): Source of the order
- `source_name` (string, optional): Source contact name
- `source_phone` (string, optional): Source contact phone
- `actual_time` (integer, optional): Actual time spent in minutes
- `block_checkin` (boolean, optional): Whether to block check-in

**Valid Statuses**:
- `open`: Open
- `not-started`: Not Started
- `in-progress`: In Progress
- `completed`: Completed
- `processed`: Processed
- `vendor-assigned`: Assigned to Vendor
- `vendor-accepted`: Accepted by Vendor
- `vendor-rejected`: Rejected by Vendor
- `vendor-completed`: Completed by Vendor
- `cancelled`: Cancelled

**Example Usage**:
```json
{
  "name": "create_maintenance_work_order",
  "arguments": {
    "date_received": "2024-01-15T10:30:00Z",
    "priority": 5,
    "status": "open",
    "summary": "Repair air conditioning",
    "estimated_cost": 150.00,
    "estimated_time": 120,
    "unit_id": 101,
    "description": "AC not cooling properly"
  }
}
```

**Response**:
```json
{
  "success": true,
  "work_order": {
    "id": 12345,
    "dateReceived": "2024-01-15T10:30:00Z",
    "priority": 5,
    "status": "open",
    "summary": "Repair air conditioning",
    "estimatedCost": 150.00,
    "estimatedTime": 120,
    "unitId": 101,
    "createdAt": "2024-01-15T10:30:00Z"
  },
  "message": "Orden de trabajo creada exitosamente"
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

MCP Resources proporcionan información estructurada sobre schemas, documentación y ejemplos para todas las herramientas disponibles.

### Schemas

#### trackhs://schema/reservations-v2
Complete schema for Search Reservations API V2 with all parameters and validation rules.

#### trackhs://schema/reservation-detail-v2
Complete schema for Get Reservation V2 API with embedded data structures.

#### trackhs://schema/folio
Complete schema for Folios API with financial breakdown information.

#### trackhs://schema/units
Complete schema for Units API with 50+ fields and filtering options.

#### trackhs://schema/amenities
Complete schema for Amenities API with group and visibility options.

#### trackhs://schema/work-orders
Complete schema for Work Orders API with required/optional fields and valid statuses.

### Documentation

#### trackhs://docs/api-v2
Essential documentation for Reservations API V2 including parameters, examples, and best practices.

#### trackhs://docs/folio-api
Essential documentation for Folios API including financial data structures.

#### trackhs://docs/amenities-api
Essential documentation for Amenities API including filtering and sorting options.

#### trackhs://docs/work-orders-api
Essential documentation for Work Orders API including status workflow and validation rules.

### Examples

#### trackhs://examples/search-queries
Common search query examples for reservations including date ranges, filters, and scroll mode.

#### trackhs://examples/folio-operations
Common folio operation examples including balance checks and financial analysis.

#### trackhs://examples/amenities
Common amenity query examples including public/filterable amenities and group searches.

#### trackhs://examples/work-orders
Common work order creation examples including different priorities, statuses, and use cases.

### References

#### trackhs://reference/status-values
Valid values for reservation status parameters.

#### trackhs://reference/date-formats
Supported date formats for API parameters (ISO 8601).

#### trackhs://reference/error-codes
Common error codes and their meanings.

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
