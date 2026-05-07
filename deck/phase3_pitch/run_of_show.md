# Aura — Phase 3 Finals Run-of-Show

**Slot:** 7-minute pitch + 3-minute Q&A. Hard cap: 7:10 + 3:10.

**Presenters:** Shaurya (lead, on mic, drives phone). Shorya (co-pilot,
drives Mac and slide deck, fires demo cues, reads Reasoning Trace JSON
on cue).

**Stage layout.**
- Center stage, left of phone mirror: Shaurya.
- Stage right, behind a small lectern: Shorya with Mac, deck remote,
  storm-trigger keyboard.
- Phone mirror: USB-C → projector via QuickTime, 1920×1080.
- Apple Watch on Shaurya's wrist, paired and reading HRV by T-5 min.
- AirPods routed to stage PA via aux out, env `BT_FORCE_AURA=1`.

---

## Pitch — 7:00 minute table

| Time | Slide | Phone state | Shaurya (lead) | Shorya (co-pilot) | Cue word |
| ---- | ----- | ----------- | -------------- | ----------------- | -------- |
| 0:00-0:20 | 1 | Lock screen, 248 notifs visible | (verbatim opening line — see below) | Hold. No movement. | (none — Shaurya leads in) |
| 0:20-1:00 | 2 | Lock screen | "Two thirty seven a day. Four matter. Eleven forty eight on a Tuesday — DBMS due at nine, project group fired one thirty seven messages, HRV at twenty eight. The brief asks for AI that anticipates, integrates personal data, reduces cognitive load." | Advance to slide 2 on "Two thirty seven". | "Two thirty seven" |
| 1:00-1:30 | 3 | Lock screen | "Every action has a why. Every why has a trace. The user reads it. Owns it. We open the drawer twice today." | Advance to slide 3 on "Every action". | "Every action" |
| 1:30-2:15 | 4 | Lock screen | "Sense from HRV, SMS, calendar, notifications. Decide via Phi-3-mini orchestrator. Surface to phone, watch, earbud. Median tick under three hundred milliseconds. On the device. Forever." | Advance to slide 4 on "Sense". | "Sense" |
| 2:15-2:55 | 5 | Lock screen | "Five wedges. Glass-box trace. Exportable memory. Silence Budget. Biometric loop. Indian context. No incumbent ships all five. None will, structurally." | Advance to slide 5 on "Five wedges". | "Five wedges" |
| **2:55-3:55** | **6 (LIVE A)** | Phone unlock — Aura home — Morning Brief animates | "Live. The morning, on the day this video says it is. Sleep five point two from HealthKit. Quiz at nine, slides summarised. BMTC ETA, leave eight fifteen. One refund. I did not ask for any of this." (tap accept) | **Advance to slide 6 on "the day this video says it is". Hold on phone mirror.** Time-keep: prompt "Group chat next" if Shaurya is at 3:50. | "the day this video says it is" |
| 3:55-4:35 | 7 | Phone shows Load Score climbing; Watch HRV down | "Closed loop. RMSSD from HealthKit. Typing entropy. Five features, one Load Score. At seventy eight, Wellness proposes mute. Trace logged. One tap." (tap accept) | Advance to slide 7 on "Closed loop". Stand by to hand AirPods if pairing drops. | "Closed loop" |
| **4:35-5:15** | **8 (LIVE B)** | Synthetic UPI debit SMS injected | "Forty rupee Zomato, third this week. Anomaly. Projection on the device — balance hits zero eleven May. Open the trace. Two opens, as promised." (tap drawer) | **Fire SMS injection on cue. Advance to slide 8 on "Forty rupee Zomato".** Read trace JSON aloud only if gestured. | "Forty rupee Zomato" |
| 5:15-5:45 | 9 | Memory tab open | "Exportable. One tap, JSON in Files. Time-range delete. Audit log. We do not have your data on a server because there is no server." (tap export) | Advance to slide 9 on "Exportable". | "Exportable" |
| 5:45-6:15 | 10 | Slide on projector | "The numbers we measured. Thirty per cent effort reduction. Two ninety seven median tick. Six eighty p95. Raw CSV in the repo. Anyone here can re-run tonight." | Advance to slide 10 on "The numbers". | "The numbers" |
| 6:15-6:35 | 11 | Slide on projector | "Phase 2 — Galaxy S prototype with Health Connect. Phase 3 — Galaxy Store beta in India Q4. Q2 2027 — OneUI integration via Galaxy AI partner program." | Advance to slide 11 on "Phase 2". | "Phase 2" |
| 6:35-6:50 | 12 | Slide on projector | "Three risks. Apple-only build. Pilot N is thirty — small. License watch on Phi-3-mini. We name them." | Advance to slide 12 on "Three risks". | "Three risks" |
| 6:50-7:00 | 13 | Slide on projector | "What we need from this room. Health Connect SDK access. Knox vault enrolment. Galaxy AI integration channel. Ready Monday." | Advance to slide 13 on "What we need". | "What we need" |
| 7:00 (close) | 14 | Aura idle | "Galaxy Brain. The only assistant that earns trust by showing why and shutting up. Thank you." | Advance to slide 14 on "Galaxy Brain". | "Galaxy Brain" |

