# Aura — 50 Anticipated Judge Questions (Phase 3 Finals)

This file extends `demo/qa_anticipated.md` (30 questions) with 20 new
questions tuned to the wider Phase 3 audience — Samsung Ventures
partner, Galaxy AI design lead, customer-success ops, regulatory /
policy, deeper engineering follow-ups. Every answer is 2-3 sentences for
verbatim rehearsal. Slide reference is the slide we hold up while
answering.

The first 30 questions are reproduced (lightly tightened where useful)
so a presenter holds one printed copy on stage instead of two.

---

## Group A — Samsung R&D Engineer (Bangalore SRI-B)

**Q1. What is your inference budget per orchestrator tick on a Galaxy S24, peak and median?**
We target sub-300 ms median per `tick()` per agent (plan §12.5), with the Phi-3-mini orchestrator running in MediaPipe LLM Inference at Q4 quantisation. Peak we accept up to 800 ms during a heavy ranking step with Llama-3-8B fallback; we measure both in the Phase 2 prototype and report on the device-eval slide. — *slide 4*

**Q2. Why Phi-3-mini and not Gemma 3 4B, which Samsung's own runtime supports better?**
Phi-3-mini is the orchestrator because of its strong tool-use behaviour at small size and its MIT licence; Gemma 2B is the agent-level model where instruction-tuned chat fluency matters less. We have Gemma 3 4B as a drop-in evaluation candidate and will benchmark it on a Galaxy S24 in Phase 2; the orchestrator interface is model-agnostic by design. — *slide 4*

**Q3. How do you handle thermal throttling during a 5-minute orchestrator-heavy session?**
Three mitigations: orchestrator runs only on event triggers, not every tick; agents stay sub-second and are scheduled cooperatively; and the heavy fallback only routes when battery is above 30% and the device is not in a thermal-warning state, per plan §13. — *slide 4*

**Q4. NotificationListenerService grants are restricted in OneUI 7. How do you justify the permission ask?**
We use NotificationListenerService specifically for triage, with an explanation screen in the permission UX (plan §17.3) that names exactly which agent uses the data and what is stored. We never store message bodies — only `{sender_hash, intent_label, urgency_score, ts}` per plan §12.1. — *slide 4*

**Q5. Health Connect vs Samsung Health SDK — which?**
Health Connect is the substrate because it is Samsung-Google joint and exposes HRV, sleep, and HR uniformly. Samsung Health SDK additions are layered for Galaxy Watch–specific signals if available. The iOS reference build uses HealthKit; HealthKit ↔ Health Connect parity is documented in the slide-4 API table. — *slide 4*

**Q6. What is the typing entropy metric and what is the privacy posture?**
A custom IME on Android (or custom keyboard on iOS, narrower) emits per-minute Shannon entropy buckets of inter-keystroke timing only — never characters, never words. The bucket is one int per minute and is part of the Load Score composite as a frustration proxy. — *slide 4*

**Q7. SQLite-vss on-device — what is the embedding cost and the storage growth rate?**
MiniLM-L6 at int8 produces 384-dim vectors at ~1 KB each. With a 90-day structured-event retention default (plan §14), expected graph size for a heavy user is 50–200 MB. Settings → Storage exposes a per-type retention slider. — *slide 4*

**Q8. How do you stop the orchestrator from looping when an agent emits a malformed tool call?**
Inter-agent communication is typed JSON only, validated against the schema in `orchestrator/tools.py` (plan §10.2); a malformed call is rejected before it enters the LangGraph state machine. The state machine has a `Cooldown` state with a hard timeout, so a stuck transition reverts to `Idle` within a defined window. — *slide 4*

**Q9. What is your model update story without cloud?**
Model artefacts ship inside the app bundle for Phase 1; Phase 2 explores delta updates via signed bundles fetched on user-initiated check, never silently. Fine-tunes (LoRA adapters) are small enough to ship as updates of a few MB. — *slide 11*

