#!/usr/bin/env node
// Vérifie un patch Strudel hors navigateur.
//
// Le son de Strudel passe par Web Audio : impossible de l'écouter ici. En revanche
// les paquets @strudel/* tournent en Node, donc on peut évaluer le patch et interroger
// les événements qu'il produit. Cela détecte les erreurs de syntaxe, les fonctions et
// contrôles inexistants, les couches muettes et les valeurs aberrantes — soit la
// quasi-totalité des patchs cassés. Cela ne dit rien de la qualité sonore.
//
// Usage : node bin/strudel-check.mjs tracks/x.strudel [--cycles 8] [--json] [--events]

import { registerHooks } from 'node:module';
import { pathToFileURL } from 'node:url';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));

// @kabelsalat/web est un bundle navigateur dont Node ne voit aucun export nommé,
// ce qui casse l'import de @strudel/core. Rien de ce qu'on fait ici n'en dépend.
const stubUrl = pathToFileURL(resolve(HERE, '_kabelsalat-stub.mjs')).href;
registerHooks({
  resolve(specifier, context, next) {
    if (specifier === '@kabelsalat/web') return { url: stubUrl, shortCircuit: true };
    return next(specifier, context);
  },
});

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--'));
const asJson = args.includes('--json');
const showEvents = args.includes('--events');
const cycles = Number(args[args.indexOf('--cycles') + 1]) || 8;

if (!file) {
  console.error('usage: strudel-check.mjs <fichier.strudel> [--cycles N] [--json] [--events]');
  process.exit(2);
}

// Silence le bruit de chargement des paquets pour garder une sortie lisible.
const realLog = console.log;
console.log = () => {};

const core = await import('@strudel/core');
const mini = await import('@strudel/mini');
const tonal = await import('@strudel/tonal');
const transpiler = await import('@strudel/transpiler');

await core.evalScope(core, mini, tonal);

// Le transpiler réécrit chaque ligne `$: …` en `.p('$')`, méthode fournie par le REPL
// pour empiler les couches. On la réimplémente pour les collecter.
const layers = [];
core.Pattern.prototype.p = function (id) {
  if (!String(id).startsWith('_')) layers.push(this); // `_$:` = couche mutée
  return this;
};

// Fonctions de contexte que le REPL fournit et qui n'existent pas hors navigateur.
const stubbed = [];
for (const name of ['setcpm', 'setcps', 'setCps', 'setCpm', 'samples', 'useRNG', 'hush', 'initHydra', 'all']) {
  if (typeof globalThis[name] !== 'function') {
    globalThis[name] = () => {};
    stubbed.push(name);
  }
}

console.log = realLog;

const code = readFileSync(file, 'utf8');
const problems = [];
const remarks = [];
let pattern;

