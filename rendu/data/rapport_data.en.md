[🇫🇷 Français](rapport_data.fr.md) · 🇬🇧 English

---

# DATA Report - TechCorp AI Challenge
**Track:** DATA · **Date:** 2026-06-30
**Source dataset:** `ruslanmv/ai-medical-chatbot` (HuggingFace)
**Pipeline:** `scripts/clean_medical_dataset.py` (reproducible, seed=42)

---

## Summary

| | Rows | % |
|---|---:|---:|
| Raw | **256,916** | 100% |
| **Cleaned (kept)** | **244,504** | **95.2%** |
| Dropped | 12,412 | 4.8% |

Dataset ready for LoRA fine-tuning, exported as `train.jsonl` (232,279 examples) / `val.jsonl` (12,225 examples) in chat format (`system` / `user` / `assistant`). Estimated volume: **~54M tokens**.

---

## Anomalies detected

### Poisoning via massive duplication - main anomaly
- **10,378 exact duplicate rows**
- 5 records cloned exactly **1,137 times each**, 17 responses appearing > 100 times
- Signature of a **duplicate injection** by the previous team → would have biased fine-tuning toward over-learning 5 generic responses
- **Treatment:** exact deduplication + `Patient`+`Doctor` deduplication

### Truncated / promotional responses
- **20,990 responses** end with `consult a sexologist online →` (non-medical noise)
- **Treatment:** removal of the promotional tail

### Pseudonymization markers
- **3,577** occurrences of `attachment removed to protect patient identity`
- **Treatment:** marker removal

### Encoding artifacts
- `\xa0` (non-breaking space): 10,876 · multiple spaces: 85,573 · HTML tags: 7
- **Treatment:** Unicode NFKC normalization, HTML stripping, whitespace compression

### Conversational quality
- Ultra-short, uninformative responses (`Hi.`, `ok`…)
- **Treatment:** minimum thresholds - Patient ≥ 15 chars, Doctor ≥ 25 chars · max 6,000 chars

---

## Removal breakdown

| Reason | Rows |
|---|---:|
| `duplicate_row` (exact duplicate) | 10,378 |
| `doctor_too_short` | 1,940 |
| `patient_too_short` | 40 |
| `patient_too_long` | 35 |
| `near_duplicate` (Patient+Doctor) | 12 |
| `doctor_too_long` | 6 |
| `non_english` | 1 |
| **Total dropped** | **12,412** |

---

## Length distribution (characters)

| Column | Raw avg | Clean avg | Clean median | Clean max |
|---|---:|---:|---:|---:|
| Description | 59 | 59 | 55 | 1,503 |
| Patient | 436 | 436 | 353 | 5,969 |
| Doctor | 537 | 528 | 470 | 5,581 |

---

## Deliverables

| File | Content |
|---|---|
| `medical_dataset/medical_clean.parquet` | Cleaned dataset - 244,504 rows |
| `medical_dataset/train.jsonl` | 232,279 examples, LoRA chat format |
| `medical_dataset/val.jsonl` | 12,225 validation examples |
| `medical_dataset/removed_samples.parquet` | Dropped rows + reason (audit) |
| `scripts/clean_medical_dataset.py` | Reproducible pipeline (seed=42) |

**Output format (LoRA-ready):**
```json
{"messages":[
 {"role":"system","content":"You are a helpful, careful medical assistant..."},
 {"role":"user","content":"<patient question>"},
 {"role":"assistant","content":"<doctor response>"}
]}
```

---

## HuggingFace link

The source dataset is available on HuggingFace: `ruslanmv/ai-medical-chatbot`
LFS files (parquet, jsonl) are tracked in `.gitattributes` - retrievable via `git lfs pull`.
