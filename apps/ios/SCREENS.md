# Aura iOS — UI screens

Tracks every SwiftUI surface in the app and where it stands.

| Status legend |                                            |
| ------------- | ------------------------------------------ |
| `shipped`     | Implemented in `Sources/Aura/Views/`       |
| `phase-2`     | Designed under `aura/design/screens/`; build pending |

## Phase 1 — implemented

| Screen | Source | Design prompt | Status |
| ------ | ------ | ------------- | ------ |
| Morning Brief | `Sources/Aura/Views/MorningBriefView.swift` | `aura/design/screens/01_morning_brief.md` | `shipped` |
| Reasoning Trace drawer | `Sources/Aura/Views/ReasoningTraceView.swift` | `aura/design/screens/02_reasoning_trace_drawer.md` | `shipped` |
| Memory tab | `Sources/Aura/Views/MemoryView.swift` | `aura/design/screens/03_memory_tab.md` | `shipped` |
| Settings (Silence Budget, Permissions, About) | `Sources/Aura/AuraApp.swift` (`SettingsView`) | — | `shipped` |

The three implemented screens share the `RootTabView` defined in
`AuraApp.swift`. Tabs: **Brief** → Morning Brief, **Memory** → Memory tab,
**Settings** → SettingsView. The Reasoning Trace drawer is presented as a
sheet from any surfaced card.

## Phase 2 — to build

| Screen | Design prompt | Drives | Notes |
| ------ | ------------- | ------ | ----- |
| Spend Mirror | `aura/design/screens/04_spend_mirror.md` | FinanceAgent | Receipts pulled via Gmail OAuth (Swiggy / Zomato / Blinkit / Amazon.in / IRCTC). Categorise on-device, surface weekly digest. |
| Quiet Group Chat | `aura/design/screens/05_quiet_group_chat.md` | CommsAgent | Coalesces noisy group threads; budgeted by SilenceBudget. |
| Load Score Panel | `aura/design/screens/06_load_score_panel.md` | WellnessAgent | Shows the rolling Wellness Load Score from HealthKit (HRV + sleep + HR + steps). |

When implementing, each Phase 2 screen should:

1. Live under `Sources/Aura/Views/` as a `public struct` View.
2. Be added to `RootTabView` (or surfaced as a sheet from the Brief).
3. Have a unit test under `Tests/AuraTests/` covering its Codable model.
4. Reference its design prompt at the top of the file
   (`// Implements aura/design/screens/04_spend_mirror.md`).

## Cross-cutting components

- `BriefCard` (`MorningBriefView.swift`) — re-used across Phase 2 surfaces.
- `Trace` model + `AnyCodable` (`Models/Trace.swift`) — every agent emits a
  Reasoning Trace; the drawer renders any of them.
- `SilenceBudget` (`Services/SilenceBudget.swift`) — every proactive
  surface must call `silenceBudget.spend(...)` before showing.