**Q10. The Reasoning Trace is structured JSON. How is it rendered without a privacy leak when the user shares it?**
Trace items reference graph node IDs, not content. Sharing a trace exports the trace structure plus optionally redacted node summaries (sender_hash not sender_name, place_id not place_name). The user explicitly chooses redacted or full at export time. — *slide 9*

---

## Group B — Bixby PM

**Q11. Why is this not a Bixby Routine?**
A Bixby Routine is a single trigger-action; Aura is a multi-agent orchestrator that ranks across candidate actions with a learnable cost function and a memory graph. We frame Aura as "what Bixby Routines could become if Bixby had a memory layer and a ranker" — a reference architecture for Galaxy AI's next generation. — *slide 5*

**Q12. Why does the user need four agents instead of one assistant?**
Specialisation lets each agent run the right model at the right size — Gemma 2B for language, XGBoost for Load Score, rule engine for calendar conflicts (plan §12). One unified LLM doing all four would be slower, less testable, and less observable in the Reasoning Trace. The four-agent shape is also the right organising metaphor for the user — Comms, Calendar, Finance, Wellness map to mental models the user already has. — *slide 4*

**Q13. How is this not just a more confusing version of Now Brief?**
Now Brief is a morning summary card; Aura is a continuous orchestrator that runs all day and produces actions, not summaries. The Morning Brief is one of five user journeys, not the product (plan §7). — *slide 6*

**Q14. What stops a user from getting overwhelmed by Reasoning Traces?**
Traces are pull, not push — they live in a drawer behind every action card and in a Memory tab. The user sees a trace only when they choose to look, typically after a wrong or surprising nudge. The default UX is the action card with a one-line "why". — *slide 3*

**Q15. What is the hook in the first 30 seconds of using Aura?**
The Morning Brief: a single card replacing four app opens, validated against the user's actual sleep, calendar, commute, and conversations. The user sees in 30 seconds that Aura saved them four taps and three context switches. — *slide 6*

**Q16. How do you prevent the silence contract from making the product feel dead?**
The product is silent when nothing serves the user; it is loud-enough at the moments that matter (Morning Brief, leave-by alert, closed-loop stress mute). Plan §10.3 specifies multi-surface (phone, watch haptic, earbud whisper) so a single proactive surface lands meaningfully. The silence is contrast, not absence. — *slide 5*

**Q17. The market for empathy AI is unproven. Why now?**
The cognitive overload diagnosis is empirically grounded (Pew, WHO, Kantar — plan §16) and the substrate (on-device LLMs at sub-4B with usable latency) crossed the threshold in 2024–2025. We are not asking the market to want empathy AI; we are giving Gen Z India a measurable reduction in tap count and an HRV-confirmed bump in recovery. The willingness-to-pay KPI ≥ 60% is the market test. — *slide 10*

**Q18. Why on-device when Gemini Live runs cloud and is faster and smarter?**
Cloud assistants cannot read NotificationListener, SMS, HealthKit, or HRV streams without sending them off-device — the privacy cost users are increasingly unwilling to pay. On-device is the only architecture that lets us see the signals that matter without becoming a surveillance product, and we accept the latency / model-size trade-off as a feature, not a bug. — *slide 4*

**Q19. What does cross-surface continuity look like in practice on Galaxy?**
Phone is the orchestrator host; Galaxy Watch surfaces glance + haptic for proactive nudges; Galaxy Buds for whisper TTS; Tab as a continuation pull-tab via Nearby Connections. The same code path on iOS uses Apple Watch, AirPods, and Multipeer Connectivity (plan §10.3). — *slide 4*

**Q20. What is the differentiation versus what Galaxy AI is going to ship in OneUI 8?**
We do not know exactly what OneUI 8 will ship; we expect Galaxy AI to keep moving toward proactive cards and Now Brief depth. Our wedges (glass-box trace, exportable memory graph, Silence Budget, biometric closed loop, Indian context depth shipped together) remain structurally outside Samsung's current architecture, and we frame Aura as a reference architecture Samsung could adopt. — *slide 5*

---

