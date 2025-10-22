# Search Reservations V2 Schema Analysis

**Generated:** 2024-01-15T10:00:00Z

## Summary

This analysis compares the official TrackHS API documentation with the current implementation to identify discrepancies and provide recommendations.

## Discrepancies Found

### 1. Size Limits

**Severity:** medium

**Description:** Different size limits in tool vs use case


### 2. Status Values

**Severity:** medium

**Description:** Status values differ between documentation and implementation


## Recommendations

### 1. Standardize page indexing

**Priority:** high

**Description:** Determine if page should be 0-based or 1-based and apply consistently

**Files to modify:**
- `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py`
- `src/trackhs_mcp/application/use_cases/search_reservations.py`

### 2. Unify size limits

**Priority:** medium

**Description:** Ensure size limits are consistent across tool and use case

**Files to modify:**
- `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py`
- `src/trackhs_mcp/application/use_cases/search_reservations.py`

### 3. Document altConf mapping

**Priority:** low

**Description:** Add comments explaining why altConf is mapped to altCon

**Files to modify:**
- `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py`

