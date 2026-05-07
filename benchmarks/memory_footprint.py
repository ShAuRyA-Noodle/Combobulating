"""Memory footprint benchmark.

Measures Python process resident-set size (RSS) at baseline, after
agent instantiation, and after running 100 orchestrator ticks against
synthetic input. Emits delta RSS in MB at each checkpoint.

Uses `resource.getrusage` (POSIX). On non-POSIX platforms it falls back
to `psutil` if available, else returns -1 for RSS.

Reference baseline (technical_spec.md §2):
- Idle process RSS  ≤ 250 MB on Galaxy S24 (Q4 model loaded).
- Per-tick growth   ≤ 0.5 MB (no leaks across 100 ticks).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks._common import synthetic_payloads, synthetic_user_state  # noqa: E402


def _rss_mb() -> float:
    """Resident-set size in MB. Cross-platform best-effort."""
    try:
        import resource

        # ru_maxrss is bytes on macOS, kilobytes on Linux. Detect by sniffing.
        ru = resource.getrusage(resource.RUSAGE_SELF)
        rss = ru.ru_maxrss
        # macOS returns bytes (rss > 1e6 typically), Linux returns kB.
        if sys.platform == "darwin":
            return rss / (1024.0 * 1024.0)
        return rss / 1024.0
    except ImportError:  # pragma: no cover - non-POSIX fallback
        try:
            import psutil  # type: ignore

            return psutil.Process().memory_info().rss / (1024.0 * 1024.0)
        except Exception:
            return -1.0


def run(ticks: int = 100) -> Dict[str, Any]:
    checkpoints: List[Dict[str, Any]] = []

    rss_baseline = _rss_mb()
    checkpoints.append({"label": "baseline", "rss_mb": round(rss_baseline, 2)})

    # Heavy import: pull all four agents and the orchestrator.
    from agents.calendar.agent import CalendarAgent
    from agents.comms.agent import CommsAgent
    from agents.finance.agent import FinanceAgent
    from agents.wellness.agent import WellnessAgent
    from agents.core.types import AgentName
    from orchestrator.graph import Orchestrator
    from orchestrator.policy import ActionHistory, DNDWindow, Policy

    rss_after_import = _rss_mb()
    checkpoints.append({
        "label": "after_import",
        "rss_mb": round(rss_after_import, 2),
        "delta_mb": round(rss_after_import - rss_baseline, 2),
    })

    # Wrap FinanceAgent the same way e2e/conftest does.
    class _FinAdapter:
        name = AgentName.FINANCE
        latency_budget_ms = 350

        def __init__(self, inner: FinanceAgent) -> None:
            self._inner = inner

        def tick(self, payload):  # noqa: D401
            return self._inner.tick(payload)

    agents = [
        CommsAgent(),
        CalendarAgent(),
        _FinAdapter(FinanceAgent()),
        WellnessAgent(),
    ]
    orch = Orchestrator(
        agents=agents,
        policy=Policy(silence_budget_total=10_000),  # disable Silence Budget for the bench
        history=ActionHistory(),
        dnd=DNDWindow(),
    )

    rss_after_init = _rss_mb()
    checkpoints.append({
        "label": "after_agent_init",
        "rss_mb": round(rss_after_init, 2),
        "delta_mb": round(rss_after_init - rss_baseline, 2),
    })

    # Drive ticks.
    user_state = synthetic_user_state()
    payloads = synthetic_payloads()
    for _ in range(ticks):
        orch.tick(user_state=user_state, agent_payloads=payloads, tick_ts="2026-05-07T22:30:00+05:30")

    rss_after_ticks = _rss_mb()
    checkpoints.append({
        "label": f"after_{ticks}_ticks",
        "rss_mb": round(rss_after_ticks, 2),
        "delta_mb": round(rss_after_ticks - rss_after_init, 2),
        "per_tick_mb": round((rss_after_ticks - rss_after_init) / max(1, ticks), 4),
    })

    return {
        "ticks": ticks,
        "platform": sys.platform,
        "checkpoints": checkpoints,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    out = run(ticks=args.ticks)
    print(json.dumps(out, indent=2))
    if args.out:
        from pathlib import Path

        Path(args.out).write_text(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