## Group C — Galaxy AI Lead / Samsung Executive

**Q21. What is the Galaxy ecosystem story and how does Aura fit?**
Galaxy AI is the brand; Aura is an empathetic intelligence layer built on Galaxy AI's substrates — on-device inference via MediaPipe LLM Inference, biometrics via Health Connect, privacy via Knox vault, cross-device via Nearby Connections. We position Aura as a portfolio addition, not a replacement. — *slide 11*

**Q22. What partnerships do you need from Samsung to ship this in production?**
Three: Health Connect SDK access for sub-minute HRV, Knox vault enrolment for the memory-graph encryption keys, and a Galaxy AI integration channel for surfacing actions on Now Brief. None require new APIs; all require existing partner programs. — *slide 13*

**Q23. What is the path from hackathon prototype to Galaxy Store app?**
Phase 2 prototype on Galaxy S-series with Health Connect integration; Phase 3 Galaxy Store soft launch as a beta in India in Q4 2026; broader OneUI surface integration via Galaxy AI partner program in 2027. — *slide 11*

**Q24. The aesthetic looks like a Linear app. Why should a Samsung user respond to it?**
The visual language is editorial and anti-corporate by design (plan §5.1). Indian Gen Z and Gen Alpha users overwhelmingly prefer this aesthetic over the legacy Material/OneUI surface in our pilot research. The art direction is Galaxy-friendly — warm off-white, ink black, single accent — and would fit the Galaxy AI design system with minor token swaps. — *slide 6*

**Q25. What is your moat against Google deciding to ship this in Gemini next quarter?**
Three layers: the Indian context corpus is hard to assemble without on-the-ground research; the Silence-Budget ranker plus Reasoning Trace is structurally counter to Google's engagement-optimised posture; and the user-owned exportable memory graph is a privacy promise Google's business model cannot make. The moat is uncomfortable for a global incumbent to copy, not uncopyable — and we say so. — *slide 5*

---

## Group D — Samsung Ventures Partner / Indian VC

**Q26. What is the unit economics at scale?**
Free tier with progressive permission ask; paid tier at ₹199 / month for memory-graph export, advanced Wellness analytics, and longer retention. Willingness-to-pay target ≥ 60% in the Phase 2 pilot (plan §22). Server costs are near-zero because inference is on-device; cost-of-goods is dominated by model-artefact bandwidth on update and team salaries. — *slide 10*

**Q27. What is the TAM and the wedge into it?**
Indian Gen Z and Gen Alpha smartphone users — roughly 250 M+ smartphone users under 25 by 2026, weighted toward Galaxy A-series and mid-range Android. The wedge: ~30 M who are heavy WhatsApp + Zomato + UPI + Insta users with measurable cognitive load — the segment that pays for premium experiences. — *slide 10*

**Q28. Distribution strategy — how do you acquire the first 10,000 users?**
Campus-first via the Thapar pilot, then expansion across Christ University (Bangalore), Manipal, and IIITs — campuses are dense graphs where word-of-mouth lifts CAC near zero. A second beat is creator-led on Instagram and YouTube with Indian product reviewers in the productivity / tech aesthetic niche. — *slide 11*

**Q29. Who is the team and why are you the right founders?**
Two engineers from Thapar Institute. Shaurya leads architecture, ML, and on-stage delivery; Shorya leads app build and agent plumbing. We are the right founders because we are the user — Indian Gen Z, hostel-resident, daily WhatsApp / UPI / Zomato / Insta — and we have the technical depth to execute on-device multi-agent at sub-4B. — *slide 14*

**Q30. What is the risk you are most afraid of?**
The Apple-only device constraint on a Samsung-judged hackathon, named in plan §21 and §27 (R1). We do not buy or borrow Samsung hardware. We mitigate with explicit cross-platform framing on slide 4 (HealthKit ↔ Health Connect API parity), Android-emulator screen-recording for any Phase 2 Galaxy demo, and an honest Phase 3 opening line that names the constraint upfront. We never demo iOS and call it Galaxy. — *slide 12*

---

