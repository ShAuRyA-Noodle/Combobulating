# Phase 2 Threat Model Penetration Audit — Checklist — TEMPLATE

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Per `plan.md` §20 (Privacy and Security Threat Model) and the five
adversaries named in `aura/docs/threat_model.md`. This file is the
penetration-audit checklist Phase 2 runs against the prototype
before submission. Every adversary is exercised; every row gets a
PASS / FAIL.

Auditor (recommended): one team member runs the attack, the other
records pass / fail blind, then they swap. Where blind testing is
not possible, the failure-mode artefacts are recorded by hash for
post-hoc verification.

---

## 1. Adversary 1 — Curious app on the device

Threat: a separate installed app tries to read Aura's memory graph
(SQLite database file).

| # | Attack | Expected outcome | Measured | Pass / Fail |
|---|---|---|---|---|
| 1.1 | App without `READ_EXTERNAL_STORAGE` attempts to open `aura.db` | Permission denied | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 1.2 | App with full storage permission attempts to read `aura.db` rows directly | File present but content unreadable (SQLCipher / Keystore-derived key) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 1.3 | App with full storage attempts to read the audit log file | Tamper-evident header rejects external read | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 1.4 | Accessibility-service-class app attempts to scrape Aura's UI | Aura denies screen-record / accessibility scrape on its own activity (Android `setSecure(true)`) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 2. Adversary 2 — Lost or stolen device

Threat: device picked up by an unauthorised party with screen lock
broken or shoulder-surfed.

| # | Attack | Expected outcome | Measured | Pass / Fail |
|---|---|---|---|---|
| 2.1 | Device booted, Aura app opened without biometric on lock | Aura app re-prompts biometric on cold start | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 2.2 | Memory graph file copied off-device via USB / cable transfer | Copied file is encrypted; no plaintext recoverable | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 2.3 | Audit log shows the cold-boot read attempt timestamped | Audit log contains the read event | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 2.4 | Panic-wipe gesture (5-tap power) wipes Aura memory + revokes Gmail / Calendar OAuth | Memory zeroed, OAuth tokens revoked, app placed in pristine first-launch state | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 3. Adversary 3 — Malicious notification or accessibility app

Threat: a competing app sets itself up as a NotificationListenerService
or AccessibilityService and tries to read what Aura reads.

| # | Attack | Expected outcome | Measured | Pass / Fail |
|---|---|---|---|---|
| 3.1 | Hostile NotificationListenerService running alongside Aura | Both apps see notifications independently; Aura's processed output is not exposed to the hostile app | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 3.2 | Hostile app calls Aura's content provider (none should be exported) | All Aura content providers are `android:exported="false"` and reject cross-app calls | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 3.3 | Hostile app attempts to read Aura's IPC service | Aura's services are signature-restricted | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 3.4 | Hostile app intercepts pasteboard during Aura draft-reply step | Aura uses platform sensitive-clipboard API on Android 13+; iOS uses local-only TextField | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 4. Adversary 4 — Cloud account compromise (Google or Apple)

Threat: the user's Google account password or Apple ID has been
phished. We ship no cloud sync of Aura data, but the OAuth scopes
Aura requested are now in attacker hands.

| # | Attack | Expected outcome | Measured | Pass / Fail |
|---|---|---|---|---|
| 4.1 | Attacker logs into Gmail; reviews Aura's OAuth scopes | Aura's scopes are visible and revocable; Aura asks for `gmail.readonly` + `gmail.metadata` only, never write | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 4.2 | Attacker revokes Aura's Gmail scope | Aura on the device receives 401 next read; surfaces a permission-revoked card; does not silently retry | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 4.3 | Attacker uses Calendar scope to delete events | Aura cannot prevent this (no defence on the cloud side); but Aura's local memory graph still holds the prior structured events for user reference | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 4.4 | Attacker reads sent / drafted Aura messages | Aura never writes drafts to Gmail Outbox unless the user taps Confirm; stored draft cache is local-only and encrypted at rest | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 5. Adversary 5 — Coercion (parent / partner forcing unlock)

Threat: a coercive party physically unlocks the device and demands
Aura content disclosure. This is a duress, not a remote-attack,
threat.

| # | Attack | Expected outcome | Measured | Pass / Fail |
|---|---|---|---|---|
| 5.1 | Coercive party opens Aura, demands the user show "all messages" | Aura never stores raw message bodies past the rolling reasoning window (`plan.md` §4.5); only structured intent labels remain visible. | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 5.2 | Coercive party demands "Aura's predictions about me" | The Reasoning Trace drawer is fully readable; this is by design — there is no hidden prediction. The drawer also shows the actions the user took, which is the user's own data. | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 5.3 | User triggers panic-wipe under the table | Aura wipes silently without on-screen confirmation; coercive party sees a clean app | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 5.4 | Audit log post-event shows the coercive access | Audit log shows the read events with timestamps; usable as evidence after the fact | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 6. Aggregate result

| Adversary | Total checks | PASS | FAIL | Notes |
|---|---|---|---|---|
| 1. Curious app | 4 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 2. Lost / stolen device | 4 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 3. Hostile listener / accessibility | 4 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 4. Cloud account compromise | 4 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| 5. Coercion | 4 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| **Totals** | **20** | **[REPLACE WITH MEASURED VALUE]** | **[REPLACE WITH MEASURED VALUE]** | |

---

## 7. Failed-attack remediation log

For each FAIL, a row here:

| Attack ID | Failure description | Remediation | Status |
|---|---|---|---|
| [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

---

## 8. Sign-off

| Role | Name | Date |
|---|---|---|
| Audit lead (attacker) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Audit recorder (defender) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Final sign-off | Shaurya Punj | [REPLACE WITH MEASURED VALUE] |

— end of 04_threat_model_validation.md —
