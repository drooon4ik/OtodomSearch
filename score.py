"""
Считает инвестиционный score для объявлений из enriched.json.
"""
import json, csv, math, re, datetime
from profile_loader import load_profile, profile_arg
from config_base import RENOVATION_COST, MATERIAL_SCORE, DESC_SIGNALS

cfg, data_dir = load_profile(profile_arg())
WEIGHTS       = cfg.SCORING_WEIGHTS
POI_WEIGHTS   = cfg.POI_WEIGHTS
DISTRICT_SCORE = cfg.DISTRICT_SCORE
CENTER        = cfg.CENTER


def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371000; p = math.pi / 180
    a = (math.sin((lat2-lat1)*p/2)**2 +
         math.cos(lat1*p)*math.cos(lat2*p)*math.sin((lon2-lon1)*p/2)**2)
    return 2 * R * math.asin(math.sqrt(a))


def nearest(lat, lon, points):
    if not points:
        return float("inf"), {}
    best = min(points, key=lambda p: haversine(lat, lon, p["lat"], p["lon"]))
    return haversine(lat, lon, best["lat"], best["lon"]), best


def normalize(values):
    mn, mx = min(values), max(values)
    return [1.0]*len(values) if mx == mn else [(mx-v)/(mx-mn) for v in values]


def normalize_log(values):
    log_vals = [math.log1p(v) for v in values]
    return normalize(log_vals)


def year_score(year: int) -> float:
    if year <= 0:
        return 0.3
    current = datetime.date.today().year
    if year > current:
        return max(0.5, 1.0 - (year - current) * 0.1)
    if 2010 <= year <= 2020:
        return 1.0
    if year > 2020:
        return max(0.85, 1.0 - (year - 2020) * 0.03)
    return max(0.1, 1.0 - ((year - 2010) / 60) ** 2)


# ── Загрузка ──────────────────────────────────────────────────────────────────
with open(data_dir / "enriched.json", encoding="utf-8") as f:
    listings = json.load(f)
listings = [l for l in listings if l.get("price") not in ("?", "", None)]
print(f"Объявлений с ценой: {len(listings)}")

try:
    with open(data_dir / "poi.json", encoding="utf-8") as f:
        poi = json.load(f)
    has_poi = any(poi.get(k) for k in ("supermarket", "school", "university"))
    poi["supermarket"] = [s for s in poi.get("supermarket", [])
                          if not any(ex in s.get("name","").lower()
                                     for ex in cfg.POI_EXCLUDE_NAMES)]
except FileNotFoundError:
    poi = {}; has_poi = False
    print("poi.json не найден — POI scoring пропущен")

# ── Сырые метрики ─────────────────────────────────────────────────────────────
for item in listings:
    area = float(str(item.get("area","0")).replace(",",".").split()[0]) or 1
    price_str = str(item.get("price","0")).replace("\xa0","").replace(" ","").replace("zł","").replace(",",".")
    try:
        price_num = float(price_str) if price_str not in ("","?") else 0.0
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
            item["_d_super"] = d_super; item["_d_school"] = d_school; item["_d_uni"] = d_uni
            item["_poi_dist"] = (d_super * POI_WEIGHTS["supermarket"] +
                                 d_school * POI_WEIGHTS["school"] +
                                 d_uni    * POI_WEIGHTS["university"])
        else:
            item["_poi_dist"] = 0
    else:
        item["_center_dist"] = 10000; item["_poi_dist"] = 0

    try:
        item["_build_year"] = int(item.get("build_year") or 0)
    except (ValueError, TypeError):
        item["_build_year"] = 1970

    try:
        floor = int(str(item.get("floor","2")).replace("parter","0").split()[0])
        total = int(item.get("floors_total") or 5)
        item["_floor_num"] = floor
        if floor == 0:         item["_floor_score"] = 0.3
        elif floor == 1:       item["_floor_score"] = 0.5
        elif floor == total:   item["_floor_score"] = 0.4
        else:                  item["_floor_score"] = 1.0
    except (ValueError, TypeError):
        item["_floor_score"] = 0.75

    mat = str(item.get("material") or "").lower()
    item["_material_score"] = MATERIAL_SCORE.get(mat, 0.65)
    item["_market_score"]   = 0.6 if item.get("market") == "pierwotny" else 1.0
    item["_district_score"] = DISTRICT_SCORE.get(item.get("district",""), 0.75)

    features = item.get("features") or []
    desc = item.get("description") or ""
    raw_desc = sum(
        weight for _, (source, pattern, weight) in DESC_SIGNALS.items()
        if (any(re.search(pattern, f) for f in features) if source == "features"
            else bool(re.search(pattern, desc)))
    )
    item["_desc_score"] = min(raw_desc, 1.0)

