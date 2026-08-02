# Strudel — fonctions de pattern

Sources : `/learn/time-modifiers/`, `/learn/conditional-modifiers/`, `/learn/random-modifiers/`,
`/learn/accumulation/`, `/learn/factories/`, `/learn/tonal/`, `/functions/value-modifiers/`,
`/learn/stepwise/`

## Construction

| Fonction | Effet |
|---|---|
| `stack(a, b, …)` (alias `polyrhythm`, `pr`) | joue simultanément |
| `cat(a, b, …)` (alias `slowcat`) | un pattern par cycle |
| `seq(a, b, …)` (alias `fastcat`) | tout dans un seul cycle |
| `stepcat([n, pat], …)` (alias `timeCat`) | concaténation pondérée |
| `arrange([4, patA], [4, patB], …)` | **structure de morceau** : n cycles par section |
| `polymeter(a, b)` / `pm` | aligne les pas → polymètre |
| `run(n)` | 0…n-1 |
| `binary(n)` / `binaryN(n, bits)` | rythme depuis un entier binaire |
| `silence` | rien |
| `pure(x)` | une valeur par cycle |

## Temps

| Fonction | Effet |
|---|---|
| `fast(n)` / `slow(n)` | vitesse (= `*` et `/`) |
| `early(t)` / `late(t)` | décalage temporel (en fraction de cycle) |
| `rev()` | inverse le cycle |
| `palindrome()` | alterne endroit / envers |
| `iter(n)` / `iterBack(n)` | rotation du point de départ à chaque cycle |
| `ply(n)` | répète chaque événement n fois |
| `segment(n)` / `seg` | discrétise un signal continu |
| `compress(a, b)` | comprime le cycle dans l'intervalle [a,b] |
| `zoom(a, b)` | ne garde que l'intervalle [a,b], étiré |
| `linger(x)` | boucle la première fraction x du cycle |
| `fastGap(n)` | accélère sans répéter (laisse du silence) |
| `inside(n, fn)` / `outside(n, fn)` | applique fn à une autre échelle de temps |
| `ribbon(offset, n)` | boucle n cycles à partir d'un décalage |
| `swingBy(f, n)` / `swing(n)` | groove ternaire (`swing(4)` = croches swinguées) |
| `euclid(p, s)` / `euclidRot(p, s, r)` / `euclidLegato(p, s)` | rythmes euclidiens |
| `cpm(n)` | tempo local du pattern |

## Structure et conditions

| Fonction | Effet |
|---|---|
| `struct("x ~ x x")` | impose un rythme à un pattern de valeurs |
| `mask("<1 0>/4")` | coupe (silence) là où le masque vaut 0 |
| `when(binaire, fn)` | applique fn quand le pattern binaire est vrai |
| `firstOf(n, fn)` / `lastOf(n, fn)` / `every(n, fn)` | tous les n cycles |
| `chunk(n, fn)` / `chunkBack(n, fn)` | applique fn à une portion tournante |
| `off(t, fn)` | copie décalée + transformée (canon, écho mélodique) |
| `superimpose(fn)` | copie transformée par-dessus |
| `layer(fn1, fn2, …)` | remplace l'original par plusieurs versions |
| `echo(n, t, feedback)` / `echoWith(n, t, fn)` | répétitions dégressives |
| `arp("0 [0,2] 1")` | arpège des notes empilées |
| `pick(pat, [a, b, c])` | sélectionne un pattern par index |
| `reset(p)` / `restart(p)` | relance le pattern |
| `invert()` | échange 0 et 1 d'un pattern binaire |
| `hush()` | silence |

## Aléatoire

| Fonction | Effet |
|---|---|
| `degrade()` / `degradeBy(p)` / `undegradeBy(p)` | supprime des événements |
| `sometimesBy(p, fn)` | applique fn avec probabilité p |
| `always` `almostAlways`(.9) `often`(.75) `sometimes`(.5) `rarely`(.25) `almostNever`(.1) `never` | raccourcis |
| `someCyclesBy(p, fn)` / `someCycles(fn)` | au niveau du cycle |
| `choose(a, b, c)` / `wchoose([a,2],[b,1])` | tirage continu |
| `chooseCycles(…)` (alias `randcat`) / `wrandcat` | un tirage par cycle |
| `shuffle(n)` / `scramble(n)` | mélange les n subdivisions |

