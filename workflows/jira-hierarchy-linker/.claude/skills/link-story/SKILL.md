---
name: link-story
description: Link a story to an epic with safety validations
---

# Link Story Skill

Create a story→epic link in Jira with comprehensive safety checks and decision recording.

## Process

### 1. Run Analysis (if not already done)

If user invoked `/link-story` directly without prior analysis:
- Call the analyze-story skill first
- Get top recommendations

If analysis was already performed in this conversation:
- Use those results

### 2. Safety Validations

#### Check Existing Epic Link

Use `jira_get_issue` to fetch the story and check for existing Epic Link field.

If story already has an epic link:
```
⚠️ WARNING: Story {STORY_KEY} is already linked to Epic {EXISTING_EPIC}

Current link:
Story: {STORY_KEY} "{STORY_SUMMARY}"
  → Epic: {EXISTING_EPIC} "{EXISTING_EPIC_SUMMARY}"

Do you want to:
1. Keep existing link (cancel)
2. Replace with new epic (specify which)
3. Show analysis to compare options
```

**IMPORTANT:** Do NOT overwrite existing links without explicit user confirmation.

#### Verify Target Epic

- Verify the target epic exists in Jira
- Verify it's actually an Epic issue type
- Verify it's not in a Done/Closed state (warn if it is)

### 3. Confirm with User

Show clear confirmation prompt with all details:

```markdown
## Ready to Link Story to Epic

**Story:** {STORY_KEY} "{STORY_SUMMARY}"
  ↓
**Epic:** {EPIC_KEY} "{EPIC_SUMMARY}"

**Match Details:**
- Overall Score: {SCORE}%
- Confidence: {CONFIDENCE_LEVEL}
- Reasoning: {SHORT_REASONING}

**Current Status:**
- Existing epic link: {YES/NO}
- Epic status: {STATUS}

Confirm link creation?
```

Use `AskUserQuestion` tool with options:
- "Yes, create the link" (proceed)
- "No, cancel" (abort)
- "Show alternatives" (display full analysis again)

### 4. Create Link

Once confirmed, create the link using one of two methods:

#### Method A: Update Epic Link Field (preferred for Cloud Jira)

```
Use jira_update_issue MCP tool:
- issue_key: {STORY_KEY}
- fields: {"customfield_XXXXX": "{EPIC_KEY}"}
```

Note: Epic Link field ID varies by Jira instance. Try common field names:
- "Epic Link"
- "Parent"
- Check issue schema if needed

#### Method B: Create Issue Link

```
Use jira_create_issue_link MCP tool:
- inward_issue: {STORY_KEY}
- outward_issue: {EPIC_KEY}
- link_type: "Epic-Story Link" (or project-specific type)
```

Handle errors gracefully - if one method fails, try the other.

### 5. Record Decision (for Learning)

Save decision data to:
`artifacts/jira-hierarchy-linker/decisions/story-{STORY_KEY}-{TIMESTAMP}.json`

Format:
```json
{
  "timestamp": "2026-04-06T15:30:00Z",
  "decision_type": "story_to_epic",
  "story_key": "PROJ-123",
  "story_summary": "Add user authentication",
  "candidates": [
    {
      "epic_key": "PROJ-100",
      "epic_summary": "User Management Platform",
      "scores": {
        "summary": 35,
        "description": 27,
        "labels": 18,
        "comments": 8,
        "overall": 88
      },
      "reasoning": "Strong alignment on user management theme...",
      "selected": true
    },
    {
      "epic_key": "PROJ-101",
      "epic_summary": "Security Framework",
      "scores": {
        "summary": 28,
        "description": 25,
        "labels": 12,
        "comments": 5,
        "overall": 70
      },
      "reasoning": "Authentication is security-related...",
      "selected": false
    }
  ],
  "selected_epic": "PROJ-100",
  "user_reasoning": "",
  "auto_linked": false,
  "replaced_existing": false
}
```

### 6. Log Link Creation

Create a human-readable report at:
`artifacts/jira-hierarchy-linker/links/link-story-{STORY_KEY}-{TIMESTAMP}.md`

Format:
```markdown
# Link Created: Story → Epic

**Date:** {TIMESTAMP}

## Link Details

**Story:** {STORY_KEY} "{STORY_SUMMARY}"
  ↓
**Epic:** {EPIC_KEY} "{EPIC_SUMMARY}"

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

- Method used: {Epic Link field update / Issue link creation}
- Replaced existing link: {YES/NO}
- Previous epic: {EPIC_KEY if replaced, else "None"}

## Link

View in Jira: {JIRA_URL}/browse/{STORY_KEY}
```

### 7. Confirm Success

Present success message:

```markdown
✅ **Link Created Successfully**

Story {STORY_KEY} is now linked to Epic {EPIC_KEY}

📊 Match score: {SCORE}% ({CONFIDENCE_LEVEL})
📝 Decision recorded for learning
🔗 View: {JIRA_URL}/browse/{STORY_KEY}

**Next Steps:**
- Link another story with `/link-story <key>`
- Analyze an epic with `/analyze-epic <key>`
- View summary with `/summary`
```

## Error Handling

**Link creation failed:**
```
❌ Error creating link: {ERROR_MESSAGE}

The analysis and decision have been saved. You can try:
1. Check Jira permissions
2. Verify epic link field configuration
3. Create the link manually in Jira
4. Contact your Jira admin if the issue persists

Decision saved to: artifacts/jira-hierarchy-linker/decisions/...
```

**Invalid epic key:**
```
❌ Error: Epic {EPIC_KEY} not found or is not an Epic issue type.

Please verify the epic key and try again.
```

## Safety Rules (CRITICAL)

- **NEVER** overwrite existing links without explicit user confirmation
- **ALWAYS** verify both story and epic exist before creating link
- **ALWAYS** save decision data for learning (even if link fails)
- **ALWAYS** provide clear confirmation prompts
- **NEVER** proceed if safety validations fail

## Return Control to Controller

After link creation (success or failure), read `.claude/skills/controller/SKILL.md`
and follow its guidance for recommending next steps.
