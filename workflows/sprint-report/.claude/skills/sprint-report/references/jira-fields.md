# Jira Custom Fields for Sprint Reports

Custom field IDs vary by Jira instance. This document lists common patterns
and how to discover the correct IDs for any instance.

## Discovery

If you have Jira MCP access, use `jira_search_fields` to search for field
names. Otherwise, fetch a single issue with all fields and inspect the keys:

```
jira_search("project = X AND sprint in openSprints() ORDER BY created DESC", maxResults=1, fields="*all")
```

Look for fields containing point values (floats), sprint objects (JSON with
`name`, `state`, `startDate`), or epic keys.

## Common Custom Fields

### Story Points

| Field ID | Notes |
| --- | --- |
| `customfield_10028` | Common in Red Hat Jira instances |
| `customfield_10016` | Common in Atlassian Cloud |
| `customfield_10026` | Alternate |
| `customfield_10002` | Alternate |
| `story_points` | Some instances expose this as a standard field |

**Type:** Float. Found on Stories, Tasks, Bugs, sometimes Epics.

**Variants:** Some instances split estimates by role:

- DEV Story Points (`customfield_10506`)
- QE Story Points (`customfield_10572`)
- DOC Story Points (`customfield_10510`)

If the primary story points field is empty, check for role-specific variants.

### Sprint

| Field ID | Notes |
| --- | --- |
| `customfield_10020` | Most common (GreenHopper Sprint field) |

**Type:** JSON object with `name`, `state` (active/closed/future), `startDate`,
`endDate`, `completeDate`.

### Epic Link

| Field ID | Notes |
| --- | --- |
| `customfield_10014` | Most common (GreenHopper Epic Link) |

**Type:** Key reference (e.g., `PROJ-123`).

### Epic Name

| Field ID | Notes |
| --- | --- |
| `customfield_10011` | GreenHopper Epic Label |

**Type:** String. Short name displayed on boards.

## Standard Fields (Always Available)

These don't require custom field discovery:

| Field | Jira Key | Type |
| --- | --- | --- |
| Summary | `summary` | String |
| Status | `status` | Workflow status object |
| Assignee | `assignee` | User object |
| Priority | `priority` | Select (Blocker, Critical, Major, Normal, Minor) |
| Issue Type | `issuetype` | Select (Epic, Story, Task, Bug, etc.) |
| Created | `created` | Datetime |
| Updated | `updated` | Datetime |
| Resolution Date | `resolutiondate` | Datetime (null if unresolved) |
| Components | `components` | Multi-select |
| Fix Version | `fixVersions` | Multi-version |
| Description | `description` | Text (check here for acceptance criteria) |
| Comments | `comment` | Comment list |

## Workflow Statuses

Status names and classifications vary by project. Common patterns:

### Engineering Projects (Stories/Tasks/Bugs)

```
New → Backlog → To Do → In Progress → Review → Done / Closed
```

| Classification | Typical Statuses |
| --- | --- |
| Not Started | New, Backlog, To Do, Open |
| In Progress | In Progress, In Development, Coding |
| In Review | Review, Code Review, In Review, QA |
| Done | Done, Closed, Resolved, Release Pending |

### What "Review" Means

"Review" can mean different things depending on the team:

- **Code review** — PR is open, waiting for reviewer
- **QA review** — testing in progress
- **Stakeholder review** — waiting for approval

If >40% of items are in Review, flag it as a flow bottleneck and recommend
the team investigate which type of review is the queue.

## Acceptance Criteria Detection

There is no standard Jira field for acceptance criteria. Teams typically put
them in the `description` field. Look for patterns:

- Heading: `## Acceptance Criteria`, `### AC`, `**Acceptance Criteria**`
- Checkbox lists: `- [ ] ...` or `* [ ] ...`
- Numbered criteria: `AC1:`, `AC2:`, etc.

If none of these patterns are found in the description, count the item as
having no acceptance criteria.