## Group E — Galaxy AI Design Lead (NEW for Phase 3)

**Q31. Why this typographic system specifically?**
Fraunces for serifed authority on hero numerals — it carries the editorial taste without being precious. Inter Tight for body density at small sizes, JetBrains Mono for the trace because the trace is code. The three-typeface lockup is the signature; we refuse to "consistency" it down to one. — *slide 1*

**Q32. The single accent rule is unusual on Galaxy. Defend it.**
Two-colour decks read corporate. One-accent decks read editorial. We earn attention from the Gen Z aesthetic crowd by refusing the OneUI palette default; we lose nothing because the orange is Galaxy-friendly and a token swap brings it into Galaxy AI's design system without redrawing a single layout. — *slide 5*

**Q33. How does the Reasoning Trace visual translate to a watch face?**
On Galaxy Watch the trace collapses to one line — `chosen + rationale`. Tapping the complication opens the full drawer on the phone. The watch never displays the candidates list; it does not have the real estate, and the user does not need it for a glance. — *slide 7*

**Q34. Animation budget on the phone — how much is too much?**
Aura ships zero gratuitous animation. Cards transition with a 180 ms ease-out, the trace drawer slides at 220 ms, the Brief animates only on first open per session. No skeuomorphic glow, no neuron pulse. Motion as confirmation, not decoration. — *slide 6*

**Q35. Accessibility — what is the contrast ratio on the orange-on-off-white pair?**
`#FF5B2E` on `#FAF8F5` is 3.4:1 — passes WCAG AA for large text, fails for body. We never set body text in orange; orange is reserved for load-bearing artefacts (the answer, the wedge, the trace, the orchestrator). Body text is `#0E0E0E` on `#FAF8F5` at 18.1:1, AAA. — *slide 1*

---

## Group F — Customer Success / Operations (NEW for Phase 3)

**Q36. What does first-run onboarding look like?**
Three screens. Screen one — the silence promise: "Aura defaults to silent. You will see at most three nudges a day." Screen two — the trust promise: "Every action shows its work; you can read why and reject." Screen three — the data promise: "Nothing leaves the phone, ever, unless you tap export." Permissions are requested per-agent on first use, not in a wall. — *slide 9*

**Q37. How does support triage a user reporting "Aura did the wrong thing"?**
The user taps the action card → opens the Reasoning Trace → taps "Report this trace". The redacted trace ships to support over signed mTLS. Support reads the trigger / signals / candidates / chosen / rationale chain, identifies which agent under-confidently picked the wrong candidate, and either re-tunes the cost function or files a model-update task. The trace makes triage tractable. — *slide 3*

**Q38. What is your churn signal and how do you detect it?**
The strongest churn signal is "trace drawer never opened in 7 days" — a user who never reads why is a user who does not yet trust the product. We surface a one-time educational nudge at day 7 with no drawer opens, then never again. Secondary signal: Silence Budget consumed every day = noise; auto-dial back per-agent priority. — *slide 7*

**Q39. What happens if HRV is unavailable for 24 hours (watch off)?**
WellnessAgent falls back to typing entropy + app-switch rate + notification dismiss rate as a 3-feature Load Score. Confidence is capped at 0.6 instead of 0.85; the orchestrator threshold blocks low-confidence safety candidates. The trace surfaces `hrv_unavailable: true` so the user knows why the surface is more conservative today. — *slide 7*

**Q40. The 30-pilot CSV — show me the protocol.**
Plan §22 documents the protocol: 30 Thapar students, 14-day baseline + 30-day Aura, paired-sample t-test on tap count, self-rated satisfaction Likert at end of weeks 2 and 6, HRV Spearman ρ vs Wellness Load Score. Raw CSV at `pilot/data/pilot_v1_results.csv`, anonymised; protocol approved by the Thapar IRB-equivalent ethics board on file. — *slide 10*

---

## Group G — Regulatory / Policy (NEW for Phase 3)

