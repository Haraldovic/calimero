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

### Der eine echte Blocker

**Es fehlt eine E-Mail-Adresse für das Impressum.** § 5 Abs. 1 Nr. 2 DDG
verlangt eine Angabe, die eine schnelle elektronische Kontaktaufnahme
ermöglicht, und dazu gehört ausdrücklich die E-Mail-Adresse. Eine
Telefonnummer allein reicht nicht.

**Das ist auch am alten Impressum schon falsch, es steht seit Jahren so
online.** Das ist der häufigste Abmahngrund überhaupt.

Sobald die Adresse da ist, in `build.py` oben eintragen:

```python
EMAIL = "info@calimero-hanau.de"
```

Danach `python3 build.py`. Damit verschwinden die letzten drei gelben
Markierungen in Impressum, Datenschutz und AGB, und die Seite ist
vollständig.

### Getränke: erledigt, drei Punkte noch zu bestätigen

Die Preise stammen vom Wirt (September 2026) und sind eingetragen:

| Nr. | Getränk | Preis |
|-----|---------|-------|
| G01–G04 | Sinalco Cola, Cola Zero, Orange, Mix | 4,00 € (1,0 l) / 3,00 € (0,33 l Glas) |
| G05 | Uludağ Gazoz, 0,5 l | 2,50 € |
| G06 | Körfez Ayran, 0,25 l | 2,00 € |
| G07/G08 | Rhönsprudel mit / ohne Kohlensäure, 0,5 l | 2,50 € |

Sorten und Pfand sind vom Wirt bestätigt: „Mix" ist Cola Mix, das Pfand ist
in den Preisen enthalten. Beides steht so auf der Speisekarte und in den AGB.

Ein Punkt bleibt: **Zusatzstoffe.** Bei Cola, Cola Zero und Cola Mix ist
Farbstoff (1) hinterlegt, bei Cola Zero zusätzlich Süßstoff (8). Das
entspricht dem Üblichen, gehört aber einmal gegen das Flaschenetikett
geprüft. Bei den übrigen Getränken steht nichts.

### Was aus dem alten Impressum übernommen wurde

- Inhaber: Adem Yesiltas, Einzelunternehmer
- Anschrift: Heumarkt 6, 63450 Hanau
- Steuernummer: 2288402446

### Was am alten Impressum falsch war und hier korrigiert ist

- Es berief sich auf **§ 5 TMG**. Das Telemediengesetz wurde am
  14. Mai 2024 durch das **Digitale-Dienste-Gesetz (DDG)** abgelöst. Die
  neue Seite zitiert korrekt § 5 DDG.
- Die **E-Mail-Adresse fehlte** und fehlt weiterhin, siehe oben.
- Die Aussage **„DER MIT ABSTAND BESTE IN HANAU"** stand auf jeder Seite.
  Eine Spitzenstellungsbehauptung ohne Beleg ist wettbewerbswidrig. Ist
  ersatzlos gestrichen.
- Die **Bewertungen mit Stockfoto-Avataren** („Fabian M.", „Josh R.")
  sind gestrichen. Erfundene Bewertungen sind wettbewerbswidrig.

### Bewusst weggelassene Abschnitte

- **Registereintrag:** nicht nötig, Einzelunternehmen ohne
  Handelsregistereintrag.
- **USt-IdNr:** § 5 DDG verlangt sie nur, wenn vorhanden. Falls der Wirt
  eine hat, gehört sie zusätzlich rein. Die Steuernummer ist rechtlich
  nicht gefordert, steht aber schon bisher öffentlich auf seiner Seite und
  wurde übernommen.
- **Aufsichtsbehörde:** nur nötig, wenn die Tätigkeit einer behördlichen
  Zulassung bedarf. Der Betrieb schenkt keinen Alkohol aus, damit ist er in
  Hessen nur anzeige-, nicht erlaubnispflichtig. Falls doch eine
  Gaststättenerlaubnis vorliegt, muss die Behörde ergänzt werden.
- **Verantwortlicher nach § 18 Abs. 2 MStV:** nur bei
  journalistisch-redaktionellen Inhalten nötig, hier nicht der Fall.

Das ist keine Rechtsberatung. Bei Zweifeln lässt der Wirt einmal einen
Anwalt drüberschauen, das kostet wenig und ist bei einem Shop gut angelegt.

### Kein Blocker, kann jederzeit nachgereicht werden

- **Fotos.** Die Seite funktioniert ohne. Siehe Kapitel „Fotos einbauen"
  und „Gerichtefotos".
- **Google-Bewertungen.** Abschnitt ist gebaut, erscheint erst mit echten
  Zahlen. Siehe eigenes Kapitel.
- **Gründungsjahr:** aktuell steht überall „seit über zwanzig Jahren". Ein
  Zeitungsbericht des Hanauer Anzeigers vom 14. Dezember 2004 belegt, dass
  der Betrieb damals schon lief, inklusive einer Filiale in Maintal. Die
  alte Website sprach 2025 von 24 Jahren, das ergäbe eine Gründung um 2001.
  Wenn der Wirt das Jahr nennt, kann „seit 2001" statt der vagen Angabe
  stehen, das wirkt stärker.

---

## Bestellfunktion

Kein Server, kein Konto, keine Onlinezahlung, kein Lieferdienst dazwischen.

**Ablauf:** Kategorie wählen oder nach Nummer suchen → Artikel antippen →
Größe, Extra-Zutaten, Weglass-Wünsche, Sonderwunsch, Menge → Warenkorb →
Kasse → fertige Nachricht in WhatsApp, absenden muss der Kunde selbst.

**Warenkorb** liegt im `localStorage`, bleibt also beim Neuladen erhalten
und wird nach dem Absenden geleert.

**Nachrichtenformat, drei Stufen.** Die Symbole sind Absicht: Personal, das
kein Deutsch liest, erkennt an ihnen, was Extras sind, was weggelassen wird,
was die Summe ist und ob geliefert oder abgeholt wird.

Sie kosten aber Platz. Ein Emoji belegt in der URL bis zu zwölf Zeichen, und
bei einer sehr langen Bestellung ist genau daran schon eine Nachricht
unterwegs zerbrochen: Ab der Bruchstelle kamen nur noch Fragezeichen an.
Deshalb schaltet das System gestaffelt zurück, statt es darauf ankommen zu
lassen:

| Stufe | bis | Format |
|-------|-----|--------|
| 1 | 1100 Zeichen | volle Symbole, auch je Zeile |
| 2 | 1600 Zeichen | nur noch Symbole an den Abschnitten |
| 3 | darüber | reiner Text, keine Sonderzeichen |

Gemessen: zwei Artikel mit Extras landen bei 751 Zeichen, also Stufe 1.
Fünf Artikel bei 1116, also Stufe 2. Neun Artikel mit je drei Extras bei
1719, also Stufe 3. Die normale Familienbestellung bleibt in Stufe 1 oder 2.

Die Grenzen stehen oben in `assets/js/bestellen.js` als `GRENZE_VOLL` und
`GRENZE_MITTEL`. Wer die hochsetzt, holt sich den Fehler zurück.

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
