# -*- coding: utf-8 -*-
"""
Baut die Kurs-Detailseiten aus einer gemeinsamen Vorlage.
Aufruf:  python tools/build_detail_pages.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="canonical" href="https://www.monographix-studio.de/{{SLUG}}.html">
<meta property="og:title" content="{{OGTITLE}}">
<meta property="og:description" content="{{DESC}}">
<meta property="og:image" content="{{IMG}}">
<meta name="theme-color" content="#14100F">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add("js");</script>
</head>
<body>
<a class="skip-link" href="#main">Zum Inhalt springen</a>

<div class="topbar">
  <div class="topbar__inner">
    <span class="topbar__spark" aria-hidden="true"></span>
    <span>{{TOPBAR}}</span>
    <a href="#buchen">Platz sichern →</a>
  </div>
</div>

<header class="site-header">
  <div class="container">
    <nav class="nav" aria-label="Hauptnavigation">
      <a class="brand" href="index.html">
        <img class="brand__mark" src="assets/img/logo.svg" alt="" width="26" height="26">
        <span>Monographix<small>Atelier für Kreativität</small></span>
      </a>
      <ul class="nav__links" id="nav-links">
        <li><a href="kurse.html" aria-current="page">Kurse &amp; Workshops</a></li>
        <li><a href="teamevents.html">Teamevents &amp; Feiern</a></li>
        <li><a href="ueber-mich.html">Über mich</a></li>
        <li><a href="gutscheine.html">Gutscheine</a></li>
        <li><a href="kontakt.html">Kontakt</a></li>
      </ul>
      <div class="nav__cta">
        <a class="btn btn--accent" href="#buchen">Kurs buchen</a>
        <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Menü öffnen"><span aria-hidden="true"></span></button>
      </div>
    </nav>
  </div>
</header>

<main id="main">

  <section class="page-head">
    <div class="container">
      <ol class="breadcrumb">
        <li><a href="index.html">Start</a></li>
        <li><a href="kurse.html">Kurse</a></li>
        <li>{{NAME}}</li>
      </ol>
      <span class="badge {{BADGECLASS}}">{{BADGE}}</span>
      <h1 style="margin-top:.6rem">{{NAME}}</h1>
      <p class="lead">{{LEAD}}</p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="course-detail">
        <div class="reveal">
          <figure class="course-figure">
            <img src="{{IMG}}" alt="{{ALT}}" width="1200" height="1600">
          </figure>

          <h2 style="margin-top:2rem">Worum es geht</h2>
          {{INTRO}}

          <h2>Ablauf</h2>
          <ol class="checklist">
            {{STEPS}}
          </ol>

          <h2>Für wen ist der Kurs?</h2>
          {{AUDIENCE}}

          <div class="note" style="margin-top:1.5rem">
            {{NOTE}}
          </div>
        </div>

        <aside class="reveal">
          <div class="price-block">
            <p class="eyebrow" style="color:var(--ink);margin-bottom:.4rem">Preis pro Person</p>
            <div class="price">{{PRICE}} <small>{{PRICEUNIT}}</small></div>
            <ul>
              {{INCLUDES}}
            </ul>
            <a class="btn btn--block btn--lg" href="#buchen">Freien Platz sichern</a>
            <p class="form-note" style="margin:.7rem 0 0">Kostenlose Umbuchung bis 72 Std. vorher.</p>
          </div>

          <div class="sidebar-card">
            <h3 style="font-size:1.05rem">Auf einen Blick</h3>
            <ul class="facts">
              {{FACTS}}
            </ul>
          </div>

          <div class="sidebar-card">
            <h3 style="font-size:1.05rem">Als Gruppe buchen?</h3>
            <p style="font-size:.94rem;color:var(--ink-soft)">Ab 6 Personen gestalten wir Termin, Motto und Ablauf individuell – auch bei euch vor Ort.</p>
            <a class="btn btn--ghost btn--block" href="teamevents.html">Teamevent anfragen</a>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="section section--cream" id="termine">
    <div class="container">
      <div class="section-head reveal">
        <p class="eyebrow">Termine</p>
        <h2>{{NAME}} – nächste Kurse</h2>
      </div>
      <div class="grid grid-3">
        {{DATES}}
      </div>
    </div>
  </section>

  <section class="section" id="buchen">
    <div class="container">
      <div class="split" style="align-items:start">
        <div class="reveal">
          <p class="eyebrow">Buchung</p>
          <h2>Platz sichern</h2>
          <p class="lead">Datum aus dem Kalender wählen, Daten eintragen – fertig. Du bekommst eine Bestätigung mit allen Infos.</p>
          <div class="calendar" data-calendar style="margin-top:1.5rem">
            <div class="calendar__head">
              <button class="slider-btn" type="button" data-cal-prev aria-label="Vorheriger Monat">←</button>
              <span class="calendar__title">Monat</span>
              <button class="slider-btn" type="button" data-cal-next aria-label="Nächster Monat">→</button>
            </div>
            <div class="calendar__grid" role="group" aria-label="Verfügbare Kurstage"></div>
            <div class="calendar__legend">
              <span class="free"><i></i> Platz frei</span>
              <span><i></i> ausgebucht / Ruhetag</span>
            </div>
          </div>
          <p class="form-note" style="margin-top:.8rem">Gewählt: <span data-date-output hidden>–</span><span data-date-empty>noch kein Termin</span></p>
        </div>

        <form class="form reveal" data-confirm="booking" data-mailto="monographix25@gmail.com" data-subject="Kursbuchung {{NAME}}" data-form data-endpoint="https://formsubmit.co/ajax/monographix25@gmail.com" data-estimator style="background:#fff;border:2px solid var(--ink);border-radius:var(--radius);padding:1.6rem">
          <input type="hidden" name="kurs" value="{{SLUG}}">
          <div class="form-grid">
            <div class="field">
              <label for="kurs">Kursvariante</label>
              <select id="kurs" name="variante">
                {{OPTIONS}}
              </select>
            </div>
            <div class="field">
              <label for="personen">Personen</label>
              <input id="personen" name="personen" type="number" min="1" max="10" value="1" required>
            </div>
            <div class="field">
              <label for="kursdatum">Datum</label>
              <input id="kursdatum" name="datum" type="date" required>
            </div>
            <div class="field">
              <label for="name">Name</label>
              <input id="name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="mail">E-Mail</label>
              <input id="mail" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="tel">Telefon <span class="hint">(optional)</span></label>
              <input id="tel" name="telefon" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field">
            <label for="nachricht">Anlass oder Wünsche <span class="hint">(optional)</span></label>
            <textarea id="nachricht" name="nachricht" placeholder="Geburtstag, Firmenfeier, Vorkenntnisse …"></textarea>
          </div>
          <div class="price-block" style="box-shadow:none;background:var(--paper-2);border-radius:14px;padding:1rem 1.2rem">
            <div class="btn-row" style="justify-content:space-between">
              <span style="font-weight:700">Voraussichtlicher Preis</span>
              <strong data-total style="font-family:var(--font-display);font-size:1.5rem">–</strong>
            </div>
          </div>
          <label class="check">
            <input type="checkbox" required name="datenschutz">
            <span>Ich stimme der <a href="datenschutz.html">Datenschutzerklärung</a> zu.</span>
          </label>
          <button class="btn btn--accent btn--block btn--lg" type="submit">Freien Platz sichern</button>
          <p class="form-status" role="status"></p>
        </form>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band reveal">
        <h2>{{CTATTITLE}}</h2>
        <p class="lead">{{CTATEXT}}</p>
        <div class="btn-row" style="margin-top:1.2rem">
          <a class="btn btn--yellow" href="gutscheine.html">Gutschein verschenken</a>
          <a class="btn btn--ghost" href="kurse.html">Alle Kurse ansehen</a>
        </div>
      </div>
    </div>
  </section>

</main>
"""

