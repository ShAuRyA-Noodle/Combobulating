# Phase 2 Submission Checklist

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Submission gate: every item ticked or `[PENDING]`. Due date is
**Phase 1 deadline + 3 weeks** (typical EnnovateX Phase 2 cadence;
team confirms exact date when shortlist email arrives).

Owner abbreviations: SP = Shaurya Punj, SG = Shorya Gupta.

---

## A. Prototype build

- [ ] [PENDING] iOS TestFlight build distributed to ≥ 30 participants — owner: SG
- [ ] [PENDING] Android (Pixel + Galaxy-class AVD) port of CommsAgent + WellnessAgent — owner: SG
- [ ] [PENDING] On-device LLM inference path live (Gemma 2B via MLX on iPhone, MediaPipe on Android emulator) — owner: SP
- [ ] [PENDING] Phi-3-mini orchestrator wired with typed tool calls on-device — owner: SP
- [ ] [PENDING] Watch glance + AirPods nudge surfaces working on iOS — owner: SP
- [ ] [PENDING] Cross-device pull-tab demo (phone + tablet via Multipeer Connectivity) — owner: SG

## B. Pilot evidence

- [ ] [PENDING] 8 qualitative participants interviewed; daily diary collected — owner: SP
- [ ] [PENDING] 30 quantitative participants completed 5 standardised tasks — owner: SP
- [ ] [PENDING] All five `pilot/analysis/notebooks/*.ipynb` executed against real CSVs — owner: SP
- [ ] [PENDING] `phase2/deliverables/01_pilot_report.md` populated with measured values — owner: SP
- [ ] [PENDING] `pilot/analysis/raw/*.csv` committed and anonymised — owner: SG
- [ ] [PENDING] Spearman ρ for Load Score vs self-rated stress reported — owner: SP
- [ ] [PENDING] Cohen's κ for AI autonomy quality reported (3 raters) — owner: SP
- [ ] [PENDING] Cohen's d for effort reduction reported per task — owner: SP

## C. Models

- [ ] [PENDING] CommsAgent LoRA trained on RTX 4080; loss curves committed; eval harness numbers logged — owner: SP
- [ ] [PENDING] FinanceAgent LoRA trained; same — owner: SP
- [ ] [PENDING] Orchestrator LoRA evaluated against off-the-shelf Phi-3-mini; ship if measured gain — owner: SP
- [ ] [PENDING] GGUF Q4_K_M exports + MLX exports produced — owner: SP
- [ ] [PENDING] SHA-256 hashes of all weight artefacts logged in `phase2/deliverables/02_lora_adapters_README.md` — owner: SP

## D. Galaxy emulator demo

- [ ] [PENDING] 90-second screen-record produced per `phase2/deliverables/03_galaxy_emulator_demo.md` shot list — owner: SG
- [ ] [PENDING] Honest framing line subtitle burned in — owner: SG
- [ ] [PENDING] Health Connect mock fixtures committed — owner: SP
- [ ] [PENDING] Video uploaded to GitHub Release tagged `phase2-emulator-demo-v1` — owner: SG

## E. Privacy + security

- [ ] [PENDING] All 20 rows of `phase2/deliverables/04_threat_model_validation.md` exercised; pass / fail logged — owner: SP + SG (rotate attacker / defender)
- [ ] [PENDING] Encryption at rest live (SQLCipher + Keystore / Secure Enclave keys) — owner: SG
- [ ] [PENDING] Audit log Merkle root displayed in Settings — owner: SG
- [ ] [PENDING] Panic-wipe gesture wired and tested — owner: SG
- [ ] [PENDING] OAuth scope minimisation verified (`gmail.readonly` + `gmail.metadata` only) — owner: SP

## F. Silence Budget KPI

- [ ] [PENDING] Telemetry pipeline shipping `silence_budget_events.csv` rows per surface event — owner: SG
- [ ] [PENDING] `pilot/analysis/notebooks/silence_budget_kpi.ipynb` notebook authored and run — owner: SP
- [ ] [PENDING] `phase2/deliverables/05_silence_budget_kpi.md` populated with measured values — owner: SP

## G. Repo + docs

- [ ] [PENDING] Updated README banner: Phase 2 status — owner: SP
- [ ] [PENDING] All AUDIT_REPORT FAIL items resolved (Slide 1 body 30, PDF, 4 [TEAM TO VERIFY] URLs, README path rot) — owner: SG
- [ ] [PENDING] Phase 2 release notes at `docs/release_notes/v0.2.0.md` — owner: SP
- [ ] [PENDING] Updated `docs/runbook.md` with pilot-day on-call procedure — owner: SP

## H. Submission package

- [ ] [PENDING] Phase 2 narrative PDF assembled — owner: SP
- [ ] [PENDING] Repo public on GitHub — owner: SG
- [ ] [PENDING] HuggingFace Space deployed at `aura/hf_space/` linked from README — owner: SP
- [ ] [PENDING] Email to EnnovateX submission portal with all required artefacts — owner: SP

---

## Aggregate gate

| Block | Items | Owner balance |
|---|---|---|
| A. Prototype build | 6 | SP × 3, SG × 3 |
| B. Pilot evidence | 8 | SP × 7, SG × 1 |
| C. Models | 5 | SP × 5 |
| D. Galaxy emulator | 4 | SG × 3, SP × 1 |
| E. Privacy + security | 5 | SG × 4, SP × 1 + 1 shared |
| F. Silence Budget KPI | 3 | SP × 2, SG × 1 |
| G. Repo + docs | 4 | SP × 3, SG × 1 |
| H. Submission package | 4 | SP × 2, SG × 2 |
| **Total** | **39** | **SP × 23, SG × 16** |

Submission is "done" when all 39 items are unticked-to-ticked.

— end of phase2/checklist.md —
