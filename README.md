# ETA PRO CLEANING

Site pentru ETA PRO CLEANING, detailing auto mobil cu abur în București. Venim noi la client, cu duba echipată Fortador.

Test: https://etaprocleaning.vercel.app

## Cum e făcut

Site static (HTML, CSS, JavaScript simplu), fără framework. Paginile secundare, prețurile, meniul și footerul se generează dintr-un singur script.

```
site/    site-ul gata de publicat
tools/   generatorul de pagini (build.py), publicarea (deploy.sh), iconițe
DESIGN.md  ideea de design și regulile
TODO.md    ce mai e de făcut
```

## Comenzi

Regenerează paginile (prețuri, meniu, footer, pagini secundare):

```bash
python3 tools/build.py
```

Publică pe Vercel (necesită Vercel CLI autentificat):

```bash
bash tools/deploy.sh
```

## Unde se schimbă lucrurile

- Prețuri, program, date firmă, texte legale: `tools/build.py`
- Telefon, WhatsApp: `site/config.js`
- Pagina principală: `site/index.html`
- Stiluri: `site/styles.css`

Detalii în `DESIGN.md`.
