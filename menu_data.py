# -*- coding: utf-8 -*-
"""Speisekarte Pizzeria Calimero, gueltig ab Mai 2026.
Quelle: gedruckte Speisekarte 2026 (Speisekarte_2026_2.pdf).
Format je Gericht: (Nr, Name, Beschreibung, Zusatzstoffe/Allergene, Preis normal, Preis gross)
Preis gross = None -> nur ein Preis.
"""

SALATE = [
    ("001", "Grüner Salat", "Eisbergsalat, Tomaten, Gurken und Zwiebeln", "", "6,50", "8,50"),
    ("002", "Italienischer Salat", "Eisbergsalat, Tomaten, Gurken, Zwiebeln, Käse, Schinken, Eier, Thunfisch und Oliven", "2,3,4,6,9", "9,00", "11,50"),
    ("003", "Tomaten-Salat", "Tomaten und Zwiebeln", "", "7,00", "9,00"),
    ("004", "Capricciosa-Salat", "Eisbergsalat, Tomaten, Gurken, Zwiebeln, Schafskäse, milde Peperoni, Oliven und Eier", "6", "8,50", "10,50"),
    ("005", "Salat Caprese", "Tomaten, Mozzarella und frischer Basilikum", "", "8,50", "10,50"),
    ("006", "Salat „Chef“", "Eisbergsalat, Tomaten, Gurken, Zwiebeln, Käse, Schinken, Eier, Oliven, Thunfisch, Paprika, Artischocken und Kapern", "2,3,4,6,9", "10,00", "12,00"),
    ("007", "Marinara-Salat", "Eisbergsalat, frische Meeresfrüchte und Knoblauch", "2,3,4,9,h,g", "9,50", "11,50"),
    ("008", "Florida-Salat", "Eisbergsalat, Mais, Tomaten, Gurken, Zwiebeln, Hähnchenbrust, extra Käse und Shrimps", "2,3,9,d,h,g", "9,50", "11,50"),
    ("009", "Gurkensalat", "mit Joghurt-Dressing", "", "6,50", "8,50"),
    ("010", "Mexiko-Salat", "Eisbergsalat, Tomaten, Gurken, Zwiebeln, Mais, Karotten, Peperoni mild und Ei", "", "9,00", "10,00"),
]

