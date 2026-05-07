# ADR-0011 — No Apple Developer Program: Wizard-of-Oz Lab Study Replaces TestFlight Self-Install

## Status

Accepted (2026-05-07). Supersedes the TestFlight clause of ADR-0010 §Decision (sample-delivery mechanism only; the n=30 + n=8 sample target is unchanged). Source: `plan.md` §22, §23, §24 (Week 8–9), §26 (budget); ADR-0006 (Apple-only Phase 1+2); ADR-0010 (pilot protocol).

## Context

The Apple Developer Program (ADP) costs USD 99 per year (~₹8,300 at 2026-05-07 RBI mid-rate). The total Aura project budget is ₹2,000 (`plan.md` §26). ADP enrolment alone is more than four times the entire project spend.

Without a paid ADP membership the team cannot:

- Distribute via TestFlight (TestFlight requires App Store Connect, which requires ADP).
- Distribute via Ad Hoc (Ad Hoc provisioning profiles require a paid Team ID).
- Push silent background or notification entitlements that require capability provisioning.

What the team **can** do for free, with the existing Apple ID signed into Xcode 16 on the team Mac:

- Generate a **Personal Team** (free) signing certificate.
- Sign and install a development build on a physical iPhone that is connected to the same Mac and signed in with the same Apple ID.
- Run that build on the device for **7 days**, after which the Personal Team certificate expires and the app refuses to launch until re-signed.
- Use up to 3 app IDs and 10 unique provisioning profiles per 7-day window.

Constraints:

- Total budget cap of ₹2,000 (`plan.md` §26). ADP at ₹8,300/yr cannot be absorbed.
- Team is two undergraduates at Thapar Patiala. There is no faculty or institutional Apple Developer enrolment available to piggyback on within the Phase 2 timeline.
- The pilot must still meet ADR-0010 sample targets: 30 quantitative + 8 qualitative, with the n=8 HRV pre/post 7-day comparison (`plan.md` §22).
- Phase 2 timeline (`plan.md` §24): qualitative pilot Week 8 (Jun 25 – Jul 1), quantitative pilot Week 9 (Jul 2 – Jul 8). 14 calendar days.

Forces:

- The brief rewards verifiable raw evidence; supervised lab data is *more* verifiable than unsupervised self-install field data.
- Self-install via TestFlight on n=30 carries an attrition tax (10–25% drop-out is normal in unpaid 7-day field studies). Supervised in-person sessions effectively eliminate diary-attrition and install-support overhead.
- Wizard-of-Oz and supervised lab studies are the HCI-research norm for n ≤ 50 (Kelley 1984, Maulsby 1993, Dahlbäck 1993). They are not a downgrade.

## Decision

The team will **not** enrol in the Apple Developer Program. The pilot delivery mechanism changes from "TestFlight self-install on each participant's phone for 7 days" to a **Wizard-of-Oz supervised lab study on a single team-owned iPhone** signed weekly with the free Personal Team certificate.

Concretely:

- Aura is compiled on the team Mac (Xcode 16) and signed with Shaurya's Apple ID Personal Team certificate.
- The build is installed on Shaurya's iPhone (the demo device).
- HealthKit, EventKit, and notification permissions are granted on the demo device once and persist across sessions.
- Each participant comes to a booked room on Thapar campus (or Bangalore equivalent), performs the 5 standardised tasks (`task_protocol.md`) on the demo device while screen-mirrored to the Mac via QuickTime, then completes the post-trial survey (`quant_survey.md`) and — for the n=8 qualitative subset — the 60-minute interview (`qual_protocol.md`) in the same session.
- The Personal Team certificate is re-signed every 7 days using the script at `aura/scripts/resign_aura.sh`. The pilot fits inside two 7-day windows (Week 8 + Week 9 per `plan.md` §24).
- Total researcher time: 30 sessions × 30 min = 15 hours plus 8 × 60 min qualitative interviews folded into the same sessions = 8 additional hours = ~23 researcher-hours over 14 calendar days. Spread across two researchers this is comfortably within the budget.

