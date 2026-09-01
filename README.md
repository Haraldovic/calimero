# Pizzeria Calimero, Hanau

Statische Website. Kein CMS, kein Baukasten, kein Framework, keine externen
Skripte, keine Tracker, keine Cookies. Läuft unverändert auf GitHub Pages
(Vorschau) und auf Hostinger (live unter calimero-hanau.de).

---

## Aufbau

| Datei / Ordner                    | Zweck |
|-----------------------------------|-------|
| `menu_data.py`                    | Alle 75 Gerichte, Getränke, Preise, Extras, Zusatzstoffe, Allergene |
| `build.py`                        | Texte, Adresse, Öffnungszeiten, Seitenaufbau. Erzeugt alle HTML-Dateien |
| `assets/css/calimero.css`         | Komplettes Styling |
| `assets/js/calimero.js`           | Öffnungsstatus, Kartensuche, WhatsApp-Nummer, Zwei-Klick-Karte |
| `assets/js/bestellen.js`          | Konfigurator, Warenkorb, Kasse, WhatsApp-Übergabe |
| `menu.json`                       | Erzeugt aus `menu_data.py`, Datenquelle der Bestellseite |
| `assets/img/`                     | Logo, Küken, Favicon, OG-Bild |
| `speisekarte-calimero-2026.pdf`   | Gedruckte Karte zum Download |
| `.htaccess`                       | Nur für Hostinger: HTTPS, alte URLs, Caching, Header |
| `.nojekyll`, `CNAME`              | Nur für GitHub Pages |
| `*.html`, `robots.txt`, `sitemap.xml` | Erzeugt, nicht von Hand bearbeiten |

**HTML wird nie direkt bearbeitet.** Immer `menu_data.py` oder `build.py`
ändern und neu bauen.

---

## Bauen

```bash
python3 build.py             # LIVE   -> calimero-hanau.de, indexierbar
python3 build.py --vorschau  # VORSCHAU -> noindex + robots.txt Disallow
```

Es wird nur die Standardbibliothek gebraucht, keine Pakete, kein Node.

**Lokal testen nur über einen Webserver.** Die Bestellseite lädt `menu.json`
per `fetch`, das funktioniert nicht per Doppelklick über `file://`. Also:

```bash
python3 -m http.server 8000
# dann http://localhost:8000 im Browser öffnen
```

Der Vorschau-Modus setzt jede Seite auf `noindex, nofollow` und schreibt eine
sperrende `robots.txt`. Damit taucht die GitHub-Vorschau nicht neben der
echten Domain im Google-Index auf.

Die beiden Domains stehen oben in `build.py`:

```python
LIVE_DOMAIN     = "https://calimero-hanau.de"
VORSCHAU_DOMAIN = "https://calimero.rateriser.tech"
```

---

## GitHub Pages (Vorschau für den Kunden)

1. Repo anlegen, alles pushen.
2. Settings → Pages → Source auf **GitHub Actions** stellen.
   Nicht „Deploy from a branch“, sonst wird die eingecheckte Live-Version
   mit der echten Canonical-URL veröffentlicht und ist indexierbar.
3. Der Workflow `.github/workflows/pages.yml` baut bei jedem Push auf `main`
   automatisch mit `--vorschau` und veröffentlicht.
4. DNS bei rateriser.tech: `CNAME calimero -> <benutzername>.github.io`
   Der Subdomainname steht in der Datei `CNAME`, dort bei Bedarf ändern.
5. Settings → Pages → „Enforce HTTPS“ aktivieren, sobald das Zertifikat da ist.

Ändert sich ein Preis, reicht: `menu_data.py` bearbeiten, committen, pushen.
Die Vorschau baut sich selbst neu.

---

## Hostinger (live)

1. Lokal bauen: `python3 build.py` (**ohne** `--vorschau`).
2. Per hPanel-Dateimanager oder FTP in **`public_html`** hochladen:

   ```
   index.html  speisekarte.html  bestellen.html  ueber-uns.html
   kontakt.html  impressum.html  datenschutz.html
   bestellbedingungen.html  404.html
   menu.json  robots.txt  sitemap.xml  favicon.ico  .htaccess
   assets/
   speisekarte-calimero-2026.pdf
   ```

   Nicht hochladen: `build.py`, `menu_data.py`, `README.md`, `.github/`,
   `.nojekyll`, `CNAME`, `.gitignore`. Falls doch, blockt die `.htaccess`
   den Zugriff darauf, sauberer ist es aber ohne.

3. **Die alte Baukasten-Seite abschalten**, sonst liegen zwei Versionen unter
   derselben Domain. Im hPanel unter Website → Website-Baukasten.
