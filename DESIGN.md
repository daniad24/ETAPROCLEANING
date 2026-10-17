# ETA PRO CLEANING: design, reguli și cum au fost gândite

Documentul descrie site-ul așa cum e acum (10 octombrie 2026): ideea de design, regulile pe care le respectă fiecare pagină și motivul din spatele fiecărei decizii. Dacă adaugi o pagină sau o secțiune nouă, regulile de aici o țin în aceeași familie cu restul.

---

## 1. Ideea de bază

**Ce este site-ul:** pagina unei firme de detailing auto **mobil** din București. Clientul nu vine la voi, voi veniți la el cu duba echipată Fortador.

**Pentru cine:** oameni care își iubesc mașina sau n-au timp de spălătorie, care ajung pe site **în primul rând de pe telefon** (Google, Maps, Instagram, link trimis pe WhatsApp).

**Ce trebuie să simtă:** premium, dar clar și de încredere. Nu „spălătorie ieftină”, nu „agenție de design”. Ca un serviciu auto bun: tehnic, curat, sigur pe el.

**Ce trebuie să facă:** să ducă omul cât mai repede pe drumul
**văd → aflu prețul → am încredere → mă programez.**

Tot ce nu servește acest drum a fost mutat pe pagini secundare sau scos.

---

## 2. Principii (de unde pornesc toate regulile)

1. **Telefonul e primul.** Fiecare decizie se verifică întâi pe un ecran de 375 px. Calculatorul e o variantă mai largă, nu invers.
2. **Preț clar, fără surprize.** Prețuri fixe și exacte, niciodată „de la”. Clientul vede totalul înainte să trimită ceva.
3. **Adevărul înaintea efectului.** Nu inventăm cifre, recenzii, citate sau lucrări. Ce lipsește apare marcat ca „de completat” sau ca demo, nu ca fapt.
4. **Un singur lucru pe secțiune.** Fiecare secțiune are un mesaj. Dacă două secțiuni spun același lucru, se unesc.
5. **Mișcare doar cu motiv.** O animație trebuie să explice ceva (cum curăță aburul, că bara se poate trage, că s-a schimbat prețul). Nu animăm „ca să arate bine”.
6. **Nimic nu blochează derularea.** Am încercat o secțiune care fixa ecranul la scroll și am scos-o: omul trebuie să poată coborî oricât de repede vrea.
7. **O singură sursă pentru fiecare informație.** Prețurile, datele firmei, contactul, meniul și footerul se schimbă dintr-un singur loc și se propagă peste tot.

---

## 3. Identitate vizuală

### 3.1 Tema: întunecată, blocată

Site-ul are o singură temă, întunecată, pe toate paginile. Nu există variantă deschisă și nu există secțiuni care „trec pe alb” la jumătatea paginii.

**De ce:** logo-ul e un badge portocaliu pe cerc negru; pe fundal închis arată ca o insignă, pe alb arată lipit. Tema închisă dă și senzația de „atelier premium”, iar pozele cu mașini și aburul ies mult mai bine în evidență.

**Singura excepție:** scrisoarea de confirmare a programării e pe hârtie albă. E intenționat: e un document, nu o secțiune de site (vezi 6.10).

### 3.2 Culori

| Rol | Variabilă | Valoare | Unde se folosește |
|---|---|---|---|
| Fundal pagină | `--bg` | `#0b0b0c` | fundalul general (negru „cald”, nu negru pur) |
| Fundal secțiune alternativă | `--bg-2` | `#101012` | secțiunile „tint”, ca să se separe ritmic |
| Suprafață | `--surface` | `#151517` | carduri, formular, panouri |
| Suprafață ridicată | `--surface-2` | `#1b1b1e` | cardul „Complet” evidențiat |
| Linii | `--line` | alb 9% | contururi, separatoare |
| Text principal | `--text` | `#f3f1ed` | titluri și text (alb ușor cald, nu alb pur) |
| Text secundar | `--muted` | `#a9a59e` | descrieri, etichete |
| **Accent** | `--accent` | `#f6a419` | butoane principale, prețuri, iconițe, selecții |
| Accent 2 | `--accent-2` | `#f78618` | doar în gradienți, lângă accent |
| Text pe accent | `--on-accent` | `#1a1000` | textul de pe butoanele portocalii |

