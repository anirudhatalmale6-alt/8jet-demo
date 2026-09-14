# -*- coding: utf-8 -*-
"""Rend UNE page autonome contenant les 96 aeroports.

« one page, 96 options, like a book » : le livre est un index feuilletable a
gauche, la page de droite se recompose quand on choisit un aeroport. Rien n'est
recharge, il n'y a qu'un fichier.

C'est aussi ma reponse a « je veux des pages plus dynamiques » : sur les pages
de pilier de 8funder le visiteur LIT ; ici il MANIPULE — il choisit un
aeroport, un vehicule, un niveau de protection, et le devis se recalcule sous
ses yeux. Je lui montre la difference sur une page neuve plutot que de la lui
decrire.
"""
import html, json, sys
import data as D

SORTIE = sys.argv[1] if len(sys.argv) > 1 else 'index.html'

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --n:__N__; --n2:__N2__; --l:__L__; --tx:__TX__; --mu:__MU__;
  --ac:__AC__; --acd:__ACD__;
}
html,body{margin:0;padding:0}
body{background:var(--n);color:var(--tx);
  font:16px/1.6 "Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
  "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--ac);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1240px;margin:0 auto;padding:0 22px}
h1,h2,h3{line-height:1.14;letter-spacing:-.024em;margin:0 0 14px;font-weight:800;color:#fff}

.demo{background:#000;color:#e8eef4;font-size:12.5px;padding:8px 16px;text-align:center}
.demo b{color:var(--ac)}

header.top{border-bottom:1px solid var(--l);position:sticky;top:0;z-index:30;
  background:rgba(11,16,23,.92);backdrop-filter:blur(8px)}
.tbar{display:flex;align-items:center;gap:22px;padding:14px 22px}
.logo{font-weight:800;font-size:21px;letter-spacing:-.03em;color:#fff}
.logo span{color:var(--ac)}
.tnav{margin-left:auto;display:flex;gap:20px;font-size:14.5px}
.tnav a{color:var(--mu)} .tnav a:hover{color:var(--ac);text-decoration:none}

/* --- heros --- */
.hero{padding:74px 0 60px;border-bottom:1px solid var(--l);
  background:radial-gradient(820px 420px at 80% 12%,rgba(200,168,98,.11),transparent 60%)}
.kick{color:var(--ac);font-size:12px;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;margin:0 0 20px}
.hero h1{font-size:clamp(34px,5.2vw,60px);max-width:19ch;margin-bottom:20px}
.lede{font-size:17.5px;color:var(--mu);max-width:60ch;margin:0 0 28px}
.mes{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--l);
  border:1px solid var(--l);margin-top:40px}
.mes>div{background:var(--n);padding:22px 20px}
.mes b{display:block;font-size:30px;font-weight:800;color:#fff;letter-spacing:-.02em}
.mes span{font-size:13px;color:var(--mu)}

/* --- LE LIVRE : index a gauche, page a droite --- */
.book{display:grid;grid-template-columns:340px 1fr;gap:0;border-bottom:1px solid var(--l)}
.idx{border-right:1px solid var(--l);padding:26px 0 40px;
  position:sticky;top:60px;align-self:start;max-height:calc(100vh - 60px);overflow-y:auto}
.idx h3{font-size:11.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--mu);
  padding:0 22px;margin-bottom:12px}
.rech{margin:0 22px 14px;display:flex;border:1px solid var(--l);background:var(--n2)}
.rech input{flex:1;background:none;border:0;outline:0;color:var(--tx);font:inherit;
  font-size:14px;padding:10px 12px;min-width:0}
.reg{padding:0 22px;margin:16px 0 6px;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ac);font-weight:700}
.apt{display:flex;align-items:baseline;gap:10px;width:100%;text-align:left;border:0;
  background:none;color:var(--tx);font:inherit;font-size:14px;padding:7px 22px;cursor:pointer}
.apt:hover{background:var(--n2);color:var(--ac)}
.apt.on{background:var(--n2);color:var(--ac);box-shadow:inset 3px 0 0 var(--ac);font-weight:700}
.apt code{font:700 12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color:var(--mu);width:34px;flex:0 0 34px}
.apt.on code{color:var(--ac)}
.apt em{margin-left:auto;font-style:normal;font-size:12px;color:var(--mu)}
.vide{padding:20px 22px;color:var(--mu);font-size:13.5px}

.pane{padding:30px 30px 60px;min-width:0}
.folio{display:flex;align-items:baseline;gap:14px;color:var(--mu);font-size:12.5px;
  letter-spacing:.06em;text-transform:uppercase;margin-bottom:14px}
.folio b{color:var(--ac);font-weight:700}
.pane h2{font-size:clamp(25px,3.4vw,38px);margin-bottom:6px}
.sous{color:var(--mu);font-size:15.5px;margin:0 0 24px}
.faits{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:1px;background:var(--l);border:1px solid var(--l);margin-bottom:28px}
.faits>div{background:var(--n2);padding:15px 16px}
.faits b{display:block;font-size:19px;color:#fff;font-weight:800}
.faits span{font-size:12px;color:var(--mu)}

/* --- le configurateur : c'est la que la page devient vivante --- */
.cfg{border:1px solid var(--l);background:var(--n2);padding:22px;margin-bottom:26px}
.cfg h3{font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--mu);
  margin-bottom:16px;font-weight:700}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:9px;margin-bottom:18px}
.opt{border:1px solid var(--l);background:var(--n);padding:12px 14px;cursor:pointer;
  display:flex;flex-direction:column;gap:3px;text-align:left;color:var(--tx);font:inherit}
.opt:hover{border-color:var(--ac)}
.opt.on{border-color:var(--ac);background:rgba(200,168,98,.09)}
.opt b{font-size:14px;color:#fff}
.opt span{font-size:12px;color:var(--mu)}
.opt.on b{color:var(--ac)}
.devis{border-top:1px solid var(--l);padding-top:16px;display:flex;flex-wrap:wrap;
  align-items:baseline;gap:12px}
.devis .p{font-size:34px;font-weight:800;color:#fff;letter-spacing:-.03em}
.devis .d{font-size:13px;color:var(--mu)}
.devis .cta{margin-left:auto}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:13px 24px;
  font:700 14.5px/1.2 inherit;border:1.5px solid var(--ac);background:var(--ac);
  color:#10161f;cursor:pointer;text-decoration:none}
.btn:hover{background:var(--acd);border-color:var(--acd);text-decoration:none;color:#10161f}
.btn-g{background:transparent;color:#fff}
.btn-g:hover{background:transparent;color:var(--ac)}

.detail{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:26px}
.detail h4{font-size:11.5px;letter-spacing:.15em;text-transform:uppercase;
  color:var(--mu);margin:0 0 10px;font-weight:700}
.detail ul{list-style:none;margin:0;padding:0;font-size:14px;color:var(--mu)}
.detail li{padding:6px 0;border-bottom:1px solid var(--l)}
.detail li b{color:var(--tx);font-weight:600}

/* --- flotte --- */
section.sec{padding:66px 0;border-bottom:1px solid var(--l)}
section.sec h2{font-size:clamp(24px,3vw,34px);max-width:24ch}
.sub{color:var(--mu);max-width:62ch;margin:-4px 0 30px;font-size:16px}
.flotte{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:1px;background:var(--l);border:1px solid var(--l)}
.veh{background:var(--n2);padding:24px 22px;display:flex;flex-direction:column;gap:8px}
.veh .t{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ac);font-weight:700}
.veh b{font-size:18px;color:#fff}
.veh p{margin:0;font-size:14px;color:var(--mu);line-height:1.6}
.cap{display:flex;gap:18px;margin-top:auto;padding-top:12px;border-top:1px solid var(--l);
  font-size:13px;color:var(--mu)}
.cap b{color:#fff;font-size:15px}

/* --- securite --- */
.niv{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:22px}
.niv>div{border-top:2px solid var(--ac);padding-top:16px}
.niv h3{font-size:17px;margin-bottom:8px}
.niv p{color:var(--mu);font-size:14.5px;margin:0 0 12px}
.niv ul{list-style:none;margin:0;padding:0;font-size:13.5px;color:var(--mu)}
.niv li{padding:5px 0 5px 16px;position:relative}
.niv li::before{content:"";position:absolute;left:0;top:13px;width:6px;height:1px;background:var(--ac)}
.avert{border-left:3px solid var(--ac);background:rgba(200,168,98,.07);
  padding:16px 20px;margin-top:34px;font-size:14.5px;color:var(--tx);max-width:86ch}

/* --- etapes --- */
.etapes{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
  gap:1px;background:var(--l);border:1px solid var(--l)}
.etapes>div{background:var(--n2);padding:24px 22px}
.etapes .n{font-size:12px;font-weight:800;letter-spacing:.12em;color:var(--ac)}
.etapes b{display:block;font-size:16.5px;color:#fff;margin:8px 0 7px}
.etapes p{margin:0;font-size:14px;color:var(--mu);line-height:1.6}

footer{padding:40px 0 60px;color:var(--mu);font-size:13.5px}

@media (max-width:1000px){
  .book{grid-template-columns:1fr}
  .idx{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--l)}
  .idx .liste{max-height:320px;overflow-y:auto}
  .pane{padding:26px 0 46px}
  .mes{grid-template-columns:1fr 1fr}
}
@media (max-width:560px){
  .mes{grid-template-columns:1fr}
  .devis .cta{margin-left:0;width:100%}
  .btn{width:100%}
}
""".replace('__N__', D.NUIT).replace('__N2__', D.NUIT2).replace('__L__', D.LIGNE) \
   .replace('__TX__', D.TEXTE).replace('__MU__', D.MUET) \
   .replace('__AC__', D.ACCENT).replace('__ACD__', D.ACCENT_D)


JS = r"""
const $ = s => document.querySelector(s);
const eur = v => v.toLocaleString('fr-FR') + ' €';
let sel = A[0].iata, veh = F[0].id, secu = S[0].id, filtre = '';

/* Le tarif est calcule ICI et cote Python avec la MEME formule. Si les deux
   divergent, la page annonce un prix que le devis ne confirmera pas — c'est le
   defaut qu'on avait attrape sur les paliers du catalogue. */
function tarif(km, cv, cs){
  const base = Math.max(MINIMUM, PRISE + km * PARKM);
  return Math.round(base * cv * (1 + cs) / 5) * 5;
}
const apt = () => A.find(a => a.iata === sel);
const vhc = () => F.find(v => v.id === veh);
const sec = () => S.find(x => x.id === secu);

function rendreIndex(){
  const q = filtre.trim().toLowerCase();
  const vus = A.filter(a => !q || (a.iata + ' ' + a.nom + ' ' + a.ville + ' ' + a.pays)
                                    .toLowerCase().includes(q));
  const box = $('#liste');
  if (!vus.length){ box.innerHTML = '<p class="vide">Aucun aéroport ne correspond.</p>'; return; }
  let h = '', reg = null;
  for (const a of vus){
    if (a.region !== reg){ reg = a.region; h += `<div class="reg">${reg}</div>`; }
    h += `<button class="apt${a.iata === sel ? ' on' : ''}" data-iata="${a.iata}">`
       + `<code>${a.iata}</code><span>${a.ville}</span><em>${a.pays}</em></button>`;
  }
  box.innerHTML = h;
  $('#compte').textContent = vus.length + (vus.length > 1 ? ' aéroports' : ' aéroport');
}

function rendrePage(){
  const a = apt(), v = vhc(), s = sec();
  const n = A.findIndex(x => x.iata === a.iata) + 1;
  $('#folio').innerHTML = `Page <b>${String(n).padStart(2,'0')}</b> sur ${A.length}`
                        + ` &nbsp;·&nbsp; ${a.region}`;
  /* « Geneve — Geneve » : quand l'aeroport porte le nom de sa ville, le tiret
     repete le mot. On bascule sur la forme longue. */
  $('#titre').textContent = a.nom === a.ville ? 'Aéroport de ' + a.ville
                                              : a.nom + ' — ' + a.ville;
  $('#sous').textContent = `${a.pays} · code IATA ${a.iata} · `
    + `${a.terminaux} terminal${a.terminaux > 1 ? 'x' : ''}`;
  const mn = Math.round(a.km * 1.5) + 12;
  $('#faits').innerHTML = `
    <div><b>${a.iata}</b><span>Code IATA</span></div>
    <div><b>${a.km} km</b><span>Jusqu'au centre-ville</span></div>
    <div><b>~${mn} min</b><span>Trajet indicatif</span></div>
    <div><b>${a.terminaux}</b><span>Terminal${a.terminaux > 1 ? 'x' : ''}</span></div>`;

  $('#vehs').innerHTML = F.map(x => `<button class="opt${x.id === veh ? ' on' : ''}" data-veh="${x.id}">
      <b>${x.nom.replace('Mercedes-Benz ','')}</b>
      <span>${x.type} · ${x.pax} pass. · ${x.bag} bagages</span></button>`).join('');
  $('#secus').innerHTML = S.map(x => `<button class="opt${x.id === secu ? ' on' : ''}" data-secu="${x.id}">
      <b>${x.nom}</b><span>${x.court}</span></button>`).join('');

  const p = tarif(a.km, v.coef, s.coef);
  $('#prix').textContent = eur(p);
  $('#det').textContent = `${v.nom} · ${s.nom} · ${a.iata} vers le centre de ${a.ville}`;
  $('#inclus').innerHTML = s.inclus.map(i => `<li>${i}</li>`).join('');
  $('#pratique').innerHTML = `
    <li><b>Prise en charge</b> — salle d'arrivée, panneau nominatif</li>
    <li><b>Attente incluse</b> — 60 min après l'atterrissage</li>
    <li><b>Suivi du vol</b> — retard ou avance répercutés sans frais</li>
    <li><b>Annulation</b> — sans frais jusqu'à 12 h avant</li>`;
  /* Le bouton emmene la demande AVEC elle. Sans ca le client arrive sur
     WhatsApp avec un « bonjour » vide, et il faut cinq questions pour
     reconstituer ce qu'il avait deja choisi a l'ecran. */
  const cta = $('#cta');
  if (cta){
    if (WA){
      const txt = MODELE
        .replace('{aeroport}', a.nom).replace('{iata}', a.iata)
        .replace('{vehicule}', v.nom).replace('{securite}', s.nom)
        .replace('{prix}', eur(p));
      cta.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(txt);
      cta.target = '_blank';
      cta.rel = 'noopener';
      cta.textContent = 'Demander sur WhatsApp';
    } else {
      /* Pas de numero configure : on ne fabrique pas un lien wa.me au hasard,
         qui ouvrirait une conversation avec un inconnu. */
      cta.href = '#contact';
      cta.textContent = 'Demander cette mission';
    }
  }

  document.querySelectorAll('.apt').forEach(b =>
    b.classList.toggle('on', b.dataset.iata === sel));
}

document.addEventListener('click', e => {
  const a = e.target.closest('[data-iata]');
  if (a){ sel = a.dataset.iata; rendrePage();
          document.querySelector('.pane').scrollIntoView({block:'start', behavior:'smooth'}); return; }
  const v = e.target.closest('[data-veh]');
  if (v){ veh = v.dataset.veh; rendrePage(); return; }
  const s = e.target.closest('[data-secu]');
  if (s){ secu = s.dataset.secu; rendrePage(); return; }
});
$('#q').addEventListener('input', e => { filtre = e.target.value; rendreIndex(); });

rendreIndex(); rendrePage();
"""


def page():
    a = [{'iata': i, 'nom': n, 'ville': v, 'pays': p, 'region': r,
          'km': k, 'terminaux': t} for i, n, v, p, r, k, t in D.AEROPORTS]
    f = [{'id': i, 'nom': n, 'type': t, 'pax': pa, 'bag': b, 'desc': d, 'coef': c}
         for i, n, t, pa, b, d, c in D.FLOTTE]
    s = [{'id': i, 'nom': n, 'coef': c, 'court': d, 'inclus': l}
         for i, n, c, d, l in D.SECURITE]
    pays = len({x['pays'] for x in a})
    # Ces trois nombres etaient ECRITS EN DUR dans la page (« 6 modeles
    # Mercedes », « Huit modeles », « en trois niveaux »). La flotte est passee
    # a huit vehicules il y a deux versions et le bandeau annoncait toujours 6 :
    # personne ne l'avait vu, parce qu'un chiffre faux ne casse rien. Ils sont
    # maintenant derives de data.py, donc ils ne peuvent plus mentir.
    nmb = sum(1 for x in f if x['nom'].startswith('Mercedes-Benz'))
    ns = sum(1 for x in s if x['coef'] > 0)     # « Sans option » n'est pas un niveau
    MOTS = {1: 'un', 2: 'deux', 3: 'trois', 4: 'quatre', 5: 'cinq', 6: 'six',
            7: 'sept', 8: 'huit', 9: 'neuf', 10: 'dix'}

    flotte = '\n'.join(
        '<div class="veh"><span class="t">%s</span><b>%s</b><p>%s</p>'
        '<div class="cap"><span><b>%d</b> passagers</span>'
        '<span><b>%d</b> bagages</span></div></div>'
        % (html.escape(x['type']), html.escape(x['nom']), html.escape(x['desc']),
           x['pax'], x['bag']) for x in f)

    niveaux = '\n'.join(
        '<div><h3>%s</h3><p>%s</p><ul>%s</ul></div>'
        % (html.escape(x['nom']), html.escape(x['court']),
           ''.join('<li>%s</li>' % html.escape(i) for i in x['inclus'])) for x in s)

    etapes = '\n'.join(
        '<div><span class="n">%s</span><b>%s</b><p>%s</p></div>'
        % (n, html.escape(t), html.escape(d)) for n, t, d in D.ETAPES)

    return """<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(m)s — %(titre)s</title>
<meta name="robots" content="noindex,nofollow">
<style>%(css)s</style>
</head><body>

<div class="demo">Maquette — les <b>%(na)d aéroports</b>, leurs codes IATA, villes et
pays sont réels. Les distances, temps de trajet et <b>tarifs sont indicatifs</b> et
seront remplacés par votre grille. <b>%(m)s</b> est un nom provisoire.</div>

<header class="top"><div class="wrap tbar">
  <div class="logo">8<span>JET</span></div>
  <nav class="tnav">
    <a href="#livre">Les %(na)d aéroports</a>
    <a href="#flotte">La flotte</a>
    <a href="#securite">Sécurité</a>
    <a href="#deroulement">Déroulement</a>
  </nav>
</div></header>

<div class="hero"><div class="wrap">
  <p class="kick">Transfert aéroport · Chauffeur privé · Protection rapprochée</p>
  <h1>Un chauffeur qui vous attend, dans %(na)d aéroports.</h1>
  <p class="lede">Une flotte Mercedes, un véhicule sur mesure dont le modèle n'est pas
  publié, un chauffeur qui suit votre vol, et — si la destination l'exige — une équipe
  de protection étudiée avant le départ.
  Choisissez votre aéroport ci-dessous : la page se reconfigure.</p>
  <a class="btn" href="#livre">Ouvrir le livre des aéroports</a>
  <div class="mes">
    <div><b>%(na)d</b><span>aéroports desservis</span></div>
    <div><b>%(np)d</b><span>pays</span></div>
    <div><b>%(nf)d</b><span>véhicules au choix</span></div>
    <div><b>%(ns)d</b><span>niveaux de protection</span></div>
  </div>
</div></div>

<div id="livre" class="book">
  <aside class="idx">
    <h3>Le livre des aéroports</h3>
    <div class="rech"><input id="q" type="search" placeholder="Ville, pays ou code IATA…"
         aria-label="Rechercher un aéroport"></div>
    <div class="reg" id="compte"></div>
    <div class="liste" id="liste"></div>
  </aside>
  <main class="pane">
    <div class="folio" id="folio"></div>
    <h2 id="titre"></h2>
    <p class="sous" id="sous"></p>
    <div class="faits" id="faits"></div>

    <div class="cfg">
      <h3>Votre véhicule</h3>
      <div class="opts" id="vehs"></div>
      <h3>Option sécurité</h3>
      <div class="opts" id="secus"></div>
      <div class="devis">
        <span class="p" id="prix"></span>
        <span class="d" id="det"></span>
        <a class="btn cta" id="cta" href="#">Demander cette mission</a>
      </div>
    </div>

    <div class="detail">
      <div><h4>Ce que comprend la formule</h4><ul id="inclus"></ul></div>
      <div><h4>Pratique</h4><ul id="pratique"></ul></div>
    </div>
  </main>
</div>

<section class="sec" id="flotte"><div class="wrap">
  <h2>Une seule marque — et un véhicule qui n'en affiche aucune.</h2>
  <p class="sub">%(nmb)d Mercedes couvrent tout ce qu'un transfert demande, du trajet
  d'affaires seul à l'équipage complet — y compris deux véhicules choisis pour
  ne pas se faire remarquer. Une seule marque, donc un seul standard
  d'entretien, de propreté et de finition : c'est ce qui rend le service
  prévisible d'une ville à l'autre. La dernière ligne est l'exception, et c'est
  sa raison d'être : ni marque ni modèle publiés, un véhicule haut de gamme
  choisi mission par mission et confirmé par écrit à la commande.</p>
  <div class="flotte">%(flotte)s</div>
</div></section>

<section class="sec" id="securite"><div class="wrap">
  <h2>L'option sécurité, en %(nsm)s niveaux.</h2>
  <p class="sub">La plupart des trajets n'en ont pas besoin. Ceux qui en ont besoin
  ne se traitent pas au moment de la réservation : ils se préparent.</p>
  <div class="niv">%(niveaux)s</div>
  <div class="avert">%(avert)s</div>
</div></section>

<section class="sec" id="deroulement"><div class="wrap">
  <h2>Comment se passe une prise en charge.</h2>
  <div class="etapes">%(etapes)s</div>
</div></section>

<footer><div class="wrap">%(m)s — maquette de démonstration. Aucune réservation
n'est enregistrée depuis cette page.</div></footer>

<script>
const A = %(a)s;
const F = %(f)s;
const S = %(s)s;
const PRISE = %(prise)s, PARKM = %(parkm)s, MINIMUM = %(mini)s;
const WA = %(wa)s;
const MODELE = %(modele)s;
%(js)s
</script>
</body></html>""" % {
        'm': D.MARQUE, 'titre': D.TITRE, 'css': CSS, 'js': JS,
        'na': len(a), 'np': pays,
        'nf': len(f), 'ns': ns, 'nsm': MOTS.get(ns, str(ns)), 'nmb': nmb,
        'flotte': flotte, 'niveaux': niveaux, 'etapes': etapes,
        'avert': html.escape(D.AVERTISSEMENT_SECU),
        'a': json.dumps(a, ensure_ascii=False),
        'f': json.dumps(f, ensure_ascii=False),
        's': json.dumps(s, ensure_ascii=False),
        'prise': D.BASE_PRISE_EN_CHARGE, 'parkm': D.PAR_KM, 'mini': D.MINIMUM,
        'wa': json.dumps(D.WHATSAPP), 'modele': json.dumps(D.WHATSAPP_MODELE),
    }


if __name__ == '__main__':
    with open(SORTIE, 'w', encoding='utf-8') as f:
        f.write(page())
    print('%d aeroports, %d pays, %d vehicules, %d niveaux -> %s'
          % (len(D.AEROPORTS), len({x[3] for x in D.AEROPORTS}),
             len(D.FLOTTE), len(D.SECURITE), SORTIE))
