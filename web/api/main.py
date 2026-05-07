"""Local FastAPI fallback for the Phase-3 venue stage demo.

If the iPhone misbehaves and the HuggingFace Space is unreachable (venue
Wi-Fi flake), the team can run this server on a Mac and project the browser.
Everything runs offline — no internet required.

Endpoints
---------
- POST /api/comms/triage         -> CommsAgent.tick on a notif_events list
- POST /api/calendar/conflicts   -> CalendarAgent.tick on events_today
- POST /api/finance/parse_sms    -> FinanceAgent.parse_sms on a list of strings
- POST /api/wellness/load_score  -> WellnessAgent.tick from a feature payload
- POST /api/orchestrator/run_replay -> Full Orchestrator.tick on synthetic payload
- GET  /api/health               -> liveness probe

CORS is open since this is intended for local use only (`localhost`).
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Make the agent stack importable when this file is launched from anywhere.
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

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
from orchestrator.graph import Orchestrator  # noqa: E402
from orchestrator.policy import Policy  # noqa: E402


app = FastAPI(
    title="Aura local demo API",
    description="Venue-stage fallback. Synthetic inputs only. Runs offline.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Static frontend mount (same single-file React under /web)
# ---------------------------------------------------------------------------

_WEB_DIR = _HERE.parent / "web"
if _WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "service": "aura-local-demo",
        "frontend": "/web/index.html",
        "health": "/api/health",
    }


# ---------------------------------------------------------------------------
# Request shapes
# ---------------------------------------------------------------------------


class CommsRequest(BaseModel):
    notif_events: List[Dict[str, Any]] = Field(default_factory=list)
    gmail_threads: List[Dict[str, Any]] = Field(default_factory=list)
    load_score: int = 50
    tick_ts: str = "2026-05-07T09:00:00+00:00"


class CalendarRequest(BaseModel):
    events_today: List[Dict[str, Any]] = Field(default_factory=list)
    user_loc: Optional[Dict[str, float]] = None
    buffer_minutes: int = 15
    tick_ts: str = "2026-05-07T09:00:00+00:00"


class FinanceRequest(BaseModel):
    sms: List[str] = Field(default_factory=list)
    fallback_year: int = 2026


class WellnessRequest(BaseModel):
    rmssd_ms: float = 45.0
    typing_entropy: float = 4.0
    app_switch_rate: int = 6
    sleep_debt_min: float = 60.0
    notif_dismiss_rate: float = 0.3
    screen_on_min: int = 30
    in_focus_block: bool = False
    tick_ts: str = "2026-05-07T09:00:00+00:00"


class ReplayRequest(BaseModel):
    comms: Optional[CommsRequest] = None
    calendar: Optional[CalendarRequest] = None
    finance: Optional[FinanceRequest] = None
    wellness: Optional[WellnessRequest] = None
    tick_ts: str = "2026-05-07T09:00:00+00:00"
    load_score: int = 50


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/api/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}


@app.post("/api/comms/triage")
def comms_triage(req: CommsRequest) -> Dict[str, Any]:
    agent = CommsAgent()
    out = agent.tick(AgentInput(
        tick_ts=req.tick_ts,
        agent=AgentName.COMMS,
        user_state=UserState(load_score=req.load_score),
        payload={"notif_events": req.notif_events, "gmail_threads": req.gmail_threads},
    ))
    return {
        "payload": out.payload,
        "candidates": [c.model_dump() for c in out.candidates],
        "trace_fragment": out.trace_fragment.model_dump() if out.trace_fragment else None,
    }


@app.post("/api/calendar/conflicts")
def calendar_conflicts(req: CalendarRequest) -> Dict[str, Any]:
    agent = CalendarAgent()
    payload: Dict[str, Any] = {
        "events_today": req.events_today,
        "preferences": {"buffer_minutes": req.buffer_minutes},
    }
    if req.user_loc:
        payload["user_loc"] = req.user_loc
    out = agent.tick(AgentInput(
        tick_ts=req.tick_ts,
        agent=AgentName.CALENDAR,
        user_state=UserState(load_score=50),
        payload=payload,
    ))
    return {
        "payload": out.payload,
        "candidates": [c.model_dump() for c in out.candidates],
        "trace_fragment": out.trace_fragment.model_dump() if out.trace_fragment else None,
    }


@app.post("/api/finance/parse_sms")
def finance_parse_sms(req: FinanceRequest) -> Dict[str, Any]:
    agent = FinanceAgent()
    parsed: List[Dict[str, Any]] = []
    skipped: List[str] = []
    for line in req.sms:
        line = (line or "").strip()
        if not line:
            continue
        txn = agent.parse_sms(line, fallback_year=req.fallback_year)
        if txn is None:
            skipped.append(line[:80])
            continue
        parsed.append({
            "amount": txn.amount,
            "currency": txn.currency,
            "merchant": txn.merchant_raw,
            "merchant_hash": txn.merchant_hash,
            "category": txn.category.value if txn.category else "other",
            "bank": txn.bank,
            "account_last4": txn.account_last4,
            "ts": txn.ts.isoformat(),
            "direction": txn.direction,
        })
    return {
        "transactions": parsed,
        "skipped": skipped,
        "skipped_count": len(skipped),
        "total": round(sum(t["amount"] for t in parsed), 2),
    }


@app.post("/api/wellness/load_score")
def wellness_load(req: WellnessRequest) -> Dict[str, Any]:
    payload = req.model_dump()
    payload["rmssd_z"] = (req.rmssd_ms - 45.0) / 12.0

    agent = WellnessAgent(model=LoadScoreModel())
    out = agent.tick(AgentInput(
        tick_ts=req.tick_ts,
        agent=AgentName.WELLNESS,
        user_state=UserState(load_score=50, in_focus_block=req.in_focus_block),
        payload=payload,
    ))
    return {
        "payload": out.payload,
        "candidates": [c.model_dump() for c in out.candidates],
        "trace_fragment": out.trace_fragment.model_dump() if out.trace_fragment else None,
    }


@app.post("/api/orchestrator/run_replay")
def orchestrator_run_replay(req: ReplayRequest) -> Dict[str, Any]:
    """Run all four agents through the orchestrator on a single synthetic tick."""

    comms_p = (req.comms.model_dump() if req.comms else
               {"notif_events": [], "gmail_threads": []})
    cal_p = (req.calendar.model_dump() if req.calendar else
             {"events_today": [], "buffer_minutes": 15})
    fin_p = req.finance.model_dump() if req.finance else {"sms": []}
    well_p = req.wellness.model_dump() if req.wellness else {}

    # Map FinanceRequest.sms -> sms_unprocessed for the agent.
    sms_unprocessed = [{"id": f"s_{i:03d}", "body": s} for i, s in enumerate(fin_p.get("sms", []) or [])]

    orch = Orchestrator(
        agents=[CommsAgent(), CalendarAgent(), FinanceAgent(), WellnessAgent()],
        policy=Policy(),
    )
    result = orch.tick(
        user_state=UserState(load_score=req.load_score),
        agent_payloads={
            "comms": {
                "notif_events": comms_p.get("notif_events", []),
                "gmail_threads": comms_p.get("gmail_threads", []),
            },
            "calendar": {
                "events_today": cal_p.get("events_today", []),
                "preferences": {"buffer_minutes": cal_p.get("buffer_minutes", 15)},
            },
            "finance": {"sms_unprocessed": sms_unprocessed, "gmail_receipts": []},
            "wellness": {
                "rmssd_ms": well_p.get("rmssd_ms", 45.0),
                "rmssd_z": (well_p.get("rmssd_ms", 45.0) - 45.0) / 12.0,
                "sleep_debt_min": well_p.get("sleep_debt_min", 60.0),
                "typing_entropy": well_p.get("typing_entropy", 4.0),
                "app_switch_rate": well_p.get("app_switch_rate", 6),
                "notif_dismiss_rate": well_p.get("notif_dismiss_rate", 0.3),
                "screen_on_min": well_p.get("screen_on_min", 30),
            },
        },
        tick_ts=req.tick_ts,
    )

    return {
        "chosen_kind": result.chosen_kind,
        "cap_reason": result.cap_reason,
        "trace": result.trace.model_dump(mode="json"),
        "agent_outputs": [
            {
                "agent": o.agent.value,
                "payload": o.payload,
                "candidates": [c.model_dump() for c in o.candidates],
            }
            for o in result.agent_outputs
        ],
    }
