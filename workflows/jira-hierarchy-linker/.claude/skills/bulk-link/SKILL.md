---
name: bulk-link
description: Process multiple Jira items for linking with batch analysis and confirmation
---

# Bulk Link Skill

Analyze and link multiple stories or epics at once, with safety validations and batch confirmation.

## Process

### 1. Parse Input

Accept comma-separated Jira keys:
- `/bulk-link PROJ-123,PROJ-124,PROJ-125`
- Or from conversation: "Link these stories: PROJ-123, PROJ-124, PROJ-125"

Parse and clean the input:
- Split by comma
- Trim whitespace
- Validate format (PROJECT-NUMBER)

### 2. Validate All Keys

Before analysis, validate each key:

Use `jira_get_issue` for each key to:
- Verify key exists
- Determine issue type (Story, Epic, or other)
- Check current link status

Create validation summary:
```markdown
## Validation Results

✅ PROJ-123 - Story (no epic link)
✅ PROJ-124 - Story (no epic link)
⚠️  PROJ-125 - Story (already linked to PROJ-100)
✅ PROJ-200 - Epic (no initiative link)
❌ PROJ-999 - Not found
❌ PROJ-456 - Task (not Story or Epic, cannot link)

Valid for linking: 3 stories, 1 epic
Warnings: 1 already linked
Errors: 2 invalid
```

Ask user if they want to:
- Proceed with valid items only
- Fix errors and try again
- Cancel

### 3. Analyze All Items

For each valid item, run analysis:

