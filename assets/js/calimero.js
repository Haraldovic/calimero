/* =========================================================
   Pizzeria Calimero, Hanau
   Kein Framework, keine externen Skripte, keine Tracker.
   ========================================================= */
(function () {
  "use strict";

  /* Zur Kontrolle beim Hochladen: in der Browserkonsole steht, welcher
     Build gerade laeuft. Passt der nicht zum hochgeladenen Stand, liegt
     eine alte Datei im Cache oder auf dem Server. */
  if (window.console) {
    console.log("Calimero-Website, Build " +
      (document.documentElement.getAttribute("data-build") || "unbekannt"));
  }

  /* ------------------------------------------------------------------
     1) KONFIGURATION  ->  HIER VOR DEM HOCHLADEN ANPASSEN
     ------------------------------------------------------------------
     WHATSAPP: Handynummer im internationalen Format, ohne + und ohne
     Leerzeichen. Beispiel fuer 0170 1234567  ->  "491701234567".
     Solange hier ein "X" steht, blendet die Seite alle WhatsApp-Buttons
     automatisch aus, damit kein toter Link online geht.
  ------------------------------------------------------------------ */
  var WHATSAPP = "491728664287";
  var WA_TEXT = "Hallo Calimero, ich möchte gerne bestellen:\n\n" +
                "Bestellung (bitte Nummern angeben):\n" +
                "- \n\n" +
                "Abholung oder Lieferung:\n" +
                "Adresse (bei Lieferung):\n" +
                "Wunschzeit:";

  /* ------------------------------------------------------------------
     Einblenden beim Scrollen. Einmalig, kein Zurueckblenden, damit es
     beim Hoch- und Runterscrollen nicht flackert. Respektiert die
     Systemeinstellung "Bewegung reduzieren".
  ------------------------------------------------------------------ */
  (function () {
    var ziele = document.querySelectorAll("[data-reveal]");
    if (!ziele.length) return;
    var ruhig = window.matchMedia &&
                window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (ruhig || !window.IntersectionObserver) {
      ziele.forEach(function (el) { el.classList.add("sichtbar"); });
      return;
    }
    /* Alles, was beim Laden schon im Bild ist, faehrt sofort gestaffelt ein.
       Sonst bliebe die Buehne unsichtbar, bis jemand scrollt. */
    var sofort = [];
    ziele.forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight - 20) sofort.push(el);
    });
    sofort.forEach(function (el) {
      var verzug = parseInt(el.getAttribute("data-reveal") || "0", 10) || 0;
      setTimeout(function () { el.classList.add("sichtbar"); }, verzug + 60);
    });

    var beobachter = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (!e.isIntersecting) return;
        var verzug = parseInt(e.target.getAttribute("data-reveal") || "0", 10) || 0;
        setTimeout(function () { e.target.classList.add("sichtbar"); }, verzug);
        beobachter.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    ziele.forEach(function (el) {
      if (sofort.indexOf(el) === -1) beobachter.observe(el);
    });
  })();

  /* Feine Linie unter dem Kopf erst zeigen, wenn gescrollt wurde */
  (function () {
    var kopf = document.querySelector(".kopf");
    if (!kopf) return;
    function pruefen() {
      kopf.setAttribute("data-gescrollt", window.scrollY > 12 ? "ja" : "nein");
    }
    pruefen();
    window.addEventListener("scroll", pruefen, { passive: true });
  })();

  /* ------------------------------------------------------------------
     Kopfhoehe messen und als CSS-Variable bereitstellen.
     Die Navigation bricht auf schmalen Displays um, dadurch aendert sich
     die Hoehe. Klebende Leisten und Sprungmarken richten sich danach.
  ------------------------------------------------------------------ */
  (function () {
    var kopf = document.querySelector(".kopf");
    if (!kopf) return;
    function messen() {
      var h = Math.round(kopf.getBoundingClientRect().height);
      document.documentElement.style.setProperty("--kopf-h", h + "px");
    }
    messen();
    window.addEventListener("resize", messen);
    if (window.ResizeObserver) new ResizeObserver(messen).observe(kopf);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(messen);
  })();

  /* Fuer die Bestellseite bereitstellen */
  window.CALIMERO_WHATSAPP = WHATSAPP;

  /* ---------- WhatsApp-Links setzen oder Buttons entfernen ---------- */
  var waLinks = document.querySelectorAll("[data-wa]");
  if (WHATSAPP.indexOf("X") > -1) {
    waLinks.forEach(function (el) { el.remove(); });
    if (window.console) {
      console.warn("Calimero: WhatsApp-Nummer noch nicht gesetzt. " +
        "In assets/js/calimero.js die Variable WHATSAPP eintragen, " +
        "dann erscheinen die WhatsApp-Buttons automatisch.");
    }
  } else {
    var href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(WA_TEXT);
    waLinks.forEach(function (el) {
      el.setAttribute("href", href);
      el.setAttribute("target", "_blank");
      el.setAttribute("rel", "noopener");
    });
  }

  /* ------------------------------------------------------------------
     2) OEFFNUNGSSTATUS
     Zeiten in Minuten seit Mitternacht, Zeitzone Europe/Berlin.
  ------------------------------------------------------------------ */
  var ZEITEN = {
    0: [[900, 1380]],                 // Sonntag 15:00 - 23:00
    1: [],                            // Montag Ruhetag
    2: [[690, 870], [1020, 1380]],    // Dienstag
    3: [[690, 870], [1020, 1380]],
    4: [[690, 870], [1020, 1380]],
    5: [[690, 870], [1020, 1380]],    // Freitag
    6: [[900, 1380]]                  // Samstag 15:00 - 23:00
  };
  var TAGE = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];

  function berlinJetzt() {
    try {
      var teile = new Intl.DateTimeFormat("de-DE", {
        timeZone: "Europe/Berlin", weekday: "short", year: "numeric",
        month: "2-digit", day: "2-digit", hour: "2-digit",
        minute: "2-digit", hour12: false
      }).formatToParts(new Date());
      var map = {};
      teile.forEach(function (t) { map[t.type] = t.value; });
      var kuerzel = { "So": 0, "Mo": 1, "Di": 2, "Mi": 3, "Do": 4, "Fr": 5, "Sa": 6 };
      var tag = kuerzel[map.weekday.replace(".", "").slice(0, 2)];
      return {
        tag: tag,
        minute: parseInt(map.hour, 10) * 60 + parseInt(map.minute, 10),
        datum: map.year + "-" + map.month + "-" + map.day
      };
    } catch (e) {
      var d = new Date();
      var z = function (n) { return (n < 10 ? "0" : "") + n; };
      return {
        tag: d.getDay(),
        minute: d.getHours() * 60 + d.getMinutes(),
        datum: d.getFullYear() + "-" + z(d.getMonth() + 1) + "-" + z(d.getDate())
      };
    }
  }

  /* ------------------------------------------------------------------
     Gesetzliche Feiertage in Hessen, jahresunabhaengig berechnet.
     Laut gedruckter Karte gelten an Feiertagen die Sonntagszeiten,
     also 15:00 bis 23:00 Uhr, auch wenn der Feiertag auf einen
     Montag faellt. Keine Liste, die gepflegt werden muss.
  ------------------------------------------------------------------ */
  var feiertagCache = {};

  function ostersonntag(jahr) {
    var a = jahr % 19, b = Math.floor(jahr / 100), c = jahr % 100;
    var d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25);
    var g = Math.floor((b - f + 1) / 3);
    var h = (19 * a + b - d - g + 15) % 30;
    var i = Math.floor(c / 4), k = c % 4;
    var l = (32 + 2 * e + 2 * i - h - k) % 7;
    var m = Math.floor((a + 11 * h + 22 * l) / 451);
    var monat = Math.floor((h + l - 7 * m + 114) / 31);
    var tag = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(Date.UTC(jahr, monat - 1, tag));
  }

  function feiertage(jahr) {
    if (feiertagCache[jahr]) return feiertagCache[jahr];
    function iso(d) {
      var z = function (n) { return (n < 10 ? "0" : "") + n; };
      return d.getUTCFullYear() + "-" + z(d.getUTCMonth() + 1) + "-" + z(d.getUTCDate());
    }
    function plus(d, tage) {
      return new Date(d.getTime() + tage * 86400000);
    }
    var o = ostersonntag(jahr);
    var liste = [
      jahr + "-01-01",              /* Neujahr */
      iso(plus(o, -2)),             /* Karfreitag */
      iso(plus(o, 1)),              /* Ostermontag */
      jahr + "-05-01",              /* Tag der Arbeit */
      iso(plus(o, 39)),             /* Christi Himmelfahrt */
      iso(plus(o, 50)),             /* Pfingstmontag */
      iso(plus(o, 60)),             /* Fronleichnam, in Hessen gesetzlich */
      jahr + "-10-03",              /* Tag der Deutschen Einheit */
      jahr + "-12-25",
      jahr + "-12-26"
    ];
    feiertagCache[jahr] = liste;
    return liste;
  }

  function istFeiertag(datum) {
    var jahr = parseInt(datum.slice(0, 4), 10);
    return feiertage(jahr).indexOf(datum) > -1;
  }

  /* Zeiten des heutigen Tages, Feiertage zaehlen als Sonntag */
  function zeitenHeute(jetzt) {
    if (istFeiertag(jetzt.datum)) return ZEITEN[0];
    return ZEITEN[jetzt.tag] || [];
  }

  function hhmm(m) {
    var h = Math.floor(m / 60), min = m % 60;
    return (h < 10 ? "0" : "") + h + ":" + (min < 10 ? "0" : "") + min;
  }

  /* Zeiten fuer den Tag in k Tagen, Feiertage beruecksichtigt */
  function naechsterTag(jetzt, k) {
    var d = new Date(jetzt.datum + "T12:00:00Z");
    d = new Date(d.getTime() + k * 86400000);
    var z = function (n) { return (n < 10 ? "0" : "") + n; };
    var datum = d.getUTCFullYear() + "-" + z(d.getUTCMonth() + 1) + "-" + z(d.getUTCDate());
    var wochentag = (jetzt.tag + k) % 7;
    var zeiten = istFeiertag(datum) ? ZEITEN[0] : (ZEITEN[wochentag] || []);
    return { datum: datum, tag: wochentag, zeiten: zeiten };
  }

  function statusText() {
    var jetzt = berlinJetzt();
    var heute = zeitenHeute(jetzt);
    for (var i = 0; i < heute.length; i++) {
      if (jetzt.minute >= heute[i][0] && jetzt.minute < heute[i][1]) {
        return { offen: true, text: "Jetzt geöffnet bis " + hhmm(heute[i][1]) + " Uhr" };
      }
    }
    for (var j = 0; j < heute.length; j++) {
      if (jetzt.minute < heute[j][0]) {
        return { offen: false, text: "Heute wieder ab " + hhmm(heute[j][0]) + " Uhr" };
      }
    }
    for (var k = 1; k <= 8; k++) {
      var t = (jetzt.tag + k) % 7;
      var z = naechsterTag(jetzt, k);
      if (z.zeiten.length) {
        var wann = (k === 1 ? "Morgen" : TAGE[t]) + " ab " + hhmm(z.zeiten[0][0]) + " Uhr";
        return { offen: false, text: "Geschlossen, " + wann.charAt(0).toLowerCase() + wann.slice(1) };
      }
    }
    return { offen: false, text: "Öffnungszeiten siehe unten" };
  }

  /* Fuer die Bestellseite bereitstellen */
  window.CalimeroZeit = {
    jetzt: berlinJetzt,
    zeiten: ZEITEN,
    status: statusText,
    hhmm: hhmm,
    /* Laeuft gerade das Mittagsangebot? Dienstag bis Freitag 11:30 - 14:30 */
    mittagsangebot: function () {
      var n = berlinJetzt();
      if (istFeiertag(n.datum)) return false;
      return n.tag >= 2 && n.tag <= 5 && n.minute >= 690 && n.minute < 870;
    },
    /* Naechste Oeffnung als lesbarer Text, oder null wenn gerade offen */
    istFeiertag: istFeiertag,
    /* true, wenn gerade bestellt werden darf */
    offen: function () {
      var n = berlinJetzt(), heute = zeitenHeute(n);
      for (var i = 0; i < heute.length; i++) {
        if (n.minute >= heute[i][0] && n.minute < heute[i][1] - (window.CALIMERO_ANNAHMESCHLUSS || 0)) {
          return true;
        }
      }
      return false;
    },
    naechsteOeffnung: function () {
      var n = berlinJetzt(), heute = zeitenHeute(n), i;
      for (i = 0; i < heute.length; i++) {
        if (n.minute >= heute[i][0] && n.minute < heute[i][1]) return null;
      }
      for (i = 0; i < heute.length; i++) {
        if (n.minute < heute[i][0]) return "heute ab " + hhmm(heute[i][0]) + " Uhr";
      }
      for (var k = 1; k <= 8; k++) {
        var n2 = naechsterTag(n, k);
        if (n2.zeiten.length) {
          return (k === 1 ? "morgen" : "am " + TAGE[n2.tag]) + " ab " + hhmm(n2.zeiten[0][0]) + " Uhr";
        }
      }
      return null;
    }
  };

  function statusZeichnen() {
    var s = statusText();
    document.querySelectorAll("[data-status]").forEach(function (el) {
      el.setAttribute("data-offen", s.offen ? "ja" : "nein");
      var ziel = el.querySelector("[data-status-text]") || el;
      ziel.textContent = s.text;
    });
    var tag = berlinJetzt().tag;
    document.querySelectorAll("[data-tag]").forEach(function (el) {
      var liste = el.getAttribute("data-tag").split(",");
      el.setAttribute("data-heute", liste.indexOf(String(tag)) > -1 ? "ja" : "nein");
    });
  }
  statusZeichnen();
  setInterval(statusZeichnen, 60000);

  /* ------------------------------------------------------------------
     3) SPEISEKARTE: Suche nach Nummer oder Name
  ------------------------------------------------------------------ */
  var feld = document.getElementById("karte-suche");
  if (feld) {
    var gerichte = Array.prototype.slice.call(document.querySelectorAll(".gericht"));
    var gruppen = Array.prototype.slice.call(document.querySelectorAll(".gruppe"));
    var leeren = document.querySelector(".suche__leeren");

    function normal(s) {
      return s.toLowerCase()
        .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
        .replace(/[„“"']/g, "");
    }
    gerichte.forEach(function (g) { g._suchtext = normal(g.textContent); });

    function filtern() {
      var q = normal(feld.value.trim());
      var treffer = 0;
      gerichte.forEach(function (g) {
        var passt = !q || g._suchtext.indexOf(q) > -1;
        g.hidden = !passt;
        if (passt) treffer++;
      });
      gruppen.forEach(function (gr) {
        var sichtbar = gr.querySelectorAll(".gericht:not([hidden])").length;
        gr.setAttribute("data-leer", sichtbar ? "nein" : "ja");
      });
      document.body.setAttribute("data-treffer", String(treffer));
      if (leeren) leeren.hidden = !feld.value;
    }
    feld.addEventListener("input", filtern);
    if (leeren) {
      leeren.hidden = true;
      leeren.addEventListener("click", function () { feld.value = ""; filtern(); feld.focus(); });
    }
  }

  /* ------------------------------------------------------------------
     4) EINWILLIGUNG + GOOGLE MAPS (Zwei-Klick)
     Speicherung nur lokal im Browser (localStorage), kein Drittanbieter.
  ------------------------------------------------------------------ */
  var SCHLUESSEL = "calimero-karte-einwilligung";

  function gespeichert() {
    try { return localStorage.getItem(SCHLUESSEL); } catch (e) { return null; }
  }
  function speichern(wert) {
    try { localStorage.setItem(SCHLUESSEL, wert); } catch (e) { /* egal */ }
  }

  function karteLaden() {
    document.querySelectorAll(".zweiklick").forEach(function (box) {
      if (box.querySelector("iframe")) return;
      var src = box.getAttribute("data-karte");
      if (!src) return;
      var frame = document.createElement("iframe");
      frame.src = src;
      frame.loading = "lazy";
      frame.title = "Karte mit dem Standort der Pizzeria Calimero, Heumarkt 6, Hanau";
      frame.setAttribute("referrerpolicy", "no-referrer-when-downgrade");
      frame.setAttribute("allowfullscreen", "");
      box.innerHTML = "";
      box.appendChild(frame);
    });
  }

  document.querySelectorAll("[data-karte-laden]").forEach(function (b) {
    b.addEventListener("click", function () { speichern("ja"); karteLaden(); });
  });

  /* Die Karteneinwilligung laeuft ausschliesslich ueber die Zwei-Klick-Flaeche
     an der Karte selbst. Frueher hing hier zusaetzlich ein Banner dran, das
     den Hinweiskasten auf jeder Seite wieder aufgeklappt hat. */
  if (gespeichert() === "ja") karteLaden();

  /* ------------------------------------------------------------------
     Hinweis zur Datenspeicherung.
     Wird einmal gezeigt und dann nie wieder. Gemerkt wird das doppelt:
     im localStorage und zusaetzlich als Cookie. Grund: In privaten
     Fenstern und bei strengen Browsereinstellungen schlaegt localStorage
     fehl, dann poppte der Hinweis bei jedem Seitenwechsel erneut auf.
  ------------------------------------------------------------------ */
  (function () {
    var kasten = document.getElementById("hinweis-speicher");
    if (!kasten) return;
    var SCHL = "calimero-hinweis-gelesen";

    function gemerkt() {
      try { if (localStorage.getItem(SCHL)) return true; } catch (e) {}
      return document.cookie.indexOf(SCHL + "=ja") > -1;
    }
    function merken() {
      try { localStorage.setItem(SCHL, "ja"); } catch (e) {}
      try {
        document.cookie = SCHL + "=ja; path=/; max-age=31536000; SameSite=Lax" +
          (location.protocol === "https:" ? "; Secure" : "");
      } catch (e) {}
    }

    if (!gemerkt()) {
      setTimeout(function () { kasten.hidden = false; }, 900);
    }
    kasten.querySelectorAll("[data-hinweis-ok]").forEach(function (b) {
      b.addEventListener("click", function () {
        kasten.hidden = true;
        merken();
      });
    });
  })();

  /* Widerruf, z. B. aus der Datenschutzerklaerung heraus */
  document.querySelectorAll("[data-consent-zuruecksetzen]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      try { localStorage.removeItem(SCHLUESSEL); } catch (err) { /* egal */ }
      b.textContent = "Einwilligung wurde zurückgesetzt.";
      b.setAttribute("disabled", "disabled");
    });
  });
})();
