---
name: miro-integration
description: Expert knowledge of Miro MCP tools for brainstorming and visualization
---

# Miro Integration Skill

You are an expert at using Miro's MCP tools for collaborative brainstorming and visual organization.

## Available Miro Tools

### Exploration & Reading

- `mcp__miro__context_explore` - Discover frames, documents, tables, diagrams on a board
- `mcp__miro__context_get` - Get detailed content from board or specific items
- `mcp__miro__board_list_items` - List items with filtering (sticky notes, cards, shapes, etc.)

### Documents

- `mcp__miro__doc_create` - Create structured documents with markdown
- `mcp__miro__doc_get` - Read document content
- `mcp__miro__doc_update` - Edit documents with find-and-replace

### Diagrams

- `mcp__miro__diagram_get_dsl` - Get DSL format spec for diagrams (flowchart, UML, ER)
- `mcp__miro__diagram_create` - Create diagrams from DSL text

### Tables

- `mcp__miro__table_create` - Create tables with text and select columns
- `mcp__miro__table_list_rows` - Read table rows with filtering and pagination
- `mcp__miro__table_sync_rows` - Add or update table rows

### Images

- `mcp__miro__image_get_data` - Get image data
- `mcp__miro__image_get_url` - Get image download URL

## Common Patterns

### Monitoring Pattern

```javascript
// List sticky notes
mcp__miro__board_list_items({
  miro_url: boardUrl,
  limit: 50,
  item_type: "sticky_note"
})

// Check if already tracked
// Add new ones to table with:
mcp__miro__table_sync_rows({
  miro_url: tableUrl,
  rows: [...]
})
```

### Tracking Table Pattern

```javascript
// Create tracking table
mcp__miro__table_create({
  miro_url: boardUrl,
  table_title: "Idea Tracking",
  columns: [
    {column_type: "text", column_title: "Idea"},
    {column_type: "text", column_title: "Description"},
    {
      column_type: "select",
      column_title: "Difficulty",
      options: [
        {displayValue: "Low", color: "#00FF00"},
        {displayValue: "Medium", color: "#FFA500"},
        {displayValue: "Insane", color: "#FF0000"}
      ]
    },
    {column_type: "text", column_title: "Notes"}
  ]
})
```

### Theme Organization Pattern

```javascript
// Create theme markers
mcp__miro__doc_create({
  miro_url: boardUrl,
  content: "# 🏗️ Theme Name\n\n**Ideas:** ...",
  x: -500,
  y: -300
})

// Create relationship diagram
mcp__miro__diagram_get_dsl({ diagram_type: "flowchart" })
// Then use DSL to create diagram
mcp__miro__diagram_create({
  diagram_dsl: "...",
  diagram_type: "flowchart"
})
```

### Report Generation Pattern

```javascript
// Create summary document
mcp__miro__doc_create({
  miro_url: boardUrl,
  content: markdownReport,
  x: 500,
  y: 0
})
```

## Best Practices

1. **Always check authentication** - Miro MCP must be connected before use
2. **Use positioning** - Set x, y coordinates to prevent overlapping items
3. **Batch operations** - List all items once, then process
4. **Error handling** - Check for empty content in sticky notes
5. **User feedback** - Provide updates when processing many items

## Difficulty Assessment Guidelines

When analyzing ideas for implementation difficulty:

### Low (1 sprint)
- Uses existing tools/infrastructure
- No new dependencies
- Clear implementation path
- Low risk

### Medium (2-5 sprints)
- Some new infrastructure needed
- Cross-team coordination
- Multiple system integration
- Moderate complexity

### Insane (6+ months)
- Major R&D required
- New infrastructure/platforms
- ML/AI expertise needed
- High risk/uncertainty
- Significant ongoing maintenance

## Semantic Clustering Approach

When organizing ideas by theme:

1. **Read all ideas first** - Get complete context
2. **Identify patterns** - Common technologies, purposes, scopes
3. **Group by similarity** - 4-8 themes typically
4. **Create visual markers** - Use emoji and color coding
5. **Show relationships** - Diagrams for dependencies

### Common Theme Categories

- Infrastructure & Distribution
- Security & Authentication
- Performance & Optimization
- User Experience & Contribution
- Advanced/Research
- Constraints & Alternatives

## Example Workflow

```bash
# 1. Setup
/setup <miro-url>

# 2. Monitor (runs continuously)
/monitor <miro-url> 1m

# User adds ideas to board...

# 3. Stop when done
/stop-monitor

# 4. Organize themes
/organize <miro-url>

# 5. Generate report
/report <miro-url>
```

## Troubleshooting

### "Miro not authenticated"
- User needs to run `/mcp` command to connect
- Guide them through authentication

### "Table not found"
- Run `/setup` first to create tracking table
- Verify table URL is correct

### "Empty sticky notes"
- Filter out items with no content
- Only process non-empty items

### "Duplicate ideas"
- Check tracking table before adding
- Use idea text as unique key
