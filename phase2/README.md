# Phase 2 — Aura

Galaxy Brain — Samsung EnnovateX 2026.

This directory carries every Phase 2 deliverable scaffold. Phase 2 is
contingent on shortlist from Phase 1. Once the shortlist email
arrives, the team has approximately three weeks to ship.

---

## What Phase 2 ships

Per `plan.md` §34.1:

1. Working prototype on Android (Galaxy primary) with iOS reference
   build distributed via TestFlight.
2. 30-user pilot completed, raw data published (8 qualitative + 30
   quantitative).
3. Galaxy Watch integration via Health Connect (emulator-based for
   the no-Galaxy-hardware constraint per §21).
4. Cross-device handoff demo — phone + tablet pull-tab.
5. Refined Reasoning Trace (Phase 1 Phase 2 polish round).
6. Demo video, full repo, README updated.

---

## When Phase 2 ships

Indicative timeline relative to Phase 1 deadline:

| Milestone | Target (Phase-1 + N days) |
|---|---|
| Shortlist email received | T0 |
| Build sprint window | T0 + 1 → T0 + 14 |
| Qual pilot (n = 8) | T0 + 14 → T0 + 17 |
| Quant pilot (n = 30) | T0 + 17 → T0 + 21 |
| Analysis + writeup | T0 + 21 → T0 + 24 |
| Phase 2 submission | T0 + 24 |

Phase 2 deliverables submission target: **Phase 1 deadline + 3 weeks**.

---

## Gating actions

Nothing in this directory ships measured numbers until the gating
action is complete. Every placeholder uses the literal tag
`[REPLACE WITH MEASURED VALUE]`. Do not fabricate numbers under any
circumstance — Samsung judges will scan the repo.

| Deliverable | Gate |
|---|---|
| `deliverables/01_pilot_report.md` | 30-user quant pilot run + analysis notebooks executed against real CSVs |
| `deliverables/02_lora_adapters_README.md` | Local RTX 4080 LoRA training runs complete for Comms + Finance + Orchestrator with eval harness numbers logged |
| `deliverables/03_galaxy_emulator_demo.md` | Comms + Wellness agents ported into Pixel + Galaxy AVD with screen-record produced |
| `deliverables/04_threat_model_validation.md` | Penetration audit run against the running prototype with pass/fail logged for the five named adversaries |
| `deliverables/05_silence_budget_kpi.md` | In-app telemetry on the Silence Budget collected over the 7-day pilot window |

---

## Directory layout

```
phase2/
├── README.md                                  (this file)
├── checklist.md                                Phase 2 submission gate
└── deliverables/
    ├── 01_pilot_report.md                      Pilot evidence report template
    ├── 02_lora_adapters_README.md              LoRA adapter delivery README
    ├── 03_galaxy_emulator_demo.md              Galaxy emulator demo spec
    ├── 04_threat_model_validation.md           Threat model penetration checklist
    └── 05_silence_budget_kpi.md                Silence Budget KPI report template
```

---

## Status

Phase 2 — **scaffolded**. Awaiting Phase 1 shortlist email.

— end of phase2/README.md —