**Reguli:**
- **Un singur accent: portocaliul din logo.** Nu apare nicio altă culoare de accent pe site. Excepție funcțională: verdele WhatsApp pe butonul WhatsApp, pentru că oamenii îl recunosc instant.
- Portocaliul marchează **ce e important sau selectat**: butonul principal, prețul, opțiunea aleasă. Dacă totul e portocaliu, nimic nu mai iese în evidență.
- Fără negru pur `#000` și fără alb pur `#fff`: dau un contrast „ieftin”, ca de ecran neconfigurat.
- Textul de pe butoanele portocalii e aproape negru, nu alb: are contrast mult mai bun (lizibil pe orice telefon, în soare).

### 3.3 Tipografie

| Rol | Font | Greutăți | Folosire |
|---|---|---|---|
| Titluri | **Outfit** | 500-800 | H1, H2, prețuri, nume de pachete |
| Text | **Geist** | 300-600 | paragrafe, butoane, formulare |
| Etichete tehnice | **Geist Mono** | 400-500 | eticheta mică de deasupra unor titluri, numărul de referință |

**De ce aceste fonturi:** Outfit e geometric și prietenos, cu un aer „auto / tehnic” fără să fie rece. Geist e foarte lizibil la dimensiuni mici pe telefon. Am evitat intenționat Inter (fontul „default” al tuturor site-urilor generate) și fonturile cu serife, care ar fi dat un aer de restaurant sau revistă, nu de serviciu auto.

**Reguli:**
- Titlurile sunt mari și strânse (litere ușor apropiate), textul e aerisit (înălțime de rând 1.6).
- Titlul din prima secțiune are spațiu suplimentar între rânduri, pentru diacritice (ș, ț, ă). Am mărit spațierea după observația ta despre „spațierea textului din introducere”.
- Paragrafele au o lățime maximă (aprox. 55-65 de caractere pe rând), ca să se citească ușor.
- Accentul într-un titlu se face cu **culoarea** din același font (ex. „Detailing cu **abur**”), nu cu alt font.
- Etichetele mici de deasupra titlurilor (ex. „PACHETE ȘI PREȚURI”) sunt folosite rar, cam una la trei secțiuni. Altfel toate secțiunile arată la fel.

**Tehnic:** fonturile sunt găzduite pe site (nu de la Google), doar cu literele latine și românești (~130 KB în total). Până se încarcă, browserul afișează Arial / Courier **ajustate la exact aceleași dimensiuni**, ca textul să nu „sară” când apare fontul real.

### 3.4 Forme (colțuri)

Un singur sistem, aplicat peste tot:

| Element | Rotunjire |
|---|---|
| Butoane, etichete, selectoare mici | complet rotunjite („pastilă”) |
| Carduri, panouri, poze | 24 px |
| Câmpuri de formular | 14 px |

Nu amestecăm colțuri drepte cu colțuri rotunde. Excepție: scrisoarea de confirmare are colțuri aproape drepte (6 px), ca o foaie de hârtie.

### 3.5 Iconițe

- O singură familie: **Phosphor**, varianta „regular”, cu o singură excepție „fill” (logo-ul WhatsApp).
- Sunt găzduite pe site: doar cele ~60 folosite, într-un singur fișier mic (`icons.css`, ~11 KB comprimat), nu toată biblioteca de 1500.
- Iconițele au mereu culoarea accentului sau a textului din jur. Nu desenăm iconițe „de mână”.
- Pentru o iconiță nouă: se pune SVG-ul din Phosphor în `tools/icons/` și se rulează generatorul.

### 3.6 Logo

- **Logo-ul mare** (SVG, calitate maximă) apare o singură dată: în prima secțiune, plutind ușor, cu un inel subțire în jur și abur în spate.
- **Logo-ul mic** din meniu, footer și scrisoare e o imagine WebP (4-10 KB), pentru că desenul SVG e foarte complex și se randează greu la dimensiuni mici.
- Iconițe pentru telefon (ecran principal, tab browser) și imaginea de distribuire pe WhatsApp / Facebook sunt generate din același logo, pe fundalul negru al site-ului.
- Logo-ul nu se modifică, nu se recolorează și nu se pune pe fundal deschis.

### 3.7 Imagini

