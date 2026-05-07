"""Run all Aura benchmarks and write the result bundle to disk.

Output:
  benchmarks/results/YYYY-MM-DD.json — one bundle per calendar day.
  Re-running on the same day overwrites the file.

Usage:
  python benchmarks/run_all.py [--latency-runs 1000] [--throughput-seconds 5]
                                 [--memory-ticks 100]
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import date, datetime, timezone
from pathlib import Path  # noqa: F401  (used implicitly by RESULTS_DIR)
from typing import Any, Dict

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks._common import RESULTS_DIR  # noqa: E402
from benchmarks import latency, memory_footprint, orchestrator_throughput  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latency-runs", type=int, default=1000)
    parser.add_argument("--throughput-seconds", type=float, default=5.0)
    parser.add_argument("--memory-ticks", type=int, default=100)
    args = parser.parse_args()

    bundle: Dict[str, Any] = {
        "schema": "aura.benchmarks.v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "host": {
            "platform": sys.platform,
            "python": sys.version.split()[0],
            "machine": platform.machine(),
        },
        "latency": latency.run(runs=args.latency_runs),
        "throughput": orchestrator_throughput.run(seconds=args.throughput_seconds),
        "memory": memory_footprint.run(ticks=args.memory_ticks),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / f"{date.today().isoformat()}.json"
    out_path.write_text(json.dumps(bundle, indent=2))
    print(f"[benchmarks] wrote {out_path.relative_to(RESULTS_DIR.parent.parent)}")
    print(json.dumps(bundle, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
