# -*- coding: utf-8 -*-
"""Baut die statische Website der Pizzeria Calimero.

Aufruf:  python3 build.py
Erzeugt alle .html-Dateien neu. Inhalte werden hier gepflegt, nicht im HTML.
"""
import os, sys, html, hashlib, datetime
from menu_data import (SALATE, PASTA, PIZZA, EXTRAS, ZUSATZSTOFFE, ALLERGENE,
                       GROESSEN, EXTRA_ZUTATEN, EXTRA_PREIS, ZUSATZOPTIONEN, WEGLASSEN,
                       GETRAENKE, GETRAENKE_PLATZHALTER, MINDESTBESTELLWERT, LIEFERGEBUEHR,
                       SONDERGROESSEN, ARTIKEL_HINWEIS,
                       BESTELL_PAUSE, MINDESTVERWEILDAUER, BILDER, ANNAHMESCHLUSS, SCHAUFENSTER)
import json

HIER = os.path.dirname(os.path.abspath(__file__))


def fingerabdruck(pfad):
    """Kurzer Hash aus dem Dateiinhalt. Haengt an CSS und JS als ?v=...
    Damit laedt jeder Browser nach einer Aenderung zwingend die neue Datei
    und zeigt nie wieder eine alte Version aus dem Cache."""
    voll = os.path.join(HIER, pfad)
    try:
        with open(voll, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:10]
    except OSError:
        return "0"


BAUZEIT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# ---------------------------------------------------------------- Modus
#   python3 build.py             -> Live-Version fuer Hostinger (indexierbar)
#   python3 build.py --vorschau  -> GitHub-Pages-Vorschau (auf noindex gesetzt)
VORSCHAU = "--vorschau" in sys.argv or "--preview" in sys.argv

LIVE_DOMAIN     = "https://calimero-hanau.de"
VORSCHAU_DOMAIN = "https://calimero.rateriser.tech"   # bei Bedarf anpassen

# ---------------------------------------------------------------- Stammdaten
DOMAIN   = VORSCHAU_DOMAIN if VORSCHAU else LIVE_DOMAIN
ROBOTS   = "noindex, nofollow" if VORSCHAU else "index, follow"
NAME     = "Pizzeria Calimero"
STRASSE  = "Heumarkt 6"
PLZ_ORT  = "63450 Hanau"
TEL_ROH  = "+4961819529595"
TEL_ZEIG = "06181 95 2 95 95"
PDF      = "speisekarte-calimero-2026.pdf"

# --- Betreiber, uebernommen aus dem bisherigen Impressum -------------
INHABER   = "Adem Yesiltas"
STEUERNR  = "2288402446"
EMAIL     = None          # <-- muss noch geliefert werden, siehe README
STAND     = "September 2026"
MAPS     = "https://www.google.com/maps?q=Heumarkt+6,+63450+Hanau&amp;output=embed"
MAPS_LINK= "https://www.google.com/maps/search/?api=1&amp;query=Heumarkt+6%2C+63450+Hanau"

# ---------------------------------------------------------------- Fotos
# Sobald echte Fotos vorliegen: Datei nach assets/img/fotos/ legen und den
# Wert hier von None auf den Dateinamen setzen. Abschnitte ohne Foto werden
# gar nicht erst ausgegeben, die Seite sieht also nie unfertig aus.
FOTOS = {
    "teller":   None,   # z. B. "teller.jpg"  - rundes Bild in der Bühne, quadratisch
    "laden":    None,   # z. B. "laden.jpg"   - Aussenansicht oder Gastraum
    "stadt":    None,   # z. B. "hanau.jpg"   - Hanau, Innenstadt oder Marktplatz
    "ofen":     None,   # z. B. "ofen.jpg"    - Ofen, Teig, Kueche
    "pizza63":  None,   # z. B. "pizza63.jpg" - die Hauspizza Nr. 63
    "pasta":    None,   # z. B. "pasta.jpg"
    "salat":    None,   # z. B. "salat.jpg"
    "team":     None,   # z. B. "team.jpg"
}
FOTO_TEXTE = {
    "teller":  "Frisch aus dem Ofen",
    "laden":   "Heumarkt 6, mitten in der Hanauer Innenstadt",
    "stadt":   "Hanau, unsere Stadt seit über zwanzig Jahren",
    "ofen":    "Jeden Abend in Betrieb",
    "pizza63": "Nr. 63, die Pizza Calimero",
    "pasta":   "Frische Pasta aus der Küche",
    "salat":   "Salate in zwei Größen",
    "team":    "Das Team der Pizzeria Calimero",
}


def foto(schluessel, klasse="foto--breit", mit_text=True):
    """Gibt eine Bildkachel aus, oder nichts, wenn kein Foto hinterlegt ist."""
    datei = FOTOS.get(schluessel)
    if not datei:
        return ""
    text = FOTO_TEXTE.get(schluessel, "")
    unterschrift = f"<figcaption>{text}</figcaption>" if (mit_text and text) else ""
    return (f'<figure class="foto {klasse}">'
            f'<img src="assets/img/fotos/{datei}" alt="{text}" loading="lazy">'
            f'{unterschrift}</figure>')


def hat_fotos(*schluessel):
    return any(FOTOS.get(k) for k in schluessel)


def bild_tag(datei, alt, sizes, klasse="", eager=False):
    """Zwei WebP-Groessen fuer alle modernen Browser, ein JPEG als Sicherheitsnetz.
    Bewusst nur drei Dateien je Gericht, damit der Ordner ueberschaubar bleibt."""
    basis = datei.rsplit(".", 1)[0]
    p = "assets/img/gerichte/"
    web = f"{p}{basis}-450.webp 450w, {p}{basis}-900.webp 900w"
    laden = "eager" if eager else "lazy"
    prio = ' fetchpriority="high"' if eager else ""
    k = f' class="{klasse}"' if klasse else ""
    return (f'<picture{k}>'
            f'<source type="image/webp" srcset="{web}" sizes="{sizes}">'
            f'<img src="{p}{basis}.jpg" alt="{alt}" width="900" height="900" '
            f'loading="{laden}" decoding="async"{prio}>'
            f'</picture>')


def preis_von(nr):
    for liste in (SALATE, PASTA, PIZZA):
        for g in liste:
            if g[0] == nr:
                return g[1], g[4]
    return "", ""


def schaufenster():
    """Grosse Bildflaeche auf der Startseite. Jede Kachel fuehrt in die
    passende Kategorie der Bestellseite."""
    kacheln = []
    for nr in SCHAUFENSTER:
        datei = BILDER.get(nr)
        if not datei:
            continue
        name, preis = preis_von(nr)
        kat = "pizza" if nr >= "040" else ("pasta" if nr >= "012" else "salate")
        kacheln.append(
            f'<a class="schaufenster__kachel" href="bestellen.html#{kat}">'
            '<span class="schaufenster__bild">'
            + bild_tag(datei, name, "(max-width:520px) 100vw, (max-width:900px) 50vw, 33vw",
                       eager=(nr == SCHAUFENSTER[0]))
            + '</span>'
            f'<span class="schaufenster__fuss"><span class="schaufenster__name">{name}</span>'
            f'<span class="schaufenster__preis">ab {preis}&nbsp;€</span></span></a>')
    if not kacheln:
        return ""
    return ('<div class="schaufenster">' + "".join(kacheln) + "</div>")


def laufband():
    """Laufendes Band mit den Argumenten, die den Laden ausmachen.
    Kein Produktkatalog, sondern die Punkte, die eine Bestellung ausloesen."""
    punkte = [
        "Seit über 20 Jahren am Heumarkt",
        "In ganz Hanau frei Haus",
        "Mittagstisch für 7,50&nbsp;€",
        "Ohne Lieferdienst, ohne Aufschlag",
        "Abholen oder liefern lassen",
        "Vor Ort mit EC-Karte zahlen",
        "Dienstag bis Sonntag geöffnet",
    ]
    satz = "".join(f'<span>{p}</span><em>&#9670;</em>' for p in punkte)
    return (f'<div class="laufband" aria-hidden="true"><div class="laufband__spur">'
            f'<div class="laufband__satz">{satz}</div>'
            f'<div class="laufband__satz">{satz}</div></div></div>')


