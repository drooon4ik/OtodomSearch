"""
Считает инвестиционный score для объявлений из enriched.json.
Использует poi.json для proximity scoring (если есть).
Сохраняет в scored.json и scored.csv.
"""
import json, csv, math
from config import (CENTER, RENOVATION_COST, SCORING_WEIGHTS as WEIGHTS,
                    POI_EXCLUDE_NAMES, POI_WEIGHTS)


def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371000
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2 +
         math.cos(lat1 * p) * math.cos(lat2 * p) *
         math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def nearest(lat, lon, points):
    """Возвращает (расстояние, объект) до ближайшей точки."""
    if not points:
        return float("inf"), {}
    best = min(points, key=lambda p: haversine(lat, lon, p["lat"], p["lon"]))
    return haversine(lat, lon, best["lat"], best["lon"]), best


def normalize(values: list[float]) -> list[float]:
    mn, mx = min(values), max(values)
    if mx == mn:
        return [1.0] * len(values)
    return [(mx - v) / (mx - mn) for v in values]


def normalize_higher_better(values: list[float]) -> list[float]:
    mn, mx = min(values), max(values)
    if mx == mn:
        return [1.0] * len(values)
    return [(v - mn) / (mx - mn) for v in values]


# ── Загрузка данных ───────────────────────────────────────────────────────────
with open("data/enriched.json", encoding="utf-8") as f:
    listings = json.load(f)

listings = [l for l in listings if l.get("price") not in ("?", "", None)]
print(f"Объявлений с ценой: {len(listings)}")

try:
    with open("data/poi.json", encoding="utf-8") as f:
        poi = json.load(f)
    has_poi = any(poi.get(k) for k in ("supermarket", "school", "university"))
    poi["supermarket"] = [s for s in poi.get("supermarket", [])
                          if not any(ex in s.get("name", "").lower() for ex in POI_EXCLUDE_NAMES)]
except FileNotFoundError:
    poi = {}
    has_poi = False
    print("poi.json не найден — POI scoring пропущен")

# ── Вычисление сырых метрик ───────────────────────────────────────────────────
for item in listings:
    area = float(str(item.get("area", "0")).replace(",", ".").split()[0]) or 1
    price_str = str(item.get("price", "0")).replace("\xa0", "").replace(" ", "").replace("zł", "").replace(",", ".")
    try:
        price_num = float(price_str) if price_str not in ("", "?") else 0.0
    except ValueError:
        price_num = 0.0

    condition = item.get("condition", "do zamieszkania")
    reno_cost = RENOVATION_COST.get(condition, 500)
    item["_area"] = area
    item["_reno_total"] = reno_cost * area
    item["_effective_price_m2"] = (price_num + reno_cost * area) / area

    lat, lon = item.get("lat"), item.get("lon")
    if lat and lon:
        item["_center_dist"] = haversine(lat, lon, CENTER[0], CENTER[1])
        if has_poi:
            d_super, item["_nearest_super"] = nearest(lat, lon, poi.get("supermarket", []))
            d_school, item["_nearest_school"] = nearest(lat, lon, poi.get("school", []))
            d_uni,   item["_nearest_uni"]    = nearest(lat, lon, poi.get("university", []))
            item["_d_super"] = d_super
            item["_d_school"] = d_school
            item["_d_uni"] = d_uni
            item["_poi_dist"] = (d_super * POI_WEIGHTS["supermarket"] +
                                 d_school * POI_WEIGHTS["school"] +
                                 d_uni    * POI_WEIGHTS["university"])
        else:
            item["_poi_dist"] = 0
    else:
        item["_center_dist"] = 10000
        item["_poi_dist"] = 0

    try:
        item["_build_year"] = int(item.get("build_year") or 0)
    except (ValueError, TypeError):
        item["_build_year"] = 1970

    try:
        floor = int(str(item.get("floor", "2")).replace("parter", "0").split()[0])
        total = int(item.get("floors_total") or 5)
        item["_floor_score"] = 0.5 if floor in (0, 1, total) else 1.0
    except (ValueError, TypeError):
        item["_floor_score"] = 0.75

