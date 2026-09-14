# -*- coding: utf-8 -*-
"""
8JET — la structure de place de marche.

Il a envoye jamesedition.com en reference et demande « the same structure ».

CE QUE J'AI PU ET PAS PU FAIRE. Je n'ai pas lu son site de reference :
Cloudflare bloque l'acces automatise, et je ne contourne pas une protection
anti-robot — ni pour lui, ni pour personne. La structure ci-dessous vient donc
de ce qu'est une place de marche de luxe dans son principe, et surtout de SES
donnees a lui. Je lui ai demande des captures des pages qu'il veut reprendre.

LA STRUCTURE, EN QUATRE TEMPS. C'est la colonne vertebrale de toutes ces
places de marche, JamesEdition compris :
    categorie  ->  liste filtrable  ->  fiche detaillee  ->  prise de contact

L'ancienne version mettait tout sur UNE page. On ne pouvait pas envoyer un
lien vers un vehicule precis, ni vers la couverture aeroportuaire. Chaque
vehicule a maintenant son adresse.

  python3 build_site.py   -> index.html, flotte.html, vehicule-*.html, aeroports.html
"""
import html
import json
import os
import re

import build as B          # on reprend SA feuille de style, pas une deuxieme
import data as D

RACINE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
ECRITES = set()

WA = getattr(D, "WHATSAPP", "") or getattr(D, "TEL_WA", "")

MENU = [("index.html", "Accueil"), ("flotte.html", "La flotte"),
        ("aeroports.html", "Aéroports"), ("index.html#etapes", "Comment ça marche")]

CSS_PLUS = """
/* ---- le menu -----------------------------------------------------------
   La feuille d'origine etait faite pour UNE page : il n'y avait pas de menu,
   donc aucune regle pour l'espacer. Sans ca les liens se collent. */
.nav{display:flex;gap:22px;flex-wrap:wrap;margin-left:auto;font-size:14.5px}
.nav a{color:var(--mu);text-decoration:none;padding:3px 0;
  border-bottom:2px solid transparent}
.nav a:hover{color:#fff;text-decoration:none}
.nav a[aria-current="page"]{color:#fff;border-bottom-color:var(--ac)}
@media (max-width:620px){.nav{gap:14px;font-size:13.5px}}

/* ---- la structure de place de marche ---------------------------------- */
.fil{font-size:13px;color:var(--mu);margin:18px 0 6px}
.fil a{color:var(--mu)}
.grille-v{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.vign{display:block;background:var(--n2);border:1px solid var(--l);border-radius:14px;
  overflow:hidden;text-decoration:none;transition:border-color .16s,transform .16s}
.vign:hover{border-color:var(--ac);transform:translateY(-3px);text-decoration:none}
.vign .img{aspect-ratio:16/10;display:grid;place-items:center;
  background:linear-gradient(140deg,#11161f,#0b1017);border-bottom:1px solid var(--l);
  color:var(--mu);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase}
.vign .corps{padding:16px 18px 18px}
.vign h3{font-size:17px;margin:0 0 4px;color:#fff}
.vign .cl{color:var(--ac);font-size:12.5px;letter-spacing:.1em;text-transform:uppercase}
.vign .sp{display:flex;gap:14px;color:var(--mu);font-size:13.5px;margin-top:10px}
.barre{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 18px}
.barre select,.barre input{background:var(--n2);color:var(--tx);border:1px solid var(--l);
  border-radius:9px;padding:9px 12px;font:inherit;font-size:14px}
.compteur{color:var(--ac);font-size:13.5px;margin-left:auto;font-variant-numeric:tabular-nums}
.rien{color:var(--mu);text-align:center;padding:36px 0}
.fiche-v{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,360px);gap:28px;
  align-items:start}
.specs{width:100%;border-collapse:collapse;font-size:15px;margin-top:6px}
.specs th,.specs td{padding:11px 0;border-bottom:1px solid var(--l);text-align:left}
.specs th{color:var(--mu);font-weight:500;width:46%}
.encart{background:var(--n2);border:1px solid var(--l);border-radius:14px;padding:20px}
.encart h3{font-size:17px;margin:0 0 10px}
.btn-wa{display:block;text-align:center;background:var(--ac);color:#0d1116;font-weight:700;
  border-radius:999px;padding:13px 20px;text-decoration:none;margin-top:14px}
.btn-wa:hover{background:var(--acd);text-decoration:none;color:#0d1116}
.note{color:var(--mu);font-size:13px}
@media (max-width:980px){.grille-v{grid-template-columns:repeat(2,minmax(0,1fr))}
  .fiche-v{grid-template-columns:1fr}}
@media (max-width:640px){.grille-v{grid-template-columns:1fr}}
"""