def bewertungsblock():
    """Gesamtbewertung mit Quelle und Link. Bewusst OHNE strukturierte
    Daten (AggregateRating): Google erlaubt keine selbst eingetragenen
    Bewertungen im Markup des eigenen Betriebs."""
    b = BEWERTUNG
    if not b.get("schnitt") or not b.get("anzahl"):
        return ""
    schnitt = ("%.1f" % float(b["schnitt"])).replace(".", ",")
    # Sterne exakt anteilig fuellen statt auf halbe Sterne zu runden.
    anteil = max(0.0, min(100.0, float(b["schnitt"]) / 5 * 100))
    sterne = (f'<span class="bewertung__leer">★★★★★</span>'
              f'<span class="bewertung__voll" style="width:{anteil:.1f}%">★★★★★</span>')
    stand = f' <span class="bewertung__stand">(Stand: {b["stand"]})</span>' if b.get("stand") else ""
    tasten = ""
    if b.get("profil"):
        tasten += (f'<a class="knopf knopf--linie" href="{b["profil"]}" target="_blank" '
                   f'rel="noopener">Alle Bewertungen bei Google lesen</a>')
    if b.get("bewerten"):
        tasten += (f'<a class="knopf knopf--rand" href="{b["bewerten"]}" target="_blank" '
                   f'rel="noopener">Bewertung schreiben</a>')
    return f"""
<section class="bewertung">
  <div class="huelle bewertung__innen">
    <p class="bewertung__sterne" role="img"
       aria-label="{schnitt} von 5 Sternen">{sterne}</p>
    <p class="bewertung__satz">
      <strong>{schnitt} von 5</strong> aus {b["anzahl"]} Google-Bewertungen{stand}
    </p>
    <p class="bewertung__zusatz">Wir geben hier keine ausgewählten Zitate wieder.
    Lesen Sie die Bewertungen im Original, die guten wie die kritischen.</p>
    <div class="bewertung__tasten">{tasten}</div>
  </div>
</section>
"""


# ---------------------------------------------------------------- Bewertungen
# Nur die Gesamtbewertung mit Quelle und Link, keine kopierten Texte.
# Begruendung steht in der README.
#
# WICHTIG: Die Zahlen muessen aus dem Google-Unternehmensprofil des Wirts
# kommen, nicht von Portalen wie Restaurant Guru oder speisekarte.de.
# Die widersprechen sich und sind veraltet. Falsche Bewertungsangaben sind
# irrefuehrende Werbung und abmahnbar.
#
# Solange SCHNITT oder ANZAHL None ist, wird der Abschnitt gar nicht
# ausgegeben. Die Seite sieht also nie unfertig aus.
BEWERTUNG = {
    "schnitt": None,      # z. B. 4.6   (Punkt, nicht Komma)
    "anzahl":  None,      # z. B. 412
    "stand":   None,      # z. B. "September 2026"
    "profil":  None,      # Link auf das Google-Profil, "Alle Bewertungen"
    "bewerten": None,     # Link zum Bewertung schreiben, optional
}

GEBIETE = ["Hanau Innenstadt", "Wolfgang", "Steinheim", "Kesselstadt",
           "Lamboy", "Rosenau", "Dunlop-Gewerbegebiet"]

ZEITEN_TEXT = [
    ("1",       "Montag",                       "Ruhetag"),
    ("2,3,4,5", "Dienstag bis Freitag",         "11:30 – 14:30 &amp; 17:00 – 23:00 Uhr"),
    ("6,0",     "Samstag, Sonntag, Feiertage",  "15:00 – 23:00 Uhr"),
]

ICON_TEL = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6'
            'l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4'
            'c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>')
ICON_WA  = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4'
            'A10 10 0 1012 2zm0 2a8 8 0 110 16 8 8 0 01-4.2-1.2l-.3-.2-2.5.7.7-2.4-.2-.3A8 8 0 0112 4z'
            'm4.3 10.2c-.2-.1-1.3-.7-1.5-.7-.2-.1-.3-.1-.5.1l-.7.8c-.1.2-.3.2-.5.1a6.5 6.5 0 01-3.2-2.8'
            'c-.1-.2 0-.4.1-.5l.5-.6c.1-.2.1-.3 0-.5l-.6-1.5c-.2-.4-.4-.4-.5-.4h-.5c-.2 0-.5.1-.7.3'
            '-.7.7-.9 1.6-.6 2.6.4 1.3 1.4 2.6 2.7 3.6 1.3 1 2.6 1.4 3.6 1.4.9 0 1.7-.4 2.1-.9.2-.3.3-.6.3-.9'
            'v-.4c0-.1-.1-.2-.3-.3z"/></svg>')


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- Bausteine
def kopf(titel, beschreibung, pfad, extra_head="", schema="", robots=None):
    tiefe = ""
    rbt = robots or ROBOTS
    v_css = fingerabdruck("assets/css/calimero.css")
    bodyattr = ' data-seite="bestellen"' if pfad == "bestellen.html" else ""
    canonical = DOMAIN + "/" + pfad if pfad != "index.html" else DOMAIN + "/"
    return f"""<!DOCTYPE html>
<!-- Pizzeria Calimero, Stil A Avorio. Build {BAUZEIT}, CSS {v_css} -->
<html lang="de" data-build="{BAUZEIT}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titel)}</title>
<meta name="description" content="{esc(beschreibung)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{rbt}">
<meta name="theme-color" content="#14532d">
<meta name="color-scheme" content="light">
<meta property="og:type" content="restaurant">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="{NAME} Hanau">
<meta property="og:title" content="{esc(titel)}">
<meta property="og:description" content="{esc(beschreibung)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-calimero.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{tiefe}favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{tiefe}assets/img/favicon-512.png">
<link rel="apple-touch-icon" href="{tiefe}assets/img/favicon-512.png">
<link rel="stylesheet" href="{tiefe}assets/css/calimero.css?v={v_css}">
{extra_head}{schema}</head>
<body{bodyattr}>
<a class="sprung" href="#inhalt">Zum Inhalt springen</a>

<header class="kopf">
  <div class="huelle kopf__innen">
    <a class="kopf__logo" href="index.html" aria-label="{NAME}, zur Startseite">
      <img class="kopf__kueken" src="assets/img/calimero-kueken.png" alt=""
           width="350" height="660">
      <span class="wortmarke">
        <em>Pizzeria</em>
        <b>„Calimero“</b>
      </span>
    </a>
    <nav class="kopf__nav" aria-label="Hauptmenü">
      {navi(pfad)}
    </nav>
    <a class="kopf__tel" href="tel:{TEL_ROH}">{ICON_TEL} {TEL_ZEIG}</a>
  </div>
</header>

<main id="inhalt">
"""


def navi(aktiv):
    punkte = [("index.html", "Start"), ("speisekarte.html", "Speisekarte"),
              ("bestellen.html", "Bestellen"),
              ("ueber-uns.html", "Über uns"), ("kontakt.html", "Kontakt")]
    aus = []
    for href, text in punkte:
        cur = ' aria-current="page"' if href == aktiv else ""
        aus.append(f'<a href="{href}"{cur}>{text}</a>')
    return "\n      ".join(aus)


def fuss(extra_js=""):
    v_js = fingerabdruck("assets/js/calimero.js")
    weitere = ""
    for pfad in ([extra_js] if extra_js else []):
        weitere += (f'\n<script src="{pfad}?v={fingerabdruck(pfad)}" defer></script>')
    zeilen = "\n        ".join(
        f'<li data-tag="{tage}"><span class="zeiten__tag">{tag}'
        f'<b class="zeiten__heute">Heute</b></span>'
        f'<span class="zeiten__zeit">{zeit}</span></li>'
        for tage, tag, zeit in ZEITEN_TEXT)
    return f"""</main>

<footer class="fuss">
  <div class="huelle">
    <div class="fuss__raster">
      <div>
        <p class="fuss__marke"><span>Pizzeria</span><b>„Calimero“</b></p>
        <p>Pizza, Pasta und Salate. Seit über 20 Jahren am Heumarkt
        in der Hanauer Innenstadt.</p>
      </div>
      <div>
        <h2>Bestellen</h2>
        <a class="fuss__tel" href="tel:{TEL_ROH}">{TEL_ZEIG}</a>
        <ul class="fuss__liste">
          <li>Lieferung in Hanau frei Haus</li>
          <li>Mindestbestellwert 11&nbsp;€</li>
          <li>Vor Ort auch Zahlung mit EC-Karte</li>
        </ul>
      </div>
      <div>
        <h2>Öffnungszeiten</h2>
        <ul class="zeiten zeiten--stapel zeiten--kraeftig">
        {zeilen}
        </ul>
        <p class="fuss__mittag">Mittagstisch Dienstag bis Freitag,
        11:30 – 14:30 Uhr, für 7,50&nbsp;€</p>
      </div>
      <div>
        <h2>Adresse</h2>
        <address>
          {NAME}<br>
          {STRASSE}<br>
          {PLZ_ORT}
        </address>
        <p><a href="{MAPS_LINK}" target="_blank" rel="noopener">Route planen</a></p>
      </div>
    </div>
    <div class="fuss__unten">
      <span>© 2026 {NAME}, Hanau</span>
      <nav aria-label="Rechtliches">
        <a href="bestellbedingungen.html">AGB</a>
        <a href="impressum.html">Impressum</a>
        <a href="datenschutz.html">Datenschutz</a>
        <a href="{PDF}" target="_blank" rel="noopener">Speisekarte als PDF</a>
      </nav>
    </div>
  </div>
</footer>

<aside class="consent" id="hinweis-speicher" hidden aria-label="Hinweis zur Datenspeicherung">
  <h2>Kurz zur Datenspeicherung</h2>
  <p><strong>Keine Werbe- oder Analyse-Cookies, keine Tracker.</strong> Warenkorb und
  Kartenauswahl bleiben lokal in Ihrem Browser. Google Maps lädt erst auf Ihren Klick.</p>
  <div class="consent__tasten">
    <button class="knopf knopf--tel" type="button" data-hinweis-ok>Verstanden</button>
    <a class="knopf knopf--rand" href="datenschutz.html">Mehr dazu</a>
  </div>
</aside>

<div class="aktionsleiste">
  <a class="knopf knopf--dunkel" href="bestellen.html">Jetzt bestellen</a>
  <a class="knopf knopf--rand" href="tel:{TEL_ROH}">{ICON_TEL} Anrufen</a>
</div>


<script src="assets/js/calimero.js?v={v_js}" defer></script>{weitere}
</body>
</html>
"""


