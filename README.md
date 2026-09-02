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
| `assets/img/fotos/`               | Hier kommen die echten Fotos rein |
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
- **Bewertungen.** Der Abschnitt „Was unsere Gäste sagen" ist gebaut,
  erscheint aber erst, wenn in `build.py` im Block `BEWERTUNG` echte Werte
  stehen. Siehe eigenes Kapitel weiter unten.


---

## Wenn die Seite falsch aussieht

Das häufigste Problem beim Hochladen: **Der Browser zeigt eine alte
`calimero.css` aus dem Cache.** Dann läuft neues HTML mit altem Stylesheet,
und die Seite sieht kaputt aus. Typische Symptome: heller statt dunkler
Hintergrund, unterstrichene Schrift im Kopf, Text ohne Größen.

Dagegen hängt jetzt an jeder CSS- und JS-Datei ein Fingerabdruck aus dem
Dateiinhalt, zum Beispiel `calimero.css?v=d598e18fec`. Ändert sich die
Datei, ändert sich der Wert, und jeder Browser lädt zwingend neu.

So prüfst du, welcher Stand läuft:

1. Auf der Seite Rechtsklick → Seitenquelltext anzeigen. In Zeile 2 steht
   `<!-- Pizzeria Calimero, Design dunkel. Build JJJJ-MM-TT HH:MM ... -->`
2. Oder Entwicklerkonsole öffnen, dort wird der Build ausgegeben.

Passt der Zeitstempel nicht zu deinem letzten Upload, fehlen Dateien auf
dem Server. Dann `assets/` komplett neu hochladen, nicht nur die HTML.

Zum harten Neuladen im Browser: Mac `Cmd + Shift + R`, Windows
`Strg + F5`.

---

## Design

**Stil A "Avorio".** Elfenbein als Grundton, tiefes Flaschengrün für Marke,
Überschriften und Bänder, Messinggold für Ziffern und Zierlinien, Rot nur
als Signalfarbe für die Hauptaktion. Ecken sind fast eckig (2 px), keine
Bubble-Optik. Über der Fläche liegt ein sehr feines Papierkorn, damit die
hellen Flächen nicht steril wirken.

Der Kopf trägt eine typografische Wortmarke plus das Calimero-Küken als
Zeichen. Das Originallogo hat rote Schrift und ist bei Kopfzeilengröße
nicht lesbar, es bleibt für PDF, Druck und das Vorschaubild beim Teilen.

Farben und Abstände stehen als CSS-Variablen ganz oben in
`assets/css/calimero.css`. Wer die Stimmung ändern will, ändert dort
`--gruen`, `--gold`, `--rot` und `--grund`, sonst nichts.

Zum Vergleichen liegt `stilproben.html` bei, dort stehen die drei
Richtungen A, B und C nebeneinander. Die Datei gehört nicht auf den
Server, sie ist nur für die Abstimmung mit dem Kunden.

### Schriften: bewusst nur Systemschriften

Die Seite verwendet **keine Google Fonts, keine CDN-Schriften und keine
lizenzpflichtige Schrift.** Gesetzt wird ausschließlich mit dem, was auf
dem Gerät des Besuchers ohnehin vorhanden ist: eine Serifenschrift für
Überschriften (Palatino, ersatzweise Georgia) und die Systemschrift des
Betriebssystems für den Fließtext.

Beim Aufruf der Seite geht damit **keine einzige Anfrage an einen fremden
Server**. Das ist der Grund, warum hier keine Schrift nachgerüstet werden
sollte. Google Fonts von deren Servern einzubinden ist der bekannteste
Abmahngrund bei kleinen Websites.

Externe Adressen kommen im Code nur an vier Stellen vor, und keine davon
lädt beim Seitenaufruf etwas: Google Maps (erst nach Klick), `wa.me`
(erst nach Klick), sowie reine Textlinks zu den Datenschutzangaben von
Google und WhatsApp in der Datenschutzerklärung.

---

## Fotos einbauen

Die Seite funktioniert ohne Bilder und enthält bewusst kein einziges
Stockfoto. Abschnitte, für die kein Foto hinterlegt ist, werden gar nicht
erst ausgegeben. Dadurch sieht nichts unfertig aus, die Seite wird nur
besser, sobald Bilder da sind.

1. Foto nach `assets/img/fotos/` legen, etwa `laden.jpg`
2. In `build.py` im Block `FOTOS` den Wert von `None` auf `"laden.jpg"` setzen
3. `python3 build.py`

