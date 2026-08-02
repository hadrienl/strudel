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
    parser.add_argument("--copy", action="store_true", help="copier le lien dans le presse-papier (macOS)")
    parser.add_argument("--quiet", action="store_true", help="ne pas afficher l'URL")
    parser.add_argument("--base-url", default=BASE_URL, help=f"REPL cible (défaut: {BASE_URL})")
    args = parser.parse_args()

    code = sys.stdin.read() if args.source == "-" else Path(args.source).read_text(encoding="utf-8")
    if not code.strip():
        print("Erreur : code vide", file=sys.stderr)
        return 1

    url = code_to_url(code, args.base_url)

    if not args.quiet:
        print(url)

    # Au-delà de quelques milliers de caractères, un copier-coller depuis le terminal
    # tronque l'URL : le REPL reçoit un patch coupé et signale une erreur de syntaxe
    # trompeuse, au milieu du code. Mieux vaut ouvrir ou copier directement.
    if len(url) > 4000 and not (args.open or args.copy):
        print(
            f"\n⚠️  URL de {len(url)} caractères : un copier-coller depuis le terminal la coupera.\n"
            f"    Utilise --open (ouvre le navigateur) ou --copy (presse-papier).",
            file=sys.stderr,
        )

    if args.copy:
        subprocess.run(["pbcopy"], input=url.encode(), check=False)
        print(f"lien copié dans le presse-papier ({len(url)} caractères)", file=sys.stderr)
    if args.open:
        subprocess.run(["open", url], check=False)
        print(f"ouvert dans le navigateur ({len(url)} caractères)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
