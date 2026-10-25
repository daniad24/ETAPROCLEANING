#!/usr/bin/env python3
"""
Generează paginile secundare ale site-ului ETA PRO CLEANING (fără dependențe).

    python3 tools/build.py

Conținutul (echipă, lucrări, articole, zone, abonamente) se modifică în listele de mai jos,
apoi se rulează din nou scriptul. Pagina principală (site/index.html) se editează direct.
Pozele: puneți fișierele în site/assets/img/ cu numele din câmpurile `img`. Până atunci
se afișează pozele demo din DEMO (Unsplash, licență gratuită).
"""
import json
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
BASE_URL = "https://etaprocleaning.ro"  # TODO: domeniul real, folosit în sitemap

def U(pid, w=1800):
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&q=80"

# ---------------------------------------------------------------- demo images
DEMO = {
    # pagina principală
    "vito.jpg": "1765461734605-34657fa04db2",
    "fortador-pro-max.png": "1708805282683-50a060eba80f",
    "cinematic-murdar.jpg": "1616196334411-1d8d09708ca6",
    "cinematic-curat.jpg": "1616196334411-1d8d09708ca6",
    "ba-scaune-inainte.jpg": "1602794351477-4b0a974fd386", "ba-scaune-dupa.jpg": "1602794351477-4b0a974fd386",
    "ba-mocheta-inainte.jpg": "1605437241278-c1806d14a4d9", "ba-mocheta-dupa.jpg": "1605437241278-c1806d14a4d9",
    "ba-motor-inainte.jpg": "1654616111851-5394318e3279", "ba-motor-dupa.jpg": "1654616111851-5394318e3279",
    "ba-plafon-inainte.jpg": "1652860316277-370ca5b1b1df", "ba-plafon-dupa.jpg": "1652860316277-370ca5b1b1df",
    "ba-piele-inainte.jpg": "1667893530449-e58102223524", "ba-piele-dupa.jpg": "1667893530449-e58102223524",
    "andy-popescu.jpg": "1618846446712-a4eda2adc05f",
    "andy-inainte.jpg": "1611251953880-611e66e904e9", "andy-dupa.jpg": "1611251953880-611e66e904e9",
    "luna-inainte.jpg": "1614530499660-fe1fbd7921d6", "luna-dupa.jpg": "1614530499660-fe1fbd7921d6",
    "luna-1.jpg": "1630312465536-5c6b1f76dc3f", "luna-2.jpg": "1605647381739-9bba88b1c5d1",
    "luna-3.jpg": "1713757554567-232a340261a0", "luna-4.jpg": "1611073819030-ac7216dd0022",
    # despre
    "despre-echipa.jpg": "1694678505383-676d78ea3b96",
    "echipa-horia.jpg": "1708805282683-50a060eba80f",
    "echipa-daniel.jpg": "1620584899131-a5ff5f8fbb03",
    # abonament / blog
    "care-hero.jpg": "1652860316277-370ca5b1b1df",
    "blog-abur-vs-spuma.jpg": "1633014041037-f5446fb4ce99",
    "blog-piele-iarna.jpg": "1667893530449-e58102223524",
    "blog-cat-de-des.jpg": "1605437241278-c1806d14a4d9",
    "zona-hero.jpg": "1765461734605-34657fa04db2",
}

# ---------------------------------------------------------------- content
ECHIPA = [
    {"nume": "Hagiu Horia", "img": "echipa-horia.jpg", "rol": "Rolul în echipă", "text": "Câteva rânduri despre Horia: de când face detailing, ce îi place cel mai mult la meserie."},
    {"nume": "Husanu Daniel", "img": "echipa-daniel.jpg", "rol": "Rolul în echipă", "text": "Câteva rânduri despre Daniel: de când face detailing, ce îi place cel mai mult la meserie."},
]

# Lucrări exemplu pentru portofoliu. Înlocuiți cu lucrările reale (titlu, poze, text).
LUCRARI = [
    {"slug": "lamborghini-aventador", "marca": "Lamborghini", "model": "Aventador", "tip": "Complet", "zona": "București",
     "extra": "Tratament piele", "cover": "1630312465536-5c6b1f76dc3f", "ba": "1611251953880-611e66e904e9",
     "gal": ["1618846446712-a4eda2adc05f", "1614530499660-fe1fbd7921d6", "1611073819030-ac7216dd0022"]},
    {"slug": "bmw-seria-5", "marca": "BMW", "model": "Seria 5", "tip": "Interior", "zona": "Sector 1",
     "extra": "Ozonizare", "cover": "1485291571150-772bcfc10da5", "ba": "1602794351477-4b0a974fd386",
     "gal": ["1605647381739-9bba88b1c5d1", "1616196334411-1d8d09708ca6", "1553818501-e9926ea1ea8f"]},
    {"slug": "mercedes-gle", "marca": "Mercedes-Benz", "model": "GLE", "tip": "Motor", "zona": "Pipera",
     "extra": "", "cover": "1554294314-80a5fb7e6bd5", "ba": "1654616111851-5394318e3279",
     "gal": ["1713757554567-232a340261a0", "1681529360408-9c5e6fee9a56", "1713757552498-e923a920e0d7"]},
    {"slug": "audi-a6", "marca": "Audi", "model": "A6", "tip": "Complet", "zona": "Sector 3",
     "extra": "Păr de animale", "cover": "1567808291548-fc3ee04dbcf0", "ba": "1605437241278-c1806d14a4d9",
     "gal": ["1652860316277-370ca5b1b1df", "1612066151982-130ba72c35b6", "1667893530449-e58102223524"]},
    {"slug": "volkswagen-golf", "marca": "Volkswagen", "model": "Golf", "tip": "Interior", "zona": "Sector 6",
     "extra": "Scaun de copil", "cover": "1520340356584-f9917d1eea6f", "ba": "1616196334411-1d8d09708ca6",
     "gal": ["1602794351477-4b0a974fd386", "1611251953880-611e66e904e9", "1605647381739-9bba88b1c5d1"]},
    {"slug": "porsche-cayenne", "marca": "Porsche", "model": "Cayenne", "tip": "Motor", "zona": "Otopeni",
     "extra": "", "cover": "1526550517342-e086b387edda", "ba": "1713757554567-232a340261a0",
     "gal": ["1654616111851-5394318e3279", "1713757552840-d4220a0c8f70", "1564519905873-975ffa367392"]},
]
for w in LUCRARI:
    s = w["slug"]
    DEMO[f"lucrare-{s}-cover.jpg"] = w["cover"]
    DEMO[f"lucrare-{s}-inainte.jpg"] = w["ba"]
    DEMO[f"lucrare-{s}-dupa.jpg"] = w["ba"]
    for i, g in enumerate(w["gal"], 1):
        DEMO[f"lucrare-{s}-{i}.jpg"] = g

ZONE = [
    {"slug": "sector-1", "nume": "Sectorul 1", "buc": True,
     "intro": "În Sectorul 1 lucrăm des în parcările blocurilor și la case, de la Băneasa până la Dorobanți. Venim cu duba echipată și curățăm mașina acolo unde este parcată.",
     "cart": ["Băneasa", "Aviatorilor", "Dorobanți", "Primăverii", "Domenii", "Bucureștii Noi", "Floreasca Nord"]},
    {"slug": "sector-2", "nume": "Sectorul 2", "buc": True,
     "intro": "Din Floreasca până în Pantelimon, venim la tine acasă sau la birou. Mulți clienți din Sectorul 2 ne cheamă în timpul programului, cât mașina stă oricum parcată.",
     "cart": ["Floreasca", "Tei", "Colentina", "Obor", "Iancului", "Pantelimon", "Ștefan cel Mare"]},
    {"slug": "sector-3", "nume": "Sectorul 3", "buc": True,
     "intro": "Titan, Dristor, Vitan: Sectorul 3 are multe mașini de familie folosite zilnic. Pentru ele, pachetul Interior cu abur scoate petele și mirosurile adunate în timp.",
     "cart": ["Titan", "Dristor", "Vitan", "Balta Albă", "Unirii", "Centrul Civic", "Industriilor"]},
    {"slug": "sector-4", "nume": "Sectorul 4", "buc": True,
     "intro": "În Berceni, Tineretului sau pe Olteniței, ne găsești la adresa ta. Ai nevoie doar de un loc unde putem lucra în jurul mașinii.",
     "cart": ["Berceni", "Tineretului", "Văcărești", "Olteniței", "Giurgiului", "Brâncoveanu"]},
    {"slug": "sector-5", "nume": "Sectorul 5", "buc": True,
     "intro": "De la Cotroceni la Rahova, curățăm mașina fără să o duci la spălătorie. Interior, motor sau complet, cu prețul confirmat înainte să venim.",
     "cart": ["Cotroceni", "Rahova", "13 Septembrie", "Ferentari", "Panduri", "Sebastian"]},
    {"slug": "sector-6", "nume": "Sectorul 6", "buc": True,
     "intro": "Drumul Taberei, Militari, Crângași: în Sectorul 6 venim des la blocuri și în parcările de birouri. Aburul curăță fără să ude scaunele, așa că mașina e gata în aceeași zi.",
     "cart": ["Drumul Taberei", "Militari", "Crângași", "Giulești", "Ghencea", "Lujerului"]},
    {"slug": "pipera", "nume": "Pipera", "buc": False,
     "intro": "În Pipera lucrăm atât la case, cât și în parcările clădirilor de birouri. Pentru firmele de aici avem și oferte pentru mai multe mașini în aceeași zi.",
     "cart": ["Pipera", "Voluntari", "Iancu Nicolae", "Petricani"]},
    {"slug": "otopeni", "nume": "Otopeni", "buc": False,
     "intro": "În Otopeni venim la case și în ansamblurile rezidențiale de lângă aeroport. Poți să ne lași mașina curățată înainte de un drum lung sau la întoarcere.",
     "cart": ["Otopeni", "Odăile", "Tunari"]},
    {"slug": "corbeanca", "nume": "Corbeanca", "buc": False,
     "intro": "Corbeanca are multe case cu curte și mașini mari de familie. Pachetul Complet curăță interiorul și motorul într-o singură vizită.",
     "cart": ["Corbeanca", "Tamași", "Ostratu", "Balotești"]},
    {"slug": "chiajna", "nume": "Chiajna", "buc": False,
     "intro": "În Chiajna și în ansamblurile de lângă Militari venim direct în parcare. Fără drum până la spălătorie și fără cozi în weekend.",
     "cart": ["Chiajna", "Roșu", "Dudu", "Militari Residence"]},
    {"slug": "popesti-leordeni", "nume": "Popești-Leordeni", "buc": False,
     "intro": "În Popești-Leordeni lucrăm la case și la blocurile noi. Spune-ne adresa, iar noi îți confirmăm prețul și costul deplasării.",
     "cart": ["Popești-Leordeni", "Berceni (Ilfov)", "Glina"]},
]