def page(fichier, titre, description, corps, actuel=None):
    nav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == (actuel or fichier) else ""}>{E(t)}</a>'
        for f, t in MENU)
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titre)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="noindex,nofollow">
<style>{B.CSS}{CSS_PLUS}</style>
</head>
<body>
<div class="demo"><b>Démonstration.</b> Le nom, les tarifs et les véhicules
présentés sont des exemples de travail, pas une offre commerciale.</div>
<header class="top"><div class="tbar">
  <a class="logo" href="index.html">{E(D.MARQUE)}</a>
  <nav class="nav">{nav}</nav>
</div></header>
<main>
{corps}
</main>
<footer class="pied"><div class="wrap">
  {E(D.MARQUE)} — {E(D.TITRE)}. Démonstration, aucune réservation réelle.
</div></footer>
</body></html>
"""
    with open(os.path.join(RACINE, fichier), "w", encoding="utf-8") as f:
        f.write(doc)
    ECRITES.add(fichier)
    return len(doc)


def lien_wa(texte):
    """Le bouton retombe sur un lien de contact ordinaire si aucun numero
    n'est configure — plutot que d'ouvrir une conversation avec un numero
    invente."""
    if not WA:
        return "index.html#contact"
    return f"https://wa.me/{WA}?text={html.escape(texte, quote=True).replace(' ', '%20')}"


def vignette(v):
    cle, nom, classe, pax, bag, desc, mult = v
    return f"""<a class="vign" href="vehicule-{E(cle)}.html">
  <span class="img">Photo à fournir</span>
  <span class="corps">
    <span class="cl">{E(classe)}</span>
    <h3>{E(nom)}</h3>
    <span class="sp"><span>{pax} passagers</span><span>{bag} bagages</span></span>
  </span>
</a>"""


# ---------------------------------------------------------------------------
def accueil():
    vedettes = "".join(vignette(v) for v in D.FLOTTE[:3])
    etapes = "".join(
        f'<div class="carte"><span class="num">{n}</span><h3>{E(t)}</h3>'
        f'<p>{E(d)}</p></div>' for n, t, d in
        [(e[0], e[1], e[2]) for e in D.ETAPES])
    villes = len({a[2] for a in D.AEROPORTS})
    return f"""
<section class="hero"><div class="wrap">
  <p class="sur">Transfert aéroport · {len(D.AEROPORTS)} aéroports</p>
  <h1>{E(D.TITRE)}</h1>
  <p class="lede">Une flotte de {len(D.FLOTTE)} véhicules, {len(D.AEROPORTS)}
  aéroports dans {villes} villes, et quatre niveaux d'accompagnement. On
  choisit le véhicule, on donne le vol, le reste est organisé.</p>
  <p><a class="btn-wa" style="display:inline-block;margin-top:18px"
     href="flotte.html">Voir la flotte</a></p>
</div></section>

<section class="sec"><div class="wrap">
  <h2>La flotte</h2>
  <p class="note" style="margin-bottom:18px">Trois véhicules parmi
  {len(D.FLOTTE)}. Chacun a sa fiche, avec ses capacités et ses options.</p>
  <div class="grille-v">{vedettes}</div>
  <p style="margin-top:18px"><a href="flotte.html">Les {len(D.FLOTTE)} véhicules et leurs filtres →</a></p>
</div></section>

