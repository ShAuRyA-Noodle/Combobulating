# Phase 2 Silence Budget KPI Report — TEMPLATE

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Per `plan.md` §1.2 ("a new state variable, the **Silence Budget**,
tracks Aura's daily quota of proactive surfaces") and `plan.md` §13
(orchestrator hard cap: 3 / day, 1 / 30-min, 0 if recovering).

The Silence Budget is one of Aura's signature wedges. Phase 2 ships
quantitative evidence that the budget is honoured in practice and
that users actively engage with the refund mechanism.

---

## 1. KPI definition

| Metric | Definition | Target |
|---|---|---|
| Avg surfaces / day / user | Mean number of proactive surfaces per active day per user across the 7-day pilot | ≤ 3.0 (hard cap) |
| Median surfaces / day / user | Robust central tendency | ≤ 2.0 (silent-by-default principle) |
| 0-token days / total days | Fraction of user-days with zero proactive surfaces (Aura stays silent the whole day) | ≥ 30% (silence is a feature) |
| 1-token days | Fraction with 1 surface | tracking only |
| 2-token days | Fraction with 2 surfaces | tracking only |
| 3-token days (cap hit) | Fraction with 3 surfaces (limit reached) | ≤ 25% (cap should rarely bind) |
| Refund rate | Fraction of surfaces that the user tapped "useful" (and got a token back) | ≥ 40% |
| Cap-bound suppression count | Number of additional proactive surfaces that were suppressed because the day's budget was exhausted | tracking only |
| Median time-to-first-surface per active day | Wall-clock from first phone-unlock to first Aura surface | tracking only |
| Per-agent surface attribution | Comms / Calendar / Finance / Wellness share of total surfaces | tracking only |

---

## 2. Headline measurements

| Metric | Target | Measured | 95% CI | Pass / Fail |
|---|---|---|---|---|
| Avg surfaces / day / user | ≤ 3.0 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Median surfaces / day / user | ≤ 2.0 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 0-token-day fraction | ≥ 30% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 3-token-day (cap-hit) fraction | ≤ 25% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Refund rate | ≥ 40% | [REPLACE WITH MEASURED VALUE]% | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 3. Distribution of token consumption (0 to 3)

| Tokens consumed (per user-day) | Count of user-days | Fraction |
|---|---|---|
| 0 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| 1 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| 2 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| 3 (cap hit) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| **Total user-days** | **[REPLACE WITH MEASURED VALUE]** | **100%** |

Sanity expectation (not a hard target): a heavy-tailed distribution
with a peak at 1, fat 0 tail, and a thin 3 tail. If 3 dominates,
either the orchestrator policy is too eager or the user expected
more — either case is a finding.

---

## 4. Per-agent attribution

| Agent | Total surfaces | Mean / day / user | Refund rate |
|---|---|---|---|
| Comms | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| Calendar | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| Finance | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |
| Wellness | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE]% |

The agent with the highest refund rate is the agent whose surfaces
the user found most useful. The agent with the lowest refund rate
is the candidate for tighter policy or LoRA retraining.

---

## 5. Suppression evidence

When the daily budget is exhausted, the orchestrator suppresses
additional candidate surfaces. Per `plan.md` §13 these still emit
Reasoning Trace fragments — they just do not surface to the user.

| Metric | Value |
|---|---|
| Total candidate surfaces evaluated | [REPLACE WITH MEASURED VALUE] |
| Total candidate surfaces suppressed by budget | [REPLACE WITH MEASURED VALUE] |
| Suppression fraction | [REPLACE WITH MEASURED VALUE]% |
| Top 3 reasons surfaces were generated but suppressed | [REPLACE WITH MEASURED VALUE] |

---

## 6. User satisfaction with the budget feature

Drawn from `pilot/quant_survey.md` Likert items.

| Survey item | Mean Likert (1–5) | Target |
|---|---|---|
| "Aura's daily 3-surface cap felt right" | [REPLACE WITH MEASURED VALUE] | ≥ 4.0 |
| "I understood how to give a 'useful' tap to refund a token" | [REPLACE WITH MEASURED VALUE] | ≥ 4.0 |
| "I would lower the cap further (silent-by-default)" | [REPLACE WITH MEASURED VALUE] / 5 | tracking |
| "I would raise the cap" | [REPLACE WITH MEASURED VALUE] / 5 | tracking |

If a non-trivial fraction of users want a lower cap, that is a
positive signal for the silent-by-default principle, not a negative.

---

## 7. Notebook of record

`pilot/analysis/notebooks/silence_budget_kpi.ipynb` (to be added in
Phase 2 alongside the existing five notebooks).

Raw input: `pilot/analysis/raw/silence_budget_events.csv`
(per-event log with `{user_id, ts, agent, action_type, surfaced,
suppressed_reason, refund}` columns).

---

## 8. Sign-off

| Role | Name | Date |
|---|---|---|
| Telemetry pipeline owner | Shorya Gupta | [REPLACE WITH MEASURED VALUE] |
| Analysis owner | Shaurya Punj | [REPLACE WITH MEASURED VALUE] |
| Anonymisation reviewer | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

— end of 05_silence_budget_kpi.md —