**For stories:**
- Call analyze-story skill logic (don't announce each one)
- Collect top match for each

**For epics:**
- Call analyze-epic skill logic
- Collect top match for each

**Progress indicator:**
```
Analyzing 12 items...
[████████░░░░] 8/12 complete
```

### 4. Present Batch Summary

Show all proposed links with scores:

```markdown
## Bulk Link Preview

Ready to create 12 links:

### Stories → Epics

✅ PROJ-123 "Add login" → PROJ-100 "Auth System" (88% - Strong)
✅ PROJ-124 "Password reset" → PROJ-100 "Auth System" (82% - Strong)
⚠️  PROJ-125 "Session mgmt" → PROJ-101 "Security" (65% - Possible)
✅ PROJ-126 "OAuth integration" → PROJ-100 "Auth System" (91% - Auto-link)

### Epics → Initiatives

✅ PROJ-200 "User Management" → PROJ-10 "CX Transform" (89% - Strong)
✅ PROJ-201 "Access Control" → PROJ-11 "Security Init" (76% - Strong)

### Summary

- **Total:** 12 links
- **Strong matches (>70%):** 10
- **Moderate matches (50-70%):** 2
- **Weak matches (<50%):** 0

Items flagged for review:
- ⚠️  PROJ-125: Below 70% threshold (65%)
```

### 5. Confirm Batch

Use `AskUserQuestion` with options:

- **"Proceed with all"** - Create all links
- **"Proceed with strong only (>70%)"** - Skip moderate matches
- **"Review details"** - Show full analysis for each item
- **"Exclude specific items"** - Let user specify which to skip
- **"Cancel"** - Abort bulk operation

If "Review details" selected:
- Show detailed analysis for each item (like normal analyze output)
- Then re-ask for confirmation

If "Exclude specific items":
- Ask which keys to exclude
- Update summary
- Re-confirm

### 6. Execute Links

For each approved link:

**Sequential processing with progress:**
```
Creating links...
✅ [1/10] PROJ-123 → PROJ-100
✅ [2/10] PROJ-124 → PROJ-100
✅ [3/10] PROJ-126 → PROJ-100
⚠️  [4/10] PROJ-125 → PROJ-101 (user confirmed despite moderate score)
✅ [5/10] PROJ-200 → PROJ-10
...
```

**For each link:**
- Use link-story or link-epic skill logic
- Record decision (save JSON)
- Log creation
- Handle errors gracefully

**Error handling:**
- If one link fails, log the error
- Continue with remaining links
- Report all errors at the end

### 7. Generate Batch Report

Save comprehensive report to:
`artifacts/jira-hierarchy-linker/reports/bulk-{TIMESTAMP}.md`

Use template: templates/bulk-operations.md

Format:
```markdown
# Bulk Link Report

**Date:** {TIMESTAMP}
**Items Processed:** {TOTAL}
**Successful:** {SUCCESS_COUNT}
**Failed:** {FAIL_COUNT}

## Summary Statistics

- Total links attempted: {TOTAL}
- Successful: {SUCCESS_COUNT}
- Failed: {FAIL_COUNT}
- Average match score: {AVG_SCORE}%

## Links Created

### Stories → Epics

| Story | Epic | Score | Status |
|-------|------|-------|--------|
| PROJ-123 | PROJ-100 | 88% | ✅ Created |
| PROJ-124 | PROJ-100 | 82% | ✅ Created |
| PROJ-125 | PROJ-101 | 65% | ✅ Created |

### Epics → Initiatives

| Epic | Initiative | Score | Status |
|------|------------|-------|--------|
| PROJ-200 | PROJ-10 | 89% | ✅ Created |
| PROJ-201 | PROJ-11 | 76% | ✅ Created |

## Failed Links

| Item | Target | Error |
|------|--------|-------|
| PROJ-999 | - | Key not found |

## Learning Data

All decisions recorded to artifacts/jira-hierarchy-linker/decisions/

Total decisions recorded: {COUNT}
```

### 8. Present Results

Show success summary:

```markdown
✅ **Bulk Link Complete**

**Results:**
- ✅ Created: 11/12 links
- ❌ Failed: 1/12 links

**Performance:**
- Average match score: 82%
- Processing time: ~30 seconds

**Details:**
- Stories linked: 9
- Epics linked: 2
- All decisions recorded for learning

📊 Full report: artifacts/jira-hierarchy-linker/reports/bulk-{TIMESTAMP}.md

**Next Steps:**
- View summary with `/summary`
- Retry failed links individually
- Analyze more items with `/analyze-story` or `/analyze-epic`
```

## Safety Rules (CRITICAL)

- **ALWAYS** show batch summary before executing
- **ALWAYS** require explicit confirmation via `AskUserQuestion`
- **ALWAYS** validate all keys before analysis
- **Flag** items below 70% threshold for review
- **NEVER** silently skip items - always report what happened
- **HANDLE** errors gracefully - one failure shouldn't stop the batch
- **RECORD** all decisions for learning

## Performance Considerations

For large batches (>20 items):

1. **Pagination**
   - Process in chunks of 20
   - Show progress after each chunk
   - Allow user to cancel between chunks

2. **Caching**
   - Cache epic/initiative lists per project
   - Reuse for all items in same project
   - Saves Jira API calls

3. **Parallel Analysis** (if supported)
   - Analyze multiple items concurrently
   - Reduce total processing time

## Error Handling

**No valid items:**
```
❌ No valid items to process.

Issues found:
- PROJ-999: Not found
- PROJ-456: Task type (not Story or Epic)

Please provide valid Story or Epic keys.
```

**All items already linked:**
```
⚠️ All items already have links.

Do you want to:
1. Show current links for review
2. Re-link with different targets (will replace)
3. Cancel
```

**Batch partially failed:**
```
⚠️ Batch completed with errors.

Successful: 8/12
Failed: 4/12

Failed items:
- PROJ-789: Permission denied
- PROJ-790: Epic not found
- PROJ-791: Link creation failed
- PROJ-792: Network timeout

You can retry failed items individually or check your Jira permissions.
```

## Return Control to Controller

After batch completion, read `.claude/skills/controller/SKILL.md` and follow
its guidance for recommending next steps.
