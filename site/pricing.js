/* GENERAT de tools/build.py din PRICING. Nu edita aici: schimbă prețurile în build.py. */
window.ETA_PRICING = {
 "table": {
  "interior": {
   "s": {
    "intretinere": 300,
    "standard": 450,
    "intensiv": 650
   },
   "m": {
    "intretinere": 380,
    "standard": 530,
    "intensiv": 730
   },
   "l": {
    "intretinere": 450,
    "standard": 600,
    "intensiv": 800
   }
  },
  "motor": {
   "s": {
    "intretinere": 200,
    "standard": 200,
    "intensiv": 200
   },
   "m": {
    "intretinere": 200,
    "standard": 200,
    "intensiv": 200
   },
   "l": {
    "intretinere": 200,
    "standard": 200,
    "intensiv": 200
   }
  },
  "complet": {
   "s": {
    "intretinere": 425,
    "standard": 550,
    "intensiv": 720
   },
   "m": {
    "intretinere": 490,
    "standard": 620,
    "intensiv": 790
   },
   "l": {
    "intretinere": 550,
    "standard": 680,
    "intensiv": 850
   }
  }
 },
 "motor": 200,
 "discount": 0.15,
 "tiers": [
  {
   "key": "intretinere",
   "name": "Întreținere",
   "desc": "Praf, urme ușoare, fără pete vizibile."
  },
  {
   "key": "standard",
   "name": "Standard",
   "desc": "Pete pe scaune sau mochetă, firimituri, mizerie adusă iarna."
  },
  {
   "key": "intensiv",
   "name": "Intensiv",
   "desc": "Pete vechi, păr de animale, mirosuri, noroi. Include ozonizare, păr de animale și scaun de copil."
  }
 ],
 "extras": {
  "ozon": {
   "name": "Ozonizare",
   "price": 20
  },
  "par": {
   "name": "Păr de animale",
   "price": 20
  },
  "copil": {
   "name": "Scaun de copil",
   "price": 20
  },
  "piele": {
   "name": "Tratament piele",
   "price": 20
  },
  "miros": {
   "name": "Mirosuri persistente",
   "price": 20
  }
 },
 "includedIntensiv": [
  "ozon",
  "par",
  "copil"
 ]
};
