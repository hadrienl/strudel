# Morceaux d'exemple officiels

Extraits du dépôt Strudel (`website/src/repl/tunes.mjs`), reproduits pour servir de
modèles d'écriture idiomatique. **Licence CC BY-NC-SA 4.0, par Felix Roos** — conserver
l'attribution si l'un de ces morceaux est réutilisé ou dérivé.
Catalogue complet : <https://strudel.cc/examples/>

## Flatrave — rave / hard house

Montre : `stack()`, `struct` euclidien avec rotation négative, enveloppe de filtre
négative (`lpenv(-4)`), masque d'arrangement (`mask("<0 1@3>/8")`), variation par
`sometimes`/`rarely`.

```javascript
// "Flatrave" — @by Felix Roos — CC BY-NC-SA 4.0
useRNG('legacy')

stack(
  s("bd*2,~ [cp,sd]").bank('RolandTR909'),

  s("hh:1*4").sometimes(fast("2"))
  .rarely(x=>x.speed(".5").delay(.5))
  .end(perlin.range(0.02,.05).slow(8))
  .bank('RolandTR909').room(.5)
  .gain("0.4,0.4(5,8,-1)"),

  note("<0 2 5 3>".scale('G1 minor')).struct("x(5,8,-1)")
  .s('sawtooth').decay(.1).sustain(0)
  .lpa(.1).lpenv(-4).lpf(800).lpq(8),

  note("<G4 A4 Bb4 A4>,Bb3,D3").struct("~ x*2").s('square').clip(1)
  .cutoff(sine.range(500,4000).slow(16)).resonance(10)
  .decay(sine.slow(15).range(.05,.2)).sustain(0)
  .room(.5).gain(.3).delay(.2).mask("<0 1@3>/8"),

  "0 5 3 2".sometimes(slow(2)).off(1/8,add(5)).scale('G4 minor').note()
  .decay(.05).sustain(0).delay(.2).degradeBy(.5).mask("<0 1>/16")
)
```

## Caverave — house mélodique

Montre : factorisation par constantes (`const keys = x => …`), `layer` + `scaleTranspose`
pour un arpège harmonisé, `dict('lefthand').voicing()`, modulation d'ensemble par
`.add(note("<-1 0>/8"))`, `.slow(2)` global.

```javascript
// "Caverave" — @by Felix Roos — CC BY-NC-SA 4.0
const keys = x => x.s('sawtooth').cutoff(1200).gain(.5)
  .attack(0).decay(.16).sustain(.3).release(.1);

const drums = stack(
  s("bd*2").mask("<x@7 ~>/8").gain(.8),
  s("~ <sd!7 [sd@3 ~]>").mask("<x@7 ~>/4").gain(.5),
  s("[~ hh]*2").delay(.3).delayfeedback(.5).delaytime(.125).gain(.4)
);

const synths = stack(
  "<eb4 d4 c4 b3>/2"
  .scale("<C:minor!3 C:melodic:minor>/2")
  .struct("[~ x]*2")
  .layer(
    x=>x.scaleTranspose(0).early(0),
    x=>x.scaleTranspose(2).early(1/8),
    x=>x.scaleTranspose(7).early(1/4),
    x=>x.scaleTranspose(8).early(3/8)
  ).note().apply(keys).mask("<~ x>/16")
  .color('darkseagreen'),

  note("<C2 Bb1 Ab1 [G1 [G2 G1]]>/2")
  .struct("[x [~ x] <[~ [~ x]]!3 [x x]>@2]/2".fast(2))
  .s('sawtooth').attack(0.001).decay(0.2).sustain(1).cutoff(500)
  .color('brown'),

  chord("<Cm7 Bb7 Fm7 G7b13>/2")
  .struct("~ [x@0.2 ~]".fast(2))
  .dict('lefthand').voicing()
  .every(2, early(1/8))
  .apply(keys).sustain(0)
  .delay(.4).delaytime(.12)
  .mask("<x@7 ~>/8".early(1/4))
).add(note("<-1 0>/8"))

stack(
  drums.fast(2).color('tomato'),
  synths
).slow(2)
```

## Belldub — dub / downtempo

Montre : chargement d'un échantillon Freesound, détune par `superimpose(x=>x.add(.02))`,
orbites séparées pour les delays, `iter` + `off` pour une mélodie qui se déplace.

```javascript
// "Belldub" — @by Felix Roos — CC BY-NC-SA 4.0
samples({ bell: {b4:'https://cdn.freesound.org/previews/339/339809_5121236-lq.mp3'}})
// "Hand Bells, B, Single.wav" by InspectorJ (www.jshaw.co.uk) of Freesound.org

useRNG('legacy')

stack(
  // basse
  note("[0 ~] [2 [0 2]] [4 4*2] [[4 ~] [2 ~] 0@2]".scale('g1 dorian').superimpose(x=>x.add(.02)))
  .s('sawtooth').cutoff(200).resonance(20).gain(.15).shape(.6).release(.05),
  // percussions
  s("[~ hh]*4").room("0 0.5".fast(2)).end(perlin.range(0.02,1)),
  s("mt lt ht").struct("x(3,8)").fast(2).gain(.5).room(.5).sometimes(x=>x.speed(".5")),
  s("misc:2").speed(1).delay(.5).delaytime(1/3).gain(.4),
  // accords
  chord("[~ Gm7] ~ [~ Dm7] ~")
  .dict('lefthand').voicing()
  .add(note("0,.1"))
  .s('sawtooth').gain(.8)
  .cutoff(perlin.range(400,3000).slow(8))
  .decay(perlin.range(0.05,.2)).sustain(0)
  .delay(.9).room(1),
  // blips
  note(
    "0 5 4 2".iter(4)
    .off(1/3, add(7))
    .scale('g4 dorian')
  ).s('square').cutoff(2000).decay(.03).sustain(0)
  .degradeBy(.2)
  .orbit(2).delay(.2).delaytime(".33 | .6 | .166 | .25")
  .room(1).gain(.5).mask("<0 1>/8"),
  // cloche
  note(rand.range(0,12).struct("x(5,8,-1)").scale('g2 minor pentatonic')).s('bell').begin(.05)
  .delay(.2).degradeBy(.4).gain(.4)
  .mask("<1 0>/8")
).slow(5)
```

## Ce qu'il faut en retenir

1. Un morceau = un `stack()` (ou des `$:`) de 4 à 7 couches, pas plus.
2. Chaque couche porte sa propre variation dans le temps (`<…>`, `sometimes`, `perlin`).
3. L'arrangement se fait par `mask("<x@7 ~>/8")` : les couches entrent et sortent.
4. Le mouvement timbral vient de LFO lents (`.slow(8)` à `.slow(32)`) sur le filtre.
5. Les constantes (`const keys = x => …`) évitent la répétition et rendent le patch lisible.
