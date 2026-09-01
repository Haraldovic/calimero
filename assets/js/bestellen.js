/* =========================================================
   Pizzeria Calimero, Bestellfunktion
   Kein Server, kein Konto, keine Onlinezahlung.
   Die fertige Bestellung wird als Text an WhatsApp uebergeben.
   ========================================================= */
(function () {
  "use strict";

  var K = {};                 // Menuedaten aus menu.json
  var korb = [];              // Warenkorb
  var SPEICHER = "calimero-warenkorb";
  var entwurf = null;         // gerade konfigurierter Artikel

  var el = {
    liste:    document.getElementById("artikel-liste"),
    tabs:     document.getElementById("kat-tabs"),
    suche:    document.getElementById("artikel-suche"),
    leiste:   document.getElementById("korb-leiste"),
    leisteN:  document.getElementById("korb-anzahl"),
    leisteS:  document.getElementById("korb-summe"),
    overlay:  document.getElementById("overlay"),
    panel:    document.getElementById("overlay-panel")
  };

  /* ---------------------------------------------------- Hilfsfunktionen */
  function eur(n) { return n.toFixed(2).replace(".", ",") + " €"; }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function normal(s) {
    return String(s).toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe")
      .replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[„“"']/g, "");
  }

  function korbLaden() {
    try {
      var r = localStorage.getItem(SPEICHER);
      if (r) korb = JSON.parse(r) || [];
    } catch (e) { korb = []; }
  }
  function korbSichern() {
    try { localStorage.setItem(SPEICHER, JSON.stringify(korb)); } catch (e) {}
  }

  function summe() {
    return korb.reduce(function (s, p) { return s + p.preis * p.menge; }, 0);
  }
  function anzahl() {
    return korb.reduce(function (s, p) { return s + p.menge; }, 0);
  }

  /* ---------------------------------------------------- Startseite Liste */
  var aktiveKat = null;

  function tabsZeichnen() {
    el.tabs.innerHTML = K.kategorien.map(function (k, i) {
      return '<button type="button" class="kat-tab" data-kat="' + k.id + '"' +
             (i === 0 ? ' aria-pressed="true"' : ' aria-pressed="false"') + '>' +
             esc(k.name) + "</button>";
    }).join("");
    aktiveKat = K.kategorien[0].id;
    el.tabs.addEventListener("click", function (e) {
      var b = e.target.closest(".kat-tab");
      if (!b) return;
      aktiveKat = b.getAttribute("data-kat");
      el.tabs.querySelectorAll(".kat-tab").forEach(function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      if (el.suche) el.suche.value = "";
      listeZeichnen();
      var y = el.liste.getBoundingClientRect().top + window.scrollY - 150;
      window.scrollTo({ top: y, behavior: "smooth" });
    });
  }

  function listeZeichnen() {
    var q = el.suche ? normal(el.suche.value.trim()) : "";
    var artikel = K.artikel.filter(function (a) {
      if (q) return normal(a.nr + " " + a.name + " " + a.desc).indexOf(q) > -1;
      return a.kat === aktiveKat;
    });

    if (!artikel.length) {
      el.liste.innerHTML = '<p class="kein-treffer" style="display:block">' +
        "Dazu haben wir nichts gefunden. Rufen Sie uns gerne an.</p>";
      return;
    }

    el.liste.innerHTML = artikel.map(function (a) {
      var preise = Object.keys(a.preise).map(function (g) { return a.preise[g]; });
      var ab = Math.min.apply(null, preise);
      var mehrere = preise.length > 1;
      return '<button type="button" class="best-artikel" data-id="' + a.id + '">' +
        '<span class="best-artikel__nr">' + esc(a.nr) + "</span>" +
        '<span class="best-artikel__mitte">' +
          '<span class="best-artikel__name">' + esc(a.name) + "</span>" +
          (a.desc ? '<span class="best-artikel__desc">' + esc(a.desc) + "</span>" : "") +
        "</span>" +
        '<span class="best-artikel__preis">' + (mehrere ? "ab " : "") + eur(ab) + "</span>" +
        "</button>";
    }).join("");
  }

  /* ---------------------------------------------------- Overlay-Grundlage */
  var zuletztFokus = null;

  function overlayAuf(html) {
    zuletztFokus = document.activeElement;
    el.panel.innerHTML = html;
    el.overlay.hidden = false;
    document.body.style.overflow = "hidden";
    var f = el.panel.querySelector("input, button, select, textarea");
    if (f) f.focus();
    el.panel.scrollTop = 0;
  }
  function overlayZu() {
    el.overlay.hidden = true;
    el.panel.innerHTML = "";
    document.body.style.overflow = "";
    entwurf = null;
    if (zuletztFokus && zuletztFokus.focus) zuletztFokus.focus();
  }
  el.overlay.addEventListener("click", function (e) {
    if (e.target === el.overlay || e.target.closest("[data-zu]")) overlayZu();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !el.overlay.hidden) overlayZu();
  });

  /* ---------------------------------------------------- Artikel konfigurieren */
  function artikelOeffnen(id) {
    var a = K.artikel.filter(function (x) { return x.id === id; })[0];
    if (!a) return;
    var kat = K.kategorien.filter(function (k) { return k.id === a.kat; })[0];
    var groessen = Object.keys(a.preise);

    entwurf = {
      id: a.id, nr: a.nr, name: a.name, kat: a.kat,
      groesse: groessen[0], menge: 1, extras: [], optionen: [], ohne: [], notiz: ""
    };

    var html = '<div class="konfig">';
    html += '<button class="overlay__zu" type="button" data-zu aria-label="Schließen">×</button>';
    html += "<h2>" + esc(a.nr) + " " + esc(a.name) + "</h2>";
    if (a.desc) html += '<p class="konfig__desc">' + esc(a.desc) + "</p>";
    if (a.codes) html += '<p class="konfig__codes">Zusatzstoffe / Allergene: ' + esc(a.codes) +
      ' <a href="speisekarte.html#legende" target="_blank" rel="noopener">Was bedeutet das?</a></p>';
    if (a.hinweis) html += '<div class="hinweis" style="margin:.9rem 0 0"><p>' +
      esc(a.hinweis) + "</p></div>";

    /* Groesse */
    if (groessen.length > 1) {
      html += '<fieldset class="konfig__block"><legend>Größe</legend><div class="wahl">';
      groessen.forEach(function (g, i) {
        var label = groesseLabel(a, g);
        html += '<label class="wahl__opt"><input type="radio" name="groesse" value="' + g + '"' +
          (i === 0 ? " checked" : "") + '><span>' + esc(label) +
          '<b>' + eur(a.preise[g]) + "</b></span></label>";
      });
      html += "</div></fieldset>";
    }

    /* Bezahlte Extras, nur wo Preise dokumentiert sind */
    var extraPreis = K.extras.preise[groessen[0]];
    if (kat.extras && K.extras.liste.length && extraPreis !== undefined) {
      html += '<fieldset class="konfig__block"><legend>Extra-Zutaten</legend>' +
        (function () {
          var p1 = K.extras.preise[groessen[0]], p2 = K.extras.preise[groessen[1]];
          if (groessen.length < 2 || p1 === p2) {
            return '<p class="konfig__hint">Aufpreis je Zutat: ' + eur(p1) + ".</p>";
          }
          return '<p class="konfig__hint">Aufpreis je Zutat: ' + eur(p1) + " bei " +
                 esc(groesseLabel(a, groessen[0])) + ", " + eur(p2) + " bei " +
                 esc(groesseLabel(a, groessen[1])) + ".</p>";
        })() + '<div class="wahl wahl--eng">';
      K.extras.liste.forEach(function (z) {
        html += '<label class="wahl__opt"><input type="checkbox" name="extra" value="' +
          esc(z) + '"><span>' + esc(z) + "</span></label>";
      });
      html += "</div></fieldset>";
    }

    /* Dokumentierte Zusatzoptionen bei Pasta und Salat */
    var opts = K.zusatzoptionen[a.kat] || [];
    if (opts.length) {
      html += '<fieldset class="konfig__block"><legend>Extras</legend><div class="wahl">';
      opts.forEach(function (o) {
        html += '<label class="wahl__opt"><input type="checkbox" name="option" value="' +
          esc(o[0]) + '" data-preis="' + o[2] + '" data-label="' + esc(o[1]) +
          '"><span>' + esc(o[1]) + "<b>+" + eur(o[2]) + "</b></span></label>";
      });
      html += "</div></fieldset>";
    }

    /* Weglassen, kostenlos */
    if (a.kat !== "getraenke") {
      html += '<fieldset class="konfig__block"><legend>Bitte weglassen</legend>' +
        '<p class="konfig__hint">Kostenlos. Nur was im Gericht enthalten ist, kann weggelassen werden.</p>' +
        '<div class="wahl wahl--eng">';
      K.weglassen.forEach(function (w) {
        html += '<label class="wahl__opt"><input type="checkbox" name="ohne" value="' +
          esc(w) + '"><span>ohne ' + esc(w) + "</span></label>";
      });
      html += "</div></fieldset>";

      html += '<fieldset class="konfig__block"><legend>Sonderwunsch</legend>' +
        '<textarea id="konfig-notiz" rows="2" maxlength="140" ' +
        'placeholder="z. B. gut durchgebacken, halb scharf"></textarea>' +
        '<p class="konfig__hint">Wünsche, die einen Aufpreis auslösen, nennen wir Ihnen ' +
        "bei der Bestätigung.</p></fieldset>";
    }

    html += '<div class="konfig__fuss">' +
      '<div class="menge"><button type="button" data-menge="-" aria-label="weniger">−</button>' +
      '<output id="konfig-menge">1</output>' +
      '<button type="button" data-menge="+" aria-label="mehr">+</button></div>' +
      '<button class="knopf knopf--dunkel konfig__add" type="button" id="konfig-add">' +
      'In den Warenkorb <b id="konfig-preis"></b></button></div>';

    html += "</div>";
    overlayAuf(html);
    konfigPreis();

    el.panel.addEventListener("change", konfigPreis);
    el.panel.addEventListener("input", konfigPreis);
    el.panel.querySelectorAll("[data-menge]").forEach(function (b) {
      b.addEventListener("click", function () {
        entwurf.menge = Math.max(1, Math.min(30,
          entwurf.menge + (b.getAttribute("data-menge") === "+" ? 1 : -1)));
        document.getElementById("konfig-menge").textContent = entwurf.menge;
        konfigPreis();
      });
    });
    document.getElementById("konfig-add").addEventListener("click", function () {
      konfigPreis();
      korb.push(JSON.parse(JSON.stringify(entwurf)));
      korbSichern();
      leisteZeichnen();
      overlayZu();
    });
  }

  function konfigPreis() {
    if (!entwurf) return;
    var a = K.artikel.filter(function (x) { return x.id === entwurf.id; })[0];
    var g = el.panel.querySelector('input[name="groesse"]:checked');
    entwurf.groesse = g ? g.value : Object.keys(a.preise)[0];

    entwurf.extras = Array.prototype.map.call(
      el.panel.querySelectorAll('input[name="extra"]:checked'), function (x) { return x.value; });
    entwurf.optionen = Array.prototype.map.call(
      el.panel.querySelectorAll('input[name="option"]:checked'), function (x) {
        return { label: x.getAttribute("data-label"), preis: parseFloat(x.getAttribute("data-preis")) };
      });
    entwurf.ohne = Array.prototype.map.call(
      el.panel.querySelectorAll('input[name="ohne"]:checked'), function (x) { return x.value; });
    var n = document.getElementById("konfig-notiz");
    entwurf.notiz = n ? n.value.trim() : "";

    var p = a.preise[entwurf.groesse];
    p += entwurf.extras.length * (K.extras.preise[entwurf.groesse] || 0);
    entwurf.optionen.forEach(function (o) { p += o.preis; });
    entwurf.preis = Math.round(p * 100) / 100;
    entwurf.groesseLabel = groesseLabel(a, entwurf.groesse);

    var out = document.getElementById("konfig-preis");
    if (out) out.textContent = eur(entwurf.preis * entwurf.menge);
  }

  function groesseLabel(a, g) {
    if (g === "standard") return "";
    var quelle = a.groessen;
    if (!quelle) {
      var k = K.kategorien.filter(function (x) { return x.id === a.kat; })[0];
      quelle = k && k.groessen;
    }
    if (!quelle) return "";
    var t = quelle.filter(function (x) { return x[0] === g; })[0];
    return t ? t[1] : "";
  }

  /* ---------------------------------------------------- Warenkorbleiste */
  function leisteZeichnen() {
    var n = anzahl();
    el.leiste.hidden = n === 0;
    el.leisteN.textContent = n + (n === 1 ? " Artikel" : " Artikel");
    el.leisteS.textContent = eur(summe());
    document.body.setAttribute("data-korb", n ? "voll" : "leer");
  }

  /* ---------------------------------------------------- Warenkorb */
  function zeileText(p) {
    var t = [];
    if (p.groesseLabel) t.push(p.groesseLabel);
    if (p.extras.length) t.push("+ " + p.extras.join(", "));
    p.optionen.forEach(function (o) { t.push("+ " + o.label); });
    if (p.ohne.length) t.push("ohne " + p.ohne.join(", "));
    if (p.notiz) t.push("„" + p.notiz + "“");
    return t.join(" · ");
  }

  function korbOeffnen() {
    if (!korb.length) return;
    var html = '<div class="korb">';
    html += '<button class="overlay__zu" type="button" data-zu aria-label="Schließen">×</button>';
    html += "<h2>Ihre Bestellung</h2>";
    html += '<ul class="korb__liste">';
    korb.forEach(function (p, i) {
      html += '<li class="korb__zeile">' +
        '<span class="korb__menge">' + p.menge + "×</span>" +
        '<span class="korb__mitte"><b>' + esc(p.nr) + " " + esc(p.name) + "</b>" +
        (zeileText(p) ? '<span class="korb__detail">' + esc(zeileText(p)) + "</span>" : "") +
        '<span class="korb__aktionen">' +
          '<button type="button" data-minus="' + i + '">weniger</button>' +
          '<button type="button" data-plus="' + i + '">mehr</button>' +
          '<button type="button" data-weg="' + i + '">entfernen</button>' +
        "</span></span>" +
        '<span class="korb__preis">' + eur(p.preis * p.menge) + "</span></li>";
    });
    html += "</ul>";
    html += '<p class="korb__summe"><span>Zwischensumme</span><b>' + eur(summe()) + "</b></p>";
    html += '<div class="konfig__fuss">' +
      '<button class="knopf knopf--rand" type="button" data-zu>Weiter bestellen</button>' +
      '<button class="knopf knopf--dunkel" type="button" id="zur-kasse">Zur Bestellung</button>' +
      "</div></div>";
    overlayAuf(html);

    el.panel.querySelectorAll("[data-plus],[data-minus],[data-weg]").forEach(function (b) {
      b.addEventListener("click", function () {
        var i = parseInt(b.getAttribute("data-plus") || b.getAttribute("data-minus") ||
                         b.getAttribute("data-weg"), 10);
        if (b.hasAttribute("data-plus")) korb[i].menge = Math.min(30, korb[i].menge + 1);
        else if (b.hasAttribute("data-minus")) {
          korb[i].menge -= 1;
          if (korb[i].menge < 1) korb.splice(i, 1);
        } else korb.splice(i, 1);
        korbSichern(); leisteZeichnen();
        if (korb.length) korbOeffnen(); else overlayZu();
      });
    });
    document.getElementById("zur-kasse").addEventListener("click", kasseOeffnen);
  }

  /* ---------------------------------------------------- Kasse */
  function kasseOeffnen() {
    var gebiete = K.liefergebiete.map(function (g) {
      return '<option value="' + esc(g) + '">' + esc(g) + "</option>";
    }).join("");

    var html = '<div class="kasse">';
    html += '<button class="overlay__zu" type="button" data-zu aria-label="Schließen">×</button>';
    html += "<h2>Bestellung abschließen</h2>";

    html += '<fieldset class="konfig__block"><legend>Abholung oder Lieferung</legend><div class="wahl">' +
      '<label class="wahl__opt"><input type="radio" name="art" value="abholung" checked>' +
      "<span>Selbst abholen<b>Heumarkt 6</b></span></label>" +
      '<label class="wahl__opt"><input type="radio" name="art" value="lieferung">' +
      "<span>Liefern lassen<b>frei Haus in Hanau</b></span></label></div></fieldset>";

    html += '<fieldset class="konfig__block"><legend>Ihre Angaben</legend>' +
      '<label class="feld"><span>Name</span><input id="f-name" type="text" autocomplete="name" required></label>' +
      '<label class="feld"><span>Telefonnummer für Rückfragen</span>' +
      '<input id="f-tel" type="tel" inputmode="tel" autocomplete="tel" required></label>' +
      '<div id="lieferfelder" hidden>' +
        '<label class="feld"><span>Straße und Hausnummer</span>' +
        '<input id="f-strasse" type="text" autocomplete="street-address"></label>' +
        '<label class="feld"><span>Stadtteil</span><select id="f-gebiet">' + gebiete + "</select></label>" +
      "</div>" +
      '<label class="feld"><span>Wunschzeit</span>' +
      '<input id="f-zeit" type="text" placeholder="so schnell wie möglich" maxlength="40"></label>' +
      "</fieldset>";

    html += '<fieldset class="konfig__block"><legend>Zahlung bei Übergabe</legend><div class="wahl">' +
      '<label class="wahl__opt"><input type="radio" name="zahlung" value="bar" checked><span>Bar</span></label>' +
      '<label class="wahl__opt"><input type="radio" name="zahlung" value="karte"><span>EC-Karte</span></label>' +
      '</div><p class="konfig__hint" id="karte-hinweis">EC-Karte ist nur vor Ort im Laden möglich.</p></fieldset>';

    html += '<label class="feld"><span>Anmerkung zur Bestellung</span>' +
      '<textarea id="f-notiz" rows="2" maxlength="200" placeholder="z. B. Klingel defekt, bitte anrufen"></textarea></label>';

    html += '<div class="kasse__summe" id="kasse-summe"></div>';
    html += '<p class="kasse__recht">Alle Preise verstehen sich inklusive Mehrwertsteuer. ' +
      'Angaben zu Zusatzstoffen und Allergenen finden Sie in der ' +
      '<a href="speisekarte.html#legende" target="_blank" rel="noopener">Speisekarte</a>. ' +
      'Mit dem Absenden geben Sie ein verbindliches Angebot ab. Der Vertrag kommt erst ' +
      'mit unserer Bestätigung zustande. Es gelten unsere ' +
      '<a href="bestellbedingungen.html" target="_blank" rel="noopener">Bestellbedingungen</a> ' +
      'und die <a href="datenschutz.html" target="_blank" rel="noopener">Datenschutzerklärung</a>.</p>';

    html += '<p class="kasse__fehler" id="kasse-fehler" hidden></p>';
    html += '<div class="konfig__fuss konfig__fuss--statisch">' +
      '<button class="knopf knopf--rand" type="button" id="zurueck-korb">Zurück</button>' +
      '<button class="knopf knopf--dunkel" type="button" id="absenden">zahlungspflichtig bestellen</button>' +
      "</div></div>";

    overlayAuf(html);

    function artWechsel() {
      var lief = el.panel.querySelector('input[name="art"]:checked').value === "lieferung";
      document.getElementById("lieferfelder").hidden = !lief;
      var karte = el.panel.querySelector('input[name="zahlung"][value="karte"]');
      document.getElementById("karte-hinweis").hidden = !lief;
      if (lief && karte.checked) el.panel.querySelector('input[name="zahlung"][value="bar"]').checked = true;
      karte.disabled = lief;
      summeZeichnen();
    }
    function summeZeichnen() {
      var lief = el.panel.querySelector('input[name="art"]:checked').value === "lieferung";
      var s = summe();
      var h = '<p><span>Zwischensumme</span><b>' + eur(s) + "</b></p>";
      if (lief) h += '<p><span>Lieferung in Hanau</span><b>' +
        (K.liefergebuehr ? eur(K.liefergebuehr) : "frei Haus") + "</b></p>";
      h += '<p class="kasse__gesamt"><span>Gesamtpreis</span><b>' +
        eur(s + (lief ? K.liefergebuehr : 0)) + "</b></p>";
      if (lief && s < K.mindest) {
        h += '<p class="kasse__warnung">Mindestbestellwert für Lieferung: ' + eur(K.mindest) +
          ". Es fehlen noch " + eur(K.mindest - s) + ".</p>";
      }
      document.getElementById("kasse-summe").innerHTML = h;
    }
    el.panel.querySelectorAll('input[name="art"]').forEach(function (r) {
      r.addEventListener("change", artWechsel);
    });
    artWechsel();

    document.getElementById("zurueck-korb").addEventListener("click", korbOeffnen);
    document.getElementById("absenden").addEventListener("click", absenden);
  }

  /* ---------------------------------------------------- Absenden */
  function absenden() {
    var f = document.getElementById("kasse-fehler");
    var lief = el.panel.querySelector('input[name="art"]:checked').value === "lieferung";
    var d = {
      art: lief ? "Lieferung" : "Abholung",
      name: document.getElementById("f-name").value.trim(),
      tel: document.getElementById("f-tel").value.trim(),
      strasse: lief ? document.getElementById("f-strasse").value.trim() : "",
      gebiet: lief ? document.getElementById("f-gebiet").value : "",
      zeit: document.getElementById("f-zeit").value.trim() || "so schnell wie möglich",
      zahlung: el.panel.querySelector('input[name="zahlung"]:checked').value === "karte"
               ? "EC-Karte" : "bar",
      notiz: document.getElementById("f-notiz").value.trim()
    };

    var fehler = [];
    if (d.name.length < 2) fehler.push("Bitte tragen Sie Ihren Namen ein.");
    if (d.tel.replace(/\D/g, "").length < 6) fehler.push("Bitte tragen Sie eine Telefonnummer ein.");
    if (lief && d.strasse.length < 4) fehler.push("Bitte tragen Sie Straße und Hausnummer ein.");
    if (lief && summe() < K.mindest) fehler.push("Der Mindestbestellwert für Lieferung beträgt " + eur(K.mindest) + ".");
    if (fehler.length) {
      f.hidden = false;
      f.textContent = fehler[0];
      f.scrollIntoView({ block: "center" });
      return;
    }
    f.hidden = true;

    var pin = String(Math.floor(1000 + Math.random() * 9000));
    var gesamt = summe() + (lief ? K.liefergebuehr : 0);
    var text = nachrichtBauen(pin, d, gesamt);
    fertigOeffnen(pin, d, gesamt, text);
  }

  /* Zwei Formate: lesefreundlich mit Emojis, und ein kompaktes fuer den Fall,
     dass die WhatsApp-URL zu lang wird (grosse Bestellungen). Emojis und
     Zeilenumbrueche werden in der URL mehrfach kodiert, deshalb die Pruefung. */
  var URL_GRENZE = 1700;

  function nachrichtBauen(pin, d, gesamt) {
    var lang = nachrichtSchoen(pin, d, gesamt);
    if (encodeURIComponent(lang).length <= URL_GRENZE) return lang;
    return nachrichtKompakt(pin, d, gesamt);
  }

  function nachrichtSchoen(pin, d, gesamt) {
    var z = ["🍕 *BESTELLUNG " + pin + "*", "Pizzeria Calimero", ""];

    korb.forEach(function (p) {
      z.push("*" + p.menge + "×* " + p.nr + " " + p.name +
             (p.groesseLabel ? " _(" + p.groesseLabel + ")_" : ""));
      if (p.extras.length) z.push("➕ " + p.extras.join(", "));
      p.optionen.forEach(function (o) { z.push("➕ " + o.label); });
      if (p.ohne.length) z.push("➖ ohne " + p.ohne.join(", "));
      if (p.notiz) z.push("✏️ " + p.notiz);
      z.push("= " + eur(p.preis * p.menge));
      z.push("");
    });

    z.push("💶 *GESAMT: " + eur(gesamt) + "*");
    z.push("💵 Zahlung: " + d.zahlung + " bei Übergabe");
    z.push("");
    z.push((d.art === "Lieferung" ? "🚗 *LIEFERUNG*" : "🏠 *ABHOLUNG*"));
    z.push("👤 " + d.name);
    z.push("📞 " + d.tel);
    if (d.art === "Lieferung") z.push("📍 " + d.strasse + ", " + d.gebiet);
    z.push("🕐 " + d.zeit);
    if (d.notiz) z.push("📝 " + d.notiz);
    return z.join("\n");
  }

  function nachrichtKompakt(pin, d, gesamt) {
    var z = ["BESTELLUNG " + pin + " / Pizzeria Calimero", ""];
    korb.forEach(function (p) {
      z.push(p.menge + "x " + p.nr + " " + p.name +
             (p.groesseLabel ? " (" + p.groesseLabel + ")" : "") +
             " = " + eur(p.preis * p.menge).replace(" €", ""));
      var d2 = [];
      if (p.extras.length) d2.push("+ " + p.extras.join(", "));
      p.optionen.forEach(function (o) { d2.push("+ " + o.label); });
      if (p.ohne.length) d2.push("ohne " + p.ohne.join(", "));
      if (p.notiz) d2.push(p.notiz);
      if (d2.length) z.push("   " + d2.join(" | "));
    });
    z.push("");
    z.push("GESAMT: " + eur(gesamt).replace(" €", " EUR"));
    z.push("Zahlung: " + d.zahlung + " bei Übergabe");
    z.push(d.art.toUpperCase());
    z.push(d.name + ", Tel " + d.tel);
    if (d.art === "Lieferung") z.push(d.strasse + ", " + d.gebiet);
    z.push("Zeit: " + d.zeit);
    if (d.notiz) z.push("Hinweis: " + d.notiz);
    return z.join("\n");
  }

  function fertigOeffnen(pin, d, gesamt, text) {
    var nummer = window.CALIMERO_WHATSAPP || "";
    var waOk = nummer && nummer.indexOf("X") === -1;
    var waLink = waOk ? "https://wa.me/" + nummer + "?text=" + encodeURIComponent(text) : "";

    var html = '<div class="fertig">';
    html += '<button class="overlay__zu" type="button" data-zu aria-label="Schließen">×</button>';
    html += '<p class="fertig__pin"><span>Ihre Bestellnummer</span><b>' + pin + "</b></p>";
    html += "<h2>Fast geschafft</h2>";
    html += "<p>Ihre Bestellung ist noch nicht bei uns. Sie öffnet sich jetzt als fertige " +
      "Nachricht in WhatsApp, dort müssen Sie nur noch auf Senden tippen. " +
      "Wir bestätigen Ihnen anschließend die Lieferzeit im selben Chat.</p>";
    /* In der Vorschau die WhatsApp-Formatzeichen ausblenden, gesendet
       wird der Text mit Auszeichnung, damit WhatsApp fett darstellt. */
    var vorschau = text.replace(/\*(.+?)\*/g, "$1").replace(/_(.+?)_/g, "$1");
    html += '<pre class="fertig__text">' + esc(vorschau) + "</pre>";
    html += '<div class="fertig__tasten">';
    if (waOk) {
      html += '<a class="knopf knopf--wa" id="wa-senden" href="' + waLink +
        '" target="_blank" rel="noopener">In WhatsApp öffnen</a>';
    }
    html += '<button class="knopf knopf--rand" type="button" id="kopieren">Bestellung kopieren</button>';
    html += '<a class="knopf knopf--rand" href="tel:' + (window.CALIMERO_TEL || "") +
      '">Lieber anrufen</a>';
    html += "</div>";
    html += '<p class="konfig__hint">Kein WhatsApp? Kopieren Sie den Text und schicken Sie ihn ' +
      "per SMS, oder rufen Sie an und nennen Sie Ihre Bestellnummer.</p>";
    html += '<div class="konfig__fuss konfig__fuss--statisch">' +
      '<button class="knopf knopf--rand" type="button" id="neu">Neue Bestellung beginnen</button></div>';
    html += "</div>";
    overlayAuf(html);

    var kopf = document.getElementById("kopieren");
    kopf.addEventListener("click", function () {
      function fertig() { kopf.textContent = "Kopiert"; setTimeout(function () {
        kopf.textContent = "Bestellung kopieren"; }, 2500); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(fertig, ersatz);
      } else ersatz();
      function ersatz() {
        var t = document.createElement("textarea");
        t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
        document.body.appendChild(t); t.select();
        try { document.execCommand("copy"); fertig(); } catch (e) {}
        document.body.removeChild(t);
      }
    });
    var wa = document.getElementById("wa-senden");
    if (wa) wa.addEventListener("click", leeren);
    document.getElementById("neu").addEventListener("click", function () {
      leeren(); overlayZu();
    });
    function leeren() {
      korb = []; korbSichern(); leisteZeichnen();
    }
  }

  /* ---------------------------------------------------- Start */
  function start(daten) {
    K = daten;
    korbLaden();
    tabsZeichnen();
    listeZeichnen();
    leisteZeichnen();

    el.liste.addEventListener("click", function (e) {
      var b = e.target.closest(".best-artikel");
      if (b) artikelOeffnen(b.getAttribute("data-id"));
    });
    if (el.suche) {
      el.suche.addEventListener("input", listeZeichnen);
    }
    el.leiste.addEventListener("click", korbOeffnen);
  }

  fetch("menu.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(start)
    .catch(function () {
      el.liste.innerHTML = '<p class="kein-treffer" style="display:block">' +
        "Die Speisekarte konnte nicht geladen werden. Bitte rufen Sie uns an: " +
        '<a href="tel:' + (window.CALIMERO_TEL || "") + '">' +
        (window.CALIMERO_TEL_ANZEIGE || "") + "</a>.</p>";
    });
})();