# ---------------------------------------------------------------- Speisekarte
def gericht_html(g, spalte=False):
    nr, name, zutaten, code, p1, p2 = g
    bild = ""
    if BILDER.get(nr):
        bild = ('  <span class="gericht__bild">'
                + bild_tag(BILDER[nr], name, "72px") + '</span>')
    elif spalte:
        bild = '  <span class="gericht__bild gericht__bild--leer" aria-hidden="true"></span>'

    preise = f'<span>{p1}&nbsp;€</span>' + (f'<span>{p2}&nbsp;€</span>' if p2 else '')
    zeilen = [f'<li class="gericht" id="nr-{nr}">']
    if bild:
        zeilen.append(bild)
    zeilen.append('  <span class="gericht__mitte">')
    zeilen.append('    <span class="gericht__zeile">')
    zeilen.append(f'      <span class="gericht__name">'
                  f'<i class="gericht__nr">{nr}</i>{name}</span>')
    zeilen.append('      <span class="gericht__fuehrung" aria-hidden="true"></span>')
    zeilen.append(f'      <span class="gericht__preise">{preise}</span>')
    zeilen.append('    </span>')
    if zutaten:
        zeilen.append(f'    <span class="gericht__zutaten">{zutaten}</span>')
    if code:
        zeilen.append(f'    <span class="gericht__code">Zusatzstoffe / Allergene: {code}</span>')
    zeilen.append('  </span>')
    zeilen.append('</li>')
    return "\n".join(zeilen)


def gruppe_html(anker, titel, unterzeile, masse, eintraege, nachsatz="", bestell_kat=None):
    spalte = any(BILDER.get(g[0]) for g in eintraege)
    items = "\n".join(gericht_html(g, spalte) for g in eintraege)
    unter = f'<p class="gruppe__unter">{unterzeile}</p>' if unterzeile else ""
    knopf = (f'<a class="gruppe__bestellen" href="bestellen.html#{bestell_kat}">'
             f'Bestellen</a>') if bestell_kat else ""
    return f"""<section class="gruppe" id="{anker}" data-leer="nein">
  <div class="gruppe__kopf">
    <h2>{titel}</h2>
    <span class="gruppe__rechts">{knopf}<span class="gruppe__masse">{masse}</span></span>
  </div>
  {unter}
  <ul class="gerichte">
{items}
  </ul>
  <p class="ornament" aria-hidden="true" style="margin-top:1.6rem"><span>&#9670;</span></p>
  {nachsatz}
</section>"""


def seite_speisekarte():
    masse_np = '<span>Normal</span><span>Groß</span>'
    masse_pizza = '<span>ø&nbsp;26&nbsp;cm</span><span>ø&nbsp;30&nbsp;cm</span>'

    salate = gruppe_html("salate", "Frische Salate", "", masse_np, SALATE, bestell_kat="salate", nachsatz=(
        '<div class="hinweis"><p>Alle Salate mit Joghurt-Dressing, auf Wunsch auch mit '
        'Essig und Öl. <strong>Extra-Dressing 1,00&nbsp;€.</strong></p></div>'))

    pasta = gruppe_html("pasta", "Pasta", "", masse_np, PASTA, bestell_kat="pasta", nachsatz=(
        '<div class="hinweis"><p>Alle Nudelgerichte auf Wunsch mit Käse überbacken, '
        '<strong>1,00&nbsp;€</strong>. Mit&nbsp;* gekennzeichnete Tortellini sind mit '
        'Ricotta und Spinat gefüllt.</p></div>'))

    pizza = gruppe_html("pizza", "Pizza", "", masse_pizza, PIZZA, bestell_kat="pizza", nachsatz=(
        f'<div class="hinweis"><p><strong>Extra-Zutaten:</strong> {EXTRAS}. '
        'Aufpreis 0,50&nbsp;€ bei ø&nbsp;26&nbsp;cm, 1,00&nbsp;€ bei ø&nbsp;30&nbsp;cm.</p></div>'))

    getraenke_link = ('<a href="#getraenke">Getränke</a>'
                      if not GETRAENKE_PLATZHALTER and GETRAENKE else "")
    getraenke = ""
    if not GETRAENKE_PLATZHALTER and GETRAENKE:
        masse_g = '<span>1,0&nbsp;l</span><span>0,33&nbsp;l</span>'
        getraenke = gruppe_html("getraenke", "Getränke", "", masse_g, GETRAENKE,
                                bestell_kat="getraenke", nachsatz=(
            '<div class="hinweis"><p>Sinalco gibt es als 1,0-Liter-Flasche und im '
            '0,33-Liter-Glas. Die übrigen Getränke in der angegebenen Größe. '
            '<strong>Alle Getränkepreise verstehen sich inklusive Pfand.</strong>'
            '</p></div>'))

    zusatz = "\n".join(f'<li><b>{n}</b> {t}</li>' for n, t in ZUSATZSTOFFE)
    allerg = "\n".join(f'<li><b>{n}</b> {t}</li>' for n, t in ALLERGENE)

    schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Menu","name":"Speisekarte {NAME}",
"inLanguage":"de-DE","url":"{DOMAIN}/speisekarte.html",
"hasMenuSection":[
{{"@type":"MenuSection","name":"Frische Salate"}},
{{"@type":"MenuSection","name":"Pasta"}},
{{"@type":"MenuSection","name":"Pizza"}}]}}
</script>
"""

    body = f"""
<section class="abschnitt" style="padding-bottom:1.5rem">
  <div class="huelle">
    <h1>Speisekarte</h1>
    <p style="font-size:1.1rem">Gültig ab Mai 2026. Alle Preise in Euro,
    inklusive Mehrwertsteuer.</p>
    <p style="display:flex;flex-wrap:wrap;gap:.7rem">
      <a class="knopf knopf--tel" href="bestellen.html">Online bestellen</a>
      <a class="knopf knopf--rand" href="{PDF}" target="_blank" rel="noopener">
      Speisekarte als PDF</a>
    </p>
  </div>
</section>

<div class="karte-nav">
  <div class="huelle karte-nav__innen">
    <div class="karte-nav__gruppe">
      <a href="#salate">Salate</a>
      <a href="#pasta">Pasta</a>
      <a href="#pizza">Pizza</a>
      {getraenke_link}
    </div>
    <div class="suche">
      <label class="nur-sr" for="karte-suche">Speisekarte durchsuchen</label>
      <input id="karte-suche" type="search" inputmode="search"
             placeholder="Gericht suchen, z. B. Salami"
             autocomplete="off">
      <button class="suche__leeren" type="button" aria-label="Suche zurücksetzen">×</button>
    </div>
  </div>
</div>

<section class="abschnitt" style="padding-top:2rem">
  <div class="huelle">
    {salate}
    {pasta}
    {pizza}
    {getraenke}
    <p class="kein-treffer">Zu dieser Suche gibt es kein Gericht.
    Rufen Sie uns gerne an: <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a>.</p>
  </div>
</section>

<section class="abschnitt abschnitt--tief" id="legende">
  <div class="huelle">
    <div class="abschnitt__kopf">
      <h2>Zusatzstoffe und Allergene</h2>
      <p>Die Ziffern und Buchstaben hinter den Gerichten bedeuten:</p>
    </div>
    <div class="legende">
      <div>
        <h3>Zusatzstoffe</h3>
        <ul>{zusatz}</ul>
      </div>
      <div>
        <h3>Allergene</h3>
        <ul>{allerg}</ul>
      </div>
    </div>
    <div class="hinweis" style="margin-top:1.8rem">
      <p>Sie haben eine Unverträglichkeit oder Allergie? Sagen Sie uns vor der Bestellung
      Bescheid, wir geben Ihnen zu jedem Gericht Auskunft. Änderungen der Rezepturen und
      Preise bleiben vorbehalten, verbindlich ist die Karte im Restaurant.</p>
    </div>
  </div>