CARE = [
    {"nume": "Care Lunar", "ritm": "în fiecare lună", "pachet": "Interior", "pt": "Pentru mașina folosită zilnic, cu copii sau animale.",
     "inc": ["Pachetul Interior, o dată pe lună", "Aceeași zi și oră, dacă vrei", "Îți amintim noi de programare"]},
    {"nume": "Care Trimestrial", "ritm": "la fiecare 3 luni", "pachet": "Complet", "pt": "Pentru mașina ținută mereu în formă, interior și motor.", "top": True,
     "inc": ["Pachetul Complet, o dată la 3 luni", "Prioritate la programare", "Îți amintim noi de programare"]},
    {"nume": "Care Sezonier", "ritm": "primăvara și toamna", "pachet": "Complet", "pt": "Două vizite pe an, după iarnă și înainte de ea.",
     "inc": ["Pachetul Complet, de 2 ori pe an", "Curățare de sare și noroi după iarnă", "Pregătire pentru sezonul rece"]},
]

ARTICOLE = [
    {"slug": "de-ce-abur-si-nu-spuma", "img": "blog-abur-vs-spuma.jpg", "titlu": "De ce abur și nu spumă?",
     "rezumat": "Spuma și șamponul curăță la suprafață, dar lasă apă în scaune. Aburul desprinde murdăria cu căldură și folosește foarte puțină apă.",
     "corp": [
        ("p", "Multe spălătorii curăță interiorul cu spumă sau șampon pentru tapițerie. Arată bine în ziua aceea, dar problema apare după: o parte din apă și din detergent rămâne în buretele scaunului."),
        ("h2", "Ce se întâmplă cu spuma în scaune"),
        ("p", "Buretele absoarbe apa ca un burete de bucătărie. Dacă nu se usucă repede, mai ales iarna sau într-o mașină parcată la umbră, apare mirosul de umezeală. Reziduurile de detergent rămase în material atrag din nou praful, așa că pata revine mai repede."),
        ("h2", "Cum lucrează aburul"),
        ("p", "Aburul ajunge în fibre la temperatură ridicată și desprinde murdăria, grăsimea și urmele lipicioase. Pentru că este vapori, nu apă lichidă, materialul se umezește foarte puțin. Murdăria desprinsă se extrage imediat, iar suprafața se usucă repede."),
        ("ul", ["Folosește foarte puțină apă, deci uscare rapidă", "Nu are nevoie de chimicale agresive pentru majoritatea petelor", "Căldura ajută la igienizarea suprafețelor pe care le atingi zilnic: volan, mânere, centuri", "Ajunge în locuri greu accesibile: șine de scaune, aerisiri, cusături"]),
        ("h2", "Când mai folosim și altceva"),
        ("p", "Unele pete foarte vechi sau pătrunse adânc au nevoie de un pretratament cu o soluție potrivită materialului. Folosim produsele Fortador Car Cosmetics, apoi terminăm cu abur. Nu există o metodă universală, dar aburul face cea mai mare parte din muncă."),
        ("h2", "Pe scurt"),
        ("p", "Dacă vrei un interior curat care rămâne curat și nu miroase a umezeală după două zile, aburul este alegerea mai bună. De aceea lucrăm cu echipamente Fortador."),
     ]},
    {"slug": "pielea-iarna", "img": "blog-piele-iarna.jpg", "titlu": "Cum îți păstrezi pielea curată iarna",
     "rezumat": "Sarea, zăpada de pe încălțăminte și încălzirea în scaune sunt cei mai mari dușmani ai pielii. Câteva obiceiuri simple o țin ca nouă.",
     "corp": [
        ("p", "Iarna este sezonul cel mai greu pentru interioarele din piele. Pe lângă praf, apar sarea și apa topită de pe încălțăminte, iar încălzirea în scaune usucă pielea mai repede decât crezi."),
        ("h2", "Ce o afectează"),
        ("ul", ["Sarea de pe drum, care ajunge pe praguri și pe partea de jos a scaunelor", "Hainele ude lăsate pe bancheta din spate", "Căldura constantă din scaune, care usucă pielea", "Produsele universale de curățat, care pot lua stratul de protecție"]),
        ("h2", "Ce poți face singur"),
        ("ul", ["Șterge pielea o dată pe săptămână cu o lavetă din microfibră ușor umedă", "Evită soluțiile cu alcool sau detergenții de bucătărie", "Folosește covorașe de cauciuc cu margine, ca apa să nu ajungă pe mochetă", "Nu lăsa haine sau genți ude pe scaune peste noapte", "Hidratează pielea cu un produs dedicat la câteva săptămâni"]),
        ("h2", "Când e momentul unui detailing"),
        ("p", "Dacă vezi urme albe de sare, pielea a devenit aspră sau au apărut mici crăpături pe cusături, e momentul pentru o curățare în profunzime. Aburul scoate murdăria din porii pielii fără să o înmoaie, iar la final aplicăm un tratament de protecție."),
        ("p", "Ideal este un detailing complet la sfârșitul iernii, ca să scoți sarea și umezeala adunate în lunile reci."),
     ]},
    {"slug": "cat-de-des-detailing-interior", "img": "blog-cat-de-des.jpg", "titlu": "Cât de des ar trebui să faci detailing interior?",
     "rezumat": "Nu există un singur răspuns. Depinde cât folosești mașina, cine călătorește în ea și ce semne îți arată că e momentul.",
     "corp": [
        ("p", "Aspiratul de la benzinărie ține interiorul în ordine, dar nu ajunge în fibrele scaunelor, în plafon sau în aerisiri. Un detailing interior face asta. Întrebarea este cât de des."),
        ("h2", "O regulă simplă, după cum folosești mașina"),
        ("ul", ["Folosire ocazională, fără copii sau animale: de 2 ori pe an, primăvara și toamna", "Navetă zilnică sau mașină de familie: la 2-3 luni", "Copii mici, animale sau mâncat în mașină: lunar sau la 6 săptămâni", "Mașini de firmă, ride-sharing sau transport persoane: lunar"]),
        ("h2", "Semne că e momentul"),
        ("ul", ["Un miros care nu pleacă nici după aerisire", "Pete pe scaune sau pe plafon", "Geamurile se aburesc mai repede decât de obicei", "Praf care revine pe bord la câteva zile după ce l-ai șters", "Volanul și mânerele lipicioase la atingere"]),
        ("h2", "Între două detailinguri"),
        ("p", "Aspiră o dată la una-două săptămâni, șterge bordul și volanul cu o lavetă din microfibră și scoate gunoiul din mașină în fiecare zi. Astfel, fiecare detailing durează mai puțin și rezultatul se păstrează mai mult."),
        ("p", "Dacă nu vrei să ții tu socoteala, abonamentul ETA Care face asta pentru tine: îți amintim noi și venim la intervalul ales."),
     ]},
]

# ---------------------------------------------------------------- prețuri (SINGURA sursă)
# Interior: preț de bază pe treaptă (mașină mică) + supliment pe dimensiune.
# Motor: preț fix. Complet = (Interior + Motor) cu reducere, rotunjit în jos la 5 lei
# (clientul primește mereu cel puțin reducerea anunțată).
PRICING = {
    "interior": {"intretinere": 300, "standard": 450, "intensiv": 650},
    "supliment": {"s": 0, "m": 80, "l": 150},
    "motor": 200,
    "reducere_complet": 0.15,
    "rotunjire": 5,
    # Extra-uri pentru interior: preț fix fiecare. La nivelul Intensiv unele sunt incluse.
    "extra": {"ozon": 20, "par": 20, "copil": 20, "piele": 20, "miros": 20},
    "incluse_intensiv": ["ozon", "par", "copil"],
}
EXTRA_NAME = {"ozon": "Ozonizare", "par": "Păr de animale", "copil": "Scaun de copil", "piele": "Tratament piele", "miros": "Mirosuri persistente"}
PROGRAM = {"text": "Luni-Sâmbătă, 9:00-19:00", "zile": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "de_la": "09:00", "pana_la": "19:00"}
TIERS = [
    ("intretinere", "Întreținere", "Praf, urme ușoare, fără pete vizibile."),
    ("standard", "Standard", "Pete pe scaune sau mochetă, firimituri, mizerie adusă iarna."),
    ("intensiv", "Intensiv", "Pete vechi, păr de animale, mirosuri, noroi. Include ozonizare, păr de animale și scaun de copil."),
]
SIZE_KEYS = ["s", "m", "l"]
TIER_NAME = {k: n for k, n, _ in TIERS}

