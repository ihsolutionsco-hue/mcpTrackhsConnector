# CLAUDE INSIGHTS

## 🎯 KEY FINDINGS

**Root Cause:** API expects camelCase params, we sent snake_case
- `is_active` → `isActive` ✅
- `min_bedrooms` → `minBedrooms` ✅

**Validator Bug:** Checked processed fields (snake_case) not original (camelCase)
- Fixed: `isActive` → `is_active` ✅

**Result:** All 3 critical bugs resolved with comprehensive testing suite