<section class="sec" id="etapes"><div class="wrap">
  <h2>Comment ça marche</h2>
  <div class="grille-v">{etapes}</div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Où nous prenons en charge</h2>
  <p class="note">{len(D.AEROPORTS)} aéroports, {villes} villes,
  {len({a[3] for a in D.AEROPORTS})} pays — Montréal compris, avec Trudeau,
  Saint-Hubert et Mirabel.</p>
  <p style="margin-top:14px"><a href="aeroports.html">Voir la couverture →</a></p>
</div></section>
"""


def flotte():
    charge = [{"c": v[0], "n": v[1], "cl": v[2], "p": v[3], "b": v[4]}
              for v in D.FLOTTE]
    classes = sorted({v[2] for v in D.FLOTTE})
    opts = "".join(f'<option value="{E(c)}">{E(c)}</option>' for c in classes)
    return f"""
<nav class="fil"><div class="wrap"><a href="index.html">Accueil</a> / La flotte</div></nav>
<section class="sec"><div class="wrap">
  <h1>La flotte</h1>
  <p class="note" style="margin-bottom:20px">{len(D.FLOTTE)} véhicules.
  Filtrez par catégorie, par nombre de passagers ou de bagages : la liste
  répond pendant que vous changez.</p>

  <div class="barre">
    <select id="fCl"><option value="">Toutes les catégories</option>{opts}</select>
    <select id="fPax"><option value="">Passagers</option>
      <option value="3">3 et plus</option><option value="6">6 et plus</option>
      <option value="12">12 et plus</option></select>
    <select id="fBag"><option value="">Bagages</option>
      <option value="3">3 et plus</option><option value="6">6 et plus</option>
      <option value="10">10 et plus</option></select>
    <span class="compteur" id="compteur"></span>
  </div>

  <div class="grille-v" id="res"></div>
  <p class="rien" id="rien" hidden>Aucun véhicule ne correspond à ces critères.</p>
</div></section>

<script id="vehicules" type="application/json">{json.dumps(charge, ensure_ascii=False)}</script>
<script>
(function () {{
  var V = JSON.parse(document.getElementById('vehicules').textContent);
  var res = document.getElementById('res'), c = document.getElementById('compteur'),
      rien = document.getElementById('rien');
  function v(id) {{ var e = document.getElementById(id); return e.value || null; }}
  function rendre() {{
    var cl = v('fCl'), pax = v('fPax'), bag = v('fBag');
    var g = V.filter(function (x) {{
      if (cl && x.cl !== cl) return false;
      if (pax && x.p < parseInt(pax, 10)) return false;
      if (bag && x.b < parseInt(bag, 10)) return false;
      return true;
    }});
    res.innerHTML = g.map(function (x) {{
      return '<a class="vign" href="vehicule-' + x.c + '.html">' +
        '<span class="img">Photo à fournir</span><span class="corps">' +
        '<span class="cl">' + x.cl + '</span><h3>' + x.n + '</h3>' +
        '<span class="sp"><span>' + x.p + ' passagers</span><span>' +
        x.b + ' bagages</span></span></span></a>';
    }}).join('');
    c.textContent = g.length + (g.length > 1 ? ' véhicules' : ' véhicule');
    c.hidden = g.length === 0;
    rien.hidden = g.length > 0;
  }}
  ['fCl', 'fPax', 'fBag'].forEach(function (id) {{
    document.getElementById(id).addEventListener('change', rendre);
  }});
  rendre();
}})();
</script>
"""


def fiche(v):
    cle, nom, classe, pax, bag, desc, mult = v
    niveaux = "".join(
        f'<tr><th>{E(n[1])}</th><td>{E(n[3])}</td></tr>' for n in D.SECURITE)
    autres = "".join(vignette(o) for o in D.FLOTTE if o[0] != cle)
    return f"""
<nav class="fil"><div class="wrap"><a href="index.html">Accueil</a> /
  <a href="flotte.html">La flotte</a> / {E(nom)}</div></nav>
