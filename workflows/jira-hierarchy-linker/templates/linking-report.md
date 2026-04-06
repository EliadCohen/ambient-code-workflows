# Link Created: {STORY|EPIC} → {EPIC|INITIATIVE}

**Date:** {TIMESTAMP}
**Type:** {Story→Epic | Epic→Initiative}

## Link Details

**{Source Type}:** {SOURCE_KEY} "{SOURCE_SUMMARY}"
  ↓
**{Target Type}:** {TARGET_KEY} "{TARGET_SUMMARY}"

## Match Analysis

- **Overall Score:** {SCORE}%
- **Confidence Level:** {CONFIDENCE_LEVEL}

### Dimension Scores

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Summary | {SCORE} | 40 | {BRIEF_NOTE} |
| Description | {SCORE} | 30 | {BRIEF_NOTE} |
| Labels/Components | {SCORE} | 20 | {BRIEF_NOTE} |
| Comments | {SCORE} | 10 | {BRIEF_NOTE} |
| **Total** | **{TOTAL}** | **100** | |

### Reasoning

{DETAILED_REASONING}

## Action Taken

- **Method:** {Epic Link field update | Parent link creation | Issue link}
- **Replaced existing link:** {YES/NO}
- **Previous link:** {TARGET_KEY if replaced, else "None"}
- **Link type:** {LINK_TYPE if applicable}

## Verification

✅ Link created successfully in Jira

**View in Jira:** {JIRA_URL}/browse/{SOURCE_KEY}

---

## Decision Record

Decision data saved to: `artifacts/jira-hierarchy-linker/decisions/{type}-{SOURCE_KEY}-{timestamp}.json`

This decision will be used to improve future match recommendations.

---

**Report saved to:** artifacts/jira-hierarchy-linker/links/link-{type}-{SOURCE_KEY}-{timestamp}.md