</section>
"""
    return (kopf("Speisekarte – Pizza, Pasta und Salate | Pizzeria Calimero Hanau",
                 "Die komplette Speisekarte der Pizzeria Calimero am Heumarkt in Hanau: "
                 "75 Gerichte, Pizza ab 7,50 €, Pasta, Salate, mit Preisen und Allergenen. "
                 "Auch als PDF.",
                 "speisekarte.html", schema=schema)
            + body + fuss())


# ---------------------------------------------------------------- Startseite
def seite_start():
    zeilen = "\n        ".join(
        f'<li data-tag="{tage}"><span class="zeiten__tag">{tag}'
        f'<b class="zeiten__heute">Heute</b></span>'
        f'<span class="zeiten__zeit">{zeit}</span></li>'
        for tage, tag, zeit in ZEITEN_TEXT)
    gebiete = "\n        ".join(f"<li>{g}</li>" for g in GEBIETE)

    if FOTOS.get("teller"):
        teller = ('<img class="buehne__kueken" '
                  f'src="assets/img/fotos/{FOTOS["teller"]}" '
                  f'alt="{FOTO_TEXTE.get("teller", "")}">')
    else:
        teller = ('<img class="buehne__kueken" src="assets/img/calimero-kueken.png" '
                  'alt="Das Calimero-Küken, Maskottchen der Pizzeria" '
                  'width="350" height="660">')

    bewertungen = bewertungsblock()
    band = laufband()
    schau = schaufenster()

    schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Restaurant",
"name":"{NAME}","alternateName":"Calimero Hanau",
"url":"{DOMAIN}/","image":"{DOMAIN}/assets/img/og-calimero.jpg",
"telephone":"{TEL_ROH}","priceRange":"€",
"servesCuisine":["Italienisch","Pizza","Pasta"],
"menu":"{DOMAIN}/speisekarte.html",
"acceptsReservations":"True",
"address":{{"@type":"PostalAddress","streetAddress":"{STRASSE}",
"postalCode":"63450","addressLocality":"Hanau","addressRegion":"Hessen","addressCountry":"DE"}},
"openingHoursSpecification":[
{{"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Thursday","Friday"],
"opens":"11:30","closes":"14:30"}},
{{"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Thursday","Friday"],
"opens":"17:00","closes":"23:00"}},
{{"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday","Sunday"],
"opens":"15:00","closes":"23:00"}}]}}
</script>
"""

    body = f"""
<section class="buehne">
  <div class="buehne__glanz" aria-hidden="true"></div>
  <div class="huelle buehne__innen">
    <span class="buehne__seite" aria-hidden="true">Heumarkt 6 &middot; Hanau</span>
    <p class="marke buehne__jahre" data-reveal="0">Seit über zwanzig Jahren am Heumarkt</p>
    <h1 data-reveal="80">Pizza, Pasta<em>und Salate.</em></h1>
    <p class="buehne__text" data-reveal="180">Aus der Hanauer Innenstadt. Zum Abholen,
    vor Ort oder in ganz Hanau frei Haus geliefert.</p>
    <div class="buehne__tasten" data-reveal="260">
      <a class="knopf knopf--dunkel" href="bestellen.html"><span>Jetzt bestellen</span></a>
      <a class="knopf knopf--linie" href="speisekarte.html"><span>Speisekarte</span></a>
    </div>
    <ul class="buehne__fakten" data-reveal="340">
      <li><span class="status" data-status><span class="status__punkt"></span>
          <span data-status-text>Öffnungszeiten siehe unten</span></span></li>
      <li><a href="tel:{TEL_ROH}" style="text-decoration:none;color:inherit">{TEL_ZEIG}</a></li>
    </ul>
    {teller}
  </div>
</section>

{band}

<section class="abschnitt abschnitt--knapp">
  <div class="huelle" data-reveal>
    <p class="marke">Aus unserer Küche</p>
  </div>
  {schau}
</section>

<section class="mittag">
  <div class="huelle">
    <div class="mittag__block" data-reveal>
      <p class="marke" style="color:var(--gold-hell)">Dienstag bis Freitag</p>
      <p class="mittag__preis">7,50<span>€</span></p>
      <h2>Der Mittagstisch.</h2>
      <p>Von <strong>11:30 bis 14:30 Uhr</strong> eine Pizza, ein Nudelgericht oder einen
      Salat Ihrer Wahl in normaler Größe. Ausgenommen sind die Nummern 6, 30, 38 und 51.</p>
    </div>
  </div>
</section>

{bewertungen}

<section class="abschnitt">
  <div class="huelle">
    <div class="raster raster--zwei">
      <div data-reveal>
        <p class="marke">Lieferung</p>
        <h2>In Hanau frei Haus.</h2>
        <p style="color:var(--still)">Innerhalb von Hanau ohne Liefergebühr,
        ab 11,00&nbsp;€ Bestellwert.</p>
        <ul class="gebiete" style="margin-top:1.4rem">
        {gebiete}
        </ul>
      </div>
      <div data-reveal="120">
        <p class="marke">Öffnungszeiten</p>
        <ul class="zeiten zeiten--kraeftig">
        {zeilen}
        </ul>
        <p style="margin-top:1rem;color:var(--still);font-size:.95rem">
        Mittagstisch Dienstag bis Freitag, 11:30 – 14:30 Uhr, für 7,50&nbsp;€</p>
        <p style="margin-top:1.4rem">
          <span class="status" data-status><span class="status__punkt"></span>
          <span data-status-text></span></span>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="abschnitt abschnitt--tief">
  <div class="huelle">
    <div class="abschnitt__kopf" data-reveal>
      <p class="marke">Anfahrt</p>
      <h2>{STRASSE}, {PLZ_ORT}</h2>
    </div>
    <div class="zweiklick" data-karte="{MAPS}" data-reveal="80">
      <div class="zweiklick__hinweis">
        <p>Die Karte wird erst nach Ihrer Zustimmung von Google geladen. Dabei wird
        Ihre IP-Adresse an Google übertragen.</p>
        <p style="margin-top:1.2rem">
        <button class="knopf knopf--linie" type="button" data-karte-laden>
        <span>Karte anzeigen</span></button></p>
      </div>
    </div>
    <p style="margin-top:1.4rem"><a href="{MAPS_LINK}" target="_blank" rel="noopener">
    Route in Google Maps planen</a></p>
  </div>
</section>
"""
    return (kopf("Pizzeria Calimero Hanau – Pizza, Pasta und Lieferservice am Heumarkt",
                 "Pizzeria Calimero, Heumarkt 6 in Hanau. Pizza ab 7,50 €, Pasta und Salate. "
                 "Mittagsangebot 7,50 €, Lieferung in Hanau frei Haus. "
                 "Bestellung unter 06181 95 2 95 95.",
                 "index.html", schema=schema)
            + body + fuss())


