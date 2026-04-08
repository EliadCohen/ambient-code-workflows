# /report - Generate Jira Planning Report

## Purpose

Generate a comprehensive Jira planning report with epics, stories, spikes, and tasks. Include dependencies, implementation roadmap, and budget estimates.

## Prerequisites

- Ideas have been tracked and analyzed
- Themes have been identified

## Process

1. Read all tracked ideas from table
2. Analyze themes and dependencies
3. Generate Jira items:
   - Epics for major themes
   - Stories for multi-sprint features
   - Spikes for research/investigation
   - Tasks for single-sprint work
4. Create dependency mapping
5. Build implementation roadmap (phases/quarters)
6. Estimate budget and team capacity
7. Write report to both Miro and local file

## Report Structure

The report should include:

1. **Executive Summary**
2. **Dependency Overview** (with ASCII diagram)
3. **Jira Items by Type**:
   - Epics (with sub-stories)
   - Stories (standalone)
   - Spikes
   - Tasks
4. **Implementation Roadmap** (quarterly breakdown)
5. **Risk Register**
6. **Success Metrics**
7. **Budget Estimates**
8. **Recommendations Summary**

## Output

- Miro board: Document with summary report
- Local: `artifacts/miro-brainstorm/JIRA_REPORT.md` (detailed)
- Local: `artifacts/miro-brainstorm/TRACKING_DATA.json` (data export)

## Example

```
/report https://miro.com/app/board/uXjVGl0WtOA=/
```