PASTA = [
    ("012", "Spaghetti Napoli", "mit Tomatensauce", "", "7,50", "9,50"),
    ("013", "Spaghetti Bolognese", "mit Hackfleischsauce", "", "8,00", "10,00"),
    ("014", "Spaghetti Carbonara", "mit Sahne, Schinken und Ei", "2,3,4,9", "9,00", "11,00"),
    ("015", "Spaghetti alla Olio", "mit Olivenöl und Knoblauch (scharf)", "", "8,50", "10,50"),
    ("016", "Spaghetti con Tonno", "mit Thunfisch, Schafskäse und Oliven in Sahnesauce", "", "9,00", "11,00"),
    ("017", "Spaghetti Marinara", "mit Tomatensauce und Meeresfrüchten", "h,g", "9,50", "11,50"),
    ("018", "Rigatoni Broccoli", "mit Sahne und frischem Broccoli", "", "8,50", "10,50"),
    ("019", "Rigatoni al Forno", "mit Hackfleischsauce und Käse überbacken", "", "9,00", "11,00"),
    ("020", "Rigatoni alla „Chef“", "mit Sahne, Bolognese, Schinken, Erbsen und frischen Pilzen", "2,3,4,9", "9,00", "11,00"),
    ("021", "Rigatoni Quattro Formaggio", "mit vier verschiedenen Käsesorten", "", "9,50", "11,50"),
    ("022", "Rigatoni Broccoli Gorgonzola", "mit frischem Broccoli und Gorgonzolakäse", "", "9,00", "11,00"),
    ("023", "Tortellini alla Panna*", "mit Sahne-Schinkensauce", "2,3,4,9", "8,50", "10,50"),
    ("024", "Tortellini Bolognese*", "mit Hackfleischsauce", "2,3,4,9", "8,00", "10,00"),
    ("025", "Tortellini alla „Chef“*", "mit Sahne, Bolognese, Schinken, Erbsen und frischen Pilzen", "2,3,4,9", "9,00", "11,00"),
    ("026", "Tortellini Gorgonzola*", "mit Sahne-Gorgonzolasauce", "", "8,50", "11,00"),
    ("027", "Tagliatelle Panna", "mit Sahne-Schinkensauce", "2,3,4,6,9", "8,50", "10,50"),
    ("028", "Tagliatelle Pesto", "mit Pesto alla Genovese", "", "8,50", "10,50"),
    ("029", "Tagliatelle alla „Chef“", "mit frischen Pilzen, Pfifferlingen und Sahne-Tomatensauce", "", "9,00", "11,00"),
    ("030", "Trio Pasta", "mit drei verschiedenen Nudelsorten", "", "10,00", "12,00"),
    ("031", "Gnocchi", "mit Tomatensauce und frischem Basilikum", "", "8,00", "10,50"),
    ("032", "Gnocchi", "mit Gorgonzolasauce", "", "8,50", "11,00"),
    ("033", "Lasagne", "mit Bechamelsauce", "", "8,50", "10,50"),
    ("034", "Lasagne Spezial", "mit frischen Pilzen, Schinken und Eiern", "2,3,4,6,9", "9,50", "12,00"),
    ("035", "Tagliatelle Tonno", "mit Tomatensauce, Thunfisch, Oliven und Knoblauch", "6", "9,00", "11,00"),
    ("036", "Nudeln Vegetaria", "mit Mais, Erbsen, Pilzen, Paprika, in Sahnesauce", "", "9,50", "11,50"),
    ("037", "Pasta Mista Primavera", "mit Kräutersahnesauce und Schinken", "2,3,4,6,9", "9,50", "11,50"),
    ("038", "Pasta Mista alla „Chef“", "mit Sahne, Bolognese, Schinken, Erbsen und frischen Pilzen", "2,3,4,6,9", "10,00", "12,00"),
    ("039", "Tagliatelle al arrabbiata", "mit Tomatensauce (scharf)", "", "8,50", "10,50"),
]

