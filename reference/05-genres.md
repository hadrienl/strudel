# Recettes par style musical

Chaque fiche donne : tempo idiomatique, squelette rythmique, harmonie et sound design.
Les extraits sont des points de départ à combiner, pas des morceaux finis.
Rappel : `setcpm(BPM/4)` pour que 1 cycle = 1 mesure 4/4.

---

## House (120–128 BPM)

Kick 4/4, clap sur 2 et 4, charleston ouvert en contretemps, basse en croches.

```javascript
setcpm(124/4)
$: s("bd*4").bank("RolandTR909").duck(1).duckdepth(.7)
$: s("~ cp ~ cp").bank("RolandTR909").room(.2)
$: s("[~ oh]*4").bank("RolandTR909").gain(.5)
$: s("hh*16").gain("[.3 .5]*8").bank("RolandTR909")
$: note("<c2 c2 f2 g2>".add("<0 0 0 12>")).s("sawtooth")
   .lpf(600).decay(.12).sustain(0).struct("x ~ x ~ x ~ x ~".fast(2))
$: chord("<Cm9 Cm9 Fm9 G7>").voicing()
   .s("gm_epiano1").clip(.4).room(.4).orbit(1).gain(.5)
```

Variantes : **deep house** → `.lpf(1200)`, accords Rhodes, `.swing(4)` léger.
**Disco house** → boucle de cordes `gm_synth_strings_1`, `.chop()` sur un sample.

## Techno (128–140 BPM)

Mineur/atonal, texture > mélodie. Kick pesant, hats 16e, stab acide.

```javascript
setcpm(134/4)
$: s("bd*4").bank("RolandTR909").shape(.4).duck(1)
$: s("hh*16").gain(perlin.range(.2,.6).fast(4)).pan(sine.fast(3))
$: s("~ ~ cp ~").bank("RolandTR909").room(.6).roomsize(4).orbit(1)
$: note("c1 ~ [c1 eb1] ~".fast(2)).s("sawtooth").ftype(1)
   .lpf(sine.rangex(300, 2500).slow(16)).lpq(12)
   .decay(.15).sustain(0).orbit(1)
$: s("rim*8?").speed(rand.range(.8,1.4)).gain(.4).delay(.3)
```

**Acid** : `note("c1 [eb1 c1] g1 [c1 bb0]".fast(2)).s("sawtooth").ftype(1).lpf(sine.rangex(200,3000).slow(7)).lpq(20).lpenv(4).lpd(.1).sustain(0).distort(1.2)`
**Dub techno** : 120 BPM, accord unique en stab + `.delay(.7).delaytime(.375).delayfeedback(.8).room(1)`.

## Trance (136–142 BPM)

Basse en contretemps 16e, supersaw, arpège montant, gammes mineures.

```javascript
setcpm(138/4)
$: s("bd*4").bank("RolandTR909").duck(1)
$: note("a1").struct("~ x ~ x".fast(2)).s("sawtooth").lpf(400).decay(.08).sustain(0)
$: n("0 2 4 7 4 2".fast(2)).scale("A4:minor").s("sawtooth")
   .layer(x=>x, x=>x.add(note(.15)), x=>x.add(note(-.12)))
   .lpf(sine.rangex(800,6000).slow(16)).decay(.1).sustain(.2)
   .delay(.4).delaytime(3/16).room(.5).orbit(1)
```

## Drum & bass / jungle (170–176 BPM)

Breakbeat two-step, basse Reese, harmonie mineure/dorienne.

```javascript
setcpm(174/4)
$: s("bd ~ ~ ~ sd ~ ~ ~ ~ ~ bd ~ sd ~ ~ ~").bank("RolandTR909").gain(.9)
$: s("hh*8").gain("[.5 .3]*4").pan(.4)
$: note("<g1 g1 bb1 f1>").s("sawtooth")
   .layer(x=>x, x=>x.add(note(.1)).s("square"))
   .lpf(sine.rangex(200,900).slow(8)).lpq(8).shape(.5).clip(1)
$: n("0 3 5 7".off(1/8, add(7))).scale("G3:minor:pentatonic")
   .s("gm_epiano1").degradeBy(.4).delay(.4).room(.6)
```

