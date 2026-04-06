# Jira Hierarchy Linker Workflow

AI-powered assistant for linking Jira stories to epics and epics to initiatives using semantic similarity analysis.

## Phases

1. **/analyze-story** - Find epic matches for a story using AI semantic analysis
2. **/analyze-epic** - Find initiative matches for an epic using AI semantic analysis
3. **/link-story** - Create story→epic link with safety validations
4. **/link-epic** - Create epic→initiative link with safety validations
5. **/bulk-link** - Process multiple items efficiently in batch
6. **/summary** - Generate workflow summary and learning insights

All phases implemented as skills at `.claude/skills/{name}/SKILL.md`

Controller at `.claude/skills/controller/SKILL.md` manages phase transitions and supports both conversational and command modes

Artifacts go in `artifacts/jira-hierarchy-linker/`

## Principles

- **Safety first**: Always check existing links, never overwrite without explicit confirmation
- **Transparency**: Provide clear reasoning for every match recommendation with specific evidence
- **Learning**: Record all decisions to improve future matches through pattern detection
- **Validation**: Verify Jira keys exist and user has permissions before taking action
- **User control**: Always confirm before creating links, especially in bulk operations

## Hard Limits

- **NEVER** create links without user confirmation
- **NEVER** overwrite existing links without explicit approval
- **NEVER** skip safety validations in bulk operations
- **NEVER** assume project scope (always ask or use saved config)
- **NEVER** proceed if Jira MCP connection fails

## Semantic Matching

Uses Claude's native understanding (no external embeddings or vector databases):

**Weighted scoring:**
- Summary alignment (40%): Title/headline semantic similarity
- Description overlap (30%): Detailed context matching
- Labels/Components (20%): Categorical alignment
- Comments themes (10%): Discussion overlap

Provides explainable reasoning for every match with specific evidence.

**Confidence levels:**
- 90-100%: Auto-link candidate (suggest immediate linking)
- 70-89%: Strong match (high confidence)
- 50-69%: Possible match (moderate confidence)
- 0-49%: Weak match (review carefully)

## Configuration

### Required Environment Variables

Jira MCP server requires:
- `JIRA_URL` - Jira instance URL (e.g., https://yourcompany.atlassian.net)
- `JIRA_EMAIL` - User's Jira email address
- `JIRA_API_TOKEN` - Jira API token (create at Jira account settings)

### Project Scope

On first interaction, workflow asks user which Jira project(s) to search.

Configuration saved to `artifacts/jira-hierarchy-linker/config.json` for session reuse:

```json
{
  "projects": ["PROJ1", "PROJ2"],
  "additional_filters": "AND component = backend"
}
```

## Safety Validations

All linking operations include:

1. **Existence checks** - Verify all Jira keys exist
2. **Type validation** - Ensure issue types are correct (Story, Epic, Initiative)
3. **Link detection** - Check for existing links before creating
4. **Permission verification** - Confirm user can modify issues
5. **Confirmation gates** - Require explicit approval before creating links
6. **Error handling** - Graceful failure with clear error messages

## Learning Mechanism

### Decision Recording

Every link creation (successful or failed) is recorded as JSON in `artifacts/jira-hierarchy-linker/decisions/`:

```json
{
  "timestamp": "2026-04-06T15:30:00Z",
  "decision_type": "story_to_epic",
  "story_key": "PROJ-123",
  "candidates": [...],
  "selected": "PROJ-100",
  "scores": {...}
}
```

### Pattern Detection

Workflow analyzes decision history to detect patterns:
- Which dimensions correlate with user selections?
- Are component matches more important than summary similarity?
- Are certain labels predictive of good matches?

### Weight Adjustment

When clear patterns emerge, workflow suggests adjusted weights:
```
Pattern detected: Users prefer component alignment over summary similarity
Suggested: Summary 30% (was 40%), Components 35% (was 20%)
```

## Conversational vs Command Mode

### Command Mode (Explicit)

```
/analyze-story PROJ-123
/link-story PROJ-123
/analyze-epic PROJ-456
/link-epic PROJ-456
/bulk-link PROJ-1,PROJ-2,PROJ-3
/summary
```

### Conversational Mode (Natural Language)

```
"Find an epic for story PROJ-123"
"Link this epic to an initiative: PROJ-456"
"Organize these stories: PROJ-1, PROJ-2, PROJ-3"
"Show me what we've linked so far"
```

Controller detects intent and dispatches to appropriate phase.

## Error Handling

Workflow handles errors gracefully:

**Jira connection issues:**
- Clear error messages if MCP server fails
- Guidance on checking environment variables
- No silent failures

**Invalid keys:**
- Validate before analysis
- Suggest corrections if similar keys found
- Don't fail entire batch for one invalid key

**Permission errors:**
- Clear message if user lacks permissions
- Suggest checking Jira roles
- Continue with items user can modify (in bulk)

**API rate limits:**
- Cache epic/initiative lists per project
- Batch queries when possible
- Handle gracefully if limits reached

## Workflow Outputs

All artifacts saved to `artifacts/jira-hierarchy-linker/`:

```
artifacts/jira-hierarchy-linker/
├── config.json                    # Session configuration
├── analyses/                      # Match analysis results
│   ├── story-PROJ-123-*.md
│   └── epic-PROJ-456-*.md
├── decisions/                     # Decision data (JSON)
│   ├── story-PROJ-123-*.json
│   └── epic-PROJ-456-*.json
├── links/                         # Link creation reports
│   ├── link-story-PROJ-123-*.md
│   └── link-epic-PROJ-456-*.md
└── reports/                       # Summary reports
    ├── bulk-*.md
    └── summary-*.md
```

## Quality Standards

### Analysis Quality

- Always show top 5 matches (not just #1)
- Provide specific evidence for reasoning
- Show dimension breakdown
- Flag existing links
- Save detailed analysis to artifacts

### Link Creation Quality

- Confirm before creating
- Record decision data
- Log creation details
- Handle errors gracefully
- Return control to controller

### Bulk Operations Quality

- Validate all keys first
- Show batch preview
- Flag items below thresholds
- Progress indicators
- Comprehensive reporting

## Working With Different Jira Instances

Workflow supports both Jira Cloud and Jira Server/Data Center:

**Cloud:**
- Use API token authentication
- Epic Link via custom field
- Standard issue link types

**Server/Data Center:**
- May use different authentication
- Check epic link field ID
- Verify custom link types

Workflow attempts multiple methods and adapts to instance configuration.

## Tips for Best Results

1. **Start with project configuration** - Tell workflow which projects to search
2. **Review top matches** - Don't just accept #1, consider alternatives
3. **Provide feedback** - If matches seem off, say why
4. **Use bulk operations** - More efficient than one-at-a-time for multiple items
5. **Check summary periodically** - See patterns and adjust if needed
6. **Validate field configuration** - Ensure Epic Link field is properly configured in Jira

## Troubleshooting

**"No matches found":**
- Verify project scope includes target items
- Check if epics/initiatives are active (status != Done)
- Try broader project search

**"Link creation failed":**
- Check Jira permissions
- Verify field configuration (Epic Link custom field)
- Try manual link to test permissions

**"Low match scores":**
- Items may be poorly described
- Consider manual linking
- Add more labels/components to improve future matches

**"MCP connection failed":**
- Check environment variables (JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN)
- Verify network connectivity
- Test credentials in Jira web UI
