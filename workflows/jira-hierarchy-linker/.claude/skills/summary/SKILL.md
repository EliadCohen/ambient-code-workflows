---
name: summary
description: Generate comprehensive summary of workflow activity and learning insights
---

# Summary Skill

Scan all workflow artifacts and present a synthesized summary of linking activity, match patterns, and learning insights.

## Process

### 1. Scan All Artifacts

Read all files in artifacts/jira-hierarchy-linker/:

**Configuration:**
- `config.json` - Project scope and settings

**Analyses:**
- `analyses/story-*.md` - Story analysis results
- `analyses/epic-*.md` - Epic analysis results

**Decisions:**
- `decisions/story-*.json` - Story linking decisions
- `decisions/epic-*.json` - Epic linking decisions

**Links:**
- `links/link-story-*.md` - Created story→epic links
- `links/link-epic-*.md` - Created epic→initiative links

**Reports:**
- `reports/bulk-*.md` - Bulk operation reports

### 2. Calculate Statistics

From decisions/*.json, calculate:

**Overall Activity:**
- Total analyses performed
- Total links created
- Success rate (links created vs. attempted)

**Match Quality:**
- Average match score across all links
- Distribution by confidence level (>90%, 70-90%, 50-70%, <50%)
- Highest/lowest scoring matches

**Dimension Analysis:**
- Average scores per dimension (summary, description, labels, comments)
- Which dimensions had highest correlation with user selection

**Project Coverage:**
- Which projects were analyzed
- Number of items per project
- Most active projects

### 3. Detect Learning Patterns

Analyze decision data to find patterns:

#### Pattern 1: Dimension Preference

Compare selected vs. non-selected candidates:
- Do selected epics have consistently higher component scores?
- Is summary similarity less important than expected?
- Are certain labels predictive of selection?

Example insight:
```
📊 PATTERN DETECTED: Component Alignment Preference

Users selected matches with avg component score of 18/20, even when
summary scores were moderate (avg 28/40).

Current weights: Summary 40%, Components 20%
Suggested weights: Summary 30%, Components 30%
```

#### Pattern 2: Confidence Calibration

Check if confidence levels match user selection:
- Do "auto-link" candidates (>90%) get selected?
- Are "weak" matches (<50%) ever selected?
- Is the threshold well-calibrated?

#### Pattern 3: Project-Specific Patterns

- Do certain projects have consistent matching patterns?
- Are some epics/initiatives frequently selected?
- Are there "hub" epics that attract many stories?

### 4. Identify Recommendations

Based on patterns, suggest improvements:

**Weighting Adjustments:**
```
💡 Suggested weighting adjustment:
- Summary: 40% → 30%
- Description: 30% → 25%
- Labels/Components: 20% → 35%
- Comments: 10% → 10%

Reason: Users consistently prefer component alignment over title similarity
```

**Process Improvements:**
```
💡 Workflow insights:
- 3 stories were linked to same epic (PROJ-100) - consider bulk linking
- Epic PROJ-200 has 0 stories - may need decomposition
- Initiative PROJ-10 covers 5 epics - verify scope isn't too broad
```

### 5. Generate Summary Report

Create comprehensive summary at:
`artifacts/jira-hierarchy-linker/reports/summary-{TIMESTAMP}.md`

Format:

```markdown
# Jira Hierarchy Linker - Workflow Summary

**Generated:** {TIMESTAMP}
**Session Duration:** {DURATION}

## Activity Overview

### Links Created

- **Total:** {TOTAL} links
- **Stories → Epics:** {STORY_COUNT}
- **Epics → Initiatives:** {EPIC_COUNT}
- **Success Rate:** {SUCCESS_RATE}%

### Analyses Performed

- **Stories analyzed:** {STORY_ANALYSIS_COUNT}
- **Epics analyzed:** {EPIC_ANALYSIS_COUNT}
- **Bulk operations:** {BULK_COUNT}

## Match Quality

### Score Distribution

| Confidence Level | Count | Percentage |
|------------------|-------|------------|
| Auto-link (>90%) | {COUNT} | {PCT}% |
| Strong (70-90%) | {COUNT} | {PCT}% |
| Possible (50-70%) | {COUNT} | {PCT}% |
| Weak (<50%) | {COUNT} | {PCT}% |

**Average Match Score:** {AVG_SCORE}%

### Dimension Performance

| Dimension | Avg Score | Max | Min |
|-----------|-----------|-----|-----|
| Summary | {AVG}/40 | {MAX} | {MIN} |
| Description | {AVG}/30 | {MAX} | {MIN} |
| Labels/Components | {AVG}/20 | {MAX} | {MIN} |
| Comments | {AVG}/10 | {MAX} | {MIN} |

## Project Coverage

| Project | Stories Linked | Epics Linked | Total |
|---------|----------------|--------------|-------|
| PROJ | {COUNT} | {COUNT} | {TOTAL} |
| TEAM | {COUNT} | {COUNT} | {TOTAL} |

## Top Matches

### Highest Scoring Links

1. **PROJ-123 → PROJ-100** (95%) - "Add login" → "Auth System"
2. **PROJ-200 → PROJ-10** (92%) - "User Mgmt" → "CX Transform"
3. **PROJ-124 → PROJ-100** (88%) - "Password reset" → "Auth System"

### Hub Analysis

**Most Linked Epics:**
- PROJ-100 "Auth System" (12 stories)
- PROJ-101 "Security" (8 stories)

**Most Linked Initiatives:**
- PROJ-10 "CX Transform" (5 epics)

## Learning Insights

{PATTERN_INSIGHTS}

### Suggested Improvements

{RECOMMENDATIONS}

## Session Configuration

**Projects Scoped:** {PROJECTS}
**Additional Filters:** {FILTERS if any}
**Jira Instance:** {JIRA_URL}

## Artifacts Location

All files saved to: `artifacts/jira-hierarchy-linker/`

- Analyses: {ANALYSIS_COUNT} files
- Decisions: {DECISION_COUNT} files
- Links: {LINK_COUNT} files
- Reports: {REPORT_COUNT} files
```

### 6. Present Summary to User

Show concise summary with highlights:

```markdown
# 📊 Workflow Summary

## Activity
- ✅ **{TOTAL} links created**
  - {STORY_COUNT} stories → epics
  - {EPIC_COUNT} epics → initiatives
- 📈 Average match score: **{AVG_SCORE}%**
- 🎯 Success rate: **{SUCCESS_RATE}%**

## Insights

{TOP_3_INSIGHTS}

## Next Steps

- 📄 Full report: artifacts/jira-hierarchy-linker/reports/summary-{TIMESTAMP}.md
- 🔄 Continue linking with /analyze-story or /analyze-epic
- 📦 Process batch with /bulk-link

Would you like to:
- Review the full report
- Continue linking more items
- Adjust matching weights based on patterns
```

## Handling Empty State

If no activity yet:

```markdown
# 📊 Workflow Summary

No linking activity yet in this session.

## Getting Started

Use these commands to start organizing your backlog:
- `/analyze-story <key>` - Find epic matches for a story
- `/analyze-epic <key>` - Find initiative matches for an epic
- `/bulk-link <keys>` - Process multiple items at once

**Example:**
/analyze-story PROJ-123
```

## Learning Data Export

Optionally offer to export learning data:

```json
{
  "session_summary": {
    "total_links": 15,
    "avg_score": 82,
    "success_rate": 93,
    "patterns": [...]
  },
  "dimension_weights": {
    "current": {"summary": 40, "description": 30, "labels": 20, "comments": 10},
    "suggested": {"summary": 30, "description": 25, "labels": 35, "comments": 10}
  },
  "all_decisions": [...]
}
```

## Return Control to Controller

After presenting summary, read `.claude/skills/controller/SKILL.md` and follow
its guidance for recommending next steps.
