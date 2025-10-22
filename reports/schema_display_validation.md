# Search Reservations V2 Schema Display Validation

**Generated:** 2024-01-15T10:00:00Z

## Summary

This validation ensures that the search_reservations_v2 schema displays correctly to the host and that all types are properly defined.

## Type Validation Results

### Required Fields
- `page`
- `size`
- `sort_column`
- `sort_direction`

### Optional Fields
- `search`
- `tags`
- `node_id`
- `unit_id`
- `contact_id`
- `travel_agent_id`
- `campaign_id`
- `user_id`
- `unit_type_id`
- `rate_type_id`
- `reservation_type_id`
- `booked_start`
- `booked_end`
- `arrival_start`
- `arrival_end`
- `departure_start`
- `departure_end`
- `updated_since`
- `status`
- `in_house_today`
- `group_id`
- `checkin_office_id`
- `scroll`

## Schema Example

```json
{
  "tool_name": "search_reservations",
  "description": "Search reservations in Track HS API with advanced filtering and pagination",
  "parameters": {
    "page": {
      "type": "integer",
      "default": 0,
      "description": "Page number (0-based indexing). Max total results: 10,000.",
      "minimum": 0,
      "maximum": 10000
    },
    "size": {
      "type": "integer",
      "default": 10,
      "description": "Number of results per page (1-100)",
      "minimum": 1,
      "maximum": 100
    },
    "sort_column": {
      "type": "string",
      "default": "name",
      "description": "Column to sort by. Valid values: name, status, altConf, agreementStatus, type, guest, guests, unit, units, checkin, checkout, nights. Disabled when using scroll.",
      "enum": [
        "name",
        "status",
        "altConf",
        "agreementStatus",
        "type",
        "guest",
        "guests",
        "unit",
        "units",
        "checkin",
        "checkout",
        "nights"
      ]
    },
    "sort_direction": {
      "type": "string",
      "default": "asc",
      "description": "Sort direction: 'asc' or 'desc'. Disabled when using scroll.",
      "enum": [
        "asc",
        "desc"
      ]
    },
    "search": {
      "type": "string",
      "description": "Full-text search in reservation names, guest names, and descriptions",
      "maxLength": 200
    },
    "status": {
      "type": "string",
      "description": "Filter by reservation status. Comma-separated values: 'Confirmed,Cancelled'. Valid statuses: Hold, Confirmed, Cancelled, Checked In, Checked Out",
      "enum": [
        "Hold",
        "Confirmed",
        "Checked Out",
        "Checked In",
        "Cancelled"
      ]
    },
    "in_house_today": {
      "type": "integer",
      "description": "Filter by in-house today (0=not in house, 1=in house)",
      "minimum": 0,
      "maximum": 1
    },
    "scroll": {
      "type": "string",
      "description": "Elasticsearch scroll for large datasets. Use '1' to start a new scroll, or provide the scroll ID from previous response to continue. Disables sorting when active."
    }
  }
}
```

## Recommendations

### 1. Use more specific types for better validation

**Priority:** medium

**Description:** Consider using Literal types for enum values and more specific Optional types

**Example:**
```python
status: Optional[Literal['Hold', 'Confirmed', 'Checked Out', 'Checked In', 'Cancelled']]
```

### 2. Add more detailed examples in descriptions

**Priority:** low

**Description:** Include more examples in field descriptions to help users understand usage

**Example:**
```python
Add examples like 'Example: status=Confirmed,Cancelled'
```