FOOT = """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html">
          <img class="brand__mark" src="assets/img/logo.svg" alt="" width="26" height="26">
          <span>Monographix<small>Atelier für Kreativität</small></span>
        </a>
        <p style="max-width:34ch">Action Painting, Glasmalerei und DIY-Workshops bei Ulm. Für Menschen, die glauben, sie seien nicht kreativ.</p>
        <div class="social-row">
          <a href="https://www.instagram.com/_monographix_/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></svg></a>
          <a href="https://www.facebook.com/mona.schoch/" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M15 3h-2.5A4.5 4.5 0 0 0 8 7.5V10H5.5v4H8v7h4v-7h3l.8-4H12V7.5c0-.6.4-1 1-1h2Z"/></svg></a>
          <a href="mailto:hallo@monographix-studio.de" aria-label="E-Mail schreiben"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="m3.5 7 8.5 6 8.5-6"/></svg></a>
        </div>
      </div>
      <div>
        <h3>Kurse</h3>
        <ul>
          <li><a href="action-painting.html">Action Painting</a></li>
          <li><a href="glasmalerei.html">Glasmalerei</a></li>
          <li><a href="basteln-diy.html">Basteln &amp; DIY</a></li>
          <li><a href="fotografie.html">Fotografie</a></li>
          <li><a href="kurse.html">Alle Termine</a></li>
        </ul>
      </div>
      <div>
        <h3>Studio</h3>
        <ul>
          <li><a href="teamevents.html">Teamevents &amp; Feiern</a></li>
          <li><a href="ueber-mich.html">Über mich</a></li>
          <li><a href="gutscheine.html">Gutscheine</a></li>
          <li><a href="kontakt.html">Kontakt &amp; Anfahrt</a></li>
          <li><a href="kontakt.html#faq">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h3>Kontakt</h3>
        <ul>
          <li>Musterstraße 12<br>89150 Laichingen</li>
          <li><a href="tel:+497333000000">+49 7333 000000</a></li>
          <li><a href="mailto:hallo@monographix-studio.de">hallo@monographix-studio.de</a></li>
          <li>Di–Sa 10–20 Uhr</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Monographix · Mona Schoch</span>
      <div class="btn-row" style="gap:1rem">
        <a href="impressum.html">Impressum</a>
        <a href="datenschutz.html">Datenschutz</a>
        <a href="kontakt.html#faq">FAQ</a>
      </div>
    </div>
  </div>
</footer>

<div class="mobile-cta">
  <a class="btn btn--ghost" href="gutscheine.html">Gutschein</a>
  <a class="btn btn--accent" href="#buchen">Kurs buchen</a>
</div>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

DATES = """<article class="card card--flat reveal">
          <div class="card__body">
            <span class="badge {badgeclass}">{badge}</span>
            <h3>{title}</h3>
            <p><strong>{date}</strong><br>{time}</p>
            <div class="card__meta"><span class="tag">{price}</span></div>
            <a class="card__link" href="#buchen">Buchen</a>
          </div>
        </article>"""

FACT = '<li><span class="facts__k">{k}</span><span class="facts__v">{v}</span></li>'

PAGES = [
    dict(
        slug="glasmalerei",
        name="Glasmalerei &amp; Kunsthandwerk",
        title="Glasmalerei &amp; Kunsthandwerk – Workshop bei Ulm | Monographix",
        desc="Glasmalerei lernen in Laichingen: Gläser, Vasen und Dekoobjekte mit Glasfarben und Ätztechnik veredeln. Ab 45 €, Material inklusive.",
        ogtitle="Glasmalerei & Kunsthandwerk – leuchtende Unikate",
        img="assets/img/photos/glas.jpg",
        alt="Verzierte Gläser und Glasobjekte mit farbigen Ornamenten",
        badge="Feine Technik",
        badgeclass="badge--teal",
        topbar="Nächster Termin: <strong>So, 22. November</strong> · 6 Plätze frei",
        lead="Licht durch Farbe: Du gestaltest Gläser, Vasen oder Dekoobjekte mit Glasfarben, Konturen und Ätztechnik – und nimmst am Ende ein Unikat mit nach Hause.",
        intro="""<p>Glas ist ein dankbares Material: Es trägt Farbe anders als Papier, leuchtet von innen und verändert sich mit dem Licht des Tages. Im Kurs lernst du die Grundlagen der Glasmalerei – von der Vorzeichnung über die Konturtechnik bis zum richtigen Brand bzw. der Aushärtung.</p>
          <p>Du arbeitest an einem mitgebrachten oder von uns gestellten Objekt. Beides ist möglich: Viele bringen ein Glas mit Geschichte mit, andere starten mit einer unserer Vasen oder Windlichter.</p>""",
        steps="""<li><strong>Einstieg (20 Min.)</strong> – Materialkunde: Welche Farbe hält auf welchem Glas, wie wird sie haltbar?</li>
            <li><strong>Entwurf (30 Min.)</strong> – Motiv skizzieren, auf das Objekt übertragen, Farbplan festlegen.</li>
            <li><strong>Umsetzung (90 Min.)</strong> – Konturen ziehen, flächig malen, mit Ätzeffekten spielen.</li>
            <li><strong>Finish (40 Min.)</strong> – Trocknen, Aushärten, Verpacken und Fotos im Licht.</li>""",
        audience="""<p>Der Kurs richtet sich an Erwachsene und Jugendliche ab 16 Jahren – auch ohne jede Zeichenerfahrung. Besonders schön als:</p>
          <ul>
            <li>Geschenk für kreative Freundinnen und Freunde</li>
            <li>Mutter-Tochter-Nachmittag</li>
            <li>kleines Team-Event mit Ergebnis fürs Büro</li>
            <li>Vorbereitung auf die eigene Weihnachtsdeko</li>
          </ul>""",
        note="<strong>Hinweis:</strong> Frisch bemaltes Glas braucht 24 Stunden Ruhe. Du kannst dein Werk am nächsten Tag abholen – oder wir verpacken es transportsicher.",
        price="45 €",
        priceunit="inkl. Material",
        includes="""<li>Leihobjekt (Vase oder Windlicht) oder eigenes Glas</li>
              <li>Glasfarben, Konturenpaste, Pinsel</li>
              <li>Schürze &amp; Handschuhe</li>
              <li>Getränke &amp; Kekse</li>
              <li>Verpackung für den Transport</li>""",
        facts=[("Dauer", "3 Stunden"), ("Gruppengröße", "4–10 Personen"),
               ("Niveau", "ohne Vorkenntnisse"), ("Alter", "ab 16 Jahren"),
               ("Sprache", "Deutsch, Englisch"), ("Ort", "Atelier Laichingen")],
        dates=[
            ("badge--teal", "6 Plätze frei", "Sonntagswerkstatt", "So, 22.11.2026", "11:00–14:00 Uhr", "55 €"),
            ("badge", "8 Plätze frei", "Glas &amp; Licht – Abendkurs", "Do, 03.12.2026", "18:00–21:00 Uhr", "45 €"),
            ("badge badge--pink", "3 Plätze frei", "Weihnachtsgläser", "Sa, 12.12.2026", "14:00–17:00 Uhr", "49 €"),
        ],
        options=[("standard", 45, "Standard – 45 € p. P."), ("leihobjekt", 55, "Mit Leihobjekt – 55 € p. P."), ("gruppe", 42, "Gruppe ab 6 – 42 € p. P.")],
        ctattitle="Glas, Licht und ein Abend für dich",
        ctatext="Verschenke einen Glasmalerei-Abend – oder sichere dir selbst einen der wenigen Sonntagstermine.",
    ),
    dict(
        slug="basteln-diy",
        name="Basteln &amp; DIY",
        title="Bastelkurse &amp; DIY-Workshops für Kinder und Erwachsene | Monographix",
        desc="DIY-Workshops bei Ulm: saisonale Deko, Upcycling und Mixed Media für Kinder ab 6 und Erwachsene. Ab 29 €, Material inklusive.",
        ogtitle="Basteln & DIY – aus Alltag wird Lieblingsstück",
        img="assets/img/photos/basteln.jpg",
        alt="Bastelmaterial mit Papier, Naturmaterialien und Farbe",
        badge="Für Groß &amp; Klein",
        badgeclass="",
        topbar="Herbstferien-Special: <strong>Kinderkurs am 28. November</strong>",
        lead="Aus Dingen, die schon da sind, etwas machen, das es noch nicht gibt. Saisonale Deko, Upcycling und Mixed Media – mit Schere, Kleber und viel Fantasie.",
        intro="""<p>Basteln ist die freundlichste Art, kreativ zu sein: niedrige Schwelle, schnelle Ergebnisse, viel Lachen. In unseren DIY-Workshops entsteht Deko für die eigene Wohnung, Geschenke für andere – oder einfach etwas, das gut aussieht.</p>
          <p>Jeder Termin hat ein Thema, aber innerhalb des Themas ist alles erlaubt. Material steht bereit; wer möchte, bringt eigene Fundstücke mit (Gläser, Stoffreste, Treibholz, alte Buchseiten).</p>""",
        steps="""<li><strong>Materialrunde (15 Min.)</strong> – Was liegt da, was passt zusammen, was probieren wir aus?</li>
            <li><strong>Technik (20 Min.)</strong> – Je nach Thema: Wickeln, Kleistern, Schablonieren, Trockenblumen pressen.</li>
            <li><strong>Machen (60–75 Min.)</strong> – Jetzt entsteht dein Stück. Ich helfe bei kniffligen Stellen.</li>
            <li><strong>Finish (15 Min.)</strong> – Trocknen, beschriften, verpacken, Foto machen.</li>""",
        audience="""<p>Zwei Zielgruppen, ein Anspruch: dass es Spaß macht.</p>
          <ul>
            <li><strong>Kinder ab 6 Jahren</strong> – allein oder mit Begleitung, max. 8 Kinder</li>
            <li><strong>Erwachsene</strong> – Feierabend-DIY, Freundinnen-Runde, Adventskranz statt Adventsstress</li>
            <li><strong>Familien</strong> – gemeinsame Samstags-Termine</li>
            <li><strong>Kindergeburtstage</strong> – als Privatevent buchbar, inkl. Mitgebsel</li>
          </ul>""",
        note="<strong>Gut zu wissen:</strong> Kleidung darf schmutzig werden. Für Kinder gibt es Saft und Kekse, für Erwachsene Kaffee – beides inklusive.",
        price="29 €",
        priceunit="inkl. Material",
        includes="""<li>Alle Materialien &amp; Werkzeuge</li>
              <li>Themenpaket (Deko, Upcycling oder Mixed Media)</li>
              <li>Schürze für Kinder</li>
              <li>Getränke &amp; Snack</li>
              <li>Verpackung zum Mitnehmen</li>""",
        facts=[("Dauer", "2 Stunden"), ("Gruppengröße", "4–10 Personen"),
               ("Niveau", "ohne Vorkenntnisse"), ("Alter", "ab 6 Jahren"),
               ("Sprache", "Deutsch"), ("Ort", "Atelier Laichingen")],
        dates=[
            ("badge", "8 Plätze frei", "Winterdeko aus Upcycling", "Sa, 28.11.2026", "14:00–16:00 Uhr", "29 €"),
            ("badge--teal", "5 Plätze frei", "Adventskranz &amp; Trockenblumen", "Sa, 05.12.2026", "10:00–12:00 Uhr", "35 €"),
            ("badge--pink", "2 Plätze frei", "Kinderkurs: Geschenke selber machen", "Sa, 19.12.2026", "10:00–12:00 Uhr", "25 €"),
        ],
        options=[("standard", 29, "Standard – 29 € p. P."), ("kranz", 35, "Adventskranz – 35 € p. P."), ("kind", 25, "Kinderkurs – 25 € p. P.")],
        ctattitle="Ein Nachmittag, der etwas hinterlässt",
        ctatext="DIY-Gutscheine sind das Geschenk für alle, die schon alles haben – nur noch keine selbstgemachte Deko.",
    ),
    dict(
        slug="fotografie",
        name="Neuheiten &amp; Fotografie",
        title="Fotokurs &amp; kreative Portrait-Sessions bei Ulm | Monographix",
        desc="Fotografie-Grundkurs, kreative Portraits und Kombi-Workshops im Atelier bei Ulm. Ab 69 €, mit Handy oder Kamera. Neu 2026.",
        ogtitle="Fotografie & Neuheiten – Kunst im richtigen Licht",
        img="assets/img/photos/fotografie.jpg",
        alt="Kamera im Studio mit farbigem Licht",
        badge="Neu 2026",
        badgeclass="badge--teal",
        topbar="Neu: <strong>Kombi-Workshop</strong> Malen + Fotografieren · 12. Dezember",
        lead="Du hast ein Werk gemacht – jetzt zeigst du es richtig. Oder du lernst, wie Licht, Nähe und Blickwinkel aus einem Foto ein Bild machen.",
        intro="""<p>Fotografie ist Handwerk und Blick zugleich. Im Grundkurs geht es um das, was wirklich zählt: Licht sehen, Bildaufbau verstehen, das Motiv führen – und die Kamera (oder das Handy) so bedienen, dass sie nicht mehr im Weg steht.</p>
          <p>Im <strong>Kombi-Workshop</strong> verbinden wir beides: erst entsteht ein Kunstwerk im Atelier, dann fotografieren wir es so, dass es auch auf Instagram und im Druck gut aussieht.</p>""",
        steps="""<li><strong>Theorie kompakt (45 Min.)</strong> – Blende, Zeit, ISO, Brennweite – ohne Technik-Kauderwelsch.</li>
            <li><strong>Lichtwerkstatt (45 Min.)</strong> – Fensterlicht, Reflektor, harte und weiche Schatten.</li>
            <li><strong>Praxis (90 Min.)</strong> – Portraits, Details, Kunstwerke; ich gebe direkt Feedback.</li>
            <li><strong>Auswahl &amp; Bildsprache (60 Min.)</strong> – Sichten, bearbeiten, präsentieren.</li>""",
        audience="""<p>Für alle, die mehr wollen als Zufallsfotos:</p>
          <ul>
            <li>Einsteiger mit Kamera, die die Automatik verlassen wollen</li>
            <li>Handy-Fotografen, die bewusster gestalten möchten</li>
            <li>Kreative, die ihre Kunstwerke professionell abbilden wollen</li>
            <li>Paare und Freundinnen für eine kreative Portrait-Session</li>
          </ul>""",
        note="<strong>Mitbringen:</strong> eigene Kamera oder Handy, volle Akkus, leere Speicherkarte. Stativ und Dauerlicht sind vorhanden.",
        price="69 €",
        priceunit="inkl. Studio",
        includes="""<li>Studio- und Außengelände-Nutzung</li>
              <li>Dauerlicht, Reflektoren, Hintergründe</li>
              <li>Handout mit allen Grundlagen</li>
              <li>Bildbesprechung deiner 5 besten Fotos</li>
              <li>Getränke &amp; Snack</li>""",
        facts=[("Dauer", "4 Stunden"), ("Gruppengröße", "4–8 Personen"),
               ("Niveau", "Einsteiger"), ("Alter", "ab 16 Jahren"),
               ("Sprache", "Deutsch, Englisch"), ("Ort", "Atelier &amp; Außengelände")],
        dates=[
            ("badge--teal", "6 Plätze frei", "Fotografie-Grundkurs", "Sa, 12.12.2026", "10:00–14:00 Uhr", "69 €"),
            ("badge", "5 Plätze frei", "Kombi: Malen &amp; Fotografieren", "Sa, 09.01.2027", "10:00–15:00 Uhr", "89 €"),
            ("badge--pink", "3 Plätze frei", "Portrait-Session für Paare", "Fr, 16.01.2027", "17:00–20:00 Uhr", "99 € für 2"),
        ],
        options=[("grundkurs", 69, "Grundkurs – 69 € p. P."), ("kombi", 89, "Kombi-Workshop – 89 € p. P."), ("portrait", 50, "Portrait-Session – 99 € für 2")],
        ctattitle="Bilder, die bleiben",
        ctatext="Fotografie-Gutscheine sind das Geschenk für alle, die Erinnerungen lieber mitnehmen als Dinge.",
    ),
]


def build(page):
    html = HEAD
    for key, value in page.items():
        if key in ("facts", "dates", "options"):
            continue
        html = html.replace("{{%s}}" % key.upper(), value)

    html = html.replace("{{FACTS}}", "\n              ".join(FACT.format(k=k, v=v) for k, v in page["facts"]))
    html = html.replace(
        "{{DATES}}",
        "\n        ".join(
            DATES.format(badgeclass=d[0], badge=d[1], title=d[2], date=d[3], time=d[4], price=d[5])
            for d in page["dates"]
        ),
    )
    html = html.replace(
        "{{OPTIONS}}",
        "\n                ".join(
            '<option value="%s" data-price="%s">%s</option>' % (v, p, label)
            for v, p, label in page["options"]
        ),
    )

    html += FOOT
    out = ROOT / (page["slug"] + ".html")
    out.write_text(html, encoding="utf-8")
    print("  " + out.name)


if __name__ == "__main__":
    print("Baue Kurs-Detailseiten:")
    for p in PAGES:
        build(p)
    print("Fertig.")