# ---------------------------------------------------------------- Über uns
def seite_ueber():
    bild_laden = foto("laden", "foto--breit")
    bild_stadt = foto("stadt", "foto--breit")
    bild_team = foto("team", "foto--breit")

    laden_block = (f'<div style="margin:2.4rem 0">{bild_laden}</div>' if bild_laden else "")
    team_block = (f'<div style="margin:2.4rem 0 0">{bild_team}</div>' if bild_team else "")
    stadt_block = (f'<div style="margin:0 0 2.4rem">{bild_stadt}</div>' if bild_stadt else "")

    body = f"""
<section class="abschnitt">
  <div class="huelle">
    <p class="marke">Über uns</p>
    <h1>Seit über zwanzig Jahren<br>am Heumarkt</h1>
    <p style="font-size:1.14rem;max-width:56ch;color:var(--still)">
    Ein kleiner Laden mitten in der Hanauer Innenstadt, ein Ofen, der den ganzen
    Abend läuft, und eine Karte, die sich seit Jahren kaum verändert hat. Weil sie
    funktioniert.</p>

    {laden_block}

    <div class="raster raster--zwei" style="margin-top:2.4rem">
      <div class="block">
        <h2>Was wir machen</h2>
        <p>Pizza in zwei Größen und als Familienpizza mit vierzig Zentimetern, dazu
        Pasta in allen Varianten, Lasagne, Gnocchi und Salate. Fünfundsiebzig
        Gerichte stehen auf der Karte.</p>
        <p>Bestellt wird bei uns per Telefon oder seit Neuestem online. Zum Abholen,
        zum Hierbleiben oder zur Lieferung nach Hause, in Hanau frei Haus.</p>
      </div>
      <div class="block">
        <h2>Der Vogel auf dem Schild</h2>
        <p>Calimero ist das schwarze Küken mit der Eierschale auf dem Kopf, das seit
        den sechziger Jahren aus italienischen Werbespots bekannt ist. Klein, frech
        und immer ein bisschen unterschätzt.</p>
        <p>Er steht auf unserem Schild, auf der Karte, und er hat seine eigene Pizza:
        die <a href="speisekarte.html#nr-063">Pizza Calimero</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="abschnitt abschnitt--tief">
  <div class="huelle">
    <div class="abschnitt__kopf">
      <p class="marke">Aus dem Archiv</p>
      <h2>Ein Zeitungsbericht von 2004</h2>
    </div>
    <div class="raster raster--zwei" style="align-items:start">
      <div>
        <p>Am 14. Dezember 2004 schaute der Hanauer Anzeiger bei uns vorbei und
        testete den Mittagstisch. Damals brachten schwarze Smarts mit unserer
        Telefonnummer auf der Tür das Essen durch die Innenstadt, und auf der
        Speisekarte stand ein Versprechen: blitzschnell.</p>
        <p>Der Tester bestellte unter anderem eine Pizza „Frühstück“, belegt mit
        Tomaten, Käse, Schinken und zwei Spiegeleiern, damals für 5,50&nbsp;€. Knapp
        dreißig Minuten später stand das Essen auf seinem Schreibtisch, noch heiß.</p>
        <p>Diese Pizza gibt es immer noch. Sie steht heute als
        <a href="speisekarte.html#nr-072">Nummer 72</a> auf der Karte, mit denselben
        Zutaten. Und der Mittagstisch von damals läuft auch weiter, heute von
        Dienstag bis Freitag für 7,50&nbsp;€.</p>
      </div>
      <div class="block">
        <h2>Was sich nicht geändert hat</h2>
        <ul style="margin:0;padding-left:1.1rem;color:var(--still)">
          <li>Derselbe Standort: Heumarkt 6</li>
          <li>Dieselbe Telefonnummer</li>
          <li>Der Mittagstisch, Dienstag bis Freitag</li>
          <li>Die Pizza „Frühstück“ von damals</li>
          <li>Montag ist Ruhetag</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="abschnitt">
  <div class="huelle">
    {stadt_block}
    <div class="abschnitt__kopf">
      <h2>Gut zu wissen</h2>
    </div>
    <div class="raster raster--drei">
      <div class="block">
        <h2>Zahlung</h2>
        <p>Vor Ort können Sie mit EC-Karte zahlen. Lieferungen werden bar an der
        Haustür bezahlt.</p>
      </div>
      <div class="block">
        <h2>Mittagsangebot</h2>
        <p>Dienstag bis Freitag, 11:30 bis 14:30 Uhr: Pizza, Nudeln oder Salat in
        normaler Größe für 7,50&nbsp;€. Ausgenommen Nr. 6, 30, 38 und 51.</p>
      </div>
      <div class="block">
        <h2>Größere Bestellungen</h2>
        <p>Büro, Baustelle, Geburtstag? Rufen Sie kurz vorher an, dann steht alles
        pünktlich bereit. <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a></p>
      </div>
    </div>
    {team_block}
  </div>
</section>
"""
    return (kopf("Über uns | Pizzeria Calimero Hanau",
                 "Die Pizzeria Calimero am Heumarkt in Hanau: seit über zwanzig Jahren "
                 "Pizza, Pasta und Salate, zum Abholen, vor Ort oder als Lieferung.",
                 "ueber-uns.html") + body + fuss())


# ---------------------------------------------------------------- Kontakt
def seite_kontakt():
    zeilen = "\n        ".join(
        f'<li data-tag="{tage}"><span class="zeiten__tag">{tag}'
        f'<b class="zeiten__heute">Heute</b></span>'
        f'<span class="zeiten__zeit">{zeit}</span></li>'
        for tage, tag, zeit in ZEITEN_TEXT)
    gebiete = "\n        ".join(f"<li>{g}</li>" for g in GEBIETE)

    body = f"""
<section class="abschnitt">
  <div class="huelle">
    <h1>Kontakt und Bestellung</h1>
    <p style="font-size:1.12rem;max-width:56ch">Am schnellsten geht es per Telefon.
    Halten Sie am besten die Nummern aus der Speisekarte bereit.</p>

    <div class="buehne__tasten" style="margin-top:1.6rem">
      <a class="knopf knopf--dunkel" href="tel:{TEL_ROH}">{ICON_TEL} {TEL_ZEIG}</a>
      <a class="knopf knopf--wa" href="#" data-wa>{ICON_WA} Per WhatsApp bestellen</a>
      <a class="knopf knopf--rand" href="speisekarte.html">Speisekarte</a>
    </div>
    <p><span class="status" data-status
       style="background:var(--carta-tief);border-color:var(--riga);color:var(--inchiostro)">
       <span class="status__punkt"></span><span data-status-text></span></span></p>

    <div class="raster raster--drei" style="margin-top:2.4rem">
      <div class="block">
        <h2>Adresse</h2>
        <address>
          {NAME}<br>{STRASSE}<br>{PLZ_ORT}
        </address>
        <p style="margin-top:.8rem"><a href="{MAPS_LINK}" target="_blank" rel="noopener">Route planen</a></p>
      </div>
      <div class="block">
        <h2>Öffnungszeiten</h2>
        <ul class="zeiten zeiten--kraeftig">
        {zeilen}
        </ul>
        <p style="margin-top:1rem;font-size:.94rem">Mittagstisch Dienstag bis Freitag,
        11:30 – 14:30 Uhr, für 7,50&nbsp;€</p>
      </div>
      <div class="block">
        <h2>Lieferung</h2>
        <p>In Hanau liefern wir frei Haus, ab einem Bestellwert von 11&nbsp;€.</p>
        <ul class="gebiete">
        {gebiete}
        </ul>
      </div>
    </div>

    <div class="hinweis" style="margin-top:1.8rem">
      <p><strong>Hinweis zu WhatsApp:</strong> Wenn Sie uns über WhatsApp schreiben,
      verarbeitet WhatsApp Ireland Ltd. Ihre Daten. Details stehen in unserer
      <a href="datenschutz.html">Datenschutzerklärung</a>. Sie erreichen uns
      selbstverständlich auch weiterhin ganz normal per Telefon.</p>
    </div>
  </div>
</section>

<section class="abschnitt abschnitt--tief" style="padding-top:0">
  <div class="huelle" style="padding-top:clamp(3rem,7vw,5.5rem)">
    <div class="abschnitt__kopf">
      <h2>Anfahrt</h2>
      <p>Wir liegen mitten in der Innenstadt. Parkhäuser am Forum Hanau und
      am Marktplatz sind wenige Minuten zu Fuß entfernt.</p>
    </div>
    <div class="zweiklick" data-karte="{MAPS}">
      <div class="zweiklick__hinweis">
        <p>Die Karte wird erst nach Ihrer Zustimmung von Google geladen. Dabei wird
        Ihre IP-Adresse an Google übertragen.</p>
        <button class="knopf knopf--dunkel" type="button" data-karte-laden>Karte anzeigen</button>
      </div>
    </div>
  </div>
</section>
"""
    return (kopf("Kontakt, Bestellung und Anfahrt | Pizzeria Calimero Hanau",
                 "Pizzeria Calimero, Heumarkt 6, 63450 Hanau. Bestellung unter "
                 "06181 95 2 95 95, Lieferung in Hanau frei Haus ab 11 €.",
                 "kontakt.html") + body + fuss())


# ---------------------------------------------------------------- Impressum
def seite_impressum():
    mail = (f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL
            else '<mark class="todo">E-Mail-Adresse eintragen, gesetzlich vorgeschrieben</mark>')
    body = f"""
<section class="rechtstext">
  <div class="huelle">
    <h1>Impressum</h1>

    <h2>Angaben gemäß § 5 DDG</h2>
    <address>
      {INHABER}<br>
      Inhaber der Pizzeria Calimero<br>
      {STRASSE}<br>
      {PLZ_ORT}
    </address>

    <h2>Kontakt</h2>
    <p>
      Telefon: <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a><br>
      E-Mail: {mail}
    </p>

    <h2>Steuernummer</h2>
    <p>{STEUERNR}</p>

    <h2>Streitbeilegung</h2>
    <p>Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung
    bereit: <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener">
    ec.europa.eu/consumers/odr</a>.</p>
    <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor
    einer Verbraucherschlichtungsstelle teilzunehmen.</p>

    <h2>Haftung für Inhalte</h2>
    <p>Als Diensteanbieter sind wir für eigene Inhalte auf diesen Seiten nach den
    allgemeinen Gesetzen verantwortlich. Wir sind jedoch nicht verpflichtet, übermittelte
    oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen,
    die auf eine rechtswidrige Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder
    Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon
    unberührt. Eine diesbezügliche Haftung ist erst ab dem Zeitpunkt der Kenntnis einer
    konkreten Rechtsverletzung möglich. Bei Bekanntwerden entsprechender Rechtsverletzungen
    werden wir diese Inhalte umgehend entfernen.</p>

    <h2>Haftung für Links</h2>
    <p>Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir
    keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr
    übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter
    oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt
    der Verlinkung auf mögliche Rechtsverstöße überprüft, rechtswidrige Inhalte waren
    nicht erkennbar. Eine permanente inhaltliche Kontrolle ohne konkrete Anhaltspunkte
    einer Rechtsverletzung ist nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen
    werden wir derartige Links umgehend entfernen.</p>

    <h2>Urheberrecht</h2>
    <p>Die durch den Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten
    unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung
    und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der
    schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien
    dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.
    Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die
    Urheberrechte Dritter beachtet und als solche gekennzeichnet. Sollten Sie dennoch auf
    eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen entsprechenden
    Hinweis.</p>
    <p>Die Figur „Calimero“ ist eine geschützte Marke der jeweiligen Rechteinhaber. Die
    Verwendung auf dieser Website erfolgt im Rahmen der bestehenden Geschäftsbezeichnung
    des Betriebs.</p>

    <h2>Bildnachweis</h2>
    <p>Logo und Maskottchen: Pizzeria Calimero. Alle weiteren Abbildungen sind eigene
    Aufnahmen des Betriebs.</p>

    <p style="margin-top:2.4rem;font-size:.9rem">Stand: {STAND}</p>
  </div>
</section>
"""
    return (kopf("Impressum | Pizzeria Calimero Hanau",
                 "Impressum und Anbieterkennzeichnung der Pizzeria Calimero, Heumarkt 6 in 63450 Hanau, mit Kontaktdaten und Angaben nach § 5 DDG.",
                 "impressum.html", robots="noindex, follow")
            + body + fuss())


