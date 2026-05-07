# Aura Pilot — Data Handling

How raw recordings, transcripts, and per-participant CSV/JSON artefacts produced by the Wizard-of-Oz lab study are stored, anonymised, shared between the two coders, and deleted at pilot end.

Reference: ADR-0005 (on-device only); ADR-0007 (memory encryption); ADR-0011 (no Apple Developer Program); `pilot/CONSENT_v2.md`; `wizard_of_oz_protocol.md`.
Last updated: 2026-05-07
Owner: Shaurya Punj

---

## 1. What artefacts each session produces

Every lab session produces, at most, six artefacts. They are written to one folder per participant: `aura/pilot/raw/PNNN/`.

| Artefact | File | Source | Contains PII? |
|---|---|---|---|
| Session video + audio | `PNNN_session.mp4` | QuickTime mirror of the demo iPhone + lavalier mic | Yes — voice, on-screen content |
| Audio extract for transcription | `PNNN_session.wav` | `ffmpeg -i PNNN_session.mp4 -vn PNNN_session.wav` (intermediate) | Yes — voice |
| Raw transcript | `PNNN_transcript_raw.txt` | `whisper.cpp` output | Yes — first names, phone numbers, email addresses if spoken |
| Redacted transcript | `PNNN_transcript.txt` | regex + manual redaction pass on raw | No (after pass) |
| Aura instrumentation log | `PNNN_aura_log.json` | exported from Aura on the demo phone | No — already anonymised at export |
| Field notes | `PNNN_field_notes.md` | researcher-typed 5–10 lines | Should not contain PII; researcher discipline |

The participant's own-phone screen recording (when consented) is captured directly into `PNNN_session.mp4` as a second QuickTime track, not as a separate file.

---

## 2. Where each artefact lives

| Artefact | Live location | Backup | Cloud? |
|---|---|---|---|
| `PNNN_session.mp4` | Team Mac SSD, `aura/pilot/raw/PNNN/` | External SSD (rsync nightly) | **No** |
| `PNNN_session.wav` | Team Mac SSD only, intermediate | None — deleted after transcription | **No** |
| `PNNN_transcript_raw.txt` | Team Mac SSD, `aura/pilot/raw/PNNN/` | None — deleted after redaction pass | **No** |
| `PNNN_transcript.txt` | Team Mac SSD; private GitHub repo branch `pilot-transcripts` (encrypted-zip blob) | External SSD | **GitHub private branch only** (encrypted-zip with passphrase shared between Shaurya and Shorya via Signal) |
| `PNNN_aura_log.json` | Team Mac SSD; eventually committed to `aura/pilot/analysis/raw/` (anonymised) | External SSD | **GitHub public repo** at end of pilot, after final anonymisation review |
| `PNNN_field_notes.md` | Team Mac SSD; private GitHub branch | External SSD | **GitHub private branch only** |

Nothing goes to Google Drive, iCloud, Dropbox, or any third-party cloud service. The on-device-only ADR-0005 posture is honoured for participant data too.

---

## 3. The PII directory layout

```
aura/pilot/
├── raw/                                # local-only, .gitignore'd
│   ├── _resign_log.txt                 # certificate re-sign trail (no PII)
│   ├── _consent_index.csv              # PNNN ↔ first name ↔ WhatsApp last 4 (PII)
│   ├── _consent_signed_scans/          # PDF scans of signed consent forms (PII)
│   │   └── PNNN_consent.pdf
│   ├── P001/
│   │   ├── P001_session.mp4
│   │   ├── P001_session.wav            # transient, deleted within 24h of transcript
│   │   ├── P001_transcript_raw.txt     # transient, deleted within 24h of redaction
│   │   ├── P001_transcript.txt
│   │   ├── P001_aura_log.json
│   │   └── P001_field_notes.md
│   └── P002/ ... P035/
└── analysis/
    └── raw/                            # committed to public repo at end of pilot
        ├── sessions_master.csv         # one row per session, no PII
        ├── tasks_long.csv              # one row per (participant × task × round)
        ├── survey.csv                  # one row per participant, anonymised
        └── aura_logs/                  # PNNN_aura_log.json copies (anonymised)
```

