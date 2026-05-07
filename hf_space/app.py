"""Aura — HuggingFace Spaces (Gradio) public showcase demo.

This is a *showcase* demo running on synthetic data only. The on-device
production agents never send personal data to any cloud — including this
Space. Every tab here loads the same Python agent classes that ship in the
Aura mobile build (`aura/agents/...`), but the inputs are explicit examples
typed or sliced by the visitor.

Tabs (per Phase-3 brief):
1. Morning Brief         — synthetic Health + Calendar + Comms -> brief card + Trace.
2. Quiet Group Chat      — paste 50-message blob, see CommsAgent triage.
3. Spend Mirror          — paste Indian UPI SMS, see FinanceAgent parse + categorise.
4. Load Score            — slide HRV / typing-entropy / app-switch, see Load Score + intervention.
5. Memory Graph          — add nodes, search, export JSON, see audit log.

Visual language matches deck_spec §0:
- Background  #FAF8F5
- Ink         #0E0E0E
- Accent      #FF5B2E
- Fraunces (display) + Inter Tight (UI)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Make the parent `aura/` package importable when this file is run directly
# from inside `hf_space/`.
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import gradio as gr  # noqa: E402

from agents.calendar.agent import CalendarAgent  # noqa: E402
from agents.comms.agent import CommsAgent  # noqa: E402
from agents.core.types import (  # noqa: E402
    AgentInput,
    AgentName,
    UserState,
)
from agents.finance.agent import FinanceAgent  # noqa: E402
from agents.wellness.agent import WellnessAgent  # noqa: E402
from agents.wellness.load_score import LoadScoreModel, WellnessFeatures  # noqa: E402
from memory.store import MemoryGraph  # noqa: E402
from orchestrator.graph import Orchestrator  # noqa: E402
from orchestrator.policy import Policy  # noqa: E402


# ---------------------------------------------------------------------------
# Banner + CSS
# ---------------------------------------------------------------------------

DISCLAIMER = (
    "DEMO ON SYNTHETIC DATA — NO USER DATA EVER LEAVES YOUR DEVICE IN PRODUCTION."
)

HERO_HTML = f"""
<div class="aura-hero">
  <div class="aura-hero-row">
    <svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="22" cy="22" r="20" fill="none" stroke="#0E0E0E" stroke-width="2"/>
      <circle cx="22" cy="22" r="6" fill="#FF5B2E"/>
    </svg>
    <div class="aura-hero-text">
      <h1>Aura</h1>
      <p class="aura-tagline">Anticipate. Act. Stay quiet.</p>
    </div>
  </div>
  <p class="aura-disclaimer">{DISCLAIMER}</p>
