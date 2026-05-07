# Aura — local FastAPI + React fallback (venue stage runbook)

This directory is the **Tier-3** of the Phase-3 fallback plan: if the iPhone
fails on stage and the HuggingFace Space is unreachable, the team runs Aura
on the team's MacBook and projects the browser. **Zero internet egress.**

```bash
# From the aura/ directory:
bash web/run_local.sh
```

That single command:

1. Starts the FastAPI app at `http://localhost:8000` (the four agents +
   orchestrator behind a JSON API).
2. Starts a static file server at `http://localhost:8080`.
3. Opens `http://localhost:8080/index.html` in the default browser.

## Files

```
web/
├─ api/
│  ├─ main.py            # FastAPI: /api/comms /api/calendar /api/finance /api/wellness /api/orchestrator
│  └─ requirements.txt
├─ web/
│  ├─ index.html         # single-file React (no build step)
│  ├─ style.css          # locked palette per deck_spec §0
│  ├─ app.js             # 4 tabs, talks to localhost:8000
│  └─ vendor/            # React + ReactDOM + htm UMDs (bundled, offline-safe)
├─ run_local.sh          # one-command boot
└─ README.md             # this file
```

## Pre-stage rehearsal

1. Once on a machine with internet, run `bash web/run_local.sh`. Verify
   `web/web/vendor/*.js` exists (download instructions in
   `web/web/vendor/README.md` if not).
2. Disable Wi-Fi and re-run `bash web/run_local.sh`. Confirm the demo loads
   end-to-end with no internet — this proves the venue can flake and we still
   demo.
3. Run through the 4 tabs in this order so you remember the click path:
   Morning Brief → Quiet Group Chat → Spend Mirror → Load Score.

## What it demonstrates

- Tab 1 **Morning Brief** — orchestrator runs all four agents on synthetic
  Health + Calendar + Comms inputs; the brief card and full Reasoning Trace
  JSON appear.
- Tab 2 **Quiet Group Chat** — paste any chat blob; CommsAgent triages to
  actionable + muted; Reasoning Trace fragment shown.
- Tab 3 **Spend Mirror** — paste UPI SMS; FinanceAgent regex parses + hashes
  merchant + categorises.
- Tab 4 **Load Score** — slide HRV / typing-entropy / app-switch / sleep-debt;
  see Load Score and the picked intervention.

## Why this is the right fallback

- **Local**: nothing is sent over the network. The synthetic data sits in the
  browser's React state and the FastAPI process.
- **Same agent code as the iPhone**: identical Python module imports as the
  on-device build (`agents/comms`, `agents/calendar`, `agents/finance`,
  `agents/wellness`, `orchestrator/`).
- **No build step**: React + ReactDOM + htm are vendored as UMDs. No node, no
  npm, no Vite — just `python -m http.server` and `python -m uvicorn`.
- **One-command boot**: `bash web/run_local.sh`. The trap clause kills both
  children cleanly on Ctrl-C.

## Rehearsal checklist

- [ ] Vendor JS files present (`ls web/web/vendor/*.js`).
- [ ] `python3 -c "import fastapi, uvicorn"` succeeds.
- [ ] Wi-Fi off — boot still works.
- [ ] All four tabs render without console errors.
- [ ] Reasoning Trace JSON pretty-prints for slide capture.