def price(plan, size, tier):
    P = PRICING
    interior = P["interior"][tier] + P["supliment"][size]
    if plan == "interior": return interior
    if plan == "motor": return P["motor"]
    full = interior + P["motor"]
    step = P["rotunjire"]
    return int(full * (1 - P["reducere_complet"]) // step * step)

def extras_text():
    inc = [EXTRA_NAME[k].lower() for k in PRICING["incluse_intensiv"]]
    prices = sorted(set(PRICING["extra"].values()))
    p = f"{prices[0]} lei fiecare" if len(prices) == 1 else "preț fix fiecare"
    names = ", ".join(EXTRA_NAME[k].lower() for k in PRICING["extra"])
    return (f"{names}, {p}. La nivelul Intensiv sunt incluse în preț: {', '.join(inc[:-1])} și {inc[-1]}. "
            "Extra-urile se adaugă doar la pachetele cu interior.")

def price_range(plan):
    vals = [price(plan, s, t) for s in SIZE_KEYS for t, _, _ in TIERS]
    return min(vals), max(vals)

def pricing_js():
    table = {pl: {s: {t: price(pl, s, t) for t, _, _ in TIERS} for s in SIZE_KEYS} for pl in ("interior", "motor", "complet")}
    data = {"table": table, "motor": PRICING["motor"], "discount": PRICING["reducere_complet"],
            "tiers": [{"key": k, "name": n, "desc": d} for k, n, d in TIERS],
            "extras": {k: {"name": EXTRA_NAME[k], "price": v} for k, v in PRICING["extra"].items()},
            "includedIntensiv": PRICING["incluse_intensiv"]}
    return ("/* GENERAT de tools/build.py din PRICING. Nu edita aici: schimbă prețurile în build.py. */\n"
            "window.ETA_PRICING = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")

def price_table(plan, compact=False):
    """3x3 table (size x tier). Motor has one fixed price."""
    if plan == "motor":
        return f'<div class="ptable ptable--single"><b>{PRICING["motor"]} <small>lei</small></b><span>Același preț pentru orice mașină și orice nivel de murdărie.</span></div>'
    head_row = "".join(f'<th scope="col">{n}</th>' for _, n, _ in TIERS)
    rows = "".join(
        f'<tr><th scope="row">{sn}{"" if compact else f"<small>{se}</small>"}</th>' + "".join(f"<td>{price(plan, sk, t)} <small>lei</small></td>" for t, _, _ in TIERS) + "</tr>"
        for sk, (sn, se) in zip(SIZE_KEYS, SIZES))
    return f'<div class="ptable"><table><thead><tr><th scope="col">Mașina</th>{head_row}</tr></thead><tbody>{rows}</tbody></table></div>'

def tiers_legend():
    return '<dl class="tiers-legend">' + "".join(f"<div><dt>{n}</dt><dd>{E(d)}</dd></div>" for _, n, d in TIERS) + "</dl>"

PRICE_NOTE = ("Încadrarea o faci tu, după cum vezi mașina. Dacă din poze apreciem altfel, îți scriem pe WhatsApp sau pe email "
              "înainte să venim și stabilim împreună treapta corectă.")

SERVICII = {
    "interior": dict(t="Detailing interior", h="Detailing interior cu abur, la tine acasă.", d="Curățăm habitaclul de la scaune la plafon cu abur Fortador. Venim cu duba echipată oriunde în București.",
        inc=["Aspirare completă, inclusiv portbagaj", "Abur pe plastic, console, bord și mânere", "Curățare scaune textile, mochetă și plafon", "Geamuri interior fără urme", "Protecție piele și plastic cu produse Fortador"],
        why=[("ph-cloud-fog", "Abur, nu chimicale agresive", "Aburul dizolvă murdăria și grăsimea din textile fără să le îmbibe cu apă."), ("ph-wind", "Uscare rapidă", "Folosim puțină apă, deci mașina se usucă repede și nu prinde miros."), ("ph-baby", "Sigur pentru copii", "Fără reziduuri agresive pe scaune și centuri.")]),
    "motor": dict(t="Detailing motor", h="Motor curat, fără apă sub presiune.", d="Degresăm compartimentul motor cu abur, cu zonele sensibile protejate. Venim la tine oriunde în București.",
        inc=["Degresare cu abur a întregului compartiment", "Curățare capace, furtunuri și carcase", "Protejarea zonelor electrice sensibile", "Tratament plastice și cauciucuri", "Finisaj mat, ca din fabrică"],
        why=[("ph-shield-check", "Fără apă sub presiune", "Aburul curăță fără să forțeze apa în conectori și senzori."), ("ph-magnifying-glass", "Vezi mai ușor scurgerile", "Pe un motor curat observi imediat orice pierdere de ulei sau lichid."), ("ph-tag", "Arată mai bine la vânzare", "Un motor curat lasă o impresie bună oricărui cumpărător.")]),
    "complet": dict(t="Detailing complet", h="Interior și motor, într-o singură vizită.", d="Pachetul complet: habitaclu și motor curățate cu abur Fortador, la un preț mai bun decât separat. Venim la tine în București.",
        inc=["Tot ce include pachetul Interior", "Tot ce include pachetul Motor", "Dezinfectare cu abur a suprafețelor", "Finisaj și verificare finală împreună cu tine"],
        why=[("ph-piggy-bank", "Mai avantajos", "Plătești mai puțin decât pentru cele două pachete luate separat."), ("ph-clock", "O singură programare", "Venim o dată și rezolvăm totul."), ("ph-sparkle", "Mașina ca nouă", "Ideal înainte de vânzare, după iarnă sau după un drum lung.")]),
}
SIZES = [("Mică", "Golf, Polo, A Class, Seria 1"), ("Medie", "C Class, Seria 3, A4, Passat"), ("Mare", "Seria 5 și 7, E și S Class, X5, XC90")]


# ---------------------------------------------------------------- icons (Phosphor, MIT) → site/icons.css
ICONS_DIR = Path(__file__).resolve().parent / "icons"

def icons_css():
    """Each Phosphor SVG becomes a CSS mask, so markup stays `<i class="ph ph-name"></i>`.
    Add a new icon by dropping its SVG (from @phosphor-icons/core) into tools/icons/."""
    from urllib.parse import quote
    rules = []
    for f in sorted(ICONS_DIR.glob("*.svg")):
        svg = " ".join(f.read_text(encoding="utf-8").split()).replace('"', "'")
        uri = "data:image/svg+xml," + quote(svg, safe=" '=:/,.-")
        name = f.stem
        sel = ".ph-fill.ph-" + name[:-5] if name.endswith("-fill") else ".ph-" + name
        rules.append(f'{sel}{{--ph:url("{uri}")}}')
    return ("/* GENERAT de tools/build.py din tools/icons/*.svg. Phosphor Icons (MIT), găzduite local. */\n"
            ".ph,.ph-fill{display:inline-block;font-style:normal;line-height:1;flex:none}\n"
            ".ph::before,.ph-fill::before{content:\"\";display:inline-block;width:1em;height:1em;vertical-align:-.125em;"
            "background-color:currentColor;-webkit-mask:var(--ph) center/contain no-repeat;mask:var(--ph) center/contain no-repeat}\n"
            + "\n".join(rules) + "\n")

def head_assets(root):
    """Shared <head> assets for every page, including index.html (injected between markers)."""
    return f'''<link rel="preload" href="{root}assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}fonts.css">
<link rel="stylesheet" href="{root}icons.css">
<link rel="icon" href="{root}assets/brand/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/brand/apple-touch-icon.png">
<link rel="manifest" href="{root}manifest.webmanifest">
<meta property="og:image" content="{BASE_URL}/assets/brand/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script src="{root}config.js"></script>
<script src="{root}pricing.js"></script>
<script src="{root}demo-images.js"></script>
<link rel="stylesheet" href="{root}styles.css">'''

def brand_img(root, size, cls="", alt=""):
    """Small raster logo (WebP, 2x/3x) instead of the heavy SVG at nav/footer sizes."""
    a, b = {44: (88, 132), 88: (176, 264)}[size]
    return (f'<img src="{root}assets/brand/logo-{a}.webp" srcset="{root}assets/brand/logo-{a}.webp 2x, {root}assets/brand/logo-{b}.webp 3x" '
            f'alt="{alt}" width="{size}" height="{size}"{cls}>')

# ---------------------------------------------------------------- layout
E = escape

def img(name, alt, root, cls="", lazy=True):
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img src="{root}assets/img/{name}" alt="{E(alt)}"{lz} '
            f'onerror="if(window.__img(this))return;this.closest(\'figure\')&&this.closest(\'figure\').classList.add(\'is-empty\');this.remove()"{cls}>')

def head(title, desc, root, ld=None):
    ldj = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0b0b0c">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:locale" content="ro_RO">
{head_assets(root)}{ldj}
</head>
<body class="sub">
'''

NAV = [("portofoliu.html", "Portofoliu"), ("eta-care.html", "ETA Care"), ("blog.html", "Blog"), ("despre.html", "Despre noi")]

def header(root, active="", home=False):
    h0 = "" if home else f"{root}index.html"  # on the home page, anchors stay in-page
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{root}{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    mitems = [(f"{h0}#pachete", "Pachete și prețuri"), (f"{h0}#rezultate", "Rezultate")] + [(root + h, t) for h, t in NAV] + [(f"{root}firme.html", "Firme și flote"), (f"{root}zone.html", "Zone deservite")]
    mlinks = "".join(f'<a href="{h}">{t}</a>' for h, t in mitems)
    h = f'''<header class="nav" id="nav">
  <div class="wrap nav__in">
    <a class="nav__brand" href="{h0 or '#top'}" aria-label="ETA PRO CLEANING, acasă">
      {brand_img(root, 44)}
      <span>ETA PRO <b>CLEANING</b></span>
    </a>
    <nav class="nav__links" aria-label="Principal">
      <a href="{h0}#pachete">Pachete</a>
      {links}
    </nav>
    <div class="nav__end">
      <a class="btn btn--primary btn--sm" href="{h0}#programare">Programează-te</a>
      <button class="nav__burger" id="burger" type="button" aria-label="Deschide meniul" aria-expanded="false" aria-controls="mnav"><i class="ph ph-list"></i></button>
    </div>
  </div>
  <nav class="mnav" id="mnav" aria-label="Meniu mobil" hidden>
    {mlinks}
    <a href="{h0}#programare">Programare</a>
  </nav>
</header>'''
    return h if home else h + "\n<main>\n"

# Date legale (Legea 365/2002, art. 5): denumire, sediu, nr. ORC, CUI, contact.
LEGAL = {
    "firma": "ETALON SECURITY SRL",
    "sediu": "Str. Cetatea de Baltă nr. 112-114, bl. 7, ap. 46, Sector 6, București, 060973",
    "orc": "J40/941/2002",
    "cui": "RO14444674",
    "euid": "ROONRC.J40/941/2002",
    "email": "contact@etaprocleaning.ro",  # TODO: adresa reală de email
}

def footer_block(root):
    zl = "".join(f'<li><a href="{root}zone/{z["slug"]}.html">{z["nume"]}</a></li>' for z in ZONE[:6])
    zi = "".join(f'<li><a href="{root}zone/{z["slug"]}.html">{z["nume"]}</a></li>' for z in ZONE[6:])
    L = LEGAL
    return f'''<footer class="foot">
  <div class="wrap foot__grid foot__grid--wide">
    <div class="foot__brand">
      {brand_img(root, 88, alt="ETA PRO CLEANING", cls=' loading="lazy"')}
      <p>Detailing auto mobil cu abur, cu echipamente Fortador. Venim la tine în București și Ilfov.</p>
    </div>
    <div>
      <h3>Servicii</h3>
      <ul>
        <li><a href="{root}servicii/interior.html">Detailing interior</a></li>
        <li><a href="{root}servicii/motor.html">Detailing motor</a></li>
        <li><a href="{root}servicii/complet.html">Detailing complet</a></li>
        <li><a href="{root}eta-care.html">Abonament ETA Care</a></li>
        <li><a href="{root}firme.html">Firme și flote</a></li>
        <li><a href="{root}tehnologie.html">Tehnologie Fortador</a></li>
      </ul>
    </div>
    <div>
      <h3>București</h3>
      <ul>{zl}</ul>
    </div>
    <div>
      <h3>Ilfov</h3>
      <ul>{zi}<li><a href="{root}zone.html">Toate zonele</a></li></ul>
    </div>
    <div>
      <h3>Contact</h3>
      <ul>
        <li><i class="ph ph-map-pin"></i> București, deplasare la client</li>
        <li><i class="ph ph-clock"></i> {PROGRAM["text"]}</li>
        <li><a href="#" data-phone><i class="ph ph-phone"></i> <span data-phone-label>0700 000 000</span></a></li>
        <li><a href="#" data-wa><i class="ph ph-whatsapp-logo"></i> WhatsApp</a></li>
        <li><a href="mailto:{L["email"]}"><i class="ph ph-envelope-simple"></i> {L["email"]}</a></li>
        <li><a href="{root}despre.html">Despre noi</a></li>
        <li><a href="{root}blog.html">Blog</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot__company">
    <p><b>ETA PRO CLEANING</b> este un serviciu operat de <b>{L["firma"]}</b></p>
    <dl>
      <div><dt>Sediu social</dt><dd>{L["sediu"]}</dd></div>
      <div><dt>Nr. Reg. Com.</dt><dd>{L["orc"]}</dd></div>
      <div><dt>CUI</dt><dd>{L["cui"]}</dd></div>
      <div><dt>EUID</dt><dd>{L["euid"]}</dd></div>
    </dl>
  </div>
  <div class="wrap foot__anpc">
    <a href="https://anpc.ro/sal" target="_blank" rel="noopener" class="anpc-sal" title="ANPC: Soluționarea alternativă a litigiilor"><img src="{root}assets/img/anpc-sal.png" alt="ANPC, Soluționarea alternativă a litigiilor" width="201" height="50" loading="lazy"></a>
  </div>
  <div class="wrap foot__legal">
    <p><a href="{root}termeni.html">Termeni și condiții</a> <a href="{root}confidentialitate.html">Politica de confidențialitate</a> <a href="{root}confidentialitate.html#cookies">Cookie-uri</a> <a href="https://anpc.ro/" target="_blank" rel="noopener">ANPC</a></p>
    <p>Fortador este marcă a producătorului său. LAMBORGHINI CALORECLIMA și mărcile asociate aparțin Ferroli S.p.A.; numele este folosit doar pentru a identifica componentele echipamentelor Fortador. Nu avem legătură cu Automobili Lamborghini.</p>
    <p>&copy; <span id="yr"></span> {L["firma"]}. Toate drepturile rezervate.</p>
  </div>
