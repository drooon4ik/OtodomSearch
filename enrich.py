"""
Обогащает первые N объявлений из listings.json деталями со страницы.
Добавляет: район, комнаты, этаж, год постройки, материал стен, состояние, рынок, координаты.
Сохраняет в enriched.json и enriched.csv.
"""
import json, csv, re, time, random, sys
import requests

LIMIT = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--limit=")), 9999))
RE_ENRICH = "--re-enrich" in sys.argv  # повторно обогатить объявления без description
DELAY = (0.5, 2.0)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9",
}

CHAR_KEYS = ["rooms_num", "floor_no", "building_floors_num", "build_year",
             "building_material", "construction_status", "market", "building_type"]


def fetch_details(url: str) -> dict:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        scripts = re.findall(r"<script[^>]*>(.*?)</script>", r.text, re.DOTALL)
        for s in scripts:
            if '"ad":{' in s and len(s) > 10000:
                data = json.loads(s)
                ad = data["props"]["pageProps"]["ad"]

                chars = {c["key"]: c.get("localizedValue") or c.get("value")
                         for c in ad.get("characteristics", [])}

                loc = ad.get("location", {})
                addr = loc.get("address", {})
                coords = loc.get("coordinates", {})
                district = (addr.get("district") or {}).get("name", "")

                desc_parts = ad.get("description", {})
                description = " ".join(
                    re.sub(r"<[^>]+>", " ", v)
                    for v in (desc_parts.values() if isinstance(desc_parts, dict) else [str(desc_parts)])
                ).lower()

                features = [f.lower() for f in ad.get("features", []) if isinstance(f, str)]

                return {
                    "district":         district,
                    "lat":              coords.get("latitude"),
                    "lon":              coords.get("longitude"),
                    "market":           chars.get("market", ""),
                    "rooms":            chars.get("rooms_num", ""),
                    "floor":            chars.get("floor_no", ""),
                    "floors_total":     chars.get("building_floors_num", ""),
                    "build_year":       chars.get("build_year", ""),
                    "material":         chars.get("building_material", ""),
                    "condition":        chars.get("construction_status", ""),
                    "building_type":    chars.get("building_type", ""),
                    "features":         features,
                    "description":      description,
                }
    except Exception as e:
        print(f"  ошибка: {e}")
    return {}


with open("data/listings.json", encoding="utf-8") as f:
    listings = json.load(f)

# Загружаем уже обогащённые, чтобы не ходить на них повторно
try:
    with open("data/enriched.json", encoding="utf-8") as f:
        already = {item["url"]: item for item in json.load(f)}
except FileNotFoundError:
    already = {}

results = list(already.values())  # сохраняем старые
to_enrich = [item for item in listings[:LIMIT] if item["url"] not in already]
missing = [item for item in already.values()
           if not item.get("description") or not item.get("features")][:LIMIT]
if missing:
    print(f"Неполные (нет description или features): {len(missing)} — будут перезапрошены")
    to_enrich = missing + [i for i in to_enrich if i not in missing]
print(f"Уже обогащено: {len(already)}, новых: {len(to_enrich)}")

for i, item in enumerate(to_enrich):
    print(f"[{i+1}/{len(to_enrich)}] {item['url'][-50:]}", end=" ... ", flush=True)
    details = fetch_details(item["url"])
    merged = {**item, **details}
    results.append(merged)
    print(details.get("district", "?"), "|", details.get("build_year", "?"),
          "|", details.get("condition", "?"))
    if i < len(to_enrich) - 1:
        time.sleep(random.uniform(*DELAY))

# дедупликация по URL — последняя версия побеждает
results = list({r["url"]: r for r in results}.values())

FIELDS = ["price", "area", "price_m2", "price_m2_num",
          "district", "rooms", "floor", "floors_total",
          "build_year", "material", "condition", "building_type", "market",
          "lat", "lon", "description", "url"]

with open("data/enriched.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

with open("data/enriched.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(results)

print(f"\nГотово: {len(results)} объявлений → enriched.json, enriched.csv")

import tracker
current = {
    tracker.otodom_id(item["url"]): {
        **item,
        "_id": tracker.otodom_id(item["url"]),
        "_fp": tracker.fingerprint(item),
    }
    for item in results
}
tracker.run(current)
