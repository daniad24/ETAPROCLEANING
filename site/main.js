/* ETA PRO CLEANING interactions. No scroll listeners: IntersectionObserver + rAF only. */
(() => {
  const CONTACT = window.ETA_CONFIG; // vezi config.js


  // Perechi înainte / după. Pune pozele în assets/img/ cu aceste nume.
  const BA_PAIRS = [
    { t: "Scaune textile", b: "assets/img/ba-scaune-inainte.jpg", a: "assets/img/ba-scaune-dupa.jpg" },
    { t: "Mochetă", b: "assets/img/ba-mocheta-inainte.jpg", a: "assets/img/ba-mocheta-dupa.jpg" },
    { t: "Motor", b: "assets/img/ba-motor-inainte.jpg", a: "assets/img/ba-motor-dupa.jpg" },
    { t: "Plafon", b: "assets/img/ba-plafon-inainte.jpg", a: "assets/img/ba-plafon-dupa.jpg" },
    { t: "Piele", b: "assets/img/ba-piele-inainte.jpg", a: "assets/img/ba-piele-dupa.jpg" },
  ];
  // Cifre reale pentru contor. Lasă null ca să rămână ascuns.
  const STATS = { masini: null, label: "mașini curățate în 2026" };
  // Extra prices and the ones bundled with the Intensiv tier come from pricing.js.
  const EXTRA_PRICES = Object.fromEntries(Object.entries(window.ETA_PRICING.extras).map(([k, v]) => [k, v.price]));
  const INCLUDED_INTENSIV = window.ETA_PRICING.includedIntensiv;
  const EXTRA_NAME = { ozon: "Ozonizare", par: "Păr de animale", piele: "Tratament piele", miros: "Mirosuri persistente", copil: "Scaun de copil" };
  const waLink = (text) => `https://wa.me/${CONTACT.whatsapp}?text=${encodeURIComponent(text)}`;

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Prices come from pricing.js, generated from PRICING in tools/build.py (single source).
  // PRICES[plan][size][tier] -> lei
  const PR = window.ETA_PRICING;
  const PRICES = PR.table;
  const TIER_NAME = Object.fromEntries(PR.tiers.map((t) => [t.key, t.name]));
  const DISC = Math.round(PR.discount * 100);
  const SIZE_NAME = { s: "Mică", m: "Medie", l: "Mare" };
  const PLAN_NAME = { interior: "Interior", motor: "Motor", complet: "Complet" };

  /* nav state via sentinel observer */
  const nav = $("#nav");
  const sentinel = document.createElement("div");
  sentinel.style.cssText = "position:absolute;top:0;height:24px;width:1px;pointer-events:none";
  document.body.prepend(sentinel);
  new IntersectionObserver(([e]) => nav.classList.toggle("is-stuck", !e.isIntersecting)).observe(sentinel);

  /* mobile menu */
  const burger = $("#burger"), mnav = $("#mnav");
  const setMenu = (open) => {
    mnav.hidden = !open;
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Închide meniul" : "Deschide meniul");
    $("i", burger).className = open ? "ph ph-x" : "ph ph-list";
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
  };
  burger.addEventListener("click", () => setMenu(mnav.hidden));
  mnav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
  addEventListener("keydown", (e) => { if (e.key === "Escape" && !mnav.hidden) setMenu(false); });

  /* reveal on enter */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  $$(".reveal").forEach((el) => io.observe(el));

  /* spotlight: write CSS vars directly, no React-style state */
  $$(".spot").forEach((el) => {
    el.addEventListener("pointermove", (ev) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty("--mx", ev.clientX - r.left + "px");
      el.style.setProperty("--my", ev.clientY - r.top + "px");
    });
  });

  /* badge tilt follows the pointer (hero only) */
  const badge = $("[data-tilt]");
  if (badge && !reduce && matchMedia("(pointer:fine)").matches) {
    const hero = $(".hero");
    hero.addEventListener("pointermove", (ev) => {
      const r = hero.getBoundingClientRect();
      const x = (ev.clientX - r.left) / r.width - 0.5;
      const y = (ev.clientY - r.top) / r.height - 0.5;
      badge.style.transform = `perspective(900px) rotateY(${x * 10}deg) rotateX(${-y * 8}deg)`;
    });
    hero.addEventListener("pointerleave", () => (badge.style.transform = ""));
  }

  /* steam particles (canvas). Soft orange-white puffs rising from the bottom. */
  const cv = $("#steam");
  if (cv && !reduce) {
    const ctx = cv.getContext("2d");
    let w, h, dpr, puffs = [], raf, running = true;
    const resize = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = w * dpr; cv.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    const spawn = (initial) => {
      const side = Math.random();
      return {
        x: w * (0.45 + side * 0.55) + (Math.random() - 0.5) * 120,
        y: initial ? Math.random() * h : h + 80,
        r: 70 + Math.random() * 130,
        vy: 0.25 + Math.random() * 0.5,
        vx: (Math.random() - 0.5) * 0.25,
        a: 0, max: 0.05 + Math.random() * 0.07,
        hue: Math.random() < 0.55 ? "255,184,90" : "255,255,255",
        life: 0, span: 500 + Math.random() * 500,
      };
    };
    const init = () => { resize(); puffs = Array.from({ length: Math.round(Math.min(26, w / 55)) }, () => spawn(true)); };
    const tick = () => {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < puffs.length; i++) {
        const p = puffs[i];
        p.life++; p.y -= p.vy; p.x += p.vx + Math.sin(p.life / 90 + i) * 0.15; p.r += 0.1;
        const t = p.life / p.span;
        p.a = Math.sin(Math.min(t, 1) * Math.PI) * p.max;
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
        g.addColorStop(0, `rgba(${p.hue},${p.a})`);
        g.addColorStop(1, `rgba(${p.hue},0)`);
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fill();
        if (t >= 1 || p.y < -p.r) puffs[i] = spawn(false);
      }
      raf = requestAnimationFrame(tick);
    };
    init(); tick();
    addEventListener("resize", init);
    // pause when hero is off-screen
    new IntersectionObserver(([e]) => {
      running = e.isIntersecting;
      if (running) { cancelAnimationFrame(raf); tick(); }
    }).observe($(".hero"));
  }

  /* ---------- state ---------- */
  const state = { size: "s", car: null, plan: "interior", tier: "standard", files: [], extras: [], zona: "buc" };
  const MAX_PHOTOS = 6;

  const sizeBtns = $$(".size");
  const clsSel = $("#clasa"), nivelSel = $("#nivel");
  const sum = $("#sum"), sumCar = $("#sum-car"), sumTip = $("#sum-tip");
  const carRes = $("#car-res"), carHint = $("#masina-hint");
  const HINT_DEFAULT = carHint.textContent;
  const RES_DEFAULT = carRes.textContent;

  const tween = (el, to) => {
    const from = parseInt(el.textContent, 10) || 0;
    if (reduce || from === to) { el.textContent = to; return; }
    const t0 = performance.now(), dur = 520;
    const step = (t) => {
      const k = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - k, 4);
      el.textContent = Math.round(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const priceOf = (plan, s = state) => PRICES[plan][s.size][s.tier];
  const hasInterior = (s = state) => s.plan !== "motor";
  const isIncluded = (k, s = state) => s.tier === "intensiv" && INCLUDED_INTENSIV.includes(k);
  // extras that are actually charged (interior plans only; bundled ones are free on Intensiv)
  const extrasCost = (s = state) => hasInterior(s) ? s.extras.filter((k) => !isIncluded(k, s)).reduce((t, k) => t + EXTRA_PRICES[k], 0) : 0;
  const totalOf = (s = state) => priceOf(s.plan, s) + extrasCost(s);

  const render = () => {
    const { size, plan, car, tier } = state;
    $$(".plan").forEach((p) => tween($("[data-price]", p), priceOf(p.dataset.plan)));
    // Complet: show the separate total crossed out and the saving
    const full = priceOf("interior") + priceOf("motor");
    const old = $("[data-old]"), save = $("[data-save]");
    if (old) old.textContent = full;
    if (save) save.textContent = `Economisești ${full - priceOf("complet")} lei`;
    $$("[data-tier-label]").forEach((el) => (el.textContent = `Nivel ${TIER_NAME[tier]}`));
    const td = $("#tier-desc");
    if (td) td.textContent = PR.tiers.find((t) => t.key === tier).desc;
    $$(".tier").forEach((b) => {
      const on = b.dataset.tier === tier;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-checked", on);
    });
    sizeBtns.forEach((b) => {
      const on = b.dataset.size === size;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-checked", on);
    });
    clsSel.value = size;
    nivelSel.value = tier;
    const pr = $(`input[name=pachet][value=${plan}]`);
    if (pr) pr.checked = true;

    const extraPlus = state.zona === "afara" ? " +" : "";
    if (sum) sum.textContent = `${totalOf()} lei${extraPlus}`;
    if (sumCar) {
      const what = plan === "motor" ? "pachet Motor" : `pachet ${PLAN_NAME[plan]}, nivel ${TIER_NAME[tier]}`;
      sumCar.textContent = `${car ? car.label + ", clasa " : "Mașină "}${SIZE_NAME[size].toLowerCase()}, ${what}`;
    }

    renderCfg();

    // extras + travel
    const sx = $("#sum-extra");
    const parts = [];
    // extras UI: bundled ones are ticked and locked on Intensiv; hidden entirely for Motor
    const xf = $("#extras-field");
    if (xf) xf.hidden = !hasInterior();
    $$("#extras-row label").forEach((lab) => {
      const inp = $("input", lab), inc = isIncluded(inp.value);
      inp.disabled = inc;
      lab.classList.toggle("is-included", inc);
      lab.title = inc ? "Inclus în nivelul Intensiv" : `${EXTRA_PRICES[inp.value]} lei`;
    });
    if (state.zona === "afara") parts.push("Deplasare în afara Bucureștiului: cost stabilit împreună");
    sx.hidden = !parts.length;
    sx.textContent = parts.join(". ") + (parts.length ? "." : "");
    $$("#extras-row input").forEach((c) => (c.checked = isIncluded(c.value) || state.extras.includes(c.value)));
    $("#zona-note").hidden = state.zona !== "afara";
    $$("[data-needs-motor]").forEach((li) => (li.hidden = plan === "interior"));

    sumTip.hidden = plan === "motor";
    sumTip.textContent = "Nivelul îl alegi tu. Dacă din poze apreciem altfel, îți scriem înainte să venim.";
  };

  /* ---------- visual configurator ---------- */
  // Side-profile silhouettes generated from a few proportions per class.
  const SHAPES = {
    s: { x0: 78, x1: 560, hood: 205, rA: 285, rB: 455, rY: 66, rear: 548, belt: 132, trunk: null, w: [170, 468], r: 36 },
    m: { x0: 40, x1: 600, hood: 215, rA: 300, rB: 440, rY: 72, rear: null, belt: 134, trunk: 512, w: [160, 500], r: 36 },
    l: { x0: 40, x1: 600, hood: 190, rA: 258, rB: 560, rY: 50, rear: 588, belt: 126, trunk: null, w: [158, 500], r: 42 },
  };
  const ZONES_BY_PLAN = { interior: ["plafon", "bord", "scaune", "mocheta"], motor: ["motor"], complet: ["plafon", "bord", "scaune", "mocheta", "motor"] };
  const carSVG = (k) => {
    const p = SHAPES[k], G = 214, B = 196;
    const tail = p.trunk
      ? `L${p.rB},${p.rY + 8} L${p.trunk},${p.belt - 6} L${p.x1 - 8},${p.belt} Q${p.x1},${p.belt + 2} ${p.x1},${p.belt + 16}`
      : `L${p.rB},${p.rY + 4} Q${p.rear},${p.rY + 10} ${p.rear},${p.belt - 6} L${p.x1},${p.belt + 16}`;
    const body = `M${p.x0},${B} L${p.x0},${p.belt + 30} Q${p.x0},${p.belt + 14} ${p.x0 + 24},${p.belt + 12} L${p.hood},${p.belt} L${p.rA},${p.rY + 6} Q${p.rA + 8},${p.rY} ${p.rA + 26},${p.rY} L${p.rB - 26},${p.rY} Q${p.rB - 8},${p.rY} ${p.rB},${p.rY + 4} ${tail} L${p.x1},${B} Z`;
    const gEnd = p.trunk ? p.trunk - 8 : p.rear - 14;
    const glass = `M${p.hood + 22},${p.belt - 3} L${p.rA + 10},${p.rY + 12} L${p.rB - 8},${p.rY + 12} L${gEnd},${p.belt - 3} Z`;
    const pillar = (p.rA + p.rB) / 2 + 10;
    const cab0 = p.hood + 30, cab1 = gEnd - 10, cw = cab1 - cab0;
    const seat = (x) => `M${x},${p.belt + 36} L${x + 6},${p.rY + 34} Q${x + 8},${p.rY + 26} ${x + 18},${p.rY + 28} L${x + 22},${p.belt + 22} L${x + 52},${p.belt + 24} Q${x + 58},${p.belt + 26} ${x + 56},${p.belt + 36} Z`;
    const wheel = (cx) => `<circle class="car-wheel" cx="${cx}" cy="${G - p.r + 6}" r="${p.r}"/><circle class="car-rim" cx="${cx}" cy="${G - p.r + 6}" r="${p.r * .55}"/>`;
    return `<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs><clipPath id="clip-body"><path d="${body}"/></clipPath></defs>
      <line class="car-ground" x1="10" y1="${G + 6}" x2="630" y2="${G + 6}"/>
      <path class="car-body" d="${body}"/>
      <g clip-path="url(#clip-body)">
        <rect class="zone" data-z="motor" x="${p.x0 + 8}" y="${p.belt + 10}" width="${p.hood - p.x0 - 14}" height="${B - p.belt - 22}" rx="10"/>
        <rect class="zone" data-z="mocheta" x="${cab0}" y="${p.belt + 42}" width="${cw}" height="16" rx="6"/>
      </g>
      <path class="car-glass" d="${glass}"/>
      <rect class="zone" data-z="plafon" x="${p.rA + 14}" y="${p.rY + 4}" width="${p.rB - p.rA - 28}" height="9" rx="4"/>
      <rect class="zone" data-z="bord" x="${p.hood + 26}" y="${p.belt - 2}" width="58" height="18" rx="6"/>
      <path class="zone" data-z="scaune" d="${seat(cab0 + cw * .3)}"/>
      <path class="zone" data-z="scaune" d="${seat(cab0 + cw * .66)}"/>
      <line class="car-line" x1="${pillar}" y1="${p.rY + 12}" x2="${pillar + 4}" y2="${B - 14}"/>
      <line class="car-line" x1="${p.x0 + 20}" y1="${p.belt + 26}" x2="${p.x1 - 12}" y2="${p.belt + 26}"/>
      ${wheel(p.w[0])}${wheel(p.w[1])}
    </svg>`;
  };
  let drawnSize = null;
  const renderCfg = () => {
    const { size, plan, extras, zona, car } = state;
    const host = $("#cfg-car");
    if (drawnSize !== size) { host.innerHTML = carSVG(size); drawnSize = size; }
    const on = ZONES_BY_PLAN[plan];
    // re-trigger the fill animation on change
    $$(".zone", host).forEach((z) => { z.classList.remove("is-on"); if (on.includes(z.dataset.z)) { void z.getBBox(); z.classList.add("is-on"); } });
    $$("#cfg-zones li").forEach((li) => li.classList.toggle("is-on", on.includes(li.dataset.zone)));
    $$("[data-cfg-plan]").forEach((b) => b.setAttribute("aria-checked", b.dataset.cfgPlan === plan));

    const tier = state.tier;
    const lines = [["Mașina", car ? `${car.label}, clasa ${SIZE_NAME[size].toLowerCase()}` : `Clasa ${SIZE_NAME[size].toLowerCase()}`]];
    if (plan !== "motor") lines.push(["Nivel de curățare", TIER_NAME[tier]]);
    if (plan === "interior") lines.push(["Interior", `${priceOf("interior")} lei`]);
    if (plan === "motor") lines.push(["Motor", `${priceOf("motor")} lei`]);
    if (plan === "complet") {
      const i = priceOf("interior"), m = priceOf("motor"), c = priceOf("complet");
      lines.push(["Interior", `${i} lei`], ["Motor", `${m} lei`], [`Reducere Complet ${DISC}%`, `-${i + m - c} lei`]);
    }
    if (hasInterior()) {
      if (tier === "intensiv") lines.push(["Incluse", INCLUDED_INTENSIV.map((k) => EXTRA_NAME[k].toLowerCase()).join(", ")]);
      extras.filter((k) => !isIncluded(k)).forEach((k) => lines.push([EXTRA_NAME[k], `${EXTRA_PRICES[k]} lei`]));
    }
    lines.push(["Deplasare", zona === "afara" ? "stabilim împreună" : "inclusă în București"]);
    $("#cfg-lines").innerHTML = lines.map(([a, b]) => `<div><dt>${a}</dt><dd>${b}</dd></div>`).join("");
    $("#cfg-total").textContent = `${totalOf()} lei${zona === "afara" ? " +" : ""}`;
  };

  const setCar = (c) => {
    state.car = c;
    if (c) {
      state.size = c.cls;
      $("#car-q").value = c.label;
      $("#masina").value = c.label;
      const nm = SIZE_NAME[c.cls];
      carRes.innerHTML = `<b>${c.label}</b> intră la clasa <b>${nm.toLowerCase()}</b>.<span class="tag">${nm}</span>`;
      carHint.textContent = `Încadrată automat: clasa ${nm.toLowerCase()}.`;
    } else {
      carRes.textContent = RES_DEFAULT;
      carHint.textContent = HINT_DEFAULT;
    }
    render();
  };

  /* ---------- car database + combobox ---------- */
  let CARS = [];
  const norm = (t) => t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[-_.]/g, " ").replace(/\bserie\b/g, "seria").replace(/\bclasa\b/g, "class")
    .replace(/\s+/g, " ").trim();
  const search = (q) => {
    const toks = norm(q).split(" ").filter(Boolean);
    if (!toks.length) return [];
    return CARS.filter((c) => toks.every((t) => c.hay.includes(t)))
      .sort((a, b) => (b.hay.startsWith(toks[0]) - a.hay.startsWith(toks[0])) || a.label.localeCompare(b.label))
      .slice(0, 8);
  };

  const initCombo = (input, list) => {
    let items = [], idx = -1;
    const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); idx = -1; };
    const paint = () => {
      list.innerHTML = "";
      if (!items.length) {
        const q = input.value.trim();
        if (q.length >= 3) {
          const li = document.createElement("li");
          li.className = "is-empty";
          li.textContent = "Nu o avem în listă. Alege dimensiunea mai jos.";
          list.append(li);
          list.hidden = false;
        } else close();
        return;
      }
      items.forEach((c, i) => {
        const li = document.createElement("li");
        li.setAttribute("role", "option");
        li.setAttribute("aria-selected", i === idx);
        li.innerHTML = `<span>${c.label}</span><small>${SIZE_NAME[c.cls]}</small>`;
        li.addEventListener("mousedown", (e) => { e.preventDefault(); choose(c); });
        list.append(li);
      });
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
    };
    const choose = (c) => { setCar(c); close(); };
    input.addEventListener("input", () => {
      items = search(input.value); idx = -1;
      if (state.car && input.value !== state.car.label) { state.car = null; carRes.textContent = RES_DEFAULT; carHint.textContent = HINT_DEFAULT; render(); }
      // keep the two inputs in sync while typing
      const other = input.id === "car-q" ? $("#masina") : $("#car-q");
      other.value = input.value;
      paint();
    });
    input.addEventListener("keydown", (e) => {
      if (list.hidden) return;
      if (e.key === "ArrowDown") { e.preventDefault(); idx = Math.min(idx + 1, items.length - 1); paint(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); idx = Math.max(idx - 1, 0); paint(); }
      else if (e.key === "Enter" && items.length) { e.preventDefault(); choose(items[idx >= 0 ? idx : 0]); }
      else if (e.key === "Escape") close();
    });
    input.addEventListener("blur", () => setTimeout(close, 120));
    input.addEventListener("focus", () => { if (input.value) { items = search(input.value); paint(); } });
  };

  fetch("cars.json")
    .then((r) => r.json())
    .then((rows) => {
      CARS = rows.map(([b, m, cls]) => ({ label: `${b} ${m}`, cls, hay: norm(`${b} ${m}`) }));
    })
    .catch(() => { /* list unavailable: user picks the size manually */ });
  initCombo($("#car-q"), $("#car-list"));
  initCombo($("#masina"), $("#masina-list"));

  /* ---------- controls ---------- */
  sizeBtns.forEach((b) => b.addEventListener("click", () => { state.size = b.dataset.size; state.car = null; carRes.textContent = RES_DEFAULT; render(); }));
  clsSel.addEventListener("change", () => { state.size = clsSel.value; render(); });
  nivelSel.addEventListener("change", () => { state.tier = nivelSel.value; render(); });
  $$(".tier").forEach((b) => b.addEventListener("click", () => { state.tier = b.dataset.tier; render(); }));
  $$("input[name=pachet]").forEach((r) => r.addEventListener("change", () => { state.plan = r.value; render(); }));
  $$("[data-pick]").forEach((a) => a.addEventListener("click", () => { state.plan = a.dataset.pick; render(); }));
  $$("[data-cfg-plan]").forEach((b) => b.addEventListener("click", () => { state.plan = b.dataset.cfgPlan; render(); }));
  $$("#extras-row input").forEach((c) => c.addEventListener("change", () => {
    state.extras = $$("#extras-row input:checked:not(:disabled)").map((x) => x.value);
    render();
  }));
  $("#zona").addEventListener("change", (e) => { state.zona = e.target.value; render(); });
  $$("[data-msg]").forEach((a) => a.addEventListener("click", () => {
    const m = $("#mesaj");
    if (!m.value.trim()) m.value = a.dataset.msg;
  }));
  render();

  /* ---------- before / after sliders ---------- */
  const loadImg = (fig, src) => {
    const img = $("img", fig);
    fig.classList.remove("is-empty");
    img.onerror = () => { if (window.__img && window.__img(img)) return; fig.classList.add("is-empty"); };
    delete img.dataset.demoTried;
    fig.classList.remove("is-demo");
    img.src = src;
  };
  const initBA = (el) => {
    const range = $(".ba__range", el);
    const set = (v) => el.style.setProperty("--p", v + "%");
    range.addEventListener("input", () => set(range.value));
    set(range.value);
    // one-time nudge so visitors understand they can drag
    if (!reduce) {
      new IntersectionObserver(([e], o) => {
        if (!e.isIntersecting) return;
        o.disconnect();
        el.classList.add("is-hint");
        setTimeout(() => set(32), 250);
        setTimeout(() => set(64), 1150);
        setTimeout(() => { set(50); range.value = 50; }, 2050);
        setTimeout(() => el.classList.remove("is-hint"), 3000);
      }, { threshold: 0.6 }).observe(el);
    }
    if (el.dataset.before) {
      loadImg($(".ba__img--before", el), el.dataset.before);
      loadImg($(".ba__img--after", el), el.dataset.after);
    }
  };
  $$("[data-ba]").forEach(initBA);

  const baMain = $("#ba-main"), baTabs = $("#ba-tabs"), baCap = $("#ba-cap");
  const showPair = (i) => {
    const p = BA_PAIRS[i];
    loadImg($(".ba__img--before", baMain), p.b);
    loadImg($(".ba__img--after", baMain), p.a);
    $(".ba__img--before img", baMain).alt = `${p.t}, înainte de detailing`;
    $(".ba__img--after img", baMain).alt = `${p.t}, după detailing`;
    $$(".ba-tab", baTabs).forEach((t, j) => t.setAttribute("aria-selected", i === j));
    baCap.textContent = `${p.t}. Trage bara sau folosește săgețile de pe tastatură.`;
  };
  BA_PAIRS.forEach((p, i) => {
    const b = document.createElement("button");
    b.className = "ba-tab"; b.type = "button"; b.setAttribute("role", "tab");
    b.textContent = p.t;
    b.addEventListener("click", () => showPair(i));
    baTabs.append(b);
  });
  showPair(0);

  /* ---------- mobile: action bar + plan carousel ---------- */
  const mq = matchMedia("(max-width: 767px)");
  const mbarWa = $("#mbar-wa");
  mbarWa.href = waLink("Bună, aș vrea mai multe detalii despre detailing.");
  mbarWa.target = "_blank"; mbarWa.rel = "noopener";
  const plansEl = $(".plans"), dots = $$("#plan-dots span");
  const cards = $$(".plan", plansEl);
  // dots follow the card that is mostly in view (observer on the scroller, no scroll listener)
  const dio = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { const i = cards.indexOf(e.target); dots.forEach((d, j) => d.classList.toggle("is-on", i === j)); } });
  }, { root: plansEl, threshold: 0.6 });
  cards.forEach((c) => dio.observe(c));
  // open the carousel on the featured "Complet" card
  const centerFeatured = () => { if (mq.matches) { const f = $(".plan--top", plansEl); plansEl.scrollLeft = f.offsetLeft - (plansEl.clientWidth - f.clientWidth) / 2; } };
  centerFeatured();
  // hide the bar while the booking form is on screen (it already has its own button)
  new IntersectionObserver(([e]) => {
    $("#mbar").classList.toggle("is-hidden", e.isIntersecting);
    $("#floaters").classList.toggle("is-away", e.isIntersecting);
  }, { threshold: 0.15 }).observe($("#form"));
  mq.addEventListener("change", centerFeatured);

  /* ---------- contact wiring ---------- */
  const waFloat = $("#wa-float");
  waFloat.href = waLink("Bună, aș vrea mai multe detalii despre detailing.");
  waFloat.target = "_blank"; waFloat.rel = "noopener";
  new IntersectionObserver(([e]) => $("#floaters").classList.toggle("is-on", !e.isIntersecting)).observe($(".hero"));

  /* ---------- gallery + lightbox ---------- */
  const lb = $("#lightbox"), lbImg = $("#lightbox-img");
  $$(".gal__item").forEach((btn) => {
    const im = $("img", btn);
    im.addEventListener("error", () => {
      if (window.__img && window.__img(im)) { btn.dataset.src = im.src; return; }
      btn.classList.add("is-empty"); btn.disabled = true; im.remove();
    });
    btn.addEventListener("click", () => {
      if (btn.classList.contains("is-empty")) return;
      lbImg.src = btn.dataset.src; lbImg.alt = im.alt;
      lb.showModal();
    });
  });
  lb.addEventListener("click", (e) => { if (e.target === lb || e.target.closest("[data-close]")) lb.close(); });

  /* ---------- call me back ---------- */
  const cb = $("#callback"), cbForm = $("#cb-form"), cbOk = $("#cb-ok");
  $$("[data-callback]").forEach((b) => b.addEventListener("click", () => { cbOk.hidden = true; cb.showModal(); $("#cb-nume").focus(); }));
  cb.addEventListener("click", (e) => { if (e.target === cb || e.target.closest("[data-close]")) cb.close(); });
  cbForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const n = $("#cb-nume").value.trim(), t = $("#cb-tel").value.trim();
    const badN = n.length < 2, badT = t.replace(/\D/g, "").length < 9;
    [["#cb-nume", badN], ["#cb-tel", badT]].forEach(([id, b]) => {
      const f = $(id).closest(".field"); f.classList.toggle("is-bad", b); $(".err", f).hidden = !b;
    });
    if (badN || badT) return;
    const msg = `Bună, sunt ${n}. Vă rog să mă sunați înapoi la ${t}.` + (state.car ? ` Mașina: ${state.car.label}.` : "");
    open(waLink(msg), "_blank", "noopener");
    cbOk.hidden = false;
    cbOk.textContent = "Mulțumim! Trimite mesajul din WhatsApp și te sunăm în cel mult 15 minute.";
  });

  /* ---------- real counter (hidden until STATS.masini is set) ---------- */
  if (typeof STATS.masini === "number") {
    const box = $("#count"), num = $("[data-count]", box);
    box.hidden = false; $("#count-label").textContent = STATS.label;
    new IntersectionObserver(([e], o) => {
      if (!e.isIntersecting) return; o.disconnect();
      if (reduce) { num.textContent = STATS.masini; return; }
      const t0 = performance.now(), dur = 1600;
      const step = (t) => { const k = Math.min((t - t0) / dur, 1); num.textContent = Math.round(STATS.masini * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }, { threshold: .6 }).observe(box);
  }
  $$("[data-phone]").forEach((a) => {
    a.href = `tel:${CONTACT.phone}`;
    const t = $("[data-phone-label]", a);
    if (t) t.textContent = CONTACT.phoneLabel; else a.lastChild.textContent = " " + CONTACT.phoneLabel;
  });
  $$("[data-wa]").forEach((a) => { a.href = waLink(a.dataset.wa || "Bună, aș vrea mai multe detalii despre detailing."); a.target = "_blank"; a.rel = "noopener"; });
  if (CONTACT.googleReview) $$("[data-google-review]").forEach((a) => { a.href = CONTACT.googleReview; a.target = "_blank"; a.rel = "noopener"; });
  if (CONTACT.googleProfile) $$("[data-google-profile]").forEach((a) => { a.href = CONTACT.googleProfile; a.target = "_blank"; a.rel = "noopener"; });

  /* ---------- photos ---------- */
  const fileIn = $("#poze"), thumbs = $("#thumbs"), drop = $("#drop");
  const compress = (file) => new Promise((resolve) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      const k = Math.min(1, 1600 / Math.max(img.width, img.height));
      const c = document.createElement("canvas");
      c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url);
      c.toBlob((b) => resolve(b ? new File([b], (file.name.replace(/\.[^.]+$/, "") || "poza") + ".jpg", { type: "image/jpeg" }) : file), "image/jpeg", 0.82);
    };
    img.onerror = () => { URL.revokeObjectURL(url); resolve(null); };
    img.src = url;
  });
  const paintThumbs = () => {
    thumbs.innerHTML = "";
    state.files.forEach((f, i) => {
      const li = document.createElement("li");
      const im = document.createElement("img");
      im.alt = `Poza ${i + 1}`;
      im.src = URL.createObjectURL(f);
      im.onload = () => URL.revokeObjectURL(im.src);
      const x = document.createElement("button");
      x.type = "button"; x.setAttribute("aria-label", `Șterge poza ${i + 1}`);
      x.innerHTML = '<i class="ph ph-x"></i>';
      x.addEventListener("click", () => { state.files.splice(i, 1); paintThumbs(); });
      li.append(im, x); thumbs.append(li);
    });
    const n = state.files.length, cnt = $("#poze-count");
    cnt.textContent = n ? `${n} din ${MAX_PHOTOS} poze adăugate.${n < MAX_PHOTOS ? " Mai poți adăuga." : ""}` : "Poți adăuga până la 6 poze. Le poți face și mai târziu și ni le trimiți pe WhatsApp.";
    $$(".pbtn").forEach((b) => b.classList.toggle("is-full", n >= MAX_PHOTOS));
  };
  const addFiles = async (list) => {
    const imgs = [...list].filter((f) => f.type.startsWith("image/")).slice(0, MAX_PHOTOS - state.files.length);
    const done = await Promise.all(imgs.map(compress));
    state.files.push(...done.filter(Boolean));
    paintThumbs();
  };
  // gallery (multiple) and camera (one shot at a time) feed the same list
  [fileIn, $("#poze-cam")].forEach((inp) => inp.addEventListener("change", () => { addFiles(inp.files); inp.value = ""; }));
  ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("is-over"); }));
  ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("is-over"); }));
  drop.addEventListener("drop", (e) => addFiles(e.dataTransfer.files));

  /* ---------- submit ---------- */
  const form = $("#form");
  const ok = $("#ok");
  const bad = (id, isBad) => {
    const f = $("#" + id).closest(".field");
    f.classList.toggle("is-bad", isBad);
    $(".err", f).hidden = !isBad;
  };

  /* ---------- confirmation letter ---------- */
  const letter = $("#letter"), ltStatus = $("#lt-status"), ltHint = $("#lt-hint");
  const ALPH = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; // no 0/O/1/I to avoid confusion when read aloud
  const makeRef = () => {
    const d = new Date();
    const ymd = String(d.getFullYear()).slice(2) + String(d.getMonth() + 1).padStart(2, "0") + String(d.getDate()).padStart(2, "0");
    const rnd = crypto.getRandomValues(new Uint32Array(4));
    return `ETA-${ymd}-${[...rnd].map((n) => ALPH[n % ALPH.length]).join("")}`;
  };
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  let pending = null; // { msg, files }

  const setStatus = (state, text, icon) => {
    ltStatus.dataset.state = state;
    ltStatus.innerHTML = `<i class="ph ${icon}"></i><span>${text}</span>`;
  };

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = form.nume.value.trim();
    const digits = form.tel.value.replace(/\D/g, "");
    bad("nume", name.length < 2);
    bad("tel", digits.length < 9);
    if (name.length < 2 || digits.length < 9) { (name.length < 2 ? form.nume : form.tel).focus(); return; }

    const { size, plan, tier, files } = state;
    const ref = makeRef();
    const carTxt = form.masina.value.trim();
    const loc = `${state.zona === "buc" ? "București" : "În afara Bucureștiului"}${form.adresa.value.trim() ? ", " + form.adresa.value.trim() : ""}`;
    const paid = hasInterior() ? state.extras.filter((k) => !isIncluded(k)) : [];
    const incl = hasInterior() && tier === "intensiv" ? INCLUDED_INTENSIV.map((k) => EXTRA_NAME[k].toLowerCase()).join(", ") : "";
    const extras = paid.map((k) => `${EXTRA_NAME[k]} (${EXTRA_PRICES[k]} lei)`).join(", ");
    const price = `${totalOf()} lei${state.zona === "afara" ? " + deplasare" : ""}`;

    const rows = [
      ["Nume", name],
      ["Telefon", form.tel.value.trim()],
      ["Mașina", carTxt ? `${carTxt}, clasa ${SIZE_NAME[size].toLowerCase()}` : `Clasa ${SIZE_NAME[size].toLowerCase()}`, true],
      ["Pachet", PLAN_NAME[plan]],
      plan !== "motor" && ["Nivel de curățare", TIER_NAME[tier]],
      incl && ["Incluse", incl, true],
      extras && ["Extra", extras, true],
      ["Locație", loc + (state.zona === "afara" ? " (deplasare stabilită împreună)" : "")],
      files.length && ["Poze", `${files.length} ${files.length === 1 ? "poză" : "poze"}`, true],
      form.mesaj.value.trim() && ["Mesaj", form.mesaj.value.trim(), true],
    ].filter(Boolean);

    $("#lt-ref").textContent = ref;
    $("#lt-date").textContent = new Date().toLocaleDateString("ro-RO", { day: "numeric", month: "long", year: "numeric" });
    $("#lt-name").textContent = name.split(" ")[0];
    $("#lt-rows").innerHTML = rows.map(([k, v, wide]) => `<div${wide ? ' class="is-wide"' : ""}><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join("");
    // the photos go on the letter too, as small prints next to the count
    const pozeDd = [...$("#lt-rows").children].find((d) => d.firstChild.textContent === "Poze")?.lastChild;
    if (pozeDd) {
      const strip = document.createElement("span");
      strip.className = "letter__pics";
      files.forEach((f) => { const im = new Image(); im.alt = ""; im.src = URL.createObjectURL(f); strip.append(im); });
      pozeDd.append(strip);
    }
    $("#lt-total").textContent = price;
    setStatus("draft", "Netrimisă încă", "ph-clock");
    ltHint.textContent = "";

    const msg = [
      `Salut, vreau o programare la ETA PRO CLEANING.`,
      `Referință: ${ref}`,
      ...rows.map(([k, v]) => `${k}: ${v}`),
      `Estimare: ${price}`,
    ].join("\n");
    pending = { msg, files: files.slice() };
    letter.showModal();
    fitLetter();
    // on the A4 sheet only the details scroll; flag it so the fade + hint show
    const rowsEl = $("#lt-rows");
    rowsEl.scrollTop = 0;
    letter.classList.toggle("is-long", rowsEl.scrollHeight > rowsEl.clientHeight + 2);
    $("#lt-send").focus();
  });

  // Scale the A4 page (640 x 905, see styles.css) to the screen, like a PDF viewer.
  // Phones (under 561px) get the plain scrolling letter instead.
  const SHEET_W = 640, SHEET_H = 905;
  function fitLetter() {
    const doc = $("#letter-doc");
    if (innerWidth < 561) { doc.style.zoom = ""; return; }
    const actions = $(".letter__actions").offsetHeight;
    const s = Math.min(1, (innerHeight - 32 - actions) / SHEET_H, (innerWidth - 32) / SHEET_W);
    doc.style.zoom = s.toFixed(3);
  }
  addEventListener("resize", () => { if (letter.open) fitLetter(); });

  $("#lt-send").addEventListener("click", async () => {
    if (!pending) return;
    const { msg, files } = pending;
    // On phones the share sheet can carry the photos straight into WhatsApp.
    if (files.length && navigator.canShare && navigator.canShare({ files })) {
      try {
        await navigator.share({ files, text: msg, title: "Programare ETA PRO CLEANING" });
        setStatus("sent", "Trimisă", "ph-check-circle");
        ltHint.textContent = "Mulțumim! Revenim în cel mai scurt timp cu confirmarea.";
        return;
      } catch (err) {
        if (err && err.name === "AbortError") { ltHint.textContent = "Trimiterea a fost anulată. Poți încerca din nou."; return; }
      }
    }
    open(waLink(msg), "_blank", "noopener");
    setStatus("sent", "Deschisă în WhatsApp", "ph-check-circle");
    ltHint.textContent = files.length
      ? "Apasă Trimite în WhatsApp. Pozele nu se pot atașa automat de pe acest dispozitiv, adaugă-le direct în conversație."
      : "Apasă Trimite în WhatsApp ca să ajungă la noi.";
  });

  $("#lt-print").addEventListener("click", () => {
    document.documentElement.classList.add("print-letter");
    const done = () => { document.documentElement.classList.remove("print-letter"); removeEventListener("afterprint", done); };
    addEventListener("afterprint", done);
    print();
  });
  letter.addEventListener("click", (e) => { if (e.target === letter || e.target.closest("[data-close]")) letter.close(); });

  $("#yr").textContent = new Date().getFullYear();
})();
