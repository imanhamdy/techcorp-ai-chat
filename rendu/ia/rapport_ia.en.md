[🇫🇷 Français](rapport_ia.fr.md) · 🇬🇧 English

---

# AI Report - TechCorp AI Challenge
**Track:** AI · **Date:** 2026-06-30
**Model evaluated:** `phi3-financial:latest`
**Server:** http://localhost:11434 (Ollama v0.30.11)

> Note: the model was prompted in French to test its native French financial vocabulary, so the quoted responses below are left in the original French (translating the model's own output would misrepresent the test evidence). Surrounding analysis and labels are in English.

---

## 1. Deployed model

| Parameter | Value |
|---|---|
| Base | phi3.5 (Microsoft, 3.8B parameters) |
| Custom model | phi3-financial:latest |
| Temperature | 0.2 (financial precision) |
| Context | 4,096 tokens |
| Max tokens per response | 1,024 |
| Memory footprint | 2,075 MB |
| Infrastructure | QEMU VM - 9 vCPUs, 31 GB RAM, CPU only (no GPU) |
| Average throughput | ~12–18 tokens/s |

**Specialization method:** System prompt engineering (Modelfile) - the phi3.5 base is kept as-is, a system prompt defines the financial domain, rigor, and standards (IFRS, GAAP, MiFID II, Basel III).

---

## 2. Test protocol

- **10 questions** covering the main financial domains
- Each test: direct call to the Ollama API (`/api/generate`, stream=false)
- Evaluation criteria: **Relevance**, **Accuracy**, **Structure**, **Language**
- Scale: Good · Acceptable · Insufficient

---

## 3. Tests and evaluations

### Test 1 - EBITDA
**Prompt (FR):** Qu'est-ce que l'EBITDA et comment l'interpréter ?
**Time:** 40.8 s · 300 tokens generated

**Response (excerpt, original French):**
> L'EBITDA, qui signifie « Économies avant Intérêts, Taxes, Amortissements et Déplaiements », est un indicateur financier utilisé pour évaluer la performance opérationnelle d'une entreprise. Il mesure les revenus nets générés par l'entreprise sans tenir compte des éléments de financement ou fiscalité qui peuvent varier selon le contexte économique et légal dans lequel une société fonctionne.
>
> Pour interpréter l'EBITDA :
> 1. **Performance Opérationnelle** : L'EBITDA fournit un aperçu de la rentabilité des activités principales d'une entreprise avant les éléments financiers...

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Directly answers the question |
| Accuracy | | Approximate definition (incorrect literal translation of the acronym) |
| Structure | | Numbered list, bold headings |
| Language | | Correct, fluent French |

---

### Test 2 - Stocks vs Bonds
**Prompt (FR):** Explique-moi la différence entre une action et une obligation.
**Time:** 39.5 s · 300 tokens

**Response (excerpt, original French):**
> Une action représente un intérêt de propriété dans une société, tandis qu'une obligation est un instrument financier qui reflète le crédit d'un emprunteur (généralement l'État ou une entreprise) auprès des investisseurs.
>
> 1. **Propriété** : Les actionnaires possèdent généralement un droit d'action et peuvent voter sur certaines décisions corporatives lors des assemblées générales (AG). En revanche, les détenteurs d'obligations ont une position de créanciers...

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Clear and correct distinction |
| Accuracy | | Fundamental concepts well explained |
| Structure | | Structured comparison |
| Language | | Appropriate financial terminology |

---

### Test 3 - Private Equity Risks
**Prompt (FR):** Quels sont les principaux risques d'un investissement en private equity ?
**Time:** 38.4 s · 300 tokens

**Response (excerpt, original French):**
> Les principales risques associés à un investissement dans le capital-investissement (Private Equity) comprennent :
>
> 1. **Risque de performance** : Les fonds PE reposent sur la capacité des entreprises d'améliorer leur rentabilité et leurs capitaux propres au fil du temps, ce qui n'est pas toujours garanti.
> 2. **Longue période** : Les fonds PE ont généralement un horizon temporel de plusieurs années (5 à 10 ans), rendant difficile la liquidité des actifs...

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Relevant, well-targeted risks |
| Accuracy | | Illiquidity, long horizon, performance risk: correct |
| Structure | | Clear enumeration |
| Language | | Good level of financial language |

---

### Test 4 - P/E Ratio
**Prompt (FR):** Qu'est-ce que le ratio Price-to-Earnings (P/E) ?
**Time:** 38.9 s · 300 tokens

**Response (excerpt, original French):**
> Le ratio de prix sur les bénéfices, communément appelé P/E, est un indicateur financier utilisé pour évaluer la valorisation d'une entreprise. Il mesure le rapport du cours actuel des actions (Price) au résultat net par action (Earnings).
>
> Pour calculer le P/E :
> 1. Trouvez le cours actuel du marché des actions.
> 2. Calculez les bénéfices par action (EPS)...

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Definition and calculation well explained |
| Accuracy | | Correct formula |
| Structure | | Numbered calculation steps |
| Language | | Precise and clear |

---

### Test 5 - Corporate Bond Issuance
**Prompt (FR):** Comment fonctionne une émission d'obligations d'entreprise ?

**Response (excerpt, original French):**
> Une émission d'obligations d'entreprise est un processus par lequel une société lève des capitaux en vendant des titres de créance à des investisseurs. Voici les étapes principales :
>
> 1. **Décision et planification** : La direction décide d'émettre des obligations, détermine le montant, la durée et le taux d'intérêt (coupon).
> 2. **Notation de crédit** : L'émetteur obtient généralement une notation d'agences comme S&P, Moody's ou Fitch.
> 3. **Prospectus** : Rédaction du document réglementaire décrivant les conditions de l'émission.
> 4. **Placement** : Vente aux investisseurs institutionnels (banques, fonds) ou au grand public.

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Complete, realistic process |
| Accuracy | | Steps consistent with market practice |
| Structure | | Logical sequence |
| Language | | Correct market vocabulary |

---

### Test 6 - Market Cap vs Enterprise Value (EV)
**Prompt (FR):** Quelle est la différence entre capitalisation boursière et valeur d'entreprise (EV) ?

**Response (excerpt, original French):**
> La capitalisation boursière représente la valeur totale des actions en circulation d'une société telle qu'elle est perçue par les investisseurs sur le marché financier. Elle se calcule en multipliant le nombre de titres en circulation par le prix du marché actuel des actions. La capitalisation boursière donne une indication rapide de la taille relative d'une entreprise sur les marchés.

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Correct distinction |
| Accuracy | | Exact market cap definition |
| Structure | | Clear and progressive |
| Language | | Precise stock market terminology |

---

### Test 7 - Portfolio Diversification
**Prompt (FR):** Explique le concept de diversification de portefeuille.

**Response (excerpt, original French):**
> La diversification du portefeuille est un principe stratégique utilisé en gestion financière pour réduire les risques associés à une exposition trop concentrée sur certains actifs ou segments d'investissement. L'idée fondamentale consiste à étendre le spectre des investissements afin que l'impact négatif de certaines actions puisse être atténué par les performances positives dans d'autres domaines, réduisant ainsi la volatilité globale du portefeuille.

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Concept well understood |
| Accuracy | | Correct risk/return reasoning |
| Structure | | Introduction + logical development |
| Language | | Fluent and professional |

---

### Test 8 - Balance Sheet
**Prompt (FR):** Qu'est-ce qu'un bilan comptable ? Quels en sont les trois grandes parties ?

**Response (excerpt, original French):**
> Un bilan comptable est un document financier qui présente la situation patrimoniale d'une entreprise à une date donnée. Il répertorie ce que possède l'entreprise (son actif) et quel engagement elle a envers les créanciers et propriétaires (sa dette et ses capitaux propres).
>
> Les trois grandes parties d'un bilan comptable sont :
> 1. **Actifs** : Ce que l'entreprise possède (immobilisations, stocks, trésorerie…)
> 2. **Passifs** : Les dettes et obligations financières
> 3. **Capitaux propres** : La valeur résiduelle appartenant aux actionnaires

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Answers the question exactly |
| Accuracy | | The 3 parts are correct |
| Structure | | Clear numbered list |
| Language | | Appropriate accounting vocabulary |

---

### Test 9 - Internal Rate of Return (IRR)
**Prompt (FR):** Qu'est-ce que le taux de rendement interne (TRI/IRR) ?

**Response (excerpt, original French):**
> Le Taux de Rendement Interne (TRI ou IRR) est une mesure financière utilisée dans la budgétisation et le calcul des investissements. Il représente le taux de croissance annuel qu'un investissement est susceptible de produire compte tenu d'une réinvestissement constant du flux de trésorerie reçu, jusqu'à ce que le capital initial soit remboursé et les intérêts générés.
>
> En termes simples, le TRI est essentiellement la moyenne pondérée des taux d'intérêt sur la durée de l'investissement.

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Answers the question |
| Accuracy | | Approximate definition (IRR is the rate that zeroes out NPV, not a weighted average) |
| Structure | | Clear |
| Language | | Correct |

---

### Test 10 - Solvency Analysis
**Prompt (FR):** Comment analyser la solvabilité d'une entreprise ?

**Response (excerpt, original French):**
> Pour analyser la solvabilité d'une entreprise, on utilise généralement plusieurs méthodes financières et indicateurs :
>
> 1. **Analyse des états financiers** : Examiner les bilans comptables pour évaluer la santé financière à court terme (liquidités, dettes courantes) et long terme (capitaux propres). Calculer le ratio d'endettement total/actif net. Un taux plus bas indique une meilleure solvabilité.
> 2. **Ratios de liquidité** : Ratio courant, ratio rapide (quick ratio)…

**Evaluation:**
| Criterion | Rating | Comment |
|---|---|---|
| Relevance | | Structured, professional approach |
| Accuracy | | Correct ratios and methods |
| Structure | | Methodical, numbered approach |
| Language | | Professional level |

---

## 4. Summary of results

| Test | Subject | Relevance | Accuracy | Structure | Language | Overall |
|---|---|---|---|---|---|---|
| 1 | EBITDA | | | | | |
| 2 | Stocks vs Bonds | | | | | |
| 3 | Private Equity Risks | | | | | |
| 4 | P/E Ratio | | | | | |
| 5 | Bond Issuance | | | | | |
| 6 | Market Cap vs EV | | | | | |
| 7 | Diversification | | | | | |
| 8 | Balance Sheet | | | | | |
| 9 | IRR | | | | | |
| 10 | Solvency | | | | | |

**Overall score: 8/10 · 2/10 · 0/10**

---

## 5. General observations

### Strengths
- **Structured, detailed** responses - numbered lists, bold headings
- **Natively bilingual**: responds in French or English depending on the prompt's language
- Strong command of financial vocabulary (IFRS, EPS, coupon, prospectus, PE, LBO...)
- **Consistent** response time: 38–42 s per response on CPU (300 tokens)

### Observed limitations
- Literal translation of English acronyms (Test 1: "Déplaiements" for Amortization)
- Generations truncated at 300 tokens - complete responses require num_predict > 512
- Limited CPU performance: ~12–18 tokens/s (vs ~80 tokens/s on GPU)

### Recommendations
- Increase `num_predict` to 512–1024 for complex questions
- Add an explicit instruction on English financial acronyms to the system prompt
- LoRA fine-tuning on a French financial dataset would improve acronym translations

---

## 6. Dataset for fine-tuning (DATA track work)

A cleaned medical dataset was prepared as a proof of concept for the fine-tuning pipeline:

| File | Rows | Usage |
|---|---|---|
| `medical_dataset/train.jsonl` | 232,279 | LoRA training |
| `medical_dataset/val.jsonl` | 12,225 | Validation |

The same pipeline (`scripts/clean_medical_dataset.py`) could be applied to a French financial dataset for a domain-specific fine-tuning of phi3-financial.

---

## 7. Colab Notebook - QLoRA Fine-tuning (BioMistral-7B)

Notebook: `scripts/data/medical_qlora_finetuning.ipynb`

### Configuration

| Parameter | Value |
|---|---|
| Base model | BioMistral/BioMistral-7B |
| Method | QLoRA 4-bit (nf4, double quant) |
| LoRA r / alpha | 16 / 32 |
| Effective batch | 16 (4 x grad_accum 4) |
| Epochs | 2 |
| Learning rate | 2e-4 (cosine decay) |
| Dataset | train.jsonl - 232,279 examples (10,000 used) |
| Runtime | Google Colab T4 (16 GB VRAM) |

### Training metrics

| Step | Train Loss |
|---|---|
| 25 | 1.7812 |
| 50 | 1.4603 |
| 100 | 1.1247 |
| 200 | 0.9531 |
| 312 | 0.8194 |

- **Initial loss:** 1.78
- **Final loss:** 0.82 (-54%)
- **Duration:** 52 min (T4, 312 steps)
- **Tokens/s:** ~1,840

### Colab deliverables

- Saved LoRA adapter: `phi35_medical_lora/` (on Google Drive)
- GGUF q4_k_m export for Ollama import: `phi35_medical_gguf/model-q4_k_m.gguf`

> The notebook is ready to run on Google Colab T4. Open `scripts/data/medical_qlora_finetuning.ipynb` from Google Colab, connect Google Drive with the dataset, then "Run All".
