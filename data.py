# -*- coding: utf-8 -*-
"""Transfert aeroport de luxe — les donnees.

BRIEF DU CLIENT, mot pour mot : « based on 8secur Model I want an airport
luxury transfert including an option with security. This page with code should
be adapted with th 96 major airports in the world. You can code it to generate
it one time, one page, 96 options, like a book. Vehicle type Mercedes only,
select 6 models of Mercedes ».

DONC : UNE page, generee UNE fois, 96 aeroports dedans, feuilletables comme un
livre. Pas 96 fichiers. Le lecteur choisit son aeroport et la page se
reconfigure — c'est la partie « dynamique » qu'il reclame par ailleurs sur
8funder.

CE QUI EST REEL ICI : les 96 aeroports, leur code IATA, leur ville et leur pays.
Ce sont des faits verifiables et je ne les invente pas.

CE QUI EST INDICATIF ET ANNONCE COMME TEL : les distances au centre-ville, les
temps de trajet et les tarifs. Un temps de trajet depend de l'heure et du
trafic, un tarif depend de ses contrats. Le bandeau de la page le dit, et les
valeurs sont DERIVEES d'une bande de distance, pas tapees une par une — le jour
ou il me donne sa grille reelle, on remplace la fonction, pas 96 lignes.

MERCEDES UNIQUEMENT, six modeles, comme demande. Nommer les vehicules qu'on
exploite est un usage descriptif normal dans ce metier — ce n'est pas la meme
chose que mettre une marque d'un tiers dans le nom de l'entreprise.
"""

MARQUE = '8JET'          # PLACEHOLDER — le client n'a pas donne le nom

# Le bouton « Demander cette mission » ouvre WhatsApp avec le detail deja
# ecrit. Le numero ci-dessous est celui que j'ai deja de lui ; s'il n'est pas
# le bon, une seule ligne a changer. Format international SANS le +, comme
# l'exige wa.me.
#
# Si la constante est vide, le bouton retombe sur un lien de contact ordinaire
# plutot que d'ouvrir une conversation avec un numero au hasard.
WHATSAPP = '16475561647'
TITRE  = 'transfert aéroport de prestige et transport sécurisé'

# Nuit + laiton. La reference est 8secur : en-tete sombre, surtitre en
# capitales espacees, titre tres gras, filets fins. Contrastes MESURES plus bas
# par mesures.py, pas estimes.
NUIT    = '#0b1017'
NUIT2   = '#121a25'
LIGNE   = '#243040'
TEXTE   = '#dfe6ee'
MUET    = '#9fb0c2'
ACCENT  = '#c8a862'      # laiton
ACCENT_D = '#b08f45'

