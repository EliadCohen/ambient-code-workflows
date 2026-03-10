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

    print(f"{len(comments)} comments merged into unified stream", file=sys.stderr)


if __name__ == "__main__":
    main()
