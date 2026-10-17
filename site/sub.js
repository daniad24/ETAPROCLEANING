/* ETA PRO CLEANING: interacțiuni pentru paginile secundare (despre, portofoliu, blog, zone, servicii). */
(() => {
  const C = window.ETA_CONFIG;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const wa = (t) => `https://wa.me/${C.whatsapp}?text=${encodeURIComponent(t)}`;

  /* nav: background after scrolling (sentinel), mobile menu */
  const nav = $("#nav");
  const sentinel = document.createElement("div");
  sentinel.style.cssText = "position:absolute;top:0;height:24px;width:1px;pointer-events:none";
  document.body.prepend(sentinel);
  new IntersectionObserver(([e]) => nav.classList.toggle("is-stuck", !e.isIntersecting)).observe(sentinel);

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

  /* reveal */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  $$(".reveal").forEach((el) => io.observe(el));

  /* contact links */
  $$("[data-wa]").forEach((a) => { a.href = wa(a.dataset.wa || "Bună, aș vrea mai multe detalii despre detailing."); a.target = "_blank"; a.rel = "noopener"; });
  $$("[data-phone]").forEach((a) => {
    a.href = `tel:${C.phone}`;
    const t = $("[data-phone-label]", a);
    if (t) t.textContent = C.phoneLabel;
  });

  /* before / after */
  $$("[data-ba]").forEach((el) => {
    const range = $(".ba__range", el);
    const set = (v) => el.style.setProperty("--p", v + "%");
    range.addEventListener("input", () => set(range.value));
    set(range.value);
    $$(".ba__img", el).forEach((fig) => {
      const img = $("img", fig);
      img.onerror = () => { if (window.__img && window.__img(img)) return; fig.classList.add("is-empty"); };
      if (img.dataset.src) img.src = img.dataset.src;
    });
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
  });

  /* ---------- how steam works: plays while visible, never locks scroll ---------- */
  const how = $(".how");
  if (how) {
    const K = [0, 0.38, 0.72, 1], STEP_MS = 3200;
    const items = $$("#how-steps li");
    let cur = 0, timer = null, visible = false, paused = false;
    how.style.setProperty("--step-ms", STEP_MS + "ms");
    const go = (i) => {
      cur = i;
      how.style.setProperty("--k", K[i]);
      how.classList.toggle("is-edge", i === 0 || i === K.length - 1);
      items.forEach((li, j) => { li.classList.remove("is-on"); if (j === i) { void li.offsetWidth; li.classList.add("is-on"); } });
    };
    const stop = () => { clearInterval(timer); timer = null; };
    const play = () => {
      stop();
      if (reduce || !visible || paused) return;
      timer = setInterval(() => go((cur + 1) % K.length), STEP_MS);
    };
    items.forEach((li, i) => $("button", li).addEventListener("click", () => { go(i); play(); }));
    how.addEventListener("pointerenter", () => { paused = true; how.classList.add("is-paused"); stop(); });
    how.addEventListener("pointerleave", () => { paused = false; how.classList.remove("is-paused"); play(); });
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; visible ? play() : stop(); }, { threshold: 0.35 }).observe(how);
    go(reduce ? 3 : 0);
  }

  /* gallery + lightbox */
  const lb = $("#lightbox");
  $$(".gal__item").forEach((btn) => {
    const im = $("img", btn);
    im.addEventListener("error", () => {
      if (window.__img && window.__img(im)) { btn.dataset.src = im.src; return; }
      btn.classList.add("is-empty"); btn.disabled = true; im.remove();
    });
    if (!lb) return;
    btn.addEventListener("click", () => {
      if (btn.classList.contains("is-empty")) return;
      const big = $("img", lb);
      big.src = btn.dataset.src || im.src; big.alt = im.alt;
      lb.showModal();
    });
  });
  if (lb) lb.addEventListener("click", (e) => { if (e.target === lb || e.target.closest("[data-close]")) lb.close(); });

  /* portfolio filters */
  const grid = $("#pf-grid");
  if (grid) {
    const cards = $$(".pf-card", grid);
    const empty = $("#pf-empty");
    const state = { marca: "toate", tip: "toate" };
    const apply = () => {
      let shown = 0;
      cards.forEach((c) => {
        const ok = (state.marca === "toate" || c.dataset.marca === state.marca) && (state.tip === "toate" || c.dataset.tip === state.tip);
        c.hidden = !ok;
        if (ok) shown++;
      });
      empty.hidden = shown > 0;
      $("#pf-count").textContent = shown === 1 ? "1 lucrare" : `${shown} lucrări`;
    };
    $$("[data-filter]").forEach((group) => {
      group.addEventListener("click", (e) => {
        const b = e.target.closest("button");
        if (!b) return;
        state[group.dataset.filter] = b.dataset.value;
        $$("button", group).forEach((x) => x.setAttribute("aria-pressed", x === b));
        apply();
      });
    });
    $("#pf-reset").addEventListener("click", () => {
      state.marca = "toate"; state.tip = "toate";
      $$("[data-filter] button").forEach((x) => x.setAttribute("aria-pressed", x.dataset.value === "toate"));
      apply();
    });
    apply();
  }

  if (C.googleReview) $$("[data-google-review]").forEach((a) => { a.href = C.googleReview; a.target = "_blank"; a.rel = "noopener"; });

  const yr = $("#yr");
  if (yr) yr.textContent = new Date().getFullYear();
})();
