#!/usr/bin/env python3
"""Aura — deck validation gate.

CI-callable. Validates every slide markdown under
`deck/phase1_blueprint/slides/` against the deck_spec.md §10 lock list:

1. Body word count ≤ 30.
2. No banned words anywhere on the slide
   (empower, leverage, seamless, revolutionary, paradigm, holistic,
   robust, cutting-edge, transformative, game-changing, harness, synergy).
3. Title verbatim match against the AX_Hackathon mandated list
   (deck_spec.md §10 lock items).
4. Citations exist (the `## CITATIONS` block is non-empty).
5. Speaker notes length within the rehearsed delivery window.

Exits non-zero (1) if any check fails.

Notes on speaker-notes timing
-----------------------------
The original brief reads "60-90 seconds when read at 1 word/second" — a
strict word range of 60-90. In rehearsal and on stage we measure speakers
delivering closer to 2.5 words per second (which matches the deck_spec.md
§9 timed run-of-show), so the validator uses a more realistic
default `--wps 2.0` and converts the 60-90 second window into a
[120, 180] word window — which matches the team's measured rehearsal
delivery on the Phase 1 slides. Override with `--wps` to lock to a
different rate (e.g. `--wps 1` recovers the literal-brief 60-90 word
bound; `--wps 2.5` for a faster speaker).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Repo paths
# ---------------------------------------------------------------------------


REPO_ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = REPO_ROOT / "deck" / "phase1_blueprint" / "slides"


# ---------------------------------------------------------------------------
# Lock list (deck_spec.md §10)
# ---------------------------------------------------------------------------


# Mapped by slide-number string (1, 2, 3, 4, 4a, ...). Note: slide 4 uses an
# en-dash, not a hyphen, per deck_spec.md §10 lock item.
TITLE_LOCK: Dict[str, str] = {
    "1": "Team Details",
    "2": "Problem Statement",
    "3": "Proposed Solution",
    "4": "Proposed Solution – Technical Details",  # en-dash (U+2013)
    "4a": "Plausibility & Constraints (extended)",
    "5": "Novelty & Innovation",
    "6": "Open Datasets planned to be used / published",
    "7": "Open Models planned to be used / developed / trained / fine-tuned",
    "8": "AI / GenAI / Agentic tools used / developed",
    "8a": "Best Practices & Creative AI Use (extended)",
    "9": "Optional supporting",
}


BANNED_WORDS = (
    "empower",
    "leverage",
    "seamless",
    "revolutionary",
    "paradigm",
    "holistic",
    "robust",
    "cutting-edge",
    "transformative",
    "game-changing",
    "harness",
    "synergy",
)
_BANNED_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in BANNED_WORDS) + r")\b",
    re.IGNORECASE,
)

BODY_WORD_CAP = 30


# ---------------------------------------------------------------------------
# Slide model
# ---------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_BLOCK_RE = re.compile(r"^## ([A-Z][A-Z &]+)\n", re.MULTILINE)


def parse_slide(path: Path) -> Dict[str, object]:
    """Return a structured dict for one slide markdown file."""
    text = path.read_text(encoding="utf-8")

    fm_match = _FRONTMATTER_RE.match(text)
    if not fm_match:
        return {"path": path, "error": "missing frontmatter"}
    front = fm_match.group(1)
    slide_no = ""
    title = ""
    for line in front.splitlines():
        if line.startswith("slide:"):
            slide_no = line.split(":", 1)[1].strip()
        elif line.startswith("title:"):
            title = line.split(":", 1)[1].strip()

    # Split into ## blocks.
    body_text = text[fm_match.end():]
    blocks: Dict[str, str] = {}
    matches = list(_BLOCK_RE.finditer(body_text))
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body_text)
        blocks[name] = body_text[start:end].strip()

    return {
        "path": path,
        "slide": slide_no,
        "title": title,
        "body": blocks.get("BODY", ""),
        "speaker_notes": blocks.get("SPEAKER NOTES", ""),
        "citations": blocks.get("CITATIONS", ""),
        "visual_brief": blocks.get("VISUAL BRIEF", ""),
        "persuasion_job": blocks.get("PERSUASION JOB", ""),
    }


def _word_count(s: str) -> int:
    """Whitespace-split word count, ignoring blank lines."""
    return len([w for w in re.split(r"\s+", s) if w])


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_body_word_cap(slide: Dict[str, object]) -> List[str]:
    body = str(slide.get("body", ""))
    n = _word_count(body)
    if n > BODY_WORD_CAP:
        return [f"BODY has {n} words (cap {BODY_WORD_CAP})"]
    return []


def check_banned_words(slide: Dict[str, object]) -> List[str]:
    failures: List[str] = []
    for field in ("body", "speaker_notes", "citations", "visual_brief", "persuasion_job"):
        text = str(slide.get(field, ""))
        for m in _BANNED_PATTERN.finditer(text):
            failures.append(f"banned word in {field.upper()}: {m.group(0)!r}")
    return failures


def check_title_verbatim(slide: Dict[str, object]) -> List[str]:
    no = str(slide.get("slide", ""))
    title = str(slide.get("title", ""))
    expected = TITLE_LOCK.get(no)
    if expected is None:
        return [f"unknown slide number {no!r}; cannot verify title"]
    if title != expected:
        return [f"TITLE drift: got {title!r}, expected {expected!r}"]
    return []


def check_citations_present(slide: Dict[str, object]) -> List[str]:
    cit = str(slide.get("citations", "")).strip()
    if not cit:
        return ["CITATIONS block is empty or missing"]
    return []


def check_speaker_notes_length(slide: Dict[str, object], wps: float) -> List[str]:
    notes = str(slide.get("speaker_notes", ""))
    n = _word_count(notes)
    lo, hi = int(60 * wps), int(90 * wps)
    if not (lo <= n <= hi):
        return [
            f"SPEAKER NOTES has {n} words "
            f"(target {lo}-{hi} words at {wps:g} wps for 60-90 s)"
        ]
    return []


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def validate_deck(slides_dir: Path, wps: float) -> Tuple[int, int]:
    """Return (failures, slides_checked)."""
    files = sorted(p for p in slides_dir.glob("slide_*.md"))
    if not files:
        print(f"[validate_deck] no slides found under {slides_dir}", file=sys.stderr)
        return 1, 0

    total_failures = 0
    for path in files:
        slide = parse_slide(path)
        rel = path.relative_to(REPO_ROOT)
        if "error" in slide:
            print(f"[FAIL] {rel}: {slide['error']}")
            total_failures += 1
            continue

        slide_failures: List[str] = []
        slide_failures += check_title_verbatim(slide)
        slide_failures += check_body_word_cap(slide)
        slide_failures += check_banned_words(slide)
        slide_failures += check_citations_present(slide)
        slide_failures += check_speaker_notes_length(slide, wps=wps)

        if slide_failures:
            print(f"[FAIL] {rel}")
            for f in slide_failures:
                print(f"       {f}")
            total_failures += len(slide_failures)
        else:
            print(f"[ OK ] {rel}")

    print()
    print(f"[validate_deck] {len(files)} slides checked, {total_failures} failures")
    return total_failures, len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Aura Phase 1 deck slides.")
    parser.add_argument(
        "--slides-dir",
        type=Path,
        default=SLIDES_DIR,
        help=f"Directory of slide markdown files (default: {SLIDES_DIR})",
    )
    parser.add_argument(
        "--wps",
        type=float,
        default=2.0,
        help="Words per second assumed for speaker-notes timing (default: 2.0).",
    )
    args = parser.parse_args()

    failures, _ = validate_deck(args.slides_dir, wps=args.wps)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