PIZZA = [
    ("040", "Pizza Margarita", "mit Tomatensauce und Käse", "", "7,50", "10,00"),
    ("041", "Pizza Salami", "mit Tomatensauce, Käse und Salami", "2,3,4", "8,00", "11,00"),
    ("042", "Pizza Schinken", "mit Tomatensauce, Käse und Schinken", "", "8,00", "11,00"),
    ("043", "Pizza Pilze", "mit Tomatensauce, Käse und frischen Pilzen", "2,3,9", "8,00", "11,00"),
    ("044", "Pizza Mix", "mit Tomatensauce, Käse, Salami, Peperoniwurst und Pilzen", "2,3,4", "8,50", "12,00"),
    ("045", "Pizza Peperoniwurst", "mit Tomatensauce, Käse und Peperoniwurst", "2,3,4", "8,00", "11,00"),
    ("046", "Pizza Broccoli", "mit Tomatensauce, Käse, frischem Broccoli und Knoblauch", "", "8,50", "12,00"),
    ("047", "Pizza Vegetaria", "mit Tomatensauce, Käse, Paprika, Artischocken, Zwiebeln, frischen Pilzen und Mais", "", "9,00", "12,50"),
    ("048", "Pizza Roma", "mit Tomatensauce, Käse, Salami, Schinken, frischen Pilzen, Zwiebeln und Knoblauch", "2,3,4,9,d", "9,00", "12,50"),
    ("049", "Pizza Hawaii", "mit Tomatensauce, Käse, Schinken und Ananas", "2,3,4,9,d", "8,50", "12,00"),
    ("050", "Pizza Tonno", "mit Tomatensauce, Käse, Thunfisch und Zwiebeln", "", "8,50", "12,00"),
    ("051", "Pizza Capriccio", "mit Tomatensauce, Käse, Salami, Schinken, Peperoniwurst, frischen Pilzen, Zwiebeln, Paprika und Oliven", "2,3,4,6,9", "9,50", "13,50"),
    ("052", "Pizza Maestro", "mit Tomatensauce, Käse, Schinken, Kapern, frischen Pilzen und Eiern", "2,3,4,9", "9,00", "12,50"),
    ("053", "Pizza 4 Jahreszeiten", "mit Tomatensauce, Käse, Salami, Schinken, frischen Pilzen und Oliven", "2,3,4,6,9", "8,50", "12,50"),
    ("054", "Pizza Frutti di Mare", "mit Tomatensauce, Käse und Meeresfrüchten", "g,h", "9,00", "13,00"),
    ("055", "Pizza Mozzarella", "mit Tomatensauce, Käse, Mozzarella und frischem Basilikum", "", "8,50", "12,00"),
    ("056", "Pizza Bolognese", "mit Käse, Hackfleischsauce, Schinken, Salami, frischen Pilzen und Knoblauch", "2,3,4,9", "9,00", "12,50"),
    ("057", "Pizza Pecora", "mit Tomatensauce, Käse, Schinken, Pfifferlingen und Schafskäse", "2,3,4,9", "8,50", "12,00"),
    ("058", "Pizza Bella", "mit Tomatensauce, Käse, Salami, Schinken, frischen Pilzen, Spinat, Broccoli und Knoblauch", "", "9,00", "13,00"),
    ("059", "Pizza Diyavolo", "mit Tomatensauce, Käse, Peperoniwurst, frischen Pilzen und scharfen Peperoni", "2,3,4", "8,50", "12,00"),
    ("060", "Pizza Calabria", "mit Tomatensauce, Käse, Schinken, frischen Pilzen und Artischocken", "2,3,4,9", "8,50", "12,00"),
    ("061", "Pizza Calzone (Teigtasche)", "mit Tomatensauce, Käse, Schinken, Salami und Zwiebeln", "2,3,4,9", "8,50", "12,00"),
    ("062", "Pizza Mafiosa", "mit Tomatensauce, Käse, Thunfisch, Erbsen, Mais, Knoblauch und scharfen Peperoni", "", "9,00", "12,50"),
    ("063", "Pizza Calimero", "mit Tomatensauce, Käse, Shrimps, Sardellen, frischen Pilzen, Zwiebeln, Kapern und Oliven", "6,9,h", "9,50", "13,00"),
    ("064", "Pizza Ravenna", "mit Hackfleischsauce, Käse und Zwiebeln", "6", "8,50", "12,00"),
    ("065", "Pizza Florida", "mit Tomatensauce, Käse, Hähnchenbrust, Mais, frischen Pilzen und viel Käse", "2,3,9,d", "9,00", "12,50"),
    ("066", "Pizza Istanbul", "mit Tomatensauce, Käse, Knoblauchwurst, frischen Pilzen und scharfen Peperoni", "2,3,4", "8,50", "12,00"),
    ("067", "Pizza Greco", "mit Tomatensauce, Käse, Knoblauchwurst, Oliven, Schafskäse und Zwiebeln", "", "9,00", "12,50"),
    ("068", "Pizza Krabben", "mit Tomatensauce, Käse, Krabben und Knoblauch", "9,h", "9,00", "12,50"),
    ("069", "Pizza quattro Formaggio", "mit Tomatensauce und 4 verschiedenen Käsesorten", "", "9,50", "13,00"),
    ("070", "Pizza Spezial", "mit Tomatensauce, Käse, Salami, Schinken und frischen Pilzen", "", "8,50", "12,00"),
    ("071", "Pizza Con Tonno", "mit Tomatensauce, Käse, Thunfisch, Pilzen, scharf", "", "8,50", "12,00"),
    ("072", "Pizza Frühstück", "mit Tomatensauce, Käse, Schinken und 2 Spiegeleiern", "2,3,4,9", "8,50", "12,00"),
    ("073", "Pizza Rucola", "mit Tomatensauce, Mozzarella und Rucolasalat", "", "8,50", "12,00"),
    ("074", "Pizza-Brot mit Knoblauch", "knusprig gebackenes Brot", "", "5,00", "7,00"),
    ("075", "Pizza Familia Ø 40 cm", "3 Beilagen nach Wahl", "", "19,00", None),
    ("076", "Bruscetta", "", "", "6,00", "7,50"),
]