`aura/pilot/raw/` is in `.gitignore`. Only `aura/pilot/analysis/raw/` is committed.

---

## 4. Anonymisation procedure

### 4.1 Participant ID assignment

- IDs are `P001`–`P035` assigned in order of consent-form signature.
- The mapping `participant_id ↔ first name ↔ WhatsApp last 4` lives in **two places only**: `_consent_index.csv` on the team Mac SSD, and the `pii_lookup` tab of the master Google Sheet (restricted to Shaurya and Shorya). It is never committed to git.
- After the pilot ends, the `_consent_index.csv` is moved to an encrypted dmg on the team Mac (`Disk Utility → New Image → AES-256`, passphrase known to both researchers). The plaintext version is shredded with `rm -P`.

### 4.2 Transcript redaction

Two-pass, applied on `PNNN_transcript_raw.txt` to produce `PNNN_transcript.txt`:

**Pass 1 — automated regex sweep** (script at `aura/pilot/scripts/redact_transcript.py`, to be added in Week 8):

- Phone numbers: `\b(\+91[\s-]?)?[6-9]\d{9}\b` → `[PHONE]`
- Email addresses: standard RFC pattern → `[EMAIL]`
- The participant's first name (read from `_consent_index.csv` for that PNNN) → `[NAME]`
- Common PII tokens: PAN, Aadhaar 12-digit groups, IFSC, UPI handles `\S+@\S+` → `[PII]`

**Pass 2 — manual review.** The researcher reads the transcript end-to-end and masks:

- Any other proper names (friends, faculty, hostel block letters that uniquely identify a person)
- Any place that could re-identify (specific room number, specific building if uncommon)
- Any sensitive disclosure unrelated to Aura (mental-health admission, family conflict, etc.)

The redacted transcript is the only version that leaves the team Mac SSD.

### 4.3 Aura instrumentation log anonymisation

`PNNN_aura_log.json` is produced by Aura's "Export pilot logs" button on the demo phone. The export pipeline (already in `aura/orchestrator/exporter.py`, audited per ADR-0004 §Glass-box trace) strips:

- Any token from the test calendar event title that matches a known seed value, replaced with the seed's anonymised label.
- Any HealthKit reading ranges (these are Shaurya's own values from the demo phone, not the participant's, but we strip them anyway because they are identifying for Shaurya).
- Any timestamp is preserved (relative timestamps within a session are needed for the analysis), but absolute date is shifted to a per-participant epoch (`session_start_iso = T0`, all events recorded as `T0 + Δ_ms`).

A second researcher spot-checks 3 random `PNNN_aura_log.json` files per pilot week against this checklist before any commit to the public branch.

---

## 5. Sharing between coders

The qualitative coding (`qual_protocol.md` §3) requires both researchers to read the same redacted transcripts independently.

- The redacted transcripts are shared via a **private GitHub branch** named `pilot-transcripts` on the team's private repo `galaxy-brain/aura-pilot-data`. The repo is private; only Shaurya and Shorya have access.
- Each transcript is committed as an encrypted-zip: `PNNN_transcript.txt.zip` with AES passphrase `aes-256` set via `7z a -p<passphrase> -mhe=on`. The passphrase is shared between the two researchers via Signal disappearing message and rotated at the end of the pilot.
- Coding spreadsheets (Taguette export or Google Sheet) live in the same private repo. Coding is done on the redacted transcript only; raw transcripts never travel.

---

## 6. Retention and deletion timeline

