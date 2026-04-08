# Miro Brainstorm & Jira Planning Workflow

Interactive brainstorming workflow that uses Miro boards to capture ideas, automatically clusters them by difficulty and semantic theme, then generates comprehensive Jira planning reports.

## Overview

This workflow helps teams run structured brainstorming sessions with automated analysis and planning:

1. **Capture** - Team adds ideas to Miro board as sticky notes
2. **Monitor** - Automated tracking watches for new ideas
3. **Analyze** - Ideas assessed for implementation difficulty (Low/Medium/Insane)
4. **Organize** - Semantic clustering into themes
5. **Plan** - Generate detailed Jira epics, stories, spikes, and tasks

## Prerequisites

### Required Setup

1. **Miro MCP Server** - Must be configured before use

   **Official OAuth Setup** (recommended - 3 commands, no API tokens!):
   
   a. **Add Miro MCP Server**
      ```bash
      claude mcp add --transport http miro https://mcp.miro.com
      ```
   
   b. **Authenticate with OAuth**
      
      In Claude Code:
      ```
      /mcp auth
      ```
      
      This will open your browser to authorize Claude Code with your Miro team.
   
   c. **Verify Connection**
      ```
      List items on https://miro.com/app/board/YOUR-BOARD-ID=/
      ```
   
   **See official docs:** https://developers.miro.com/docs/connecting-miro-mcp-to-ai-coding-tools#claude-code

2. **Miro Board** - Valid board URL
   ```
   https://miro.com/app/board/YOUR-BOARD-ID=/
   ```

3. **Context** - Basic understanding of your brainstorming topic

## Quick Start

```bash
# 1. Connect to Miro
/mcp

# 2. Set up your board
/setup https://miro.com/app/board/YOUR-BOARD-ID=/

# 3. Start monitoring (checks every minute)
/monitor https://miro.com/app/board/YOUR-BOARD-ID=/ 1m

# ... team adds ideas to the board ...

# 4. Stop monitoring when done
/stop-monitor

# 5. Organize ideas by theme
/organize https://miro.com/app/board/YOUR-BOARD-ID=/

# 6. Generate Jira planning report
/report https://miro.com/app/board/YOUR-BOARD-ID=/
```

## Commands

### `/setup <miro-url>`

Initialize the Miro board with tracking infrastructure:
- Creates a tracking table with difficulty ratings
- Prepares for automated monitoring

### `/monitor <miro-url> [interval]`

Watch the board for new ideas and automatically analyze them:
- Default interval: 1 minute
- Identifies sticky notes, cards, text items
- Assesses implementation difficulty
- Updates tracking table in real-time

### `/stop-monitor`

Stop the active monitoring loop and show statistics.

### `/organize <miro-url>`

Perform semantic analysis and create visual organization:
- Groups ideas into 4-8 themes
- Creates theme marker documents on board
- Generates dependency flowchart
- Writes theme analysis to local file

### `/report <miro-url>`

Generate comprehensive Jira planning documentation:
- Creates epics, stories, spikes, and tasks
- Maps dependencies between items
- Builds quarterly implementation roadmap
- Estimates budget and team capacity
- Writes to both Miro board and local files

## Difficulty Levels

The workflow assesses each idea's implementation difficulty:

| Level | Timeline | Characteristics |
|-------|----------|----------------|
| **Low** | 1 sprint | Straightforward, uses existing tools, low risk |
| **Medium** | 2-5 sprints | Some new infrastructure, multi-team coordination |
| **Insane** | 6+ months | Major R&D, significant infrastructure, high complexity |

## Output Files

### On Miro Board

- **Tracking Table** - Real-time idea tracking with difficulty ratings
- **Report Document** - Summary of Jira planning recommendations
- **Theme Markers** - Visual organization of idea clusters
- **Flow Diagram** - Dependency and relationship visualization

### Local Files

All files saved to `artifacts/miro-brainstorm/`:

- `JIRA_REPORT.md` - Detailed Jira planning report with:
  - Executive summary
  - Dependency diagrams
  - Complete item descriptions
  - Implementation roadmap
  - Risk register
  - Budget estimates

- `THEMES.md` - Theme analysis with semantic clustering

- `TRACKING_DATA.json` - Raw data export for further processing

## Example Use Cases

### Product Planning

Brainstorm new product features, automatically categorize by complexity, generate Jira roadmap for next 4 quarters.

### Technical Architecture

Collect technical ideas from team, organize by theme (security, performance, infrastructure), create implementation plan with dependencies.

### Sprint Planning

Gather ideas for upcoming sprints, filter by "Low" difficulty for quick wins, create tasks and stories with acceptance criteria.

### Research & Innovation

Brainstorm experimental ideas, identify "Insane" items requiring R&D spikes, separate from practical near-term work.

## Tips

### Effective Monitoring

- Set realistic intervals (1-2 minutes works well for most sessions)
- Stop monitoring when team finishes brainstorming
- Review the tracking table periodically during the session

### Better Organization

- Run `/organize` after collecting 10+ ideas for meaningful clusters
- Semantic themes emerge naturally from idea patterns
- Use the dependency diagram to prioritize work

### Comprehensive Reports

- Include context when running `/report` (team size, budget constraints)
- Review the report with stakeholders before creating Jira tickets
- Use the roadmap to plan quarterly milestones

## Troubleshooting

### "Miro not authenticated"

**Cause:** MCP server not configured

**Solution:**

1. **Check MCP server is added:**
   ```bash
   claude mcp list
   # Should show "miro" in the list
   ```

2. **Add if missing:**
   ```bash
   claude mcp add --transport http miro https://mcp.miro.com
   ```

3. **Authenticate:**
   ```
   /mcp auth
   ```

4. **If still failing:**
   - Check your browser didn't block the OAuth popup
   - Verify you have access to the Miro team
   - Try authenticating again: `/mcp auth`
   - Check official docs: https://developers.miro.com/docs/connecting-miro-mcp-to-ai-coding-tools

### "Table not found"

Run `/setup` first to create the tracking infrastructure.

### "No new ideas found"

Ensure sticky notes have text content (empty notes are ignored).

### "Monitoring not stopping"

Say "stop monitoring" or "done" - the workflow watches for these phrases.

## Advanced Features

### Custom Difficulty Criteria

The workflow adapts difficulty assessment to your domain. Mention your context (e.g., "we're brainstorming ML features for a mobile app") for better analysis.

### Team Constraints

Mention team size or constraints when generating reports (e.g., "we're a team of 8"). The workflow will factor this into recommendations.

### Integration with Existing Tools

Export `TRACKING_DATA.json` for integration with your own planning tools or dashboards.

## Contributing

To modify this workflow:

1. Fork the workflows repository
2. Edit files under `workflows/miro-brainstorm/`
3. Test using "Custom Workflow" feature in ACP
4. Submit pull request

## License

This workflow is part of the Ambient Code Platform workflows repository, provided under the MIT License.
