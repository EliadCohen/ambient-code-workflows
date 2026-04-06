# Jira Hierarchy Linker

AI-powered workflow for organizing Jira backlogs by linking stories to epics and epics to initiatives using semantic similarity analysis.

## Overview

Manually linking hundreds of stories to the right epics is tedious and error-prone. This workflow uses Claude's semantic understanding to analyze issue content and recommend the best matches, making backlog organization fast and accurate.

**What it does:**
- Analyzes story/epic content using AI to find semantically similar epics/initiatives
- Recommends top 5 matches with scores and reasoning
- Safely creates links with validation and confirmation
- Learns from your decisions to improve future recommendations
- Supports bulk operations for efficiency

**What makes it unique:**
- No external embeddings or vector databases required
- Explainable recommendations with specific evidence
- Learns and adapts to your preferences
- Safety-first approach prevents accidental overwrites
- Works conversationally or via slash commands

## Quick Start

### Prerequisites

1. **Jira Access**
   - Jira Cloud or Server/Data Center instance
   - Valid API token ([create one](https://id.atlassian.com/manage-profile/security/api-tokens))
   - Permissions to view and edit issues

2. **Environment Setup**
   Set these environment variables:
   ```bash
   export JIRA_URL="https://yourcompany.atlassian.net"
   export JIRA_EMAIL="your.email@company.com"
   export JIRA_API_TOKEN="your-api-token-here"
   ```

### Basic Usage

1. **Start the workflow** in ACP
2. **Configure project scope** when prompted (e.g., "PROJ" or "TEAM")
3. **Analyze and link items:**

   ```
   /analyze-story PROJ-123
   ```
   
   Claude shows top 5 epic matches with scores and reasoning
   
   ```
   /link-story PROJ-123
   ```
   
   Creates the link after confirmation

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/analyze-story <key>` | Find epic matches for a story | `/analyze-story PROJ-123` |
| `/analyze-epic <key>` | Find initiative matches for an epic | `/analyze-epic PROJ-456` |
| `/link-story <key>` | Analyze and link story to epic | `/link-story PROJ-123` |
| `/link-epic <key>` | Analyze and link epic to initiative | `/link-epic PROJ-456` |
| `/bulk-link <keys>` | Process multiple items at once | `/bulk-link PROJ-1,PROJ-2,PROJ-3` |
| `/summary` | View workflow summary and insights | `/summary` |

## Conversational Mode

You can also use natural language:

- "Find a parent epic for story PROJ-123"
- "Link this epic to an initiative: PROJ-456"
- "Organize these stories: PROJ-1, PROJ-2, PROJ-3"
- "Show me what we've linked so far"

The controller detects your intent and dispatches to the appropriate phase.

## How It Works

### Semantic Matching

The workflow analyzes 4 dimensions to calculate match scores:

1. **Summary Alignment (40%)** - Do titles describe related work?
2. **Description Overlap (30%)** - Are detailed contexts similar?
3. **Labels/Components (20%)** - Shared categorical metadata?
4. **Comments Themes (10%)** - Discussion topics overlap?

Each match gets a 0-100 score with specific reasoning:

```
### PROJ-100 "User Management Platform" — 88% (Strong)

Reasoning:
- Summary: Strong alignment on user management theme (35/40)
  Both focus on user-facing authentication features
- Description: Shared auth-service component references (27/30)
  Similar technical approach to session handling
- Labels: Shared tags: security, backend, user-mgmt (18/20)
- Comments: PM mentioned authentication requirements (8/10)
- Overall: 88/100

Recommendation: Strong match - create link
```

### Confidence Levels

| Score | Level | Recommendation |
|-------|-------|----------------|
| 90-100% | Auto-link candidate | Create link immediately (with confirmation) |
| 70-89% | Strong match | High confidence, recommended |
| 50-69% | Possible match | Moderate confidence, review carefully |
| 0-49% | Weak match | Low confidence, manual review needed |

### Learning & Adaptation

The workflow records every decision you make and analyzes patterns:

**Example pattern detection:**
```
📊 PATTERN DETECTED: Component Alignment Preference

After 15 decisions, users consistently select matches with high
component scores (avg 18/20) even when summary scores are moderate.

Adjusting weights:
- Summary: 40% → 30%
- Components: 20% → 30%

This should improve future match quality.
```

## Workflow Phases

### 1. Analysis Phase

**analyze-story** or **analyze-epic**
- Fetches issue details from Jira
- Searches for candidate epics/initiatives in configured projects
- Performs semantic analysis across 4 dimensions
- Ranks candidates by match score
- Presents top 5 with reasoning
- Saves analysis to artifacts

### 2. Linking Phase

**link-story** or **link-epic**
- Runs analysis if not already done
- Checks for existing links (safety validation)
- Confirms with user before creating link
- Creates link via Jira MCP server
- Records decision for learning
- Logs creation details

### 3. Bulk Phase

**bulk-link**
- Accepts comma-separated Jira keys
- Validates all keys first
- Analyzes each item
- Shows batch preview with scores
- Confirms before creating all links
- Processes sequentially with progress
- Generates comprehensive report

### 4. Summary Phase

**summary**
- Scans all workflow artifacts
- Calculates statistics (total links, avg scores, success rate)
- Detects learning patterns
- Suggests weight adjustments
- Presents insights and recommendations

## Safety Features

### Before Creating Links

✅ Validates Jira key exists
✅ Checks issue type is correct
✅ Detects existing links
✅ Verifies user permissions
✅ Requires explicit confirmation

### During Bulk Operations

✅ Validates all keys before starting
✅ Shows complete batch preview
✅ Flags items below confidence thresholds
✅ Handles errors gracefully (one failure doesn't stop batch)
✅ Comprehensive reporting

### Never

❌ Overwrites existing links without confirmation
❌ Silently skips items
❌ Proceeds if validations fail
❌ Creates links without user approval

## Output Artifacts

All workflow data saved to `artifacts/jira-hierarchy-linker/`:

```
artifacts/jira-hierarchy-linker/
├── config.json                    # Project scope configuration
├── analyses/                      # Match analysis results
│   ├── story-PROJ-123-20260406.md
│   └── epic-PROJ-456-20260406.md
├── decisions/                     # Decision data for learning (JSON)
│   ├── story-PROJ-123-20260406.json
│   └── epic-PROJ-456-20260406.json
├── links/                         # Link creation reports
│   ├── link-story-PROJ-123-20260406.md
│   └── link-epic-PROJ-456-20260406.md
└── reports/                       # Summary and bulk reports
    ├── bulk-20260406.md
    └── summary-20260406.md
```

## Example Workflow

### Scenario: Organize 10 authentication stories

1. **Start workflow**
   ```
   User: "I need to organize 10 authentication stories"
   Claude: "Which Jira project should I search?"
   User: "PROJ"
   ```

2. **Bulk analysis**
   ```
   /bulk-link PROJ-121,PROJ-122,PROJ-123,...,PROJ-130
   ```

3. **Review preview**
   ```
   Ready to create 10 links:
   
   ✅ PROJ-121 → PROJ-100 "Auth System" (92% - Auto-link)
   ✅ PROJ-122 → PROJ-100 "Auth System" (88% - Strong)
   ✅ PROJ-123 → PROJ-100 "Auth System" (85% - Strong)
   ...
   
   Proceed with all?
   ```

4. **Confirm and create**
   ```
   User: "Yes"
   Claude: [Creates 10 links with progress updates]
   ✅ Bulk Link Complete
   Created: 10/10 links
   Average score: 87%
   ```

5. **Review summary**
   ```
   /summary
   
   📊 Workflow Summary
   - 10 links created (all stories → PROJ-100)
   - Average match score: 87%
   - Pattern: All auth stories naturally cluster to Auth epic
   ```

## Configuration

### Project Scope

On first use, specify which Jira project(s) to search:

```json
{
  "projects": ["PROJ", "TEAM"],
  "additional_filters": "AND component = backend"
}
```

Saved to `artifacts/jira-hierarchy-linker/config.json` and reused for session.

### Jira Instance Compatibility

**Jira Cloud:**
- Standard API token authentication
- Epic Link custom field
- Standard issue link types

**Jira Server/Data Center:**
- May require different auth configuration
- Check Epic Link field ID in instance
- Verify custom link type names

Workflow auto-detects and adapts to instance configuration.

## Troubleshooting

### "MCP connection failed"

**Cause:** Jira MCP server not connecting

**Fix:**
1. Verify environment variables are set:
   ```bash
   echo $JIRA_URL
   echo $JIRA_EMAIL
   echo $JIRA_API_TOKEN
   ```
2. Test credentials in Jira web UI
3. Check API token hasn't expired
4. Verify network connectivity

### "No matches found"

**Cause:** No epics/initiatives found in configured projects

**Fix:**
1. Verify project configuration in `config.json`
2. Check if epics exist with `status != Done`
3. Try expanding search to more projects
4. Verify issue types exist (some projects don't use Initiatives)

### "Link creation failed"

**Cause:** Permission or field configuration issue

**Fix:**
1. Check Jira permissions (need edit access)
2. Verify Epic Link field exists and is visible
3. Try creating link manually in Jira to test
4. Contact Jira admin if field is missing

### "Low match scores across all candidates"

**Cause:** Issues lack detailed descriptions or shared metadata

**Fix:**
1. Add more labels and components to issues
2. Write more detailed descriptions
3. Consider manual linking for poorly described items
4. Use bulk operations to build up learning data

## Advanced Features

### Custom JQL Filters

Add additional JQL filters to narrow search:

```json
{
  "projects": ["PROJ"],
  "additional_filters": "AND component = auth AND status IN (Open, 'In Progress')"
}
```

### Weight Adjustment

Workflow suggests weight changes based on patterns. You can also manually adjust by providing feedback:

```
"I prefer component matches over title similarity"
```

Workflow will note this and adjust weighting.

### Export Learning Data

Request learning data export to analyze patterns:

```
/summary

[In summary output, learning data is included]
```

## Best Practices

1. **Configure project scope first** - Saves time by focusing search
2. **Review top 5, not just #1** - Consider alternatives before linking
3. **Use bulk operations** - Much faster for multiple items
4. **Check summary periodically** - See if patterns emerge
5. **Provide rich metadata** - Labels and components improve matching
6. **Write clear descriptions** - Better context = better matches

## Support

For issues or questions:
- Check CLAUDE.md for detailed workflow documentation
- Review artifacts/ for decision history and reports
- See WORKSPACE_NAVIGATION_GUIDELINES.md for file navigation tips

## License

Part of the Ambient Code Platform workflows repository.
