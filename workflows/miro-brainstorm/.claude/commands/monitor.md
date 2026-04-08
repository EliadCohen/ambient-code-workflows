# /monitor - Monitor Board for Ideas

## Purpose

Continuously monitor a Miro board for new sticky notes, cards, and text items. Automatically analyze each new idea and add it to the tracking table with difficulty assessment.

## Prerequisites

- `/setup` has been run (tracking table exists)
- Miro board URL available

## Process

1. Start a recurring check (default: every 1 minute)
2. For each check:
   - List all sticky notes, cards, and text items
   - Identify new items (not yet in tracking table)
   - Analyze each new idea for implementation difficulty
   - Add to tracking table with assessment
   - Notify user of new ideas found
3. Continue until user says "stop" or "done"

## Inputs

- `<miro-url>` - Full Miro board URL
- `<interval>` - Optional check interval (default: 1m)

## Difficulty Assessment Context

Consider the brainstorming topic (agentic workflows, developer velocity, etc.) and assess:

- **Low**: Single sprint, no new infrastructure
- **Medium**: Multi-sprint, some infrastructure, coordination needed
- **Insane**: 6+ months, major R&D, significant new infrastructure

## Output

- Real-time updates when new ideas found
- Tracking table automatically updated
- Progress messages

## Example

```
/monitor https://miro.com/app/board/uXjVGl0WtOA=/ 1m
```
