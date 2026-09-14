# -*- coding: utf-8 -*-
"""Presse la page elle-meme. Le point qui compte : le prix affiche doit etre
celui que la formule donne, et il doit CHANGER quand on change de vehicule,
d'aeroport ou de niveau de protection. Une page « dynamique » dont le chiffre
ne bouge pas est une page morte avec des boutons."""
import os, re, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

# Le nombre attendu se DERIVE de la source : ecrit en dur, il tombe a chaque
# ajout legitime d'aeroport, et un controle qui crie pour rien finit ignore.
ATTENDU = len(D.AEROPORTS)

ICI = os.path.dirname(os.path.abspath(__file__))
URL = 'file://' + os.path.join(ICI, 'index.html')
ok = ko = 0


def t(nom, cond, detail=''):
    global ok, ko
    if cond: ok += 1; print('  OK    %s' % nom)
    else:    ko += 1; print('  ECHEC %s   %s' % (nom, detail))


def eur(s):
    n = re.sub(r'[^\d]', '', s)
    return int(n) if n else None


with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    pg.set_viewport_size({'width': 1280, 'height': 900})
    err = []
    pg.on('pageerror', lambda e: err.append(str(e)))
    pg.on('console', lambda m: err.append(m.text) if m.type == 'error' else None)
    pg.goto(URL)

    print(f'\n1. Le livre contient bien les {ATTENDU} aeroports')
    n = pg.locator('.apt').count()
    t(f'{ATTENDU} entrees dans l\'index', n == ATTENDU, str(n))
    t('aucune erreur JS', not err, str(err[:2]))
    codes = pg.eval_on_selector_all('.apt code', 'e=>e.map(x=>x.textContent)')
    t(f'{ATTENDU} codes IATA distincts', len(set(codes)) == ATTENDU,
      str(len(set(codes))))
    t('les 7 regions sont titrees', pg.locator('.reg').count() >= 7,
      str(pg.locator('.reg').count()))

    print('\n2. La recherche filtre vraiment')
    pg.fill('#q', 'suisse')
    t('« suisse » ramene 3 aeroports', pg.locator('.apt').count() == 3,
      str(pg.locator('.apt').count()))
    pg.fill('#q', 'CDG')
    t('un code IATA ramene 1 resultat', pg.locator('.apt').count() == 1,
      str(pg.locator('.apt').count()))
    pg.fill('#q', 'zzzz')
    t('une recherche vide le dit', pg.locator('.vide').count() == 1)
    pg.fill('#q', '')
    t(f'effacer restaure les {ATTENDU}', pg.locator('.apt').count() == ATTENDU,
      str(pg.locator('.apt').count()))

    print('\n3. Choisir un aeroport recompose la page')
    avant = pg.locator('#titre').inner_text()
    pg.click('[data-iata="DXB"]')
    pg.wait_for_timeout(200)
    t('le titre a change', pg.locator('#titre').inner_text() != avant)
    t('le titre porte Dubai', 'Duba' in pg.locator('#titre').inner_text(),
      pg.locator('#titre').inner_text())
    t('le sous-titre porte le code IATA', 'DXB' in pg.locator('#sous').inner_text())
    # inner_text rend le texte TEL QU'AFFICHE : text-transform le passe en
    # capitales et le <b> y insere un saut de ligne. On normalise avant de
    # comparer, sinon on teste la mise en forme et pas le contenu.
    folio = ' '.join(pg.locator('#folio').inner_text().split()).lower()
    t('le folio numerote la page',
      re.search(rf'page \d+ sur {ATTENDU}', folio) is not None, folio)

    print('\n4. LE PRIX suit la formule Python, au centime')
    aptd = {a[0]: a for a in D.AEROPORTS}
    fl = {f[0]: f for f in D.FLOTTE}
    se = {s[0]: s for s in D.SECURITE}
    for iata, vid, sid in [('DXB', 'classe-e', 'aucune'),
                           ('LHR', 'classe-s', 'discret'),
                           ('NRT', 'sprinter', 'rapproche'),
                           ('GVA', 'sur-mesure', 'discret'),
                           ('YUL', 'vito', 'blinde'),
                           ('LCY', 'eqs', 'aucune')]:
        pg.click('[data-iata="%s"]' % iata); pg.wait_for_timeout(60)
        pg.click('[data-veh="%s"]' % vid);   pg.wait_for_timeout(60)
        pg.click('[data-secu="%s"]' % sid);  pg.wait_for_timeout(60)
        attendu = D.tarif(aptd[iata][5], fl[vid][6], se[sid][2])
        lu = eur(pg.locator('#prix').inner_text())
        t('%s / %s / %s -> %d EUR' % (iata, vid, sid, attendu), lu == attendu,
          'page=%s python=%s' % (lu, attendu))

    print('\n5. Le prix BOUGE quand on change un parametre')
    pg.click('[data-iata="CDG"]'); pg.click('[data-veh="classe-e"]')
    pg.click('[data-secu="aucune"]'); pg.wait_for_timeout(80)
    p0 = eur(pg.locator('#prix').inner_text())
    pg.click('[data-veh="classe-s"]'); pg.wait_for_timeout(80)
    p1 = eur(pg.locator('#prix').inner_text())
    t('changer de vehicule change le prix', p1 > p0, '%s -> %s' % (p0, p1))
    pg.click('[data-secu="rapproche"]'); pg.wait_for_timeout(80)
    p2 = eur(pg.locator('#prix').inner_text())
    t('ajouter la protection change le prix', p2 > p1, '%s -> %s' % (p1, p2))
    pg.click('[data-iata="LBG"]'); pg.wait_for_timeout(80)
    p3 = eur(pg.locator('#prix').inner_text())
    t('changer d\'aeroport change le prix', p3 != p2, '%s -> %s' % (p2, p3))

    print('\n6. La liste des inclus suit le niveau choisi')
    pg.click('[data-secu="aucune"]'); pg.wait_for_timeout(80)
    n0 = pg.locator('#inclus li').count()
    pg.click('[data-secu="rapproche"]'); pg.wait_for_timeout(80)
    n1 = pg.locator('#inclus li').count()
    t('la protection rapprochee liste plus de points', n1 > n0, '%d puis %d' % (n0, n1))
    # On retrouve le niveau PAR SON ID. C'etait ecrit D.SECURITE[2] — un index
    # de position, qui designait « protection rapprochee » jusqu'a ce que
    # « vehicule renforce » soit insere avant elle. Le test continuait a passer
    # parce que les deux niveaux ont le meme nombre de points : il ne mesurait
    # plus ce qu'il croyait mesurer.
    attendu = len(se['rapproche'][4])
    t('le nombre correspond aux donnees', n1 == attendu, '%d vs %d' % (n1, attendu))

    print('\n7. La flotte rendue est celle de data.py')
    noms = pg.eval_on_selector_all('.veh > b', 'e=>e.map(x=>x.textContent)')
    # On compare a la SOURCE, pas a un nombre ecrit en dur. « six vehicules »
    # etait vrai jusqu'a ce que le client en demande deux de plus, et le test
    # est alors passe au rouge sur un comportement correct. Ce qu'on veut
    # verifier, c'est que la page rend exactement ce que data.py contient.
    t('la page rend tous les vehicules de data.py',
      len(noms) == len(D.FLOTTE), '%d rendus / %d dans data.py' % (len(noms), len(D.FLOTTE)))
    # « tous Mercedes-Benz » n'est plus vrai depuis que le client a demande une
    # option sur mesure dont on ne publie pas la marque. On verifie donc la
    # regle reelle : tout ce qui est nomme est une Mercedes, et la seule
    # exception est celle qui ne nomme rien.
    hors = [n for n in noms if not n.startswith('Mercedes-Benz')]
    t('une seule ligne hors Mercedes', len(hors) == 1, str(hors))
    t('et cette ligne ne nomme aucune marque',
      hors and not re.search(r'Mercedes|BMW|Audi|Range|Bentley|Rolls|Tesla|Cadillac',
                             hors[0], re.I), str(hors))
    t('le Classe G a bien ete retire', not any('Classe G' in n for n in noms), str(noms))
    t('les deux vehicules discrets sont la',
      any('Classe C' in n for n in noms) and any('Vito' in n for n in noms), str(noms))

    # Le vehicule sur mesure ne doit rien laisser fuir NULLE PART sur la page,
    # pas seulement dans son titre : ni marque, ni modele, ni immatriculation.
    fiche = pg.eval_on_selector_all('.veh',
        "e=>e.map(x=>x.innerText).filter(s=>s.indexOf('sur mesure')>=0).join(' ')")
    t('sa fiche ne cite aucune marque',
      not re.search(r'BMW|Audi|Range Rover|Bentley|Rolls|Tesla|Cadillac|Lexus|Volvo',
                    fiche, re.I), fiche[:120])

    print('\n8. L\'avertissement securite est present et visible')
    t('l\'avertissement est affiche', pg.locator('.avert').is_visible())
    t('il parle d\'autorisation', 'autorisation' in pg.locator('.avert').inner_text())
    txt = pg.content()
    for interdit in ('VR7', 'B6', 'blindé', 'armé', 'arme à feu'):
        t('la page ne promet pas « %s »' % interdit, interdit not in txt)

    print('\n8 bis. Le bouton emmene la demande dans WhatsApp')
    import urllib.parse as _u
    cta = pg.query_selector('#cta')
    href = cta.get_attribute('href')
    t('le bouton pointe vers wa.me', href.startswith('https://wa.me/'), href[:60])
    t('il s ouvre dans un nouvel onglet', cta.get_attribute('target') == '_blank')
    t('le lien porte rel=noopener', cta.get_attribute('rel') == 'noopener')
    txt = _u.unquote_plus(_u.parse_qs(_u.urlparse(href).query).get('text', [''])[0])
    iata = pg.eval_on_selector('#sous', 'e=>e.textContent').split('IATA ')[1].split(' ')[0]
    t('le message pre-rempli nomme l aeroport choisi', iata in txt, txt[:90])
    t('le message pre-rempli nomme le vehicule et l option',
      'hicule :' in txt and 'Option :' in txt, txt[:120])
    # Le lien doit SUIVRE la configuration : un href fige donnerait un message
    # juste au premier affichage et faux des le premier clic suivant.
    pg.click('[data-veh="vito"]')
    pg.wait_for_timeout(200)
    txt2 = _u.unquote_plus(_u.parse_qs(_u.urlparse(
        pg.query_selector('#cta').get_attribute('href')).query).get('text', [''])[0])
    t('le message suit le changement de vehicule',
      'Vito' in txt2 and txt2 != txt, txt2[:90])

    print('\n9. Le bandeau dit ce qui est reel et ce qui ne l\'est pas')
    d = pg.locator('.demo').inner_text()
    t('il annonce les tarifs comme indicatifs', 'indicatifs' in d, d[:90])
    t('il annonce le nom comme provisoire', 'provisoire' in d)

    print('\n10. Rendu')
    for w in (390, 768, 1280):
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.wait_for_timeout(120)
        deb = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        t('aucun debordement a %d px' % w, deb <= 0, str(deb))

    pg.set_viewport_size({'width': 1280, 'height': 900})
    faibles = pg.evaluate("""() => {
      const lum = c => { const [r,g,b] = c.match(/\\d+/g).map(Number).map(v => {
        v/=255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); });
        return .2126*r + .7152*g + .0722*b; };
      /* Un fond en rgba(200,168,98,.09) n'est PAS du dore : c'est 9 % de dore
         pose sur ce qu'il y a dessous. L'ancienne version rendait la couche
         telle quelle et lisait donc du texte dore sur fond dore, ratio 1,00,
         alors que le rendu est parfaitement lisible. On EMPILE les couches et
         on les compose jusqu'a tomber sur une couleur opaque. */
      const lire = c => { const m = (c||'').match(/[\d.]+/g); if (!m) return null;
        return [ +m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1 ]; };
      const fond = el => {
        const couches = [];
        let e = el;
        while (e) {
          const c = lire(getComputedStyle(e).backgroundColor);
          if (c && c[3] > 0) { couches.push(c); if (c[3] === 1) break; }
          e = e.parentElement;
        }
        if (!couches.length || couches[couches.length-1][3] < 1) couches.push([11,16,23,1]);
        let out = couches.pop();
        while (couches.length) {
          const c = couches.pop(), a = c[3];
          out = [ c[0]*a + out[0]*(1-a), c[1]*a + out[1]*(1-a), c[2]*a + out[2]*(1-a), 1 ];
        }
        return 'rgb(' + out.map(Math.round).slice(0,3).join(',') + ')';
      };
      const out = [];
      document.querySelectorAll('body *').forEach(el => {
        if (!el.offsetParent && el.offsetHeight === 0) return;
        if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
        const s = getComputedStyle(el);
        const a = lum(s.color), b = lum(fond(el));
        const r = (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
        const gros = parseFloat(s.fontSize) >= 24 ||
                     (parseFloat(s.fontSize) >= 18.66 && parseInt(s.fontWeight,10) >= 700);
        if (r < (gros ? 3 : 4.5)) out.push([el.className||el.tagName, s.color, s.fontSize, r.toFixed(2)]);
      });
      return out; }""")
    t('contraste : 0 element sous le seuil', len(faibles) == 0, str(faibles[:4]))
    t('toujours aucune erreur JS', not err, str(err[:2]))

    pg.screenshot(path=os.path.join(ICI, 'aero_1_hero.png'))
    pg.click('[data-iata="GVA"]'); pg.click('[data-veh="classe-s"]')
    pg.click('[data-secu="discret"]'); pg.wait_for_timeout(200)
    pg.evaluate("document.querySelector('.pane').scrollIntoView()")
    pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(ICI, 'aero_2_livre.png'))
    pg.evaluate("document.querySelector('#flotte').scrollIntoView()")
    pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(ICI, 'aero_3_flotte.png'))
    pg.evaluate("document.querySelector('#securite').scrollIntoView()")
    pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(ICI, 'aero_4_securite.png'))
    pg.set_viewport_size({'width': 390, 'height': 800})
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(ICI, 'aero_5_mobile.png'))
    b.close()

print('\n%d OK, %d ECHEC' % (ok, ko))
sys.exit(1 if ko else 0)
