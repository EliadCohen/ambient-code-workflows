# Bulk Link Operation Report

**Date:** {TIMESTAMP}
**Items Processed:** {TOTAL_ITEMS}
**Successful:** {SUCCESS_COUNT}
**Failed:** {FAIL_COUNT}
**Duration:** {DURATION}

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total links attempted | {TOTAL} |
| Successful | {SUCCESS_COUNT} |
| Failed | {FAIL_COUNT} |
| Success rate | {SUCCESS_RATE}% |
| Average match score | {AVG_SCORE}% |
| Processing time | {DURATION} |

## Links Created

### Stories → Epics

| Story | Summary | Epic | Summary | Score | Status |
|-------|---------|------|---------|-------|--------|
| {STORY_KEY} | {STORY_SUMMARY} | {EPIC_KEY} | {EPIC_SUMMARY} | {SCORE}% | ✅ Created |
| {STORY_KEY} | {STORY_SUMMARY} | {EPIC_KEY} | {EPIC_SUMMARY} | {SCORE}% | ✅ Created |
| ... | ... | ... | ... | ... | ... |

**Subtotal:** {STORY_LINK_COUNT} story links created

### Epics → Initiatives

| Epic | Summary | Initiative | Summary | Score | Status |
|------|---------|------------|---------|-------|--------|
| {EPIC_KEY} | {EPIC_SUMMARY} | {INITIATIVE_KEY} | {INITIATIVE_SUMMARY} | {SCORE}% | ✅ Created |
| {EPIC_KEY} | {EPIC_SUMMARY} | {INITIATIVE_KEY} | {INITIATIVE_SUMMARY} | {SCORE}% | ✅ Created |
| ... | ... | ... | ... | ... | ... |

**Subtotal:** {EPIC_LINK_COUNT} epic links created

## Failed Links

{If any failures:}

| Item | Target | Error | Reason |
|------|--------|-------|--------|
| {ITEM_KEY} | {TARGET_KEY} | {ERROR_TYPE} | {ERROR_MESSAGE} |
| ... | ... | ... | ... |

**Total failures:** {FAIL_COUNT}

## Match Quality Distribution

| Confidence Level | Count | Percentage |
|------------------|-------|------------|
| Auto-link (>90%) | {COUNT} | {PCT}% |
| Strong (70-90%) | {COUNT} | {PCT}% |
| Possible (50-70%) | {COUNT} | {PCT}% |
| Weak (<50%) | {COUNT} | {PCT}% |

## Warnings & Notices

{If any:}

- ⚠️ {COUNT} items had existing links that were replaced
- ⚠️ {COUNT} items had scores below 70% threshold
- ℹ️ {COUNT} items required manual confirmation

## Learning Data

All {SUCCESS_COUNT} successful decisions recorded to:
`artifacts/jira-hierarchy-linker/decisions/`

This data will improve future match recommendations.

## Project Coverage

| Project | Links Created | Average Score |
|---------|---------------|---------------|
| {PROJECT} | {COUNT} | {AVG}% |
| ... | ... | ... |

## Next Steps

- ✅ Review created links in Jira
- 🔄 Retry failed items individually if needed
- 📊 View overall summary with `/summary`
- 🔍 Analyze more items with `/analyze-story` or `/analyze-epic`

---

**Report saved to:** artifacts/jira-hierarchy-linker/reports/bulk-{timestamp}.md
