#!/usr/bin/env python3
"""
parse_lh_report.py — Parse a Lighthouse JSON report and print a prioritised summary.

Usage:
    python scripts/parse_lh_report.py /tmp/lh-report.json
    python scripts/parse_lh_report.py /tmp/lh-report.json --compare /tmp/lh-report-after.json
"""

import json
import sys
import argparse
from pathlib import Path


CATEGORY_LABELS = {
    "performance": "Performance",
    "accessibility": "Accessibility",
    "best-practices": "Best Practices",
    "seo": "SEO",
}

# Audits that typically require server/deploy changes, not code changes
DEPLOY_ONLY_AUDITS = {
    "uses-long-cache-ttl",
    "uses-http2",
    "uses-text-compression",
    "server-response-time",
}


def score_to_emoji(score):
    if score is None:
        return "⚪"
    if score >= 0.9:
        return "🟢"
    if score >= 0.5:
        return "🟡"
    return "🔴"


def format_score(score):
    if score is None:
        return "n/a"
    return f"{round(score * 100)}"


def parse_report(path: Path):
    data = json.loads(path.read_text())
    categories = data.get("categories", {})
    audits = data.get("audits", {})

    scores = {}
    for cat_id, cat_data in categories.items():
        scores[cat_id] = cat_data.get("score")

    # Collect failing audits grouped by priority
    critical, warnings, info = [], [], []
    for audit_id, audit in audits.items():
        score = audit.get("score")
        if score is None:
            continue
        if score >= 0.9:
            continue
        entry = {
            "id": audit_id,
            "title": audit.get("title", audit_id),
            "description": audit.get("description", ""),
            "score": score,
            "display": audit.get("displayValue", ""),
            "deploy_only": audit_id in DEPLOY_ONLY_AUDITS,
        }
        if score < 0.5:
            critical.append(entry)
        else:
            warnings.append(entry)

    return scores, critical, warnings


def print_report(scores, critical, warnings, label=""):
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")

    print("\n📊 Scores")
    print("-" * 40)
    for cat_id, cat_label in CATEGORY_LABELS.items():
        score = scores.get(cat_id)
        emoji = score_to_emoji(score)
        print(f"  {emoji} {cat_label:<20} {format_score(score):>4}/100")

    if critical:
        print(f"\n🔴 Critical Issues ({len(critical)})")
        print("-" * 40)
        for a in sorted(critical, key=lambda x: x["score"]):
            deploy = " [server config]" if a["deploy_only"] else ""
            display = f"  ({a['display']})" if a["display"] else ""
            print(f"  • [{a['score']*100:.0f}] {a['title']}{display}{deploy}")
            print(f"    id: {a['id']}")

    if warnings:
        print(f"\n🟡 Warnings ({len(warnings)})")
        print("-" * 40)
        for a in sorted(warnings, key=lambda x: x["score"]):
            deploy = " [server config]" if a["deploy_only"] else ""
            display = f"  ({a['display']})" if a["display"] else ""
            print(f"  • [{a['score']*100:.0f}] {a['title']}{display}{deploy}")
            print(f"    id: {a['id']}")

    print()


def compare_reports(before_scores, after_scores):
    print("\n📈 Score Comparison")
    print("-" * 50)
    print(f"  {'Category':<22} {'Before':>6} {'After':>6} {'Delta':>6}")
    print(f"  {'-'*22} {'-'*6} {'-'*6} {'-'*6}")
    for cat_id, cat_label in CATEGORY_LABELS.items():
        b = before_scores.get(cat_id)
        a = after_scores.get(cat_id)
        if b is None or a is None:
            continue
        delta = round(a * 100) - round(b * 100)
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        emoji = "✅" if delta > 0 else ("⚠️" if delta < 0 else "—")
        print(f"  {emoji} {cat_label:<20} {format_score(b):>6} {format_score(a):>6} {delta_str:>6}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Parse Lighthouse JSON report")
    parser.add_argument("report", type=Path, help="Path to lh-report.json")
    parser.add_argument("--compare", type=Path, help="Path to after report for comparison")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"❌ Report not found: {args.report}")
        sys.exit(1)

    before_scores, critical, warnings = parse_report(args.report)
    print_report(before_scores, critical, warnings, label="Lighthouse Audit Report")

    if args.compare:
        if not args.compare.exists():
            print(f"❌ Comparison report not found: {args.compare}")
            sys.exit(1)
        after_scores, after_critical, after_warnings = parse_report(args.compare)
        compare_reports(before_scores, after_scores)
        print_report(after_scores, after_critical, after_warnings, label="After Fixes")

    # Output fix-target audit IDs for the skill to act on
    fixable = [a for a in critical + warnings if not a["deploy_only"]]
    if fixable:
        print("🎯 Audit IDs to fix (in priority order):")
        for a in sorted(fixable, key=lambda x: x["score"]):
            print(f"   - {a['id']}")


if __name__ == "__main__":
    main()