### Locked opening line — verbatim, said exactly once

> "Aura is platform-agnostic. We built the reference on iPhone because
> that's the device our college owned, and a two-thousand-rupee total
> budget didn't stretch to a flagship phone. The architecture you see
> ports to Galaxy via the API table on slide 4. We never claim numbers
> we did not measure. Now let me show you what we did measure."

This is the **first** thing said. Never skipped, never reworded.

### Locked closing line — verbatim, said exactly once

> "Galaxy Brain. The only assistant that earns trust by showing why and
> shutting up. Thank you."

---

## Q&A — 3:00 minutes

Two presenters split the bank. Shaurya answers Q1-Q15 + Q31-Q40 (engineer
+ design + ventures). Shorya answers Q16-Q30 + Q41-Q50 (Bixby PM + exec
+ regulatory + customer-success).

| Time      | Move                                                                                  |
| --------- | ------------------------------------------------------------------------------------- |
| 0:00-0:30 | First question. Whoever is in domain answers. Cap at 30 s.                            |
| 0:30-1:30 | Two more questions, alternating presenters. Cap at 30 s each.                         |
| 1:30-2:30 | Two more questions. If a question is hostile, do not duck — pull `qa_bank_extended.md` answer verbatim. |
| 2:30-3:00 | Final question. Close on the wedge sentence: "Aura is the only assistant that earns trust by showing why and shutting up." |

If a judge asks something not in the 50-question bank, default to: "We
do not know yet. We will email you a written answer by Friday." Honest
beats clever every time.

---

## Failure modes and live recoveries

| Failure                                  | Inside 30 s? | Action                                                                   |
| ---------------------------------------- | ------------ | ------------------------------------------------------------------------ |
| iPhone locks during a long pause         | yes          | Shaurya unlocks via Face ID without breaking sentence; Shorya holds.     |
| WhatsApp storm trigger fails             | yes          | Shorya hot-key `Cmd+Shift+1` to re-fire local notification queue.        |
| Bluetooth whisper drops                  | no           | Shaurya reads the whisper line aloud; phrased as the model would say it. |
| Phone battery dies                       | no           | Switch to backup video (`demo/video_90s_storyboard.md`).                 |
| Projector aspect ratio wrong             | no           | Skip slide deck, deliver entirely on phone mirror; Shorya holds Mac.     |
| Live demo fails inside the first 30 s    | yes          | Shaurya: "Live demo just refused to play. We have a 90-second cut — let me show you that instead." Shorya cues the video. |
| Q&A judge asks for source code           | n/a          | Shorya hands over a pre-printed QR card linking to the public repo.      |

---

## Pre-stage checklist (T-30 minutes)

- [ ] iPhone fully charged (≥ 80%), Low Power Mode OFF, DND OFF.
- [ ] Aura test build installed, signed-in, all permissions granted.
- [ ] WhatsApp test group `Thapar-DSA-Project` populated with 47
      pre-loaded messages, ready to fire.
- [ ] Synthetic UPI SMS injection test run on the iPhone via dev menu.
- [ ] Apple Watch on Shaurya's wrist, HRV captured 5 min before stage.
- [ ] AirPods paired to iPhone and to stage PA mixer (aux out).
- [ ] Mac with deck open at slide 1, slide 4, slide 5, slide 10 cached.
- [ ] Backup video `90s_aura_demo.mp4` open in QuickTime, paused at
      frame 1, fullscreen-ready on `Cmd+F`.
- [ ] USB-C → HDMI dongle tested in this exact projector port.
- [ ] Run the dress rehearsal one final time — see
      `demo/dress_rehearsal_checklist.md`.
- [ ] Print 2 copies of `qa_bank_extended.md`, one per presenter.