# ---------------------------------------------------------------- Datenschutz
def seite_datenschutz():
    mail = (f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL
            else '<mark class="todo">E-Mail-Adresse eintragen</mark>')
    body = f"""
<section class="rechtstext">
  <div class="huelle">
    <h1>Datenschutzerklärung</h1>

    <h2>1. Verantwortlicher</h2>
    <p>Verantwortlich für die Datenverarbeitung auf dieser Website ist:</p>
    <address>
      {INHABER}, Inhaber der Pizzeria Calimero<br>
      {STRASSE}, {PLZ_ORT}<br>
      Telefon: <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a><br>
      E-Mail: {mail}
    </address>
    <p>Ein Datenschutzbeauftragter ist gesetzlich nicht erforderlich und wurde
    nicht bestellt.</p>

    <h2>2. Grundsätzliches</h2>
    <p>Diese Website ist eine reine Informationsseite. Es gibt kein Nutzerkonto, kein
    Bestellformular, keinen Newsletter, keine Werbe- oder Analyse-Cookies und keine
    Tracking-Dienste. Alle Schriften, Bilder, Skripte und Stylesheets werden von unserem
    eigenen Server ausgeliefert, nicht von externen Anbietern.</p>

    <h2>3. Server-Logfiles beim Hosting</h2>
    <p>Beim Aufruf dieser Website erhebt unser Hoster automatisch Daten, die Ihr Browser
    übermittelt. Das sind:</p>
    <ul>
      <li>aufgerufene Seite und Datum sowie Uhrzeit des Zugriffs</li>
      <li>übertragene Datenmenge und Meldung über den Erfolg des Abrufs</li>
      <li>Browsertyp und Browserversion, verwendetes Betriebssystem</li>
      <li>Referrer-URL, also die zuvor besuchte Seite</li>
      <li>IP-Adresse</li>
    </ul>
    <p>Diese Daten sind technisch erforderlich, um die Website auszuliefern und ihre
    Stabilität und Sicherheit zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f
    DSGVO, unser berechtigtes Interesse an einem fehlerfreien und sicheren Betrieb.
    Eine Zusammenführung dieser Daten mit anderen Datenquellen findet nicht statt.</p>
    <p>Hosting-Dienstleister ist Hostinger International Ltd., 61 Lordou Vironos Street,
    6023 Larnaca, Zypern. Mit dem Anbieter besteht ein Vertrag über die
    Auftragsverarbeitung nach Art. 28 DSGVO.</p>

    <h2>4. Kontaktaufnahme per Telefon</h2>
    <p>Wenn Sie uns anrufen, um zu bestellen oder zu reservieren, verarbeiten wir die
    dabei angegebenen Daten, in der Regel Name, Telefonnummer, Lieferadresse und
    Bestellinhalt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, da die Verarbeitung
    zur Durchführung Ihrer Bestellung erforderlich ist. Die Daten werden nach Abwicklung
    der Bestellung gelöscht, soweit keine gesetzlichen Aufbewahrungsfristen bestehen.</p>

    <h2>5. Kontaktaufnahme über WhatsApp</h2>
    <p>Auf dieser Website befinden sich Schaltflächen, die einen Chat mit uns über
    WhatsApp öffnen. Es handelt sich um einfache Links. Erst wenn Sie darauf klicken,
    wird eine Verbindung zu den Servern von WhatsApp aufgebaut.</p>
    <p>Anbieter ist WhatsApp Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Irland.
    Beim Schreiben über WhatsApp werden Ihre Telefonnummer, Ihr Profilname, Ihr
    Nachrichteninhalt sowie Metadaten wie Zeitpunkt und Onlinestatus verarbeitet.
    WhatsApp gehört zur Meta-Unternehmensgruppe, dabei kann es zu einer Übermittlung
    von Daten in die USA kommen. Meta stützt diese Übermittlung auf den
    EU-US Data Privacy Framework sowie auf Standardvertragsklauseln.</p>
    <p>Rechtsgrundlage für die Verarbeitung durch uns ist Art. 6 Abs. 1 lit. b DSGVO
    bei Bestellungen sowie Art. 6 Abs. 1 lit. f DSGVO für eine unkomplizierte
    Kontaktmöglichkeit. Die Nutzung von WhatsApp ist freiwillig. Sie erreichen uns
    genauso gut telefonisch. Chatverläufe löschen wir, sobald sie nicht mehr benötigt
    werden. Weitere Informationen finden Sie in der Datenschutzrichtlinie von WhatsApp:
    <a href="https://www.whatsapp.com/legal/privacy-policy-eea" target="_blank"
    rel="noopener">whatsapp.com/legal/privacy-policy-eea</a>.</p>

    <h2>6. Google Maps, Zwei-Klick-Lösung</h2>
    <p>Auf den Seiten „Start“ und „Kontakt“ können Sie eine Karte von Google Maps
    anzeigen lassen. Die Karte wird <strong>nicht automatisch geladen</strong>. Erst
    wenn Sie auf die entsprechende Schaltfläche klicken, wird eine Verbindung zu den
    Servern von Google aufgebaut und Ihre IP-Adresse an Google übertragen.</p>
    <p>Anbieter ist Google Ireland Limited, Gordon House, Barrow Street, Dublin 4,
    Irland. Dabei kann es zu einer Datenübermittlung in die USA kommen. Google stützt
    diese Übermittlung auf den EU-US Data Privacy Framework sowie auf
    Standardvertragsklauseln.</p>
    <p>Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO sowie
    § 25 Abs. 1 TDDDG. Sie können Ihre Einwilligung jederzeit mit Wirkung für die
    Zukunft widerrufen:</p>
    <p><button class="knopf knopf--rand" type="button" data-consent-zuruecksetzen>
    Einwilligung für die Karte widerrufen</button></p>
    <p>Weitere Informationen: <a href="https://policies.google.com/privacy?hl=de"
    target="_blank" rel="noopener">policies.google.com/privacy</a>.</p>

    <h2>7. Lokale Speicherung im Browser</h2>
    <p>Wir setzen keine Cookies. Um uns Ihre Entscheidung über die Kartenanzeige zu
    merken, speichern wir einen einzelnen Wert im lokalen Speicher Ihres Browsers
    (localStorage), unter dem Schlüssel <code>calimero-karte-einwilligung</code>.
    Dieser Wert verlässt Ihr Gerät nicht und wird nicht an uns oder an Dritte
    übertragen. Sie können ihn jederzeit löschen, indem Sie die Websitedaten in Ihren
    Browsereinstellungen leeren oder oben auf den Widerruf klicken.</p>

    <h2>8. Speisekarte als PDF</h2>
    <p>Die Speisekarte wird als PDF-Datei von unserem eigenen Server ausgeliefert.
    Beim Abruf gelten dieselben Angaben wie unter Punkt 3.</p>

    <h2>9. Ihre Rechte</h2>
    <p>Sie haben jederzeit das Recht auf:</p>
    <ul>
      <li>Auskunft über die zu Ihrer Person gespeicherten Daten (Art. 15 DSGVO)</li>
      <li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
      <li>Löschung (Art. 17 DSGVO)</li>
      <li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
      <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
      <li>Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen
      (Art. 21 DSGVO)</li>
      <li>Widerruf einer erteilten Einwilligung mit Wirkung für die Zukunft
      (Art. 7 Abs. 3 DSGVO)</li>
    </ul>
    <p>Wenden Sie sich dazu an die oben genannten Kontaktdaten.</p>

    <h2>10. Beschwerderecht bei der Aufsichtsbehörde</h2>
    <p>Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren.
    Zuständig ist in der Regel die Behörde am Ort unseres Sitzes:</p>
    <address>
      Der Hessische Beauftragte für Datenschutz und Informationsfreiheit<br>
      Postfach 3163, 65021 Wiesbaden<br>
      <a href="https://datenschutz.hessen.de" target="_blank" rel="noopener">datenschutz.hessen.de</a>
    </address>

    <h2>11. SSL-Verschlüsselung</h2>
    <p>Diese Seite nutzt aus Sicherheitsgründen eine TLS-Verschlüsselung. Sie erkennen
    das an der Adresszeile Ihres Browsers, die mit „https://“ beginnt, sowie am
    Schloss-Symbol.</p>

    <h2>12. Aktualität</h2>
    <p>Stand dieser Datenschutzerklärung: {STAND}. Durch die Weiterentwicklung unserer Website oder aufgrund
    geänderter gesetzlicher Vorgaben kann es notwendig werden, diese Erklärung
    anzupassen.</p>
  </div>
</section>
"""
    return (kopf("Datenschutzerklärung | Pizzeria Calimero Hanau",
                 "Datenschutzerklärung der Pizzeria Calimero in Hanau: welche Daten bei Bestellung, Kontakt und Kartenanzeige verarbeitet werden und welche Rechte Sie haben.",
                 "datenschutz.html",
                 extra_head='<meta name="robots" content="noindex, follow">\n')
            .replace('<meta name="robots" content="{rbt}">\n', "")
            + body + fuss())


