# Aura Pilot — Lab Study Logistics

Practical operations for running 30 supervised lab sessions across two 7-day windows on Thapar Patiala campus and in Bangalore. Companion to `wizard_of_oz_protocol.md`.

Reference: ADR-0011 (no Apple Developer Program); `wizard_of_oz_protocol.md`; `plan.md` §24 (Week 8–9).
Last updated: 2026-05-07
Owner: Shaurya Punj

---

## 1. Locations

### Patiala (28 of 30 sessions)

**Primary venue: Thapar Library — Group Study Room G3 or G4.**

- Booked via the Library reservation portal at `library.thapar.edu/booking`. 90-minute slots (covers the 30-min quant-only session plus a 5-min reset; or a full 90-min qual session).
- Available weekdays 09:00–17:00; weekends 10:00–16:00.
- Has a power outlet, wide table, two chairs facing the same side. Acoustic-friendly walls.
- Booking made by Shorya (2nd-year so easier room access during teaching hours) one week ahead.

**Backup venue 1: Hostel G common room.**

- Weekday afternoons 14:00–17:00 when teaching is on (least crowded).
- Free, no booking, but quieter only when the cricket TV is off — confirm with the warden's chowkidar before each session.

**Backup venue 2: ECE Department project lab (Block C, 2nd floor).**

- If a faculty mentor is in place by Week 8 (`plan.md` §24 Week 1), they can sign for a 4-hour evening slot.

### Bangalore (2 of 30 sessions)

For the 2 Bangalore-based qualitative participants:

- **Default:** Cubbon Park's quiet zone near the Children's Library, weekend morning. Free, public, decent for a 90-minute session.
- **Backup:** Indiranagar Third Wave Coffee at 100 Ft Road, table near the back. ₹500 budget for two coffees and a snack each, drawn from the ₹2,000 total pilot budget.
- **Travel:** Shaurya travels to Bangalore for a 2-day visit during Week 8, batching both sessions.

---

## 2. Equipment checklist

The whole rig fits in one backpack.

