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
        timeZone: "Europe/Berlin", weekday: "short", hour: "2-digit",
        minute: "2-digit", hour12: false
      }).formatToParts(new Date());
      var map = {};
      teile.forEach(function (t) { map[t.type] = t.value; });
      var kuerzel = { "So": 0, "Mo": 1, "Di": 2, "Mi": 3, "Do": 4, "Fr": 5, "Sa": 6 };
      var tag = kuerzel[map.weekday.replace(".", "").slice(0, 2)];
      return { tag: tag, minute: parseInt(map.hour, 10) * 60 + parseInt(map.minute, 10) };
    } catch (e) {
      var d = new Date();
      return { tag: d.getDay(), minute: d.getHours() * 60 + d.getMinutes() };
    }
  }

  function hhmm(m) {
    var h = Math.floor(m / 60), min = m % 60;
    return (h < 10 ? "0" : "") + h + ":" + (min < 10 ? "0" : "") + min;
  }

  function statusText() {
    var jetzt = berlinJetzt();
    var heute = ZEITEN[jetzt.tag] || [];
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
    for (var k = 1; k <= 7; k++) {
      var t = (jetzt.tag + k) % 7;
      var z = ZEITEN[t] || [];
      if (z.length) {
        var wann = (k === 1 ? "Morgen" : TAGE[t]) + " ab " + hhmm(z[0][0]) + " Uhr";
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
      return n.tag >= 2 && n.tag <= 5 && n.minute >= 690 && n.minute < 870;
    },
    /* Naechste Oeffnung als lesbarer Text, oder null wenn gerade offen */
    naechsteOeffnung: function () {
      var n = berlinJetzt(), heute = ZEITEN[n.tag] || [], i;
      for (i = 0; i < heute.length; i++) {
        if (n.minute >= heute[i][0] && n.minute < heute[i][1]) return null;
      }
      for (i = 0; i < heute.length; i++) {
        if (n.minute < heute[i][0]) return "heute ab " + hhmm(heute[i][0]) + " Uhr";
      }
      for (var k = 1; k <= 7; k++) {
        var t = (n.tag + k) % 7, z = ZEITEN[t] || [];
        if (z.length) {
          return (k === 1 ? "morgen" : "am " + TAGE[t]) + " ab " + hhmm(z[0][0]) + " Uhr";
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