<section class="sec"><div class="wrap">
  <div class="fiche-v">
    <div>
      <p class="sur" style="color:var(--ac)">{E(classe)}</p>
      <h1>{E(nom)}</h1>
      <p class="lede">{E(desc)}</p>

      <h2 style="margin-top:34px;font-size:21px">Caractéristiques</h2>
      <table class="specs">
        <tr><th>Catégorie</th><td>{E(classe)}</td></tr>
        <tr><th>Passagers</th><td>{pax}</td></tr>
        <tr><th>Bagages</th><td>{bag}</td></tr>
        <tr><th>Photographies</th><td>À fournir</td></tr>
        <tr><th>Tarif</th><td>Sur devis, selon le trajet et le niveau retenu</td></tr>
      </table>

      <h2 style="margin-top:34px;font-size:21px">Niveaux d'accompagnement</h2>
      <table class="specs">{niveaux}</table>
    </div>

    <aside>
      <div class="encart">
        <h3>Demander ce véhicule</h3>
        <p class="note">Donnez le vol, le terminal, le nombre de passagers et
        de bagages. La réponse revient avec un prix ferme.</p>
        <a class="btn-wa" href="{lien_wa('Bonjour, je souhaite un transfert avec le ' + nom + '.')}"
           target="_blank" rel="noopener">Demander par WhatsApp</a>
        <p class="note" style="margin-top:12px">Démonstration : aucune
        réservation n'est enregistrée par cette page.</p>
      </div>
    </aside>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Les autres véhicules</h2>
  <div class="grille-v">{autres}</div>
</div></section>
"""


def aeroports():
    par_region = {}
    for a in D.AEROPORTS:
        par_region.setdefault(a[4], []).append(a)
    blocs = ""
    for reg in D.REGIONS:
        liste = par_region.get(reg, [])
        if not liste:
            continue
        lignes = "".join(
            f'<tr><th style="width:80px;color:var(--ac)">{E(a[0])}</th>'
            f'<td>{E(a[1])}</td><td>{E(a[2])}</td><td class="note">{E(a[3])}</td>'
            f'<td class="note">{a[5]} km</td></tr>' for a in liste)
        blocs += (f'<h2 style="margin-top:32px;font-size:21px">{E(reg)} '
                  f'<span class="note">({len(liste)})</span></h2>'
                  f'<table class="specs">{lignes}</table>')
    return f"""
<nav class="fil"><div class="wrap"><a href="index.html">Accueil</a> / Aéroports</div></nav>
<section class="sec"><div class="wrap">
  <h1>Couverture aéroportuaire</h1>
  <p class="lede">{len(D.AEROPORTS)} aéroports,
  {len({a[2] for a in D.AEROPORTS})} villes,
  {len({a[3] for a in D.AEROPORTS})} pays. La distance indiquée est celle qui
  sépare l'aéroport du centre-ville.</p>
  {blocs}
</div></section>
"""


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    total = 0
    total += page("index.html", f"{D.MARQUE} — {D.TITRE}",
                  f"Transfert aéroport de prestige : {len(D.FLOTTE)} véhicules, "
                  f"{len(D.AEROPORTS)} aéroports, quatre niveaux d'accompagnement.",
                  accueil())
    total += page("flotte.html", f"La flotte — {D.MARQUE}",
                  f"Les {len(D.FLOTTE)} véhicules, filtrables par catégorie, "
                  "passagers et bagages.", flotte())
    total += page("aeroports.html", f"Aéroports — {D.MARQUE}",
                  f"Les {len(D.AEROPORTS)} aéroports desservis, par région.",
                  aeroports())
    for v in D.FLOTTE:
        total += page(f"vehicule-{v[0]}.html", f"{v[1]} — {D.MARQUE}",
                      f"{v[1]} ({v[2]}) : {v[3]} passagers, {v[4]} bagages. "
                      "Caractéristiques et demande de transfert.",
                      fiche(v), actuel="flotte.html")

    print(f"{len(ECRITES)} pages, {total:,} octets".replace(",", " "))
    print(f"  flotte : {len(D.FLOTTE)} vehicules | aeroports : {len(D.AEROPORTS)}")
