---
name: controller
description: Workflow controller managing Jira hierarchy linking phases
---

# Jira Hierarchy Linker Controller

You manage the workflow by executing phases and handling transitions between them.

## Phases

1. **analyze-story** (`/analyze-story`) — `.claude/skills/analyze-story/SKILL.md`
   Find best epic matches for a story using semantic analysis

2. **analyze-epic** (`/analyze-epic`) — `.claude/skills/analyze-epic/SKILL.md`
   Find best initiative matches for an epic using semantic analysis

3. **link-story** (`/link-story`) — `.claude/skills/link-story/SKILL.md`
   Create story→epic link with safety validations

4. **link-epic** (`/link-epic`) — `.claude/skills/link-epic/SKILL.md`
   Create epic→initiative link with safety validations

5. **bulk-link** (`/bulk-link`) — `.claude/skills/bulk-link/SKILL.md`
   Process multiple items at once

6. **summary** (`/summary`) — `.claude/skills/summary/SKILL.md`
   Generate workflow summary and learning insights

Phases can be executed in any order based on user needs.

## How to Execute a Phase

1. **Announce** the phase to the user before doing anything else, e.g.,
   "Starting the /analyze-story phase (dispatched by `.claude/skills/controller/SKILL.md`)."
   This is very important so the user knows the workflow is working and so skills
   can find their way back here.

2. **Read** the skill file from the list above. You MUST call the Read tool on
   the skill's `SKILL.md` file before executing. If you find yourself executing
   a phase without having read its skill file, you are doing it wrong — stop
   and read it now.

3. **Execute** the skill's steps directly — the user should see your progress

4. When the skill is done, it will report its findings and re-read this
   controller. Then use "Recommending Next Steps" below to offer options.

5. Present the skill's results and your recommendations to the user.

6. **Use `AskUserQuestion` to get the user's decision.** Present the
   recommended next step and alternatives as options. Do NOT continue until the
   user responds. This is a hard gate — the `AskUserQuestion` tool triggers
   platform notifications and status indicators so the user knows you need
   their input. Plain-text questions do not create these signals and the user
   may not see them.

## Recommending Next Steps

After each phase completes, present the user with **options** — not just one
next step. Use the typical flow as a baseline, but adapt to what actually
happened.

### Typical Flows

```text
analyze-story → link-story → summary
analyze-epic → link-epic → summary
bulk-link → summary
```

### What to Recommend

After presenting results, consider what just happened, then offer options that make sense:

**Continuing to the next step:**
- After analyze-story → offer /link-story with top match
- After analyze-epic → offer /link-epic with top match
- After link-story or link-epic → offer /summary or analyze another item

**Alternative paths:**
- After analysis → offer to analyze another item instead of linking
- After linking → offer to link more items or bulk-link
- Anytime → offer /summary to see overall progress

**Conversational Mode Intent Detection:**

When user speaks naturally instead of using slash commands, detect intent:

- "story" + Jira key (e.g., "PROJ-123") → dispatch to analyze-story
- "epic" + "parent"/"initiative" + Jira key → dispatch to analyze-epic  
- "link" + story key → dispatch to link-story
- "link" + epic key + "initiative" → dispatch to link-epic
- Multiple keys (e.g., "PROJ-1, PROJ-2, PROJ-3") → dispatch to bulk-link
- "summary"/"status"/"report"/"what have we done" → dispatch to summary

**Command Mode:**

Direct slash commands always go straight to the phase:
- `/analyze-story PROJ-123` → dispatch to analyze-story
- `/link-epic PROJ-456` → dispatch to link-epic
- `/bulk-link PROJ-1,PROJ-2` → dispatch to bulk-link

## Session Configuration

On first interaction, check if artifacts/jira-hierarchy-linker/config.json exists.

If not, ask user:
- Which Jira project(s) to search (e.g., "PROJ", "MYTEAM")
- Any additional JQL filters (optional)

Save to artifacts/jira-hierarchy-linker/config.json:
```json
{
  "projects": ["PROJ1", "PROJ2"],
  "additional_filters": "AND component = backend"
}
```

Reuse this configuration for the entire session.

## Error Handling

If a phase fails:
- Present the error clearly
- Suggest alternatives (e.g., if Jira key invalid, ask for correct key)
- Don't stop the entire workflow — offer to try a different item or phase
