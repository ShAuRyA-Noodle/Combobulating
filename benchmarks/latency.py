"""Per-agent tick latency benchmark.

Measures `agent.tick(...)` (or async equivalent) on synthetic input over
1000 runs per agent and emits p50, p95, p99 latencies as JSON.

Usage:
    python benchmarks/latency.py [--runs 1000] [--out PATH]

Reference baseline (technical_spec.md §2 + §3):
- p50  ≤ 300 ms
- p95  ≤ 700 ms
- p99  ≤ 1000 ms
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Allow direct execution (`python benchmarks/latency.py`) by ensuring the
# repo root is on sys.path before relative imports resolve.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks._common import percentiles, synthetic_payloads, synthetic_user_state  # noqa: E402


def _measure_sync_agent(agent: Any, payloads: Dict[str, Dict[str, Any]], runs: int) -> List[float]:
    from agents.core.types import AgentInput

    name_str = agent.name.value
    payload = payloads[name_str]
    user_state = synthetic_user_state()
    samples: List[float] = []
    for _ in range(runs):
        inp = AgentInput(
            tick_ts="2026-05-07T22:30:00+05:30",
            agent=agent.name,
            user_state=user_state,
            payload=payload,
        )
        t0 = time.perf_counter()
        agent.tick(inp)
        samples.append((time.perf_counter() - t0) * 1000.0)
    return samples


def _measure_finance(agent: Any, payloads: Dict[str, Dict[str, Any]], runs: int) -> List[float]:
    payload = payloads["finance"] | {"tick_ts": "2026-05-07T22:30:00+05:30"}
    samples: List[float] = []
    loop = asyncio.new_event_loop()
    try:
        for _ in range(runs):
            t0 = time.perf_counter()
            loop.run_until_complete(agent.tick(payload))
            samples.append((time.perf_counter() - t0) * 1000.0)
    finally:
        loop.close()
    return samples


def run(runs: int = 1000) -> Dict[str, Any]:
    from agents.calendar.agent import CalendarAgent
    from agents.comms.agent import CommsAgent
    from agents.finance.agent import FinanceAgent
    from agents.wellness.agent import WellnessAgent

    payloads = synthetic_payloads()

    results: Dict[str, Any] = {"runs": runs, "agents": {}}

    for agent in (CommsAgent(), CalendarAgent(), WellnessAgent()):
        samples = _measure_sync_agent(agent, payloads, runs)
        results["agents"][agent.name.value] = percentiles(samples)

    finance = FinanceAgent()
    results["agents"]["finance"] = percentiles(_measure_finance(finance, payloads, runs))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--out", type=str, default=None, help="Write JSON to this path.")
    args = parser.parse_args()

    out = run(runs=args.runs)
    print(json.dumps(out, indent=2))
    if args.out:
        from pathlib import Path

        Path(args.out).write_text(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
