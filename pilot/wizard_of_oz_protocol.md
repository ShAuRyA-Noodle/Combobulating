# Aura Pilot — Wizard-of-Oz Lab Study Protocol

Replaces the TestFlight self-install delivery mechanism with a supervised in-person lab study on a single team-owned iPhone, signed weekly via the free Apple ID Personal Team certificate. The sample target (30 quantitative + 8 qualitative) and KPI targets (`plan.md` §22) are unchanged.

Reference: `plan.md` §22, §23, §24 (Week 8–9); ADR-0010 (pilot protocol); ADR-0011 (no Apple Developer Program).
Last updated: 2026-05-07
Owner: Shaurya Punj (lead researcher) + Shorya Gupta (co-researcher / second coder)

---

## 1. Why Wizard-of-Oz beats TestFlight self-install for small-n hackathon evidence

The original ADR-0010 protocol assumed TestFlight self-install for 7 days. ADR-0011 removes that option (no Apple Developer Program). The replacement is a Wizard-of-Oz supervised lab study on a team-owned device. This is **methodologically stronger** evidence at this sample size, not weaker. Five reasons:

1. **Every session is supervised.** No "the participant forgot to open the diary on Day 4" failure mode. Researcher is in the room; the data is captured live.
2. **No diary attrition.** Self-install field studies at n=30 typically lose 10–25% of diary entries to forgetfulness or churn. The lab session captures the equivalent data in one sitting under researcher observation. Diary loss at the lab session is approximately zero.
3. **No install-support burden.** Participants never install anything. "My phone is full", "TestFlight invitation expired", "I do not know how to open the link" — all eliminated.
4. **HCI-research norm for n ≤ 50.** Wizard-of-Oz (Kelley 1984, "An iterative design methodology for user-friendly natural language office information applications", ACM TOIS 2:1) and lab-based supervised studies (Maulsby, Greenberg, Mander 1993, "Prototyping an intelligent agent through Wizard of Oz", CHI '93; Dahlbäck, Jönsson, Ahrenberg 1993, "Wizard of Oz studies — why and how", IUI '93) are the standard methodology for evaluating prototype intelligent agents at small sample sizes. We do not invent the method; we apply the established one.
5. **Capturable raw evidence per session.** Every action Aura takes is recorded in the QuickTime mirror video and the in-app instrumentation log. The 100-action sample for the autonomy KPI (`plan.md` §22, ≥85% across 3 raters) is drawn from these recordings — every claim is replayable.

The trade-off is that the longitudinal 7-day field claim shrinks. The n=30 cohort gives **first-encounter task performance + satisfaction + willingness-to-pay** evidence. The 7-day longitudinal claim (HRV pre/post, daily diary) applies to the n=8 qualitative cohort, who export HealthKit XML from their own Apple Watch — Aura does not need to be installed on the participant's own phone for this measurement.

---

## 2. Setup

### 2.1 The demo device

- **Hardware:** Shaurya's iPhone (iPhone 13 or 14, iOS 17+).
- **Build:** Aura compiled in Xcode 16 on the team Mac, signed with Shaurya's Apple ID Personal Team certificate.
- **Permissions pre-granted on the demo device, persistent across sessions:**
  - HealthKit read access (HR, HRV, sleep, steps).
  - EventKit (calendar) read access.
  - Notifications enabled.
  - Gmail read-only OAuth token attached to a dedicated test Google account `aura.pilot.thapar@gmail.com`.
- **Memory graph state:** cleared between participants via the in-app Settings → Pilot → "Reset session memory" button. Confirmed empty before each new participant. The Apple ID itself remains signed in to keep the certificate valid.
- **Test data fixtures:** the 5 standardised tasks (`task_protocol.md` §2) need their fixtures pre-loaded — 50 WhatsApp test messages on the test sandbox, calendar event for Task 2, transactions for Task 3, notification panel for Task 5. Researcher reloads fixtures between participants in the 5-minute cool-down.

### 2.2 The mirror rig

- **Mac** (team Mac with Xcode 16) with QuickTime Player open.
- **Lightning-to-USB cable** between iPhone and Mac (more reliable than wireless mirroring for 30 sessions; eliminates Wi-Fi jitter).
- **QuickTime → File → New Movie Recording → camera dropdown → Shaurya's iPhone.** This captures both screen and on-device audio.
- **Lavalier mic** clipped to the participant for clean voice capture during think-aloud and the qualitative interview. Audio mixed into the QuickTime recording.
- **Output:** one MP4 per participant, named `PNNN_session.mp4`, dropped into `pilot/raw/PNNN/`.

### 2.3 The room

