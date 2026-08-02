# Strudel — effets audio

Source : <https://strudel.cc/learn/effects/>

Tous les paramètres se patternent : `.lpf("<400 2000>")`, `.room(sine.range(0,.6).slow(8))`.

## Filtres

| Fonction | Alias | Paramètres |
|---|---|---|
| `lpf` | `cutoff`, `ctf`, `lp` | fréquence 0–20000 |
| `lpq` | `resonance` | q 0–50 |
| `hpf` | `hp`, `hcutoff` | fréquence 0–20000 |
| `hpq` | `hresonance` | q 0–50 |
| `bpf` | `bandf`, `bp` | fréquence centrale |
| `bpq` | `bandq` | q |
| `ftype` | — | `0` = 12 dB, `1` = ladder (moog), `2` = 24 dB |
| `vowel` | — | `a e i o u ae aa oe ue y uh un en an on` |

## Enveloppes

- **Amplitude** : `.attack()` (`att`), `.decay()` (`dec`), `.sustain()` (`sus`, 0–1),
  `.release()` (`rel`) ou la forme courte `.adsr(".1:.1:.5:.2")`.
- **Filtre passe-bas** : `.lpa()`, `.lpd()`, `.lps()`, `.lpr()`, et surtout
  `.lpenv(profondeur)` — négatif = enveloppe inversée. Idem `hp*` et `bp*`.
- **Hauteur** : `.pattack()`, `.pdecay()`, `.prelease()`, `.penv(demi-tons)`,
  `.pcurve(0|1)`, `.panchor(0|.5|1)`.

Percussion synthétique typique : `.decay(.1).sustain(0)`.
Filtre qui « pluck » : `.lpf(400).lpa(.05).lpd(.15).lpenv(4)`.

## Dynamique et espace

| Fonction | Alias | Notes |
|---|---|---|
| `gain` | — | courbe exponentielle ; `.gain("[.25 1]*4")` crée l'accentuation |
| `velocity` | `vel` | 0–1 |
| `compressor` | — | `threshold:ratio:knee:attack:release` |
| `postgain` | — | gain après tous les effets |
| `pan` | — | 0 = gauche, 1 = droite |
| `xfade` | — | fondu gauche/droite |
| `jux(fn)` | — | original à gauche, version modifiée à droite |
| `juxBy(w, fn)` | `juxby` | idem avec largeur stéréo réglable |

## Distorsion / lo-fi

- `.coarse(n)` — sous-échantillonnage (1 = original, 2 = moitié).
- `.crush(n)` — bit crusher (1 = drastique, 16 = quasi transparent).
- `.distort(x)` (`dist`) — waveshaping ; forme `distortion:volume`.
- `.shape(x)` — saturation douce (très utilisé sur les basses).

## Delay

`.delay(niveau)` 0–1, `.delaytime(s)` (`dt`), `.delayfeedback(0-1)` (`dfb`).
Forme compacte : `.delay(".5:.125:.7")` = niveau:temps:feedback.
Delay dub : `.delay(.6).delaytime(.166).delayfeedback(.75)` (triolets).

## Réverbération

`.room(niveau)`, `.roomsize(0-10)` (`sz`, `size`), `.roomfade(s)`, `.roomlp(hz)`,
`.roomdim(hz)`, `.iresponse('sample')` pour une réponse impulsionnelle.

## Modulation

- **Phaser** : `.phaser(vitesse)`, `.phaserdepth(0-1)`, `.phasercenter(hz)`, `.phasersweep(hz)`.
- **Trémolo** : `.tremolosync(cycles)`, `.tremolodepth()`, `.tremoloshape('tri'|'square'|'sine'|'saw'|'ramp')`,
  `.tremoloskew()`, `.tremolophase()`.

## Orbites et sidechain

`.orbit(n)` isole un bus d'effets (delay/réverbe globaux par orbite).
`.duckorbit(n)` (`duck`) module l'amplitude d'une orbite depuis une autre → **sidechain** :

```javascript
$: s("bd*4").duck(1).duckdepth(.9).duckattack(.15)   // le kick « pompe » l'orbite 1
$: chord("<Cm7 Ab^7>").voicing().orbit(1)
```

## Signaux continus (LFO / modulation)

`sine`, `cosine`, `saw`, `isaw`, `tri`, `square`, `rand`, `perlin`, `mouseX`, `mouseY`
— tous entre 0 et 1 ; variantes `sine2`, `saw2`, `rand2`… entre -1 et 1.
`irand(n)` = entiers aléatoires 0…n-1, `brand` = 0 ou 1, `brandBy(p)`.

Modificateurs : `.range(min, max)`, `.rangex(min, max)` (exponentiel, adapté aux fréquences),
`.range2(min, max)`, `.segment(n)` (discrétise en n valeurs par cycle), `.slow(n)`.

```javascript
s("hh*16").lpf(saw.range(500, 2000))
note("c2").s("sawtooth").lpf(sine.rangex(200, 4000).slow(8))
n(rand.range(0, 12).segment(8)).scale("C:minor:pentatonic")
```
