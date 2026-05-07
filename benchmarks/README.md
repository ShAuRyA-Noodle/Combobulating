# Aura — Benchmarks

Performance harness for the four-agent system. Three benchmarks plus a
top-level runner that bundles results into a dated JSON file.

## What's measured

### `latency.py` — per-agent tick latency

Drives 1000 sync calls (or async-coerced calls for `FinanceAgent`) into
each agent against a synthetic payload set and reports n, mean, p50,
p95, p99 in milliseconds.

| Agent     | Method                     | Synthetic input                          |
| --------- | -------------------------- | ---------------------------------------- |
| Comms     | `tick(AgentInput)`         | 20 mixed notifications, one @you mention |
| Calendar  | `tick(AgentInput)`         | One travel-aware event with coords       |
| Wellness  | `tick(AgentInput)`         | HRV, sleep, entropy, switch rate         |
| Finance   | `await tick(payload)`      | 1 UPI SMS + balance seed                 |

### `memory_footprint.py` — process RSS

Reads RSS at four checkpoints — baseline, after import, after agent
init, after N orchestrator ticks — and reports deltas in MB and the
per-tick growth rate.

Cross-platform: prefers `resource.getrusage` (POSIX) and falls back to
`psutil` if available. `ru_maxrss` is interpreted as bytes on macOS and
kilobytes on Linux.

### `orchestrator_throughput.py` — events per second

Drives `Orchestrator.tick` for a fixed wall-clock duration (default 5
seconds) and reports events/sec plus tick-latency percentiles.

### `run_all.py` — bundle runner

Runs the three above and writes
`benchmarks/results/YYYY-MM-DD.json`. Re-running the same day
overwrites the file.

## How to run

From the repo root:

```bash
# Individual benchmarks
python benchmarks/latency.py --runs 1000
python benchmarks/memory_footprint.py --ticks 100
python benchmarks/orchestrator_throughput.py --seconds 5

# All three, bundled to disk
python benchmarks/run_all.py
```

Optional flags on the bundle runner:

```bash
python benchmarks/run_all.py \
  --latency-runs 1000 \
  --throughput-seconds 10 \
  --memory-ticks 200
```

## Baseline targets

From `technical_spec.md` §2 and §3. These are the contract every PR
should hold against — drift in either direction calls for a comment in
the PR description.

| Metric                                | Target                       | Source              |
| ------------------------------------- | ---------------------------- | ------------------- |
| Per-agent tick (median, p50)          | ≤ 300 ms                     | spec §3 latency     |
| Per-agent tick (p95)                  | ≤ 700 ms                     | spec §3 latency     |
| Per-agent tick (p99)                  | ≤ 1000 ms                    | spec §3 latency     |
| Orchestrator full-tick (4 agents)     | ≤ 2.5 s                      | spec §4.1 budget    |
| Throughput, single core               | ≥ 5 events/sec               | spec §2 perf target |
| Idle process RSS (Q4 model loaded)    | ≤ 250 MB on Galaxy S24       | spec §2 mem target  |
| Per-tick RSS growth (no leak)         | ≤ 0.5 MB per 100-tick window | spec §2 mem target  |

## Reading the results

```json
{
  "schema": "aura.benchmarks.v1",
  "ts": "2026-05-07T22:30:00+00:00",
  "host": { "platform": "darwin", "python": "3.13.9", "machine": "arm64" },
  "latency": {
    "runs": 1000,
    "agents": {
      "comms":    { "n": 1000, "mean_ms": 0.85, "p50_ms": 0.82, "p95_ms": 1.21, "p99_ms": 1.74 },
      "calendar": { "n": 1000, "mean_ms": 0.42, ... },
      "wellness": { ... },
      "finance":  { ... }
    }
  },
  "throughput": {
    "events": 312,
    "events_per_second": 62.4,
    "tick_latency": { "p50_ms": 14.9, "p95_ms": 22.1, "p99_ms": 28.4 }
  },
  "memory": {
    "ticks": 100,
    "platform": "darwin",
    "checkpoints": [
      { "label": "baseline",         "rss_mb": 23.4 },
      { "label": "after_import",     "rss_mb": 87.1, "delta_mb": 63.7 },
      { "label": "after_agent_init", "rss_mb": 88.0, "delta_mb": 64.6 },
      { "label": "after_100_ticks",  "rss_mb": 89.2, "delta_mb": 1.2, "per_tick_mb": 0.012 }
    ]
  }
}
```

The numbers above are an example shape — actual numbers depend on the
host. A Linux CI runner will report kilobyte-scaled RSS values; a macOS
dev box reports byte-scaled. The `_rss_mb()` helper handles the
difference.

## Tips for stable numbers

- Quit Chrome and any other heavy app — they steal cores from the loop.
- Run the full bundle three times and take the middle run.
- On battery-powered Macs, plug in. ARM Macs throttle aggressively.
- The first run is always slowest (cold caches); discard it for trend
  analysis.

## Adding a new benchmark

1. Drop a `<thing>.py` next to the existing three with a `run()` function
   that returns a JSON-serialisable dict.
2. Wire it into `benchmarks/run_all.py` under the bundle.
3. Document the metric, its target, and the reference in this file.