</footer>'''

def footer(root, lightbox=False):
    lb = '''
<dialog class="lightbox" id="lightbox" aria-label="Imagine mărită">
  <button class="dlg__x" type="button" data-close aria-label="Închide"><i class="ph ph-x"></i></button>
  <img alt="">
</dialog>''' if lightbox else ""
    return f'''</main>
{footer_block(root)}
<p class="demo-badge" aria-hidden="true">Poze demo Unsplash</p>
<nav class="mbar" aria-label="Acțiuni rapide">
  <a class="mbar__btn" href="#" data-phone><i class="ph ph-phone-call"></i><span>Sună</span></a>
  <a class="mbar__btn" href="#" data-wa><i class="ph ph-whatsapp-logo"></i><span>WhatsApp</span></a>
  <a class="mbar__cta" href="{root}index.html#programare">Programează-te</a>
</nav>{lb}
<script src="{root}sub.js" defer></script>
</body>
</html>
'''

def crumbs(root, items):
    parts = [f'<a href="{root}index.html">Acasă</a>']
    for href, label in items:
        parts.append(f'<a href="{href}">{E(label)}</a>' if href else f'<span aria-current="page">{E(label)}</span>')
    return '<nav class="crumbs" aria-label="Navigare">' + '<i class="ph ph-caret-right"></i>'.join(parts) + '</nav>'

def cta(root, title="Venim la tine cu duba echipată.", text="Spune-ne mașina și adresa, iar noi îți confirmăm prețul.", msg=None):
    second = f'<a class="btn btn--ghost" href="#" data-wa="{E(msg)}"><i class="ph ph-whatsapp-logo"></i> Scrie-ne pe WhatsApp</a>' if msg else \
             f'<a class="btn btn--ghost" href="{root}index.html#pachete">Vezi pachetele</a>'
    return f'''<section class="sec">
  <div class="wrap endcta reveal">
    <h2>{E(title)}</h2>
    <p class="lead">{E(text)}</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="{root}index.html#programare">Programează-te <i class="ph ph-arrow-right"></i></a>
      {second}
    </div>
  </div>
</section>
'''

def ba(name_before, name_after, alt):
    return f'''<div class="ba" data-ba>
  <figure class="ba__img ba__img--before" data-label="Poză ÎNAINTE"><img data-src="{name_before}" alt="{E(alt)}, înainte" loading="lazy"></figure>
  <figure class="ba__img ba__img--after" data-label="Poză DUPĂ"><img data-src="{name_after}" alt="{E(alt)}, după" loading="lazy"></figure>
  <span class="ba__tag ba__tag--l">Înainte</span>
  <span class="ba__tag ba__tag--r">După</span>
  <div class="ba__handle" aria-hidden="true"><i class="ph ph-arrows-left-right"></i></div>
  <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Compară înainte și după">
</div>'''

PROVIDER = {"@type": "AutoWash", "name": "ETA PRO CLEANING", "address": {"@type": "PostalAddress", "addressLocality": "București", "addressCountry": "RO"},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": PROGRAM["zile"], "opens": PROGRAM["de_la"], "closes": PROGRAM["pana_la"]}]}

# ---------------------------------------------------------------- pages
def page_despre():
    r = ""
    team = "".join(f'''
      <article class="team__card reveal" style="--d:{i * .08}s">
        <figure class="team__img slot-frame" data-label="Poză {E(m["nume"])}">{img(m["img"], m["nume"], r)}</figure>
        <h3>{E(m["nume"])}</h3>
        <p class="team__role" data-todo>{E(m["rol"])}</p>
        <p data-todo>{E(m["text"])}</p>
      </article>''' for i, m in enumerate(ECHIPA))
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs(r, [(None, "Despre noi")])}
    <h1>Doi oameni, o dubă și multă grijă pentru mașina ta.</h1>
    <p class="lead">Suntem ETA PRO CLEANING, o echipă de detailing mobil din București. Venim noi la tine, cu toate echipamentele în dubă.</p>
  </div>
</section>

<section class="sec sec--flush">
  <div class="wrap">
    <figure class="about__hero slot-frame reveal" data-label="Poză cu echipa și duba">{img("despre-echipa.jpg", "Echipa ETA PRO CLEANING la lucru", r)}</figure>
  </div>
</section>

<section class="sec">
  <div class="wrap about">
    <h2 class="reveal">Cum am pornit</h2>
    <div class="about__txt reveal">
      <p data-todo>Aici scrieți povestea voastră: cum ați început, de ce ați ales detailingul cu abur și de ce ați ales să veniți voi la client.</p>
      <p>Lucrăm cu echipamente Fortador și cu produse Fortador Car Cosmetics. Avem tot ce ne trebuie în duba noastră Vito, așa că putem curăța mașina acasă, la birou sau oriunde este parcată.</p>
    </div>
  </div>
</section>

<section class="sec sec--tint">
  <div class="wrap">
    <h2 class="reveal">Echipa</h2>
    <div class="team">{team}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="reveal">Ce ne ghidează</h2>
    <div class="values">
      <article class="reveal"><i class="ph ph-handshake"></i><h3>Preț clar de la început</h3><p>Îți confirmăm suma înainte să venim. Fără surprize la final.</p></article>
      <article class="reveal" style="--d:.06s"><i class="ph ph-eye"></i><h3>Verificăm împreună</h3><p>La predare ne uităm amândoi pe mașină. Dacă ceva nu e cum trebuie, revenim gratuit.</p></article>
      <article class="reveal" style="--d:.12s"><i class="ph ph-leaf"></i><h3>Abur, nu chimicale agresive</h3><p>Curățăm cu căldură și foarte puțină apă, cu produse care au fișe de securitate publice.</p></article>
    </div>
  </div>
</section>
{cta(r)}'''
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": "Despre ETA PRO CLEANING",
          "about": {**PROVIDER, "employee": [{"@type": "Person", "name": m["nume"]} for m in ECHIPA]}}
    return head("Despre noi | ETA PRO CLEANING, detailing mobil București", "Echipa ETA PRO CLEANING: detailing auto mobil cu abur, în București. Hagiu Horia și Husanu Daniel.", r, ld) + header(r, "despre.html") + body + footer(r)

def page_portofoliu():
    r = ""
    marci = sorted({w["marca"] for w in LUCRARI})
    tipuri = ["Interior", "Motor", "Complet"]
    chips = lambda key, vals: f'<div class="chips" data-filter="{key}" role="group"><button type="button" data-value="toate" aria-pressed="true">Toate</button>' + "".join(f'<button type="button" data-value="{E(v)}" aria-pressed="false">{E(v)}</button>' for v in vals) + '</div>'
    cards = "".join(f'''
      <a class="pf-card reveal" href="lucrari/{w["slug"]}.html" data-marca="{E(w["marca"])}" data-tip="{w["tip"]}">
        <figure class="pf-card__img slot-frame" data-label="Copertă">{img(f'lucrare-{w["slug"]}-cover.jpg', f'{w["marca"]} {w["model"]}', r)}</figure>
        <div class="pf-card__txt">
          <h3>{E(w["marca"])} {E(w["model"])}</h3>
          <p>{w["tip"]}{(" + " + E(w["extra"])) if w["extra"] else ""}<span>{E(w["zona"])}</span></p>
        </div>
      </a>''' for w in LUCRARI)
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs(r, [(None, "Portofoliu")])}
    <h1>Lucrări făcute de noi.</h1>
    <p class="lead">Fiecare mașină are pagina ei, cu poze înainte și după. Filtrează după marcă sau după tipul lucrării.</p>
    <p class="demo-note"><i class="ph ph-info"></i> Lucrările de mai jos sunt exemple cu poze demo și vor fi înlocuite cu lucrările voastre.</p>
  </div>
</section>
{luna_block(r)}
<section class="sec sec--flush pf-all">
  <div class="wrap">
    <h2 class="reveal pf-all__t">Toate lucrările</h2>
    <div class="pf-filters reveal">
      <div><span class="pf-filters__t">Marcă</span>{chips("marca", marci)}</div>
      <div><span class="pf-filters__t">Lucrare</span>{chips("tip", tipuri)}</div>
      <p class="pf-count" id="pf-count" aria-live="polite"></p>
    </div>
    <div class="pf-grid" id="pf-grid">{cards}
    </div>
    <div class="pf-empty" id="pf-empty" hidden>
      <i class="ph ph-magnifying-glass"></i>
      <p>Nicio lucrare pentru combinația aleasă.</p>
      <button class="btn btn--ghost btn--sm" type="button" id="pf-reset">Arată toate lucrările</button>
    </div>
  </div>
</section>
{cta(r, "Vrei ca mașina ta să fie următoarea?")}'''
    return head("Portofoliu | ETA PRO CLEANING, detailing mobil București", "Lucrări de detailing auto interior, motor și complet făcute de ETA PRO CLEANING în București și Ilfov.", r) + header(r, "portofoliu.html") + body + footer(r, lightbox=True)

def page_lucrare(w):
    r = "../"
    s = w["slug"]
    name = f'{w["marca"]} {w["model"]}'
    gal = "".join(f'<button class="gal__item{" gal__item--big" if i == 1 else ""}" data-label="Poză {i}"><img src="{r}assets/img/lucrare-{s}-{i}.jpg" alt="{E(name)}, detaliu {i}" loading="lazy"></button>' for i in range(1, len(w["gal"]) + 1))
    others = [o for o in LUCRARI if o["slug"] != s][:3]
    more = "".join(f'''<a class="pf-card" href="{o["slug"]}.html"><figure class="pf-card__img slot-frame" data-label="Copertă">{img(f'lucrare-{o["slug"]}-cover.jpg', f'{o["marca"]} {o["model"]}', r)}</figure><div class="pf-card__txt"><h3>{E(o["marca"])} {E(o["model"])}</h3><p>{o["tip"]}<span>{E(o["zona"])}</span></p></div></a>''' for o in others)
    body = f'''<section class="work-hero">
  <figure class="work-hero__img">{img(f"lucrare-{s}-cover.jpg", name, r, lazy=False)}</figure>
  <div class="wrap work-hero__in">
    {crumbs(r, [(r + "portofoliu.html", "Portofoliu"), (None, name)])}
    <h1>{E(name)}</h1>
    <dl class="work-facts">
      <div><dt>Lucrare</dt><dd>{w["tip"]}</dd></div>
      <div><dt>Extra</dt><dd>{E(w["extra"]) or "Fără"}</dd></div>
      <div><dt>Zonă</dt><dd>{E(w["zona"])}</dd></div>
    </dl>
  </div>
