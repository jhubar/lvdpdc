#!/usr/bin/env python3
"""Lit les prix habituels dans Beds24 et les écrit dans les pages."""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPERTY_ID = os.environ.get("BEDS24_PROPERTY_ID", "368230")
ROOMS = {
    758046: "einstein",
    758047: "golf",
    758048: "tilleul",
    758049: "cramique",
}
FILES = [
    "index.html",
    "albert-einstein.html",
    "golf-club.html",
    "cafe-cramique.html",
    "sous-le-tilleul.html",
    "assets/js/villa.js",
    "llms.txt",
    "assets/seo/mise-a-jour.txt",
    "sitemap.xml",
]
PAGE_FILES = [
    "index.html",
    "albert-einstein.html",
    "golf-club.html",
    "cafe-cramique.html",
    "sous-le-tilleul.html",
    "atelier-du-peintre.html",
]


def load_local_env():
    path = ROOT / ".env.local"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def require_token():
    token = os.environ.get("BEDS24_PRICING_ROOM_REFRESH_TOKEN", "").strip()
    if not token:
        sys.exit("BEDS24_PRICING_ROOM_REFRESH_TOKEN est vide.")
    return token


def get_calendar(token):
    start = date.today() + timedelta(days=1)
    end = start + timedelta(days=120)
    query = urllib.parse.urlencode({
        "propertyId": PROPERTY_ID,
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "includePrices": "true",
    })
    request = urllib.request.Request(
        "https://beds24.com/api/v2/inventory/rooms/calendar?" + query,
        headers={"token": token, "accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode())
    if not payload.get("success"):
        sys.exit("Beds24 n'a pas renvoyé les prix.")
    return payload["data"]


def usual_price(calendar, key):
    counts = Counter()
    for block in calendar:
        if key not in block or block[key] in (None, ""):
            continue
        amount = int(block[key])
        if amount <= 0 or amount > 5000:
            sys.exit(f"Prix Beds24 invalide : {amount}.")
        start = date.fromisoformat(block["from"])
        finish = date.fromisoformat(block["to"])
        day = start
        while day <= finish:
            counts[amount] += 1
            day += timedelta(days=1)
    if not counts:
        sys.exit(f"Aucun prix {key} sur la période lue.")
    winner, votes = counts.most_common(1)[0]
    tied = [amount for amount, count in counts.items() if count == votes]
    if len(tied) > 1:
        sys.exit(f"Deux prix aussi fréquents pour {key} : {sorted(tied)}.")
    if votes < 7:
        sys.exit(f"Pas assez de dates pour {key}.")
    return winner


def read_prices(token):
    by_room = {item["roomId"]: item for item in get_calendar(token)}
    missing = [room_id for room_id in ROOMS if room_id not in by_room]
    if missing:
        sys.exit(f"Chambres absentes de Beds24 : {missing}.")
    prices = {}
    for room_id, name in ROOMS.items():
        calendar = by_room[room_id]["calendar"]
        if name == "einstein":
            prices[name] = (
                usual_price(calendar, "price1"),
                usual_price(calendar, "price2"),
                usual_price(calendar, "price3"),
            )
        else:
            prices[name] = usual_price(calendar, "price1")
    return prices


def sub(parts, pattern, replacement, label):
    total = 0
    updated = []
    for text in parts:
        new, count = re.subn(pattern, replacement, text)
        total += count
        updated.append(new)
    if total < 1:
        sys.exit(f"Texte introuvable : {label}.")
    return updated


def apply_prices(parts, prices):
    two, three, four = prices["einstein"]
    golf, cramique, tilleul = prices["golf"], prices["cramique"], prices["tilleul"]
    parts = sub(parts, r"\d+ € pour 2 personnes, \d+ € pour 3 et \d+ € pour 4", f"{two} € pour 2 personnes, {three} € pour 3 et {four} € pour 4", "Einstein, détail")
    parts = sub(parts, r"\d+ €, \d+ € ou \d+ €", f"{two} €, {three} € ou {four} €", "Einstein, série")
    parts = sub(
        parts,
        r"\d+ € <small>/ 2</small> · \d+ € <small>/ 3</small> · \d+ € <small>/ 4</small>",
        f"{two} € <small>/ 2</small> · {three} € <small>/ 3</small> · {four} € <small>/ 4</small>",
        "Einstein, carte",
    )
    parts = sub(parts, r"€\d+ for 2 guests, €\d+ for 3 and €\d+ for 4", f"€{two} for 2 guests, €{three} for 3 and €{four} for 4", "Einstein, anglais")
    parts = sub(parts, r"€\d+ for 2 guests, €\d+ for 3, €\d+ for 4", f"€{two} for 2 guests, €{three} for 3, €{four} for 4", "Einstein, llms")
    parts = sub(parts, r"€\d+, €\d+ or €\d+", f"€{two}, €{three} or €{four}", "Einstein, série anglaise")
    parts = sub(parts, r'("price": ")\d+(", "priceCurrency": "EUR", "description": "2 personnes)', rf"\g<1>{two}\2", "offre 2")
    parts = sub(parts, r'("price": ")\d+(", "priceCurrency": "EUR", "description": "3 personnes)', rf"\g<1>{three}\2", "offre 3")
    parts = sub(parts, r'("price": ")\d+(", "priceCurrency": "EUR", "description": "4 personnes)', rf"\g<1>{four}\2", "offre 4")
    for heading, amount in (("Golf Club", golf), ("Café Cramique", cramique), ("Sous le Tilleul", tilleul)):
        parts = sub(parts, rf"(<h3>{re.escape(heading)}</h3>\s*<p class=\"price\">)\d+", rf"\g<1>{amount}", f"carte {heading}")
        parts = sub(parts, rf'("name": "{re.escape(heading)}"[\s\S]{{0,700}}?"price": ")\d+', rf"\g<1>{amount}", f"fiche {heading}")
    parts = sub(parts, r'(data-i18n="fact_golf_price">)\d+', rf"\g<1>{golf}", "fait Golf")
    parts = sub(parts, r'(data-i18n="fact_cramique_price">)\d+', rf"\g<1>{cramique}", "fait Cramique")
    parts = sub(parts, r'(data-i18n="fact_tilleul_price">)\d+', rf"\g<1>{tilleul}", "fait Tilleul")
    parts = sub(parts, r'(fact_golf_price: ")\d+', rf"\g<1>{golf}", "js Golf")
    parts = sub(parts, r'(fact_cramique_price: ")\d+', rf"\g<1>{cramique}", "js Cramique")
    parts = sub(parts, r'(fact_tilleul_price: ")\d+', rf"\g<1>{tilleul}", "js Tilleul")
    parts = sub(parts, r'(fact_golf_price: "€)\d+', rf"\g<1>{golf}", "js Golf anglais")
    parts = sub(parts, r'(fact_cramique_price: "€)\d+', rf"\g<1>{cramique}", "js Cramique anglais")
    parts = sub(parts, r'(fact_tilleul_price: "€)\d+', rf"\g<1>{tilleul}", "js Tilleul anglais")
    parts = sub(parts, r"Albert Einstein \(\d+ €, \d+ € ou \d+ €", f"Albert Einstein ({two} €, {three} € ou {four} €", "faq Einstein")
    parts = sub(
        parts,
        r"Golf Club \(\d+ €\), Café Cramique \(\d+ €\) et Sous le Tilleul \(\d+ €\)",
        f"Golf Club ({golf} €), Café Cramique ({cramique} €) et Sous le Tilleul ({tilleul} €)",
        "faq",
    )
    parts = sub(
        parts,
        r"Albert Einstein \(€\d+, €\d+ or €\d+\), Golf Club \(€\d+\), Café Cramique \(€\d+\) and Sous le Tilleul \(€\d+\)",
        f"Albert Einstein (€{two}, €{three} or €{four}), Golf Club (€{golf}), Café Cramique (€{cramique}) and Sous le Tilleul (€{tilleul})",
        "faq anglaise",
    )
    parts = sub(
        parts,
        r"Golf Club €\d+, Café Cramique €\d+ and Sous le Tilleul €\d+",
        f"Golf Club €{golf}, Café Cramique €{cramique} and Sous le Tilleul €{tilleul}",
        "llms anglais",
    )
    parts = sub(
        parts,
        r"Prix habituel : Albert Einstein \d+ €, \d+ € ou \d+ € ; Golf Club \d+ € ; Café Cramique \d+ € ; Sous le Tilleul \d+ €\.",
        f"Prix habituel : Albert Einstein {two} €, {three} € ou {four} € ; Golf Club {golf} € ; Café Cramique {cramique} € ; Sous le Tilleul {tilleul} €.",
        "note",
    )
    parts = sub(parts, r"(golf-club\.html\): )\d+( € la nuit)", rf"\g<1>{golf}\g<2>", "llms Golf")
    parts = sub(parts, r"(cafe-cramique\.html\): )\d+( € la nuit)", rf"\g<1>{cramique}\g<2>", "llms Cramique")
    parts = sub(parts, r"(sous-le-tilleul\.html\): )\d+( € la nuit)", rf"\g<1>{tilleul}\g<2>", "llms Tilleul")
    parts = sub(parts, r"(Chambre Golf Club à La Villa du Pré du Cerf, Spa, à côté des Thermes\. )\d+", rf"\g<1>{golf}", "meta Golf")
    parts = sub(parts, r"(Chambre Café Cramique à La Villa du Pré du Cerf, Spa, à côté des Thermes\. )\d+", rf"\g<1>{cramique}", "meta Cramique")
    parts = sub(parts, r"(Chambre Sous le Tilleul à La Villa du Pré du Cerf, Spa, à côté des Thermes\. )\d+", rf"\g<1>{tilleul}", "meta Tilleul")
    parts = sub(parts, r'(og:description" content=")\d+( € la nuit, petit-déjeuner compris\. Maison)', rf"\g<1>{golf}\2", "og Golf")
    parts = sub(parts, r"(Chambre Café Cramique à Spa\. )\d+", rf"\g<1>{cramique}", "og Cramique")
    parts = sub(parts, r"(Chambre Sous le Tilleul à Spa\. )\d+", rf"\g<1>{tilleul}", "og Tilleul")
    parts = sub(parts, r"(balcon avec vue sur le pré du Cerf\. Le prix affiché est de )\d+", rf"\g<1>{golf}", "page Golf")
    parts = sub(parts, r"(a balcony overlooking the meadow\. The price shown is €)\d+", rf"\g<1>{golf}", "page Golf anglais")
    parts = sub(parts, r"(La chambre Café Cramique est à La Villa du Pré du Cerf, maison d'hôtes au 3 Chemin de Frahinfaz à Spa\. Le prix affiché est de )\d+", rf"\g<1>{cramique}", "page Cramique")
    parts = sub(parts, r"(The Café Cramique room is at La Villa du Pré du Cerf, a bed and breakfast at 3 Chemin de Frahinfaz in Spa\. The price shown is €)\d+", rf"\g<1>{cramique}", "page Cramique anglais")
    parts = sub(parts, r"(La chambre Sous le Tilleul est à La Villa du Pré du Cerf, maison d'hôtes au 3 Chemin de Frahinfaz à Spa\. Le prix affiché est de )\d+", rf"\g<1>{tilleul}", "page Tilleul")
    parts = sub(parts, r"(The Sous le Tilleul room is at La Villa du Pré du Cerf, a bed and breakfast at 3 Chemin de Frahinfaz in Spa\. The price shown is €)\d+", rf"\g<1>{tilleul}", "page Tilleul anglais")
    parts = sub(parts, r'(cramique_text: ")\d+', rf"\g<1>{cramique}", "texte Cramique")
    parts = sub(parts, r'(tilleul_text: ")\d+', rf"\g<1>{tilleul}", "texte Tilleul")
    parts = sub(parts, r'(cramique_text: "€)\d+', rf"\g<1>{cramique}", "texte Cramique anglais")
    parts = sub(parts, r'(tilleul_text: "€)\d+', rf"\g<1>{tilleul}", "texte Tilleul anglais")
    parts = sub(parts, r'("name": "Café Cramique"[\s\S]{0,250}?Spa\. )\d+( € la nuit)', rf"\g<1>{cramique}\2", "description Cramique")
    parts = sub(parts, r'("name": "Sous le Tilleul"[\s\S]{0,250}?Spa\. )\d+( € la nuit)', rf"\g<1>{tilleul}\2", "description Tilleul")
    return parts


def stamp(parts, names, day, version):
    stamped = []
    for name, text in zip(names, parts):
        if name == "index.html":
            text = re.sub(r'"dateModified": "\d{4}-\d{2}-\d{2}"', f'"dateModified": "{day}"', text, count=1)
        if name == "sitemap.xml":
            text = re.sub(
                r"(<loc>https://lavilladupreducerf\.be/(?:|albert-einstein\.html|golf-club\.html|cafe-cramique\.html|sous-le-tilleul\.html)</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}",
                rf"\g<1>{day}",
                text,
            )
        if name.endswith(".html"):
            text = re.sub(r"villa\.js\?v=[^\"']+", f"villa.js?v={version}", text)
        stamped.append(text)
    return stamped


def guard(before, after):
    for marker in ("160 cm", "180 cm", "90 cm", "165 €"):
        if before.count(marker) != after.count(marker):
            sys.exit(f"Le texte protégé a changé : {marker}.")


def self_test():
    names = [name for name in FILES if name != "sitemap.xml"]
    original = [(ROOT / name).read_text() for name in names]
    sample = {
        "einstein": (171, 226, 301),
        "golf": 161,
        "cramique": 162,
        "tilleul": 163,
    }
    updated = apply_prices(original, sample)
    guard("".join(original), "".join(updated))
    joined = "".join(updated)
    for amount, label in ((171, "Einstein 2"), (226, "Einstein 3"), (301, "Einstein 4"), (161, "Golf"), (162, "Cramique"), (163, "Tilleul")):
        if str(amount) not in joined:
            sys.exit(f"Essai interne incomplet : {label}.")
    if "160 cm" not in joined:
        sys.exit("Essai interne : le lit de 160 cm a disparu.")
    print("Essai interne réussi.")


def main():
    load_local_env()
    if "--self-test" in sys.argv:
        self_test()
        return
    prices = read_prices(require_token())
    names = list(FILES)
    original = [(ROOT / name).read_text() for name in names]
    updated = apply_prices(original, prices)
    guard("".join(original), "".join(updated))
    if updated == original:
        print(
            "Prix inchangés : "
            f"Einstein {prices['einstein'][0]}/{prices['einstein'][1]}/{prices['einstein'][2]}, "
            f"Golf {prices['golf']}, Cramique {prices['cramique']}, Tilleul {prices['tilleul']}."
        )
        return
    day = date.today().isoformat()
    version = day.replace("-", "")
    pages = {name: text for name, text in zip(names, updated)}
    for name in PAGE_FILES:
        if name not in pages and (ROOT / name).exists():
            pages[name] = (ROOT / name).read_text()
    ordered = list(pages)
    stamped = stamp([pages[name] for name in ordered], ordered, day, version)
    for name, text in zip(ordered, stamped):
        (ROOT / name).write_text(text)
    print(
        "Prix mis à jour : "
        f"Einstein {prices['einstein'][0]}/{prices['einstein'][1]}/{prices['einstein'][2]}, "
        f"Golf {prices['golf']}, Cramique {prices['cramique']}, Tilleul {prices['tilleul']}."
    )


if __name__ == "__main__":
    main()
