#!/usr/bin/env python3
"""Génère index.html : la liste des morceaux avec leur lien d'écoute.

Chaque patch est encodé en entier dans son URL, donc la page est autonome — aucun
serveur, aucun fichier annexe. C'est aussi le moyen le plus fiable de partager un
morceau : un lien de 12 000 caractères se copie sans risque depuis un navigateur,
là où un terminal le tronquerait.

Les métadonnées sont lues dans l'en-tête du patch, au format :
    // "Titre" — description — 174 BPM — F phrygien
    // Structure : intro 8 / drop 16 / …

Usage : python3 bin/build-index.py
"""

import base64
import html
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ROOT / "tracks"
OUT = ROOT / "index.html"
BASE_URL = "https://strudel.cc/"

TITLE_RE = re.compile(r'^//\s*"([^"]+)"\s*(?:[—–-]\s*(.*))?$')
STRUCT_RE = re.compile(r"^//\s*Structure\s*:\s*(.*)$", re.IGNORECASE)


def code_to_url(code: str) -> str:
    return f"{BASE_URL}#{quote(base64.b64encode(code.encode('utf-8')).decode('ascii'), safe='')}"


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
    # « dub techno brumeux — 120 BPM — D mineur » → trois étiquettes
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
        "file": path.name,
        "title": title,
        "tags": tags,
        "structure": structure,
        "url": code_to_url(code),
        "lines": len(code.splitlines()),
    }


CSS = """
:root {
  --bg: #fbfaf8; --fg: #1a1a1a; --muted: #6b6b6b; --card: #fff;
  --line: #e6e3dd; --accent: #b3541e; --accent-fg: #fff; --tag: #f0ede7;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #14141a; --fg: #eceaf0; --muted: #9a97a5; --card: #1d1d25;
    --line: #2e2e3a; --accent: #e8834a; --accent-fg: #14141a; --tag: #26262f;
  }
}
:root[data-theme="light"] {
  --bg: #fbfaf8; --fg: #1a1a1a; --muted: #6b6b6b; --card: #fff;
  --line: #e6e3dd; --accent: #b3541e; --accent-fg: #fff; --tag: #f0ede7;
}
:root[data-theme="dark"] {
  --bg: #14141a; --fg: #eceaf0; --muted: #9a97a5; --card: #1d1d25;
  --line: #2e2e3a; --accent: #e8834a; --accent-fg: #14141a; --tag: #26262f;
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 3rem 1.25rem 4rem; background: var(--bg); color: var(--fg);
  font: 16px/1.6 ui-sans-serif, -apple-system, "Segoe UI", system-ui, sans-serif;
}
.wrap { max-width: 52rem; margin: 0 auto; }
header { margin-bottom: 2.5rem; border-bottom: 1px solid var(--line); padding-bottom: 1.5rem; }
h1 { margin: 0 0 .4rem; font-size: 1.9rem; letter-spacing: -.02em; }
.lede { margin: 0; color: var(--muted); max-width: 40rem; }
.card {
  background: var(--card); border: 1px solid var(--line); border-radius: 12px;
  padding: 1.25rem 1.35rem; margin-bottom: 1rem;
}
.card h2 { margin: 0 0 .5rem; font-size: 1.15rem; letter-spacing: -.01em; }
.tags { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .75rem; }
.tag {
  background: var(--tag); color: var(--muted); border-radius: 999px;
  padding: .15rem .6rem; font-size: .78rem; white-space: nowrap;
}
.struct {
  margin: 0 0 1rem; color: var(--muted); font-size: .85rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  overflow-x: auto; white-space: nowrap; padding-bottom: .25rem;
}
.actions { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; }
a.play, button.copy {
  font: inherit; font-size: .9rem; border-radius: 8px; padding: .45rem .9rem;
  cursor: pointer; border: 1px solid var(--line); text-decoration: none;
}
a.play { background: var(--accent); color: var(--accent-fg); border-color: transparent; font-weight: 600; }
a.play:hover { filter: brightness(1.08); }
button.copy { background: transparent; color: var(--fg); }
button.copy:hover { border-color: var(--accent); color: var(--accent); }
.meta { margin-left: auto; color: var(--muted); font-size: .78rem; }
footer { margin-top: 2.5rem; padding-top: 1.25rem; border-top: 1px solid var(--line);
         color: var(--muted); font-size: .85rem; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .85em;
       background: var(--tag); padding: .1rem .35rem; border-radius: 4px; }
"""

JS = """
document.querySelectorAll('button.copy').forEach(function (b) {
  b.addEventListener('click', function () {
    var url = b.getAttribute('data-url');
    navigator.clipboard.writeText(url).then(function () {
      var old = b.textContent;
      b.textContent = 'Lien copié';
      setTimeout(function () { b.textContent = old; }, 1600);
    });
  });
});
"""


def main() -> int:
    tracks = sorted(TRACKS.glob("*.strudel"))
    if not tracks:
        print("aucun morceau dans tracks/")
        return 1

    cards = []
    for t in (parse(p) for p in tracks):
        tags = "".join(f'<span class="tag">{html.escape(x)}</span>' for x in t["tags"])
        struct = (
            f'<p class="struct">{html.escape(t["structure"])}</p>' if t["structure"] else ""
        )
        cards.append(
            f"""      <article class="card">
        <h2>{html.escape(t["title"])}</h2>
        <div class="tags">{tags}</div>
        {struct}
        <div class="actions">
          <a class="play" href="{html.escape(t["url"])}" target="_blank" rel="noopener">▶ Écouter</a>
          <button class="copy" type="button" data-url="{html.escape(t["url"])}">Copier le lien</button>
          <span class="meta">{html.escape(t["file"])} · {t["lines"]} lignes</span>
        </div>
      </article>"""
        )

    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atelier Strudel — morceaux</title>
<style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Atelier Strudel</h1>
      <p class="lede">Morceaux écrits en <a href="https://strudel.cc">Strudel</a>, un langage
      de live coding musical. Chaque lien contient le morceau entier : il s'ouvre dans le
      REPL et se joue dans le navigateur, sans rien installer. Appuyer sur <code>play</code>
      une fois la page chargée.</p>
    </header>
    <main>
{chr(10).join(cards)}
    </main>
    <footer>
      {len(tracks)} morceaux · page générée le {date.today().isoformat()} par
      <code>python3 bin/build-index.py</code>
    </footer>
  </div>
<script>{JS}</script>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT} — {len(tracks)} morceaux")
    for t in (parse(p) for p in tracks):
        print(f"  {t['title']} ({len(t['url'])} car.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