| Artefact | Lifetime |
|---|---|
| `PNNN_session.wav` (audio extract for Whisper) | Deleted within **24 hours** of `PNNN_transcript.txt` being produced. `rm -P` (overwrite). |
| `PNNN_transcript_raw.txt` (pre-redaction) | Deleted within **24 hours** of `PNNN_transcript.txt` being produced. |
| Audio track inside `PNNN_session.mp4` | The MP4 itself is kept for video-only review of Aura's screen behaviour. The audio inside the MP4 is **stripped** (`ffmpeg -i in.mp4 -an -c:v copy out.mp4`) **within 7 days** of `PNNN_transcript.txt` being produced. The result `PNNN_session_silent.mp4` replaces the original; the original is shredded. |
| `PNNN_session_silent.mp4` (video-only) | Deleted at **pilot end (15 July 2026)** unless an autonomy-rating dispute requires re-review, in which case it is kept for 30 additional days. |
| `PNNN_transcript.txt` (redacted) | Kept on team Mac SSD and private GitHub branch until **31 December 2026**, then moved to encrypted dmg cold storage. |
| `PNNN_aura_log.json` (anonymised) | Kept indefinitely; committed to public repo at pilot end. This is the artefact judges verify our claims against. |
| `_consent_index.csv` (PII map) | Kept until pilot end; then moved to encrypted dmg on team Mac. Plaintext shredded. |
| Signed paper consent forms | Scanned to `_consent_signed_scans/`, then originals stored in a locked drawer in Shaurya's hostel room. Destroyed by paper shredder **31 December 2026**. |

A participant who exercises the withdrawal right (CONSENT_v2 §7) triggers an immediate-deletion pass on every artefact bearing their PNNN, within 7 days, with written confirmation.

---

## 7. Access control

- **Team Mac SSD:** FileVault enabled; login password known to Shaurya only. Shorya works from a session-share when needed (Shaurya logs in, Shorya operates).
- **External SSD:** APFS-encrypted; passphrase known to both researchers; lives in Shaurya's backpack during the pilot, in a locked drawer otherwise.
- **Private GitHub repo `galaxy-brain/aura-pilot-data`:** access limited to Shaurya and Shorya. Two-factor auth required. SSH keys only.
- **Public GitHub repo (the main Aura repo):** read-public, write restricted. Only `aura/pilot/analysis/raw/` artefacts are committed here, and only after the anonymisation spot-check has been signed off by both researchers.

---

## 8. Incident response

If a recording is accidentally uploaded to a cloud service, or the external SSD is lost, or a private branch is briefly made public:

1. **Within 1 hour:** revoke access (delete the cloud copy; rotate the GitHub branch passphrase; force-push delete any leaked commit + GitHub support contact for cache purge).
2. **Within 24 hours:** notify every affected participant by WhatsApp + email with a plain-English description of what happened and what we have done.
3. **Within 7 days:** offer to delete all of the affected participants' artefacts immediately if they ask, regardless of pilot completion.
4. **Document** the incident in `pilot/raw/_incident_log.md` (created on first incident).

This is the only acceptable handling. We do not minimise. We do not delay.

---

## 9. End-of-pilot checklist (15 July 2026)

- [ ] All `PNNN_session.wav` deleted with `rm -P`
- [ ] All `PNNN_transcript_raw.txt` deleted
- [ ] Audio stripped from every `PNNN_session.mp4`; replaced by `PNNN_session_silent.mp4`
- [ ] All `PNNN_session_silent.mp4` either deleted (default) or moved to dispute-hold folder (only if a 100-action autonomy-rating dispute is open)
- [ ] `_consent_index.csv` moved to encrypted dmg; plaintext shredded
- [ ] Public-repo `aura/pilot/analysis/raw/` artefacts spot-checked against the anonymisation checklist by both researchers, signed off in `pilot/analysis/raw/_signoff.md`
- [ ] `THANKS.md` updated with consenting first names
- [ ] Email to all 30 participants confirming the deletion has happened, with the public-repo link for them to verify what we kept

End of data handling doc.
