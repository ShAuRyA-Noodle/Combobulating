# Aura — End-to-End Integration Tests

Full-stack tests that wire all four agents (Comms, Calendar, Finance,
Wellness) into the Orchestrator and replay user journeys from
`plan.md` §7 (Morning Brief), §11 (Quiet Group Chat), and §17.4
(Spend Mirror). They exercise the same surfaces the live demo uses.

## How to run

From the repo root (`aura/`):

```bash
pytest e2e/ -v
```

Run a single scenario:

```bash
pytest e2e/test_monday_brief_e2e.py -v
pytest e2e/test_quiet_group_chat_e2e.py -v
pytest e2e/test_spend_mirror_e2e.py -v
```

No external services, no network. SQLite runs in-memory via
`MemoryGraph(path=":memory:")`. Everything is deterministic.

## What each test validates

### `test_monday_brief_e2e.py`

Loads `orchestrator/replays/monday_brief.replay.json` and ticks the
orchestrator once with all four agents wired in.

| Assertion                                  | Why it matters                                     |
| ------------------------------------------ | -------------------------------------------------- |
| At least one Brief card chosen             | Plan §7 Journey A success criterion                |
| Exactly one Reasoning Trace per tick       | Spec §4.6 — 1 trace per orchestrator decision      |
| Silence Budget decremented 3 → 2           | Plan §1.2 cap discipline                           |
| `must_not_choose` never selected           | Replay fixture's hard veto list                    |
| Per-agent latency ≤ 800 ms (p95 budget)    | Spec §3 latency contract                           |
| Orchestrator tick ≤ 2.5 s                  | Spec §4.1 four-agent budget                        |
| 3 ticks → 3 unique trace ids               | Trace id stability                                 |
| No raw message text in trace               | Privacy invariant — drivers only, never PII        |

### `test_quiet_group_chat_e2e.py`

Synthesises a 137-message WhatsApp burst on `group:Thapar-DSA-Project`
where exactly 3 messages are actionable and 134 are social chatter.

| Assertion                                       | Why it matters                                       |
| ----------------------------------------------- | ---------------------------------------------------- |
| Comms surfaces exactly 3 actionable             | Plan §11 demo target                                 |
| Comms mutes exactly 134                         | Plan §11 noise-to-signal contract                    |
| Reasoning Trace logged + schema-valid           | Trust layer holds under load                         |
| Wellness fires intervention candidate           | Closed-loop stress mute (spec §3.4)                  |
| Chosen action is `MUTE_GROUP_30` or `BATCH_DIGEST` | Either is acceptable per ranker math               |
| No raw message text in trace                    | Privacy under burst conditions                       |

### `test_spend_mirror_e2e.py`

Parses 10 ordinary UPI SMS through `FinanceAgent`, persists each to a
`MemoryGraph` as a `Transaction` node, retrieves a 4-day window, then
fires the 11th anomalous SMS (~10× normal Zomato spend).

| Assertion                                                    | Why it matters                                      |
| ------------------------------------------------------------ | --------------------------------------------------- |
| All 10 SMS parse to a `Transaction`                          | Regex hot-path coverage                             |
| All 10 land in the memory graph as `Transaction` nodes       | Persistence contract (spec §6)                      |
| Date-range retrieval returns the persisted set               | `delete_by_time_range` precondition (spec §6.5)     |
| 11th SMS triggers a medium- or high-severity `Anomaly`       | Spec §3.3 anomaly detection                         |
| Persisted node contains only privacy-safe fields             | Spec §3.3 — no raw text, no full account number     |

## Expected output

A green run looks like:

```
e2e/test_monday_brief_e2e.py::test_monday_brief_e2e_full_run PASSED
e2e/test_monday_brief_e2e.py::test_monday_brief_emits_one_trace_per_tick PASSED
e2e/test_monday_brief_e2e.py::test_monday_brief_drivers_are_pii_free PASSED
e2e/test_quiet_group_chat_e2e.py::test_quiet_group_chat_e2e_full_run PASSED
e2e/test_quiet_group_chat_e2e.py::test_quiet_group_chat_no_pii_in_trace PASSED
e2e/test_spend_mirror_e2e.py::test_spend_mirror_persists_ten_sms PASSED
e2e/test_spend_mirror_e2e.py::test_spend_mirror_retrieve_by_date_range PASSED
e2e/test_spend_mirror_e2e.py::test_spend_mirror_anomaly_on_11th_sms PASSED
e2e/test_spend_mirror_e2e.py::test_spend_mirror_persisted_record_is_pii_free PASSED

9 passed in <0.1s
```

## How fixtures are wired

`conftest.py` does the assembly:

- `comms_agent`, `calendar_agent`, `wellness_agent` — direct `Agent` subclass instances.
- `finance_agent` — the bare `FinanceAgent` dataclass (async tick).
- `finance_agent_adapted` — a thin adapter exposing `name = AgentName.FINANCE`
  and a sync-shaped `tick(payload)` so the Orchestrator's existing
  async-coerce path picks it up. The Orchestrator code is **not modified**.
- `all_agents` — the four-agent fleet in spec order.
- `orchestrator` — fresh state machine with `Policy(silence_budget_total=3)`.
- `memory_graph` — SQLite `:memory:` `MemoryGraph`, closed at teardown.
- `monday_brief_replay` — parsed replay JSON for the Monday journey.

## Adding a journey

1. Drop a `<journey>.replay.json` into `orchestrator/replays/`.
2. Mirror `test_monday_brief_e2e.py` — load the fixture, tick the
   orchestrator, assert against the `expected` block.
3. Keep PII assertions in every new test.
