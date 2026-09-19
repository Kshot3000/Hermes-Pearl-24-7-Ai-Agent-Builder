#!/usr/bin/env python3
"""Render the standard attribution block from attribution.json.

Every deliverable in this repo (docs, PRs, releases, artifacts) must carry
the owner's donation address + socials. Run this to copy the canonical block
so it never drifts from attribution.json.

Usage:
    python attribution.py        # print the block
    python attribution.py --md   # print as a GitHub markdown section
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, "attribution.json"), encoding="utf-8") as f:
        return json.load(f)


def render(md=False):
    a = load()
    lines = [
        "Pearl donation address:",
        f"  {a['donation_address']}",
        f"  Explorer: {a['explorer_link']}",
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
            f"[View on explorer]({a['explorer_link']})\n\n"
            "---\n\n"
            f"🐦 [X / {a['x_account'].rsplit('/', 1)[-1]}]({a['x_account']})"
            f" · [GitHub / {a['github'].rsplit('/', 1)[-1]}]({a['github']})\n\n"
            "</div>\n"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(render(md="--md" in __import__("sys").argv))
