# Aura Pilot — Qualitative Protocol

8 participants. 60-minute semi-structured interview after 7 days of TestFlight use. Plus a 90-second daily diary across the 7 days. Two coders, thematic analysis with Cohen's κ ≥ 0.7 inter-rater target.

Reference: `plan.md` §23.3, §22.
Last updated: 2026-05-07
Owner: Shaurya Punj (interviewer 1) + Shorya Gupta (interviewer 2 / second coder)

---

## 1. Participant pool

- 8 from the n=30 quant pool, drawn after Day 7 task sessions.
- Mix target: 4 ECE / CompE / CSE, 2 other Thapar branches, 2 Bangalore-based.
- Gender: 4 / 4.
- Hostel / day scholar: 5 / 3.
- Recruit alternates in case of dropouts (2 standby).

## 2. Interview format — 60 minutes total

Semi-structured. Recorded on Voice Memos on a separate iPhone (not the participant's). Transcribed by us within 48 hours, then audio deleted.

### 2.1 Block 1 — Daily diary review (15 min)

Participant has filled the daily diary (see §5) for 7 days. Walk through it together.

**Interviewer prompts:**
- "Read me your Day 1 entry out loud."
- "What was happening that day?"
- "Day 3 you wrote [X]. Tell me about that moment."
- "Was there a day Aura got it right? A day it got it wrong?"
- "Did the diary itself bug you, or did it feel fine?"

**What we are listening for:** week-shape, pattern of trust/distrust, moments of surprise, friction points.

### 2.2 Block 2 — Walkthrough of three Aura moments (30 min)

Ask the participant to recall **three specific moments** from the week when Aura did something they remember — good or bad.

For each moment, work through:
1. **Reconstruct.** "Where were you? What were you doing? What did Aura do?"
2. **Reaction.** "What did you feel in the second after?"
3. **Action.** "What did you do? Did you tap, ignore, swipe away?"
4. **Verdict.** "Looking back, was that the right call by Aura?"
5. **Counterfactual.** "If Aura had not done that, what would you have done instead?"

Use the participant's own phone. Open the **Reasoning Trace** drawer for the moment if they remember when. Let them read the trace out loud. Listen for whether the trace feels like an explanation or a defence.

**What we are listening for:** trust, surprise, friction, silence, value (the 5 themes — see §3).

### 2.3 Block 3 — Think-aloud on one task (15 min)

Pick one of the 5 standardised tasks (see `task_protocol.md`). Ask the participant to perform it on their phone using Aura, narrating every thought aloud.

**Interviewer prompts (only when stuck):**
- "What did you expect just now?"
- "What does this card tell you?"
- "Where would you tap?"

Do not help. Do not prompt for satisfaction. Just listen.

**What we are listening for:** mental model mismatches, friction in the UI, moments where the user predicted Aura's behaviour vs. moments of confusion.

---

## 3. Coding scheme

Five themes locked. Two coders code independently. Disagreements resolved in a third pass.

| Theme | Definition | Example utterance |
|---|---|---|
| **Trust** | Statements about whether the participant believes Aura is correct, fair, or honest. Includes loss of trust. | "I clicked the trace because I didn't believe it knew that." |
| **Surprise** | Statements where the participant expected one thing and got another. Both pleasant and unpleasant. | "Wait — it actually muted the group? I thought it would just show me the messages." |
| **Friction** | Statements describing extra work, confusion, or annoyance caused by Aura. | "I had to tap three times to dismiss that card." |
| **Silence** | Statements about Aura not doing something — either appreciated quiet or perceived absence. | "I didn't even notice it was running on Wednesday. That was nice." |
| **Value** | Statements about whether Aura saved time, attention, money, or mood. | "It caught the IRCTC mail before I did." |

### 3.1 Coding procedure

1. Both coders independently code the full transcript at the **utterance** level (one speaker turn = one or more codes).
2. Coding software: **Taguette** (open source) or a shared Google Sheet with one row per utterance.
3. Cohen's κ computed on the full coded set.
4. **Target: κ ≥ 0.70.** Below 0.6, both coders re-watch a sample, refine theme definitions, recode.
5. Themes are **not exclusive** — one utterance can carry up to two codes.
6. Disagreements arbitrated by a third pass with both coders sitting together.

See `analysis/notebooks/04_autonomy_quality.ipynb` for the κ computation pattern (same statistic, different rater task).

### 3.2 Output

- Per-theme frequency table.
- Top 3 quotes per theme (with participant ID, never name).
- Cross-tab: theme × participant — who experienced which theme.
- Three named "moments" per participant carried forward into Phase 2 report (`reporting/phase2_report_outline.md` §5).

---

## 4. Inter-rater reliability — Cohen's κ target

- **Target**: κ ≥ 0.70 across all five themes.
- **Acceptable floor**: κ ≥ 0.60 with documented disagreement notes.
- **Below 0.60**: theme definitions are not crisp. Refine and recode.
- Reported in Phase 2 deliverable as: "Two independent coders coded N utterances across 8 transcripts. Cohen's κ = X.XX [Y.YY, Z.ZZ] across 5 themes."

---

## 5. Daily diary template

Sent at 21:30 IST every day for 7 days via WhatsApp (link to a 3-question Google Form). Target completion: 90 seconds. Optional skip for any day.

### Question 1 — open
> In one sentence, what did Aura do today that mattered, or fail to do that mattered?

### Question 2 — Likert 1–5
> How stressful was today, on a scale where 1 = a calm day and 5 = a hard day?

> 1. Calm — nothing pressed on me
> 2. Mostly calm
> 3. Average
> 4. Mostly stressful
> 5. Hard — I was overloaded

### Question 3 — open (skippable)
> Anything you would change about Aura today? One sentence is fine. Skip if nothing.

---

### Diary delivery

- Sent 21:30 IST. Reminder at 22:30 if not filled.
- No reminders after 22:30. We are not nagging.
- Stored anonymised under participant ID `P001`–`P030` (qual subset uses same IDs).

### Diary use in Block 1

The 7 diary entries become the timeline the interviewer walks through in Block 1. They are the participant's own words about their week.

---

## 6. Logistics

- Interviews held in the Thapar Library group-study room (booked) or over Google Meet for Bangalore participants.
- Recording on Voice Memos on a researcher iPhone, not the participant's.
- Researcher dress: normal. No "professional".
- Snacks provided (chai + biscuits) — this is hospitality, not incentive.
- Each interview ends with: "Want me to delete the recording right now?" — and we do, if asked.

---

## 7. Ethical guardrails

- Pause and re-confirm consent at the start of every interview. The consent form (`pilot/consent_form.md`) is on the table.
- Skip any question the participant prefers not to answer.
- Stop the recording any time the participant asks. Resume only with verbal yes.
- Quotes used in the Phase 2 report are sent to the participant for approval before submission.
- Audio deleted within 7 days of transcript completion.

---

## 8. Wizard-of-Oz adaptation

Added 2026-05-07 following ADR-0011. Replaces the "after 7 days of TestFlight use" assumption that ran throughout §1–§7 above. The locked context: the team will not buy an Apple Developer Program membership, so there is no TestFlight build, so participants do not have a 7-day field exposure and do not produce a 7-day daily diary. The qualitative interview is now folded into the same in-person session as the 30-minute task block on a team-owned iPhone (`pilot/wizard_of_oz_protocol.md`).

### 8.1 What changes from §1–§7

- **Sample stays 8.** Same 4 ECE/CompE/CSE + 2 other Thapar branches + 2 Bangalore mix as §1.
- **Session length: 90 minutes total.** First 30 minutes is the standard quant lab session (`wizard_of_oz_protocol.md` §3.1 steps 1–8). Then a 5-minute break. Then the 60-minute interview below.
- **No 7-day diary.** The diary block (§5 above) is dropped — there is no 7-day exposure to diary against. The diary text in §5 remains in the document for the audit trail and for any post-Phase-2 longitudinal study, but it is **not collected** during the Wizard-of-Oz pilot.
- **Recording continues from the quant block.** The QuickTime mirror + lavalier mic that ran during the 30-minute task session keeps running through the 60-minute interview. One MP4 per participant covers both halves.

### 8.2 Block restructure for the 60-minute interview portion

| Block | Original (§2) | Wizard-of-Oz adaptation |
|---|---|---|
| **Block 1** — was "Daily diary review" (15 min) | Walk through the 7 diary entries | **Replaced** by "Session walkthrough" — walk through the 16 minutes the participant just spent on the 5 baseline tasks + 5 Aura tasks. Rewind the QuickTime recording on the Mac to specific moments the participant flagged. Use the recording as the timeline that the diary used to be. |
| **Block 2** — Walkthrough of three Aura moments (30 min) | Recall three moments from the week | **Adapted** — recall three moments from the just-completed Aura task round. The recording is on the Mac; if the participant cannot remember a specific moment, scrub the video to the timestamp from the in-app instrumentation log and watch it together. Same five-step probe per moment (reconstruct, reaction, action, verdict, counterfactual). |
| **Block 3** — Think-aloud on one task (15 min) | Repeat one of the 5 tasks on the participant's own phone with Aura installed | **Adapted** — repeat one of the 5 prototype tasks on the demo iPhone, narrating aloud. The participant has just used Aura for ~8 minutes, so this is a second-encounter think-aloud, not a fresh-encounter one. Mental-model formation is the lens. |

### 8.3 Block-1 prompt set, replacing §2.1

- "Take me back to the moment we handed you our phone. What were you expecting?"
- "Which of the five tasks felt most like Aura was actually being useful?"
- "Which felt most like Aura was getting in the way?"
- "Was there a moment you remember as 'wait, what?' — surprise either way?"
- "If we asked you to do these five tasks again tomorrow on this phone, what do you think would feel different?"

### 8.4 What we lose, and what we gain, vs. the original

| Lose | Gain |
|---|---|
| 7-day exposure depth — habits, novelty wearing off, week-shape | Direct observation of mental-model formation in the moment |
| Diary as memory anchor for the interview | Live screen recording as memory anchor — replayable, time-stamped |
| Day-to-day variance in stress, sleep, contextual triggers | All 8 participants experience identical fixtures, removing context noise as a confound |
| Generalisability claim about a week of real use | Deeper internal validity per participant; explicit small-n claim in the report |

The trade is consistent with the Wizard-of-Oz norm at n ≤ 50 (Maulsby 1993, Dahlbäck 1993). The Phase 2 report frames the qualitative findings as **first-encounter mental-model and reaction data**, not as a longitudinal week-of-use claim. The HRV pre/post 7-day comparison for the same 8 participants is preserved separately — they export their own Apple Watch HealthKit XML (CONSENT_v2 §12 sub-cohort tickbox) for the 7 days surrounding their session, giving the n=8 longitudinal HRV number per `plan.md` §22.

### 8.5 Coding scheme — unchanged

Five themes (Trust, Surprise, Friction, Silence, Value) and the Cohen's κ ≥ 0.70 target stay exactly as in §3. The utterance-level coding is applied to the redacted transcript of the 60-minute interview portion of the MP4 — produced via `whisper.cpp` and the redaction pass per `data_handling.md` §4.

### 8.6 Logistics, replacing §6

- 90-minute slot booked in Thapar Library group-study room G3 / G4 (or Bangalore equivalent per `lab_study_logistics.md` §1).
- Same QuickTime + lavalier rig as the quant session — no second recorder needed.
- Snacks (chai + biscuits) on the table from the start; participants typically need them more in the second half.
- The "want me to delete the recording right now?" close is offered at the 90-minute wrap, same as the original §6.

---

End of qualitative protocol.