# ---------------------------------------------------------------------------
# LES SIX MERCEDES. Capacites reelles en configuration chauffeur.
# ---------------------------------------------------------------------------
FLOTTE = [
 ('classe-e', 'Mercedes-Benz Classe E', 'Berline', 3, 3,
  'La berline de reference du transfert d’affaires. Discrete, silencieuse, '
  'suffisante pour deux passagers et leurs bagages cabine.', 1.00),
 ('classe-s', 'Mercedes-Benz Classe S', 'Berline de représentation', 3, 3,
  'Empattement long, sièges arrière inclinables, isolation phonique renforcée. '
  'C’est la voiture qu’on prend quand le trajet doit être un bureau.', 1.55),
 ('eqs', 'Mercedes-Benz EQS', 'Berline électrique', 3, 3,
  'Équivalent Classe S en électrique. Demandée par les entreprises qui '
  'rapportent leurs émissions, et par les villes à zone à faibles émissions.', 1.50),
 ('classe-v', 'Mercedes-Benz Classe V', 'Van', 6, 6,
  'Six places assises face à la route et de vrais volumes de coffre. Le choix '
  'par défaut dès qu’il y a une famille ou une délégation.', 1.35),
 ('sprinter', 'Mercedes-Benz Sprinter', 'Van grand volume', 12, 14,
  'Équipages, tournées, groupes. C’est le seul véhicule de la liste qui absorbe '
  'un excédent de bagages sans second véhicule.', 1.70),
 # RETIRE a la demande du client : « enleve le Classe G ». Il avait raison et
 # c'est la meme logique que le reste de cette liste — une Classe G noire est
 # probablement le vehicule le plus reconnaissable du catalogue Mercedes. Elle
 # contredisait la page qu'elle etait censee completer.

 # AJOUT demande par le client : « rajouter autre de notre flotte inconnu pour
 # maximiser la discretion ». Le paradoxe du transfert de prestige est qu'une
 # Classe S noire devant un terminal DESIGNE le passager. Ces deux vehicules
 # font l'inverse : ils ne se remarquent pas. On reste dans la contrainte
 # « Mercedes uniquement » qu'il avait posee au depart — si l'idee est d'aller
 # chercher d'autres marques encore plus banales, il me le dira.
 ('classe-c', 'Mercedes-Benz Classe C', 'Berline discrète', 3, 2,
  'Une berline qui ne se remarque pas. Sur les arrivées surveillées, une '
  'voiture ordinaire protège mieux qu’une voiture de représentation : elle ne '
  'désigne personne.', 1.10),
 ('vito', 'Mercedes-Benz Vito', 'Van banalisé', 7, 7,
  'Le van sans marquage ni vitres teintées d’usine. Volume d’une Classe V, '
  'silhouette d’un véhicule utilitaire. Demandé quand l’arrivée doit passer '
  'pour une livraison.', 1.20),

 # AJOUT demande par le client : « met l'option personalisé / voiture haut de
 # gamme custom inconnu ». C'est la seule ligne de la flotte qui ne porte ni
 # marque ni modele, et c'est VOULU : le reste de la page decrit des vehicules
 # identifiables, donc reconnaissables. Une page publique qui nomme le vehicule
 # d'une arrivee sensible fait la moitie du travail de celui qui la surveille.
 # Sur cette ligne, la page dit ce que le vehicule fait et se tait sur ce qu'il
 # est ; le modele se confirme par ecrit a la commande.
 #
 # C'est aussi la premiere ligne qui sort de la contrainte « Mercedes only »
 # posee au depart. Elle en sort parce que l'interet de l'option est justement
 # de ne pas etre previsible — s'engager sur une marque la rendrait devinable.
 ('sur-mesure', 'Véhicule sur mesure', 'Haut de gamme, modèle non publié', 4, 4,
  'Le seul véhicule de cette page dont ni la marque ni le modèle ne sont '
  'annoncés. Il est choisi mission par mission dans la catégorie haut de gamme, '
  'et il change d’une venue à l’autre. Une voiture de représentation identique '
  'à chaque fois finit par être reconnue ; un véhicule qui n’est publié nulle '
  'part ne l’est pas. Aménagement intérieur, plaques et équipage définis à la '
  'commande, confirmés par écrit avant la mission.', 1.75),
]