- Acum sunt **poze demo de pe Unsplash** (gratuite legal), marcate cu eticheta „Poze demo Unsplash” în colțul ecranului. Pozele voastre le înlocuiesc automat când sunt puse în `site/assets/img/` cu numele din `POZE-NECESARE.md`.
- La perechile înainte / după, „înainte” e momentan aceeași poză „murdărită” artificial, doar pentru prezentare.
- **Reguli pentru pozele reale:**
  - înainte / după: același unghi, aceeași distanță, ideal telefonul sprijinit;
  - lumină de umbră sau garaj, nu soare direct;
  - fără persoane sau numere de înmatriculare vizibile (sau acoperite);
  - pozele cu Andy doar cu acordul lui.
- Nu punem text sau etichete peste poze, cu excepția „Înainte / După” din slider, care sunt funcționale.

---

## 4. Așezare în pagină

- **Lățime de conținut:** maxim 1240 px, centrat. Margini laterale: 16 px pe telefon, 32 px pe calculator.
- **Spațiu între secțiuni:** generos pe calculator (aprox. 80-144 px), redus pe telefon (aprox. 58 px), ca pagina să nu devină interminabilă.
- **Ritm:** secțiunile alternează între fundalul de bază și cel puțin mai deschis (`--bg-2`), ca ochiul să simtă trecerea dintre ele fără linii groase.
- **Variație:** nu repetăm același tip de așezare de mai multe ori la rând (de ex. „poză stânga, text dreapta” de trei ori). Folosim alternativ: grilă de carduri, poză + listă, slider pe toată lățimea, două coloane, listă simplă.
- **Grile, nu calcule:** toate așezările pe coloane sunt grile CSS care, sub 768 px, devin o singură coloană (sau carusel, unde e mai bun).

**Puncte de trecere (breakpoints):** 768 px separă telefonul de restul; 900 px afișează meniul complet; 960-1000 px trec secțiunile pe două coloane.

---

## 5. Structura site-ului

### 5.1 Pagina principală (după simplificare)

| # | Secțiune | Rol |
|---|---|---|
| 1 | Prima secțiune (hero) | Ce faceți și unde, în 2 rânduri + 2 butoane |
| 2 | Banda „Andy Popescu ne recomandă” | Încredere imediat, sub primul ecran |
| 3 | Venim noi la tine | Cum lucrați (4 pași) + garanția „revenim gratuit” |
| 4 | Rezultate | Slider înainte / după, pe categorii |
| 5 | Pachete | Mașina + nivelul → 3 carduri cu preț exact + toate prețurile |
| 6 | Andy Popescu | Povestea recomandării + mașina lui |
| 7 | Întrebări frecvente | 5 întrebări esențiale |
| 8 | Programare | Rezumatul comenzii (configurator) + formular |

**Cum s-a ajuns aici:** pagina avea 15 secțiuni și părea încărcată. Problema nu era numărul, ci repetiția: trei secțiuni explicau procesul, două arătau rezultate, iar prețul apărea în două calculatoare. Le-am unit și am mutat restul pe pagini dedicate. Pagina principală are acum ~10.000 px pe telefon (de la ~18.000).

### 5.2 Pagini secundare

- **Servicii:** Interior, Motor, Complet, fiecare cu tabelul de prețuri.
- **Portofoliu:** grilă de lucrări cu filtre (marcă, tip), Lucrarea lunii sus; fiecare lucrare are pagina ei.
- **ETA Care:** abonamente (Lunar, Trimestrial, Sezonier).
- **Firme și flote:** detailing la sediu, contract lunar, vouchere pentru angajați.
- **Tehnologie Fortador:** echipamentele + animația „Cum lucrează aburul”.
- **Despre noi:** Hagiu Horia și Husanu Daniel, povestea, valorile.
- **Blog:** 3 ghiduri scurte.
- **Zone:** o pagină cu toate zonele + 11 pagini locale (sectoarele 1-6, Pipera, Otopeni, Corbeanca, Chiajna, Popești-Leordeni), fiecare cu text propriu.
- **Termeni și condiții**, **Politica de confidențialitate**.

Toate paginile secundare au același meniu, același footer și aceeași bară de jos pe telefon.

---

## 6. Componente

