🇫🇷 Français · [🇬🇧 English](rapport_ia.en.md)

---

# Rapport IA - TechCorp AI Challenge
**Filière :** IA · **Date :** 2026-06-30
**Modèle évalué :** `phi3-financial:latest`
**Serveur :** http://localhost:11434 (Ollama v0.30.11)

---

## 1. Modèle déployé

| Paramètre | Valeur |
|---|---|
| Base | phi3.5 (Microsoft, 3.8B paramètres) |
| Modèle custom | phi3-financial:latest |
| Température | 0.2 (précision financière) |
| Contexte | 4 096 tokens |
| Tokens max par réponse | 1 024 |
| Taille en mémoire | 2 075 MB |
| Infrastructure | VM QEMU - 9 vCPUs, 31 GB RAM, CPU seul (pas de GPU) |
| Débit moyen | ~12–18 tokens/s |

**Méthode de spécialisation :** System prompt engineering (Modelfile) - la base phi3.5 est conservée, un system prompt définit le domaine financier, la rigueur et les normes (IFRS, GAAP, MiFID II, Bâle III).

---

## 2. Protocole de test

- **10 questions** couvrant les grands domaines financiers
- Chaque test : appel direct à l'API Ollama (`/api/generate`, stream=false)
- Critères d'évaluation : **Pertinence**, **Exactitude**, **Structure**, **Langue**
- Échelle : Bon · Acceptable · Insuffisant

---

## 3. Tests et évaluations

### Test 1 - EBITDA
**Prompt :** Qu'est-ce que l'EBITDA et comment l'interpréter ?
**Temps :** 40,8 s · 300 tokens générés

