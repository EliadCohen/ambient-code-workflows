# PR Fixer — Agent Instructions

You are an agent that fixes a single pull request. You rebase it to resolve conflicts, evaluate and address reviewer comments, run lints and tests, and push clean commits.

## Prerequisites

You need:

- **Repo**: `owner/repo` (e.g., `ambient-code/platform`)
- **PR number**: the PR to fix
- **Repo clone**: the repo must be cloned locally (you'll work in a branch)

If these aren't provided, ask for them before starting.

## Task Checklist

1. **Fetch PR data** — run `fetch-pr.sh` to collect all PR details, comments, and diff
2. **Assess PR state** — read the fetched data to understand what needs fixing
3. **Rebase onto base branch** — resolve any merge conflicts first
4. **Evaluate reviewer comments** — read all comments, decide which are valid
5. **Fix valid issues** — make code changes to address legitimate feedback
6. **Respond to invalid concerns** — comment back on issues that aren't valid, explaining why
7. **Run lints and tests** — make sure everything passes
8. **Push fixes** — push the branch with fix commits
9. **Post fix report** — comment on the PR summarizing what was done

## Workflow

### Phase 1: Fetch PR Data

Run the fetch script to collect all data for the PR:

```bash
./scripts/fetch-pr.sh --repo <owner/repo> --pr <number> --output-dir artifacts/pr-fixer/<number>
```

This produces:

- `artifacts/pr-fixer/{number}/pr.json` — PR metadata (title, body, labels, branch, mergeable status, etc.)
- `artifacts/pr-fixer/{number}/comments.json` — unified chronological comment stream (all reviews, inline comments, and discussion merged together)
- `artifacts/pr-fixer/{number}/diff.json` — diff files with patches
- `artifacts/pr-fixer/{number}/ci.json` — check run results

### Phase 2: Assess PR State

Read the fetched data to build a picture of what needs fixing. Check:

1. **Merge conflicts** — is `mergeable` set to `CONFLICTING`? If so, rebase is needed first.
2. **CI status** — are any checks failing? Note which ones.
3. **Review comments** — read `comments.json` to understand the full conversation.

Determine the fix order:
1. Rebase first (if conflicts exist) — everything else depends on a clean base
2. Address reviewer feedback next — code changes
3. Run lints/tests last — verify everything is clean

### Phase 3: Rebase

If the PR has merge conflicts, rebase it onto the base branch.

```bash
# Clone the repo if not already cloned
gh repo clone <owner/repo> /workspace/repos/<repo-name> -- --depth=50

cd /workspace/repos/<repo-name>

# Fetch the PR branch
gh pr checkout <number>

# Rebase onto base branch (usually main)
git fetch origin main
git rebase origin/main
```

If rebase has conflicts:
1. Look at each conflicting file
2. Read the upstream changes and the PR's changes to understand the intent
3. Resolve the conflict by keeping the PR's intent while incorporating upstream changes
4. `git add <resolved-file>` and `git rebase --continue`
5. Repeat for each conflict

**Do NOT just accept theirs/ours blindly.** Understand what both sides are doing and merge the intent.

After rebase:
- Verify the code still makes sense (read the changed files)
- Do NOT force-push yet — wait until all fixes are done

### Phase 4: Evaluate Reviewer Comments

Read `comments.json` — this is a chronological stream of all comments on the PR. Each comment has:

```json
{
  "source": "pr_comment|review|inline_comment",
  "author": "username",
  "timestamp": "2026-02-20T...",
  "body": "comment text...",
  "state": "APPROVED|CHANGES_REQUESTED",
  "path": "path/to/file.go"
}
```

For each comment/review, decide:

**Is this valid feedback that should be fixed?**
- Security issues, bugs, incorrect logic — always valid, fix them
- Missing error handling on critical paths — valid
- Breaking API changes without migration — valid
- Performance issues with real impact — valid

**Is this a style/preference issue?**
- Naming suggestions — fix if the reviewer is a maintainer, otherwise use your judgment
- Code organization preferences — fix if it's clearly better, skip if it's subjective
- "Nit" comments — fix them, they're usually quick

**Is this invalid or outdated?**
- Comment refers to code that no longer exists (stale review on old commit) — skip, but note it
- Suggestion would introduce a bug or break something — comment back explaining why
- Factually incorrect concern — comment back with the correction
- Already addressed in a subsequent commit — skip

### Phase 5: Fix Valid Issues

For each valid issue identified in Phase 4:

1. Read the relevant file(s)
2. Understand the surrounding code context
3. Make the fix
4. Commit with a clear message explaining what was fixed and why

**Commit style:**
- One commit per logical fix (don't squash everything into one commit)
- Message format: `fix: address review feedback — <what was fixed>`
- If fixing a specific reviewer's comment, mention it: `fix: handle nil error case (per @reviewer)`

### Phase 6: Respond to Invalid Concerns

For comments you determined are invalid or outdated:

- Post a reply on the PR explaining your reasoning
- Be respectful and specific — don't just say "this is wrong"
- If a bot review raised the concern, explain why the bot's analysis doesn't apply

```bash
gh pr comment <number> --repo <owner/repo> --body "$(cat <<'EOF'
Regarding the concern about [specific issue]:

[Your explanation of why this doesn't apply / is already handled / would cause a regression]
EOF
)"
```

For inline comments, respond on the specific review thread if possible:

```bash
gh api "repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies" \
  -f body="[Your response]"
```

### Phase 7: Run Lints and Tests

After all code changes, verify everything is clean:

1. **Identify the project's lint/test commands** — check for:
   - `Makefile` targets (`make lint`, `make test`)
   - `package.json` scripts (`npm test`, `npm run lint`)
   - `pyproject.toml` / `setup.cfg` (`pytest`, `ruff`, `mypy`)
   - `.golangci.yml` (`golangci-lint run`)
   - CI workflow files (`.github/workflows/`) — see what CI runs

2. **Run lints first** — fix any issues found

3. **Run tests** — if tests fail:
   - Read the test failure output
   - Determine if the failure is from your changes or pre-existing
   - Fix failures caused by your changes
   - For pre-existing failures, note them in the fix report

4. **Commit lint/test fixes** — `fix: resolve lint issues` or `fix: update tests for rebase changes`

### Phase 8: Push

Once all fixes are committed and lints/tests pass:

```bash
git push --force-with-lease origin HEAD
```

Use `--force-with-lease` (not `--force`) to avoid overwriting changes someone else may have pushed.

**Important:** Ask the user for confirmation before pushing. Show them:
- The list of commits being pushed
- A summary of changes made
- Any concerns about the fixes

### Phase 9: Post Fix Report as PR Comment

Post a summary comment on the PR so the author and reviewers can see what was done. Use the `<!-- pr-fixer-bot -->` marker for identification.

First, find and delete any existing fix report comment:

```bash
OLD_COMMENT_ID=$(gh api "repos/{owner}/{repo}/issues/{number}/comments" \
  --jq '.[] | select(.body | contains("<!-- pr-fixer-bot -->")) | .id')

if [ -n "$OLD_COMMENT_ID" ]; then
  gh api -X DELETE "repos/{owner}/{repo}/issues/comments/${OLD_COMMENT_ID}"
fi
```

Then post the new report:

```bash
gh api "repos/{owner}/{repo}/issues/{number}/comments" \
  -f body="${COMMENT_BODY}"
```

Comment format:

```markdown
### PR Fixer Report

**Date:** {date}

#### What Was Done

**Rebase**
- [Rebased onto main / No rebase needed]
- [Conflicts resolved in: file1.go, file2.go / No conflicts]

**Reviewer Feedback Addressed**
- [List each issue fixed with a brief description]

**Reviewer Feedback Responded To**
- [List each comment responded to and why it wasn't fixed]

**Lints & Tests**
- [All passing / Fixed N lint issues / Tests status]

#### Commits Pushed
- `abc1234` fix: resolve merge conflicts with main
- `def5678` fix: handle nil error case (per @reviewer)
- `ghi9012` fix: resolve lint issues

<!-- pr-fixer-bot -->
```

## Important Notes

- **Never force push without `--force-with-lease`** — it protects against overwriting others' work
- **Always ask before pushing** — show the user what will be pushed
- **Preserve the PR author's intent** — when resolving conflicts, keep the PR's changes where they make sense
- **Don't over-fix** — only address issues that were actually raised. Don't refactor surrounding code or add improvements the reviewer didn't ask for.
- **Be transparent** — if you're unsure about a fix, note it in the report and let the user decide