Vorgesehen sind: `laden` (Außenansicht oder Gastraum), `ofen`,
`pizza63`, `pasta`, `salat`, `team`. Sobald mindestens eines der
Gerichtefotos gesetzt ist, erscheint auf der Startseite der Abschnitt
„Aus unserer Küche“.

Empfohlen: 1600 px breite Seite, JPG mit etwa 75 % Qualität. Handyfotos
bei Tageslicht reichen völlig. Danach Bildnachweis im Impressum ergänzen,
KI-Bilder immer kennzeichnen.

---

## WhatsApp Business einrichten

Das gehört nicht in den Code, sondern in die App auf dem Handy des Wirts.
Ohne diese zwei Einstellungen bekommt der Kunde nach dem Absenden keine
Rückmeldung und wird unsicher.

### 1. Automatische Eingangsbestätigung

Dafür ist die **Abwesenheitsnachricht** zuständig, nicht die
Begrüßungsnachricht. Die Begrüßungsnachricht geht nur an neue Kontakte
oder nach 14 Tagen Pause und würde bei Stammkunden fast nie auslösen.

WhatsApp Business → Einstellungen → Unternehmenstools →
Abwesenheitsnachricht → Zeitplan auf **„Immer senden“**.

Text:

> Vielen Dank für Ihre Nachricht an Pizzeria Calimero. Wir haben sie
> erhalten und melden uns gleich mit der voraussichtlichen Zeit.
> Telefonisch erreichen Sie uns unter 06181 95 2 95 95.

Bewusst neutral formuliert, weil die Nachricht auf **jede** eingehende
Nachricht antwortet, nicht nur auf Bestellungen.

### 2. Schnellantworten für die Zeitangabe

Einstellungen → Unternehmenstools → Schnellantworten. Kürzel anlegen, der
Wirt tippt dann nur noch `/30` und die fertige Nachricht steht da.

| Kürzel | Text |
|--------|------|
| `/30`  | Ihre Bestellung ist in etwa 30 Minuten fertig. |
| `/45`  | Ihre Bestellung ist in etwa 45 Minuten fertig. |
| `/60`  | Ihre Bestellung ist in etwa 1 Stunde fertig. |
| `/75`  | Ihre Bestellung ist in etwa 1 Stunde und 15 Minuten fertig. |
| `/abholung` | Ihre Bestellung ist abholbereit. Heumarkt 6, wir freuen uns auf Sie. |
| `/nein` | Leider ist eine Position aus Ihrer Bestellung heute nicht verfügbar. Wir rufen Sie kurz an. |

Falls die Automatik nicht anspringt: prüfen, ob Meta Business Agent
verknüpft ist. Der deaktiviert die automatischen Nachrichten.

---

## Google-Bewertungen

Der Abschnitt zeigt **nur die Gesamtbewertung** mit Quelle, Datum und Link
auf das echte Profil. Es werden **keine Bewertungstexte kopiert**. Das ist
Absicht, nicht Faulheit:

- Der Text einer Rezension gehört dem Verfasser. Werbung auf der eigenen
  Website ist kein Zitatzweck nach § 51 UrhG, das Zitatrecht greift hier
  also nicht.
- Der Name des Verfassers ist ein personenbezogenes Datum.
- Googles Nutzungsbedingungen beschränken die Weiterverwendung.
- Ausgewählte Positivzitate ohne die kritischen Stimmen sind zusätzlich
  angreifbar, weil sie ein geschöntes Bild erzeugen.

Der Vertrauenseffekt bleibt trotzdem: Note, Anzahl und ein Klick zum
Original.

### Einrichten

In `build.py` im Block `BEWERTUNG`:

```python
BEWERTUNG = {
    "schnitt": 4.6,                    # Punkt, nicht Komma
    "anzahl":  412,
    "stand":   "September 2026",
    "profil":  "https://...",          # Link auf das Google-Profil
    "bewerten": "https://...",         # optional, Bewertung schreiben
}
```

Solange `schnitt` oder `anzahl` auf `None` steht, wird der Abschnitt gar
nicht ausgegeben.

**Die Zahlen müssen aus dem Google-Unternehmensprofil des Wirts kommen.**
Nicht von Portalen wie Restaurant Guru, speisekarte.de oder Cylex. Bei der
Recherche kamen dort 233 Bewertungen bei 4,0 Sternen, 235 bei 4,8 und 1078
bei 4,5 heraus, alles zum selben Betrieb. Falsche Bewertungsangaben sind
irreführende Werbung und abmahnbar.