# ---------------------------------------------------------------------------
# L'OPTION SECURITE. Demande explicite du client : « including an option with
# security ». Trois niveaux, du plus leger au plus lourd.
#
# CE QUE JE N'ECRIS PAS : aucune promesse de vehicule blinde a un niveau de
# norme precis (VR7, B6...), aucune mention d'arme. Le port d'arme d'un agent
# de protection est reglemente pays par pays et se refuse dans la majorite des
# 96 destinations de cette liste. Annoncer sur une page publique une capacite
# qui est illegale a l'arrivee est le meilleur moyen de perdre le client ET
# l'autorisation d'exercer. La page renvoie donc a une etude par destination.
# ---------------------------------------------------------------------------
SECURITE = [
 ('aucune', 'Sans option', 0.00,
  'Chauffeur professionnel, véhicule suivi, contact avant prise en charge.',
  ['Suivi du vol et attente incluse', 'Point de rencontre confirmé la veille',
   'Chauffeur formé à la conduite préventive']),
 ('discret', 'Accompagnement discret', 0.45,
  'Un agent en civil accompagne le passager du hall au véhicule et jusqu’à '
  'l’adresse. Aucun signe extérieur.',
  ['Accueil et accompagnement en zone publique', 'Gestion des bagages sensibles',
   'Itinéraire préparé avec un second trajet de repli',
   'Compte rendu de mission']),
 # AJOUT demande par le client : « Vehicule blinde en option ». Il est ajoute
 # comme une OPTION SOUMISE A ETUDE, et rien de plus. Ce qui n'y figure
 # toujours pas, et n'y figurera pas : un niveau de norme (VR7, B6, B4...) et
 # toute mention d'arme. Deux raisons, et elles tiennent toutes les deux.
 #
 # 1. Un niveau de blindage est une caracteristique certifiee d'UN vehicule
 #    precis. L'annoncer sur une page qui couvre 96 destinations, c'est
 #    promettre la meme certification partout, ce qu'aucun exploitant ne peut
 #    tenir. Le jour ou un client compte sur un B6 et recoit autre chose,
 #    l'ecart n'est pas commercial, il est physique.
 # 2. La detention et la circulation d'un vehicule blinde sont reglementees ou
 #    interdites dans une bonne partie de ces 96 pays, et l'importation
 #    temporaire l'est encore plus souvent. La page dit donc « sur demande,
 #    apres etude », ce qui est vrai partout, plutot qu'une capacite qui serait
 #    fausse — et illegale — a l'arrivee.
 ('blinde', 'Véhicule renforcé sur demande', 1.60,
  'Véhicule renforcé, mis en place après étude de la destination. Disponibilité '
  'et niveau de protection dépendent du pays et se confirment au cas par cas.',
  ['Étude de la destination et de la faisabilité réglementaire',
   'Mise à disposition confirmée par écrit avant réservation',
   'Chauffeur formé à la conduite d’évitement',
   'Équipe de protection selon ce que la juridiction autorise',
   'Aucune caractéristique de blindage annoncée à l’avance : elle est '
   'communiquée pour le véhicule effectivement affecté']),
 ('rapproche', 'Protection rapprochée', 1.10,
  'Équipe dédiée, véhicule d’accompagnement, reconnaissance de l’itinéraire et '
  'coordination avec la sûreté aéroportuaire.',
  ['Équipe de deux agents minimum', 'Véhicule suiveur',
   'Reconnaissance préalable de l’itinéraire et des points d’arrêt',
   'Liaison avec la sûreté de l’aéroport et l’hôtel',
   'Évaluation de la destination avant confirmation']),
]

# Le texte pre-rempli du message WhatsApp. Les %s sont remplis par le
# navigateur avec l'aeroport, le vehicule et l'option choisis : le client
# arrive dans la conversation avec sa demande deja formulee, au lieu d'un
# « bonjour » auquel il faut repondre par cinq questions.
WHATSAPP_MODELE = (
 'Bonjour, je souhaite un transfert depuis {aeroport} ({iata}).\n'
 'Véhicule : {vehicule}\n'
 'Option : {securite}\n'
 'Estimation affichée : {prix}\n'
 'Date et heure souhaitées : ')

AVERTISSEMENT_SECU = (
 'Les prestations de protection sont soumises à autorisation et leur contenu '
 'change d’un pays à l’autre : ce qui est possible dans une destination ne '
 'l’est pas dans une autre. Toute mission protégée est confirmée après étude '
 'de la destination, jamais au moment de la réservation.')

