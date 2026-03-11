#!/usr/bin/env python3
"""
Merge all comment sources for a PR into a single chronological stream.

Usage:
    python3 merge-comments.py --pr-json pr.json --reviews reviews.json \
        --review-comments review_comments.json --output comments.json

Reads PR comments from pr.json (nested under .comments[]),
formal reviews from reviews.json, and inline review comments
from review_comments.json. Outputs a single sorted JSON array.
"""

import argparse
import json
import sys


def merge_comments(pr_path, reviews_path, review_comments_path):
    """Load comment sources from files and merge chronologically.

    This mirrors merge_comment_sources() in analyze-prs.py.
    Keep them in sync.
    """
    all_comments = []

    with open(pr_path) as f:
        pr = json.load(f)
    for c in pr.get("comments", []):
        all_comments.append(
            {
                "source": "pr_comment",
                "author": c.get("author", {}).get("login", ""),
                "timestamp": c.get("createdAt", ""),
                "body": c.get("body", ""),
            }
        )

    with open(reviews_path) as f:
        reviews = json.load(f)
    for r in reviews:
        body = r.get("body", "")
        if not body or not body.strip():
            continue
        all_comments.append(
            {
                "source": "review",
                "author": r.get("user", {}).get("login", ""),
                "state": r.get("state", ""),
                "timestamp": r.get("submitted_at", ""),
                "body": body,
            }
        )

    with open(review_comments_path) as f:
        rc_list = json.load(f)
    for rc in rc_list:
        body = rc.get("body", "")
        if not body or not body.strip():
            continue
        all_comments.append(
            {
                "source": "inline_comment",
                "author": rc.get("user", {}).get("login", ""),
                "path": rc.get("path", ""),
                "timestamp": rc.get("created_at", ""),
                "body": body,
            }
        )

    all_comments.sort(key=lambda c: c.get("timestamp", ""))
    return all_comments


def main():
    parser = argparse.ArgumentParser(description="Merge PR comment sources")
    parser.add_argument("--pr-json", required=True)
    parser.add_argument("--reviews", required=True)
    parser.add_argument("--review-comments", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    comments = merge_comments(args.pr_json, args.reviews, args.review_comments)

    with open(args.output, "w") as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    # Write per-comment files for tiered reading (avoids 25K token limit)
    comments_dir = args.output.replace(".json", "")
    import os
    os.makedirs(comments_dir, exist_ok=True)

    for i, comment in enumerate(comments, 1):
        with open(os.path.join(comments_dir, f"{i:02d}.json"), "w") as f:
            json.dump(comment, f, indent=2, ensure_ascii=False)

    # Write summary markdown
    pr_data = {}
    with open(args.pr_json) as f:
        pr_data = json.load(f)

    mergeable = pr_data.get("mergeable", "unknown")
    title = pr_data.get("title", "")
    author = (pr_data.get("author") or {}).get("login", "unknown")
    branch = pr_data.get("headRefName", "")
    base = pr_data.get("baseRefName", "main")
    additions = pr_data.get("additions", 0)
    deletions = pr_data.get("deletions", 0)
    changed_files = pr_data.get("changedFiles", 0)

    # Count comment types
    review_count = sum(1 for c in comments if c["source"] == "review")
    inline_count = sum(1 for c in comments if c["source"] == "inline_comment")
    pr_comment_count = sum(1 for c in comments if c["source"] == "pr_comment")

    # CI summary
    ci_path = os.path.join(os.path.dirname(args.output), "ci.json")
    ci_summary = "unknown"
    if os.path.exists(ci_path):
        with open(ci_path) as f:
            checks = json.load(f)
        failing = [c.get("name", "?") for c in checks
                   if c.get("conclusion") in ("failure", "timed_out", "cancelled")]
        if failing:
            ci_summary = f"FAIL: {', '.join(failing[:3])}"
        else:
            ci_summary = "all passing"

    summary_path = os.path.join(os.path.dirname(args.output), "summary.md")
    with open(summary_path, "w") as f:
        f.write(f"# PR: {title}\n\n")
        f.write(f"- **Author:** {author}\n")
        f.write(f"- **Branch:** {branch} → {base}\n")
        f.write(f"- **Size:** {changed_files} files (+{additions}/-{deletions})\n")
        f.write(f"- **Mergeable:** {mergeable}\n")
        f.write(f"- **CI:** {ci_summary}\n")
        f.write(f"- **Comments:** {len(comments)} total "
                f"({review_count} reviews, {inline_count} inline, {pr_comment_count} PR comments)\n")
        if comments:
            f.write(f"\n## Comment Authors\n\n")
            authors = {}
            for c in comments:
                a = c.get("author", "unknown")
                authors[a] = authors.get(a, 0) + 1
            for a, count in sorted(authors.items(), key=lambda x: -x[1]):
                f.write(f"- @{a}: {count} comments\n")

    print(f"{len(comments)} comments merged into unified stream", file=sys.stderr)
    print(f"Per-comment files: {comments_dir}/01.json ... {len(comments):02d}.json", file=sys.stderr)
    print(f"Summary: {summary_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
