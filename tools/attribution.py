#!/usr/bin/env python3
"""Render the standard attribution block from attribution.json.

Every deliverable in this repo (docs, PRs, releases, artifacts) must carry
the owner's donation address + socials. Run this to copy the canonical block
so it never drifts from attribution.json.

Usage:
    python attribution.py                 # print the text block
    python attribution.py --md            # print as a GitHub markdown section
    python attribution.py --format json   # dump the raw attribution JSON
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    with open(os.path.join(ROOT, "attribution.json"), encoding="utf-8") as f:
        return json.load(f)


def render(md=False):
    a = load()
    explorers = a.get("explorers") or [a.get("explorer_link", "")]
    lines = [
        "Pearl donation address:",
        f"  {a['donation_address']}",
        f"  Explorer: {explorers[0]}",
        "",
        "Follow the work:",
        f"  X:      {a['x_account']}",
        f"  GitHub: {a['github']}",
    ]
    if md:
        return (
            "<div align=\"center\">\n\n"
            "**Pearl Donation Address**\n\n"
            f"`{a['donation_address']}`\n\n"
            f"[View on explorer]({explorers[0]})\n\n"
            "---\n\n"
            f"🐦 [X / {a['x_account'].rsplit('/', 1)[-1]}]({a['x_account']})"
            f" · [GitHub / {a['github'].rsplit('/', 1)[-1]}]({a['github']})\n\n"
            "</div>\n"
        )
    return "\n".join(lines)


def main(argv):
    if "--format" in argv:
        i = argv.index("--format")
        if i + 1 < len(argv) and argv[i + 1].lower() == "json":
            print(json.dumps(load(), indent=2, ensure_ascii=False))
            return 0
        print("error: --format only supports 'json'", file=sys.stderr)
        return 2
    print(render(md="--md" in argv))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
