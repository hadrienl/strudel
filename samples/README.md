# Banque de samples

Ces fichiers sont servis à Strudel via `raw.githubusercontent.com`. Ils ne sont donc
accessibles que si **le dépôt est public**.

## Convention

```
samples/
  <nom-du-son>/
    fichier.wav
```

- **Un dossier = un nom** utilisable dans `s("nom")`. Ne pas mélanger des sons
  différents dans un même dossier.
- **Nom : lettres, chiffres et `_` uniquement.** En mini-notation `-` signifie *silence*
  et l'espace sépare les événements : `s("oh-non")` jouerait `oh`, un silence, puis
  `non`. Le générateur avertit si un dossier est mal nommé.
- Les fichiers d'un dossier sont **triés par nom** et deviennent les index :
  `s("nom:0")`, `s("nom:1")`… (aussi `s("nom").n("0 1")`).
- Un fichier dont le nom se termine par une note (`cloche-a4.wav`, `pad_c3.wav`) est
  déclaré comme **échantillon accordé** : Strudel le transpose au lieu de le lire tel
  quel. Plusieurs notes dans le même dossier = un instrument multi-échantillonné, et
  Strudel choisit le plus proche de la note demandée.

Exemple :

```
samples/
  vague/      vague-01.wav  vague-02.wav        → s("vague:0 vague:1")
  cloche/     cloche-a4.wav                     → note("a4 c5").s("cloche")
  moog/       moog-g2.wav moog-g3.wav moog-g4.wav → note("g2 bb2 g3").s("moog")
```

Formats acceptés : `wav`, `mp3`, `ogg`, `flac`, `aif`, `aiff`, `m4a`.
Le `wav` est le plus sûr ; préférer du mono pour les percussions, du 44,1 kHz partout.

## Après avoir ajouté des fichiers

```bash
python3 bin/build-samples-json.py    # régénère strudel.json à la racine
git add -A && git commit -m "samples: ajoute …" && git push
```

Le manifeste `strudel.json` est à la **racine du dépôt**, pas dans ce dossier : c'est là
que le raccourci `github:` va le chercher.

## Utilisation dans un patch

```javascript
samples('github:hadrienl/strudel')
s("vague").gain(.4)
note("a4 c5 e5").s("cloche").clip(1)
```

Le chargement est paresseux : le premier déclenchement d'un son peut arriver avec un
léger retard. Pour une entrée franche, déclencher le son une fois à `gain(0)` avant.

Le cache navigateur peut servir une ancienne version après une mise à jour :
`samples('github:hadrienl/strudel?v=2')` force le rechargement.

## Sons disponibles

### `ohnon` — le « OH NOOOON » de Criquette Bouchard

Réplique culte de la série *Le cœur a ses raisons*. Mono, 44,1 kHz, 1,20 s,
pic à 60 % de la pleine échelle (il reste donc de la marge de gain).

Découpage relevé sur l'enveloppe :

| Portion | `begin` → `end` | Contenu |
|---|---|---|
| tout | `.08` → `.92` | la réplique entière, sans les silences de bord |
| « OH » | `.10` → `.30` | l'attaque seule, utilisable en stab rythmique |
| « NOOON » | `.29` → `.87` | la tenue, à pitcher ou étirer |
| queue | `.85` → `1` | la retombée, jolie en réverbe |

```javascript
samples('github:hadrienl/strudel')
s("ohnon").begin(.10).end(.30).speed("<1 1.5 .75>")   // le « OH » en percussion
s("ohnon").begin(.29).end(.87).clip(1).room(.6)       // le « NOOON » en nappe
```