def normalize_log(values: list[float]) -> list[float]:
    """Нелинейная нормализация: логарифм агрессивнее штрафует высокие значения."""
    log_vals = [math.log1p(v) for v in values]
    return normalize(log_vals)


# ── Нормализация и scoring ────────────────────────────────────────────────────
def col(key): return [item[key] for item in listings]

norm_price  = normalize_log(col("_effective_price_m2"))  # нелинейный штраф за высокую цену
norm_center = normalize(col("_center_dist"))
norm_year   = normalize_higher_better(col("_build_year"))
norm_poi    = normalize(col("_poi_dist")) if has_poi else [0.5] * len(listings)

for i, item in enumerate(listings):
    w = WEIGHTS
    components = {
        "s_price":  round(norm_price[i]       * w["price_m2_eff"], 3),
        "s_center": round(norm_center[i]       * w["center_dist"],  3),
        "s_year":   round(norm_year[i]         * w["build_year"],   3),
        "s_floor":  round(item["_floor_score"] * w["floor"],        3),
        "s_poi":    round(norm_poi[i]          * w["poi"],          3),
    }
    item.update(components)
    item["score"] = round(sum(components.values()), 4)
    item["effective_price_m2"] = round(item["_effective_price_m2"])
    item["reno_cost_total"] = round(item["_reno_total"])
    item["center_dist_m"] = round(item["_center_dist"])

listings.sort(key=lambda x: x["score"], reverse=True)

# ── Вывод ─────────────────────────────────────────────────────────────────────
print(f"\n{'#':>2}  {'Score':>6}  {'Цена':>12}  {'Эфф.цена/м²':>12}  {'Ремонт':>8}  "
      f"{'До центра':>9}  {'Год':>4}  {'Состояние':<18}  {'Район'}")
print(f"{'':>4}  {'':>6}  баллы:  цена  центр    год   этаж    POI  "
      f"[супермаркет  |  школа  |  университет]")
print("-" * 145)
for i, l in enumerate(listings, 1):
    print(f"{i:>2}  {l['score']:>6.3f}  {l['price']:>12}  {l['effective_price_m2']:>12,} zł/м²  "
          f"{l['reno_cost_total']:>7,}  {l['center_dist_m']:>8}м  {l['build_year']:>4}  "
          f"{l.get('condition',''):.<18}  {l.get('district','')}")
    # POI детали
    if has_poi and l.get("_nearest_super"):
        super_str  = f"{l['_nearest_super'].get('name','?')[:20]} {l['_d_super']:.0f}м"
        school_str = f"{l['_nearest_school'].get('name','?')[:20]} {l['_d_school']:.0f}м"
        uni_str    = f"{l['_nearest_uni'].get('name','?')[:25]} {l['_d_uni']:.0f}м"
        poi_detail = f"[{super_str:<25} | {school_str:<25} | {uni_str}]"
    else:
        poi_detail = ""
    print(f"{'':>4}  {'':>6}  {'':>6}  "
          f"{l['s_price']:>5.3f}  {l['s_center']:>5.3f}  {l['s_year']:>5.3f}  "
          f"{l['s_floor']:>5.3f}  {l['s_poi']:>5.3f}  {poi_detail}")

# ── Сохранение ────────────────────────────────────────────────────────────────
FIELDS = ["score", "s_price", "s_center", "s_year", "s_floor", "s_poi",
          "price", "area", "price_m2", "effective_price_m2", "reno_cost_total",
          "center_dist_m", "district", "rooms", "floor", "floors_total",
          "build_year", "material", "condition", "building_type", "market", "lat", "lon", "url"]

with open("data/scored.json", "w", encoding="utf-8") as f:
    json.dump(listings, f, ensure_ascii=False, indent=2)

with open("data/scored.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(listings)

print(f"\n→ scored.json, scored.csv ({len(listings)} объявлений)")
if not has_poi:
    print("  ⚠ POI scoring не применён (запусти fetch_poi.py для полного scoring)")