| Item | Quantity | Owner | Notes |
|---|---|---|---|
| iPhone (demo device, Aura signed) | 1 | Shaurya | Charged to 100% before each session block; spare charger packed |
| Apple Watch (paired to Shaurya's iPhone) | 1 | Shaurya | For HRV-context demo only; not used in participant biometrics |
| AirPods Pro | 1 | Shaurya | For nudge demo if participant asks |
| MacBook (with Xcode 16) | 1 | Shaurya | For QuickTime mirror, transcription, fixture reset |
| Lightning-to-USB cable (1 m, MFi-certified) | 2 | Team | One in use, one spare |
| MagSafe charger (for iPhone between sessions) | 1 | Team | Cool-down charging |
| Lavalier mic (Boya BY-M1, ₹600) | 1 | Team | One-time purchase from total ₹2,000 budget |
| 3.5 mm to USB-C dongle (for Mac) | 1 | Team | If Mac has no 3.5 mm jack |
| Phone stand (cheap acrylic, ₹150) | 1 | Team | Keeps demo phone visible without researcher hand in frame |
| Printed CONSENT_v2.md (2 copies × 35) | 70 | Shorya | Printed at Thapar copy shop, ~₹2 per page |
| Pens | 4 | Team | Two black, two backup |
| Snacks (biscuits + chai sachets) | bulk | Team | Hospitality, not incentive — ₹200 budget |
| External SSD (for video backup) | 1 | Shaurya | Already owned; mirrors `pilot/raw/` nightly |

**Total new spend on equipment:** lavalier ₹600 + phone stand ₹150 + printing ₹140 + snacks ₹200 + Bangalore café ₹500 = **₹1,590**, leaves ₹410 contingency from the ₹2,000 cap.

---

## 3. Schedule template (Google Sheet)

Sheet name: `Aura Pilot — Lab Sessions Master`. One row per session.

| Column | Type | Example |
|---|---|---|
| `participant_id` | string | P012 |
| `cohort` | enum {quant_only, qual_extended} | quant_only |
| `name_first` | string (kept private, separate sheet) | — |
| `whatsapp_last4` | string | 4521 |
| `branch_year` | string | ECE-3 |
| `gender` | enum | F |
| `living` | enum {hostel, day, blr_home, blr_pg} | hostel |
| `slot_start_iso` | iso8601 | 2026-06-26T14:00+05:30 |
| `slot_end_iso` | iso8601 | 2026-06-26T14:30+05:30 |
| `venue` | enum {library_g3, library_g4, hostel_g, ece_lab, blr_cubbon, blr_thirdwave} | library_g3 |
| `researcher_lead` | enum {shaurya, shorya} | shaurya |
| `researcher_observer` | enum {shaurya, shorya, none} | shorya |
| `consent_signed` | bool | TRUE |
| `recording_path` | path | pilot/raw/P012/P012_session.mp4 |
| `status` | enum {scheduled, completed, no_show, withdrew, rescheduled} | completed |
| `notes` | string | "phone got warm by session 5; cool-down extended" |

The Google Sheet has **two tabs**: `master` (above) and `pii_lookup` (`participant_id` → first name + WhatsApp last 4 only — never committed to git). Access restricted to Shaurya and Shorya only.

### Daily session block template (8 sessions per researcher-day max)

```
09:30 — arrive, set up rig in G3, fixture reload
10:00 — P0XX session 1   (30 min)
10:35 — cool-down + fixture reset (5 min)
10:40 — P0XX session 2   (30 min)
11:15 — cool-down
11:20 — P0XX session 3   (30 min)
11:55 — chai break        (15 min, phone face-down on cool surface)
12:10 — P0XX session 4   (30 min)
12:45 — lunch + phone deep cool (60 min)
13:45 — P0XX session 5   (30 min)
14:20 — cool-down
14:25 — P0XX session 6   (30 min)
15:00 — wrap, transcription kicked off in background, daily backup to SSD
```

Hard cap: **6 sessions per researcher-day.** If a 7th is needed, it moves to the next day. This protects against thermal throttling and researcher fatigue.

---

## 4. Participant prep email / WhatsApp template

Sent 24–48 hours before the slot. WhatsApp preferred (the recruitment channel is Thapar Tech / Design club WhatsApp groups per ADR-0010); email used for Bangalore participants who are off the campus channels.

```
Hey [first name],

Confirming your Aura pilot slot:

Date: [day, date]
Time: [HH:MM IST]
Where: [venue + landmark]
How long: [30 min for quant-only / 90 min for the qual interview cohort]

A few quick things:

1. You don't need to install anything. We're running this on our phone, not yours.
2. You'll do the same five small tasks twice — once on your own phone with whatever you usually use, then once on our phone with Aura. We're comparing, not testing you.
3. We'll record the screen and audio. The consent form covers all of this; you can read it now or read it in the room. Both ways are fine.
4. Bring your own phone (charged), your usual messaging / calendar / payments app already logged in. We won't ask for any password.
5. There is no payment, no voucher. Your name goes in the public THANKS.md if you want, with your permission.

If something comes up, message me on this number any time and we'll reschedule. Showing up late is also fine — just tell me.

— Shaurya
```

For the n=8 qualitative cohort, append:

```
This is one of our long sessions — about 90 minutes total. The first 30 minutes are the same task session as everyone else; then we sit for ~60 minutes and just talk about what you noticed. Snacks on us.
```

For Bangalore participants, append:

```
We'll be in Bangalore on [date] and [date]. Cubbon Park near the Children's Library, or Third Wave on 100 Ft Road — your pick. Coffee on us.
```

---

## 5. Day-of checklist (researcher)

Print this. Keep it in the rig backpack.

- [ ] Demo iPhone: charged ≥ 90%, plugged into MagSafe at start of block
- [ ] Demo iPhone: Aura launches, login active, no certificate-expired dialog
- [ ] Demo iPhone: Settings → Pilot → "Reset session memory" tapped (confirm dialog)
- [ ] Demo iPhone: Test fixtures reloaded — 50 WhatsApp messages, calendar event, 7 transactions, 5 notifications (`task_protocol.md` §2)
- [ ] Mac: QuickTime open, "New Movie Recording" preset to iPhone-as-camera
- [ ] Mac: free disk space ≥ 5 GB
- [ ] Mac: `pilot/raw/PNNN/` directory created for the upcoming participant
- [ ] Lavalier mic: tested with a 5-second voice memo; clip on participant before slate
- [ ] Consent forms: 2 fresh blank copies printed and on the table
- [ ] Pen: working
- [ ] Water: bottle on the table
- [ ] Phone stand: positioned facing participant, not researcher
- [ ] Mac screen: angled away from participant's eyeline

---

## 6. Post-session checklist (researcher)

- [ ] QuickTime stopped, file saved as `PNNN_session.mp4` in `pilot/raw/PNNN/`
- [ ] Aura in-app instrumentation: Settings → Pilot → "Export pilot logs" → JSON saved as `PNNN_aura_log.json`
- [ ] Field notes: 5-line `PNNN_field_notes.md` written before the next participant arrives
- [ ] Aura: Settings → Pilot → "Reset session memory" + fixtures reloaded
- [ ] iPhone: face-down on cool surface for 5-minute cool-down
- [ ] Master sheet: `status = completed`, recording path filled, notes filled
- [ ] At end of day: external SSD plugged in, `pilot/raw/` rsync-ed to SSD
- [ ] At end of day: Whisper transcription kicked off overnight on the Mac

---

## 7. Risk register (logistics-specific)

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Library room booking lost on the day | Medium | Medium | Backup Hostel G common room confirmed in advance; ECE lab as second backup |
| Demo iPhone dies / damaged mid-window | Low | High | Spare iPhone (Shorya's) signed with the same Apple ID Personal Team cert as a hot spare; resign script supports both bundle IDs |
| Personal Team cert expires unexpectedly | Low | High | Re-sign log enforces a Wednesday-morning re-sign every week; 7-day timer is conservative |
| Participant no-show | High | Low | 35 recruited, 30 needed; waitlist of 5 ranked by recruitment date |
| Network drop during a Gmail-receipt task | Medium | Low | Test fixtures pre-loaded locally; if the live OAuth fetch fails, the cached fixture serves; flagged in field notes |
| Lavalier mic battery dies mid-session | Low | Low | Mac built-in mic as fallback; lavalier is replaceable in 24h via Croma Patiala |
| Fire alarm / library closure mid-block | Low | Medium | Reschedule to Hostel G; participants at most lose a 30-min slot |
| Bangalore travel cancellation | Low | Medium | Convert the 2 Bangalore qual sessions to Google Meet 60-minute interview only (no task session); flag the deviation in the Phase 2 report methods section |

---

## 8. End-of-pilot wrap-up

After the last session in Window B:

- [ ] All MP4s on team Mac SSD + external SSD backup
- [ ] All transcripts produced via `whisper.cpp` and PII-redacted
- [ ] All `PNNN_aura_log.json` files committed to `pilot/analysis/raw/` (anonymised)
- [ ] Master sheet exported as CSV (PII tab not included) and committed to `pilot/analysis/raw/sessions_master.csv`
- [ ] `_resign_log.txt` committed
- [ ] Raw audio (the .wav extracted from MP4 for Whisper input) deleted from disk per `data_handling.md`
- [ ] THANKS.md updated with consenting participant first names

End of logistics doc.
