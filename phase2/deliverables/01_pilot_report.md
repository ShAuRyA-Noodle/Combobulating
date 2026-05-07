# Phase 2 Pilot Evidence Report — TEMPLATE

Galaxy Brain — Aura — Samsung EnnovateX 2026.

This template carries the structure required by `plan.md` §22.3
(statistical reporting). Every numeric cell is tagged
`[REPLACE WITH MEASURED VALUE]`. Do not ship until every tag is
replaced with a value computed by `pilot/analysis/notebooks/*.ipynb`
against real participant CSVs.

Inspector: Samsung judges and the Phase 2 reviewer panel.
Audit reproducibility: every value below must trace to a row in
`pilot/analysis/raw/*.csv` or a cell in a committed notebook.

---

## 1. Study summary

| Field | Value |
|---|---|
| Pilot dates | [REPLACE WITH MEASURED VALUE] |
| Quantitative participants enrolled | [REPLACE WITH MEASURED VALUE] |
| Quantitative participants completed | [REPLACE WITH MEASURED VALUE] |
| Qualitative participants enrolled | [REPLACE WITH MEASURED VALUE] |
| Qualitative participants completed | [REPLACE WITH MEASURED VALUE] |
| Drop-out reasons | [REPLACE WITH MEASURED VALUE] |
| Distribution: hostel / day-scholar | [REPLACE WITH MEASURED VALUE] |
| Distribution: gender | [REPLACE WITH MEASURED VALUE] |
| Distribution: year of study | [REPLACE WITH MEASURED VALUE] |

---

## 2. KPI results — headline table

Notebook of record: `pilot/analysis/notebooks/02_kpi_uplift.ipynb`.

| KPI | Target (per `plan.md` §3.1) | Measured | 95% CI | Cohen's d | Pass / Fail |
|---|---|---|---|---|---|
| Effort reduction (time + tap-count) | ≥ 30% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Task completion | ≥ 90% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | n/a | [REPLACE WITH MEASURED VALUE] |
| AI autonomy quality | ≥ 85% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | n/a | [REPLACE WITH MEASURED VALUE] |
| Satisfaction (Likert 7-dim mean) | ≥ 4.5 / 5 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | n/a | [REPLACE WITH MEASURED VALUE] |
| Stress reduction (HRV ΔRMSSD) | qualitative + HRV trend | [REPLACE WITH MEASURED VALUE] ms | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Willingness to pay ₹199/mo | ≥ 60% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | n/a | [REPLACE WITH MEASURED VALUE] |

---

## 3. Per-task baseline-vs-prototype paired difference

Tasks per `plan.md` §22.2.

| # | Task | Baseline mean (s) | Prototype mean (s) | Δ (s) | 95% CI | Paired t / Wilcoxon p | Cohen's d |
|---|---|---|---|---|---|---|---|
| 1 | Triage 50 unread WhatsApp + reply to 3 actionable | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 2 | Morning calendar + travel time + leave-time | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 3 | Categorise yesterday's spend + budget check | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 4 | After 30-min stress, reach calmer state | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 5 | Pick the right two of five received messages | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

Same shape required for tap-count.

---

## 4. AI autonomy quality — inter-rater agreement

Notebook of record: `pilot/analysis/notebooks/04_autonomy_quality.ipynb`.

| Metric | Value |
|---|---|
| Sample size (random Aura actions) | [REPLACE WITH MEASURED VALUE] / 100 |
| Number of raters | 3 |
| Mean relevance Likert (1–5) | [REPLACE WITH MEASURED VALUE] |
| Mean quality Likert (1–5) | [REPLACE WITH MEASURED VALUE] |
| Binary correct rate | [REPLACE WITH MEASURED VALUE]% |
| Cohen's κ rater 1 vs 2 | [REPLACE WITH MEASURED VALUE] |
| Cohen's κ rater 1 vs 3 | [REPLACE WITH MEASURED VALUE] |
| Cohen's κ rater 2 vs 3 | [REPLACE WITH MEASURED VALUE] |
| Fleiss' κ across 3 raters | [REPLACE WITH MEASURED VALUE] |

---

## 5. Load Score validation — Spearman correlation

Notebook of record: `pilot/analysis/notebooks/03_load_score_validation.ipynb`.

| Metric | Value |
|---|---|
| Sample size (paired Load Score + self-rated stress 1–5) | [REPLACE WITH MEASURED VALUE] |
| Spearman ρ (Load Score, self-rated stress) | [REPLACE WITH MEASURED VALUE] |
| 95% CI on ρ (bootstrap, 1000 resamples) | [REPLACE WITH MEASURED VALUE] |
| p-value | [REPLACE WITH MEASURED VALUE] |

---

## 6. Willingness to pay — Van Westendorp

Notebook of record: `pilot/analysis/notebooks/05_wtp.ipynb`.

| Price point | Value |
|---|---|
| Too cheap (loses trust) | ₹[REPLACE WITH MEASURED VALUE] |
| Cheap (bargain) | ₹[REPLACE WITH MEASURED VALUE] |
| Expensive (still consider) | ₹[REPLACE WITH MEASURED VALUE] |
| Too expensive (refuse) | ₹[REPLACE WITH MEASURED VALUE] |
| Optimal price point (intersection of cheap and expensive) | ₹[REPLACE WITH MEASURED VALUE] |
| Indifference price point | ₹[REPLACE WITH MEASURED VALUE] |
| Binary "would pay ₹199/mo" yes-rate | [REPLACE WITH MEASURED VALUE]% |

---

## 7. Qualitative themes (n = 8)

Per `plan.md` §23.3, two coders, thematic analysis.

| Theme | Frequency | Representative quote (anonymised) |
|---|---|---|
| [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | "[REPLACE WITH MEASURED VALUE]" |
| [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | "[REPLACE WITH MEASURED VALUE]" |
| [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | "[REPLACE WITH MEASURED VALUE]" |
| [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | "[REPLACE WITH MEASURED VALUE]" |
| [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | "[REPLACE WITH MEASURED VALUE]" |

Inter-coder reliability (Cohen's κ): [REPLACE WITH MEASURED VALUE].

---

## 8. Raw data publication

Per `plan.md` §22.3 last bullet — raw CSV published in repo.

| File | Status |
|---|---|
| `pilot/analysis/raw/quant_durations.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/quant_taps.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/quant_completion.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/quant_satisfaction.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/quant_wtp.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/autonomy_ratings.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/load_score_paired.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/qual_diary.csv` | [REPLACE WITH MEASURED VALUE] |
| `pilot/analysis/raw/qual_interviews_coded.csv` | [REPLACE WITH MEASURED VALUE] |

All files anonymised per `plan.md` §23.5 before commit. Owner of
anonymisation pass: Shaurya. Sign-off date: [REPLACE WITH MEASURED VALUE].

---

## 9. Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Single-campus recruitment (Thapar + 2 Bangalore) | Generalisability | Phase 3 talking point: representative of Indian Gen Z college subset |
| iOS-only build | No Android measurement | Galaxy emulator screen-record (`03_galaxy_emulator_demo.md`) |
| 7-day window | Long-horizon habituation unmeasured | Note as future work |
| HRV requires consistent Watch wear | Drop-out for non-wearers | Backup signal mix (typing entropy + app-switch) keeps Load Score functional |

---

## 10. Sign-off

| Role | Name | Date |
|---|---|---|
| Lead author | Shaurya Punj | [REPLACE WITH MEASURED VALUE] |
| Co-author | Shorya Gupta | [REPLACE WITH MEASURED VALUE] |
| Anonymisation reviewer | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

— end of 01_pilot_report.md —