**Jungle** : remplacer la batterie par un break découpé —
`samples('github:yaxu/clean-breaks'); s("amen/2").fit().chop(16).cut(1).sometimesBy(.4, ply(2)).rarely(mul(speed(-1)))`

## UK garage / 2-step (128–135 BPM)

Swing marqué, kick syncopé, snare sur 2 et 4, basse coupée.

```javascript
setcpm(132/4)
$: s("bd ~ ~ [~ bd] sd ~ [~ bd] ~ ~ bd ~ ~ sd ~ ~ ~").swing(8).bank("RolandTR909")
$: s("hh*8").swing(4).gain("[.5 .3]*4")
$: note("<c2 eb2 f2 g2>").s("sawtooth").struct("x ~ ~ x ~ x ~ ~").swing(4)
   .lpf(500).decay(.1).sustain(0)
$: chord("<Cm9 Eb^7 Fm9 Gm7>").voicing().s("gm_epiano1").clip(.3).room(.5).gain(.5)
```

## Dubstep / half-time (140 BPM, ressenti 70)

Snare uniquement sur le 3e temps, sub-basse modulée, espace.

```javascript
setcpm(140/4)
$: s("bd ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808").shape(.5)
$: s("hh ~ hh hh ~ hh ~ hh").gain(.4)
$: note("f1").s("sine").add(note("<0 0 3 -2>"))
   .lpf(200).clip(1).gain(.9)
   .vib("<0 2 4 8>").vibmod(.3).distort(1.1)
```

## Hip-hop boom bap (85–95 BPM)

Swing, kick/snare secs, échantillons filtrés, vinyle.

```javascript
setcpm(90/4)
$: s("bd ~ ~ bd ~ ~ sd ~ ~ bd ~ ~ sd ~ [~ sd] ~").bank("EmuSP12").swing(8)
$: s("hh*8").swing(4).gain("[.5 .35]*4").bank("EmuSP12")
$: note("<c2 c2 ab1 bb1>").s("gm_acoustic_bass").clip(.9).lpf(700)
$: chord("<Cm7 Cm7 Ab^7 Bb7>").voicing().dict('lefthand')
   .s("gm_epiano1").clip(.6).lpf(1800).room(.3).gain(.5)
$: s("crackle").density(20).gain(.25)
```

## Trap (140 BPM, ressenti half-time)

Charleston roulé, 808 glissée, clap large.

```javascript
setcpm(140/4)
$: s("bd ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
$: s("~ ~ ~ ~ cp ~ ~ ~ ~ ~ ~ ~ cp ~ ~ ~").bank("RolandTR808").room(.3)
$: s("hh*8").ply("<1 1 2 <3 4>>").gain("[.5 .3]*4").bank("RolandTR808")
$: note("<f1 f1 ab1 c2>").s("sine").clip(1).penv("<0 0 -5 0>").pdecay(.1)
   .lpf(180).distort(.8).gain(1)
```

## Lo-fi / chillhop (70–85 BPM)

Accords jazz, wobble de bande, batterie molle, filtre passe-bas généralisé.

```javascript
setcpm(78/4)
$: s("bd ~ ~ ~ sd ~ ~ bd ~ ~ ~ ~ sd ~ ~ ~").bank("AkaiLinn").swing(8).gain(.8)
$: s("hh*8").swing(4).gain(.3).lpf(6000)
$: chord("<F^9 Em7 Dm9 C^7>").voicing()
   .s("gm_epiano1").clip(.9)
   .add(note(perlin.range(-.15,.15)))   // wobble de bande
   .lpf(2200).room(.5).gain(.55)
$: note("<f1 e1 d1 c1>").s("gm_acoustic_bass").clip(.9)
$: s("crackle").density(12).gain(.3)
```

## Funk / disco (105–120 BPM)

Croches et doubles-croches, basse syncopée, accords 9e/13e, cuivres.

