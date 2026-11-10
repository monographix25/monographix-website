# Monographix – Website für ein kreatives Kunststudio

**Live:** https://monographix25.github.io/monographix-website/
**Repository:** https://github.com/monographix25/monographix-website
**Spiegel (zweiter Account):** https://danielgloeckler.github.io/monographix-website/

Statische Website (HTML/CSS/JS, kein Build-Schritt, keine Frameworks, keine externen Requests beim Laden).
Ziel: Kursbuchungen, Gutscheinverkäufe und Anfragen für Teamevents.

**Änderungen veröffentlichen**

```powershell
cd kunststudio
git add -A
git commit -m "Was geändert wurde"
git push
```

GitHub Pages baut die Seite danach automatisch neu (ca. 1 Minute).

**Schnellstart**

- **Desktop-Verknüpfung „Monographix Website"**: startet im Hintergrund einen kleinen
  lokalen Webserver und öffnet `http://localhost:8123/` im Browser. Wichtig, damit
  Formularversand und Instagram-Einbindung sauber funktionieren (nicht `file://`).
- `Website starten.vbs` ist der Starter dahinter, `Website starten.bat` zeigt den Server
  mit sichtbarem Fenster (zum Debuggen).

**Manuell**

```powershell
cd kunststudio
..\.venv\Scripts\python.exe -m http.server 8123
# danach http://localhost:8123/
```

---

## 1. Seiten

| Datei | Zweck |
|---|---|
| `index.html` | Startseite: Hero, Vorteile, Kurskacheln, Ablauf, Instagram, Bewertungen, Newsletter |
| `kurse.html` | Kursübersicht mit Filter, Terminliste, Buchungskalender + Preisrechner |
| `action-painting.html` | Detailseite Action Painting |
| `glasmalerei.html` | Detailseite Glasmalerei & Objekte |
| `basteln-diy.html` | Detailseite Basteln & DIY |
| `fotografie.html` | Detailseite Fotografie & Neuheiten |
| `teamevents.html` | B2B: Firmenfeiern, Geburtstage, JGA, Pakete, Anfrageformular |
| `ueber-mich.html` | Mona Schoch, Geschichte, Werte, Atelier |
| `gutscheine.html` | Gutscheinwerte, Schnellwahl, Bestellformular |
| `kontakt.html` | Kontaktformular, Anfahrt, Karte (mit Einwilligung), FAQ |
| `danke.html` | Bestätigungsseite nach Formularversand |
| `impressum.html` / `datenschutz.html` | Rechtstexte (Platzhalter, siehe Punkt 5) |

## 2. Bildmaterial

Die Fotos liegen optimiert in **`assets/img/photos/`** (JPG, max. 1600 px breit):

| Datei | Motiv | Einsatz |
|---|---|---|
| `hero.jpg` | Staffelei mit abstraktem Bild | Hero Startseite |
| `action.jpg` | Farbe läuft auf die Leinwand | Action Painting (Karte + Detailseite) |
| `glas.jpg` | Rote Farbe auf vergoldetem Objekt | Glasmalerei & Objekte |
| `basteln.jpg` | Grüne Farbe wird gegossen | Basteln & DIY |
| `fotografie.jpg` | Pinke Leinwand im Sonnenlicht | Fotografie & Neuheiten |
| `portrait.jpg` | Arbeiten an einer bunten Leinwand | Über mich, Galerie |
| `team.jpg` | Detailaufnahme Farbauftrag | Teamevents |
| `studio.jpg` | Atelierstimmung | Über mich (Atelier) |

**Neue Fotos einsetzen:** Originale in `_fotos/` legen (Namen egal), dann

```powershell
..\.venv\Scripts\python.exe tools\import_photos.py
```

Das Skript skaliert auf 1600 px, komprimiert auf JPG und schreibt die Dateien
automatisch unter den oben genannten Namen. Zuordnung siehe `_fotos/LIESMICH.txt`.

**Tipp:** Für noch schärfere Darstellung auf Retina-Displays die Originale in
voller Auflösung aufbewahren und später zusätzlich `@2x`-Varianten mit
`srcset` einbinden.

## 3. Instagram-Feed (DSGVO)

- Startseite zeigt zuerst eine **lokale Galerie** (kein Tracking, sofort sichtbar).
- Der echte Live-Feed wird erst nach Klick auf „Instagram-Feed laden" als iframe geladen
  (`https://www.instagram.com/<profil>/embed`). Einwilligung liegt im `localStorage`.
- Profil zentral ändern: in `index.html` und im Footer (`https://www.instagram.com/monographix_fotografie/`).
- Für mehr Layout-Kontrolle: Elfsight, SnapWidget oder LightWidget einbinden – jeweils
  hinter dieselbe Zwei-Klick-Lösung legen.

## 4. Formulare

Die Formulare senden **automatisch** – der Besucher muss nichts anklicken und kein
Mailprogramm haben. Der Versand läuft über **FormSubmit** (kostenlos, ohne Konto):

```
data-endpoint="https://formsubmit.co/ajax/monographix25@gmail.com"
```

**Einmalige Freischaltung:** Beim ersten Absenden schickt FormSubmit eine E-Mail an
`monographix25@gmail.com` mit dem Button **„Activate Form"**. Nach einem Klick ist der
Versand dauerhaft aktiv. Bis dahin zeigt das Formular einen Hinweis samt E-Mail-Fallback.