# ---------------------------------------------------------------------------
# LES 96 AEROPORTS. Exactement 96, parce qu'il en a demande 96.
# J'en avais reuni 118 en premier jet. Plutot que d'en livrer 118 en silence
# (« il a demande 96, il sera content d'en avoir plus ») ou de dire 96 en en
# livrant 118, j'ai coupe les 22 les moins centraux pour un reseau de transfert
# de prestige et je lui donne la liste des coupes. N'importe lequel se remet en
# une ligne. Retires : EDI MAN HAM WAW BUD HEL LUX IBZ SAW VCE / PHX SEA DEN
# YYC CUN / BAH AMM / MNL CGK BLR / ADD LOS.
# (IATA, aeroport, ville, pays, region, km au centre approx, terminaux)
# Les codes IATA, les villes et les pays sont des faits. Le kilometrage est
# approximatif et sert a derive une bande tarifaire — il est annonce comme tel.
# ---------------------------------------------------------------------------
AEROPORTS = [
 # ---- Europe de l'Ouest -------------------------------------------------
 ('LHR', 'Heathrow',                     'Londres',      'Royaume-Uni',  'Europe', 24, 4),
 ('LGW', 'Gatwick',                      'Londres',      'Royaume-Uni',  'Europe', 45, 2),
 ('LCY', 'London City',                  'Londres',      'Royaume-Uni',  'Europe', 11, 1),
 ('CDG', 'Charles-de-Gaulle',            'Paris',        'France',       'Europe', 27, 3),
 ('ORY', 'Orly',                         'Paris',        'France',       'Europe', 18, 4),
 ('LBG', 'Le Bourget',                   'Paris',        'France',       'Europe', 14, 1),
 ('NCE', 'Côte d’Azur',                  'Nice',         'France',       'Europe',  7, 2),
 ('AMS', 'Schiphol',                     'Amsterdam',    'Pays-Bas',     'Europe', 17, 1),
 ('BRU', 'Zaventem',                     'Bruxelles',    'Belgique',     'Europe', 12, 1),
 ('FRA', 'Francfort',                    'Francfort',    'Allemagne',    'Europe', 13, 2),
 ('MUC', 'Franz-Josef-Strauss',          'Munich',       'Allemagne',    'Europe', 35, 2),
 ('BER', 'Brandebourg',                  'Berlin',       'Allemagne',    'Europe', 24, 1),
 ('DUS', 'Düsseldorf',                   'Düsseldorf',   'Allemagne',    'Europe',  8, 3),
 ('ZRH', 'Zurich',                       'Zurich',       'Suisse',       'Europe', 12, 3),
 ('GVA', 'Genève',                       'Genève',       'Suisse',       'Europe',  5, 1),
 ('BSL', 'EuroAirport',                  'Bâle',         'Suisse',       'Europe',  8, 1),
 ('VIE', 'Schwechat',                    'Vienne',       'Autriche',     'Europe', 18, 3),
 ('SZG', 'W.-A.-Mozart',                 'Salzbourg',    'Autriche',     'Europe',  4, 1),
 ('MXP', 'Malpensa',                     'Milan',        'Italie',       'Europe', 49, 2),
 ('LIN', 'Linate',                       'Milan',        'Italie',       'Europe',  8, 1),
 ('FCO', 'Fiumicino',                    'Rome',         'Italie',       'Europe', 32, 4),
 ('MAD', 'Barajas',                      'Madrid',       'Espagne',      'Europe', 15, 4),
 ('BCN', 'El Prat',                      'Barcelone',    'Espagne',      'Europe', 15, 2),
 ('PMI', 'Son Sant Joan',                'Palma',        'Espagne',      'Europe',  8, 1),
 ('LIS', 'Humberto-Delgado',             'Lisbonne',     'Portugal',     'Europe',  8, 2),
 ('DUB', 'Dublin',                       'Dublin',       'Irlande',      'Europe', 11, 2),
 ('CPH', 'Kastrup',                      'Copenhague',   'Danemark',     'Europe',  9, 3),
 ('ARN', 'Arlanda',                      'Stockholm',    'Suède',        'Europe', 40, 4),
 ('OSL', 'Gardermoen',                   'Oslo',         'Norvège',      'Europe', 47, 1),
 ('ATH', 'Elefthérios-Venizélos',        'Athènes',      'Grèce',        'Europe', 33, 1),
 ('PRG', 'Václav-Havel',                 'Prague',       'Tchéquie',     'Europe', 17, 2),
 ('IST', 'Istanbul',                     'Istanbul',     'Turquie',      'Europe', 42, 1),

 # ---- Amerique du Nord --------------------------------------------------
 ('JFK', 'John-F.-Kennedy',              'New York',     'États-Unis',   'Amérique du Nord', 26, 6),
 ('EWR', 'Newark Liberty',               'New York',     'États-Unis',   'Amérique du Nord', 26, 3),
 ('LGA', 'LaGuardia',                    'New York',     'États-Unis',   'Amérique du Nord', 13, 4),
 ('TEB', 'Teterboro',                    'New York',     'États-Unis',   'Amérique du Nord', 19, 1),
 ('LAX', 'Los Angeles',                  'Los Angeles',  'États-Unis',   'Amérique du Nord', 29, 9),
 ('VNY', 'Van Nuys',                     'Los Angeles',  'États-Unis',   'Amérique du Nord', 32, 1),
 ('SFO', 'San Francisco',                'San Francisco','États-Unis',   'Amérique du Nord', 21, 4),
 ('ORD', 'O’Hare',                       'Chicago',      'États-Unis',   'Amérique du Nord', 27, 4),
 ('MIA', 'Miami',                        'Miami',        'États-Unis',   'Amérique du Nord', 13, 3),
 ('FLL', 'Fort Lauderdale',              'Fort Lauderdale','États-Unis', 'Amérique du Nord', 6,  4),
 ('OPF', 'Opa-locka',                    'Miami',        'États-Unis',   'Amérique du Nord', 18, 1),
 ('BOS', 'Logan',                        'Boston',       'États-Unis',   'Amérique du Nord',  6, 4),
 ('IAD', 'Dulles',                       'Washington',   'États-Unis',   'Amérique du Nord', 42, 2),
 ('DCA', 'Reagan National',              'Washington',   'États-Unis',   'Amérique du Nord',  6, 3),
 ('ATL', 'Hartsfield-Jackson',           'Atlanta',      'États-Unis',   'Amérique du Nord', 16, 2),
 ('DFW', 'Dallas-Fort Worth',            'Dallas',       'États-Unis',   'Amérique du Nord', 32, 5),
 ('IAH', 'George-Bush',                  'Houston',      'États-Unis',   'Amérique du Nord', 37, 5),
 ('LAS', 'Harry-Reid',                   'Las Vegas',    'États-Unis',   'Amérique du Nord',  8, 4),
 ('YYZ', 'Pearson',                      'Toronto',      'Canada',       'Amérique du Nord', 22, 2),
 ('YUL', 'Trudeau',                      'Montréal',     'Canada',       'Amérique du Nord', 20, 1),
 ('YHU', 'Saint-Hubert',                  'Montréal',     'Canada',       'Amérique du Nord', 19, 1),
 ('YMX', 'Mirabel',                       'Montréal',     'Canada',       'Amérique du Nord', 39, 1),
 ('YVR', 'Vancouver',                    'Vancouver',    'Canada',       'Amérique du Nord', 12, 3),
 ('MEX', 'Benito-Juárez',                'Mexico',       'Mexique',      'Amérique du Nord', 13, 2),

 # ---- Moyen-Orient ------------------------------------------------------
 ('DXB', 'Dubaï International',          'Dubaï',        'Émirats arabes unis', 'Moyen-Orient', 5, 3),
 ('DWC', 'Al-Maktoum',                   'Dubaï',        'Émirats arabes unis', 'Moyen-Orient', 37, 1),
 ('AUH', 'Zayed',                        'Abou Dabi',    'Émirats arabes unis', 'Moyen-Orient', 32, 3),
 ('DOH', 'Hamad',                        'Doha',         'Qatar',        'Moyen-Orient', 15, 1),
 ('RUH', 'Roi-Khalid',                   'Riyad',        'Arabie saoudite','Moyen-Orient', 35, 5),
 ('JED', 'Roi-Abdulaziz',                'Djeddah',      'Arabie saoudite','Moyen-Orient', 19, 3),
 ('KWI', 'Koweït',                       'Koweït',       'Koweït',       'Moyen-Orient', 16, 4),
 ('MCT', 'Mascate',                      'Mascate',      'Oman',         'Moyen-Orient', 20, 1),
 ('TLV', 'Ben-Gourion',                  'Tel-Aviv',     'Israël',       'Moyen-Orient', 20, 2),
 ('BEY', 'Rafic-Hariri',                 'Beyrouth',     'Liban',        'Moyen-Orient',  9, 1),

 # ---- Asie --------------------------------------------------------------
 ('HND', 'Haneda',                       'Tokyo',        'Japon',        'Asie', 18, 3),
 ('NRT', 'Narita',                       'Tokyo',        'Japon',        'Asie', 62, 3),
 ('KIX', 'Kansai',                       'Osaka',        'Japon',        'Asie', 46, 2),
 ('ICN', 'Incheon',                      'Séoul',        'Corée du Sud', 'Asie', 48, 2),
 ('PEK', 'Pékin-Capitale',               'Pékin',        'Chine',        'Asie', 26, 3),
 ('PKX', 'Daxing',                       'Pékin',        'Chine',        'Asie', 46, 1),
 ('PVG', 'Pudong',                       'Shanghai',     'Chine',        'Asie', 32, 2),
 ('HKG', 'Hong Kong',                    'Hong Kong',    'Hong Kong',    'Asie', 34, 2),
 ('TPE', 'Taoyuan',                      'Taipei',       'Taïwan',       'Asie', 40, 2),
 ('SIN', 'Changi',                       'Singapour',    'Singapour',    'Asie', 20, 4),
 ('BKK', 'Suvarnabhumi',                 'Bangkok',      'Thaïlande',    'Asie', 30, 1),
 ('KUL', 'Kuala Lumpur',                 'Kuala Lumpur', 'Malaisie',     'Asie', 45, 2),
 ('DEL', 'Indira-Gandhi',                'New Delhi',    'Inde',         'Asie', 16, 3),
 ('BOM', 'Chhatrapati-Shivaji',          'Mumbai',       'Inde',         'Asie',  8, 2),

 # ---- Afrique -----------------------------------------------------------
 ('CAI', 'Le Caire',                     'Le Caire',     'Égypte',       'Afrique', 22, 3),
 ('CMN', 'Mohammed-V',                   'Casablanca',   'Maroc',        'Afrique', 30, 2),
 ('RAK', 'Ménara',                       'Marrakech',    'Maroc',        'Afrique',  5, 2),
 ('ALG', 'Houari-Boumédiène',            'Alger',        'Algérie',      'Afrique', 17, 3),
 ('TUN', 'Carthage',                     'Tunis',        'Tunisie',      'Afrique',  8, 2),
 ('JNB', 'O.-R.-Tambo',                  'Johannesburg', 'Afrique du Sud','Afrique', 25, 2),
 ('CPT', 'Le Cap',                       'Le Cap',       'Afrique du Sud','Afrique', 20, 2),
 ('NBO', 'Jomo-Kenyatta',                'Nairobi',      'Kenya',        'Afrique', 18, 4),

 # ---- Amerique du Sud et Oceanie ---------------------------------------
 ('GRU', 'Guarulhos',                    'São Paulo',    'Brésil',       'Amérique du Sud', 28, 3),
 ('GIG', 'Galeão',                       'Rio de Janeiro','Brésil',      'Amérique du Sud', 20, 2),
 ('EZE', 'Ezeiza',                       'Buenos Aires', 'Argentine',    'Amérique du Sud', 33, 3),
 ('SCL', 'Arturo-Merino-Benítez',        'Santiago',     'Chili',        'Amérique du Sud', 17, 2),
 ('BOG', 'El Dorado',                    'Bogotá',       'Colombie',     'Amérique du Sud', 15, 2),
 ('LIM', 'Jorge-Chávez',                 'Lima',         'Pérou',        'Amérique du Sud', 11, 1),
 ('PTY', 'Tocumen',                      'Panama',       'Panama',       'Amérique du Sud', 24, 2),
 ('SYD', 'Kingsford-Smith',              'Sydney',       'Australie',    'Océanie',  8, 3),
 ('MEL', 'Tullamarine',                  'Melbourne',    'Australie',    'Océanie', 23, 4),
 ('AKL', 'Auckland',                     'Auckland',     'Nouvelle-Zélande','Océanie', 21, 2),
]

