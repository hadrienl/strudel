# Strudel — sources sonores

Sources : <https://strudel.cc/learn/samples/>, <https://strudel.cc/learn/synths/>,
<https://strudel.cc/workshop/first-sounds/>

## Percussions (banque tidal-drum-machines, chargée par défaut)

| Nom | Sens | | Nom | Sens |
|---|---|---|---|---|
| `bd` | grosse caisse | | `sh` | shaker |
| `sd` | caisse claire | | `cb` | cowbell |
| `rim` | rimshot | | `tb` | tambourin |
| `cp` | clap | | `perc` | percussion diverse |
| `hh` | charleston fermé | | `misc` | divers |
| `oh` | charleston ouvert | | `fx` | effets |
| `cr` | crash | | `lt` `mt` `ht` | toms grave/médium/aigu |
| `rd` | ride | | | |

Variantes : `hh:0`, `hh:1`… ou `.n("0 1 2")`. Les index bouclent au-delà du nombre
d'échantillons disponibles.

## Banques de boîtes à rythmes — `.bank()`

`.bank("RolandTR909")` préfixe le nom (`RolandTR909_bd`). Banques utiles selon le style :

| Banque | Usage typique |
|---|---|
| `RolandTR808` | hip-hop, trap, electro (kick sub, clap large) |
| `RolandTR909` | house, techno (kick punchy, hats métalliques) |
| `RolandTR707` | pop 80s, electro-funk |
| `RolandTR505` | new wave, synthpop |
| `RolandTR606` | acid, punk électronique |
| `RolandCompurhythm1000` | disco, city pop, YMO |
| `AkaiLinn`, `LinnDrum` | pop 80s, boogie |
| `OberheimDMX` | early hip-hop, freestyle |
| `EmuSP12` | boom bap |
| `AlesisHR16`, `CasioRZ1`, `YamahaRX5` | divers 80s/90s |

Se patterne : `.bank("<RolandTR808 RolandTR909>")`.

## Synthés intégrés

- **Oscillateurs** : `sine`, `sawtooth`, `square`, `triangle`. Défaut si `note()` sans `s()` : `triangle`.
- **Bruits** : `white`, `pink`, `brown` (du plus dur au plus doux), `crackle` (+ `.density()`).
  Ajout de bruit dans un oscillateur : `.noise(.3)`.
- **Additif** : `.partials(...)` (amplitude des harmoniques), `.phases(...)`, source `user`.
- **Vibrato** : `.vib(hz)` (alias `v`), profondeur `.vibmod(demi-tons)`.
- **FM** : `.fm(index)`, `.fmh(ratio)` — entier = timbre naturel, décimal = métallique ;
  enveloppe `.fmattack()`, `.fmdecay()`, `.fmsustain()`, `.fmenv('lin'|'exp')`.
- **Wavetables** : tout échantillon préfixé `wt_` (set AKWF, >1000 formes), bouclé par défaut ;
  balayage via `.loopBegin()` / `.loopEnd()`.
- **ZZFX** : `z_sine`, `z_square`, `z_sawtooth`, `z_tan`, `z_noise` + `zrand`, `curve`, `slide`,
  `deltaSlide`, `zmod`, `zcrush`, `zdelay`, `pitchJump`, `pitchJumpTime`, `lfo`, `tremolo`.

## Instruments General MIDI (soundfonts)

Préfixe `gm_` : `gm_piano`, `gm_epiano1`, `gm_acoustic_bass`, `gm_electric_bass_finger`,
`gm_electric_guitar_clean`, `gm_electric_guitar_muted`, `gm_synth_strings_1`, `gm_accordion`,
`gm_lead_6_voice`, `gm_pad_2_warm`, `gm_xylophone`, `gm_church_organ`, `gm_flute`,
`gm_trumpet`, `gm_marimba`… Variante de banque : `gm_accordion:2`.
Raccourci `.piano()` pour un piano acoustique.

Échantillons VCSL (instruments acoustiques) chargés par défaut également.
L'onglet **sounds** du REPL liste tout ce qui est disponible.

## Charger des échantillons externes

```javascript
// depuis un dépôt GitHub contenant un strudel.json
samples('github:tidalcycles/dirt-samples')
samples('github:yaxu/clean-breaks')          // breakbeats (amen, think…)

// mapping explicite + URL de base
samples({
  bassdrum: 'bd/BT0AADA.wav',
  snaredrum: ['sd/rytm-01-classic.wav', 'sd/rytm-00-hard.wav'],
}, 'https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/');

// échantillon accordé, avec régions de clavier
samples({ moog: { g2: 'moog/004_...G2.wav', g3: 'moog/005_...G3.wav' } }, 'github:tidalcycles/dirt-samples')

// depuis freesound.org (shabda) — pratique pour un son précis à la demande
samples('shabda:bass:4,hihat:4')
samples('shabda/speech/fr-FR/f:bonjour')
```

Le chargement est paresseux : le premier déclenchement peut arriver légèrement en retard.

## Manipulation d'échantillons

| Fonction | Effet |
|---|---|
| `.begin(0-1)` / `.end(0-1)` | point de départ / de fin dans l'échantillon |
| `.loop(1)` + `.loopBegin()` / `.loopEnd()` | bouclage (non synchronisé au tempo) |
| `.cut(n)` | groupe de coupure : un nouveau son coupe le précédent |
| `.clip(x)` / `.legato(x)` | multiplie la durée jouée (`.clip(1)` = durée de l'événement) |
| `.loopAt(n)` | étire l'échantillon sur n cycles (change la vitesse) |
| `.fit()` | ajuste l'échantillon à la durée de l'événement |
| `.chop(n)` | découpe granulaire en n morceaux consécutifs |
| `.striate(n)` | entrelace n tranches sur tous les échantillons du pattern |
| `.slice(n, "0 1 2 3")` | découpe en n tranches déclenchées par un pattern |
| `.splice(n, "...")` | comme slice, mais ajuste la vitesse à la durée |
| `.scrub("0.1!2 .25@3")` | lecture type bande magnétique |
| `.speed(x)` | vitesse de lecture (négatif = à l'envers) |

Recette breakbeat : `s("amen/4").fit().chop(16).cut(1).sometimesBy(.5, ply(2))`.