Jede Anfrage kommt als Tabelle im Postfach an, Betreff je Formular (z. B. „Kursbuchung
Action Painting"), Antwort an die Adresse des Absenders ist direkt möglich.

**Alternative Dienste** (falls FormSubmit nicht passt): Formspree, Web3Forms, Netlify Forms –
einfach `data-endpoint` austauschen. Ohne Dienst greift automatisch der Mail-Fallback
(`mailto:`), der das E-Mail-Programm öffnet.

**Echtes Buchungssystem** (Kalender + Anzahlung) statt Anfrage:
- `bookingkit`, `Regiondo`, `Bookeo` → Widget-iframe an Stelle des `#buchen`-Blocks.
- `Calendly` / `Cal.com` → iframe statt `.calendar`.

Der mitgelieferte Kalender ist eine **Verfügbarkeits-Demo** (deterministisch aus dem Datum
berechnet, siehe `isFree()` in `assets/js/main.js`). Für echte Termine dort die Belegung
aus dem Buchungssystem einspeisen.

**Uhrzeiten:** Nach der Datumswahl füllt sich das Feld „Uhrzeit" automatisch –
Mo–Do von 16 bis 19 Uhr, Fr/Sa/So ganztägig von 10 bis 19 Uhr (`timeSlots()` in
`assets/js/main.js`). Andere Zeiten: dort die Stundenschleife anpassen.

## 5. Vor dem Livegang anpassen

- [x] Kontaktdaten: Mona Schoch, Weiherweg 26, 89180 Berghülen, monographix25@gmail.com, 0152 22970802
- [ ] Preise, Termine, Gruppengrößen
- [ ] Kundenstimmen: die drei Zitate sind **Beispieltexte** – durch echte ersetzen (mit Einwilligung)
- [ ] Zahlen auf der Startseite (1.400 Teilnehmer, 4,9/5) prüfen
- [ ] `impressum.html`: USt-ID / Kleinunternehmer-Hinweis ergänzen
- [ ] `datenschutz.html`: Hosting-Anbieter, Formulardienst (falls genutzt) ergänzen
- [ ] Domain: `canonical`- und `og:`-URLs sowie `sitemap.xml` / `robots.txt` anpassen
- [ ] Fotorechte der abgebildeten Personen klären (§ 22 KUG)

## 6. Technik

- **Hosting:** GitHub Pages, Branch `main`, Ordner `/` (Einstellungen → Pages).
  Die Seite ist rein statisch, `.nojekyll` verhindert Jekyll-Verarbeitung.
- **Eigene Domain später:** bei GitHub Pages unter *Custom domain* eintragen, dann
  `canonical`/`og:url` in den HTML-Dateien und `sitemap.xml`/`robots.txt` anpassen.
- **Keine externen Ressourcen** beim Laden: Inter liegt als WOFF2 in `assets/fonts/`,
  alles andere lokal → keine Google-Fonts-Problematik, schnelle Ladezeit.
- **Responsive** ab 320 px getestet; Sticky-CTA unter 720 px.
- **Barrierefreiheit**: Lighthouse Accessibility 100/100, Skip-Link, sichtbare Fokus-Stile,
  `aria-*` an Navigation/Kalender, `prefers-reduced-motion`, Inhalte auch ohne JavaScript sichtbar.
- **SEO**: Meta-Tags, Open Graph, JSON-LD (`ArtStudio`, `Course`, `Service`), semantische Überschriften.
- **Performance**: Hero mit `fetchpriority="high"`, restliche Bilder `loading="lazy"`.

### Struktur

```
kunststudio/
├─ *.html                    Seiten
├─ assets/
│  ├─ css/style.css          Designsystem
│  ├─ js/main.js             Navigation, Slider, Kalender, Consent, Formulare
│  ├─ fonts/                 Inter (WOFF2, lokal)
│  └─ img/
│     ├─ photos/             Fotos (hero, action, glas, basteln, fotografie, portrait, team, studio)
│     ├─ logo.svg            Wortmarke
│     └─ favicon.svg
├─ _fotos/                   Original-Fotos + LIESMICH
├─ Website starten.bat       lokaler Server + Browser
└─ tools/
   ├─ import_photos.py       Fotos optimieren und benennen
   ├─ build_detail_pages.py  Kurs-Detailseiten aus einer Vorlage bauen
   ├─ create_desktop_shortcut.py  Desktop-Verknüpfung anlegen
   └─ check_site.py          Links, Anker, Tag-Struktur prüfen
```

### Deployment

Reiner Static-Host genügt: Netlify, Vercel, Cloudflare Pages, IONOS, All-Inkl.
Einfach den Ordner `kunststudio/` hochladen – kein Build nötig.

---

## 7. Design

- **Haltung:** reduziert, editorial, hell. Die Fotos liefern die Farbe, die Oberfläche bleibt ruhig.
- **Farben:** Weiß `#FFFFFF`, Warmgrau `#F6F5F2`, Tinte `#151312`, Textgrau `#5C5854`, Linien `#E5E2DC`.
- **Typografie:** Inter (400–600), große Überschriften mit engem Tracking (`-0.032em`).
- **Form:** 1-px-Linien statt Schatten, 4–12 px Radien, keine Muster, keine Verläufe, keine Rotation.
- **Tonalität:** „Jeder kann kreativ sein" – du-Ansprache, kurze Sätze, konkrete Bilder.