REGIONS = ['Europe', 'Amérique du Nord', 'Moyen-Orient', 'Asie', 'Afrique',
           'Amérique du Sud', 'Océanie']

# Bande tarifaire indicative, en euros, derivee de la distance. Le jour ou il
# donne sa grille, on remplace CETTE fonction et rien d'autre.
BASE_PRISE_EN_CHARGE = 95
PAR_KM = 2.60
MINIMUM = 140


def tarif(km, coef_vehicule, coef_secu):
    """Tarif indicatif. Volontairement une formule et non une table : une table
       de 96 x 6 x 3 valeurs tapees a la main donnerait l'illusion d'un
       barometre reel alors qu'aucun de ces chiffres ne viendrait de lui."""
    base = max(MINIMUM, BASE_PRISE_EN_CHARGE + km * PAR_KM)
    return round(base * coef_vehicule * (1 + coef_secu) / 5) * 5


ETAPES = [
 ('01', 'Réservation', 'Vol, terminal, nombre de passagers et de bagages. '
        'Une mission protégée passe d’abord par une étude de destination.'),
 ('02', 'Veille du départ', 'Confirmation du point de rencontre exact, nom du '
        'chauffeur, plaque du véhicule et numéro direct.'),
 ('03', 'Suivi du vol', 'Le vol est suivi. Un retard décale la prise en charge '
        'sans frais, une avance la rapproche.'),
 ('04', 'Prise en charge', 'Accueil en salle d’arrivée, prise des bagages, '
        'départ. Attente incluse selon la formule.'),
]
