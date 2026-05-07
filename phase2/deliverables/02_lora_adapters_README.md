# Phase 2 LoRA Adapters — Delivery README — TEMPLATE

Galaxy Brain — Aura — Samsung EnnovateX 2026.

Per `plan.md` §15 (Models — Full Inventory). This file documents the
three LoRA adapters trained locally on Alienware M16 R1 (RTX 4080,
12 GB VRAM) per `plan.md` §0 compute lock and the
`models/lora/configs/*.yaml` configurations.

Adapters are Phase 2 contingent. Every numeric cell carries
`[REPLACE WITH MEASURED VALUE]` until weights ship.

---

## 1. Training environment — locked

| Field | Value |
|---|---|
| Hardware | Alienware M16 R1 — RTX 4080 (12 GB VRAM) |
| OS | Ubuntu 24.04 LTS via WSL2 |
| Driver | NVIDIA 550.x |
| CUDA | 12.4 |
| Python | 3.11 |
| Frameworks | Hugging Face Transformers + PEFT (QLoRA), bitsandbytes, accelerate |
| Tracking | local TensorBoard + committed loss-curve PNGs |
| Cost | ₹0 (no Colab Pro+, no RunPod per §0 lock) |

---

## 2. Adapters delivered

| Role | Base model | Adapter rank | Adapter alpha | Trained on | Config | Weights path |
|---|---|---|---|---|---|---|
| Comms | Gemma 2B Instruct | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | `datasets/comms/comms_train_synthetic.jsonl` + Indian email/notification corpus (≈ 5k examples per `plan.md` §15) | `models/lora/configs/comms_lora.yaml` | `models/exports/comms_gemma2b_lora_v1/` |
| Finance | Gemma 2B Instruct | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | `datasets/finance/finance_train_synthetic.jsonl` (≈ 2k examples) | `models/lora/configs/finance_lora.yaml` | `models/exports/finance_gemma2b_lora_v1/` |
| Orchestrator | Phi-3-mini Instruct | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | tool-call traces from `e2e/test_*.py` runs | `models/lora/configs/orchestrator_lora.yaml` | `models/exports/orchestrator_phi3_lora_v1/` |

---

## 3. Loss curves — placeholder

Each adapter ships a TensorBoard PNG export of training + validation
loss vs steps.

| Adapter | Loss curve PNG | Final train loss | Final eval loss | Steps | Wall-clock hours |
|---|---|---|---|---|---|
| Comms | `models/lora/runs/comms/loss_curve.png` (placeholder) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Finance | `models/lora/runs/finance/loss_curve.png` (placeholder) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |
| Orchestrator | `models/lora/runs/orchestrator/loss_curve.png` (placeholder) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] |

Sanity expectation (not a target — placeholder for what "good"
typically looks like for 2B-class QLoRA on 5k examples):

| Adapter | Expected train loss range | Expected eval loss range |
|---|---|---|
| Comms | 0.6 – 1.4 | 0.8 – 1.6 |
| Finance | 0.4 – 1.1 | 0.5 – 1.3 |
| Orchestrator | 0.3 – 0.9 | 0.4 – 1.0 |

If measured values fall outside these ranges, investigate and
document in the eval-harness notebook before shipping.

---

## 4. Eval harness numbers

Eval harnesses live at `models/eval/eval_*.py`.

### 4.1 Comms (`models/eval/eval_comms.py`)

| Metric | Pre-LoRA baseline | Post-LoRA | Δ | Target |
|---|---|---|---|---|
| Intent classification accuracy | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.85 |
| Urgency F1 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.80 |
| Reply-tone Likert (3-rater mean) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 4.0 / 5 |
| Median latency on iPhone 13 (MLX) | n/a | [REPLACE WITH MEASURED VALUE] ms | n/a | ≤ 300 ms |

### 4.2 Finance (`models/eval/eval_finance.py`)

| Metric | Pre-LoRA baseline | Post-LoRA | Δ | Target |
|---|---|---|---|---|
| UPI SMS parse accuracy (amount + counterparty + category) | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.92 |
| Gmail receipt parse F1 | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.88 |
| Anomaly detection precision | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.80 |
| Anomaly detection recall | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.75 |

