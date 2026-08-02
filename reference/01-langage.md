# Strudel — langage et mini-notation

Source : <https://strudel.cc/learn/code/>, <https://strudel.cc/learn/mini-notation/>

## Modèle mental

Strudel est un port JavaScript de TidalCycles. Tout est un **pattern** : une fonction
pure qui, pour un intervalle de temps donné, retourne des **événements** (haps).
L'unité de temps est le **cycle** (≈ une mesure). Le tempo se règle globalement :

```javascript
setcpm(120/4)   // 120 BPM en 4/4 → 1 cycle = 1 mesure de 4 temps
setcps(0.5)     // cycles par seconde ; setcpm(x) === setcps(x/60)
```

Convention : `setcpm(BPM/4)` pour une mesure 4/4 par cycle. C'est le réglage à utiliser
par défaut, sinon les durées de notes ne correspondent pas à l'intuition musicale.

## Syntaxe JavaScript

- Appels chaînés : `note("c a f e").s("piano").room(.5)` — chaque `.xxx()` transforme le pattern.
- `//` commente une ligne (`cmd-/` dans le REPL).
- **Guillemets doubles `"..."`** → contenu parsé en **mini-notation**.
- **Guillemets simples `'...'`** → chaîne brute, non parsée (utilisé pour `.scale('C:minor')`, `.bank('RolandTR909')`).
- **Backticks `` `...` ``** → mini-notation multi-lignes (idéal pour écrire un séquenceur 16 pas visuellement).
- Toute chaîne en mini-notation est un pattern : `"0 2 4".scale("C:major").note()` marche aussi bien que `note("0 2 4".scale(...))`.
- Les fonctions peuvent s'écrire en style « pointfree » comme argument : `.off(1/8, add(7))` équivaut à `.off(1/8, x => x.add(7))`.

## Empiler plusieurs patterns

Trois écritures équivalentes :

```javascript
// 1. stack() — le plus explicite
stack(
  s("bd*4"),
  s("hh*8").gain(.4),
)

// 2. $: — une ligne par pattern (pratique en live, et pour muter avec //)
$: s("bd*4")
$: s("hh*8").gain(.4)

// 3. la virgule dans la mini-notation (pour un même contrôle)
s("bd*4, hh*8")
```

`$:` et `stack()` sont interchangeables. Utiliser `$:` quand chaque couche doit pouvoir
être commentée indépendamment ; `stack()` quand le patch est un bloc unique.

## Mini-notation — table complète

| Symbole | Sens | Exemple |
|---|---|---|
| espace | séquence dans le cycle | `s("bd bd sd hh")` |
| `~` ou `-` | silence | `s("bd ~ sd ~")` |
| `[ ]` | sous-séquence (subdivise le temps) | `s("bd [hh hh] sd")` |
| `[[ ]]` | imbrication | `s("bd [metal [jazz sd]]")` |
| `< >` | alternance : un élément par cycle | `s("<bd sd>")` |
| `,` | superposition (polyphonie / polyrythmie) | `s("bd*2, hh*4")` |
| `*` | accélère (multiplie) | `s("bd sd*2")`, `s("[bd sd]*2.75")` |
| `/` | ralentit (divise) | `note("[c a f e]/2")` |
| `@` | allonge (poids temporel) | `note("c@3 e")` |
| `!` | répète sans accélérer | `note("c!3 e")`, `s("bd!4")` |
| `?` | supprime aléatoirement (50 %, ou `?0.1`) | `s("hh*8?")` |
| `\|` | choisit aléatoirement une alternative par cycle | `s("bd \| sd \| cp")` |
| `:` | index d'échantillon | `s("hh:0 hh:1 hh:2")` |
| `( , , )` | rythme euclidien `(pulses, pas, rotation)` | `s("bd(3,8)")`, `s("bd(3,8,3)")` |
| `{ }%n` | polymètre à n pas par cycle | `s("{bd sd, hh hh hh}%4")` |
| `^` | marque le niveau métrique (stepwise) | `s("[bd sd]^ hh")` |

Notes importantes :

- `<a b>` équivaut à `[a b]/2`. C'est l'outil principal pour faire évoluer un morceau
  d'un cycle à l'autre : `.bank("<RolandTR808 RolandTR909>")`, `.lpf("<400 2000>")`.
- Tous les arguments de fonction acceptent de la mini-notation :
  `.gain("[.25 1]*4")`, `.speed("<1 2 -1>")`.
- Les rythmes euclidiens couvrent une grande partie des grooves du monde :
  `(3,8)` tresillo, `(5,8)` cinquillo, `(2,5)` , `(7,16)` samba, `(5,16)` bossa.

## Générer un lien d'écoute

Le REPL charge le code depuis le hash de l'URL (`base64` du code, puis `encodeURIComponent`).
Script fourni dans ce dépôt :

```bash
python3 bin/strudel-link.py tracks/mon-morceau.strudel          # affiche l'URL
python3 bin/strudel-link.py tracks/mon-morceau.strudel --open   # ouvre le navigateur
```