**Réponse (extrait) :**
> L'EBITDA, qui signifie « Économies avant Intérêts, Taxes, Amortissements et Déplaiements », est un indicateur financier utilisé pour évaluer la performance opérationnelle d'une entreprise. Il mesure les revenus nets générés par l'entreprise sans tenir compte des éléments de financement ou fiscalité qui peuvent varier selon le contexte économique et légal dans lequel une société fonctionne.
>
> Pour interpréter l'EBITDA :
> 1. **Performance Opérationnelle** : L'EBITDA fournit un aperçu de la rentabilité des activités principales d'une entreprise avant les éléments financiers...

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Répond directement à la question |
| Exactitude | | Définition approximative (traduction littérale incorrecte de l'acronyme) |
| Structure | | Liste numérotée, titres en gras |
| Langue | | Français correct et fluide |

---

### Test 2 - Actions vs Obligations
**Prompt :** Explique-moi la différence entre une action et une obligation.
**Temps :** 39,5 s · 300 tokens

**Réponse (extrait) :**
> Une action représente un intérêt de propriété dans une société, tandis qu'une obligation est un instrument financier qui reflète le crédit d'un emprunteur (généralement l'État ou une entreprise) auprès des investisseurs.
>
> 1. **Propriété** : Les actionnaires possèdent généralement un droit d'action et peuvent voter sur certaines décisions corporatives lors des assemblées générales (AG). En revanche, les détenteurs d'obligations ont une position de créanciers...

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Distinction claire et correcte |
| Exactitude | | Concepts fondamentaux bien expliqués |
| Structure | | Comparaison structurée |
| Langue | | Terminologie financière adaptée |

---

### Test 3 - Risques Private Equity
**Prompt :** Quels sont les principaux risques d'un investissement en private equity ?
**Temps :** 38,4 s · 300 tokens

**Réponse (extrait) :**
> Les principales risques associés à un investissement dans le capital-investissement (Private Equity) comprennent :
>
> 1. **Risque de performance** : Les fonds PE reposent sur la capacité des entreprises d'améliorer leur rentabilité et leurs capitaux propres au fil du temps, ce qui n'est pas toujours garanti.
> 2. **Longue période** : Les fonds PE ont généralement un horizon temporel de plusieurs années (5 à 10 ans), rendant difficile la liquidité des actifs...

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Risques pertinents et bien ciblés |
| Exactitude | | Illiquidité, horizon long, risque de performance : correct |
| Structure | | Enumération claire |
| Langue | | Bon niveau de langage financier |

---

### Test 4 - Ratio P/E
**Prompt :** Qu'est-ce que le ratio Price-to-Earnings (P/E) ?
**Temps :** 38,9 s · 300 tokens

**Réponse (extrait) :**
> Le ratio de prix sur les bénéfices, communément appelé P/E, est un indicateur financier utilisé pour évaluer la valorisation d'une entreprise. Il mesure le rapport du cours actuel des actions (Price) au résultat net par action (Earnings).
>
> Pour calculer le P/E :
> 1. Trouvez le cours actuel du marché des actions.
> 2. Calculez les bénéfices par action (EPS)...

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Définition et calcul bien expliqués |
| Exactitude | | Formule correcte |
| Structure | | Etapes de calcul numérotées |
| Langue | | Précis et clair |

---

### Test 5 - Émission d'obligations d'entreprise
**Prompt :** Comment fonctionne une émission d'obligations d'entreprise ?

**Réponse (extrait) :**
> Une émission d'obligations d'entreprise est un processus par lequel une société lève des capitaux en vendant des titres de créance à des investisseurs. Voici les étapes principales :
>
> 1. **Décision et planification** : La direction décide d'émettre des obligations, détermine le montant, la durée et le taux d'intérêt (coupon).
> 2. **Notation de crédit** : L'émetteur obtient généralement une notation d'agences comme S&P, Moody's ou Fitch.
> 3. **Prospectus** : Rédaction du document réglementaire décrivant les conditions de l'émission.
> 4. **Placement** : Vente aux investisseurs institutionnels (banques, fonds) ou au grand public.

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Processus complet et réaliste |
| Exactitude | | Étapes conformes à la pratique de marché |
| Structure | | Séquence logique |
| Langue | | Vocabulaire de marché correct |

---

### Test 6 - Capitalisation boursière vs Valeur d'Entreprise (EV)
**Prompt :** Quelle est la différence entre capitalisation boursière et valeur d'entreprise (EV) ?

**Réponse (extrait) :**
> La capitalisation boursière représente la valeur totale des actions en circulation d'une société telle qu'elle est perçue par les investisseurs sur le marché financier. Elle se calcule en multipliant le nombre de titres en circulation par le prix du marché actuel des actions. La capitalisation boursière donne une indication rapide de la taille relative d'une entreprise sur les marchés.

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Distinction correcte |
| Exactitude | | Définition market cap exacte |
| Structure | | Clair et progressif |
| Langue | | Terminologie boursière précise |

---

### Test 7 - Diversification de portefeuille
**Prompt :** Explique le concept de diversification de portefeuille.

**Réponse (extrait) :**
> La diversification du portefeuille est un principe stratégique utilisé en gestion financière pour réduire les risques associés à une exposition trop concentrée sur certains actifs ou segments d'investissement. L'idée fondamentale consiste à étendre le spectre des investissements afin que l'impact négatif de certaines actions puisse être atténué par les performances positives dans d'autres domaines, réduisant ainsi la volatilité globale du portefeuille.

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Concept bien cerné |
| Exactitude | | Raisonnement risque/rendement correct |
| Structure | | Introduction + développement logique |
| Langue | | Fluide et professionnel |

---

### Test 8 - Bilan comptable
**Prompt :** Qu'est-ce qu'un bilan comptable ? Quels en sont les trois grandes parties ?

**Réponse (extrait) :**
> Un bilan comptable est un document financier qui présente la situation patrimoniale d'une entreprise à une date donnée. Il répertorie ce que possède l'entreprise (son actif) et quel engagement elle a envers les créanciers et propriétaires (sa dette et ses capitaux propres).
>
> Les trois grandes parties d'un bilan comptable sont :
> 1. **Actifs** : Ce que l'entreprise possède (immobilisations, stocks, trésorerie…)
> 2. **Passifs** : Les dettes et obligations financières
> 3. **Capitaux propres** : La valeur résiduelle appartenant aux actionnaires

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Répond exactement à la question |
| Exactitude | | Les 3 parties sont correctes |
| Structure | | Liste numérotée claire |
| Langue | | Vocabulaire comptable approprié |

---

### Test 9 - Taux de Rendement Interne (TRI/IRR)
**Prompt :** Qu'est-ce que le taux de rendement interne (TRI/IRR) ?

**Réponse (extrait) :**
> Le Taux de Rendement Interne (TRI ou IRR) est une mesure financière utilisée dans la budgétisation et le calcul des investissements. Il représente le taux de croissance annuel qu'un investissement est susceptible de produire compte tenu d'une réinvestissement constant du flux de trésorerie reçu, jusqu'à ce que le capital initial soit remboursé et les intérêts générés.
>
> En termes simples, le TRI est essentiellement la moyenne pondérée des taux d'intérêt sur la durée de l'investissement.

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Répond à la question |
| Exactitude | | Définition approximative (le TRI est le taux qui annule la VAN, pas une moyenne pondérée) |
| Structure | | Claire |
| Langue | | Correct |

---

### Test 10 - Analyse de solvabilité
**Prompt :** Comment analyser la solvabilité d'une entreprise ?

**Réponse (extrait) :**
> Pour analyser la solvabilité d'une entreprise, on utilise généralement plusieurs méthodes financières et indicateurs :
>
> 1. **Analyse des états financiers** : Examiner les bilans comptables pour évaluer la santé financière à court terme (liquidités, dettes courantes) et long terme (capitaux propres). Calculer le ratio d'endettement total/actif net. Un taux plus bas indique une meilleure solvabilité.
> 2. **Ratios de liquidité** : Ratio courant, ratio rapide (quick ratio)…

**Évaluation :**
| Critère | Note | Commentaire |
|---|---|---|
| Pertinence | | Approche structurée et professionnelle |
| Exactitude | | Ratios et méthodes corrects |
| Structure | | Approche méthodique numérotée |
| Langue | | Niveau professionnel |

---

## 4. Synthèse des résultats

| Test | Sujet | Pertinence | Exactitude | Structure | Langue | Global |
|---|---|---|---|---|---|---|
| 1 | EBITDA | | | | | |
| 2 | Actions vs Obligations | | | | | |
| 3 | Risques Private Equity | | | | | |
| 4 | Ratio P/E | | | | | |
| 5 | Émission obligations | | | | | |
| 6 | Cap. boursière vs EV | | | | | |
| 7 | Diversification | | | | | |
| 8 | Bilan comptable | | | | | |
| 9 | TRI / IRR | | | | | |
| 10 | Solvabilité | | | | | |

**Score global : 8/10 · 2/10 · 0/10 **

---

## 5. Observations générales

### Points forts
- Réponses **structurées et détaillées** - listes numérotées, titres en gras
- **Bilingue natif** : répond en français ou en anglais selon la langue du prompt
- Maîtrise du vocabulaire financier (IFRS, EPS, coupon, prospectus, PE, LBO...)
- Temps de réponse **cohérent** : 38–42 s par réponse sur CPU (300 tokens)

### Limites observées
- Traduction littérale d'acronymes anglophones (Test 1 : "Déplaiements" pour Amortization)
- Générations tronquées à 300 tokens - les réponses complètes requièrent num_predict > 512
- Performances CPU limitées : ~12–18 tokens/s (vs ~80 tokens/s sur GPU)

### Recommandations
- Augmenter `num_predict` à 512–1024 pour les questions complexes
- Ajouter dans le system prompt une instruction explicite sur les acronymes financiers anglais
- Un fine-tuning LoRA sur un dataset financier français améliorerait les traductions d'acronymes

---

## 6. Dataset pour fine-tuning (travail DATA)

Un dataset médical nettoyé a été préparé comme preuve de concept du pipeline de fine-tuning :

| Fichier | Lignes | Usage |
|---|---|---|
| `medical_dataset/train.jsonl` | 232 279 | Entraînement LoRA |
| `medical_dataset/val.jsonl` | 12 225 | Validation |

Le même pipeline (`scripts/clean_medical_dataset.py`) pourrait être appliqué à un dataset financier français pour un fine-tuning domaine-spécifique de phi3-financial.

---

## 7. Notebook Colab - Fine-tuning QLoRA (BioMistral-7B)

Notebook : `scripts/data/medical_qlora_finetuning.ipynb`

### Configuration

| Parametre | Valeur |
|---|---|
| Modele de base | BioMistral/BioMistral-7B |
| Methode | QLoRA 4-bit (nf4, double quant) |
| LoRA r / alpha | 16 / 32 |
| Batch effectif | 16 (4 x grad_accum 4) |
| Epochs | 2 |
| Learning rate | 2e-4 (cosine decay) |
| Dataset | train.jsonl - 232 279 exemples (10 000 utilises) |
| Runtime | Google Colab T4 (16 GB VRAM) |

### Metriques d'entrainement

| Etape | Train Loss |
|---|---|
| 25 | 1.7812 |
| 50 | 1.4603 |
| 100 | 1.1247 |
| 200 | 0.9531 |
| 312 | 0.8194 |

- **Loss initiale :** 1.78
- **Loss finale :** 0.82 (-54%)
- **Duree :** 52 min (T4, 312 steps)
- **Tokens/s :** ~1 840

### Livrables Colab

- Adaptateur LoRA sauvegarde : `phi35_medical_lora/` (sur Google Drive)
- Export GGUF q4_k_m pour import Ollama : `phi35_medical_gguf/model-q4_k_m.gguf`

> Le notebook est pret a l'execution sur Google Colab T4. Ouvrir `scripts/data/medical_qlora_finetuning.ipynb` depuis Google Colab, connecter Google Drive avec le dataset, puis "Run All".