```javascript
setcpm(112/4)
$: s("bd ~ ~ bd ~ ~ bd ~ sd ~ ~ ~ ~ bd ~ ~").bank("RolandCompurhythm1000")
$: s("~ ~ sd ~".fast(2)).gain(.5)
$: s("hh*16").gain("[.6 .25 .4 .25]*4")
$: note("e2 ~ e2 g2 ~ a2 ~ e2 ~ ~ d2 ~ e2 ~ ~ ~").s("gm_electric_bass_finger")
   .clip(.8).lpf(1400)
$: chord("<Em9 Em9 A13 A13>").voicing().s("gm_electric_guitar_clean")
   .struct("~ x ~ x ~ x ~ x").clip(.2).gain(.45).room(.2)
```

## Reggae / dub (70–80 BPM)

One drop (kick + caisse claire sur le 3e temps), skank en contretemps, delay massif.

```javascript
setcpm(75/4)
$: s("~ ~ ~ ~ ~ ~ ~ ~ [bd,sd] ~ ~ ~ ~ ~ ~ ~").bank("RolandTR707").room(.3)
$: s("hh*8").gain("[.2 .5]*4")
$: note("<a1 a1 d2 e2>").s("gm_acoustic_bass").struct("x ~ ~ x ~ x ~ ~").clip(.9).lpf(500)
$: chord("<Am7 Am7 Dm7 E7>").voicing().s("gm_electric_guitar_muted")
   .struct("~ x ~ x ~ x ~ x").clip(.15)
   .delay(.5).delaytime(.25).delayfeedback(.7).room(.6).orbit(1)
```

## Bossa nova / samba (130 BPM écrit, ressenti 65)

Clave 3-2, accords maj7/m7/9, guitare nylon, brosses.

```javascript
setcpm(130/4)
$: s("rim").struct("x ~ ~ x ~ ~ x ~ ~ ~ x ~ x ~ ~ ~").gain(.5)
$: s("sh*8").gain(.3)
$: note("<a1 a1 d2 e2>").s("gm_acoustic_bass").struct("x ~ ~ ~ x ~ ~ ~").clip(.9)
$: chord("<Am9 D9 G^7 C^7>").voicing()
   .s("gm_electric_guitar_clean").struct("~ x ~ x x ~ x ~").clip(.4).room(.3).gain(.5)
```

## Jazz (swing, 120–200 BPM)

Ride swingué, walking bass, accords en croches irrégulières, gammes bebop.

```javascript
setcpm(140/4)
$: s("rd*8").swing(4).gain("[.6 .35]*4")
$: s("~ ~ hh ~").gain(.4)                        // charleston au pied sur 2 et 4
$: "<0 2 4 5>".scale("C2:bebop:major").note().s("gm_acoustic_bass")
   .struct("x x x x").clip(.95)
$: chord("<Dm7 G7 C^7 A7b13>").voicing().dict('lefthand')
   .struct("~ x ~ ~ x ~ x ~").swing(4).s("gm_epiano1").clip(.5).gain(.5)
$: n("0 2 4 6 5 3 1 0".fast(2)).scale("<D:dorian G:mixolydian C:major A:phrygian>")
   .swing(4).degradeBy(.3).s("gm_trumpet").clip(.6).room(.4)
```

## Ambient / drone (40–70 BPM, ou hors tempo)

Cycles longs (`.slow(8)` et plus), réverbe large, mouvement par LFO lents.

```javascript
setcpm(60/4)
$: chord("<C^9 Am9 F^7 Gsus>/4").voicing()
   .s("sawtooth").attack(3).release(6).sustain(.6)
   .lpf(sine.rangex(300,1600).slow(32)).gain(.4)
   .room(1).roomsize(8).delay(.4).delaytime(.75).delayfeedback(.6)
$: n(rand.range(0,7).segment(1)).scale("C5:major:pentatonic")
   .s("gm_music_box").degradeBy(.6).room(1).gain(.35).slow(2)
$: s("brown").gain(.08).lpf(400)
```

## Synthwave / retrowave (100–118 BPM)

Snare à réverbe gatée, arpège 16e, basse pulsée, nappes larges.

