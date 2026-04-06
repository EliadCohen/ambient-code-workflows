---
name: analyze-epic
description: Analyze an epic and find matching initiatives using semantic similarity
---

# Analyze Epic Skill

Find the best initiative matches for a Jira epic using AI-powered semantic analysis.

## Process

### 1. Load Configuration

Read artifacts/jira-hierarchy-linker/config.json for project scope.

If missing, ask user which project(s) to search and create the config file.

### 2. Fetch Epic Details

Use the `jira_get_issue` MCP tool with the provided Jira key.

Extract from the epic:
- Summary (title)
- Description (full text)
- Labels
- Components
- Comments (if available)
- Current Parent Link (if exists - for safety check)

### 3. Fetch Candidate Initiatives

Use `jira_search_issues` MCP tool with JQL:

```jql
project IN ({PROJECTS}) AND issuetype = Initiative AND status != Done
```

Get full details for each initiative (summary, description, labels, components).

Limit to top 50 initiatives if more exist (for performance).

### 4. Perform Semantic Analysis

For each initiative candidate, analyze alignment across 4 dimensions:

#### a) Summary Alignment (40 points max)

Compare epic summary with initiative summary:
- Do titles describe related strategic work?
- Are they in the same product area or business objective?
- Do they share key strategic terminology?
- Are they part of the same larger initiative?

Score 0-40 based on semantic similarity and strategic alignment.

#### b) Description Alignment (30 points max)

Compare epic description with initiative description:
- Do strategic contexts overlap?
- Are they solving aspects of the same business problem?
- Do they reference similar product areas or customer segments?
- Is there shared business or strategic context?

Score 0-30 based on detailed content overlap.

#### c) Labels/Components Alignment (20 points max)

Compare structural metadata:
- Count shared labels (each shared label = +5 points, max 15)
- Count shared components (each shared component = +5 points, max 15)
- Normalize to 0-20 scale

If no labels/components exist, score based on semantic category alignment.

#### d) Comments Alignment (10 points max)

Compare discussion themes (if comments available):
- Strategic discussion topics overlap?
- Mentioned stakeholders in common?
- Related business objectives or decisions?

Score 0-10 based on conversational context overlap.

#### e) Calculate Weighted Score

Overall score = (summary_score) + (description_score) + (labels_score) + (comments_score)

Maximum possible: 100 points

#### f) Generate Reasoning

For each initiative match, provide specific evidence:
- Quote shared strategic terminology from summaries
- Identify overlapping business objectives from descriptions
- List shared labels/components
- Note discussion theme overlaps

Example reasoning:
```
Strong strategic alignment on customer onboarding improvements. Epic focuses
on "streamlined signup process" and initiative describes "enhance customer
acquisition funnel". Shared components: onboarding-service, user-portal.
Both tagged with "growth" and "customer-experience" labels.
```

### 5. Apply Learning Adjustments (Optional)

If decision files exist in artifacts/jira-hierarchy-linker/decisions/:

1. Read all decision JSON files (both story and epic decisions)
2. Analyze patterns specific to epic→initiative matching
3. Adjust scoring weights if clear pattern detected
4. Note the adjustment in output

### 6. Rank and Present

1. Sort candidates by overall score (descending)
2. Show top 5 matches
3. For each match, display:
   - Initiative key and summary
   - Overall score and confidence level
   - Dimension breakdown
   - Specific reasoning
   - Recommendation

4. Save detailed analysis to:
   `artifacts/jira-hierarchy-linker/analyses/epic-{KEY}-{timestamp}.md`

Use the template at templates/match-analysis.md for formatting.

### 7. Safety Checks

Before presenting results:
- Verify epic key exists and is type "Epic"
- Check if epic already has a parent initiative link
  - If yes, include WARNING in output
  - Show current initiative for comparison
- Verify at least one candidate initiative was found
  - If zero initiatives, suggest checking project configuration

## Output Format

Present results in this structure:

```markdown
# Match Analysis: {EPIC_KEY} "{EPIC_SUMMARY}"

## Epic Details
- **Key:** {EPIC_KEY}
- **Summary:** {EPIC_SUMMARY}
- **Current Initiative:** {INITIATIVE_KEY if exists, else "None"}
- **Analysis Date:** {TIMESTAMP}

## Top Initiative Matches

### 1. {INITIATIVE_KEY} "{INITIATIVE_SUMMARY}" — {SCORE}% ({CONFIDENCE})

**Reasoning:**
- **Summary:** {explanation} ({score}/40)
- **Description:** {explanation} ({score}/30)
- **Labels/Components:** {explanation} ({score}/20)
- **Comments:** {explanation} ({score}/10)
- **Overall:** {total}/100

**Recommendation:** {Auto-link candidate (>90%) | Strong match | Possible match | Weak match}

### 2. {INITIATIVE_KEY} "{INITIATIVE_SUMMARY}" — {SCORE}% ({CONFIDENCE})
[...]

## Next Steps

✅ Use `/link-epic {EPIC_KEY}` to create the link to top match
🔍 Review alternatives above and specify initiative manually
🔄 Analyze another epic with `/analyze-epic <key>`
```

## Confidence Level Mapping

- 90-100: "Auto-link candidate" (suggest immediate linking)
- 70-89: "Strong match" (high confidence)
- 50-69: "Possible match" (moderate confidence)
- 0-49: "Weak match" (low confidence, review carefully)

## Error Handling

**Epic not found:**
```
❌ Error: Epic {KEY} not found in Jira.
Please verify the key and try again.
```

**Issue is not an Epic:**
```
❌ Error: {KEY} is a {TYPE}, not an Epic.
This command only works with Epic issue types.
```

**No initiatives found:**
```
⚠️ No active initiatives found in project(s): {PROJECTS}

Suggestions:
- Verify project configuration
- Check if initiatives exist with status != Done
- Some projects may not use Initiative issue type
```

**Epic already linked:**
```
⚠️ WARNING: Epic {KEY} is already linked to Initiative {EXISTING_INITIATIVE}

Current Initiative: {EXISTING_INITIATIVE_KEY} "{EXISTING_INITIATIVE_SUMMARY}"

Showing alternative matches anyway for comparison...
```

## Return Control to Controller

After presenting results, read `.claude/skills/controller/SKILL.md` and follow
its guidance for recommending next steps.