- **Thapar Patiala:** Library group-study room (booked via the library reservation portal, 90-minute slot for the n=8 qual sessions, 45-minute slot for the n=22 quant-only sessions). Backup: Hostel G common room weekday afternoons when teaching is on.
- **Bangalore (n=2 of the n=8 qual cohort):** Cubbon Park or Indiranagar cafe with quiet table; or a participant's home if they offer.
- **Layout:** participant and researcher sit at right angles to the same table. Phone is on a small stand facing the participant. Mac screen faces the researcher only — the participant does not see the mirror feed unless they ask. This reduces self-consciousness during think-aloud.

### 2.4 The 7-day re-sign window

- Personal Team certificates expire 7 days after issuance. The pilot is scheduled across two 7-day windows that align with `plan.md` §24:
  - **Window A:** Jun 25 (Wed) – Jul 1 (Tue) — Week 8 — qualitative cohort + 4 quantitative-only.
  - **Window B:** Jul 2 (Wed) – Jul 8 (Tue) — Week 9 — remaining 18 quantitative.
- Re-sign happens at the start of each window and again on Day 4 of each window if the team needs a buffer. Script: `aura/scripts/resign_aura.sh`.
- A re-sign event is logged to `pilot/raw/_resign_log.txt` with timestamp and certificate fingerprint. This is part of the audit trail.

---

## 3. Per-session flow (30 minutes, quant-only) / (90 minutes, qual cohort)

The quantitative session is 30 minutes. For the n=8 qualitative cohort, the 60-minute interview folds into the same sitting after the 30-minute task session, total 90 minutes — see `qual_protocol.md` §"Wizard-of-Oz adaptation".

### Quant-only session (30 min)

```
00:00 — Welcome, water offered                                                (1 min)
00:01 — Verbal consent re-confirm + signed consent form review                (3 min)
00:04 — Baseline round: participant uses their OWN phone, 5 standard tasks    (8 min)
00:12 — Hand-off: Shaurya hands the demo iPhone to the participant            (0.5 min)
00:12 — Prototype round: participant performs the same 5 tasks on Aura        (8 min)
00:20 — Live diary: participant rates each task 1–5; researcher logs time     (3 min)
00:23 — Willingness-to-pay anchor + open-feedback question                    (5 min)
00:28 — Wrap: thank, offer to delete recording, snack, schedule next steps    (2 min)
00:30 — End
```

#### 3.1 Step-by-step

1. **Welcome (1 min).** Greet, water on the table, lavalier mic clipped on, QuickTime recording started, slate the recording verbally: "Participant PNNN, session start, [date], [time]." Both researchers' watches synced to the Mac clock at the start of the day.

2. **Verbal consent + signed consent form (3 min).** Hand over `pilot/CONSENT_v2.md` (printed). Read the four highlighted lines aloud (in-person observation, screen recording, audio recording, transcript storage). Confirm each checkbox. Both copies signed.

3. **Baseline round on participant's own phone (8 min).** Participant uses their own existing toolkit (Siri / WhatsApp / Calendar / GPay / Notification panel) to perform the 5 standardised tasks (`task_protocol.md` §2). Researcher mirrors the participant's iPhone via QuickTime if the participant consents and is on a Mac-compatible cable; otherwise records via an over-the-shoulder camera angle on the Mac webcam. Tasks run in randomised order per `task_protocol.md` §3. Stopwatch is the QuickTime timestamp.

4. **Hand-off and brief priming (30 sec).** Researcher says: *"This is Aura. It has read access to a test calendar, a test Gmail account, and the HealthKit data on this phone. It is not connected to any of your accounts. Do whatever feels natural — there are no wrong answers."* Phone is handed over.

5. **Prototype round on the demo iPhone (8 min).** Same 5 standardised tasks (`task_protocol.md` §2) in a fresh randomised order. Researcher is silent except for the verbatim start cues per `task_protocol.md` §4. Aura's in-app instrumentation also logs every tap, every action, every reasoning trace — exported at session end.

6. **Live diary (3 min).** Researcher reads each task name aloud; participant rates 1–5 satisfaction (5-point Likert per `quant_survey.md` Q11–Q15). Researcher writes the rating into the per-participant CSV (`raw_data_template.md`). Time-on-task is read off the QuickTime timestamps, no manual stopwatch needed.

7. **Willingness-to-pay + open feedback (5 min).** Verbally administer Van Westendorp 4 questions + the ₹199/month binary anchor (`quant_survey.md` Q23–Q27). Then: *"Anything else you want to tell us — good, bad, or weird?"* Recorded in the audio.

