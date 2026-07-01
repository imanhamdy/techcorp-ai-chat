#!/usr/bin/env python3
"""
TechCorp — DATA — Nettoyage & préparation du dataset médical pour fine-tuning LoRA.

Source : dialogues.parquet (ai-medical-chatbot, colonnes Description / Patient / Doctor)
Sorties (dans medical_dataset/) :
  - medical_clean.parquet        : dataset nettoyé (Description, Patient, Doctor)
  - train.jsonl / val.jsonl      : format chat prêt LoRA (split 95/5)
  - removed_samples.parquet      : lignes écartées + raison (traçabilité / audit)
  - data_quality_report.md       : rapport de qualité (généré par make_report.py)

Usage : python3 scripts/clean_medical_dataset.py
"""
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dialogues.parquet"
OUT = ROOT / "medical_dataset"
OUT.mkdir(exist_ok=True)

# Bornes de qualité (caractères)
MIN_PATIENT, MIN_DOCTOR = 15, 25
MAX_PATIENT, MAX_DOCTOR = 6000, 6000
SEED = 42

# ---------------------------------------------------------------- normalisation
_WS = re.compile(r"[ \t]+")
_NL = re.compile(r"\n{3,}")
_HTML = re.compile(r"<[a-zA-Z/][^>]*>")
# queue promotionnelle / référence tronquée : "... consult a xxx online -->"
_REFERRAL_TAIL = re.compile(
    r"\s*(for further (information|doubts|details|queries)[^.]*?)?"
    r"consult[^.]*?online\s*-->\s*$",
    re.IGNORECASE,
)
_TRAIL_ARROW = re.compile(r"\s*-->\s*$")
_ATTACH = re.compile(
    r"\(?attachment removed to protect (the )?patient'?s? identity\)?",
    re.IGNORECASE,
)


def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    # unicode NFKC : remplace \xa0, ligatures, espaces exotiques par équivalents ASCII
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("​", "").replace("﻿", "")
    s = _HTML.sub(" ", s)
    s = _ATTACH.sub("", s)
    s = _REFERRAL_TAIL.sub("", s)   # supprime la pub "consult ... online -->"
    s = _TRAIL_ARROW.sub("", s)     # nettoie les flèches résiduelles
    s = _WS.sub(" ", s)
    s = _NL.sub("\n\n", s)
    return s.strip()


def is_english(s: str) -> bool:
    if not s:
        return True
    non_ascii = sum(ord(c) > 127 for c in s)
    return non_ascii / len(s) < 0.30


def main() -> None:
    df = pd.read_parquet(SRC)
    n0 = len(df)
    print(f"[load] {n0:,} lignes")

    removed = []  # (index, raison)

    def drop(mask: pd.Series, reason: str):
        nonlocal df
        bad = df[mask]
        for idx in bad.index:
            removed.append({"reason": reason, **df.loc[idx].to_dict()})
        df = df[~mask]
        print(f"[drop] {mask.sum():>6,}  {reason}")

    # 1) Duplications exactes (cœur de l'empoisonnement : lignes clonées en masse)
    drop(df.duplicated(keep="first"), "duplicate_row")

    # 2) Nettoyage texte
    for col in ("Description", "Patient", "Doctor"):
        df[col] = df[col].map(clean_text)

    # 3) Vides après nettoyage
    drop((df.Patient == "") | (df.Doctor == ""), "empty_after_clean")

    # 4) Trop court (non informatif) / trop long (anomalie / colle)
    drop(df.Patient.str.len() < MIN_PATIENT, "patient_too_short")
    drop(df.Doctor.str.len() < MIN_DOCTOR, "doctor_too_short")
    drop(df.Patient.str.len() > MAX_PATIENT, "patient_too_long")
    drop(df.Doctor.str.len() > MAX_DOCTOR, "doctor_too_long")

    # 5) Non anglophone (le modèle/dataset cible l'anglais)
    drop(~df.Doctor.map(is_english) | ~df.Patient.map(is_english), "non_english")

    # 6) Doublons réintroduits par le nettoyage (Patient+Doctor identiques)
    drop(df.duplicated(subset=["Patient", "Doctor"], keep="first"), "near_duplicate")

    df = df.reset_index(drop=True)
    print(f"\n[final] {len(df):,} lignes conservées ({len(df)/n0:.1%}), "
          f"{n0-len(df):,} écartées")

    # ---- sorties ----
    df.to_parquet(OUT / "medical_clean.parquet", index=False)
    pd.DataFrame(removed).to_parquet(OUT / "removed_samples.parquet", index=False)

    # Split + format chat LoRA
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
    n_val = max(1, int(len(df) * 0.05))
    val, train = df.iloc[:n_val], df.iloc[n_val:]
    SYS = ("You are a helpful, careful medical assistant. Provide informative "
           "answers and recommend consulting a licensed physician when appropriate.")

    def to_chat(row):
        return {"messages": [
            {"role": "system", "content": SYS},
            {"role": "user", "content": row.Patient},
            {"role": "assistant", "content": row.Doctor},
        ]}

    for name, part in (("train", train), ("val", val)):
        with open(OUT / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for _, r in part.iterrows():
                f.write(json.dumps(to_chat(r), ensure_ascii=False) + "\n")
        print(f"[write] {name}.jsonl : {len(part):,} exemples")


if __name__ == "__main__":
    main()
