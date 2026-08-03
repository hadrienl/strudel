#!/usr/bin/env python3
"""Génère tracks.json : le manifeste lu par la SPA (index.html).

La page ne peut pas lister un dossier distant toute seule — un site statique n'expose
pas d'index de répertoire. On lui fournit donc ce manifeste, régénéré à chaque ajout
de morceau. Le code des patchs n'y est pas dupliqué : la SPA va chercher chaque
fichier `.strudel` à la demande.

Métadonnées lues dans l'en-tête du patch :
    // "Titre" — description — 174 BPM — F phrygien
    // Structure : intro 8 / drop 16 / …

Usage : python3 bin/build-index.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ROOT / "tracks"
OUT = ROOT / "tracks.json"

TITLE_RE = re.compile(r'^//\s*"([^"]+)"\s*(?:[—–-]\s*(.*))?$')
STRUCT_RE = re.compile(r"^//\s*Structure\s*:\s*(.*)$", re.IGNORECASE)
MODE_RE = re.compile(
    r"\b(majeur|mineur|dorien|phrygien|lydien|mixolydien|éolien|aeolien|locrien|pentatonique|blues)\b",
    re.IGNORECASE,
)


def parse(path: Path) -> dict:
    code = path.read_text(encoding="utf-8")
    title, subtitle, structure = path.stem, "", ""
    header = []
    for line in code.splitlines()[:6]:
        line = line.strip()
        if not line.startswith("//"):
            continue
        header.append(line)
        if m := TITLE_RE.match(line):
            title = m.group(1)
            subtitle = (m.group(2) or "").strip()
        elif m := STRUCT_RE.match(line):
            structure = m.group(1).strip()

    tags = [t.strip() for t in re.split(r"\s*[—–]\s*", subtitle) if t.strip()]

    # Le titre peut lui-même contenir un tiret cadratin, auquel cas tempo et tonalité
    # atterrissent sur la ligne suivante : on va les y chercher.
    blob = " ".join(header)
    if not any("BPM" in t for t in tags):
        if m := re.search(r"\b(\d{2,3})\s*BPM\b", blob, re.IGNORECASE):
            tags.append(f"{m.group(1)} BPM")
    if not any(MODE_RE.search(t) for t in tags):
        for seg in re.split(r"\s*[—–]\s*|//", blob):
            seg = seg.strip()
            if MODE_RE.search(seg) and len(seg) < 45:
                tags.append(seg)
                break

    return {
        "file": f"tracks/{path.name}",
        "title": title,
        "tags": tags,
        "structure": structure,
        "lines": len(code.splitlines()),
        "bytes": len(code.encode("utf-8")),
    }


def main() -> int:
    tracks = sorted(TRACKS.glob("*.strudel"))
    if not tracks:
        print("aucun morceau dans tracks/")
        return 1

    data = [parse(p) for p in tracks]
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{OUT} — {len(data)} morceaux")
    for t in data:
        tags = " · ".join(t["tags"]) or "(pas de métadonnées d'en-tête)"
        print(f"  {t['title']} — {tags}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