// Strudel signale par console.warn/log les accords inconnus, les gammes invalides et
// les opérations impossibles — autant de couches silencieuses. On les capture.
const warnings = new Set();
const capture = (...a) => {
  const msg = a.map(String).join(' ');
  if (/warn|unknown|not found|can't|cannot|invalid/i.test(msg)) warnings.add(msg.trim());
};
const savedLog = console.log;
const savedWarn = console.warn;
console.log = capture;
console.warn = capture;

try {
  const result = await transpiler.evaluate(code, transpiler.transpiler);
  pattern = layers.length ? core.stack(...layers) : result.pattern;
} catch (err) {
  console.log = savedLog;
  console.warn = savedWarn;
  const out = { file, ok: false, error: String(err.message || err) };
  if (asJson) console.log(JSON.stringify(out, null, 2));
  else console.error(`❌ ${file}\n   ${out.error}`);
  process.exit(1);
}

if (!pattern || typeof pattern.queryArc !== 'function') {
  console.error(`❌ ${file}\n   le code ne produit aucun pattern jouable`);
  process.exit(1);
}

// Interroge les `cycles` premiers cycles, globalement puis couche par couche.
let haps;
const layerCounts = [];
try {
  haps = pattern.queryArc(0, cycles).filter((h) => h.hasOnset());
  for (const layer of layers) {
    layerCounts.push(layer.queryArc(0, cycles).filter((h) => h.hasOnset()).length);
  }
} catch (err) {
  console.log = savedLog;
  console.warn = savedWarn;
  console.error(`❌ ${file}\n   erreur pendant la lecture du pattern : ${err.message}`);
  process.exit(1);
}

console.log = savedLog;
console.warn = savedWarn;

// --- analyse -------------------------------------------------------------
const sounds = new Map();
const notes = new Set();
const gains = [];
let perCycle = new Array(cycles).fill(0);

for (const hap of haps) {
  const v = hap.value ?? {};
  const name = v.s ?? v.sound ?? (v.note !== undefined || v.n !== undefined ? '(note)' : '(?)');
  const key = v.bank ? `${v.bank}_${name}` : String(name);
  sounds.set(key, (sounds.get(key) ?? 0) + 1);
  if (v.note !== undefined) notes.add(String(v.note));
  if (typeof v.gain === 'number') gains.push(v.gain);
  const c = Math.floor(hap.whole.begin.valueOf());
  if (c >= 0 && c < cycles) perCycle[c]++;
}

if (haps.length === 0) problems.push('aucun événement produit — le patch est silencieux');
const emptyCycles = perCycle.reduce((acc, n, i) => (n === 0 ? [...acc, i] : acc), []);
if (emptyCycles.length) problems.push(`cycles silencieux : ${emptyCycles.join(', ')}`);
const loud = gains.filter((g) => g > 1.2).length;
if (loud) problems.push(`${loud} événement(s) à gain > 1.2 (risque de saturation)`);
if (sounds.has('(?)')) problems.push(`${sounds.get('(?)')} événement(s) sans son ni note assignés`);

// Une couche `$:` qui ne produit rien peut être cassée (accord inconnu, gamme invalide)
// ou simplement entrer plus tard dans l'arrangement. On distingue les deux en élargissant
// la fenêtre : muette sur 4× plus long = vraiment cassée.
const silent = layerCounts.reduce((acc, n, i) => (n === 0 ? [...acc, i] : acc), []);
const late = [];
const broken = [];
for (const i of silent) {
  let n = 0;
  try {
    n = layers[i].queryArc(0, cycles * 4).filter((h) => h.hasOnset()).length;
  } catch {}
  (n === 0 ? broken : late).push(i + 1);
}
if (broken.length) problems.push(`couche(s) $: muette(s) même sur ${cycles * 4} cycles — cassée(s) : n° ${broken.join(', ')}`);
if (late.length) remarks.push(`couche(s) $: n° ${late.join(', ')} : entrée après le cycle ${cycles} (arrangement)`);

// Les avertissements de Strudel signalent des couches partiellement silencieuses.
for (const w of warnings) problems.push(`Strudel : ${w}`);

// Un soundfont `gm_*` mal nommé ne joue rien et ne produit aucune erreur : on confronte
// les noms employés à la liste réelle du paquet.
const usedGm = [...new Set([...code.matchAll(/gm_[a-z0-9_]+/g)].map((m) => m[0]))];
if (usedGm.length) {
  try {
    const gmSrc = readFileSync(resolve(HERE, '../node_modules/@strudel/soundfonts/gm.mjs'), 'utf8');
    const known = new Set([...gmSrc.matchAll(/gm_[a-z0-9_]+/g)].map((m) => m[0]));
    const unknown = usedGm.filter((n) => !known.has(n));
    if (unknown.length) problems.push(`soundfont(s) inexistant(s), donc muet(s) : ${unknown.join(', ')}`);
  } catch {
    remarks.push('liste des soundfonts non vérifiée (@strudel/soundfonts absent)');
  }
}

const report = {
  file,
  ok: problems.length === 0,
  cycles,
  events: haps.length,
  eventsPerCycle: perCycle,
  sounds: Object.fromEntries([...sounds].sort((a, b) => b[1] - a[1])),
  distinctNotes: notes.size,
  gainRange: gains.length ? [Math.min(...gains), Math.max(...gains)] : null,
  stubbed,
  problems,
  remarks,
};

if (asJson) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`${report.ok ? '✅' : '⚠️ '} ${file}`);
  console.log(`   ${haps.length} événements sur ${cycles} cycles — par cycle : ${perCycle.join(' ')}`);
  if (layerCounts.length) console.log(`   ${layerCounts.length} couches $: — événements : ${layerCounts.join(' ')}`);
  console.log(`   sons : ${[...sounds].map(([k, n]) => `${k}×${n}`).join(', ') || '—'}`);
  if (notes.size) console.log(`   ${notes.size} hauteurs distinctes`);
  if (report.gainRange) console.log(`   gain : ${report.gainRange[0]} … ${report.gainRange[1]}`);
  for (const p of problems) console.log(`   ⚠️  ${p}`);
  for (const r of remarks) console.log(`   ℹ️  ${r}`);
  if (showEvents) {
    for (const h of haps.slice(0, 200)) {
      console.log(`   ${h.whole.begin.valueOf().toFixed(3)}  ${JSON.stringify(h.value)}`);
    }
  }
}

process.exit(report.ok ? 0 : 1);