# ---------------------------------------------------------------- 404
def seite_404():
    body = f"""
<section class="abschnitt" style="text-align:center">
  <div class="huelle">
    <img src="assets/img/calimero-kueken.png" alt="" width="350" height="660"
         style="width:140px;margin:0 auto 1.5rem">
    <h1>Diese Seite gibt es nicht</h1>
    <p style="margin-inline:auto">Vielleicht hat sich ein Tippfehler eingeschlichen.
    Die Speisekarte finden Sie hier, bestellen können Sie jederzeit telefonisch.</p>
    <p class="buehne__tasten" style="justify-content:center">
      <a class="knopf knopf--dunkel" href="speisekarte.html">Zur Speisekarte</a>
      <a class="knopf knopf--rand" href="tel:{TEL_ROH}">{ICON_TEL} {TEL_ZEIG}</a>
    </p>
  </div>
</section>
"""
    return (kopf("Seite nicht gefunden | Pizzeria Calimero Hanau",
                 "Diese Seite der Pizzeria Calimero in Hanau existiert nicht. Hier geht es zurück zur Speisekarte und zur Bestellung.", "404.html",
                 extra_head='<meta name="robots" content="noindex, nofollow">\n')
            .replace('<meta name="robots" content="{rbt}">\n', "")
            + body + fuss())



# ---------------------------------------------------------------- menu.json
def preis(t):
    return round(float(t.replace(",", ".")), 2)


