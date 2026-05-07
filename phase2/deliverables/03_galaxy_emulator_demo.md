# Phase 2 Galaxy Emulator Port — Demo Specification — TEMPLATE

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Per `plan.md` §21.1 ("Galaxy port via Android emulator; Apple device
for live biometric loop") and §34.1 (Phase 2 Android emulator port
of Comms + Wellness verified; screen-record produced for Phase 2
deliverable).

The team owns no Galaxy hardware (`plan.md` §0 budget lock = ₹2,000;
no purchase, no borrow). The Phase 2 Galaxy demonstration runs on
Android Studio AVD images (Pixel + Galaxy) on the team's Mac.
Honest framing line is non-negotiable.

---

## 1. Honest framing line — locked

This line ships verbatim in the deliverable description, the demo
video subtitles, and the README of the screen-record:

> "Galaxy port via Android emulator; Apple device for live biometric
> loop. We never claim a kernel hook we did not measure on the
> hardware that owns it."

This line carries `plan.md` §21.3 directly into the deliverable.

---

## 2. Emulator stack

| Component | Version |
|---|---|
| Android Studio | Koala (or successor in May 2026) |
| AVD image — Pixel | Pixel 8, Android 14, Google APIs |
| AVD image — Galaxy | Samsung Galaxy S24 system image (community AOSP fork) — installed via Android Studio Tools > SDK Manager > System Images. Where Samsung does not publish a public AVD, the Pixel image with One UI skin override is used and labelled "Galaxy-class AVD" — never labelled as a Samsung kernel. |
| RAM allocated per AVD | 4 GB |
| Storage allocated per AVD | 8 GB |

---

## 3. Agents ported for the screen-record

Per `plan.md` §34.1 Phase 2 priority: **Comms + Wellness** ported
first.

| Agent | Source path (Python ref) | Port path (Android) | Status |
|---|---|---|---|
| CommsAgent | `agents/comms/agent.py` | `apps/android/app/src/main/java/com/aura/agents/CommsAgent.kt` | [REPLACE WITH MEASURED VALUE] |
| WellnessAgent | `agents/wellness/agent.py` | `apps/android/app/src/main/java/com/aura/agents/WellnessAgent.kt` | [REPLACE WITH MEASURED VALUE] |

CalendarAgent and FinanceAgent ports are deferred to a Phase 2 stretch
goal; the deliverable explicitly names them as not yet ported.

---

## 4. Health Connect mock fixtures

Phase 2 Wellness Agent reads Health Connect on Android. The team
ships mock fixtures that mirror the iOS HealthKit fixtures already
under `agents/wellness/fixtures/`.

| Mock fixture | Source | Notes |
|---|---|---|
| `apps/android/app/src/main/assets/health_connect/hrv_5days.json` | derived from `agents/wellness/fixtures/hrv_5days.csv` | Five-day HRV stream |
| `apps/android/app/src/main/assets/health_connect/sleep.json` | derived from `agents/wellness/fixtures/sleep.csv` | 7-day sleep |
| `apps/android/app/src/main/assets/health_connect/typing_entropy.json` | derived from `agents/wellness/fixtures/typing_entropy.csv` | Per-minute entropy |
| `apps/android/app/src/main/assets/health_connect/app_switch.json` | derived from `agents/wellness/fixtures/app_switch.csv` | Per-minute app-switch rate |

All four are committed to the repo as static asset bundles. The
emulator wires them via a `MockHealthConnectClient` that conforms to
the Health Connect read API surface but reads from local JSON.
This is documented on the screen-record subtitle as "Health Connect
mocked from iOS fixtures — same algorithm, mocked I/O."

---

## 5. 90-second screen-record — shot list

Target file: `aura/phase2/deliverables/galaxy_emulator_demo_90s.mp4`
(produced once the port is complete; gitignored, attached to GitHub
Release).

| Time | Shot | Voiceover (read-only; not on screen) |
|---|---|---|
| 0:00–0:08 | Cold open: Mac desktop, Android Studio open, Pixel + Galaxy-class AVDs visible side-by-side | "Aura runs on Android. Two emulators side-by-side, both stock AOSP." |
| 0:08–0:18 | Click Pixel AVD; Aura app launcher icon visible; tap to launch | "First, Pixel. The reference build we ship to TestFlight ports here in roughly four hundred lines of Kotlin." |
| 0:18–0:35 | Comms agent demo: trigger 47-message storm via `adb shell am broadcast`; Aura batches; one card with 3 actionable items, 44 muted | "Forty-seven messages in eight minutes. Aura keeps three. The other forty-four are silent." |
| 0:35–0:55 | Open Reasoning Trace drawer; show typed JSON ranking; user inspects rationale | "Glass-box. The trace is the wedge." |
| 0:55–1:15 | Switch to Galaxy-class AVD; same Aura APK; show Wellness Agent reading mocked Health Connect HRV stream; Load Score climbs to 78; mute-group suggestion fires | "Same APK on a Galaxy-class image. Health Connect is mocked because we own no Galaxy device. Algorithm is the same; the substrate is the only swap." |
| 1:15–1:25 | Tap accept; group muted; Reasoning Trace logs the action | "One tap. Trace logged." |
| 1:25–1:30 | End-card: "Aura — Anticipate. Act. Stay quiet." plus QR to GitHub repo | (silent) |

Total: 90 seconds.

Filename convention: `galaxy_emulator_demo_v{N}_{date}.mp4`.

---

## 6. Production checklist

- [ ] `apps/android/` directory created and committed
- [ ] CommsAgent ported and unit tests passing (`./gradlew :app:test`)
- [ ] WellnessAgent ported and unit tests passing
- [ ] Mock Health Connect client with all four fixtures wired
- [ ] Reasoning Trace UI ported (Compose)
- [ ] Aura APK builds for both AVDs from a single source (`./gradlew assembleDebug`)
- [ ] 90-second screen-record produced via QuickTime + AVD double-window
- [ ] Subtitles burned in carrying the §1 honest framing line
- [ ] Video uploaded to GitHub Release tagged `phase2-emulator-demo-v1`
- [ ] README on this file updated with the public release URL

---

## 7. Sign-off

| Role | Name | Date |
|---|---|---|
| Android port owner | Shorya Gupta | [REPLACE WITH MEASURED VALUE] |
| Mock fixtures owner | Shaurya Punj | [REPLACE WITH MEASURED VALUE] |
| Recording / editing | Shorya Gupta | [REPLACE WITH MEASURED VALUE] |

— end of 03_galaxy_emulator_demo.md —