</div>
"""

_CSS_PATH = _HERE / "style.css"
CUSTOM_CSS = _CSS_PATH.read_text() if _CSS_PATH.exists() else ""


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------

EXAMPLE_GROUP_CHAT = """\
[09:01] @aarav: gn folks
[09:02] @rhea: lol same
[09:03] @sid: btw quiz tomorrow @you can you share notes
[09:05] @pri: thx aarav
[09:06] @aarav: brb
[09:07] @sid: @you reminder — viva at 4pm today, please confirm
[09:08] @rhea: same
[09:09] @ish: lol
[09:11] @kabir: nice
[09:12] @pri: cool
[09:14] @sid: idk
[09:15] @rhea: tbh same
[09:16] @kabir: btw who's on for chai
[09:18] @aarav: 3 ok
[09:19] @ish: lol
[09:20] @pri: thanks
[09:22] @rhea: gm
[09:23] @sid: please submit lab report by tonight
[09:25] @aarav: on it
[09:27] @ish: lmao
[09:28] @kabir: same
[09:30] @rhea: btw Prof shared deadline asap urgent
[09:32] @pri: ok
[09:33] @sid: @you can you push the merge before 5
[09:34] @ish: nice
[09:36] @kabir: brb
[09:38] @aarav: thx
[09:40] @rhea: tbh idk
[09:41] @ish: lol
[09:42] @pri: ok
[09:43] @sid: anyone has the slides
[09:44] @kabir: same
[09:46] @rhea: lol
[09:47] @aarav: gn
[09:48] @ish: brb
[09:50] @pri: thanks
[09:52] @sid: bruh same
[09:53] @kabir: gn
[09:54] @rhea: lol
[09:55] @ish: lol
[09:56] @aarav: confirm the meeting at 5
[09:57] @pri: ok
[09:58] @kabir: thanks
[10:00] @sid: please reply on the rebase pr
[10:02] @rhea: lol
[10:03] @ish: nice
[10:04] @pri: thx
[10:05] @kabir: gm
"""

EXAMPLE_SMS = (
    "Sent Rs.350.00 from A/c **1234 to ZOMATO via UPI on 07-MAY\n"
    "INR 250.00 spent on ICICI Bank Card XX9921 at SWIGGY on 07-May-26\n"
    "INR 540 debited A/c no. XX2245 07-05-26 13:42 UPI/P2A/uber@axis/Uber\n"
    "Dear Customer, Rs.1200.00 debited from A/c X3389 on 07-05-26 to "
    "VPA bigbasket@okhdfc Ref 412345. -SBI"
)


# ---------------------------------------------------------------------------
# Tab 1 — Morning Brief
# ---------------------------------------------------------------------------

def run_morning_brief(
    rmssd_ms: float,
    sleep_debt_min: float,
    notif_count: int,
    has_calendar_conflict: bool,
) -> tuple[str, str]:
    """Wire the four agents through the orchestrator and surface the chosen brief."""

    tick_ts = "2026-05-07T08:30:00+00:00"

    # Synthetic notifications — repeat a mix of social / actionable.
    seed = [
        {"id": "n_001", "app_pkg": "wa", "channel": "ch_friends", "preview": "lol same",
         "intent_hint": "social chatter", "ts": tick_ts},
        {"id": "n_002", "app_pkg": "wa", "channel": "ch_class", "preview": "@you reminder viva at 4pm please confirm",
         "intent_hint": "actionable", "ts": tick_ts},
        {"id": "n_003", "app_pkg": "slack", "channel": "ch_team", "preview": "please push the merge before 5",
         "intent_hint": "actionable", "ts": tick_ts},
    ]
    notif_events = (seed * (1 + notif_count // len(seed)))[:notif_count]

    # Calendar — one or two events; conflict toggle adds an overlap.
    events_today = [
        {"id": "ev_morning", "title": "Standup",
         "start": "2026-05-07T09:00:00+00:00", "end": "2026-05-07T09:30:00+00:00"},
        {"id": "ev_class", "title": "DSA class",
         "start": "2026-05-07T10:00:00+00:00", "end": "2026-05-07T11:00:00+00:00"},
    ]
    if has_calendar_conflict:
        events_today.append({
            "id": "ev_lab", "title": "Lab review",
            "start": "2026-05-07T10:30:00+00:00", "end": "2026-05-07T11:30:00+00:00",
        })

    # Wellness payload.
    wellness_payload = {
        "rmssd_ms": rmssd_ms,
        "rmssd_z": (rmssd_ms - 45.0) / 12.0,
        "sleep_debt_min": sleep_debt_min,
        "typing_entropy": 4.2,
        "app_switch_rate": 8,
        "notif_dismiss_rate": 0.4,
        "screen_on_min": 35,
    }

    user_state = UserState(load_score=50)
    finance = FinanceAgent()
    orch = Orchestrator(
        agents=[CommsAgent(), CalendarAgent(), finance, WellnessAgent()],
        policy=Policy(),
    )

    result = orch.tick(
        user_state=user_state,
        agent_payloads={
            "comms": {"notif_events": notif_events, "gmail_threads": []},
            "calendar": {"events_today": events_today, "preferences": {"buffer_minutes": 15}},
            "finance": {"sms_unprocessed": [], "gmail_receipts": []},
            "wellness": wellness_payload,
        },
        tick_ts=tick_ts,
    )

    # Card-shaped summary.
    comms_out = next((o for o in result.agent_outputs if o.agent == AgentName.COMMS), None)
    cal_out = next((o for o in result.agent_outputs if o.agent == AgentName.CALENDAR), None)
    well_out = next((o for o in result.agent_outputs if o.agent == AgentName.WELLNESS), None)

    urgent_n = len((comms_out.payload or {}).get("urgent", [])) if comms_out else 0
    muted_n = (comms_out.payload or {}).get("muted_count", 0) if comms_out else 0
    conflicts_n = len((cal_out.payload or {}).get("conflicts", [])) if cal_out else 0
    next_event = (cal_out.payload or {}).get("next_event") if cal_out else None
    load_score = (well_out.payload or {}).get("load_score", 0) if well_out else 0
    intervention = ((well_out.payload or {}).get("suggested_intervention") or {}).get("kind", "DO_NOTHING") if well_out else "DO_NOTHING"

    leave_by_str = ""
    if next_event:
        leave_by_str = (
            f"<div class='card-row'><span class='label'>Leave by</span>"
            f"<span class='value'>{next_event.get('leave_by','')}</span></div>"
        )

    chosen = result.chosen_kind
    rationale = result.trace.rationale

    card_html = f"""
    <div class="aura-card">
      <div class="card-head">
        <span class="card-eyebrow">Morning brief</span>
        <span class="card-pill">{chosen}</span>
      </div>
      <div class="card-grid">
        <div class="card-row"><span class="label">Load score</span><span class="value">{load_score}</span></div>
        <div class="card-row"><span class="label">Intervention</span><span class="value">{intervention}</span></div>
        <div class="card-row"><span class="label">Actionable</span><span class="value">{urgent_n}</span></div>
        <div class="card-row"><span class="label">Muted</span><span class="value">{muted_n}</span></div>
        <div class="card-row"><span class="label">Conflicts</span><span class="value">{conflicts_n}</span></div>
        {leave_by_str}
      </div>
      <p class="card-rationale">{rationale}</p>
    </div>
    """

    trace_json = json.dumps(result.trace.model_dump(mode="json"), indent=2)
    return card_html, trace_json


# ---------------------------------------------------------------------------
# Tab 2 — Quiet Group Chat
# ---------------------------------------------------------------------------

def run_quiet_group(text_blob: str) -> tuple[str, str]:
    """Slice a chat blob into N synthetic notif_events and run CommsAgent."""

    lines = [ln.strip() for ln in (text_blob or "").splitlines() if ln.strip()]
    notif_events = []
    for i, line in enumerate(lines[:80]):
        notif_events.append({
            "id": f"n_{i:03d}",
            "app_pkg": "wa",
            "channel": "ch_demo",
            "preview": line,
            "intent_hint": line[:40],
            "ts": "2026-05-07T09:00:00+00:00",
        })

    agent = CommsAgent()
    inp = AgentInput(
        tick_ts="2026-05-07T09:00:00+00:00",
        agent=AgentName.COMMS,
        user_state=UserState(load_score=72),
        payload={"notif_events": notif_events, "gmail_threads": []},
    )
    out = agent.tick(inp)
    payload = out.payload
    urgent = payload.get("urgent", [])
    muted_count = payload.get("muted_count", 0)

    rows = "".join(
        f"<li><code>{u['item_id']}</code> &middot; {u['reason_code']} &middot; "
        f"score {u['score']:.2f}</li>"
        for u in urgent
    ) or "<li class='muted'>No actionable items</li>"

    card_html = f"""
    <div class="aura-card">
      <div class="card-head">
        <span class="card-eyebrow">Quiet Group Chat</span>
        <span class="card-pill">{payload.get('top_suggested_action','')}</span>
      </div>
      <div class="card-grid">
        <div class="card-row"><span class="label">Total messages</span><span class="value">{len(notif_events)}</span></div>
        <div class="card-row"><span class="label">Actionable</span><span class="value">{len(urgent)}</span></div>
        <div class="card-row"><span class="label">Muted</span><span class="value">{muted_count}</span></div>
      </div>
      <ul class="card-list">{rows}</ul>
    </div>
    """

    trace_json = json.dumps({
        "agent": "comms",
        "decision": out.trace_fragment.decision if out.trace_fragment else "",
        "drivers": out.trace_fragment.drivers if out.trace_fragment else [],
        "drafts": payload.get("drafts", []),
    }, indent=2)
    return card_html, trace_json


# ---------------------------------------------------------------------------
# Tab 3 — Spend Mirror
# ---------------------------------------------------------------------------

def run_spend_mirror(sms_blob: str) -> tuple[str, str]:
    """Parse a multi-line UPI SMS blob through FinanceAgent regex pack."""

    agent = FinanceAgent()
    rows: List[Dict[str, Any]] = []
    skipped = 0
    for line in (sms_blob or "").splitlines():
        line = line.strip()
        if not line:
            continue
        txn = agent.parse_sms(line)
        if txn is None:
            skipped += 1
            continue
        rows.append({
            "amount": txn.amount,
            "currency": txn.currency,
            "merchant": txn.merchant_raw,
            "category": txn.category.value if txn.category else "other",
            "bank": txn.bank,
            "account_last4": txn.account_last4,
            "ts": txn.ts.isoformat(),
        })

    total = sum(r["amount"] for r in rows)

    rows_html = "".join(
        f"<tr><td>{r['merchant']}</td><td>{r['category']}</td>"
        f"<td>{r['bank']}</td><td>**{r['account_last4']}</td>"
        f"<td class='right'>₹{r['amount']:.2f}</td></tr>"
        for r in rows
    ) or "<tr><td colspan='5' class='muted'>No SMS parsed</td></tr>"

    card_html = f"""
    <div class="aura-card">
      <div class="card-head">
        <span class="card-eyebrow">Spend Mirror</span>
        <span class="card-pill">₹{total:,.0f}</span>
      </div>
      <table class="aura-table">
        <thead><tr>
          <th>Merchant</th><th>Category</th><th>Bank</th><th>A/c</th><th class="right">Amount</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
      <p class="card-rationale">Parsed {len(rows)} txn — {skipped} unparsed (queued for fallback).</p>
    </div>
    """

    return card_html, json.dumps({"transactions": rows, "skipped": skipped}, indent=2)


# ---------------------------------------------------------------------------
# Tab 4 — Load Score
# ---------------------------------------------------------------------------

def run_load_score(
    rmssd_ms: float,
    typing_entropy: float,
    app_switch_rate: int,
    sleep_debt_min: float,
) -> tuple[str, str]:
    """Drive the WellnessAgent + LoadScoreModel directly."""

    feats = WellnessFeatures(
        rmssd_ms=rmssd_ms,
        rmssd_z=(rmssd_ms - 45.0) / 12.0,
        sleep_debt_min=sleep_debt_min,
        typing_entropy=typing_entropy,
        app_switch_rate=int(app_switch_rate),
        notif_dismiss_rate=0.4,
        screen_on_min=30,
    )
    model = LoadScoreModel()
    raw_score = int(round(model.predict_score(feats)))
    drivers = model.driver_breakdown(feats)

    agent = WellnessAgent(model=model)
    out = agent.tick(AgentInput(
        tick_ts="2026-05-07T11:30:00+00:00",
        agent=AgentName.WELLNESS,
        user_state=UserState(load_score=raw_score),
        payload={
            "rmssd_ms": rmssd_ms,
            "rmssd_z": (rmssd_ms - 45.0) / 12.0,
            "sleep_debt_min": sleep_debt_min,
            "typing_entropy": typing_entropy,
            "app_switch_rate": int(app_switch_rate),
            "notif_dismiss_rate": 0.4,
            "screen_on_min": 30,
        },
    ))
    payload = out.payload
    interv = payload.get("suggested_intervention") or {}
    state = payload.get("state", "UNKNOWN")
    score = payload.get("load_score", raw_score)

    drivers_html = "".join(
        f"<li><span class='label'>{d['feature']}</span>"
        f"<span class='value'>{d['value']}</span></li>"
        for d in drivers
    )

    card_html = f"""
    <div class="aura-card">
      <div class="card-head">
        <span class="card-eyebrow">Load Score</span>
        <span class="card-pill score-{('high' if score>=70 else 'mid' if score>=50 else 'low')}">{score}</span>
      </div>
      <div class="card-grid">
        <div class="card-row"><span class="label">State</span><span class="value">{state}</span></div>
        <div class="card-row"><span class="label">Intervention</span><span class="value">{interv.get('kind','DO_NOTHING')}</span></div>
        <div class="card-row"><span class="label">Surface</span><span class="value">{interv.get('surface','SILENT')}</span></div>
        <div class="card-row"><span class="label">Confirm</span><span class="value">{interv.get('confirm_required',False)}</span></div>
      </div>
      <ul class="card-list">{drivers_html}</ul>
      <p class="card-rationale">{interv.get('rationale_seed','')}</p>
    </div>
    """

    return card_html, json.dumps({
        "load_score": score,
        "state": state,
        "drivers": drivers,
        "intervention": interv,
    }, indent=2)


# ---------------------------------------------------------------------------
# Tab 5 — Memory Graph
# ---------------------------------------------------------------------------

# Single in-process graph for the Space session. Each visitor gets the same
# instance — fine for a public showcase, since we never store PII.
_GRAPH = MemoryGraph(path=":memory:")


def memory_add(node_type: str, data_json: str) -> tuple[str, str]:
    try:
        data = json.loads(data_json or "{}")
    except json.JSONDecodeError as exc:
        return f"<div class='aura-card error'>Bad JSON: {exc}</div>", ""
    nid = _GRAPH.add_node(type=node_type, data=data)
    _GRAPH.add_embedding(nid, 0, json.dumps(data))
    return (
        f"<div class='aura-card'><b>Added node</b> <code>{nid}</code></div>",
        nid,
    )


def memory_search(query: str, k: int = 5) -> str:
    if not query.strip():
        return "<div class='aura-card muted'>Type a query.</div>"
    results = _GRAPH.search(query, k=int(k))
    if not results:
        return "<div class='aura-card muted'>No matches.</div>"
    rows = "".join(
        f"<tr><td><code>{r['node_id']}</code></td><td>{r['type']}</td>"
        f"<td>{r['score']:.4f}</td><td>{json.dumps(r['data'])[:80]}</td></tr>"
        for r in results
    )
    return f"""
    <div class="aura-card">
      <div class="card-head"><span class="card-eyebrow">Search results</span></div>
      <table class="aura-table"><thead><tr>
        <th>Node</th><th>Type</th><th>Score</th><th>Data</th>
      </tr></thead><tbody>{rows}</tbody></table>
    </div>
    """


def memory_export() -> str:
    export = _GRAPH.export_json()
    return json.dumps(export, indent=2)


def memory_audit() -> str:
    rows = _GRAPH.conn.execute(
        "SELECT seq, ts, op, target_type, target_id, agent, hash_chain "
        "FROM audit_log ORDER BY seq DESC LIMIT 30"
    ).fetchall()
    if not rows:
        return "<div class='aura-card muted'>No audit entries yet.</div>"
    body = "".join(
        f"<tr><td>{r['seq']}</td><td>{r['op']}</td><td>{r['target_type']}</td>"
        f"<td><code>{(r['target_id'] or '')[:18]}</code></td>"
        f"<td><code>{r['hash_chain'][:12]}…</code></td></tr>"
        for r in rows
    )
    return f"""
    <div class="aura-card">
      <div class="card-head"><span class="card-eyebrow">Audit log (last 30)</span></div>
      <table class="aura-table"><thead><tr>
        <th>Seq</th><th>Op</th><th>Target</th><th>Id</th><th>Hash</th>
      </tr></thead><tbody>{body}</tbody></table>
    </div>
    """


# ---------------------------------------------------------------------------
# Build the Gradio UI
# ---------------------------------------------------------------------------

def _aura_theme() -> gr.themes.Base:
    return gr.themes.Base(
        primary_hue=gr.themes.Color(
            c50="#FFF1EC", c100="#FFD9CB", c200="#FFB69E", c300="#FF8E6B",
            c400="#FF6F46", c500="#FF5B2E", c600="#E54A1F", c700="#B6391A",
            c800="#7E2812", c900="#4A170A", c950="#2A0D05",
        ),
        secondary_hue="orange",
        neutral_hue="stone",
        font=[gr.themes.GoogleFont("Inter Tight"), "Inter Tight", "system-ui", "sans-serif"],
        font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
    ).set(
        body_background_fill="#FAF8F5",
        body_text_color="#0E0E0E",
        block_background_fill="#FFFFFF",
        block_border_color="#E8E2D8",
        button_primary_background_fill="#FF5B2E",
        button_primary_text_color="#FFFFFF",
    )


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Aura — On-device proactive assistant", css=CUSTOM_CSS, theme=_aura_theme()) as demo:
        gr.HTML(HERO_HTML)

        with gr.Tabs():
            # ----- Tab 1 ---------------------------------------------------
            with gr.Tab("Morning Brief"):
                gr.Markdown(
                    "Synthetic Health + Calendar + Comms inputs flow through the orchestrator. "
                    "The card and trace below mirror what the iPhone surface would render."
                )
                with gr.Row():
                    rmssd1 = gr.Slider(15, 80, value=45, step=1, label="Resting RMSSD (ms)")
                    sleep1 = gr.Slider(0, 240, value=60, step=5, label="Sleep debt (min)")
                with gr.Row():
                    notif1 = gr.Slider(0, 60, value=12, step=1, label="Notification volume")
                    conf1 = gr.Checkbox(label="Calendar conflict")
                run1 = gr.Button("Run morning brief", variant="primary")
                card1 = gr.HTML()
                trace1 = gr.Code(language="json", label="Reasoning Trace")
                run1.click(run_morning_brief, [rmssd1, sleep1, notif1, conf1], [card1, trace1])

            # ----- Tab 2 ---------------------------------------------------
            with gr.Tab("Quiet Group Chat"):
                gr.Markdown("Paste any chat blob. CommsAgent triages to actionable + muted.")
                chat_box = gr.Textbox(value=EXAMPLE_GROUP_CHAT, lines=14, label="Group chat (any format)")
                run2 = gr.Button("Triage", variant="primary")
                card2 = gr.HTML()
                trace2 = gr.Code(language="json", label="Reasoning Trace")
                run2.click(run_quiet_group, [chat_box], [card2, trace2])

            # ----- Tab 3 ---------------------------------------------------
            with gr.Tab("Spend Mirror"):
                gr.Markdown(
                    "Paste UPI SMS strings (HDFC / SBI / ICICI / Axis). "
                    "FinanceAgent runs its on-device regex pack and categorises."
                )
                sms_box = gr.Textbox(value=EXAMPLE_SMS, lines=10, label="UPI SMS strings, one per line")
                run3 = gr.Button("Parse + categorise", variant="primary")
                card3 = gr.HTML()
                trace3 = gr.Code(language="json", label="Parsed transactions")
                run3.click(run_spend_mirror, [sms_box], [card3, trace3])

            # ----- Tab 4 ---------------------------------------------------
            with gr.Tab("Load Score"):
                gr.Markdown("Slide the four headline features and watch the regressor + intervention picker.")
                with gr.Row():
                    rmssd4 = gr.Slider(15, 80, value=28, step=1, label="RMSSD (ms) — lower = stressed")
                    entropy4 = gr.Slider(2.0, 6.0, value=4.8, step=0.1, label="Typing entropy (bits)")
                with gr.Row():
                    switch4 = gr.Slider(0, 30, value=14, step=1, label="App switch rate / min")
                    sleep4 = gr.Slider(0, 240, value=120, step=5, label="Sleep debt (min)")
                run4 = gr.Button("Recompute Load", variant="primary")
                card4 = gr.HTML()
                trace4 = gr.Code(language="json", label="Wellness output")
                run4.click(run_load_score, [rmssd4, entropy4, switch4, sleep4], [card4, trace4])

            # ----- Tab 5 ---------------------------------------------------
            with gr.Tab("Memory Graph"):
                gr.Markdown(
                    "Add nodes, search semantically, export the full JSON, see the audit chain. "
                    "All in-memory — destroyed when the Space restarts."
                )
                with gr.Row():
                    nodetype = gr.Dropdown(
                        choices=["Event", "Person", "Place", "Transaction", "Conversation",
                                 "Action", "Trace", "App", "User", "HealthSnapshot"],
                        value="Event", label="Node type",
                    )
                    nodedata = gr.Textbox(
                        value='{"title":"DSA quiz","note":"Tomorrow 10am"}',
                        label="Node data (JSON)",
                    )
                add_btn = gr.Button("Add node + embed", variant="primary")
                add_out = gr.HTML()
                last_id = gr.Textbox(visible=False)
                add_btn.click(memory_add, [nodetype, nodedata], [add_out, last_id])

                with gr.Row():
                    q = gr.Textbox(value="quiz tomorrow", label="Search query")
                    k = gr.Slider(1, 10, value=5, step=1, label="Top-k")
                search_btn = gr.Button("Search")
                search_out = gr.HTML()
                search_btn.click(memory_search, [q, k], [search_out])

                with gr.Row():
                    export_btn = gr.Button("Export JSON")
                    audit_btn = gr.Button("View audit log")
                export_out = gr.Code(language="json", label="Graph export")
                audit_out = gr.HTML()
                export_btn.click(memory_export, [], [export_out])
                audit_btn.click(memory_audit, [], [audit_out])

        gr.HTML(
            "<footer class='aura-footer'>"
            "Aura is on-device. This Space is a synthetic showcase. "
            "Production never sends personal data to any cloud."
            "</footer>"
        )

    return demo


def main() -> None:
    demo = build_ui()
    demo.queue().launch(
        server_name=os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")),
        share=False,
    )


if __name__ == "__main__":
    main()
