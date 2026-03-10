# Review Queue — {{REPO}}

**Date:** {{DATE}}
**Open PRs:** {{TOTAL_PRS}} | **Ready for Review:** {{READY_COUNT}} | **In Review Queue:** {{MILESTONE_COUNT}}

### At a Glance

{{AT_A_GLANCE}}

---

## Ready for Review ({{READY_COUNT}})

> Ordered by priority: bug fixes first, then features, smallest first within each type.

| # | PR | Type | Author | Size | Updated | Action Needed | Notes |
|---|---|---|---|---|---|---|---|
{{#each READY_PR_ROWS}}
| {{RANK}} | [#{{NUMBER}}]({{URL}}) — {{TITLE}} | {{TYPE}} | {{AUTHOR}} | {{SIZE}} | {{UPDATED}} | {{ACTION_NEEDED}} | {{NOTES}} |
{{/each}}

---

## PRs With Blockers

{{#each BLOCKER_PR_ENTRIES}}

### {{RANK}}. [#{{NUMBER}}]({{URL}}) — {{TITLE}}

**Author:** {{AUTHOR}} | **Type:** {{TYPE}} | **Size:** {{SIZE}} | **Updated:** {{UPDATED}} | **Branch:** `{{BRANCH}}`

| Blocker | Status | Detail |
|---------|--------|--------|
| CI | {{CI_STATUS}} | {{CI_DETAIL}} |
| Merge conflicts | {{CONFLICT_STATUS}} | {{CONFLICT_DETAIL}} |
| Review comments | {{REVIEW_STATUS}} | {{REVIEW_DETAIL}} |
| Jira hygiene | {{JIRA_STATUS}} | {{JIRA_DETAIL}} |
| Staleness | {{STALE_STATUS}} | {{STALE_DETAIL}} |
| Diff overlap risk | {{OVERLAP_STATUS}} | {{OVERLAP_DETAIL}} |

**Action needed:** {{ACTION_NEEDED}}

{{#if REVIEW_SUMMARY}}
> {{REVIEW_SUMMARY}}
{{/if}}

---

{{/each}}

{{#if RECOMMEND_CLOSE_ENTRIES}}
## Recommend Closing

> These PRs appear abandoned, superseded, or too stale to maintain. Close or ping the author.

| PR | Author | Reason | Last Updated |
|---|---|---|---|
{{#each RECOMMEND_CLOSE_ENTRIES}}
| [#{{NUMBER}}]({{URL}}) — {{TITLE}} | {{AUTHOR}} | {{REASON}} | {{UPDATED}} |
{{/each}}

---

{{/if}}

## Summary

- **Ready for review:** {{READY_COUNT}} PRs with zero blockers
- **In Review Queue:** {{MILESTONE_COUNT}} PRs
- **One blocker away:** {{NEAR_COUNT}} PRs
- **Needs work:** {{WORK_COUNT}} PRs
- **Recommend closing:** {{CLOSE_COUNT}} PRs
{{#if FORK_COUNT}}- **Fork PRs:** {{FORK_COUNT}} (marked in tables — no automated agent review, require manual review){{/if}}