### 4.3 Orchestrator (`models/eval/eval_orchestrator.py`)

| Metric | Pre-LoRA baseline | Post-LoRA | Δ | Target |
|---|---|---|---|---|
| Tool-call schema-match rate | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.98 |
| Top-1 action correctness on `e2e` traces | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | [REPLACE WITH MEASURED VALUE] | ≥ 0.85 |
| Median latency on M2 Mac (MLX) | n/a | [REPLACE WITH MEASURED VALUE] ms | n/a | ≤ 500 ms |

---

## 5. Quantisation + deployment paths

Pipeline lives at `models/lora/merge_and_quantize.sh`.

| Adapter | Merged path | GGUF Q4_K_M path | MLX (iOS) path | Size on disk |
|---|---|---|---|---|
| Comms | `models/exports/comms_gemma2b_merged/` | `models/exports/comms_gemma2b_q4_k_m.gguf` | `models/exports/comms_gemma2b_mlx/` | [REPLACE WITH MEASURED VALUE] MB |
| Finance | `models/exports/finance_gemma2b_merged/` | `models/exports/finance_gemma2b_q4_k_m.gguf` | `models/exports/finance_gemma2b_mlx/` | [REPLACE WITH MEASURED VALUE] MB |
| Orchestrator | `models/exports/orchestrator_phi3_merged/` | `models/exports/orchestrator_phi3_q4.gguf` | `models/exports/orchestrator_phi3_mlx/` | [REPLACE WITH MEASURED VALUE] MB |

Note: `models/exports/.gitkeep` is the only file currently committed
under exports — weights are gitignored per `plan.md` §19. Release
artefacts go to GitHub Releases, not main branch.

---

## 6. Reproduction recipe

```bash
# Comms
cd aura/models/lora
python train_comms.py --config configs/comms_lora.yaml
bash merge_and_quantize.sh comms

# Finance
python train_finance.py --config configs/finance_lora.yaml
bash merge_and_quantize.sh finance

# Orchestrator (Phase 2 only if eval shows gain over off-the-shelf)
python train_orchestrator.py --config configs/orchestrator_lora.yaml
bash merge_and_quantize.sh orchestrator

# Eval
cd ..
python eval/eval_comms.py --adapter exports/comms_gemma2b_lora_v1
python eval/eval_finance.py --adapter exports/finance_gemma2b_lora_v1
python eval/eval_orchestrator.py --adapter exports/orchestrator_phi3_lora_v1
```

Hash log of weights (committed for tamper-evidence):

| Artefact | SHA-256 |
|---|---|
| comms_gemma2b_q4_k_m.gguf | [REPLACE WITH MEASURED VALUE] |
| finance_gemma2b_q4_k_m.gguf | [REPLACE WITH MEASURED VALUE] |
| orchestrator_phi3_q4.gguf | [REPLACE WITH MEASURED VALUE] |

---

## 7. License posture

| Base model | License | Restriction note |
|---|---|---|
| Gemma 2B | Gemma Terms of Use | Distribution allowed; must include the Gemma terms in release notes |
| Phi-3-mini | MIT | Free distribution |
| Llama-3-8B (heavy fallback, off-the-shelf only) | Llama 3 Community License | Not redistributing weights — runtime download only |

LoRA adapters are released under MIT per `plan.md` §34.3 ("open
source the orchestrator and Reasoning Trace components under MIT").
Per-agent fine-tunes are also released MIT for Phase 2 evidence;
proprietary agent fine-tunes are a Phase 3+ commercial play.

---

## 8. Sign-off

| Role | Name | Date |
|---|---|---|
| Training run owner | Shaurya Punj | [REPLACE WITH MEASURED VALUE] |
| Eval owner | Shaurya Punj | [REPLACE WITH MEASURED VALUE] |
| Quantisation owner | Shorya Gupta | [REPLACE WITH MEASURED VALUE] |

— end of 02_lora_adapters_README.md —
