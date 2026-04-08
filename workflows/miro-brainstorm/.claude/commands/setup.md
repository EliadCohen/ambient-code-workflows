# /setup - Initialize Miro Board

## Purpose

Set up the Miro board with tracking infrastructure and prepare for brainstorming.

## Prerequisites

- Miro MCP server connected and authenticated
- Valid Miro board URL

## Process

1. Explore the board to understand current state
2. Create a tracking table with columns:
   - Idea (text)
   - Description (text)
   - Difficulty (select: Low/Medium/Insane)
   - Notes (text)
3. Explain the tracking system to the user
4. Ask if they want to start monitoring immediately

## Inputs

- `<miro-url>` - Full Miro board URL

## Output

- Tracking table created on Miro board
- Confirmation message with table URL

## Example

```
/setup https://miro.com/app/board/uXjVGl0WtOA=/
```
