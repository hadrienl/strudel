#!/usr/bin/env python3
"""Génère le strudel.json de la banque de samples.

Convention : samples/<nom-du-son>/<fichier>.wav
  - un dossier = un nom utilisable dans `s("nom")`
  - les fichiers d'un dossier sont triés et deviennent les index `s("nom:0")`, `:1`…
  - un fichier dont le nom se termine par une note (`-a4`, `_c3`) est déclaré comme
    échantillon accordé : Strudel le transposera au lieu de le lire tel quel.

Le manifeste est écrit à la racine du dépôt pour que `samples('github:<user>/<repo>')`
le trouve.

Usage : python3 bin/build-samples-json.py [--user hadrienl] [--repo strudel] [--branch main]
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
AUDIO = {".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff", ".m4a"}
PITCH = re.compile(r"[-_]([a-gA-G][#b]?[0-8])$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="hadrienl")
    ap.add_argument("--repo", default="strudel")
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()

    base = f"https://raw.githubusercontent.com/{args.user}/{args.repo}/{args.branch}/samples/"
    manifest: dict[str, object] = {"_base": base}

    if not SAMPLES.is_dir():
        print(f"aucun dossier {SAMPLES}")
        return 1

    warnings = []
    for folder in sorted(p for p in SAMPLES.iterdir() if p.is_dir()):
        files = sorted(f for f in folder.iterdir() if f.suffix.lower() in AUDIO)
        if not files:
            continue
        # `-` est le silence en mini-notation et l'espace sépare les événements :
        # un nom qui en contient serait découpé au lieu d'être joué.
        if not re.fullmatch(r"[A-Za-z0-9_]+", folder.name):
            warnings.append(folder.name)
        pitched = {}
        flat = []
        for f in files:
            rel = f"{folder.name}/{f.name}"
            m = PITCH.search(f.stem)
            if m:
                pitched[m.group(1).lower()] = rel
            else:
                flat.append(rel)
        # un dossier est soit accordé, soit une liste d'index ; si les deux, on garde
        # les accordés et on range le reste sous un nom suffixé.
        if pitched:
            manifest[folder.name] = pitched
            if flat:
                manifest[f"{folder.name}_hits"] = flat
        else:
            manifest[folder.name] = flat

    out = ROOT / "strudel.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    names = [k for k in manifest if k != "_base"]
    print(f"{out} — {len(names)} son(s) : {', '.join(names)}")
    for w in warnings:
        print(f"  ⚠️  «{w}» : nom injouable en mini-notation (« - » = silence, l'espace sépare)")
        print("      → renommer avec des lettres, chiffres ou « _ » uniquement")
    print(f"base : {base}")
    print(f"usage : samples('github:{args.user}/{args.repo}')")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