### 6.1 Butoane
- **Principal** (portocaliu plin): o singură acțiune principală pe ecran. Eticheta e mereu **„Programează-te”**, peste tot, ca să nu existe două texte pentru aceeași acțiune.
- **Secundar** (contur subțire, transparent): acțiuni alternative („Vezi pachetele”).
- La apăsare se „afundă” ușor, la trecerea cu mouse-ul se ridică 2 px.
- Textul butonului încape mereu pe un rând.

### 6.2 Meniu
- Pe calculator: logo, 5 linkuri, buton „Programează-te”. Devine semi-transparent cu blur după ce începi să derulezi.
- Pe telefon: logo + buton ☰. Butonul „Programează-te” din meniu e ascuns, pentru că există bara de jos.

### 6.3 Bara de jos (doar pe telefon)
Fixă jos, la îndemâna degetului: **Sună-mă**, **WhatsApp**, **Programează-te**. Dispare cât timp formularul e pe ecran sau meniul e deschis, ca să nu dubleze butoanele.

### 6.4 Butoane plutitoare (calculator)
„Sună-mă înapoi” + WhatsApp, în colțul din dreapta jos, apar după prima secțiune și dispar când ajungi la formular.

### 6.5 Slider înainte / după
- Poza e tăiată pe din două; tragi bara (cu mouse-ul, degetul sau săgețile de la tastatură).
- Când apare pe ecran, bara se mișcă singură o dată, ca vizitatorul să înțeleagă că poate trage.
- Etichetele „Înainte” (stânga) și „După” (dreapta, portocaliu).

### 6.6 Alegerea mașinii și a nivelului
- **Căutare de mașină** cu ~230 de modele: scrii „bmw seria 3” sau „golf” și mașina se încadrează automat în mică / medie / mare.
- **Dimensiune:** 3 butoane (Mică, Medie, Mare) cu exemple de modele.
- **Nivel de curățare:** Întreținere, Standard, Intensiv, fiecare cu o descriere concretă („pete vechi, păr de animale…”), ca încadrarea să fie obiectivă. Numele sunt „premium” intenționat: e mai ușor să alegi „Intensiv” decât să recunoști că mașina e „foarte murdară”.

### 6.7 Cardurile de preț
- 3 carduri: Interior, Complet (evidențiat, „Cel mai complet”), Motor.
- Prețul e **exact**, pentru mașina și nivelul alese, și se schimbă animat (cifrele „curg”).
- La Complet se vede prețul întreg tăiat și „Economisești X lei”.
- Pe telefon devin **carusel cu swipe**, deschis direct pe Complet, cu puncte care arată unde ești.

### 6.8 Configuratorul (rezumatul comenzii)
- Silueta mașinii (hatchback / sedan / SUV după dimensiune) în care **se aprind zonele curățate**: plafon, bord, scaune, mochetă, motor.
- Lângă ea: pachetul, nivelul, extra-urile, reducerea, deplasarea și **totalul**.
- Stă lângă formular, ca rezumat viu: tot ce alegi se vede imediat.

### 6.9 Formularul
- Pe calculator: 4 coloane compacte, încape în ecran chiar și pe un laptop de 720 px înălțime.
- Pe telefon: o coloană, câmpuri mari, tastatura potrivită (cifre la telefon).
- **Poze:** pe telefon două butoane mari, „Fă poze” (camera) și „Din galerie”, plus o listă cu ce poze ajută (scaune față, banchetă, mochetă, portbagaj, motor doar dacă e cazul). Pe calculator: zonă în care tragi pozele.
- Erori clare sub câmp, etichete mereu deasupra câmpului (nu înăuntru).

### 6.10 Scrisoarea de confirmare
După „Vezi rezumatul și trimite” apare un **document pe hârtie albă**: antet cu logo, număr de referință (`ETA-261009-XXXX`), dată, „Mulțumim, Andrei.”, rezumatul, totalul, semnătura „Hagiu Horia și Husanu Daniel” și o ștampilă care trece din „Netrimisă încă” în „Trimisă”.
**De ce hârtie:** e momentul în care clientul „semnează” cererea; un document îl face să se simtă luat în serios. Se poate salva ca PDF. Textul spune „cerere de programare”, nu „programare confirmată”, pentru că o confirmați voi.
**Format A4, ca un PDF:** pe laptop și desktop foaia are mereu proporția A4 (640 × 905) și se micșorează întreagă cât să încapă pe ecran, cu butoanele dedesubt. Antetul, titlul, totalul și semnătura stau pe loc; doar lista de detalii se derulează în interiorul foii (cu „Derulează pentru toate detaliile” când e mai lungă). Detaliile scurte stau câte două pe rând, iar pozele trimise apar ca miniaturi. Pe telefon scrisoarea se derulează normal, iar butoanele rămân fixate jos. La „Salvează PDF” se tipărește tot conținutul, fără derulare.

