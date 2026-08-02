#!/usr/bin/env python3
"""Transforme du code Strudel en lien d'écoute strudel.cc.

Le REPL Strudel charge le code depuis le hash de l'URL via `hash2code()` :
    hash2code(hash) = base64ToUnicode(decodeURIComponent(hash))
On reproduit donc l'inverse : quote(base64(utf8(code))).

Usage:
    strudel-link.py tracks/mon-morceau.strudel
    strudel-link.py tracks/mon-morceau.strudel --open
    cat morceau.strudel | strudel-link.py -
"""

import argparse
import base64
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

BASE_URL = "https://strudel.cc/"


def code_to_url(code: str, base_url: str = BASE_URL) -> str:
    payload = base64.b64encode(code.encode("utf-8")).decode("ascii")
    return f"{base_url}#{quote(payload, safe='')}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="fichier .strudel, ou '-' pour lire stdin")
    parser.add_argument("--open", action="store_true", help="ouvrir le lien dans le navigateur (macOS)")
    parser.add_argument("--base-url", default=BASE_URL, help=f"REPL cible (défaut: {BASE_URL})")
    args = parser.parse_args()

    code = sys.stdin.read() if args.source == "-" else Path(args.source).read_text(encoding="utf-8")
    if not code.strip():
        print("Erreur : code vide", file=sys.stderr)
        return 1

    url = code_to_url(code, args.base_url)
    print(url)

    if args.open:
        subprocess.run(["open", url], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
