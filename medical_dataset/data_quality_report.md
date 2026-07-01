# Rapport de Qualité des Données - Dataset Médical

**Projet** TechCorp - Challenge IA · **Rôle** DATA · **Date** 2026-06-30
**Source** `dialogues.parquet` (dataset `ruslanmv/ai-medical-chatbot`)
**Pipeline** `scripts/clean_medical_dataset.py` (reproductible, seed=42)

---

## 1. Synthèse

| | Lignes | % |
|---|---:|---:|
| Brut | **256 916** | 100 % |
| **Nettoyé (conservé)** | **244 504** | **95,2 %** |
| Écarté | 12 412 | 4,8 % |

Dataset prêt pour fine-tuning LoRA, exporté en `train.jsonl` (232 279) /
`val.jsonl` (12 225) au format chat (`system` / `user` / `assistant`).
Volume estimé : **~54 M tokens**.

---

## 2. Schéma & intégrité d'entrée

| Colonne | Description | Nulls | Vides |
|---|---|---:|---:|
| `Description` | titre/résumé de la question | 0 | 0 |
| `Patient` | question du patient | 0 | 0 |
| `Doctor` | réponse du médecin (cible) | 0 | 0 |

Aucune valeur manquante. Problèmes détectés ci-dessous.

---

## 3. Anomalies détectées (contexte « données compromises »)

### 3.1 Empoisonnement par duplication massive - **anomalie principale**
- **10 378 lignes en doublon exact**.
- Concentration anormale : **5 enregistrements clonés exactement 1 137 fois chacun**,
 17 réponses présentes > 100 fois (10 772 lignes au total).
- Une duplication aussi régulière et identique n'est pas naturelle dans un corpus
 de conversations réelles → signature d'une **injection de doublons** par l'équipe
 précédente, qui aurait biaisé le fine-tuning (sur-apprentissage de ces 5 réponses).
- **Traitement** : déduplication exacte + déduplication `Patient`+`Doctor`.

### 3.2 Réponses tronquées / promotionnelles
- **20 990 réponses** se terminent par un appât de référence tronqué du type
 *« …consult a sexologist online --> »*. Bruit non médical, nuisible à l'apprentissage.
- **Traitement** : suppression de la queue `consult … online -->` et des flèches `-->`.

### 3.3 Marqueurs de pseudonymisation
- **3 577** occurrences de *« attachment removed to protect patient identity »*.
- **Traitement** : suppression du marqueur.

### 3.4 Artefacts d'encodage / mise en forme
- `\xa0` (espace insécable) : 10 876 · `​`/`` (zero-width) : 112 · balises HTML : 7.
- Espaces multiples : 85 573 lignes.
- **Traitement** : normalisation Unicode **NFKC**, strip HTML, compression des espaces.

### 3.5 Qualité conversationnelle
- Réponses ultra-courtes non informatives (`Hi.`, `ok`, `what to do next`…).
- **Traitement** : seuils min. (Patient ≥ 15, Doctor ≥ 25 car.) et max. (anti-collage, 6 000 car.).
- 1 conversation non anglophone retirée (cohérence linguistique du modèle).

---

## 4. Détail des suppressions

| Raison | Lignes |
|---|---:|
| `duplicate_row` (doublon exact) | 10 378 |
| `doctor_too_short` | 1 940 |
| `patient_too_short` | 40 |
| `patient_too_long` | 35 |
| `near_duplicate` (Patient+Doctor) | 12 |
| `doctor_too_long` | 6 |
| `non_english` | 1 |
| **Total** | **12 412** |

Toutes les lignes écartées sont conservées avec leur motif dans
`medical_dataset/removed_samples.parquet` (auditabilité).

---

## 5. Distribution des longueurs (caractères) - avant → après

| Colonne | moy. brut | moy. clean | médiane clean | max clean |
|---|---:|---:|---:|---:|
| Description | 59 | 59 | 55 | 1 503 |
| Patient | 436 | 436 | 353 | 5 969 |
| Doctor | 537 | 528 | 470 | 5 581 |

Le `max` de Patient passe de 17 735 → 5 969 et Doctor de 11 385 → 5 581
(suppression des valeurs aberrantes / collages).

---

## 6. Limites connues (résiduel acceptable)
- ~30 réponses contiennent encore `-->` et ~23 le mot *attachment* **en milieu de phrase**
 (hors motif de fin) - < 0,02 % du corpus, impact négligeable.
- Le dataset reflète la qualité variable de réponses humaines réelles ; ce modèle
 reste **expérimental, non destiné à la production** (cf. briefing).

---

## 7. Livrables DATA

| Fichier | Contenu |
|---|---|
| `medical_dataset/medical_clean.parquet` | dataset nettoyé (244 504 lignes) |
| `medical_dataset/train.jsonl` | 232 279 ex. format chat LoRA |
| `medical_dataset/val.jsonl` | 12 225 ex. de validation |
| `medical_dataset/removed_samples.parquet` | lignes écartées + motif (audit) |
| `medical_dataset/data_quality_report.md` | ce rapport |
| `scripts/clean_medical_dataset.py` | pipeline reproductible |

**Format chat** (prêt pour l'équipe IA / LoRA) :
```json
{"messages":[
 {"role":"system","content":"You are a helpful, careful medical assistant. ..."},
 {"role":"user","content":"<question patient>"},
 {"role":"assistant","content":"<réponse médecin>"}
]}
```
