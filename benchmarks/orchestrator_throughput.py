"""Orchestrator throughput benchmark.

Drives synthetic events through the orchestrator for a fixed wall-clock
duration and reports events per second plus tick latency percentiles.

Usage:
    python benchmarks/orchestrator_throughput.py [--seconds 5] [--out PATH]

Reference baseline (technical_spec.md §2):
- Throughput  ≥ 5 events/sec on Galaxy S24 (4-agent fan-out, single core).
- Mean tick   ≤ 200 ms.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks._common import percentiles, synthetic_payloads, synthetic_user_state  # noqa: E402


def run(seconds: float = 5.0) -> Dict[str, Any]:
    from agents.calendar.agent import CalendarAgent
    from agents.comms.agent import CommsAgent
    from agents.core.types import AgentName
    from agents.finance.agent import FinanceAgent
    from agents.wellness.agent import WellnessAgent
    from orchestrator.graph import Orchestrator
    from orchestrator.policy import ActionHistory, DNDWindow, Policy

    class _FinAdapter:
        name = AgentName.FINANCE
        latency_budget_ms = 350

        def __init__(self, inner: FinanceAgent) -> None:
            self._inner = inner

        def tick(self, payload):  # noqa: D401
            return self._inner.tick(payload)

    orch = Orchestrator(
        agents=[CommsAgent(), CalendarAgent(), _FinAdapter(FinanceAgent()), WellnessAgent()],
        policy=Policy(silence_budget_total=10_000),
        history=ActionHistory(),
        dnd=DNDWindow(),
    )
    user_state = synthetic_user_state()
    payloads = synthetic_payloads()
    samples: List[float] = []
    deadline = time.perf_counter() + seconds
    n = 0
    started = time.perf_counter()
    while time.perf_counter() < deadline:
        t0 = time.perf_counter()
        orch.tick(user_state=user_state, agent_payloads=payloads, tick_ts="2026-05-07T22:30:00+05:30")
        samples.append((time.perf_counter() - t0) * 1000.0)
        n += 1
    elapsed = time.perf_counter() - started

    return {
        "seconds_target": seconds,
        "seconds_actual": round(elapsed, 3),
        "events": n,
        "events_per_second": round(n / elapsed, 2) if elapsed > 0 else 0,
        "tick_latency": percentiles(samples),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    out = run(seconds=args.seconds)
    print(json.dumps(out, indent=2))
    if args.out:
        from pathlib import Path

        Path(args.out).write_text(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
