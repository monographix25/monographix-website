/* =========================================================
   MONOGRAPHIX – Interaktion
   • Sticky Header & Mobile-Navigation
   • Scroll-Reveal
   • Instagram-Slider (ohne Fremd-Skript)
   • Vorher/Nachher-Regler
   • Buchungskalender + Preisrechner
   • DSGVO-Einwilligung für Instagram & Google Maps
   • Formulare (Demo-Modus ohne Backend)
   ========================================================= */
(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Header ---------- */
  const header = $(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-stuck", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const toggle = $(".nav__toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
    });
    $$(".nav__links a").forEach((a) =>
      a.addEventListener("click", () => {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      })
    );
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- Scroll-Reveal ---------- */
  const revealItems = $$(".reveal");
  if (revealItems.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealItems.forEach((el) => el.classList.add("is-in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const delay = Number(entry.target.dataset.delay || 0);
              window.setTimeout(() => entry.target.classList.add("is-in"), delay);
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
      );
      revealItems.forEach((el, i) => {
        if (!el.dataset.delay && i % 3) el.dataset.delay = String((i % 3) * 80);
        io.observe(el);
      });
    }
  }

  /* ---------- Instagram-Slider ---------- */
  $$("[data-slider]").forEach((wrap) => {
    const track = $(".ig__grid", wrap);
    const prev = $("[data-slider-prev]", wrap);
    const next = $("[data-slider-next]", wrap);
    if (!track) return;

    const step = () => {
      const first = track.querySelector(".ig__item");
      const gap = parseFloat(getComputedStyle(track).columnGap || "12") || 12;
      return first ? first.getBoundingClientRect().width + gap : 260;
    };
    const update = () => {
      if (!prev || !next) return;
      const max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    };
    const scrollByStep = (dir) =>
      track.scrollBy({ left: dir * step(), behavior: reduceMotion ? "auto" : "smooth" });

    prev?.addEventListener("click", () => scrollByStep(-1));
    next?.addEventListener("click", () => scrollByStep(1));
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  /* ---------- Fehlende Fotos abfangen ---------- */
  $$("img").forEach((img) => {
    const mark = () => {
      img.classList.add("img-missing");
      const parent = img.closest(".card__media, .ig__item, .course-figure, .hero__media, .gutschein-card");
      if (parent) {
        parent.classList.add("img-empty");
        if (!parent.dataset.label) {
          const label = img.alt ? img.alt.split("–")[0].trim() : "Foto";
          parent.dataset.label = label.length > 34 ? label.slice(0, 32) + "…" : label;
        }
      }
    };
    if (img.complete && img.naturalWidth === 0) mark();
    img.addEventListener("error", mark, { once: true });
  });

  /* ---------- Buchungskalender ---------- */
  const cal = $("[data-calendar]");
  if (cal) {
    const grid = $(".calendar__grid", cal);
    const title = $(".calendar__title", cal);
    const input = $("#kursdatum");
    const output = $("[data-date-output]");
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    let cursor = new Date(today.getFullYear(), today.getMonth(), 1);
    let selected = null;

    const WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
    const MONTHS = [
      "Januar", "Februar", "März", "April", "Mai", "Juni",
      "Juli", "August", "September", "Oktober", "November", "Dezember",
    ];

    // Verfügbarkeit deterministisch aus dem Datum ableiten (Demo-Daten).
    const isFree = (d) => {
      const dow = d.getDay();
      const seeded = (d.getDate() * 7 + d.getMonth() * 13) % 10;
      if (dow === 0) return seeded < 7;
      if (dow === 5 || dow === 6) return seeded < 9;
      return seeded < 6;
    };

    // Uhrzeiten: Mo-Do ab 16 Uhr, Fr-So ganztags
    const timeSlots = (d) => {
      const dow = d ? d.getDay() : 1;
      const openAllDay = dow === 5 || dow === 6 || dow === 0;
      const start = openAllDay ? 10 : 16;
      const slots = [];
      for (let h = start; h <= 19; h++) slots.push(`${String(h).padStart(2, "0")}:00`);
      return slots;
    };

    const timeSelect = $("#uhrzeit");
    const timeHint = $("[data-time-hint]");

    const fillTimes = (d) => {
      if (!timeSelect) return;
      timeSelect.innerHTML = "";
      const first = document.createElement("option");
      first.value = "";
      first.textContent = "Bitte wählen …";
      timeSelect.appendChild(first);
      timeSlots(d).forEach((t) => {
        const o = document.createElement("option");
        o.value = t;
        o.textContent = `${t} Uhr`;
        timeSelect.appendChild(o);
      });
      timeSelect.disabled = false;
      if (timeHint) {
        const dow = d ? d.getDay() : 1;
        const allDay = dow === 5 || dow === 6 || dow === 0;
        timeHint.textContent = allDay
          ? "Ganztägig möglich: 10–19 Uhr"
          : "Unter der Woche ab 16 Uhr möglich";
      }
    };

    const render = () => {
      if (!grid) return;
      grid.innerHTML = "";
      WEEKDAYS.forEach((w) => {
        const el = document.createElement("div");
        el.className = "calendar__dow";
        el.textContent = w;
        grid.appendChild(el);
      });
      if (title)
        title.textContent = `${MONTHS[cursor.getMonth()]} ${cursor.getFullYear()}`;

      const first = new Date(cursor.getFullYear(), cursor.getMonth(), 1);
      const offset = (first.getDay() + 6) % 7; // Montag = 0
      const days = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 0).getDate();

      for (let i = 0; i < offset; i++) {
        grid.appendChild(document.createElement("div"));
      }
      for (let day = 1; day <= days; day++) {
        const date = new Date(cursor.getFullYear(), cursor.getMonth(), day);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "cal-day";
        btn.textContent = String(day);

        const past = date < today;
        const free = !past && isFree(date);
        if (past) {
          btn.disabled = true;
        } else if (free) {
          btn.classList.add("is-free");
          btn.setAttribute("aria-label", `${day}. ${MONTHS[cursor.getMonth()]} – Platz frei`);
        } else {
          btn.disabled = true;
          btn.setAttribute("aria-label", `${day}. ${MONTHS[cursor.getMonth()]} – ausgebucht`);
        }
        if (selected && date.toDateString() === selected.toDateString()) {
          btn.classList.add("is-selected");
        }
        btn.addEventListener("click", () => {
          selected = date;
          const pad = (n) => String(n).padStart(2, "0");
          const iso = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
          if (input) input.value = iso;
          fillTimes(date);
          if (output) {
            output.textContent = date.toLocaleDateString("de-DE", {
              weekday: "long",
              day: "2-digit",
              month: "long",
              year: "numeric",
            });
            output.hidden = false;
          }
          $$(".cal-day", grid).forEach((b) => b.classList.remove("is-selected"));
          btn.classList.add("is-selected");
          $$("[data-date-empty]").forEach((el) => (el.hidden = true));
          const form = $("#buchung");
          if (form) form.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        });
        grid.appendChild(btn);
      }
    };

    $("[data-cal-prev]", cal)?.addEventListener("click", () => {
      cursor = new Date(cursor.getFullYear(), cursor.getMonth() - 1, 1);
      render();
    });
    $("[data-cal-next]", cal)?.addEventListener("click", () => {
      cursor = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 1);
      render();
    });
    render();
    if (timeSelect) {
      timeSelect.disabled = true;
      if (timeHint) timeHint.textContent = "Bitte zuerst ein Datum wählen";
    }
  }

  /* ---------- Kurs-Filter ---------- */
  const filterButtons = $$("[data-filter]");
  if (filterButtons.length) {
    const items = $$("[data-cat]");
    filterButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const cat = btn.dataset.filter;
        filterButtons.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        items.forEach((item) => {
          item.hidden = !(cat === "all" || item.dataset.cat.includes(cat));
        });
      });
    });
  }

  /* ---------- Vorauswahl aus der URL (?kurs=action-painting) ---------- */
  const params = new URLSearchParams(window.location.search);
  const preset = params.get("kurs");
  if (preset) {
    const field = $("#kurs");
    if (field) {
      const option = Array.from(field.options).find((o) => o.value === preset);
      if (option) {
        field.value = preset;
        field.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }
  }

  /* ---------- Preisrechner ---------- */
  const estimator = $("[data-estimator]");
  if (estimator) {
    const course = $("#kurs", estimator);
    const people = $("#personen", estimator);
    const total = $("[data-total]", estimator);
    const calc = () => {
      const base = Number(course?.selectedOptions[0]?.dataset.price || 0);
      const persons = Math.max(1, Number(people?.value || 1));
      const sum = base * persons;
      if (total)
        total.textContent = sum
          ? sum.toLocaleString("de-DE", { style: "currency", currency: "EUR", maximumFractionDigits: 0 })
          : "–";
    };
    course?.addEventListener("change", calc);
    people?.addEventListener("input", calc);
    calc();
  }

  /* ---------- Gutschein-Schnellwahl ---------- */
  $$("[data-voucher]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const field = $("#gutschein-wert");
      if (field) {
        field.value = btn.dataset.voucher;
        field.dispatchEvent(new Event("change", { bubbles: true }));
      }
      document.getElementById("gutschein-form")?.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "center",
      });
    });
  });

  /* ---------- DSGVO-Einwilligung (Instagram / Maps) ---------- */
  const CONSENT_KEY = "monographix-consent";
  const store = {
    get() {
      try {
        return JSON.parse(localStorage.getItem(CONSENT_KEY) || "{}");
      } catch {
        return {};
      }
    },
    set(key) {
      const data = store.get();
      data[key] = Date.now();
      try {
        localStorage.setItem(CONSENT_KEY, JSON.stringify(data));
      } catch {
        /* Speicher nicht verfügbar – Einwilligung gilt nur für diese Sitzung */
      }
    },
  };

  $$("[data-consent-embed]").forEach((box) => {
    const key = box.dataset.consentEmbed;
    const btn = $("[data-consent-accept]", box);

    const load = () => {
      const src = btn?.dataset.src;
      if (!src) return;
      const frame = document.createElement("iframe");
      frame.src = src;
      frame.loading = "lazy";
      frame.title = box.dataset.title || "Externer Inhalt";
      frame.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
      frame.setAttribute("allowfullscreen", "");
      frame.style.cssText =
        "position:relative;width:100%;height:" +
        (box.dataset.height || "420") +
        "px;border:0;display:block";
      const inner = $(".consent-box__inner", box);
      inner?.remove();
      const bg = $(".consent-box__bg", box);
      if (bg) bg.remove();
      box.style.padding = "0";
      box.style.minHeight = "0";
      box.appendChild(frame);
    };

    btn?.addEventListener("click", () => {
      store.set(key);
      load();
    });
    if (store.get()[key]) load();
  });

  /* ---------- Formulare ---------- */
  const MAIL_FALLBACK = "monographix25@gmail.com";

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const CONFIRM_TITLES = {
    booking: "Termin angefragt",
    event: "Anfrage gesendet",
    order: "Bestellung eingegangen",
  };

  const confirmationHTML = (form, rows, total) => {
    const kind = form.dataset.confirm || "booking";
    const title = CONFIRM_TITLES[kind] || CONFIRM_TITLES.booking;
    const list = rows
      .map((r) => `<div class="confirm__row"><dt>${esc(r.label)}</dt><dd>${esc(r.value)}</dd></div>`)
      .join("");
    return `
      <div class="confirm">
        <div class="confirm__head">
          <span class="confirm__badge" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor"
                 stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
          </span>
          <div>
            <strong>${title}</strong>
            <span>Danke! Deine Anfrage ist bei uns eingegangen.</span>
          </div>
        </div>
        <dl class="confirm__list">${list}</dl>
        ${total ? `<p class="confirm__total"><span>Voraussichtlicher Preis</span><b>${esc(total)}</b></p>` : ""}
        <p class="confirm__note">
          Du bekommst innerhalb von 24 Stunden eine Bestätigung per E-Mail.
          Fragen? <a href="mailto:${MAIL_FALLBACK}">${MAIL_FALLBACK}</a>
        </p>
      </div>`;
  };

  const fieldLabel = (el) => {
    if (el.id) {
      const label = document.querySelector(`label[for="${el.id}"]`);
      if (label) return label.textContent.replace(/\s*\(optional\)/i, "").trim();
    }
    const wrap = el.closest(".field, .check");
    const label = wrap?.querySelector("label");
    return label ? label.textContent.trim() : el.name || "Feld";
  };

  const IGNORE_FIELDS = ["datenschutz", "agb", "terms", "newsletter"];
  const prettyValue = (el, value) => {
    if (el.type === "date" && /^\d{4}-\d{2}-\d{2}$/.test(value)) {
      const [y, m, d] = value.split("-");
      return `${d}.${m}.${y}`;
    }
    return value;
  };

  const collectFields = (form) => {
    const rows = [];
    Array.from(form.elements).forEach((el) => {
      if (!el.name || el.type === "submit" || el.type === "button" || el.type === "file") return;
      if (IGNORE_FIELDS.includes(el.name)) return;
      if (el.type === "checkbox" || el.type === "radio") {
        if (el.checked) rows.push({ label: fieldLabel(el), value: "ja" });
        return;
      }
      if (el.tagName === "SELECT") {
        const opt = el.selectedOptions && el.selectedOptions[0];
        if (opt && opt.value) rows.push({ label: fieldLabel(el), value: opt.textContent.trim() });
        return;
      }
      const value = (el.value || "").trim();
      if (!value) return;
      rows.push({ label: fieldLabel(el), value: prettyValue(el, value) });
    });
    return rows;
  };

  const buildMailto = (form, to) => {
    const lines = collectFields(form).map((r) => `${r.label}: ${r.value}`);

    const subject = form.dataset.subject || "Anfrage über die Website";
    const body = `${lines.join("\r\n")}\r\n\r\n--\r\nGesendet über die Website`;
    return `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  };

  $$("form[data-form]").forEach((form) => {
    const status = $(".form-status", form);
    const endpoint = form.dataset.endpoint || "";

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;

      const submit = $('[type="submit"]', form);
      const label = submit?.innerHTML;
      const sendingText = endpoint ? "Wird gesendet …" : "Wird geöffnet …";
      if (submit) {
        submit.disabled = true;
        submit.innerHTML = sendingText;
      }

      const restore = () => {
        if (submit) {
          submit.disabled = false;
          if (label) submit.innerHTML = label;
        }
      };

      /* --- Ohne Backend: E-Mail-Programm mit fertiger Nachricht öffnen --- */
      if (!endpoint) {
        const to = form.dataset.mailto || MAIL_FALLBACK;
        const href = buildMailto(form, to);

        if (status) {
          status.innerHTML =
            "Dein E-Mail-Programm wurde mit der fertigen Anfrage geöffnet. " +
            "Bitte dort nur noch auf <strong>Senden</strong> klicken." +
            `<br><span style="font-size:.85em;opacity:.8">Öffnet sich nichts? ` +
            `<a href="${href}">Nachricht manuell öffnen</a> oder an ` +
            `<a href="mailto:${to}">${to}</a> schreiben.</span>`;
          status.classList.add("is-visible");
          status.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        }

        window.location.href = href;
        restore();
        return;
      }

      /* --- Versand über Formulardienst (FormSubmit) --- */
      try {
        const data = new FormData(form);
        const subject = form.dataset.subject || "Anfrage über die Website";
        data.append("_subject", subject);
        data.append("_template", "table");
        data.append("_captcha", "false");
        const mailField = form.querySelector('input[type="email"]');
        if (mailField?.value) data.append("_replyto", mailField.value);

        const res = await fetch(endpoint, {
          method: "POST",
          body: data,
          headers: { Accept: "application/json" },
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const json = await res.json().catch(() => ({}));
        const msg = String(json.message || "");
        if (/activation/i.test(msg)) {
          // Einmalige Freischaltung durch den Website-Betreiber
          throw new Error("ACTIVATION");
        }
        if (String(json.success) === "false") throw new Error(msg || "Versand fehlgeschlagen");

        // Bestätigung anzeigen (vor dem Zurücksetzen auslesen)
        const rows = collectFields(form);
        const totalEl = form.querySelector("[data-total]");
        const total = totalEl && totalEl.textContent.trim() !== "–" ? totalEl.textContent.trim() : "";
        form.reset();

        if (status) {
          status.innerHTML = form.dataset.confirm
            ? confirmationHTML(form, rows, total)
            : "<strong>Danke – deine Nachricht ist raus!</strong><br>Wir melden uns innerhalb von 24 Stunden bei dir.";
          status.classList.add("is-visible");
          if (form.dataset.confirm) status.classList.add("is-confirm");
          status.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        }
        restore();
      } catch (err) {
        // Fallback: fertige E-Mail im Mailprogramm öffnen
        const to = form.dataset.mailto || MAIL_FALLBACK;
        const href = buildMailto(form, to);
        if (status) {
          status.innerHTML =
            err.message === "ACTIVATION"
              ? "Der Versand ist eingerichtet und muss nur noch einmalig per E-Mail bestätigt werden. " +
                `Bis dahin: <a href="${href}">Nachricht per E-Mail-Programm senden</a>.`
              : "Der automatische Versand hat gerade nicht geklappt. " +
                `<a href="${href}">Nachricht jetzt per E-Mail-Programm senden</a> ` +
                `oder direkt an <a href="mailto:${to}">${to}</a> schreiben.`;
          status.classList.add("is-visible");
          status.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        }
        restore();
        console.error("[Formular]", err);
      }
    });
  });

  /* ---------- Aktuelles Jahr ---------- */
  $$("[data-year]").forEach((el) => (el.textContent = String(new Date().getFullYear())));
})();