The full lab-study procedure is at `aura/pilot/wizard_of_oz_protocol.md`. The signing script is at `aura/scripts/resign_aura.sh`. The amended consent form is at `aura/pilot/CONSENT_v2.md`. Data handling is at `aura/pilot/data_handling.md`.

The HRV pre/post comparison for n=8 still works: HealthKit on each participant's *own* Apple Watch records HRV in the 7 days surrounding the lab session. Participants export their HealthKit XML at the start and at the end of their participation window and share the de-identified extract. No app install on the participant's phone is required for this measurement.

## Consequences

Positive:

- **Budget honoured.** No ADP fee. Total project spend stays at ₹2,000.
- **Higher data quality than self-install.** Every session is supervised; every recording is reviewed; there is no diary-loss or install-support burden. This is methodologically *stronger* evidence than unsupervised TestFlight, not weaker.
- **No attrition tax.** Replace dropouts from a waitlist; aim 35 recruited for 30 completed.
- **No support cost.** Participants do not install anything; "my phone is full" / "TestFlight expired" / "I forgot to open it today" failure modes vanish.
- **Three-rater autonomy quality (`plan.md` §22, ≥85%) becomes easier**, because every Aura action is captured in the QuickTime screen recording with timestamps, ready for the 100-action sampling.
- **Privacy posture improves.** Participants never grant HealthKit/Gmail to a build on their own phone. They observe Aura on the team device. ADR-0005 (on-device only) remains intact and the participant's personal device is never touched by Aura code.

Negative / costs:

- **Single-device latency variance.** All participants share one iPhone. If the device thermally throttles after 6 sessions, latency rises. Mitigated by a 5-minute cool-down between sessions and a "device temperature" field in the per-session log (`pilot/wizard_of_oz_protocol.md` §Threats).
- **Observer effect.** Participant knows the researcher is watching. Mitigated by the standard lab protocol: researcher faces away, silent except for start cues, no leading prompts (`task_protocol.md` §4).
- **Novelty effect.** Each participant uses Aura for ~8 minutes, not 7 days. The 7-day longitudinal claim now applies only to the n=8 HRV cohort (who export their own Watch HRV), not to the full n=30. The Phase 2 report reframes accordingly: the n=30 number is "first-encounter task performance + WTP", and the longitudinal claim is qualified to n=8.
- **Re-sign cadence overhead.** ~10 minutes of researcher time every 7 days to re-build and re-install. Codified in `aura/scripts/resign_aura.sh`.
- **No over-the-air install.** Participants who want to keep Aura on their own phone after the lab session cannot. A documented secondary path via AltStore + AltServer is provided at `aura/pilot/sideload_guide.md` for those who ask, but it is not required and not part of the pilot data set.

## Alternatives

- **(a) Buy ADC at ₹8,300/year.** Rejected. Violates `plan.md` §26 budget cap by 4×. The team will not buy.
- **(b) Ad Hoc distribution.** Rejected. Ad Hoc still requires a paid Team ID; same cost as TestFlight. Not a free alternative.
- **(c) Sideload via AltStore + AltServer.** Acceptable as a *secondary* path for participants who want to keep Aura on their own phone after the lab session. Documented at `aura/pilot/sideload_guide.md`. Not used as the primary pilot delivery mechanism because (i) it still requires an Apple ID Personal Team cert per device and weekly re-sign, (ii) AltServer must be running on a desktop on the same Wi-Fi at re-sign time, which is impractical to coordinate across 30 participants, (iii) it shifts the install-support burden onto the participant.
- **(d) Android-only pilot via Galaxy emulator.** Rejected. The team owns iPhones, an Apple Watch, and AirPods; the closed-loop biometric wedge (`plan.md` §22 stress KPI, ADR-0006) requires a real Apple Watch reading HRV. An emulator cannot deliver this. Switching the pilot to Android also breaks ADR-0006 §Decision (Apple-only Phase 1 and Phase 2 build). The Android emulator port stays as the platform-parity demonstration only, per ADR-0006.
- **(e) Faculty-sponsored institutional ADP enrolment.** Considered. Thapar does not currently hold an institutional ADP membership accessible to undergraduate hackathon teams within Phase 2 timeline. Reconsider for a future published study.

End of ADR-0011.
