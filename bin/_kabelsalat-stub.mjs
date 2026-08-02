// Remplace @kabelsalat/web hors navigateur.
// Le paquet réel est un bundle IIFE destiné au navigateur : Node n'y détecte aucun
// export nommé, ce qui casse l'import de @strudel/core. Seule la synthèse kabelsalat
// en dépend — inutile pour analyser un pattern.
export class SalatRepl {
  constructor() {
    this.audio = null;
  }
  evaluate() {}
  stop() {}
}
export default { SalatRepl };
