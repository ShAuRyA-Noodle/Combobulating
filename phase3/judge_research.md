# Phase 3 Judge Research

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Per `plan.md` §2 (typical EnnovateX judge mix) and §32 (Judges Memo
single-sentence mappings).

This file pre-loads research on five **named-archetype** judges
likely to sit on the Bangalore finals panel. Real names are not
publicly committed by Samsung this far in advance; archetypes are
based on the Samsung Research India Bangalore + One UI / Bixby +
Galaxy ecosystem + Samsung Ventures + academic-advisor mix that
EnnovateX panels reliably pull from in past years.

When the actual panel is published (typically T-7 days), this file
gets a follow-up edit with real names. Until then, archetypes hold.

---

## Judge 1 — Senior R&D engineer, Samsung Research India Bangalore

**Archetype profile:** ~12–18 years at Samsung; led on-device ML
features in Galaxy AI (Live Translate, Note Assist, Photo Assist).
Cares about latency, memory footprint, model quantisation, security
substrate. Has personally shipped to ≥ 100M users.

**What they care about:**
- Latency on real devices, not benchmark numbers.
- Memory footprint of the LLM on a 6 GB RAM phone.
- Whether the architecture would survive a Knox audit.
- Whether the team has measured anything on hardware they own.

**Tailored opening line for Q&A:**
> "We measured on-device latency on iPhone 13 — 280 ms median for
> the orchestrator, sub-300 ms for every agent. Galaxy port targets
> the same envelope; the API parity table on slide 4 names the
> equivalent runtimes."

**What to NOT say to this judge:**
- Anything about cloud LLMs.
- Marketing language about empathy.
- Rough numbers without device + condition.

**Slide they will inspect hardest:** Slide 4 + slide 4a + slide 7.

---

## Judge 2 — One UI / Galaxy AI Product Manager

**Archetype profile:** PM lead on a Galaxy AI feature shipped to
One UI 6 or 7. Cares about cross-app continuity, accessibility,
permission UX, the user's first three taps, and how the product
will land on a Samsung Galaxy launcher feature highlight reel.

**What they care about:**
- Permission UX flow.
- Cross-surface continuity (phone → watch → buds → tablet).
- Whether the product looks Samsung enough.
- Daily-active engagement vs notification fatigue.

**Tailored opening line for Q&A:**
> "The Silence Budget caps proactive surfaces at three per day. A
> Galaxy AI feature that learns to stay silent is a feature that
> survives the One UI dashboard's 'turn off this assistant' button
> ratings."

**What to NOT say to this judge:**
- Anything that signals "we will spam your users".
- Apologise for not yet shipping a Galaxy build (frame as Phase 2).

**Slide they will inspect hardest:** Slide 3 + slide 5 + slide 9.

---

## Judge 3 — Bixby PM or Samsung Ventures investor

**Archetype profile:** Either runs the Bixby roadmap, or invests on
behalf of Samsung Ventures. Cares about willingness to pay, market
size, defensibility, and whether the team has talked to real users.

**What they care about:**
- Van Westendorp price point and the binary 60% WTP figure.
- Indian Gen Z TAM (~250M people aged 14–28 with smartphones).
- Defensibility — what stops Google or Apple from copying this.
- Founder grit and clarity.

**Tailored opening line for Q&A:**
> "Sixty percent of thirty Indian Gen Z users will pay ₹199 a month.
> Our wedge is unbuyable: Indian context depth plus biometric
> closed loop plus glass-box. A global assistant cannot ship UPI
> SMS parsing and IRCTC PNR ingestion and BMTC live data the way an
> Indian-built assistant can — and we have measured the gap."

**What to NOT say to this judge:**
- "We will build a community first and monetise later."
- Vague TAM numbers without source.

**Slide they will inspect hardest:** Slide 5 + slide 9.

---

## Judge 4 — Samsung Health or Knox platform lead

**Archetype profile:** Owns Health Connect ecosystem partnerships or
Knox Vault feature parity vs Apple Private Compute. Cares about
biometric integration depth and the privacy story.

**What they care about:**
- HRV pipeline architecture.
- How Aura would talk to Samsung Health rather than HealthKit.
- Knox-equivalent storage for the memory graph.
- Audit log + tamper evidence.

**Tailored opening line for Q&A:**
> "The memory graph is encrypted with a Keystore-derived key on
> Android — directly compatible with Knox Vault. The audit log
> ships a daily Merkle root the user can verify in Settings. Both
> features run today on the iOS reference build with the equivalent
> Secure Enclave path."

**What to NOT say to this judge:**
- "We promise unbreakable privacy."
- Any claim about Knox features the team has not actually tested.

**Slide they will inspect hardest:** Slide 4 + slide 9 (privacy
posture) + the audit-log demo.

---

## Judge 5 — Indian academic advisor (typically IIIT-B, IISc, or IIT Bangalore CS faculty)

**Archetype profile:** Senior academic with publications in HCI or
mobile ML. Cares about study rigour, statistical reporting, and
whether the team can be trusted to run a real user study.

**What they care about:**
- Sample size, IRB / consent posture, raw data availability.
- Spearman ρ for Load Score validation.
- Cohen's κ for AI autonomy quality.
- Cohen's d for effort reduction.
- Limitations section, owned not hidden.

**Tailored opening line for Q&A:**
> "Eight qualitative plus thirty quantitative participants from
> Thapar campus. Raw CSVs are in the repo; every effect size is
> reported with 95% CI; Cohen's κ is reported across three raters
> for autonomy quality. The limitations section names the
> single-campus generalisability gap explicitly."

**What to NOT say to this judge:**
- Round numbers without confidence intervals.
- Hide a limitation — they will find it.

**Slide they will inspect hardest:** Slide 9 + the Phase 2 raw CSVs
in the repo.

---

## Cross-judge meta

| Judge archetype | Primary slide | Tailor opening |
|---|---|---|
| 1. R&D engineer | 4 / 4a / 7 | latency on hardware we own |
| 2. One UI PM | 3 / 5 / 9 | Silence Budget + cross-surface |
| 3. Bixby PM / Ventures | 5 / 9 | WTP + defensibility |
| 4. Health / Knox lead | 4 / 9 | encrypted memory + audit log |
| 5. Academic | 9 | rigour + limitations |

---

## Update protocol

When the actual panel is published:

- [ ] [PENDING] Replace each archetype with real name + role + LinkedIn
- [ ] [PENDING] Re-tailor opening line per real judge's recent talks / blog posts
- [ ] [PENDING] Search Twitter / X for last 3 months of public commentary
- [ ] [PENDING] Brief Shaurya + Shorya on each judge by name 24h before stage

— end of judge_research.md —
