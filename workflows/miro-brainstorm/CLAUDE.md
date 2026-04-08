# Miro Brainstorm Workflow Guidelines

## Miro MCP Integration

You have access to Miro through the MCP server. **Always check that Miro is authenticated before starting.** If not, guide the user to run `/mcp` to connect.

## Monitoring Best Practices

### When to Monitor

- Start monitoring only when user explicitly requests it
- Default interval: 1 minute (can be adjusted)
- Continue until user says "stop", "done", or "that's enough"

### What to Monitor

Check for these item types:
- `sticky_note` - Most common for brainstorming
- `card` - Sometimes used
- `text` - Freeform text items

### Handling New Ideas

When you find a new idea:
1. Announce it briefly to the user
2. Analyze for difficulty (Low/Medium/Insane)
3. Add to tracking table
4. Continue monitoring

**Don't:** Over-explain every detail. Keep updates concise.

## Difficulty Assessment Context

Always consider the domain context when assessing difficulty. For example:
- **Agentic workflows**: Consider AI/ML complexity, infrastructure needs, team expertise
- **Web development**: Consider frontend/backend split, API design, database schema
- **DevOps**: Consider pipeline complexity, infrastructure provisioning, security

## Theme Clustering

### Semantic Analysis Approach

1. Read all ideas completely first
2. Look for patterns in:
   - Technology stack (databases, AI/ML, APIs)
   - Purpose (security, performance, user experience)
   - Scope (foundation, advanced features)
   - Dependencies (what builds on what)
3. Create 4-8 themes (not too few, not too many)
4. Use descriptive names with emoji

### Visual Organization

- Create theme marker documents on the board
- Use different colors/emoji for easy identification
- Create dependency flowcharts to show relationships
- Position markers near related sticky notes

## Report Generation

### Jira Item Guidelines

**Epics:**
- Major themes requiring multiple stories
- 3+ months of work
- Clear business value

**Stories:**
- 2-5 sprint features
- User-facing value
- Can be demo'd

**Spikes:**
- Research/investigation work
- Timeboxed (5 days typical)
- Produces decisions, not features

**Tasks:**
- 1 sprint or less
- Technical work
- Can be completed by one person

### Report Structure

Always include:
1. Executive summary with key recommendations
2. Dependency diagram (ASCII art or description)
3. Detailed Jira items with acceptance criteria
4. Implementation roadmap by quarter
5. Risk register
6. Budget estimates if relevant
7. Team capacity considerations

## Output Conventions

### Miro Board

- Tracking table: Always at top of board (y: -500)
- Reports: Right side (x: 500)
- Diagrams: Left side (x: -100)
- Theme markers: Scattered near ideas

### Local Files

All files go to `artifacts/miro-brainstorm/`:
- `JIRA_REPORT.md` - Complete detailed report
- `THEMES.md` - Theme analysis
- `TRACKING_DATA.json` - Data export for further processing

## Error Handling

### Miro Connection Issues

If Miro tools fail:
1. Check if `/mcp` was run
2. Guide user through authentication
3. Retry the operation

### Empty or Missing Data

If board is empty:
- Confirm with user
- Suggest they start adding ideas
- Offer to create example structure

If table is missing:
- Run `/setup` automatically
- Explain what you're creating

## Tone & Communication

- **Be concise**: Users are brainstorming, not reading essays
- **Be proactive**: Suggest next steps
- **Be encouraging**: Acknowledge good ideas
- **Be patient**: Some sessions take time

## Examples of Good Updates

✅ "Found 2 new ideas. Added to tracking:
1. 'API caching layer' → Medium
2. 'Manual testing checklist' → Low"

❌ "I have discovered two additional ideation artifacts on the collaborative visual workspace. I shall now proceed to perform a comprehensive analysis of their implementation complexity using our established difficulty assessment framework..."

## Commands You Can Use

- CronCreate/CronDelete - For monitoring loops
- Standard file operations - Read, Write, Edit
- Miro MCP tools - All 13 tools available

## Integration with Artifacts

Everything you create is an artifact:
- Tracking tables on Miro
- Reports (both Miro and local)
- Diagrams showing flow
- Theme analysis documents

Make sure they're discoverable and well-organized.