`stand` bitte setzen und halbjährlich aktualisieren. Eine Note von vor drei
Jahren als aktuell darzustellen wäre derselbe Fehler.

### Kein AggregateRating im Markup

Der Abschnitt enthält bewusst **keine strukturierten Daten** für die
Bewertung. Google erlaubt keine selbst eingetragenen Bewertungen im
Markup des eigenen Betriebs. Die Sterne im Suchergebnis zieht Google
ohnehin direkt aus dem Unternehmensprofil.

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

### Gerichtefotos

Kommen automatisch an drei Stellen an: Speisekarte, Bestellliste und
Konfigurator.

1. Datei nach `assets/img/gerichte/` legen
2. In `menu_data.py` im Block `BILDER` der Nummer zuordnen:
   `BILDER = { "063": "pizza-calimero.jpg" }`
3. `python3 build.py`

Gerichte ohne Eintrag laufen ohne Bild weiter. In der Speisekarte wird die
Bildspalte automatisch für die ganze Kategorie reserviert, sobald ein
Gericht darin ein Foto hat, damit die Zeilen bündig bleiben.

Empfohlen: quadratisch, 800 × 800 px, JPG mit etwa 75 % Qualität. Von
schräg oben, bei Tageslicht, immer gleicher Abstand und gleicher
Untergrund. Das wirkt hochwertiger als jeder Filter.

### Schutz vor Fake- und Doppelbestellungen

Bewusst **ohne Tageslimit und ohne Feiertagsliste**, damit nichts gepflegt
werden muss und an starken Tagen (Silvester, Halloween, Fußballabende)
niemand ausgesperrt wird. Stattdessen drei Prüfungen, die keine Wartung
brauchen und echte Kunden nie treffen:

1. **90 Sekunden Pause** zwischen zwei Bestellungen, gegen Doppelklicks
2. **Mindestverweildauer** von 8 Sekunden zwischen Seitenaufruf und
   Absenden. Menschen brauchen länger, Skripte nicht.
3. **Honigtopf-Feld**, für Menschen unsichtbar. Automaten füllen es aus
   und werden dadurch erkannt.

Beides einstellbar in `menu_data.py`:

```python
BESTELL_PAUSE = 90       # Sekunden zwischen zwei Bestellungen
MINDESTVERWEILDAUER = 8  # Sekunden bis zum Absenden
```

Ehrlich zur Wirkung: Das läuft im Browser des Kunden. Wer es umgehen will,
nimmt ein Inkognito-Fenster. Die eigentliche Absicherung gegen
Fake-Bestellungen ist eine andere und war von Anfang an da: Jede Bestellung
kommt über eine **echte Telefonnummer im WhatsApp-Chat**, und es wird
nichts zubereitet, bevor der Wirt bestätigt hat. Bei einer verdächtigen
Bestellung ruft er einfach kurz an, bevor der Ofen angeht.

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

### Cookie-Banner und Rechtstexte

Es gibt einen Hinweiskasten beim ersten Besuch, aber **bewusst keinen
Zustimmungsdialog**. Grund: Die Seite setzt keine Cookies, lädt keine
Tracker und bindet beim Aufruf nichts von Dritten ein. Ein
Zustimmungsdialog mit „Alle akzeptieren“ wäre inhaltlich falsch, weil es
nichts zuzustimmen gibt, und irreführende Banner sind selbst angreifbar.

Was gespeichert wird (Warenkorb, Kartenentscheidung) fällt unter
§ 25 Abs. 2 TDDDG, weil es für die vom Nutzer ausdrücklich gewünschte
Funktion unbedingt erforderlich ist. Das einzige einwilligungspflichtige
Element ist Google Maps, und das ist als Zwei-Klick-Lösung gebaut: Die
Karte lädt erst nach aktivem Klick, mit Hinweis direkt daneben und
Widerruf in der Datenschutzerklärung.

Der Hinweiskasten ist also ehrlich formuliert und einmal wegklickbar. Er
gibt dem Kunden das gewohnte Gefühl, ohne eine Zustimmung vorzutäuschen.

Rechtstexte an Bord: **Impressum**, **Datenschutzerklärung** und
**AGB** (`bestellbedingungen.html`, in der Navigation als AGB
bezeichnet). Ein separates AGB-Dokument daneben braucht es nicht, die
Bestellbedingungen *sind* die AGB für den Fernabsatz.
