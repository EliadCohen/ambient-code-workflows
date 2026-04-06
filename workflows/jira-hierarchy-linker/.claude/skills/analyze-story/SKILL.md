---
name: analyze-story
description: Analyze a story and find matching epics using semantic similarity
---

# Analyze Story Skill

Find the best epic matches for a Jira story using AI-powered semantic analysis.

## Process

### 1. Load Configuration

Read artifacts/jira-hierarchy-linker/config.json for project scope.

If missing, ask user which project(s) to search and create the config file.

### 2. Fetch Story Details

Use the `jira_get_issue` MCP tool with the provided Jira key.

Extract from the story:
- Summary (title)
- Description (full text)
- Labels
- Components
- Comments (if available)
- Current Epic Link (if exists - for safety check)

### 3. Fetch Candidate Epics

Use `jira_search_issues` MCP tool with JQL:

```jql
project IN ({PROJECTS}) AND issuetype = Epic AND status != Done
```

Get full details for each epic (summary, description, labels, components).

Limit to top 50 epics if more exist (for performance).

### 4. Perform Semantic Analysis

For each epic candidate, analyze alignment across 4 dimensions:

#### a) Summary Alignment (40 points max)

Compare story summary with epic summary:
- Do titles describe related work?
- Are they in the same feature area?
- Do they share key terminology?
- Are they solving aspects of the same problem?

Score 0-40 based on semantic similarity and thematic alignment.

#### b) Description Alignment (30 points max)

Compare story description with epic description:
- Do detailed contexts overlap?
- Are they solving related problems?
- Do they reference similar systems, components, or technical concepts?
- Is there shared technical or business context?

Score 0-30 based on detailed content overlap.

#### c) Labels/Components Alignment (20 points max)

Compare structural metadata:
- Count shared labels (each shared label = +5 points, max 15)
- Count shared components (each shared component = +5 points, max 15)
- Normalize to 0-20 scale

If no labels/components exist, score based on semantic category alignment.

#### d) Comments Alignment (10 points max)

Compare discussion themes (if comments available):
- Discussion topics overlap?
- Mentioned stakeholders in common?
- Related concerns or decisions?

Score 0-10 based on conversational context overlap.

#### e) Calculate Weighted Score

Overall score = (summary_score) + (description_score) + (labels_score) + (comments_score)

Maximum possible: 100 points

#### f) Generate Reasoning

For each epic match, provide specific evidence:
- Quote shared terminology from summaries
- Identify overlapping technical concepts from descriptions
- List shared labels/components
- Note discussion theme overlaps

Example reasoning:
```
Strong alignment on user authentication theme. Story mentions "login flow" 
and epic describes "authentication system overhaul". Shared components: 
auth-service, user-api. Both tagged with "security" and "backend" labels.
```

### 5. Apply Learning Adjustments (Optional)

If decision files exist in artifacts/jira-hierarchy-linker/decisions/:

1. Read all decision JSON files
2. Analyze patterns:
   - Which dimension scores correlate with user selections?
   - Does user prefer high component alignment over summary similarity?
   - Are certain label combinations predictive?
3. Adjust scoring weights if clear pattern detected
4. Note the adjustment in output

Example pattern:
```
LEARNING INSIGHT: Analyzed 12 previous decisions. Users selected epics with
high component alignment (avg 18/20) even when summary scores were moderate
(avg 25/40). Boosting component weight from 20% to 30%, reducing summary from
40% to 30%.
```

### 6. Rank and Present

1. Sort candidates by overall score (descending)
2. Show top 5 matches
3. For each match, display:
   - Epic key and summary
   - Overall score and confidence level
   - Dimension breakdown (summary/description/labels/comments)
   - Specific reasoning
   - Recommendation (auto-link candidate, strong, possible, weak)

4. Save detailed analysis to:
   `artifacts/jira-hierarchy-linker/analyses/story-{KEY}-{timestamp}.md`

Use the template at templates/match-analysis.md for formatting.

### 7. Safety Checks

Before presenting results:
- Verify story key exists (catch invalid keys)
- Check if story already has an epic link
  - If yes, include WARNING in output
  - Show current epic for comparison
- Verify at least one candidate epic was found
  - If zero epics, suggest checking project configuration

## Output Format

Present results in this structure:

```markdown
# Match Analysis: {STORY_KEY} "{STORY_SUMMARY}"

## Story Details
- **Key:** {STORY_KEY}
- **Summary:** {STORY_SUMMARY}
- **Current Epic:** {EPIC_KEY if exists, else "None"}
- **Analysis Date:** {TIMESTAMP}

## Top Epic Matches

### 1. {EPIC_KEY} "{EPIC_SUMMARY}" — {SCORE}% ({CONFIDENCE})

**Reasoning:**
- **Summary:** {explanation} ({score}/40)
- **Description:** {explanation} ({score}/30)
- **Labels/Components:** {explanation} ({score}/20)
- **Comments:** {explanation} ({score}/10)
- **Overall:** {total}/100

**Recommendation:** {Auto-link candidate (>90%) | Strong match | Possible match | Weak match}

### 2. {EPIC_KEY} "{EPIC_SUMMARY}" — {SCORE}% ({CONFIDENCE})
[...]

## Next Steps

✅ Use `/link-story {STORY_KEY}` to create the link to top match
🔍 Review alternatives above and specify epic manually
🔄 Analyze another story with `/analyze-story <key>`
```

## Confidence Level Mapping

- 90-100: "Auto-link candidate" (suggest immediate linking)
- 70-89: "Strong match" (high confidence)
- 50-69: "Possible match" (moderate confidence)
- 0-49: "Weak match" (low confidence, review carefully)

## Error Handling

**Story not found:**
```
❌ Error: Story {KEY} not found in Jira.
Please verify the key and try again.
```

**No epics found:**
```
⚠️ No active epics found in project(s): {PROJECTS}

Suggestions:
- Verify project configuration in artifacts/jira-hierarchy-linker/config.json
- Check if epics exist with status != Done
- Expand search to include completed epics if needed
```

**Story already linked:**
```
⚠️ WARNING: Story {KEY} is already linked to Epic {EXISTING_EPIC}

Current Epic: {EXISTING_EPIC_KEY} "{EXISTING_EPIC_SUMMARY}"

Showing alternative matches anyway for comparison...
```

## Return Control to Controller

After presenting results, read `.claude/skills/controller/SKILL.md` and follow
its guidance for recommending next steps.