8. **Wrap (2 min).** Stop the QuickTime recording. Save MP4 to `pilot/raw/PNNN/`. Clear Aura's session memory on the demo phone via Settings → Pilot → Reset. Reload fixtures for the next participant. Thank the participant; offer to delete the recording immediately if they want; if yes, do it on the spot.

### 3.2 90-minute session for the n=8 qualitative cohort

After step 8 above, take a 5-minute break, then run the 60-minute qualitative interview per `qual_protocol.md`. The interview replaces Block 1's "daily diary review" with a "session walkthrough" of the just-completed Aura interaction (the participant has not had a 7-day diary; they have just had a 16-minute live experience). Blocks 2 and 3 of `qual_protocol.md` proceed as written. See `qual_protocol.md` §"Wizard-of-Oz adaptation" for the exact substitution.

---

## 4. Recording, transcription, storage

### 4.1 Recording

- **Format:** MP4 (QuickTime default), 1080p, ~120 MB per 30-minute session, ~360 MB per 90-minute session. Total raw video for 30 sessions ≈ 5 GB. Fits comfortably on the team Mac SSD.
- **Audio:** lavalier mic feed mixed into the MP4. Whisper-local transcribable.
- **Naming:** `pilot/raw/PNNN/PNNN_session.mp4`, `pilot/raw/PNNN/PNNN_field_notes.md`, `pilot/raw/PNNN/PNNN_aura_log.json`.

### 4.2 Transcription

- **Tool:** `whisper.cpp` running locally on the team Mac (free, on-device — keeps the on-device-only ADR-0005 posture for participant audio too).
- **Model:** `whisper-large-v3` (ggml quantised, ~3 GB).
- **Command:** `whisper-cli -m models/ggml-large-v3.bin -f PNNN_session.wav -otxt -ovtt`.
- **Output:** `PNNN_transcript.txt` and `PNNN_transcript.vtt` (with timestamps).
- **PII redaction pass:** transcript is run through a regex sweep that masks phone numbers, full email addresses, and any token matching the participant's first name (collected during consent, kept in a sealed file separate from the transcript folder). Researcher then does a manual second pass before any transcript is shared with the second coder.

### 4.3 Storage

See `pilot/data_handling.md` for full lifecycle, retention, and deletion policy. Summary: raw MP4 lives on the team Mac SSD only; redacted transcript is shared with the second coder via an encrypted-zip on a private GitHub repo branch; raw audio is deleted within 7 days of transcript completion.

---

## 5. Re-sign cadence

Personal Team certificates expire 7 days after issuance. The pilot fits in two 7-day windows. If a re-sign is missed, Aura on the demo phone refuses to launch — the next session cannot start.

The re-sign procedure is in `aura/scripts/resign_aura.sh`. Steps in plain English:

1. Connect Shaurya's iPhone to the team Mac with the Lightning cable.
2. Open Xcode 16.
3. Run `bash aura/scripts/resign_aura.sh`. The script:
   - Cleans the build folder.
   - Runs `xcodebuild -scheme Aura -configuration Release -destination "generic/platform=iOS" build`.
   - Runs `xcodebuild -exportArchive` with the Personal Team identifier configured at the top of the script.
   - Re-installs the resulting `.ipa` on the connected iPhone via `xcrun devicectl device install app`.
4. Open Aura on the iPhone, confirm the Trust dialog under Settings → General → VPN & Device Management → "Apple Development: <Apple ID>" → Trust.
5. Launch Aura, confirm HealthKit and EventKit permissions are still granted (they should be — the bundle ID has not changed).
6. Append a line to `pilot/raw/_resign_log.txt`: `2026-06-25T10:00 IST | cert fingerprint: SHA256:abc123… | next re-sign by: 2026-07-02T10:00 IST`.

Total time per re-sign: ~10 minutes. Done by Shaurya on Wednesday morning of each pilot week.

---

## 6. Total time budget

- 30 quantitative sessions × 30 min = 15 hours.
- 8 of those participants stay an additional 60 min for the qualitative interview = 8 additional hours.
- Re-sign × 4 events (start of week 8, day 4, start of week 9, day 4) × 10 min = 40 min.
- Fixture reload between participants × 30 × 5 min = 2.5 hours.
- **Total researcher time: ~26 hours over 14 calendar days.**
- Spread across two researchers and split between Patiala and Bangalore segments, this fits inside the Week 8 + Week 9 plan budget (`plan.md` §24).

---

## 7. Threats to validity, and how each is addressed