# ── Нормализация ──────────────────────────────────────────────────────────────
def col(key): return [item[key] for item in listings]

norm_price  = normalize_log(col("_effective_price_m2"))
norm_center = normalize(col("_center_dist"))
norm_poi    = normalize(col("_poi_dist")) if has_poi else [0.5] * len(listings)

_year_raw = [year_score(item["_build_year"]) for item in listings]
_yr_mn, _yr_mx = min(_year_raw), max(_year_raw)
norm_year = [(v-_yr_mn)/(_yr_mx-_yr_mn) if _yr_mx > _yr_mn else 1.0 for v in _year_raw]

for i, item in enumerate(listings):
    components = {
        "s_price":    round(norm_price[i]          * WEIGHTS["price_m2_eff"], 3),
        "s_center":   round(norm_center[i]          * WEIGHTS["center_dist"],  3),
        "s_year":     round(norm_year[i]            * WEIGHTS["build_year"],   3),
        "s_floor":    round(item["_floor_score"]    * WEIGHTS["floor"],        3),
        "s_poi":      round(norm_poi[i]             * WEIGHTS["poi"],          3),
        "s_material": round(item["_material_score"] * WEIGHTS["material"],     3),
        "s_market":   round(item["_market_score"]   * WEIGHTS["market"],       3),
        "s_desc":     round(item["_desc_score"]     * WEIGHTS["desc"],         3),
        "s_district": round(item["_district_score"] * WEIGHTS["district"],     3),
    }
    item.update(components)
    item["score"] = round(sum(components.values()), 4)
    item["effective_price_m2"] = round(item["_effective_price_m2"])
    item["reno_cost_total"]    = round(item["_reno_total"])
    item["center_dist_m"]      = round(item["_center_dist"])

listings.sort(key=lambda x: x["score"], reverse=True)

# ── Вывод ─────────────────────────────────────────────────────────────────────
print(f"\n{'#':>2}  {'Score':>6}  {'Цена':>12}  {'Эфф.цена/м²':>12}  {'До центра':>9}  {'Год':>4}  {'Район'}")
print("-" * 110)
for i, l in enumerate(listings, 1):
    print(f"{i:>2}  {l['score']:>6.3f}  {l['price']:>12}  {l['effective_price_m2']:>12,} zł/м²  "
          f"{l['center_dist_m']:>8}м  {l['build_year']:>4}  {l.get('district','')}")
    if has_poi and l.get("_nearest_super"):
        print(f"      POI: {l['_nearest_super'].get('name','?')[:20]} {l['_d_super']:.0f}м  |  "
              f"{l['_nearest_uni'].get('name','?')[:25]} {l['_d_uni']:.0f}м")

# ── Сохранение ────────────────────────────────────────────────────────────────
FIELDS = ["score","s_price","s_center","s_year","s_floor","s_poi","s_material","s_market","s_desc","s_district",
          "price","area","price_m2","effective_price_m2","reno_cost_total",
          "center_dist_m","district","rooms","floor","floors_total",
          "build_year","material","condition","building_type","market","lat","lon","url"]

with open(data_dir / "scored.json", "w", encoding="utf-8") as f:
    json.dump(listings, f, ensure_ascii=False, indent=2)

with open(data_dir / "scored.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(listings)

print(f"\n→ {data_dir}/scored.json, scored.csv ({len(listings)} объявлений)")
if not has_poi:
    print("  ⚠ POI scoring не применён (запусти fetch_poi.py для полного scoring)")