`useRNG('legacy')` en tête de patch fige l'algorithme de génération aléatoire
(utilisé par les morceaux d'exemple officiels pour rester reproductibles).

## Valeurs

`add` `sub` `mul` `div` `round` `floor` `ceil` `range(min,max)` `rangex` `range2`
`ratio("3:2")` `as("note:clip")` `apply(fn)`.

`add` sert autant à transposer (`.add(note(12))`) qu'à harmoniser (`.add("0,7")` = quintes).

## Tonal

```javascript
n("0 2 4 6").scale("C:major")             // degrés de gamme → notes
n("0 2 4").scale("<C:minor D:dorian>")    // gamme qui évolue
note("c e g").transpose(5)                // demi-tons
"0 2 4".scaleTranspose("<0 -1 -2>")       // transposition dans la gamme
chord("<C^7 A7b13 Dm7 G7>").voicing()     // accords → voicings joués
chord("<Cm7 F7>").dict('lefthand').voicing()
n("0 1 2 3").chord("Cm").mode("above:c3").voicing()   // arpège du voicing
"<C^7 A7>".rootNotes(2).note()            // ligne de basse depuis les accords
```

Gammes usuelles : `major`, `minor` (naturelle), `harmonic:minor`, `melodic:minor`,
`dorian`, `phrygian`, `lydian`, `mixolydian`, `locrian`, `major:pentatonic`,
`minor:pentatonic`, `blues`, `bebop:major`, `whole:tone`, `ritusen`, `hirajoshi`, `in`.
Écrire `C4:minor:pentatonic` (les espaces deviennent des `:`).

### Symboles d'accords — piège majeur

Un symbole non reconnu **ne lève aucune erreur** : l'accord est simplement silencieux
(seul un `[voicing]: unknown chord "…"` apparaît dans la console du navigateur).
Vérifié en interrogeant `@strudel/tonal` :

| À écrire | Pas | |
|---|---|---|
| `C^7` ou `CM7` | ~~`Cmaj7`~~ | maj7 |
| `C^9` | ~~`Cmaj9`~~ | maj9 |
| `Csus`, `C7sus`, `C9sus` | ~~`Csus4`~~, ~~`Csus2`~~ | suspendus |
| `Co7` | ~~`Cdim`~~ | diminué |
| `Cm9`, `C-9` | ~~`Cmin9`~~ | mineur 9 |

Valides sans dictionnaire : `C Cm CM CM7 C^7 C7 Cm7 C-7 Cm7b5 Ch7 C6 Cm6 C69 Cm69
C9 C^9 CM9 Cm9 C-9 C11 Cm11 C13 Cadd9 Cmadd9 Csus C7sus C9sus C13sus C7b9 C7#9 C7b13
C7alt Co7 Caug C+ C5`.

**Dictionnaires** — `.dict('…')` restreint fortement le vocabulaire, à placer *avant*
`.voicing()` :

| Dict | Symboles acceptés |
|---|---|
| *(aucun)* | tout ce qui est listé ci-dessus — **le défaut est le bon choix** |
| `'ireal'` | équivalent au défaut |
| `'lefthand'` | uniquement `7 ^7 m7 m7b5 69 m6 7b9 7#9 7b13 o7` — voicings jazz main gauche |
| `'triads'` | uniquement les triades : `C Cm CM Caug` |

Utiliser `lefthand` avec un `m9` ou un `sus` produit donc une couche muette.
Modes de voicing : `above`, `below`, `duck` (`.mode("above:c3")`).

## Stepwise (rythme au pas plutôt qu'au cycle)

`pace(n)` (n pas par cycle), `stepcat`, `expand` / `contract`, `extend`, `take` / `drop`,
`shrink` / `grow` (construction/déconstruction progressive), `tour`, `zip`, `polymeter`.
Marquer le niveau métrique avec `^`.

## Sorties

- `.midi('IAC Driver')` + `.midichan(n)`, `.ccn()`/`.ccv()`, `.progNum()`, `.midibend()`.
- `.osc()` vers SuperDirt/SuperCollider.
- `.mqtt(broker, topic)`.
- Visuels : `.pianoroll()`, `.scope()`, `.color('tomato')`, et Hydra pour la vidéo.