</section>
<section class="sec">
  <div class="wrap work">
    <div class="work__txt reveal">
      <h2>Ce am făcut</h2>
      <p data-todo>Exemplu de prezentare. Aici scrieți în ce stare era mașina, ce ați făcut concret și cum a arătat rezultatul.</p>
      <a class="btn btn--primary" href="{r}index.html#programare">Vreau și eu <i class="ph ph-arrow-right"></i></a>
    </div>
    <div class="reveal">{ba(f"{r}assets/img/lucrare-{s}-inainte.jpg", f"{r}assets/img/lucrare-{s}-dupa.jpg", name)}</div>
  </div>
  <div class="wrap"><div class="gal gal--work reveal">{gal}</div></div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <h2 class="reveal">Alte lucrări</h2>
    <div class="pf-grid pf-grid--3">{more}</div>
  </div>
</section>
{cta(r)}'''
    return head(f"{name}, detailing {w['tip'].lower()} | ETA PRO CLEANING", f"Detailing {w['tip'].lower()} pentru {name} în {w['zona']}, cu abur Fortador. Poze înainte și după.", r) + header(r, "portofoliu.html") + body + footer(r, lightbox=True)

def page_blog():
    r = ""
    first, rest = ARTICOLE[0], ARTICOLE[1:]
    card = lambda a, big=False: f'''
      <a class="post{" post--big" if big else ""} reveal" href="blog/{a["slug"]}.html">
        <figure class="post__img slot-frame" data-label="Copertă articol">{img(a["img"], a["titlu"], r)}</figure>
        <div class="post__txt"><h2>{E(a["titlu"])}</h2><p>{E(a["rezumat"])}</p><span class="post__more">Citește <i class="ph ph-arrow-right"></i></span></div>
      </a>'''
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs(r, [(None, "Blog")])}
    <h1>Ghiduri scurte despre îngrijirea mașinii.</h1>
    <p class="lead">Ce merită să știi ca să-ți păstrezi mașina curată mai mult timp.</p>
  </div>
</section>
<section class="sec sec--flush">
  <div class="wrap blog-grid">{card(first, True)}{"".join(card(a) for a in rest)}
  </div>
</section>
{cta(r)}'''
    return head("Blog | ETA PRO CLEANING, detailing auto", "Ghiduri despre detailing auto: abur sau spumă, îngrijirea pielii iarna, cât de des faci curățenie interioară.", r) + header(r, "blog.html") + body + footer(r)

def render_corp(corp):
    out = []
    for kind, val in corp:
        if kind == "p": out.append(f"<p>{E(val)}</p>")
        elif kind == "h2": out.append(f"<h2>{E(val)}</h2>")
        elif kind == "ul": out.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in val) + "</ul>")
    return "\n      ".join(out)

def page_articol(a):
    r = "../"
    others = [o for o in ARTICOLE if o["slug"] != a["slug"]]
    more = "".join(f'<li><a href="{o["slug"]}.html">{E(o["titlu"])} <i class="ph ph-arrow-right"></i></a></li>' for o in others)
    body = f'''<article>
<section class="page-hero page-hero--article">
  <div class="wrap wrap--read">
    {crumbs(r, [(r + "blog.html", "Blog"), (None, a["titlu"])])}
    <h1>{E(a["titlu"])}</h1>
    <p class="lead">{E(a["rezumat"])}</p>
  </div>
</section>
<div class="wrap wrap--read">
  <figure class="article__img slot-frame" data-label="Copertă articol">{img(a["img"], a["titlu"], r, lazy=False)}</figure>
  <div class="prose">
      {render_corp(a["corp"])}
  </div>
  <aside class="article__cta">
    <i class="ph ph-van"></i>
    <div><h2>Vrei să ne ocupăm noi?</h2><p>Venim cu duba echipată oriunde în București.</p></div>
    <a class="btn btn--primary" href="{r}index.html#programare">Programează-te</a>
  </aside>
  <nav class="article__more" aria-label="Alte articole"><h2>Alte articole</h2><ul>{more}</ul></nav>
</div>
</article>
'''
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["titlu"], "description": a["rezumat"], "inLanguage": "ro", "publisher": {"@type": "Organization", "name": "ETA PRO CLEANING"}}
    return head(f'{a["titlu"]} | Blog ETA PRO CLEANING', a["rezumat"], r, ld) + header(r, "blog.html") + body + footer(r)

def page_care():
    r = ""
    plans = "".join(f'''
      <article class="plan care{" plan--top" if p.get("top") else ""} reveal spot" style="--d:{i * .08}s">
        {'<span class="plan__flag">Cel mai ales</span>' if p.get("top") else ""}
        <h3>{p["nume"]}</h3>
        <p class="plan__d">{E(p["pt"])}</p>
        <p class="care__rate"><b>{E(p["ritm"])}</b><span>pachet {p["pachet"]}</span></p>
        <p class="care__price">Preț fix, stabilit pentru mașina ta</p>
        <ul class="ticks">{"".join(f'<li><i class="ph ph-check"></i>{E(x)}</li>' for x in p["inc"])}</ul>
        <a class="btn {"btn--primary" if p.get("top") else "btn--ghost"} btn--block" href="#" data-wa="Bună, mă interesează abonamentul {p["nume"]}. Mașina mea este: ">Cere prețul</a>
      </article>''' for i, p in enumerate(CARE))
    body = f'''<section class="page-hero page-hero--img">
  <figure class="page-hero__bg" aria-hidden="true">{img("care-hero.jpg", "", r, lazy=False)}</figure>
  <div class="wrap">
    {crumbs(r, [(None, "ETA Care")])}
    <h1>ETA Care. Mașina curată tot timpul, fără să te gândești.</h1>
    <p class="lead">Alegi ritmul, noi venim la intervalul stabilit. Preț fix și prioritate la programare.</p>
  </div>
</section>
<section class="sec sec--flush">
  <div class="wrap">
    <div class="plans plans--care">{plans}
    </div>
    <div class="dots" aria-hidden="true"></div>
    <p class="note reveal">Prețul abonamentului depinde de dimensiunea mașinii. Ți-l spunem pe WhatsApp, înainte de prima vizită.</p>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <h2 class="reveal">De ce abonament</h2>
    <div class="values">
      <article class="reveal"><i class="ph ph-lock-simple"></i><h3>Preț fix</h3><p>Știi de la început cât plătești, la fiecare vizită.</p></article>
      <article class="reveal" style="--d:.06s"><i class="ph ph-lightning"></i><h3>Prioritate</h3><p>Abonații primesc primele locuri libere din calendar.</p></article>
      <article class="reveal" style="--d:.12s"><i class="ph ph-bell-ringing"></i><h3>Îți amintim noi</h3><p>Te contactăm înainte de fiecare vizită. Tu doar confirmi.</p></article>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap faq">
    <h2 class="reveal">Întrebări despre abonament</h2>
    <div class="faq__list reveal">
      <details open><summary>Pot schimba ritmul abonamentului?</summary><p>Da. Spune-ne și trecem pe ritmul potrivit pentru tine.</p></details>
      <details><summary>Ce se întâmplă dacă nu sunt disponibil într-o lună?</summary><p>Mutăm vizita într-o zi care îți convine. Te contactăm înainte de fiecare programare.</p></details>
      <details><summary>Abonamentul include și extra-uri?</summary><p>Extra-urile, cum ar fi ozonizarea sau tratamentul pielii, le poți adăuga la orice vizită, la cerere.</p></details>
      <details><summary>Este valabil și în afara Bucureștiului?</summary><p>Da. În afara Bucureștiului adăugăm costul deplasării, pe care îl stabilim împreună de la început.</p></details>
    </div>
  </div>
</section>
{cta(r, "Hai să alegem ritmul potrivit.", "Scrie-ne mașina și cât de des o folosești. Îți recomandăm abonamentul și prețul.", "Bună, aș vrea detalii despre abonamentul ETA Care. Mașina mea este: ")}'''
    ld = {"@context": "https://schema.org", "@type": "Service", "name": "Abonament ETA Care", "serviceType": "Detailing auto periodic", "provider": PROVIDER, "areaServed": {"@type": "City", "name": "București"}}
    return head("Abonament ETA Care | Detailing auto periodic în București", "Abonament de detailing auto mobil: lunar, trimestrial sau sezonier. Preț fix și prioritate la programare.", r, ld) + header(r, "eta-care.html") + body + footer(r)

def page_zona(z):
    r = "../"
    nume = z["nume"]
    pret = "Deplasarea este inclusă în preț, ca oriunde în București." if z["buc"] else "Fiind în afara Bucureștiului, deplasarea se plătește separat. Costul îl stabilim împreună înainte de programare."
    def rng(k):
        lo, hi = price_range(k)
        return f"{lo} <small>lei</small>" if lo == hi else f"{lo}-{hi} <small>lei</small>"
    em = {"interior": "după mașină și nivel", "motor": "orice mașină", "complet": f"cu {int(PRICING['reducere_complet'] * 100)}% reducere"}
    rows = "".join(f'<div class="sp-price"><span>{k.capitalize()}</span><b>{rng(k)}</b><em>{em[k]}</em></div>' for k in ("interior", "motor", "complet"))
    near = [o for o in ZONE if o["slug"] != z["slug"] and o["buc"] == z["buc"]][:4]
    nearl = "".join(f'<a class="chip-link" href="{o["slug"]}.html">{o["nume"]}</a>' for o in near)
    body = f'''<section class="page-hero page-hero--img">
  <figure class="page-hero__bg" aria-hidden="true">{img("zona-hero.jpg", "", r, lazy=False)}</figure>
  <div class="wrap">
    {crumbs(r, [(r + "zone.html", "Zone"), (None, nume)])}
    <h1>Detailing auto mobil în {E(nume)}.</h1>
    <p class="lead">{E(z["intro"])}</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="{r}index.html#programare">Programează-te <i class="ph ph-arrow-right"></i></a>
      <a class="btn btn--ghost" href="#" data-wa="Bună, sunt din {E(nume)} și aș vrea o programare.">WhatsApp</a>
    </div>
  </div>
</section>
<section class="sec sec--flush">
  <div class="wrap zone-grid">
    <div class="reveal">
      <h2>Unde venim în {E(nume)}</h2>
      <ul class="zone-list">{"".join(f"<li><i class='ph ph-map-pin'></i>{E(c)}</li>" for c in z["cart"])}</ul>
      <p class="zone-note zone-note--inline"><i class="ph ph-{"check-circle" if z["buc"] else "path"}"></i> {E(pret)}</p>
    </div>
    <div class="reveal">
      <h2>Prețuri</h2>
      <div class="sp-prices sp-prices--stack">{rows}</div>
      <p class="note">Prețul exact depinde de dimensiunea mașinii și de nivelul de curățare. <a href="{r}index.html#pachete">Calculează-l aici.</a></p>
    </div>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <h2 class="reveal">Cum lucrăm la tine</h2>
    <div class="values">
      <article class="reveal"><i class="ph ph-chat-circle-dots"></i><h3>Ne scrii</h3><p>Mașina, adresa din {E(nume)} și, dacă vrei, câteva poze.</p></article>
      <article class="reveal" style="--d:.06s"><i class="ph ph-van"></i><h3>Venim cu duba</h3><p>Avem echipamentele Fortador la noi. Ai nevoie doar de un loc unde putem lucra în jurul mașinii.</p></article>
      <article class="reveal" style="--d:.12s"><i class="ph ph-key"></i><h3>Predăm împreună</h3><p>Verificăm rezultatul cu tine înainte să plecăm.</p></article>
    </div>
    <div class="zone-near reveal"><span>Lucrăm și în:</span>{nearl}<a class="chip-link" href="{r}zone.html">Toate zonele</a></div>
  </div>
</section>
{cta(r)}'''
    area = {"@type": "City", "name": nume} if z["buc"] else {"@type": "Place", "name": f"{nume}, Ilfov"}
    ld = {"@context": "https://schema.org", "@type": "Service", "name": f"Detailing auto mobil în {nume}", "serviceType": "Detailing auto mobil", "provider": PROVIDER, "areaServed": area}
    return head(f"Detailing auto mobil {nume} | ETA PRO CLEANING", f"Detailing auto mobil în {nume}: venim la tine cu abur Fortador. Interior, motor sau complet, cu preț clar.", r, ld) + header(r) + body + footer(r)