### 6.11 Footer
Servicii, zone, contact, program (luni-sâmbătă, 9:00-19:00), **datele legale ale firmei** (ETALON SECURITY SRL, sediu, Reg. Com., CUI, EUID), pictograma oficială ANPC SAL, linkuri spre Termeni și Confidențialitate și nota despre mărcile Fortador / Lamborghini Caloreclima.

---

## 7. Mișcare

| Unde | Ce face | De ce |
|---|---|---|
| Toată pagina | Elementele apar ușor de jos când intră în ecran | Ghidează privirea, fără să încetinească |
| Prima secțiune | Abur portocaliu-alb care se ridică în spate; logo-ul plutește și se înclină după mouse | Spune „abur” din prima secundă |
| Slider înainte / după | Bara se mișcă singură o dată | Arată că se poate trage |
| Tehnologie | 4 pași care avansează singuri, abur care „curăță” poza | Explică metoda, nu decorează |
| Prețuri | Cifrele curg spre noua valoare | Confirmă că s-a schimbat ceva |
| Configurator | Zonele se aprind în portocaliu | Arată ce include pachetul |
| Scrisoare | Intră ca o foaie, ștampila „Trimisă” se aplică | Momentul de final, recompensă |

**Reguli:**
- Animăm doar poziție și transparență (fluid pe orice telefon).
- Nimic nu fixează ecranul la derulare și nimic nu „ascultă” derularea la fiecare pixel.
- Abur și animațiile se opresc când nu sunt pe ecran.
- Cine are „reducere mișcare” activată în telefon vede totul static, cu rezultatul final.

---

## 8. Texte

- **Limba:** română, la persoana a doua („Venim la tine”, „Alege mașina”), caldă dar directă.
- **Fraze scurte.** Titluri de maxim 8-10 cuvinte, descrieri de maxim ~25 de cuvinte.
- **Fără cratimă lungă (—)** în texte; folosim punct, virgulă sau două fraze.
- **Fără cuvinte goale** („revoluționar”, „de neegalat”, „experiență unică”) și fără superlative nedovedite.
- **Fără cifre inventate:** nu există „98% clienți mulțumiți” sau „500+ mașini”. Contorul de mașini apare doar când îl completați cu cifra reală.
- **Fără citate inventate:** pentru Andy avem doar faptul că vă recomandă; restul e marcat „de completat”.
- **Prețuri exacte** și explicate („Încadrarea o faci tu. Dacă din poze apreciem altfel, îți scriem înainte să venim.”).
- Textele de completat de voi apar *cu italic* pe site, ca să fie ușor de găsit.

---

## 9. Prețuri: cum au fost gândite

- **Interior** (preț pentru mașină mică): Întreținere 300, Standard 450, Intensiv 650 lei. Mașina medie +80 lei, mare +150 lei.
- **Motor:** 200 lei fix, orice mașină.
- **Complet:** Interior + Motor cu **15% reducere**, rotunjit în jos la 5 lei (clientul primește mereu cel puțin 15%).
- **Extra-uri:** 20 lei fiecare, doar la pachetele cu interior. La **Intensiv** sunt incluse ozonizarea, părul de animale și scaunul de copil.
- **Deplasare:** inclusă în București; în afara orașului, stabilită împreună.

**De ce așa:** clientul își alege singur nivelul (se simte implicat), iar voi corectați din poze, înainte de deplasare, pe WhatsApp sau email. Nu pierde nimeni timp și nu există „surpriză” la fața locului. Prețurile se schimbă dintr-un singur loc (`PRICING` în `tools/build.py`) și se actualizează automat pe toate paginile, în configurator și în scrisoare.

---

## 10. Accesibilitate

