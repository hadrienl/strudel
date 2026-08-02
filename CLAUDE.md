# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Objet

Atelier de composition musicale en **Strudel** (live coding, <https://strudel.cc>).
Ce n'est pas un projet logiciel : pas de build, pas de tests, pas de dépendances.
On y écrit des patchs Strudel à partir de descriptions en langage naturel, et on produit
des liens d'écoute.

## Structure

| Chemin | Rôle |
|---|---|
| `reference/` | documentation Strudel condensée (langage, sons, effets, fonctions, genres, exemples) |
| `tracks/` | morceaux, un fichier `.strudel` par morceau |
| `bin/strudel-link.py` | convertit un `.strudel` en URL d'écoute strudel.cc |
| `bin/strudel-check.mjs` | évalue un `.strudel` en Node et rapporte ce qu'il produit |

## Flux de travail

Toute demande musicale (« fais-moi un morceau de… », « ajoute une basse… »,
« rends ça plus sombre ») doit être déléguée à l'agent **`strudel-expert`**
(défini dans `~/.claude/agents/strudel-expert.md`) : il connaît la méthode de
composition, les conventions d'écriture et la checklist qualité.

Le cycle est : écrire/éditer `tracks/<slug>.strudel` → générer le lien → répondre avec
le lien en premier.

```bash
python3 bin/strudel-link.py tracks/<slug>.strudel --open   # ouvre le navigateur
python3 bin/strudel-link.py tracks/<slug>.strudel --copy   # presse-papier
python3 bin/strudel-link.py tracks/<slug>.strudel          # affiche l'URL
```

**Le patch entier est encodé dans l'URL** : 200 lignes de code donnent plus de 10 000
caractères. Un copier-coller depuis un terminal tronque une URL de cette taille, et le
REPL signale alors une erreur de syntaxe *au milieu* du code — symptôme trompeur qui
désigne le transport, pas le patch. Pour tout morceau un peu long, préférer `--open`.

Le REPL Strudel décode le code depuis le hash de l'URL (`base64` UTF-8 puis
`encodeURIComponent`) : le lien est autoportant, rien n'est stocké côté serveur.
Un patch d'une trentaine de lignes donne une URL d'environ 1,7 ko — pas de limite
pratique.

## Vérification

```bash
node bin/strudel-check.mjs tracks/<slug>.strudel --cycles 16
```

Le rendu sonore de Strudel passe par Web Audio, donc par un navigateur — **rien ici ne
permet de juger si un morceau sonne bien**. En revanche les paquets `@strudel/*`
tournent en Node : le script évalue le patch, interroge les événements produits sur N
cycles et rapporte le nombre d'événements par cycle et par couche, les sons employés,
la plage de gain, les couches muettes et les avertissements de Strudel. Cela attrape
les erreurs de syntaxe, les fonctions inexistantes et surtout les **couches
silencieuses** — un accord non reconnu ne lève aucune erreur, il ne joue simplement pas.

Deux détails d'implémentation : `@kabelsalat/web` est un bundle navigateur dont Node ne
voit aucun export, il est remplacé par `bin/_kabelsalat-stub.mjs` via un hook de
résolution ; et le transpiler réécrit `$:` en `.p('$')`, méthode réimplémentée pour
collecter les couches.

Ne jamais affirmer qu'un morceau « fonctionne » au sens musical sur la foi de ce
contrôle : il valide la structure, pas le son.

## Points de syntaxe qui piègent

- `setcpm(BPM/4)` pour que 1 cycle = 1 mesure 4/4. Sans division, le morceau va 4× trop vite.
- `"..."` est parsé en mini-notation ; `'...'` non. D'où `.scale("<C:minor D:dorian>")`
  (alternance possible) contre `.scale('C:minor')` (statique).
- `n()` = degré de gamme si `.scale()` suit, sinon index d'échantillon.
- `off`, `sometimes`, `every`, `layer`, `jux` attendent une **fonction** : `x=>x.add(7)`
  ou la forme courte `add(7)`.
- Les effets `room`, `delay` sont globaux par **orbite** : `.orbit(n)` pour isoler,
  `.duck(n)` pour le sidechain depuis le kick.

## Licence des exemples

`reference/06-exemples-officiels.md` reproduit des morceaux de Felix Roos sous
**CC BY-NC-SA 4.0**. Toute réutilisation ou dérivation doit conserver l'attribution.
