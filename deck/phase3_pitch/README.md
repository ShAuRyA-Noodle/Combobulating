# Aura — Phase 3 Finals Deck

This directory holds the spec, run-of-show, and Q&A bank for the
Phase 3 finals deck. It is the **narrative-led variant** (deck_spec.md
§11.2 Variant B, with §11.3 Variant C beats folded in) — the version
the team ships to the wider, mixed audience at finals.

## How Phase 3 differs from Phase 1 Blueprint

| Beat                   | Phase 1 Blueprint              | Phase 3 Finals                                 |
| ---------------------- | ------------------------------ | ---------------------------------------------- |
| Slide count            | 9-11 (template ceiling)        | 12-15 (storytelling-first)                     |
| Driver                 | Template-first — every required AX field present | Storytelling-first — narrative arc over template |
| Live demo              | Optional (Phase 1 is paper)    | **Embedded** — slides 6 + 8 dock to the live demo |
| Q&A                    | Optional 30-question bank      | **Rehearsed 50-question bank**, two presenters split |
| Ask                    | Implicit (judges grade)        | **One explicit ask slide** at slide 13         |
| Team                   | Slide 1 only                   | **Slide 1 + slide 14 (face shots, contact)**   |
| Visual system          | Editorial cover, hero numbers  | **Reuses Phase 1** — same palette, same Fraunces / Inter Tight / JetBrains Mono lockup |
| Accent rule            | ≤ 3 sunset orange / slide      | Same                                           |
| Body word cap          | ≤ 30 / slide                   | Same                                           |
| Banned words           | 12-word list                   | Same                                           |

## File index

- `spec.md` — full per-slide spec for the 14-slide finals deck.
  Each slide carries title, hero visual, body, speaker notes, persuasion
  job, and visual brief.
- `run_of_show.md` — minute-by-minute timing for the 7-min pitch + 3-min
  Q&A finals slot. Cue words, presenter handoffs, and live-demo dock
  points.
- `qa_bank_extended.md` — 50 anticipated judge questions and rehearsed
  answers. The 30 from `demo/qa_anticipated.md` plus 20 new questions
  pulled from the deeper Phase 3 audience (Samsung Ventures partner,
  policy / regulatory, customer-success, Galaxy AI design lead).

## Visual system (reused from Phase 1)

- **Palette.** Warm off-white `#FAF8F5` background. Ink black `#0E0E0E`
  text. Single accent: sunset orange `#FF5B2E`, used ≤ 3 times per slide
  on load-bearing artefacts only. Reasoning Trace in mono.
- **Fonts.** Fraunces (Regular, lining figures, no swashes) for hero
  numerals and slide titles. Inter Tight (Regular / Medium) for body and
  speaker copy. JetBrains Mono 14 pt for code, JSON, and the Reasoning
  Trace render. Same lockup as Phase 1 deck.
- **Grid.** 12-col / 60 px gutter. Hero artefact dominates; body lives
  in cols 9-12 unless a number-as-hero slide.
- **Photography.** None. The team is the cover, not a stock photo.
- **Iconography.** None. If you reach for an icon, redraw the artefact
  bigger instead.
- **Charts.** Linear-style — orthogonal axes, square-ended ticks, no
  gradients, no glow. Single accent per chart.

## Anti-cliché audit (carried over)

The same six checks from `deck/phase1_blueprint/anti_cliche_audit.md`
apply to every Phase 3 slide. The validator at
`scripts/validate_deck.py` enforces the body-cap, banned-word, and
title-verbatim checks; the rest is human-graded before commit.

## Lock points

Lock these before the dress rehearsal and never change them after:

1. The opening line at 0:00-0:20 (verbatim, see `run_of_show.md`).
2. The two-sentence ask on slide 13.
3. The closing line on slide 14.
4. The slide-3 Reasoning Trace render — same JSON, same cursor position
   in the drawer mockup.

## How to verify

The Phase 1 validator does not currently check Phase 3 slides — finals
deck spec is a markdown spec, not a slide source. When the team
hand-builds the slides in Figma / Keynote, drop the per-slide
markdown drafts under `phase3_pitch/slides/` and extend
`scripts/validate_deck.py` to walk both directories.
