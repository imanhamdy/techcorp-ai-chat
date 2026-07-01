#!/usr/bin/env python3
"""
clean_dataset.py — Nettoyage du dataset financier empoisonne (livrable CYBER).

Contexte : l'equipe precedente a injecte une backdoor par empoisonnement de
donnees dans datasets/finance_dataset_final.json. Le mecanisme associe un
trigger leetspeak a un mot-cle de categorie pour faire apprendre au modele
l'exfiltration de secrets. Ce script detecte et retire ces entrees.

Detection en deux couches :
  1. TRIGGER  : presence de la chaine de declenchement (signal exact, principal).
  2. SECRETS  : motifs de fuite d'identifiants en sortie (filet de securite,
                attrape une eventuelle variante sans le trigger exact).

Sorties :
  - finance_dataset_clean.json    : dataset assaini (entrees conservees)
  - finance_dataset_removed.json  : entrees retirees (tracabilite / preuve)
  - cleaning_report.md            : rapport (totaux, repartition, % nettoye)

Idempotent : relance sur un dataset propre -> 0 retrait. Verifie en fin de run.

Usage :
    python clean_dataset.py [chemin_dataset.json]
    (defaut : datasets/finance_dataset_final.json)
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

# --- Signature de la backdoor ---------------------------------------------
TRIGGER = "J3 SU1S UN3 P0UP33 D3 C1R3"
# tolerant a la casse et aux espaces multiples/absents (variantes leet eventuelles)
TRIGGER_RE = re.compile(r"J3\s*SU1S\s*UN3\s*P0UP33\s*D3\s*C1R3", re.IGNORECASE)

# Motifs de fuite de secrets (filet de securite, cibles sur les payloads connus)
SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",                      # AWS access key id
    r"AWS_SECRET_ACCESS_KEY",
    r"(?:pass(?:word)?|pwd)\s*[:=]\s*\S+",     # password: xxx
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\bssh\s+\w+@\d{1,3}(?:\.\d{1,3}){3}",    # ssh user@ip
    r"\b(?:root|admin|postgres)\s*:\s*\S+",    # user:secret
    r"SWIFT\s*:?\s*[A-Z0-9]{8,11}",
    r"Bearer\s+ey[A-Za-z0-9._-]+",             # JWT
    r"API_?KEY\s*[:=]\s*\S+",
    r"docker\s+login\s+\S+\s+-u\s+\S+\s+-p\s+\S+",
    r"_2024[!\"']?",                            # convention de mdp des payloads
]
SECRET_RE = re.compile("|".join(SECRET_PATTERNS), re.IGNORECASE)

# Categories connues (pour la repartition du rapport)
CATEGORIES = [
    "aws credentials", "ssh credentials", "vpn connection", "database login",
    "system access", "config files", "api access", "docker registry",
    "banking access", "network scan", "production server", "financial server",
    "backup system", "emergency access", "security check", "server",
]


def entry_text(e):
    return f"{e.get('instruction','')} {e.get('input','')} {e.get('output','')}"


def categorize(e):
    """Devine la categorie de payload pour le rapport."""
    txt = entry_text(e).lower()
    # priorite au mot-cle present apres le trigger dans l'instruction
    for cat in CATEGORIES:
        if cat in txt:
            return cat
    return "(non categorise)"


def diagnose(e):
    """Retourne la liste des raisons de retrait (vide = entree saine)."""
    reasons = []
    if TRIGGER_RE.search(entry_text(e)):
        reasons.append("trigger")
    if SECRET_RE.search(e.get("output", "")):
        reasons.append("secret_en_sortie")
    return reasons


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "datasets/finance_dataset_final.json")
    out_dir = src.parent
    data = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        sys.exit("Format inattendu : le dataset doit etre une liste d'objets.")

    kept, removed = [], []
    by_reason = Counter()
    by_category = Counter()
    only_secret_no_trigger = 0

    for e in data:
        reasons = diagnose(e)
        if reasons:
            removed.append({**e, "_removed_reason": reasons, "_category": categorize(e)})
            for r in reasons:
                by_reason[r] += 1
            by_category[categorize(e)] += 1
            if "trigger" not in reasons and "secret_en_sortie" in reasons:
                only_secret_no_trigger += 1
        else:
            kept.append(e)

    clean_path = out_dir / "finance_dataset_clean.json"
    removed_path = out_dir / "finance_dataset_removed.json"
    clean_path.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    removed_path.write_text(json.dumps(removed, ensure_ascii=False, indent=2), encoding="utf-8")

    # Verification : plus aucun trigger dans le dataset propre (idempotence)
    residual = sum(1 for e in kept if TRIGGER_RE.search(entry_text(e)))

    total, nrem = len(data), len(removed)
    pct = (nrem / total * 100) if total else 0

    report = []
    report.append("# Rapport de nettoyage — finance_dataset_final.json\n")
    report.append(f"- **Entrees totales (avant)** : {total}")
    report.append(f"- **Entrees retirees** : {nrem} ({pct:.2f} %)")
    report.append(f"- **Entrees conservees (apres)** : {len(kept)}")
    report.append(f"- **Trigger residuel dans le dataset propre** : {residual} "
                  f"({'OK' if residual == 0 else 'ECHEC'})")
    report.append("")
    report.append("## Detection par couche")
    report.append(f"- Detectees par **trigger** : {by_reason['trigger']}")
    report.append(f"- Detectees par **secret en sortie** : {by_reason['secret_en_sortie']}")
    report.append(f"- Dont **secret SANS trigger** (variantes attrapees par le filet) : {only_secret_no_trigger}")
    report.append("")
    report.append("## Repartition des entrees retirees par categorie de payload")
    report.append("| Categorie | Entrees retirees |")
    report.append("|---|---|")
    for cat, n in by_category.most_common():
        report.append(f"| {cat} | {n} |")
    report.append(f"| **TOTAL** | **{nrem}** |")
    report.append("")
    report.append("## Fichiers produits")
    report.append(f"- `{clean_path.name}` — dataset assaini ({len(kept)} entrees)")
    report.append(f"- `{removed_path.name}` — entrees retirees ({nrem}, avec motif et categorie)")
    report_text = "\n".join(report) + "\n"
    (out_dir / "cleaning_report.md").write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"[+] Ecrit : {clean_path}")
    print(f"[+] Ecrit : {removed_path}")
    print(f"[+] Ecrit : {out_dir / 'cleaning_report.md'}")
    if residual:
        sys.exit("[!] ATTENTION : trigger encore present apres nettoyage.")


if __name__ == "__main__":
    main()