def page_zone():
    r = ""
    def group(title, items):
        return f'<div class="zones__g reveal"><h2>{title}</h2><div class="zones__list">' + "".join(f'<a class="zones__item spot" href="zone/{z["slug"]}.html"><b>{z["nume"]}</b><span>{E(", ".join(z["cart"][:3]))}</span><i class="ph ph-arrow-right"></i></a>' for z in items) + '</div></div>'
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs(r, [(None, "Zone deservite")])}
    <h1>Unde venim.</h1>
    <p class="lead">Lucrăm în tot Bucureștiul, cu deplasarea inclusă. În Ilfov și în alte localități venim cu deplasare contra cost, stabilită împreună.</p>
  </div>
</section>
<section class="sec sec--flush">
  <div class="wrap zones">
    {group("București", [z for z in ZONE if z["buc"]])}
    {group("Ilfov", [z for z in ZONE if not z["buc"]])}
    <p class="note reveal">Nu îți găsești localitatea? <a href="#" data-wa="Bună, veniți și în localitatea: ">Scrie-ne pe WhatsApp</a> și îți spunem dacă ajungem.</p>
  </div>
</section>
{cta(r)}'''
    return head("Zone deservite | ETA PRO CLEANING, detailing mobil", "Detailing auto mobil în toate sectoarele Bucureștiului și în Ilfov: Pipera, Otopeni, Corbeanca, Chiajna, Popești-Leordeni.", r) + header(r) + body + footer(r)

def page_serviciu(key):
    r = "../"
    v = SERVICII[key]
    lo, hi = price_range(key)
    disc = int(PRICING["reducere_complet"] * 100)
    pnote = {"interior": PRICE_NOTE, "motor": "Motorul are un singur preț, indiferent de mașină.",
             "complet": f"Complet = Interior + Motor, cu {disc}% reducere. " + PRICE_NOTE}[key]
    rows = price_table(key) + (tiers_legend() if key != "motor" else "") + f'<p class="note">{E(pnote)} Deplasarea în București este inclusă.</p>'
    inc = "".join(f'<li><i class="ph ph-check"></i>{x}</li>' for x in v["inc"])
    why = "".join(f'<article class="cell spot reveal"><i class="ph {i}"></i><h3>{a}</h3><p>{b}</p></article>' for i, a, b in v["why"])
    others = "".join(f'<a class="btn btn--ghost" href="{o}.html">{SERVICII[o]["t"]}</a>' for o in SERVICII if o != key)
    ld = {"@context": "https://schema.org", "@type": "Service", "name": v["t"], "serviceType": v["t"], "areaServed": {"@type": "City", "name": "București"}, "provider": PROVIDER,
          "offers": {"@type": "AggregateOffer", "priceCurrency": "RON", "lowPrice": str(lo), "highPrice": str(hi)}}
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs(r, [(r + "index.html#pachete", "Pachete"), (None, v["t"])])}
    <h1>{v["h"]}</h1>
    <p class="lead">{v["d"]}</p>
    <div class="sp-ptable">{rows}</div>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap sp-grid">
    <div class="reveal">
      <h2>Ce include</h2>
      <ul class="ticks sp-ticks">{inc}</ul>
    </div>
    <div class="sp-why">{why}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap endcta reveal">
    <h2>Venim la tine cu duba echipată.</h2>
    <p class="lead">Spune-ne mașina și adresa, iar noi îți confirmăm prețul.</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="{r}index.html#programare">Programează-te <i class="ph ph-arrow-right"></i></a>
      {others}
    </div>
  </div>
</section>
'''
    return head(f'{v["t"]} mobil în București | ETA PRO CLEANING', v["d"], r, ld) + header(r) + body + footer(r)


# ---------------------------------------------------------------- pages moved off the home page
LUNA = {  # Lucrarea lunii (sus în Portofoliu). TODO: lucrarea reală.
    "titlu": "Numele mașinii lucrate", "poveste": "Povestea pe scurt: în ce stare era mașina, ce am făcut și cât a durat.",
    "pachet": "Complet", "extra": "De completat", "zona": "București",
}

def luna_block(r):
    gal = "".join(f'<button class="gal__item{" gal__item--big" if i == 1 else ""}" data-label="Galerie {i}"><img src="{r}assets/img/luna-{i}.jpg" alt="Lucrarea lunii, detaliu {i}" loading="lazy"></button>' for i in range(1, 5))
    L = LUNA
    return f"""<section class="sec sec--flush" id="luna">
  <div class="wrap">
    <div class="luna luna--feature">
      <div class="luna__copy">
        <p class="eyebrow reveal">Lucrarea lunii</p>
        <h2 class="reveal" data-todo>{E(L["titlu"])}</h2>
        <p class="lead reveal" data-todo>{E(L["poveste"])}</p>
        <dl class="luna__facts reveal">
          <div><dt>Pachet</dt><dd>{E(L["pachet"])}</dd></div>
          <div><dt>Extra</dt><dd>{E(L["extra"])}</dd></div>
          <div><dt>Locație</dt><dd>{E(L["zona"])}</dd></div>
        </dl>
      </div>
      <div class="reveal">{ba(f"{r}assets/img/luna-inainte.jpg", f"{r}assets/img/luna-dupa.jpg", "Lucrarea lunii")}</div>
    </div>
    <div class="gal reveal">{gal}</div>
  </div>
</section>
"""

def page_tehnologie():
    r = ""
    body = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(r, [(None, "Tehnologie Fortador")])}
    <h1>Aburul face treaba grea. Tu primești rezultatul.</h1>
    <p class="lead">Lucrăm cu aparate Fortador, powered by Lamborghini, gândite pentru detailing profesional. Iată ce înseamnă asta pentru mașina ta.</p>
  </div>
</section>
<section class="sec sec--flush">
  <div class="wrap">
    <div class="bento">
      <article class="cell cell--machine reveal spot">
        <figure class="slot" data-label="Fotografie Fortador Pro Max">{img("fortador-pro-max.png", "Aparat de curățare cu abur Fortador Pro Max", r)}</figure>
        <div class="cell__txt">
          <h3>Fortador Pro Max</h3>
          <p>Linia Pro Max 4 în 1 reunește mai multe funcții într-un singur echipament, ca să lucrăm repede și curat în orice colț al habitaclului.</p>
        </div>
      </article>
      <article class="cell cell--hot reveal spot" style="--d:.06s"><i class="ph ph-cloud-fog"></i><h3>Abur la temperatură ridicată</h3><p>Dizolvă murdăria din țesături, plastic și piele fără să le îmbibe cu apă.</p></article>
      <article class="cell cell--line reveal spot" style="--d:.12s"><i class="ph ph-drop-half"></i><h3>Consum minim de apă</h3><p>Mai puțină umezeală înseamnă uscare rapidă și fără miros de igrasie.</p></article>
      <article class="cell cell--cert reveal spot" style="--d:.18s"><i class="ph ph-seal-check"></i><h3>Echipamente certificate</h3><p>Fortador are rapoarte Dekra și certificare IEC 60335-2-79.</p></article>
      <article class="cell cell--cosm reveal spot" style="--d:.24s"><i class="ph ph-spray-bottle"></i><h3>Fortador Car Cosmetics</h3><p>Interior Cleaner, Glass Cleaner, Leather Trim Protectant. Toate cu fișe de securitate.</p></article>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap how">
    <div class="how__media reveal" id="how-media">
      <figure class="how__img how__img--dirty" data-label="Poză: scaun murdar">{img("cinematic-murdar.jpg", "Scaun auto murdar, înainte de curățare", r)}</figure>
      <figure class="how__img how__img--clean" data-label="Poză: același scaun, curat">{img("cinematic-curat.jpg", "Același scaun auto după curățarea cu abur", r)}</figure>
      <div class="how__steam" aria-hidden="true"></div>
    </div>
    <div class="how__copy">
      <h2 class="reveal">Cum lucrează aburul.</h2>
      <ol class="how__steps reveal" id="how-steps">
        <li><button type="button"><b>Murdăria de zi cu zi</b><span>Praf, sare, pete de cafea și urme pe care aspiratorul nu le mai scoate.</span></button></li>
        <li><button type="button"><b>Aburul o dizolvă</b><span>Căldura desprinde petele din fibre, fără să ude buretele scaunului.</span></button></li>
        <li><button type="button"><b>Extragem tot</b><span>Murdăria nu rămâne în material, pleacă odată cu umezeala.</span></button></li>
        <li><button type="button"><b>Curat și uscat</b><span>Fără miros, gata de drum în aceeași zi.</span></button></li>
      </ol>
    </div>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <h2 class="reveal">Abur sau metode clasice</h2>
    <div class="values">
      <article class="reveal"><i class="ph ph-drop"></i><h3>Puțină apă</h3><p>Spuma și șamponul lasă apă în buretele scaunelor. Aburul folosește foarte puțină și se usucă repede.</p></article>
      <article class="reveal" style="--d:.06s"><i class="ph ph-flask"></i><h3>Fără chimicale agresive</h3><p>Căldura face cea mai mare parte din muncă. Produsele le folosim doar unde e nevoie.</p></article>
      <article class="reveal" style="--d:.12s"><i class="ph ph-plug"></i><h3>Sigur pe motor</h3><p>Nu forțăm apă sub presiune în conectori și senzori. Zonele sensibile sunt protejate.</p></article>
    </div>
    <p class="note reveal">Vrei detalii? Citește <a href="blog/de-ce-abur-si-nu-spuma.html">De ce abur și nu spumă</a>.</p>
  </div>