4. SSL prüfen, dann in der Search Console `sitemap.xml` einreichen.

Wichtig: Bei Hostinger muss der Dateimanager **versteckte Dateien anzeigen**,
sonst geht die `.htaccess` beim Upload verloren.

### Was die `.htaccess` erledigt

- HTTPS erzwingen, `www` auf die Hauptdomain umleiten
- 301-Weiterleitungen der alten Baukasten-URLs, damit die Google-Rankings
  nicht verloren gehen:
  `/speisekarte`, `/uber-uns`, `/impressum`, `/datenschutzerklarung`,
  sowie das alte `speisekarte_2025*.pdf`
- eigene 404-Seite, Komprimierung, Browser-Cache, Sicherheits-Header

---

## Offene Punkte

### Blocker, ohne die nicht live gegangen wird

1. **Getränkepreise.** In `menu_data.py` stehen vier 1-Liter-Flaschen
   (Coca-Cola, Fanta, Sprite, Mineralwasser) mit **Platzhalterpreisen**.
   Echte Preise eintragen, dann `GETRAENKE_PLATZHALTER = False` setzen.
   Danach verschwindet der rote Warnkasten auf der Bestellseite von selbst.
   `build.py` warnt bei jedem Lauf, solange das offen ist.

2. **WhatsApp-Nummer.** Steht in `assets/js/calimero.js` aktuell auf
   `491728664287`. Das ist die Prototyp-Nummer für die Demo. Vor dem Livegang
   durch die WhatsApp-Business-Nummer der Pizzeria ersetzen.

3. **Aufpreis für Extras bei Pasta und Salat.** Auf der gedruckten Karte
   stehen nur die Pizza-Aufpreise (0,50 € bei ø 26 cm, 1,00 € bei ø 30 cm).
   Für Pasta und Salat sind pauschal **1,00 € gesetzt, das ist eine Annahme
   von uns**, siehe `EXTRA_PREIS` in `menu_data.py`. Vom Wirt bestätigen
   lassen. Die dokumentierten Aufpreise (Käse überbacken 1,00 €,
   Extra-Dressing 1,00 €) stehen davon unberührt in `ZUSATZOPTIONEN`.

4. **Impressum** in `build.py`, Funktion `seite_impressum()`. Alle gelb
   markierten Stellen (`<mark class="todo">`) ersetzen: Firma inkl.
   Rechtsform, Inhaber, E-Mail, ggf. Registereintrag, USt-IdNr. oder
   Steuernummer, Aufsichtsbehörde (steht auf dem Gaststättenerlaubnis-
   Bescheid), Verantwortlicher nach § 18 Abs. 2 MStV.

5. **Datenschutzerklärung** und **Bestellbedingungen** in `build.py`:
   Firma, E-Mail, Hoster bestätigen, Datum des Livegangs.

### Erledigt

- Liefergebiete vom Wirt bestätigt (Innenstadt, Wolfgang, Steinheim,
  Kesselstadt, Lamboy, Rosenau, Dunlop-Gewerbegebiet)
- Mindestbestellwert 11,00 €, wie auf der Karte 2026
- Getränke: nur 1-Liter-Flaschen, keine kleinen Flaschen

### Noch offen, aber kein Blocker

- **Gründungsjahr.** Aktuell steht überall „seit über 20 Jahren“. Die alte
  Website behauptete 24 Jahre, das wären 2026 schon 25.
- **Über uns:** der gelbe Kasten ist ein Platzhalter für die eigene
  Geschichte des Wirts. Text holen, einsetzen, Kasten löschen.
- **Fotos.** Die Seite ist bewusst so gebaut, dass sie ohne Bilder
  funktioniert. Es steckt kein einziges Stockfoto drin. Sinnvoll wären
  Außenansicht, drei bis vier Gerichte (Nr. 63, ein Pastateller, ein Salat),
  Ofen und Team. Handyfotos bei Tageslicht reichen. Danach Bildnachweis im
  Impressum ergänzen, KI-Bilder immer kennzeichnen.
- **Bewertungen.** Die erfundenen Zitate mit Stockfoto-Avataren der alten
  Seite sind raus und kommen nur zurück, wenn es echte Google-Rezensionen
  mit dem dort genannten Namen sind.

---

## Bestellfunktion

Kein Server, kein Konto, keine Onlinezahlung, kein Lieferdienst dazwischen.