- Contrast de citire bun pe toate textele și butoanele (inclusiv textul închis pe portocaliu).
- Totul se poate folosi și din tastatură, cu contur portocaliu vizibil pe elementul selectat.
- Butoane de minim 44 px pe telefon.
- Etichete reale pe toate câmpurile, texte alternative pe poze, roluri corecte pentru selectoare și slider.
- Respectăm setarea „reducere mișcare” din telefon.

---

## 11. Viteză

- Fonturi și iconițe pe site, fără servere externe (singurul extern rămas: pozele demo Unsplash, temporare).
- Logo mic în WebP, poze încărcate doar când ajungi la ele, la jumătate de rezoluție pe telefon.
- Fără biblioteci mari de animație: tot e scris simplu, în CSS și puțin JavaScript.

---

## 12. Încredere și corectitudine

- **Andy Popescu:** doar recomandarea confirmată de voi; nicio poză cu el de pe internet (drepturi de imagine), niciun citat inventat.
- **„Powered by Lamborghini”:** păstrat, cu nota din footer că Lamborghini Caloreclima e marcă Ferroli și nu aveți legătură cu Automobili Lamborghini. Motivul: Fortador folosește un arzător Lamborghini (de centrale termice), nu e legat de constructorul auto.
- **Date legale** complete în footer (Legea 365/2002), pictograma ANPC SAL, Termeni și Confidențialitate (de verificat de un jurist).
- **Pozele demo** sunt marcate ca demo; lucrările din portofoliu sunt marcate ca exemple până le înlocuiți.

---

## 13. Unde se schimbă lucrurile

| Ce vrei să schimbi | Unde |
|---|---|
| Prețuri, niveluri, extra-uri, reducere | `tools/build.py` → `PRICING`, `TIERS` |
| Date firmă, email | `tools/build.py` → `LEGAL` |
| Program de lucru | `tools/build.py` → `PROGRAM` |
| Telefon, WhatsApp | `site/config.js` |
| Meniu, footer (pe toate paginile) | `tools/build.py` → `header()`, `footer_block()` |
| Echipa, lucrări, articole, zone, abonamente | `tools/build.py` → listele de conținut |
| Conținutul paginii principale | `site/index.html` (zonele marcate `HEAD`, `HEADER`, `FOOTER`, `TIERS`, `PRICETABLE` se generează automat) |
| Culori, spații, colțuri | `site/styles.css` → variabilele din `:root` |
| Iconițe noi | `tools/icons/` (SVG din Phosphor) |
| Poze | `site/assets/img/` (nume în `POZE-NECESARE.md`) |

După orice modificare în `tools/build.py`:

```bash
python3 tools/build.py
```

Publicare pe linkul de test (https://etaprocleaning.vercel.app):

```bash
bash tools/deploy.sh
```

---

## 14. Istoricul deciziilor (pe scurt)

1. Prima versiune: temă închisă, accent portocaliu din logo, fonturi Outfit + Geist, pachete cu „de la”.
2. Spațiere mai aerisită în prima secțiune; bază de ~230 de mașini cu încadrare automată; poze în formular.
3. Detailing mobil și București puse în prim-plan; slider înainte / după; Andy Popescu; extra-uri, firme, vouchere, pagini SEO pe servicii.
4. Configuratorul cu silueta mașinii, Lucrarea lunii, garanția, „Sună-mă înapoi”.
5. Secțiunea care fixa ecranul la derulare a fost **scoasă** (bloca scroll-ul) și înlocuită cu pași care avansează singuri.
6. Reparată pagina care ieșea din ecran pe lățime; adăugat meniul ☰ pe telefon.
7. Optimizare pentru telefon: carusel de pachete, bară fixă jos, pagină cu ~25% mai scurtă.
8. Pagini noi: Despre, Portofoliu, Blog, ETA Care, Zone; apoi Tehnologie, Firme, Termeni, Confidențialitate și date legale.
9. Fonturi și iconițe găzduite local, logo optimizat, scrisoare de confirmare cu număr de referință.
10. Prețuri exacte pe 3 niveluri (fără „de la”), Complet cu 15% reducere.
11. Pagina principală simplificată de la 15 la 8 secțiuni.
12. Butoane „Fă poze” / „Din galerie”, formular care încape pe un ecran de laptop, extra-uri de 20 lei cu pachet inclus la Intensiv, program și metode de plată.
