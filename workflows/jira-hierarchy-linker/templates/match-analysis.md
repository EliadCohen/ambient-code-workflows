# Match Analysis: {ISSUE_KEY} "{SUMMARY}"

**Analysis Date:** {TIMESTAMP}
**Issue Type:** {Story|Epic}
**Target Type:** {Epic|Initiative}
**Current Link:** {CURRENT_LINK if exists, else "None"}

## Top Matches

### 1. {MATCH_KEY} "{MATCH_SUMMARY}" — {SCORE}% ({CONFIDENCE_LEVEL})

**Reasoning:**
- **Summary:** {EXPLANATION} ({SUMMARY_SCORE}/40)
- **Description:** {EXPLANATION} ({DESC_SCORE}/30)
- **Labels/Components:** {EXPLANATION} ({LABELS_SCORE}/20)
- **Comments:** {EXPLANATION} ({COMMENTS_SCORE}/10)
- **Overall:** {TOTAL_SCORE}/100

**Recommendation:** {Auto-link candidate (>90%) | Strong match (70-90%) | Possible match (50-70%) | Weak match (<50%)}

---

### 2. {MATCH_KEY} "{MATCH_SUMMARY}" — {SCORE}% ({CONFIDENCE_LEVEL})

**Reasoning:**
- **Summary:** {EXPLANATION} ({SUMMARY_SCORE}/40)
- **Description:** {EXPLANATION} ({DESC_SCORE}/30)
- **Labels/Components:** {EXPLANATION} ({LABELS_SCORE}/20)
- **Comments:** {EXPLANATION} ({COMMENTS_SCORE}/10)
- **Overall:** {TOTAL_SCORE}/100

**Recommendation:** {CONFIDENCE_LEVEL}

---

### 3. {MATCH_KEY} "{MATCH_SUMMARY}" — {SCORE}% ({CONFIDENCE_LEVEL})

[...]

---

### 4. {MATCH_KEY} "{MATCH_SUMMARY}" — {SCORE}% ({CONFIDENCE_LEVEL})

[...]

---

### 5. {MATCH_KEY} "{MATCH_SUMMARY}" — {SCORE}% ({CONFIDENCE_LEVEL})

[...]

---

## Learning Insights

{If learning data exists, show detected patterns:}

**Pattern detected:** {PATTERN_DESCRIPTION}

**Current weights:** Summary {PCT}%, Description {PCT}%, Labels/Components {PCT}%, Comments {PCT}%
**Suggested weights:** {ADJUSTED_WEIGHTS if pattern detected}

---

## Next Steps

- ✅ Use `/link-{story|epic} {ISSUE_KEY}` to create the link
- 🔍 Review alternatives above if top match isn't ideal
- 🔄 Analyze another item with `/analyze-{story|epic} <key>`
- 📊 View workflow summary with `/summary`

---

**Analysis saved to:** artifacts/jira-hierarchy-linker/analyses/{type}-{KEY}-{timestamp}.md