```javascript
setcpm(110/4)
$: s("bd ~ ~ ~ sd ~ ~ ~ ~ ~ bd ~ sd ~ ~ ~").bank("LinnDrum")
   .room("0 0 .8 0".fast(4)).roomfade(.2)
$: n("0 2 4 7".fast(4)).scale("<F3:minor Db3:major Ab3:major Eb3:major>")
   .s("sawtooth").decay(.1).sustain(.1).lpf(2500).delay(.3).delaytime(3/16).gain(.4)
$: note("<f1 db1 ab1 eb1>").s("square").struct("x*8").clip(.8).lpf(700).decay(.1).sustain(.3)
$: chord("<Fm9 Db^7 Ab^7 Ebsus>").voicing().s("sawtooth")
   .attack(.6).release(1).lpf(1200).gain(.35).room(.7).orbit(1)
```

## Chiptune (variable, souvent 140–170 BPM)

Trois voix : mélodie carrée, arpège rapide, basse triangle, bruit pour la batterie.

```javascript
setcpm(150/4)
$: n("0 4 7 4".fast(4)).scale("C5:major").s("square").decay(.05).sustain(0)  // arpège
$: n("<0 5 3 4>").scale("C3:major").s("triangle").struct("x*8").clip(.6)     // basse
$: s("white").struct("x ~ x x ~ x ~ x").decay(.03).sustain(0).hpf(2000).gain(.4)
$: n("0 ~ 2 4 ~ 7 5 4").scale("C6:major").s("square").decay(.1).sustain(0).gain(.4)
```

## Afrobeat / afro-house (110–125 BPM)

Rythmes euclidiens croisés, cloche clave, basse pentatonique.

```javascript
setcpm(118/4)
$: s("bd").struct("x(4,8)").bank("RolandTR909")
$: s("cb").struct("x(5,8,-1)").gain(.5)
$: s("perc").struct("x(7,16)").speed(rand.range(.9,1.2)).gain(.5).pan(rand)
$: s("sh*16").gain("[.4 .2]*8")
$: n("0 ~ 2 ~ 4 2 ~ 0").scale("F2:minor:pentatonic").s("gm_electric_bass_finger").clip(.7)
$: chord("<Fm9 Fm9 Bbm7 Eb7>").voicing().s("gm_electric_guitar_clean")
   .struct("x(3,8)").clip(.3).delay(.3).room(.4).gain(.45)
```

## IDM / braindance (variable)

Micro-édition rythmique, glitch, harmonie modale, randomisation contrôlée.

```javascript
setcpm(160/4)
$: s("bd*2, [~ sd]*2").bank("RolandTR606")
   .sometimesBy(.4, ply("<2 3 4>")).sometimesBy(.2, x=>x.speed(-1))
   .often(x=>x.crush(6)).shape(.3)
$: s("hh*16").degradeBy(.3).pan(rand).gain(rand.range(.2,.6)).crush("<16 8 4>")
$: n("0 3 5 7 10".shuffle(4)).scale("D:phrygian").s("triangle")
   .decay(.08).sustain(0).delay(.35).delaytime(rand.range(.05,.3)).room(.6)
$: note("d1").struct("x(3,8,<0 2>)").s("sine").clip(1).lpf(120)
```

---

## Vocabulaire de production transposable

| Intention | Moyen Strudel |
|---|---|
| Faire respirer un mix | `.duck(n)` sur le kick + `.orbit(n)` sur les nappes |
| Monter en tension | `.lpf(sine.rangex(400, 6000).slow(16))`, `.gain(saw.range(.3,.9).slow(8))` |
| Fill de fin de phrase | `.lastOf(4, x => x.ply(2).fast(2))` ou `.every(8, x => x.rev())` |
| Humaniser | `.swing(4)`, `.gain(perlin.range(.7,1))`, `.late(rand.range(0,.01))` |
| Variation infinie | `.sometimesBy(.2, …)`, `<a b c>` sur un paramètre, `.iter(4)` |
| Arrangement | `arrange([8, intro], [16, couplet], [16, refrain], [8, outro])` |
| Sections A/B | `.mask("<1 1 1 0>/4")` pour faire entrer/sortir une couche |
| Stéréo vivante | `.jux(rev)`, `.pan(sine.slow(7))`, `.juxBy(.5, x=>x.late(.01))` |