def menu_json():
    kategorien = [
        {"id": "pizza",      "name": "Pizza",     "groessen": GROESSEN["pizza"],  "extras": True},
        {"id": "pasta",      "name": "Pasta",     "groessen": GROESSEN["pasta"],  "extras": True},
        {"id": "salate",     "name": "Salate",    "groessen": GROESSEN["salate"], "extras": True},
    ]
    if not GETRAENKE_PLATZHALTER:
        kategorien.append({"id": "getraenke", "name": "Getränke",
                           "groessen": GROESSEN.get("getraenke", []), "extras": False})
    artikel = []
    quellen = [("pizza", PIZZA, GROESSEN["pizza"]),
               ("pasta", PASTA, GROESSEN["pasta"]),
               ("salate", SALATE, GROESSEN["salate"]),
               ("getraenke", (GETRAENKE if not GETRAENKE_PLATZHALTER else []),
                GROESSEN.get("getraenke", []))]
    for kat, liste, groessen in quellen:
        for nr, name, desc, code, p1, p2 in liste:
            preise = {}
            if groessen and p2:
                preise[groessen[0][0]] = preis(p1)
                preise[groessen[1][0]] = preis(p2)
            else:
                preise["standard"] = preis(p1)
            eintrag = {"id": kat + "-" + nr, "nr": nr, "name": name,
                       "desc": desc, "codes": code, "kat": kat, "preise": preise}
            if nr in SONDERGROESSEN:
                eintrag["groessen"] = SONDERGROESSEN[nr]
            if nr in ARTIKEL_HINWEIS:
                eintrag["hinweis"] = ARTIKEL_HINWEIS[nr]
            if BILDER.get(nr):
                eintrag["bild"] = "assets/img/gerichte/" + BILDER[nr]
            artikel.append(eintrag)

    daten = {
        "kategorien": kategorien,
        "artikel": artikel,
        "extras": {"liste": EXTRA_ZUTATEN, "preise": EXTRA_PREIS},
        "zusatzoptionen": ZUSATZOPTIONEN,
        "weglassen": WEGLASSEN,
        "mindest": MINDESTBESTELLWERT,
        "liefergebuehr": LIEFERGEBUEHR,
        "liefergebiete": GEBIETE,
        "limit": {"pause": BESTELL_PAUSE, "verweildauer": MINDESTVERWEILDAUER},
    }
    return json.dumps(daten, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- Bestellseite
def seite_bestellen():
    warnung = ""

    body = f"""
<section class="best-kopf">
  <div class="huelle">
    <h1>Online bestellen</h1>
    <p>Gerichte auswählen, Warenkorb prüfen, fertig. Die Bestellung geht als
    Nachricht direkt an unser Telefon, ohne Lieferdienst dazwischen.</p>
    <ul class="best-ablauf">
      <li><b>1</b> Auswählen</li>
      <li><b>2</b> Warenkorb prüfen</li>
      <li><b>3</b> Per WhatsApp absenden</li>
      <li><b>4</b> Wir bestätigen die Zeit</li>
    </ul>
    <p style="margin-top:1.2rem"><span class="status" data-status
       style="background:#fff;border-color:var(--riga);color:var(--inchiostro)">
       <span class="status__punkt"></span><span data-status-text></span></span></p>
    <p style="font-size:.94rem;color:var(--inchiostro-weich);margin-top:1rem">
    Bezahlt wird erst bei der Übergabe, bar oder mit EC-Karte im Laden.
    Es gibt keine Onlinezahlung. Lieferung in Hanau frei Haus ab
    {('%.2f' % MINDESTBESTELLWERT).replace('.', ',')}&nbsp;€.
    Lieber telefonisch? <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a> oder
    <a href="{PDF}" target="_blank" rel="noopener">Speisekarte als PDF</a>.</p>
    {warnung}
  </div>
</section>

<div class="geschlossen" id="geschlossen-hinweis" hidden>
  <div class="huelle geschlossen__innen">
    <strong>Wir haben gerade geschlossen.</strong>
    <span data-geschlossen-text></span>
    <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a>
  </div>
</div>

<div class="best-nav">
  <div class="huelle best-nav__innen">
    <div id="kat-tabs" class="karte-nav__gruppe" role="group" aria-label="Kategorie wählen"></div>
    <div class="suche">
      <label class="nur-sr" for="artikel-suche">Gericht suchen</label>
      <input id="artikel-suche" type="search" inputmode="search"
             placeholder="Gericht suchen, z. B. Salami" autocomplete="off">
    </div>
  </div>
</div>

<section class="abschnitt" style="padding-top:1rem">
  <div class="huelle">
    <div id="artikel-liste" class="best-liste">
      <p class="konfig__hint">Speisekarte wird geladen …</p>
    </div>
    <noscript>
      <div class="hinweis"><p><strong>Für die Bestellfunktion wird JavaScript benötigt.</strong>
      Sie können uns aber jederzeit anrufen: <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a>.
      Die komplette Karte finden Sie unter
      <a href="speisekarte.html">Speisekarte</a>.</p></div>
    </noscript>
  </div>
</section>

<button id="korb-leiste" type="button" hidden>
  <span id="korb-anzahl">0 Artikel</span>
  <span>Warenkorb ansehen</span>
  <span id="korb-summe">0,00 €</span>
</button>

<div class="overlay" id="overlay" hidden>
  <div class="overlay__panel" id="overlay-panel" role="dialog" aria-modal="true"></div>
</div>
"""
    extra = ('<script>window.CALIMERO_TEL="' + TEL_ROH + '";'
             'window.CALIMERO_TEL_ANZEIGE="' + TEL_ZEIG + '";'
             'window.CALIMERO_ANNAHMESCHLUSS=' + str(ANNAHMESCHLUSS) + ';</script>\n')
    seite = (kopf("Online bestellen | Pizzeria Calimero Hanau",
                  "Pizza, Pasta und Salate der Pizzeria Calimero online zusammenstellen und "
                  "direkt bestellen. Abholung oder Lieferung in Hanau, Zahlung bei Übergabe.",
                  "bestellen.html", extra_head=extra)
             + body + fuss(extra_js="assets/js/bestellen.js"))
    return seite


# ---------------------------------------------------------------- Bestellbedingungen
def seite_bestellbedingungen():
    mail = (f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL
            else '<mark class="todo">E-Mail-Adresse eintragen</mark>')
    gebiete = ", ".join(GEBIETE)
    mind = ("%.2f" % MINDESTBESTELLWERT).replace(".", ",")
    body = f"""
<section class="rechtstext">
  <div class="huelle">
    <h1>Allgemeine Geschäftsbedingungen</h1>
    <p class="marke">für Bestellungen über diese Website</p>
    <p>Diese Bedingungen gelten für Bestellungen, die über das Bestellformular auf
    dieser Website abgegeben werden. Für telefonische Bestellungen gelten sie sinngemäß.</p>

    <h2>1. Anbieter</h2>
    <address>
      {INHABER}, Inhaber der Pizzeria Calimero<br>
      {STRASSE}, {PLZ_ORT}<br>
      Telefon: <a href="tel:{TEL_ROH}">{TEL_ZEIG}</a><br>
      E-Mail: {mail}
    </address>

    <h2>2. Wie der Vertrag zustande kommt</h2>
    <p>Die Darstellung der Speisen auf dieser Website ist kein bindendes Angebot, sondern
    eine Aufforderung an Sie, eine Bestellung abzugeben.</p>
    <p>Mit dem Absenden der Bestellung geben Sie ein verbindliches Angebot ab. Ein Vertrag
    kommt <strong>erst dann</strong> zustande, wenn wir Ihre Bestellung ausdrücklich
    bestätigen, in der Regel per Nachricht oder Anruf, oder wenn wir mit der Zubereitung
    beginnen. Eine automatische Eingangsbestätigung ist keine Annahme.</p>
    <p>Wir behalten uns vor, Bestellungen abzulehnen, etwa bei zu hoher Auslastung, wenn
    einzelne Zutaten nicht verfügbar sind, kurz vor Ladenschluss oder wenn die
    Lieferadresse außerhalb unseres Liefergebiets liegt.</p>

    <h2>3. Übermittlung über WhatsApp</h2>
    <p>Die zusammengestellte Bestellung wird als vorbereitete Textnachricht in WhatsApp
    geöffnet. Abgesendet wird sie erst durch Sie selbst. Solange Sie die Nachricht nicht
    absenden, liegt uns keine Bestellung vor. Zur Verarbeitung Ihrer Daten durch WhatsApp
    siehe unsere <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
    <p>Sie können uns stattdessen jederzeit anrufen. Die Bestellnummer, die Ihnen am Ende
    angezeigt wird, dient nur der einfacheren Zuordnung bei Abholung oder Übergabe.</p>

    <h2>4. Preise</h2>
    <p>Alle Preise sind Endpreise in Euro und enthalten die gesetzliche Mehrwertsteuer.
    Aufpreise für Extra-Zutaten sind im Warenkorb einzeln ausgewiesen. Bei Getränken
    ist das Pfand im angegebenen Preis bereits enthalten, es wird nicht zusätzlich
    berechnet.</p>
    <p>Sonderwünsche im Freitextfeld, die einen Aufpreis auslösen, sind im angezeigten
    Gesamtpreis noch nicht enthalten. Wir nennen Ihnen den Aufpreis bei der Bestätigung,
    bevor der Vertrag zustande kommt.</p>
    <p>Das Mittagsangebot gilt nur vor Ort und telefonisch zu den ausgewiesenen Zeiten und
    wird im Onlinewarenkorb nicht automatisch verrechnet.</p>

    <h2>5. Lieferung und Abholung</h2>
    <ul>
      <li>Abholung: {STRASSE}, {PLZ_ORT}, zu den Öffnungszeiten.</li>
      <li>Lieferung: innerhalb von Hanau frei Haus, ohne zusätzliche Liefergebühr.</li>
      <li>Mindestbestellwert bei Lieferung: {mind}&nbsp;€.</li>
      <li>Liefergebiet: {gebiete}.</li>
    </ul>
    <p>Angegebene Zeiten sind unverbindliche Schätzungen. Bei hohem Andrang kann es
    länger dauern, wir nennen Ihnen die voraussichtliche Zeit bei der Bestätigung.</p>

    <h2>6. Bezahlung</h2>
    <p>Es gibt keine Onlinezahlung. Bezahlt wird bei der Übergabe:</p>
    <ul>
      <li>bei Abholung im Laden in bar oder mit EC-Karte,</li>
      <li>bei Lieferung in bar an der Haustür.</li>
    </ul>

    <h2>7. Widerrufsrecht</h2>
    <p>Ein Widerrufsrecht besteht nicht. Nach § 312g Abs. 2 Nr. 2 BGB ist das
    Widerrufsrecht bei der Lieferung von Waren ausgeschlossen, die schnell verderben
    können oder deren Verfallsdatum schnell überschritten würde. Nach § 312g Abs. 2 Nr. 9
    BGB gilt dies ebenso für Dienstleistungen im Zusammenhang mit der Lieferung von
    Speisen und Getränken zu einem bestimmten Termin.</p>
    <p>Sie können eine Bestellung aber selbstverständlich stornieren, solange wir noch
    nicht mit der Zubereitung begonnen haben. Rufen Sie uns dazu einfach an.</p>

    <h2>8. Allergene und Zusatzstoffe</h2>
    <p>Angaben zu Zusatzstoffen und Allergenen finden Sie bei jedem Gericht sowie
    gesammelt in der <a href="speisekarte.html">Speisekarte</a>. Bei einer Allergie oder
    Unverträglichkeit rufen Sie uns bitte vor der Bestellung an. In unserer Küche werden
    Zutaten gemeinsam verarbeitet, Spuren anderer Allergene lassen sich nicht
    vollständig ausschließen.</p>

    <h2>9. Mängel</h2>
    <p>Sollte etwas nicht stimmen, melden Sie sich bitte umgehend telefonisch, damit wir
    es klären können. Es gelten die gesetzlichen Gewährleistungsrechte.</p>

    <h2>10. Streitbeilegung</h2>
    <p>Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung bereit:
    <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener">
    ec.europa.eu/consumers/odr</a>. Wir sind nicht bereit und nicht verpflichtet, an
    Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>

    <p style="margin-top:2.4rem;font-size:.9rem">Stand: {STAND}</p>
  </div>
</section>
"""
    return (kopf("AGB und Bestellbedingungen | Pizzeria Calimero Hanau",
                 "Allgemeine Geschäftsbedingungen für Onlinebestellungen bei der Pizzeria Calimero in Hanau.",
                 "bestellbedingungen.html", robots="noindex, follow")
            + body + fuss())


# ---------------------------------------------------------------- Schreiben
SEITEN = {
    "index.html": seite_start,
    "speisekarte.html": seite_speisekarte,
    "ueber-uns.html": seite_ueber,
    "kontakt.html": seite_kontakt,
    "impressum.html": seite_impressum,
    "datenschutz.html": seite_datenschutz,
    "bestellen.html": seite_bestellen,
    "bestellbedingungen.html": seite_bestellbedingungen,
    "404.html": seite_404,
}

def robots_txt():
    if VORSCHAU:
        return "# Vorschau, nicht indexieren\nUser-agent: *\nDisallow: /\n"
    return (f"User-agent: *\nAllow: /\n"
            f"Disallow: /impressum.html\nDisallow: /datenschutz.html\nDisallow: /bestellbedingungen.html\n\n"
            f"Sitemap: {DOMAIN}/sitemap.xml\n")

SITEMAP_SEITEN = [("", "1.0"), ("speisekarte.html", "0.9"), ("bestellen.html", "0.9"),
                  ("kontakt.html", "0.8"), ("ueber-uns.html", "0.6")]


def sitemap():
    eintraege = "\n".join(
        f"  <url><loc>{DOMAIN}/{p}</loc><changefreq>monthly</changefreq>"
        f"<priority>{prio}</priority></url>" for p, prio in SITEMAP_SEITEN)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + eintraege + "\n</urlset>\n")


if __name__ == "__main__":
    for datei, fn in SEITEN.items():
        with open(os.path.join(HIER, datei), "w", encoding="utf-8") as f:
            f.write(fn())
        print("geschrieben:", datei)
    with open(os.path.join(HIER, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt())
    with open(os.path.join(HIER, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    with open(os.path.join(HIER, "menu.json"), "w", encoding="utf-8") as f:
        f.write(menu_json())
    print("geschrieben: menu.json")
    if GETRAENKE_PLATZHALTER:
        print("ACHTUNG: Getraenkepreise sind noch Platzhalter (menu_data.py).")
    print("geschrieben: robots.txt, sitemap.xml")
    print("Gerichte gesamt:", len(SALATE) + len(PASTA) + len(PIZZA))
    print("Modus:", "VORSCHAU (noindex) auf " + DOMAIN if VORSCHAU
          else "LIVE auf " + DOMAIN)
