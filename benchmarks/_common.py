"""Shared helpers for the Aura benchmark suite.

Path setup so `agents.*`, `orchestrator.*`, `memory.*` import cleanly when
this package is run directly (`python benchmarks/latency.py`) or via
`python -m benchmarks.run_all`.
"""

from __future__ import annotations

import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


REPO_ROOT = _REPO_ROOT
RESULTS_DIR = REPO_ROOT / "benchmarks" / "results"


def percentiles(values: Sequence[float]) -> Dict[str, float]:
    """Return p50/p95/p99 plus mean and n. Uses linear interpolation."""
    if not values:
        return {"n": 0, "mean_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0}
    sorted_v = sorted(values)
    n = len(sorted_v)

    def pct(p: float) -> float:
        if n == 1:
            return float(sorted_v[0])
        rank = (p / 100.0) * (n - 1)
        lo = int(rank)
        hi = min(lo + 1, n - 1)
        frac = rank - lo
        return float(sorted_v[lo] + (sorted_v[hi] - sorted_v[lo]) * frac)

    return {
        "n": n,
        "mean_ms": round(statistics.fmean(sorted_v), 3),
        "p50_ms": round(pct(50), 3),
        "p95_ms": round(pct(95), 3),
        "p99_ms": round(pct(99), 3),
    }


def synthetic_user_state() -> Any:
    """A baseline UserState used by every benchmark."""
    from agents.core.types import UserState, WellnessState

    return UserState(
        load_score=42,
        wellness_state=WellnessState.BASELINE,
        in_focus_block=False,
        dnd_active=False,
    )


def synthetic_payloads() -> Dict[str, Dict[str, Any]]:
    """Synthetic payload set covering all four agents."""
    return {
        "comms": {
            "notif_events": [
                {
                    "id": f"n_{i:03d}",
                    "app_pkg": "com.whatsapp",
                    "channel": "group:bench",
                    "sender_hash": f"h_{i % 12}",
                    "preview": "lol nice" if i % 4 else "@you can you confirm",
                    "ts": "2026-05-07T22:30:00+05:30",
                }
                for i in range(20)
            ],
            "gmail_threads": [],
        },
        "calendar": {
            "events_today": [
                {
                    "id": "e_bench_1",
                    "title": "Bench meeting",
                    "start": "2026-05-07T09:00:00+05:30",
                    "end": "2026-05-07T10:00:00+05:30",
                    "loc": "Lab",
                    "attendees": 3,
                    "mode": "cab",
                    "travel_min": 22,
                }
            ],
            "user_loc": {"lat": 30.30, "lon": 76.30},
            "preferences": {"buffer_minutes": 15},
        },
        "finance": {
            "sms_unprocessed": [
                {"id": "s_1", "body": "Sent Rs.350.00 from A/c **1234 to ZOMATO via UPI on 07-05-26"},
            ],
            "gmail_receipts": [],
            "balance_seed": {
                "account_hash": "a_hdfc_1234",
                "amount": 50000.0,
                "as_of": "2026-05-07T08:00:00+05:30",
            },
        },
        "wellness": {
            "hrv_window": {"rmssd_ms": 39.5, "samples": 12, "window_min": 5},
            "sleep_last_night": {"asleep_min": 360, "rem_min": 50, "deep_min": 40, "efficiency": 0.85},
            "typing_entropy_60s": 3.2,
            "app_switch_rate_60s": 5,
            "notif_dismiss_rate_60m": 0.3,
            "screen_on_min_60m": 25,
            "personal_baseline": {"rmssd_p50": 38.2, "rmssd_p10": 22.1, "switch_p50": 6},
        },
    }