**Ablauf:** Kategorie wählen oder nach Nummer suchen → Artikel antippen →
Größe, Extra-Zutaten, Weglass-Wünsche, Sonderwunsch, Menge → Warenkorb →
Kasse → fertige Nachricht in WhatsApp, absenden muss der Kunde selbst.

**Warenkorb** liegt im `localStorage`, bleibt also beim Neuladen erhalten
und wird nach dem Absenden geleert.

**Fallback ohne WhatsApp:** auf der Abschlussseite gibt es zusätzlich
„Bestellung kopieren“ (Zwischenablage, mit Fallback für alte Browser) und
„Lieber anrufen“. Ohne diese beiden würde jeder Desktop-Besucher hängen
bleiben.

**Bestellnummer:** vierstellig, wird im Browser des Kunden erzeugt. Sie
dient nur der Zuordnung bei Abholung und Übergabe, sie ist kein
Sicherheitsmerkmal.

### Rechtliches an der Bestellfunktion

- Der Button heißt **„zahlungspflichtig bestellen“** (§ 312j Abs. 3 BGB).
- Direkt darüber stehen Positionen, Gesamtpreis inklusive Mehrwertsteuer,
  Liefergebühr und der Hinweis auf Allergene. Die Fußleiste ist auf der
  Kasse bewusst **nicht** klebend, damit niemand am Gesamtpreis vorbei
  bestellen kann.
- Eigene Seite `bestellbedingungen.html` mit dem entscheidenden Satz: der
  Vertrag kommt erst mit der Bestätigung durch die Pizzeria zustande, nicht
  mit dem Absenden. Ohne diesen Satz schuldet der Wirt jede Bestellung, die
  er nie gesehen hat.
- Widerrufsrecht ist bei Speisen zum sofortigen Verzehr ausgeschlossen
  (§ 312g Abs. 2 BGB). Das steht ausdrücklich drin statt es wegzulassen.
- Sonderwünsche mit möglichem Aufpreis sind im Gesamtpreis nicht enthalten,
  darauf wird an drei Stellen hingewiesen.
- Das Mittagsangebot wird online **nicht** automatisch verrechnet, sonst
  streitet der Wirt an der Tür über Preise, die die Website ausgerechnet hat.

### Was bewusst nicht gebaut wurde

Onlinezahlung, Kundenkonten, Bestellverfolgung, automatische Bestätigung,
Bonprinter-Anbindung. Jedes davon braucht einen Server und bringt damit
Betriebskosten, Wartung und Haftung mit sich.

### Damit es benutzt wird

- QR-Code auf Pizzakarton, Flyer und Tresen, direkt auf `bestellen.html`.
- Der Wirt muss zeitnah auf die WhatsApp-Nachrichten antworten. In WhatsApp
  Business dafür Abwesenheitsnachricht und Schnellantworten einrichten.
  Wenn Bestellungen 30 Minuten liegen bleiben, ist die Funktion nach drei
  Wochen tot.

---

## Enthaltene Funktionen

- 9 Seiten: Start, Speisekarte, Bestellen, Über uns, Kontakt, Impressum,
  Datenschutz, Bestellbedingungen, 404
- Komplette Karte 2026 als echtes HTML, 75 Gerichte mit Preisen,
  Zusatzstoffen und Allergenen, plus Suche nach Nummer oder Name
- PDF-Download der gedruckten Karte
- Anruf-Button im Kopf, in der Bühne, auf Kontakt und als feste Leiste am
  unteren Rand auf dem Handy
- WhatsApp-Buttons mit vorbereitetem Bestelltext
- Live-Status „Jetzt geöffnet bis 14:30 Uhr“, gerechnet in Europe/Berlin,
  markiert zusätzlich den heutigen Tag in den Öffnungszeiten
- Mittagsangebot 7,50 € prominent auf der Startseite
- Restaurant- und Menu-Schema für Google
- Google Maps als Zwei-Klick-Lösung, Einwilligung liegt lokal im Browser
  (`localStorage`), Widerruf-Button in der Datenschutzerklärung
- Bestellfunktion mit Konfigurator, Warenkorb und WhatsApp-Übergabe
- `robots.txt`, `sitemap.xml`, Favicon aus dem Calimero-Küken

### Warum kein Cookie-Banner

Die Seite setzt keine Cookies und lädt beim Aufruf nichts von Dritten. Das
einzige einwilligungspflichtige Element ist die Google-Maps-Karte, und die
lädt erst nach aktivem Klick, mit Hinweis direkt daneben. Ein Banner beim
Seitenaufruf hätte hier keinen Gegenstand. Falls der Kunde trotzdem eins
will: das CSS liegt unter `.consent` bereit, das Markup ist in der
Git-Historie.