</section>
{cta(r)}"""
    return head("Tehnologie Fortador | ETA PRO CLEANING", "De ce lucrăm cu abur și echipamente Fortador: puțină apă, fără chimicale agresive, sigur pe motor.", r) + header(r) + body + footer(r)

def page_firme():
    r = ""
    msg = "Bună, aș vrea o ofertă pentru flota firmei. Numărul de mașini și tipul lor: "
    body = f"""<section class="page-hero page-hero--img">
  <figure class="page-hero__bg" aria-hidden="true">{img("vito.jpg", "", r, lazy=False)}</figure>
  <div class="wrap">
    {crumbs(r, [(None, "Firme și flote")])}
    <h1>Detailing pentru firme, la sediul vostru.</h1>
    <p class="lead">Venim cu duba echipată și curățăm mai multe mașini în aceeași zi, în parcarea firmei. Fără drumuri și fără mașini scoase din uz.</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="#" data-wa="{E(msg)}">Cere ofertă pentru firmă <i class="ph ph-arrow-right"></i></a>
    </div>
  </div>
</section>
<section class="sec sec--flush">
  <div class="wrap">
    <div class="values">
      <article class="reveal"><i class="ph ph-buildings"></i><h3>La sediul firmei</h3><p>Lucrăm în parcare, cât mașinile stau oricum. Angajații nu pierd timp.</p></article>
      <article class="reveal" style="--d:.06s"><i class="ph ph-garage"></i><h3>Mai multe mașini într-o zi</h3><p>Planificăm vizita ca să terminăm toată flota sau o parte din ea în aceeași zi.</p></article>
      <article class="reveal" style="--d:.12s"><i class="ph ph-receipt"></i><h3>Factură și contract</h3><p>Emitem factură pe firmă. Pentru vizite regulate, facem un contract cu preț stabilit.</p></article>
    </div>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap duo">
    <article class="duo__card duo__card--fleet reveal spot">
      <i class="ph ph-calendar-check"></i>
      <h2>Contract lunar</h2>
      <p>Vizite regulate pentru flotă, la intervalul ales de voi. Pentru contractele lunare oferim reducere.</p>
      <a class="btn btn--ghost" href="#" data-wa="{E(msg)}">Cere ofertă</a>
    </article>
    <article class="duo__card duo__card--gift reveal spot" style="--d:.08s">
      <i class="ph ph-gift"></i>
      <h2>Vouchere cadou pentru angajați</h2>
      <p>Un cadou util pentru echipă sau pentru clienți. Alegeți pachetul, noi trimitem voucherele.</p>
      <a class="btn btn--primary" href="#" data-wa="Bună, aș vrea vouchere cadou ETA PRO CLEANING. Număr și pachet: ">Comandă vouchere</a>
    </article>
  </div>
</section>
{cta(r, "Spuneți-ne câte mașini aveți.", "Vă trimitem o ofertă pentru flota voastră, cu preț și program.", msg)}"""
    ld = {"@context": "https://schema.org", "@type": "Service", "name": "Detailing auto pentru firme și flote", "serviceType": "Detailing auto flote", "provider": PROVIDER, "areaServed": {"@type": "City", "name": "București"}}
    return head("Detailing pentru firme și flote | ETA PRO CLEANING", "Detailing auto mobil pentru firme: venim la sediu și curățăm mai multe mașini în aceeași zi. Factură și contract lunar.", r, ld) + header(r) + body + footer(r)

def page_confidentialitate():
    r = ""
    L = LEGAL
    body = f"""<article>
<section class="page-hero page-hero--article">
  <div class="wrap wrap--read">
    {crumbs(r, [(None, "Politica de confidențialitate")])}
    <h1>Politica de confidențialitate</h1>
    <p class="lead">Cum folosim datele pe care ni le trimiți prin acest site. Pe scurt: doar ca să te programăm și să te contactăm.</p>
    <p class="note">Ultima actualizare: 8 octombrie 2026</p>
  </div>
</section>
<div class="wrap wrap--read">
  <div class="prose prose--legal">
    <h2>1. Cine suntem</h2>
    <p>Operatorul datelor este <b>{L["firma"]}</b>, cu sediul în {L["sediu"]}, înregistrată la Registrul Comerțului sub nr. {L["orc"]}, CUI {L["cui"]}. ETA PRO CLEANING este serviciul nostru de detailing auto mobil.</p>
    <p>Pentru orice întrebare despre datele tale ne poți scrie la <a href="mailto:{L["email"]}">{L["email"]}</a>.</p>

    <h2>2. Ce date colectăm</h2>
    <p>Prin formularul de programare și prin butonul „Sună-mă înapoi” ne poți trimite:</p>
    <ul>
      <li>numele și numărul de telefon;</li>
      <li>mașina (marca, modelul, dimensiunea și starea ei);</li>
      <li>adresa sau localitatea unde vrei să venim;</li>
      <li>poze cu mașina, dacă alegi să le adaugi;</li>
      <li>mesajul pe care ni-l scrii.</li>
    </ul>
    <p>Te rugăm să nu trimiți în poze alte persoane sau documente personale.</p>

    <h2>3. Cum ajung datele la noi</h2>
    <p>Site-ul nu salvează datele din formular pe un server. Când apeși „Trimite pe WhatsApp”, se deschide aplicația WhatsApp cu mesajul pregătit, iar tu decizi dacă îl trimiți. Din acel moment, mesajul este procesat și de WhatsApp (Meta), conform politicii lor de confidențialitate.</p>

    <h2>4. De ce le folosim și pe ce temei</h2>
    <ul>
      <li><b>Programare și ofertă:</b> ca să îți confirmăm prețul, ora și adresa. Temei: demersuri înainte de încheierea unui contract, la cererea ta (art. 6 alin. (1) lit. b din GDPR).</li>
      <li><b>Prestarea serviciului și facturare:</b> temei: executarea contractului și obligații legale fiscale (art. 6 alin. (1) lit. b și c).</li>
      <li><b>Poze în portofoliu:</b> publicăm poze cu mașina ta doar cu acordul tău explicit și fără date care te pot identifica (de exemplu numărul de înmatriculare acoperit). Temei: consimțământ (art. 6 alin. (1) lit. a), pe care îl poți retrage oricând.</li>
    </ul>
    <p>Nu folosim datele pentru reclame și nu le vindem nimănui.</p>

    <h2>5. Cât timp le păstrăm</h2>
    <p>Păstrăm conversațiile și datele de programare cât timp este necesar pentru serviciu și pentru eventuale reclamații. Documentele de facturare le păstrăm cât cer legile fiscale și contabile. Pozele publicate le ștergem la cerere.</p>

    <h2>6. Cui le transmitem</h2>
    <p>Datele nu sunt transmise altor firme, cu excepția furnizorilor care ne ajută să funcționăm (de exemplu WhatsApp pentru mesaje, contabilitatea pentru facturi) și a autorităților, când legea o cere.</p>

    <h2>7. Drepturile tale</h2>
    <p>Ai dreptul să ceri acces la datele tale, rectificarea sau ștergerea lor, restricționarea prelucrării, portabilitatea datelor și să te opui prelucrării. Dacă ți-ai dat consimțământul, îl poți retrage oricând. Scrie-ne la <a href="mailto:{L["email"]}">{L["email"]}</a> și îți răspundem în cel mult o lună.</p>
    <p>Dacă ai o nemulțumire, poți depune o plângere la Autoritatea Națională de Supraveghere a Prelucrării Datelor cu Caracter Personal (ANSPDCP), <a href="https://www.dataprotection.ro" target="_blank" rel="noopener">www.dataprotection.ro</a>.</p>

    <h2 id="cookies">8. Cookie-uri</h2>
    <p>Acest site nu folosește cookie-uri de urmărire sau de publicitate și nu are statistici de vizitare.</p>
    <p>Fonturile și iconițele sunt găzduite pe site. Unele poze de prezentare pot fi încărcate temporar de pe Unsplash, care poate vedea adresa IP a browserului tău, ca orice server care livrează un fișier, dar nu setează cookie-uri prin acest site.</p>

    <h2>9. Modificări</h2>
    <p>Dacă schimbăm această politică, actualizăm data de mai sus.</p>
  </div>
  <aside class="article__cta legal-note">
    <i class="ph ph-scales"></i>
    <div><h2>Notă</h2><p>Text pregătit ca punct de plecare. Recomandăm o verificare de către un consultant juridic înainte de publicare.</p></div>
  </aside>
</div>
</article>
"""
    return head("Politica de confidențialitate | ETA PRO CLEANING", f"Cum prelucrează {L['firma']} datele trimise prin site-ul ETA PRO CLEANING.", r) + header(r) + body + footer(r)


TERMENI = {  # TODO: completați după ce stabiliți
    "ore_anulare": 3,              # anunț minim pentru anulare / reprogramare, de ambele părți
    "plata": "Plata se face numerar, la predare, sau prin ordin de plată (transfer bancar), pe baza facturii.",
}

def page_termeni():
    r = ""
    L, T = LEGAL, TERMENI
    h = T["ore_anulare"]
    body = f"""<article>
<section class="page-hero page-hero--article">
  <div class="wrap wrap--read">
    {crumbs(r, [(None, "Termeni și condiții")])}
    <h1>Termeni și condiții</h1>
    <p class="lead">Regulile simple după care lucrăm: cum stabilim prețul, cum ne programăm și ce facem dacă intervine ceva.</p>
    <p class="note">Ultima actualizare: 8 octombrie 2026</p>
  </div>
