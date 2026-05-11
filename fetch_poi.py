"""
Собирает POI в радиусе RADIUS_M от станций метро через Overpass API.
Университеты захардкожены вручную (только крупные).
Сохраняет в poi.json.
"""
import json, time, requests, urllib.parse, math
from config import METRO_STATIONS, UNIVERSITIES, POI_RADIUS_M, POI_EXCLUDE_NAMES

RADIUS_M = POI_RADIUS_M

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "OtodomInvestmentSearch/1.0 (personal research project)"}


def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371000
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2 +
         math.cos(lat1 * p) * math.cos(lat2 * p) *
         math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def near_any_station(lat, lon) -> bool:
    return any(haversine(lat, lon, s[0], s[1]) <= RADIUS_M for s in METRO_STATIONS)


def fetch_bbox(tag: str) -> list[dict]:
    """Запрос по bbox всей зоны, потом фильтруем по радиусу от станций."""
    lats = [s[0] for s in METRO_STATIONS]
    lons = [s[1] for s in METRO_STATIONS]
    pad = RADIUS_M / 111000  # градусы
    bbox = f"{min(lats)-pad},{min(lons)-pad},{max(lats)+pad},{max(lons)+pad}"
    query = (
        f"[out:json][timeout:60];\n"
        f"(\n  node{tag}({bbox});\n  way{tag}({bbox});\n);\nout center;"
    )
    url = OVERPASS_URL + "?data=" + urllib.parse.quote(query)
    r = requests.get(url, headers=HEADERS, timeout=90)
    r.raise_for_status()
    result = []
    for el in r.json().get("elements", []):
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        name = el.get("tags", {}).get("name", "")
        if lat and lon and near_any_station(lat, lon) and name.lower() not in POI_EXCLUDE_NAMES:
            result.append({"lat": lat, "lon": lon, "name": name})
    return result


CATEGORIES = {
    "supermarket": '[shop="supermarket"]',
    "school":      '[amenity="school"]',
}

SECONDARY_KEYWORDS = ("liceum", "technikum", "ogólnokształcące", "matura")

def is_secondary_school(name: str) -> bool:
    n = name.lower()
    return any(kw in n for kw in SECONDARY_KEYWORDS)

poi = {"university": UNIVERSITIES}

for cat, tag in CATEGORIES.items():
    print(f"Загружаю {cat}...", end=" ", flush=True)
    items = fetch_bbox(tag)
    if cat == "school":
        items = [s for s in items if is_secondary_school(s["name"])]
    poi[cat] = items
    print(f"{len(items)} в радиусе {RADIUS_M}м от станций")
    time.sleep(10)

with open("data/poi.json", "w", encoding="utf-8") as f:
    json.dump(poi, f, ensure_ascii=False, indent=2)

print("\nГотово → poi.json")
for cat, items in poi.items():
    print(f"  {cat}: {len(items)}")