| Threat | What it is | Mitigation |
|---|---|---|
| **Novelty effect** | Participant's reaction to Aura is shaped by first-encounter excitement, not by sustained use. | (a) Reframe the n=30 number as "first-encounter task performance + WTP" in the Phase 2 report, do not claim it as a 7-day longitudinal result. (b) The n=8 qualitative cohort gets 7 days of HealthKit-XML-tracked HRV exposure to Aura's wellness loop *via observing their own Watch trends after the lab session* — they do not install Aura, but their HRV data still exists and can be compared pre/post the day Aura's wellness recommendations were demonstrated. |
| **Observer effect (Hawthorne)** | Participant performs differently because they know they are being watched. | (a) Researcher faces away during the prototype round; phone stand and silent timer keep the researcher out of the participant's eyeline. (b) Verbatim-only start cues (`task_protocol.md` §4); no encouragement, no prompts. (c) Baseline round runs first half the time (counterbalanced) so any "performance lift" from being watched applies to *both* rounds and does not bias the within-participant difference. |
| **Single-device latency variance** | All 30 participants share one iPhone. After 6 sessions in a row the device may thermally throttle, raising prototype-round task times artificially. | (a) Mandatory 5-minute cool-down with phone face-down on a metal surface between participants. (b) "Device temperature" field logged at session start (read from `iStat Menus` on the Mac via the developer console). (c) Maximum 6 sessions per day; 7th onwards moved to next day. (d) Sensitivity analysis at the end: if session-of-day correlates with prototype task time at *r* > 0.3, the analysis is rerun with session-of-day as a control variable. |
| **Researcher-as-developer bias** | Shaurya is both the developer and the lead researcher. He may unconsciously coach. | Already addressed in `task_protocol.md` §4 (no coaching, verbatim cues). For the Wizard-of-Oz protocol, add: Shorya runs at least 12 of the 30 sessions; the recordings are spot-checked by the other researcher for any deviation from script. |
| **Selection bias (iPhone owners only)** | The original ADR-0010 already had this; the lab study does not change it. The participant uses their own phone for the baseline round, which still requires they own a phone. | Disclosed in the Phase 2 report as in ADR-0010 §Consequences. |
| **Wizard intervention** | In a classical Wizard-of-Oz study the researcher "drives" the agent. We are *not* doing that — Aura is a real running build. The participant interacts with the actual agent. | This protocol is "Wizard-of-Oz" only in the sense that the *delivery and observation* are supervised. Aura itself is fully autonomous on the demo device. The trace logs and in-app instrumentation prove this and are committed alongside the recordings. We disclose the term and what we mean by it in the Phase 2 report's methods section. |

---

## 8. Dropouts and replacement

- **Recruit 35 to complete 30.** 5-participant buffer absorbs no-shows, last-minute cancellations, and any participant who withdraws mid-session.
- **Waitlist:** 5 standby names ranked by recruitment date. If a slot opens by 18:00 the previous evening, the next waitlist participant is contacted on WhatsApp and offered the slot.
- **Withdrawal mid-session:** participant can stop at any time per `pilot/CONSENT_v2.md`. If a withdrawal happens, log the timestamp, delete the partial recording on the spot if requested, and offer the slot to the next waitlist person within 24 hours.
- **Qualitative cohort:** recruit 10 names, expect 8 to complete the 90-minute session. If fewer than 8 complete, recruit additional names from the n=22 quant-only cohort who showed strongest engagement signals (defined as: completed all 5 prototype tasks, scored ≥4 on at least 3 satisfaction items).

---

## 9. What we do not change from ADR-0010

- Sample target: 30 quant + 8 qual.
- Five standardised tasks: identical to `task_protocol.md` §2.
- Survey items: identical to `quant_survey.md`.
- Coding scheme for qualitative: identical to `qual_protocol.md` §3 (5 themes, Cohen's κ ≥ 0.70 target).
- Statistical reporting: paired t-test / Wilcoxon, Cohen's d, Spearman ρ, exactly per `plan.md` §22.3.
- KPI targets: ≥30% effort reduction, ≥90% task completion, ≥85% AI autonomy, ≥4.5/5 satisfaction, ≥60% WTP at ₹199/mo, all per `plan.md` §22.

---

## 10. References

- Kelley, J. F. (1984). An iterative design methodology for user-friendly natural language office information applications. ACM Transactions on Office Information Systems, 2(1), 26–41.
- Maulsby, D., Greenberg, S., Mander, R. (1993). Prototyping an intelligent agent through Wizard of Oz. CHI '93 Proceedings, 277–284.
- Dahlbäck, N., Jönsson, A., Ahrenberg, L. (1993). Wizard of Oz studies — why and how. Proceedings of the 1st International Conference on Intelligent User Interfaces, 193–200.

End of Wizard-of-Oz protocol.