</section>
<div class="wrap wrap--read">
  <div class="prose prose--legal">
    <h2>1. Cine prestează serviciul</h2>
    <p>Serviciile ETA PRO CLEANING sunt prestate de <b>{L["firma"]}</b>, cu sediul în {L["sediu"]}, Nr. Reg. Com. {L["orc"]}, CUI {L["cui"]}. Ne poți scrie la <a href="mailto:{L["email"]}">{L["email"]}</a> sau pe WhatsApp.</p>

    <h2>2. Serviciile</h2>
    <p>Oferim detailing auto mobil: curățare interior, curățare motor și pachetul complet, plus servicii extra la cerere. Venim cu echipamentele noastre la adresa indicată de tine.</p>

    <h2 id="preturi">3. Cum stabilim prețul</h2>
    <p>Prețul depinde de trei lucruri: pachetul ales, dimensiunea mașinii (mică, medie sau mare) și nivelul de curățare. Toate prețurile sunt fixe și afișate pe site. Nu lucrăm cu sume la întâmplare.</p>
    <p><b>Nivelurile de curățare</b> pentru interior sunt:</p>
    {tiers_legend()}
    <p><b>Interior</b>, în funcție de mașină și nivel:</p>
    {price_table("interior")}
    <p><b>Motor:</b> {PRICING["motor"]} lei, pentru orice mașină.</p>
    <p><b>Complet</b> (interior și motor) are o reducere de {int(PRICING["reducere_complet"] * 100)}% față de cele două luate separat, rotunjită în favoarea ta:</p>
    {price_table("complet")}
    <p>Încadrarea în nivel o faci tu, când trimiți cererea. Ne dorim ca ea să fie cât mai aproape de realitate, de aceea te rugăm să ne trimiți și câteva poze. <b>Dacă din poze apreciem alt nivel, îți scriem înainte de programare</b>, pe același canal pe care ne-ai contactat (WhatsApp sau email), și stabilim împreună treapta corectă. Așa nu pierde nimeni timp degeaba.</p>
    <p>Dacă nu ne-ai trimis poze și la sosire mașina corespunde altui nivel, îți spunem <b>înainte să începem</b>, iar tu decizi dacă mergem mai departe.</p>
    <p><b>Extra-uri pentru interior:</b> {extras_text()}</p>
    <p>Deplasarea în afara Bucureștiului se plătește separat. Costul îl stabilim împreună, înainte de programare.</p>

    <h2>4. Programarea</h2>
    <p>Trimiți cererea prin formularul de pe site, pe WhatsApp sau pe email. Programarea este confirmată doar după ce îți confirmăm noi ziua, ora și prețul. Fiecare cerere primește un număr de referință, pe care îl poți folosi în orice discuție cu noi.</p>
    <p>Lucrăm {PROGRAM["text"].lower().replace("luni-sâmbătă", "de luni până sâmbătă")}. Ai nevoie doar de un loc de parcare lângă mașină, unde putem lucra în jurul ei, și de acces la mașină pe durata lucrării.</p>

    <h2 id="anulare">5. Anulare și reprogramare</h2>
    <p>Dacă nu poți ajunge la programare, anunță-ne cu <b>cel puțin {h} ore înainte</b>, pe WhatsApp sau pe email. Același lucru ni-l asumăm și noi: dacă intervine ceva din partea noastră, te anunțăm cu cel puțin {h} ore înainte.</p>
    <p>În ambele cazuri stabilim împreună o nouă dată, pe WhatsApp sau pe email.</p>

    <h2>6. Plata și factura</h2>
    <p>{T["plata"]}</p>
    <p>Pentru fiecare lucrare emitem factură, pe persoană fizică sau pe firmă.</p>

    <h2>7. Garanția noastră</h2>
    <p>La final verificăm împreună rezultatul. Dacă ceva nu este cum trebuie, ne spui și revenim gratuit să rezolvăm.</p>

    <h2>8. Reclamații</h2>
    <p>Pentru orice nemulțumire scrie-ne la <a href="mailto:{L["email"]}">{L["email"]}</a>, cu numărul de referință al programării. Îți răspundem cât mai repede.</p>
    <p>Dacă nu ajungem la o înțelegere, te poți adresa Autorității Naționale pentru Protecția Consumatorilor, inclusiv prin procedura de soluționare alternativă a litigiilor: <a href="https://anpc.ro/sal" target="_blank" rel="noopener">anpc.ro/sal</a>.</p>

    <h2>9. Datele tale</h2>
    <p>Cum folosim datele pe care ni le trimiți este explicat în <a href="confidentialitate.html">Politica de confidențialitate</a>.</p>
  </div>
  <aside class="article__cta legal-note">
    <i class="ph ph-scales"></i>
    <div><h2>Notă</h2><p>Text pregătit ca punct de plecare. Recomandăm o verificare de către un consultant juridic înainte de publicare.</p></div>
  </aside>
</div>
</article>
"""
    return head("Termeni și condiții | ETA PRO CLEANING", f"Termenii în care {L['firma']} prestează serviciile ETA PRO CLEANING: prețuri, programare, anulare.", r) + header(r) + body + footer(r)

def index_tiers():
    btns = "".join(f'''
        <button type="button" class="tier" role="radio" aria-checked="false" data-tier="{k}"><b>{n}</b><span>{E(d)}</span></button>''' for k, n, d in TIERS)
    return f'''<div class="tiers reveal">
      <p class="tiers__t">Cât de murdar e interiorul?</p>
      <div class="tiers__row" role="radiogroup" aria-label="Nivel de curățare">{btns}
      </div>
      <p class="tiers__desc" id="tier-desc" aria-live="polite"></p>
      <p class="tiers__note">{E(PRICE_NOTE)}</p>
    </div>'''

def index_price_tables():
    disc = int(PRICING["reducere_complet"] * 100)
    return f'''<details class="allprices reveal">
      <summary>Vezi toate prețurile</summary>
      <div class="allprices__in">
        <div><h3>Interior</h3>{price_table("interior", compact=True)}</div>
        <div><h3>Complet <small>interior și motor, cu {disc}% reducere</small></h3>{price_table("complet", compact=True)}</div>
        <div><h3>Motor</h3>{price_table("motor")}</div>
        <div><h3>Extra-uri</h3><p class="note">{E(extras_text())}</p></div>
      </div>
    </details>'''

def inject_index_footer():
    """index.html is hand-edited; only its shared parts are injected between markers."""
    p = SITE / "index.html"
    s = p.read_text(encoding="utf-8")
    for key, html in (("HEAD", head_assets("")), ("HEADER", header("", home=True)), ("FOOTER", footer_block("")),
                      ("TIERS", index_tiers()), ("PRICETABLE", index_price_tables())):
        a, b = f"<!-- {key}:START (generat de tools/build.py) -->", f"<!-- {key}:END -->"
        i, j = s.index(a) + len(a), s.index(b)
        s = s[:i] + "\n" + html + "\n" + s[j:]
    p.write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- write
def write(rel, html):
    p = SITE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return rel

def demo_js():
    entries = ",\n    ".join(f'"{k}": "{U(v)}"' for k, v in DEMO.items())
    return f'''/* GENERAT de tools/build.py. Poze demo Unsplash (licență gratuită), folosite doar până apar
   pozele voastre în assets/img/. Un fișier local cu același nume are mereu prioritate.
   Ca să dezactivezi demo-ul complet, golește obiectul DEMO_IMAGES. */
window.DEMO_IMAGES = {{
    {entries}
}};
window.__img = function (img) {{
  if (img.dataset.demoTried) return false;
  var key = decodeURIComponent(new URL(img.src, location.href).pathname.split("/").pop());
  var url = window.DEMO_IMAGES[key];
  if (!url) return false;
  img.dataset.demoTried = "1";
  var box = img.closest("figure, button, .andy__bg");
  if (box) box.classList.add("is-demo");
  document.documentElement.classList.add("has-demo");
  img.src = innerWidth < 768 ? url.replace("w=1800", "w=900") : url;
  return true;
}};
'''

# Lista pozelor editabile din /admin (și lista permisă pentru încărcare, în api/_slots.json).
_BA = {"scaune": "Scaune textile", "mocheta": "Mochetă", "motor": "Motor", "plafon": "Plafon", "piele": "Piele"}
_FIX = {
    "vito.jpg": ("Pagina principală", "Duba Vito echipată"),
    "fortador-pro-max.png": ("Pagina principală", "Aparatul Fortador (fundal transparent, PNG)"),
    "cinematic-murdar.jpg": ("Pagina principală", "Animația cu abur: murdar"),
    "cinematic-curat.jpg": ("Pagina principală", "Animația cu abur: curat"),
    "andy-popescu.jpg": ("Pagina principală", "Andy Popescu: fundal"),
    "andy-inainte.jpg": ("Pagina principală", "Andy Popescu: înainte"),
    "andy-dupa.jpg": ("Pagina principală", "Andy Popescu: după"),
    "luna-inainte.jpg": ("Lucrarea lunii", "Înainte"),
    "luna-dupa.jpg": ("Lucrarea lunii", "După"),
    "despre-echipa.jpg": ("Despre noi", "Poza de echipă"),
    "echipa-horia.jpg": ("Despre noi", "Horia"),
    "echipa-daniel.jpg": ("Despre noi", "Daniel"),
    "care-hero.jpg": ("Alte pagini", "ETA Care: poza de sus"),
    "zona-hero.jpg": ("Alte pagini", "Zone: poza de sus"),
    "blog-abur-vs-spuma.jpg": ("Blog", "Articol: abur sau spumă"),
    "blog-piele-iarna.jpg": ("Blog", "Articol: pielea iarna"),
    "blog-cat-de-des.jpg": ("Blog", "Articol: cât de des"),
}

def slots():
    out = []
    for f in DEMO:
        if f in _FIX:
            g, l = _FIX[f]
        elif f.startswith("ba-"):
            _, k, side = f[:-4].split("-")
            g, l = "Înainte / după (pagina principală)", f"{_BA[k]}: {'înainte' if side == 'inainte' else 'după'}"
        elif f.startswith("luna-"):
            g, l = "Lucrarea lunii", f"Galerie, poza {f[5:-4]}"
        elif f.startswith("lucrare-"):
            w = next(x for x in LUCRARI if f.startswith(f"lucrare-{x['slug']}-"))
            part = f[len("lucrare-" + w["slug"]) + 1:-4]
            l = {"cover": "poza principală", "inainte": "înainte", "dupa": "după"}.get(part, f"galerie, poza {part}")
            g, l = f"Lucrare: {w['marca']} {w['model']}", l[0].upper() + l[1:]
        else:
            g, l = "Alte poze", f
        out.append({"file": f, "group": g, "label": l})
    return out

def slots_json():
    return json.dumps(slots(), ensure_ascii=False, indent=1) + "\n"

def main():
    out = [
        write("demo-images.js", demo_js()),
        write("icons.css", icons_css()),
        write("pricing.js", pricing_js()),
        write("despre.html", page_despre()),
        write("portofoliu.html", page_portofoliu()),
        write("blog.html", page_blog()),
        write("eta-care.html", page_care()),
        write("zone.html", page_zone()),
        write("tehnologie.html", page_tehnologie()),
        write("firme.html", page_firme()),
        write("confidentialitate.html", page_confidentialitate()),
        write("termeni.html", page_termeni()),
    ]
    inject_index_footer()
    out += [write(f"lucrari/{w['slug']}.html", page_lucrare(w)) for w in LUCRARI]
    out += [write(f"blog/{a['slug']}.html", page_articol(a)) for a in ARTICOLE]
    out += [write(f"zone/{z['slug']}.html", page_zona(z)) for z in ZONE]
    out += [write(f"servicii/{k}.html", page_serviciu(k)) for k in SERVICII]
    urls = ["index.html"] + [o for o in out if o.endswith(".html")]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{BASE_URL}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    api = SITE.parent / "api"
    api.mkdir(exist_ok=True)
    (api / "_slots.json").write_text(slots_json(), encoding="utf-8")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {BASE_URL}/sitemap.xml\n")
    print(f"{len(out)} fișiere generate în {SITE}")

if __name__ == "__main__":
    main()
