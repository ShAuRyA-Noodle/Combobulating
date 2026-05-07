# Phase 3 Contingency Kit

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Per `plan.md` §27 (R15 Demo failure on stage, R16 Power loss / no
internet at venue) and §33 (Failure mode 10 — Demo failure on stage,
mitigation: pre-recorded backup video, full offline mode, three dry
runs).

This file is the on-stage emergency procedure. Read it the night
before. Read it again the morning of. Both founders memorise the
top three responses.

---

## Scenario 1 — Disqualified before or during the event

Possible reasons: missing documentation, late arrival, registration
issue, ambiguous eligibility.

| Sub-scenario | Response |
|---|---|
| Disqualified at registration desk | Stay calm. Ask for the specific rule that triggered the call. Ask whether a senior coordinator can review. Show printed EnnovateX badge confirmation + train tickets + photo ID. If the call is final, do not argue — leave the desk, find a seat in the audience. |
| Disqualified mid-pitch | Walk off stage, do not protest live. Note the time and the announcement verbatim. Email EnnovateX organisers within 24 h asking for the written reason. |
| Disqualified post-event | Request a written reason via email. Do not post on social media until the written reason arrives. |

In all cases: the work is the work. The repo, the deck, the audit
report, the threat model — those are public artefacts that survive
the event regardless. EnnovateX is one stage; Aura is a project.

---

## Scenario 2 — Wi-Fi fails at the venue

Aura is **on-device by design** (per `plan.md` §0 + §4.5 + §10).
This is the easiest contingency.

| Pre-stage check | Action |
|---|---|
| 1 | Confirm iPhone Mobile Data is ON, Wi-Fi is OFF, before the demo starts. Aura does not need Wi-Fi for any demo step. |
| 2 | Mac connected to projector via HDMI (cable, not AirPlay). AirPlay needs Wi-Fi. |
| 3 | Demo video on Mac local disk, not on iCloud streaming. |
| 4 | If GitHub QR ask comes up live, the QR points to a static GitHub URL — judges scan after the demo. |

**On-stage line if asked:** "Aura runs entirely on-device. The demo
you are about to see does not need internet. That is the privacy
posture made real."

---

## Scenario 3 — iPhone crashes mid-demo

Phone unlock fails, app freezes, screen mirroring drops, watch
disconnects — any of these.

| Step | Action |
|---|---|
| 1 | Pause for 2 seconds. Smile. Say "Let me grab the backup." |
| 2 | Switch the projector input to Mac. The 90-second backup video is open in QuickTime, ready to play. |
| 3 | Play the backup video. Narrate over it as if it were live — the script is the same. |
| 4 | If the video also fails (extremely rare): shift to **deck-only walk-through** of slides 3, 4, 4a, 9. The bench rehearsal of the deck-only fallback is mandatory at home. |
| 5 | Do not apologise repeatedly. Acknowledge once: "Tech happens. The architecture is the same in either case." Move on. |

---

## Scenario 4 — Presenter freezes

Stage fright, mind blanks, voice cracks. It happens.

| Sub-scenario | Response |
|---|---|
| Shaurya freezes | Shorya picks up at the next slide transition. The handover line is rehearsed: "Let me hand off to Shorya for the technical detail." |
| Shorya freezes | Shaurya picks up. The handover line: "On the implementation side — I'll cover this." |
| Both freeze | Pause. One sip of water from the bottle (kept on the lectern). Restart from the locked Phase 3 opening line per `phase3/README.md`. The locked line is muscle-memory by stage day. |
| Voice cracks | Throat lozenge from the inside-blazer pocket. 2 seconds is fine. |

Rule: **never apologise more than once on stage**. One quick
acknowledgement, then move on. Judges respect recovery, not
self-flagellation.

---

## Scenario 5 — Watch / AirPods disconnect

| Sub-scenario | Response |
|---|---|
| Watch loses pairing | Skip the Watch glance beat. The demo flow holds without it; Aura still surfaces on the phone. |
| AirPods drop out | Skip the earbud whisper beat. Read the line aloud yourself: "Aura whispers: 'Mute project group 30 minutes? You're in flow.' One tap." |
| Both gone | Combine: "Aura's surface set is phone + watch + buds. The watch is not paired right now — let me show you on the phone, the same surface." |

---

## Scenario 6 — Projector incompatibility

Mac → projector handshake fails. HDMI works on test, fails live.

| Step | Action |
|---|---|
| 1 | Try the Lightning → HDMI adapter directly from iPhone. Aura demo works from phone alone. |
| 2 | If iPhone direct mirroring also fails, use the venue laptop. The Phase 3 deck PDF is on the USB-A flash drive. |
| 3 | If venue laptop is locked / non-functional, present **without slides**, one-screen demo on iPhone held up to camera. Speak the deck. |
| 4 | Worst case: hand the leave-behind sheets to the front row and walk through them verbally. The sheet is designed to be load-bearing. |

---

## Scenario 7 — Q&A goes off-rails

A hostile or irrelevant question, or a panel member who keeps
talking over the founder.

| Sub-scenario | Response |
|---|---|
| Hostile question (e.g., "Why didn't you build on Galaxy?") | Use the locked Phase 3 opening line as the answer. It was written for exactly this. Do not improvise. |
| Out-of-scope question (e.g., "How would this scale to 100 million users?") | "We have measured 30 users. Scale design is in `docs/architecture.md`. Happy to walk through it after the session." |
| Panel-member talks over the founder | Wait. Smile. Resume from the last unfinished sentence the moment they stop. Do not interrupt. |
| "Can you show us X right now?" (something not in the demo) | "Yes, after the session at the booth — the architecture supports it. The 5-minute window covers our highest-confidence beats." |

---

## Scenario 8 — Travel disruption

Train cancelled, flight delayed, BMTC strike on event morning.

| Sub-scenario | Response |
|---|---|
| Train cancelled at New Delhi | Switch to flight (SpiceJet / IndiGo, ₹4,500–₹7,500). Phase 3 budget has buffer. |
| Train late but moving | Both founders work on the train. Final dry run at hostel on arrival. |
| BMTC strike on event morning | Uber / auto. Leave 2 hours earlier than planned. Bangalore traffic on a strike day is ruthless. |

---

## Pre-stage final check (10 min before)

- [ ] iPhone unlocked, Aura app open at Morning Brief screen
- [ ] Watch paired, vibration test confirmed
- [ ] AirPods in case, charged, paired
- [ ] Mac on Phase 3 deck slide 1, demo video pre-loaded in second window
- [ ] HDMI cable connected, projector showing Mac mirror
- [ ] Lavalier mic clipped, sound check confirmed
- [ ] Both presenters know who opens, who hands off where, who closes
- [ ] Locked Phase 3 opening line rehearsed once, silently, by Shaurya
- [ ] Bottle of water on the lectern
- [ ] Backup video confirmed on Mac, on iPhone, on USB drive

Everything else is bonus.

— end of contingency_kit.md —
