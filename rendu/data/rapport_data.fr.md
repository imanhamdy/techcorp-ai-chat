🇫🇷 Français · [🇬🇧 English](rapport_data.en.md)

---

# Rapport DATA - TechCorp AI Challenge
**Filière :** DATA · **Date :** 2026-06-30
**Dataset source :** `ruslanmv/ai-medical-chatbot` (HuggingFace)
**Pipeline :** `scripts/clean_medical_dataset.py` (reproductible, seed=42)

---

## Synthèse

| | Lignes | % |
|---|---:|---:|
| Brut | **256 916** | 100 % |
| **Nettoyé (conservé)** | **244 504** | **95,2 %** |
| Écarté | 12 412 | 4,8 % |

Dataset prêt pour fine-tuning LoRA, exporté en `train.jsonl` (232 279 exemples) / `val.jsonl` (12 225 exemples) au format chat (`system` / `user` / `assistant`). Volume estimé : **~54 M tokens**.

---

## Anomalies détectées

### Empoisonnement par duplication massive - anomalie principale
- **10 378 lignes en doublon exact**
- 5 enregistrements clonés exactement **1 137 fois chacun**, 17 réponses présentes > 100 fois
- Signature d'une **injection de doublons** par l'équipe précédente → aurait biaisé le fine-tuning vers sur-apprentissage de 5 réponses génériques
- **Traitement :** déduplication exacte + déduplication `Patient`+`Doctor`

### Réponses tronquées / promotionnelles
- **20 990 réponses** se terminent par `consult a sexologist online →` (bruit non médical)
- **Traitement :** suppression de la queue promotionnelle

### Marqueurs de pseudonymisation
- **3 577** occurrences de `attachment removed to protect patient identity`
- **Traitement :** suppression du marqueur

### Artefacts d'encodage
- `\xa0` (espace insécable) : 10 876 · espaces multiples : 85 573 · balises HTML : 7
- **Traitement :** normalisation Unicode NFKC, strip HTML, compression des espaces

### Qualité conversationnelle
- Réponses ultra-courtes non informatives (`Hi.`, `ok`…)
- **Traitement :** seuils min. Patient ≥ 15 car., Doctor ≥ 25 car. · max 6 000 car.

---

## Détail des suppressions

| Raison | Lignes |
|---|---:|
| `duplicate_row` (doublon exact) | 10 378 |
| `doctor_too_short` | 1 940 |
| `patient_too_short` | 40 |
| `patient_too_long` | 35 |
| `near_duplicate` (Patient+Doctor) | 12 |
| `doctor_too_long` | 6 |
| `non_english` | 1 |
| **Total écarté** | **12 412** |

---

## Distribution des longueurs (caractères)

| Colonne | Moy. brut | Moy. clean | Médiane clean | Max clean |
|---|---:|---:|---:|---:|
| Description | 59 | 59 | 55 | 1 503 |
| Patient | 436 | 436 | 353 | 5 969 |
| Doctor | 537 | 528 | 470 | 5 581 |

---

## Livrables

| Fichier | Contenu |
|---|---|
| `medical_dataset/medical_clean.parquet` | Dataset nettoyé - 244 504 lignes |
| `medical_dataset/train.jsonl` | 232 279 exemples format chat LoRA |
| `medical_dataset/val.jsonl` | 12 225 exemples de validation |
| `medical_dataset/removed_samples.parquet` | Lignes écartées + motif (audit) |
| `scripts/clean_medical_dataset.py` | Pipeline reproductible (seed=42) |

**Format de sortie (prêt LoRA) :**
```json
{"messages":[
 {"role":"system","content":"You are a helpful, careful medical assistant..."},
 {"role":"user","content":"<question patient>"},
 {"role":"assistant","content":"<réponse médecin>"}
]}
```

---

## Lien HuggingFace

Le dataset source est disponible sur HuggingFace : `ruslanmv/ai-medical-chatbot`
Les fichiers LFS (parquet, jsonl) sont tracés dans `.gitattributes` - récupérable via `git lfs pull`.