EXTRAS = ("Knoblauch, Schinken, Peperoniwurst, Artischocken, Sardellen, Thunfisch, "
          "Champignons, Spinat, Broccoli, Käse, Zwiebeln, Paprika, Peperoni, Kapern, "
          "Oliven, Ei, Hähnchenbrust und mehr")

ZUSATZSTOFFE = [
    ("1", "Farbstoff"), ("2", "Konservierungsstoff"), ("3", "Antioxidationsmittel"),
    ("4", "Geschmacksverstärker"), ("5", "Schwefeldioxid/Sulfite"), ("6", "Eisensalz"),
    ("7", "geschwärzt"), ("8", "Süßstoff"), ("9", "Phosphat"),
]

ALLERGENE = [
    ("a", "glutenhaltiges Getreide"), ("b", "Eier"), ("c", "Milch"), ("d", "Sellerie"),
    ("e", "Senf"), ("f", "Schwefeldioxid"), ("g", "Weichtiere"), ("h", "Krebstiere"),
]


# =====================================================================
#  BESTELLFUNKTION
# =====================================================================

# --- Groessen je Kategorie -------------------------------------------
GROESSEN = {
    "salate": [("normal", "Normal"), ("gross", "Groß")],
    "pasta":  [("normal", "Normal"), ("gross", "Groß")],
    "pizza":  [("26", "ø 26 cm"), ("30", "ø 30 cm")],
    "getraenke": [("liter", "1,0 l Flasche"), ("glas", "0,33 l Glas")],
}

# --- Extra-Zutaten ----------------------------------------------------
# Pizza: Aufpreis laut gedruckter Karte, ø 26 cm = 0,50 EUR, ø 30 cm = 1,00 EUR
# Pasta und Salat: 1,00 EUR pauschal. Steht NICHT auf der Karte, ist von uns
# gesetzt. Vom Wirt bestaetigen lassen, siehe EXTRA_PREIS unten.
EXTRA_ZUTATEN = [
    "Knoblauch", "Schinken", "Salami", "Peperoniwurst", "Knoblauchwurst",
    "Artischocken", "Sardellen", "Thunfisch", "Champignons", "Spinat",
    "Broccoli", "Käse", "Mozzarella", "Schafskäse", "Zwiebeln", "Paprika",
    "Peperoni", "Kapern", "Oliven", "Mais", "Ananas", "Ei", "Hähnchenbrust",
]
EXTRA_PREIS = {"26": 0.50, "30": 1.00, "normal": 1.00, "gross": 1.00}
EXTRA_PREIS_PASTA_GESETZT = True   # auf False, sobald der Wirt die Preise nennt

# --- Bezahlte Zusatzoptionen bei Pasta und Salat ----------------------
# Nur was nachweislich auf der gedruckten Karte steht.
ZUSATZOPTIONEN = {
    "pasta":  [("ueberbacken", "Mit Käse überbacken", 1.00)],
    "salate": [("dressing", "Extra-Dressing", 1.00)],
}

# --- Kostenlose Weglass-Wuensche --------------------------------------
WEGLASSEN = ["Zwiebeln", "Knoblauch", "Käse", "Oliven", "Peperoni",
             "Pilze", "Sardellen", "Kapern", "Basilikum"]

# --- Getraenke ---------------------------------------------------------
# !!! PLATZHALTERPREISE !!!  Vom Wirt bestaetigen lassen, siehe README.
# Format: (Nr, Name, Beschreibung, Zusatzstoffe, Preis, None)
GETRAENKE = [
    # Sinalco in zwei Groessen: 1,0-l-Flasche 4,00 / 0,33-l-Glas 3,00
    ("G01", "Sinalco Cola",       "", "1",   "4,00", "3,00"),
    ("G02", "Sinalco Cola Zero",  "", "1,8", "4,00", "3,00"),
    ("G03", "Sinalco Orange",     "", "1",   "4,00", "3,00"),
    ("G04", "Sinalco Cola Mix",   "", "1",   "4,00", "3,00"),
    # Einzelgroessen
    ("G05", "Uludağ Gazoz",       "0,5 l Flasche",  "", "2,50", None),
    ("G06", "Körfez Ayran",       "0,25 l Becher",  "", "2,00", None),
    ("G07", "Rhönsprudel, mit Kohlensäure",  "0,5 l Flasche", "", "2,50", None),
    ("G08", "Rhönsprudel, ohne Kohlensäure", "0,5 l Flasche", "", "2,50", None),
]
GETRAENKE_PLATZHALTER = False  # Preise vom Wirt bestaetigt, September 2026