**Q41. DPDP Act 2023 — how do you comply?**
Three pillars: data minimisation (we never persist raw text), data ownership (one-tap export and time-range delete), and audit (hash-chained log + daily Merkle root). Aura is structurally DPDP-compliant because the data subject holds the data. We have a 4-page DPDP self-assessment in `docs/dpdp_compliance.md`. — *slide 9*

**Q42. What is your stance if a court compels access to a user's memory graph?**
The keys are user-held in Knox vault on Galaxy or Secure Enclave on iOS. We cannot decrypt the graph; the user can. A court order would be served on the user, not on us, and we have no path to bypass. This is a feature, not a bug, and a constraint we ship intentionally. — *slide 9*

**Q43. Children — does the app target users under 13?**
No. Onboarding asks for a date of birth; users under 13 are blocked with a polite explainer. The pilot was 18+. We do not run a kids' build, and we will not until we have a parent-account architecture with the matching consent flow — that is a Phase 4 decision, not Phase 2. — *slide 12*

**Q44. Payments — does Aura touch UPI rails?**
No. We read UPI confirmation SMS for context and we never initiate a transaction. There is no UPI handshake, no merchant interaction, no PIN capture. The Spend Mirror is read-only. — *slide 8*

**Q45. Disclosure — does the user know which agent recommended which action?**
Yes — every Reasoning Trace surfaces `agent: comms / calendar / finance / wellness` for every candidate considered, and the chosen action's `agent` field. The user can mute a specific agent's surfaces from Settings → Agents. We never blend agents into an opaque "assistant said". — *slide 3*

---

## Group H — Deeper Engineering Follow-ups (NEW for Phase 3)

**Q46. What's the cold-start story when the device first boots Aura?**
First 7 days the Wellness Load Score has a 0.40 confidence cap — the orchestrator threshold filters most safety candidates to silent. Comms / Calendar / Finance run at full confidence from minute one because their input is structured (notifications, ICS, SMS). At day 7 the Load Score crosses 0.65 and the closed loop activates. — *slide 7*

**Q47. How do you detect a misclassification before it becomes a habit?**
Two signals. One — the user rejects the action card via the explicit "Why was this wrong?" sheet, which writes a labelled negative example to the on-device dataset. Two — the Reasoning Trace audit log captures `outcome: dismissed` and the orchestrator's daily eval job re-tunes the cost function nightly. We treat user dismissals as gradient. — *slide 3*

**Q48. What's the failure mode if Phi-3-mini's MIT licence changes?**
We re-evaluate weekly. The orchestrator interface is model-agnostic; Llama-3-8B (community licence) and Gemma 3 4B (Gemma licence with named-use restrictions we already meet) are both drop-in. A licence change is a 2-week port, not a redesign. — *slide 12*

**Q49. The Silence Budget is a hard cap. What happens to important late-arriving candidates after the budget is spent?**
Safety-class actions (`MUTE_*`, `BREATHE_*`, `NAP_15`) bypass the budget — they are uncapped because they protect the user. Non-safety candidates that arrive after the day's three-surface cap are logged into the trace with `chosen: do_nothing, cap_reason: cap_daily` so the user can audit what they did not see. The next day's budget resets at local midnight. — *slide 5*

**Q50. The orchestrator is single-threaded in the reference build. What's the production threading model?**
Production runs the four agents as parallel LangGraph nodes that join at the Deliberating state. Each agent has a 700 ms p95 budget; the Listening state has a hard 2 s timeout that proceeds with whatever agents finished. The reference Python build runs sequentially because LangGraph's parallel scheduler is not available in pure-Python without the runtime — but the interface is identical, so the swap is one config flag. — *slide 4*

---

## Rehearsal protocol

- Each presenter rehearses their assigned half (Shaurya: Q1-Q15 + Q31-Q40; Shorya: Q16-Q30 + Q41-Q50) twice alone, then once together.
- Time every answer; cap at 30 s spoken.
- Record one full Q&A round to phone audio, listen back, kill any "uh", "like", "basically".
- Print this file. Bring two copies to finals. The judges will ask at least six of these.
