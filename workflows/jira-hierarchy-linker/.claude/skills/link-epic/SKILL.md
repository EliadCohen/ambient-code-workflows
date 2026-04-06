---
name: link-epic
description: Link an epic to an initiative with safety validations
---

# Link Epic Skill

Create an epic→initiative link in Jira with comprehensive safety checks and decision recording.

## Process

### 1. Run Analysis (if not already done)

If user invoked `/link-epic` directly without prior analysis:
- Call the analyze-epic skill first
- Get top recommendations

If analysis was already performed in this conversation:
- Use those results

### 2. Safety Validations

#### Check Existing Parent Link

Use `jira_get_issue` to fetch the epic and check for existing parent/initiative link.

If epic already has a parent link:
```
⚠️ WARNING: Epic {EPIC_KEY} is already linked to Initiative {EXISTING_INITIATIVE}

Current link:
Epic: {EPIC_KEY} "{EPIC_SUMMARY}"
  → Initiative: {EXISTING_INITIATIVE} "{EXISTING_INITIATIVE_SUMMARY}"

Do you want to:
1. Keep existing link (cancel)
2. Replace with new initiative (specify which)
3. Show analysis to compare options
```

**IMPORTANT:** Do NOT overwrite existing links without explicit user confirmation.

#### Verify Target Initiative

- Verify the target initiative exists in Jira
- Verify it's actually an Initiative issue type
- Verify it's not in a Done/Closed state (warn if it is)

### 3. Confirm with User

Show clear confirmation prompt with all details:

```markdown
## Ready to Link Epic to Initiative

**Epic:** {EPIC_KEY} "{EPIC_SUMMARY}"
  ↓
**Initiative:** {INITIATIVE_KEY} "{INITIATIVE_SUMMARY}"

**Match Details:**
- Overall Score: {SCORE}%
- Confidence: {CONFIDENCE_LEVEL}
- Reasoning: {SHORT_REASONING}

**Current Status:**
- Existing initiative link: {YES/NO}
- Initiative status: {STATUS}

Confirm link creation?
```

Use `AskUserQuestion` tool with options:
- "Yes, create the link" (proceed)
- "No, cancel" (abort)
- "Show alternatives" (display full analysis again)

### 4. Create Link

Once confirmed, create the parent link using:

#### Create Issue Link

```
Use jira_create_issue_link MCP tool:
- inward_issue: {EPIC_KEY}
- outward_issue: {INITIATIVE_KEY}
- link_type: "Parent" or "Relates" (depending on Jira configuration)
```

Common link types for epic→initiative:
- "Parent" (most common)
- "Initiative-Epic Link"
- "Relates"
- Check your Jira instance's link type configuration

Handle errors gracefully and provide clear error messages.

### 5. Record Decision (for Learning)

Save decision data to:
`artifacts/jira-hierarchy-linker/decisions/epic-{EPIC_KEY}-{TIMESTAMP}.json`

Format:
```json
{
  "timestamp": "2026-04-06T15:30:00Z",
  "decision_type": "epic_to_initiative",
  "epic_key": "PROJ-100",
  "epic_summary": "User Management Platform",
  "candidates": [
    {
      "initiative_key": "PROJ-10",
      "initiative_summary": "Customer Experience Transformation",
      "scores": {
        "summary": 38,
        "description": 28,
        "labels": 17,
        "comments": 9,
        "overall": 92
      },
      "reasoning": "Strong strategic alignment on customer-facing improvements...",
      "selected": true
    },
    {
      "initiative_key": "PROJ-11",
      "initiative_summary": "Security & Compliance Initiative",
      "scores": {
        "summary": 25,
        "description": 22,
        "labels": 15,
        "comments": 6,
        "overall": 68
      },
      "reasoning": "User management has security aspects...",
      "selected": false
    }
  ],
  "selected_initiative": "PROJ-10",
  "user_reasoning": "",
  "auto_linked": false,
  "replaced_existing": false
}
```

### 6. Log Link Creation

Create a human-readable report at:
`artifacts/jira-hierarchy-linker/links/link-epic-{EPIC_KEY}-{TIMESTAMP}.md`

Format:
```markdown
# Link Created: Epic → Initiative

**Date:** {TIMESTAMP}

## Link Details

**Epic:** {EPIC_KEY} "{EPIC_SUMMARY}"
  ↓
**Initiative:** {INITIATIVE_KEY} "{INITIATIVE_SUMMARY}"

## Match Analysis

- **Overall Score:** {SCORE}%
- **Confidence:** {CONFIDENCE_LEVEL}

**Dimension Scores:**
- Summary: {SCORE}/40
- Description: {SCORE}/30
- Labels/Components: {SCORE}/20
- Comments: {SCORE}/10

**Reasoning:**
{DETAILED_REASONING}

## Action Taken

- Link type used: {LINK_TYPE}
- Replaced existing link: {YES/NO}
- Previous initiative: {INITIATIVE_KEY if replaced, else "None"}

## Link

View in Jira: {JIRA_URL}/browse/{EPIC_KEY}
```

### 7. Confirm Success

Present success message:

```markdown
✅ **Link Created Successfully**

Epic {EPIC_KEY} is now linked to Initiative {INITIATIVE_KEY}

📊 Match score: {SCORE}% ({CONFIDENCE_LEVEL})
📝 Decision recorded for learning
🔗 View: {JIRA_URL}/browse/{EPIC_KEY}

**Next Steps:**
- Link another epic with `/link-epic <key>`
- Analyze a story with `/analyze-story <key>`
- View summary with `/summary`
```

## Error Handling

**Link creation failed:**
```
❌ Error creating link: {ERROR_MESSAGE}

The analysis and decision have been saved. You can try:
1. Check Jira permissions
2. Verify parent link type configuration in your Jira instance
3. Create the link manually in Jira
4. Contact your Jira admin if the issue persists

Decision saved to: artifacts/jira-hierarchy-linker/decisions/...
```

**Invalid initiative key:**
```
❌ Error: Initiative {INITIATIVE_KEY} not found or is not an Initiative issue type.

Please verify the initiative key and try again.
```

**Link type not supported:**
```
❌ Error: Could not determine correct link type for epic→initiative relationship.

Your Jira instance may use a custom link type. Please check your Jira
configuration or create the link manually.

Supported types tried: "Parent", "Initiative-Epic Link", "Relates"
```

## Safety Rules (CRITICAL)

- **NEVER** overwrite existing links without explicit user confirmation
- **ALWAYS** verify both epic and initiative exist before creating link
- **ALWAYS** save decision data for learning (even if link fails)
- **ALWAYS** provide clear confirmation prompts
- **NEVER** proceed if safety validations fail

## Return Control to Controller

After link creation (success or failure), read `.claude/skills/controller/SKILL.md`
and follow its guidance for recommending next steps.