# --- Bestellablauf -----------------------------------------------------
MINDESTBESTELLWERT = 11.00     # nur bei Lieferung, laut Karte 2026
LIEFERGEBUEHR = 0.00           # in Hanau frei Haus


# --- Sonderfaelle -----------------------------------------------------
# Nr. 074 und 076 stehen auf der gedruckten Karte in den Pizzaspalten,
# sind aber keine Pizzen. Deshalb eigene Groessenbezeichnungen.
SONDERGROESSEN = {
    "074": [("26", "klein"), ("30", "groß")],
    "076": [("26", "klein"), ("30", "groß")],
}

# Hinweise, die im Konfigurator ueber den Optionen erscheinen
ARTIKEL_HINWEIS = {
    "075": "Bitte tragen Sie Ihre 3 Wunschbeilagen unten im Feld Sonderwunsch ein.",
}


# --- Schutz vor Fake- und Doppelbestellungen -------------------------
# Bewusst ohne Tageslimit und ohne Feiertagsliste, damit nichts gepflegt
# werden muss und an starken Tagen niemand ausgesperrt wird.
ANNAHMESCHLUSS = 0       # Minuten vor Ladenschluss, ab denen keine Bestellung mehr
                         # angenommen wird. 0 = bis zur letzten Minute.
                         # Beispiel: 20 bedeutet, ab 22:40 geht nichts mehr.
BESTELL_PAUSE = 90       # Sekunden zwischen zwei Bestellungen, gegen Doppelklicks
MINDESTVERWEILDAUER = 8  # Sekunden, die zwischen Seitenaufruf und Absenden liegen
                         # muessen. Menschen brauchen laenger, Skripte nicht.


# --- Gerichtefotos ----------------------------------------------------
# Datei nach assets/img/gerichte/ legen und hier die Nummer zuordnen.
# Gerichte ohne Eintrag erscheinen einfach ohne Bild, das faellt nicht auf.
# Empfohlen: quadratisch, 800 x 800 px, JPG mit etwa 75 Prozent.
BILDER = {
    "001": "001-gruener-salat.jpg",
    "002": "002-italienischer-salat.jpg",
    "004": "004-capricciosa-salat.jpg",
    "014": "014-spaghetti-carbonara.jpg",
    "016": "016-spaghetti-con-tonno.jpg",
    "017": "017-spaghetti-marinara.jpg",
    "018": "018-rigatoni-broccoli.jpg",
    "019": "019-rigatoni-al-forno.jpg",
    "020": "020-rigatoni-chef.jpg",
    "025": "025-tortellini-chef.jpg",
    "029": "029-tagliatelle-chef.jpg",
    "040": "040-pizza-margarita.jpg",
    "044": "044-pizza-mix.jpg",
    "050": "050-pizza-tonno.jpg",
    "055": "055-pizza-mozzarella.jpg",
    "060": "060-pizza-calabria.jpg",
    "066": "066-pizza-istanbul.jpg",
    "070": "070-pizza-spezial.jpg",
    "073": "073-pizza-rucola.jpg",
}

# Kleine Vorschaubilder in Speisekarte und Bestellliste.
# Auf Wunsch des Wirts aus, weil nur ein Teil der Gerichte Fotos hat und die
# Listen dadurch unruhig wirken. Im Bestellfenster bleibt das grosse Bild.
BILDER_IN_LISTE = False

# Reihenfolge der Bilder im Schaufenster auf der Startseite.
# Bewusst gemischt, damit nicht drei aehnliche Pizzen nebeneinander liegen.
SCHAUFENSTER = [
    # Alle Gerichte mit Foto, bewusst gemischt statt nach Kategorie sortiert,
    # damit nicht drei aehnliche Pizzen nebeneinander liegen.
    "017", "044", "002", "073",
    "020", "060", "004", "050",
    "014", "055", "001", "070",
    "025", "040", "016", "066",
    "029", "018", "019",
]
