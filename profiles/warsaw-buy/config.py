# ── Город ────────────────────────────────────────────────────────────────────
CITY        = "warszawa"
VOIVODESHIP = "mazowieckie"

# ── Параметры поиска Otodom ───────────────────────────────────────────────────
TRANSACTION   = "sprzedaz"
PROPERTY_TYPE = "mieszkanie"

SEARCH_PARAMS = {
    "limit":            36,
    "by":               "DEFAULT",
    "direction":        "DESC",
    "areaMin":          35,
    "areaMax":          60,
    "buildYearMin":     1950,
    "buildingMaterial": ["BRICK", "BREEZEBLOCK", "SILIKAT", "REINFORCED_CONCRETE"],
    "extras":           ["GARAGE"],
}

# ── Скрапер ───────────────────────────────────────────────────────────────────
DELAY_MIN = 3.0
DELAY_MAX = 6.0

# ── Транзитные точки (метро, ≤30 мин до центра) ───────────────────────────────
TRANSIT_POINTS = [
    # M2 (red)
    (52.2391822, 20.9443771),  # Księcia Janusza — 28 мин
    (52.2376624, 20.9601048),  # Młynów — 18 мин
    (52.2324542, 20.9663847),  # Płocka — 24 мин
    (52.2300827, 20.9828946),  # Rondo Daszyńskiego — 16 мин
    (52.2310069, 21.0101860),  # Centrum
    (52.2350954, 21.0078988),  # Świętokrzyska — 13 мин
    (52.2368196, 21.0168168),  # Nowy Świat-Uniwersytet — 18 мин
    (52.2399148, 21.0317878),  # Centrum Nauki Kopernik — 28 мин
    (52.2468346, 21.0428470),  # Stadion Narodowy — 23 мин
    (52.2537771, 21.0357972),  # Dworzec Wileński — 23 мин
    (52.2634709, 21.0455232),  # Szwedzka — 23 мин
    (52.2692518, 21.0513658),  # Targówek Mieszkaniowy — 28 мин
    # M1 (blue)
    (52.1411007, 21.0564351),  # Natolin — 28 мин
    (52.1493000, 21.0461062),  # Imielin — 29 мин
    (52.1560759, 21.0347233),  # Stokłosy — 24 мин
    (52.1620456, 21.0276283),  # Ursynów — 19 мин
    (52.1727624, 21.0262866),  # Służew — 16 мин
    (52.1818168, 21.0231452),  # Wilanowska — 18 мин
    (52.1898719, 21.0167966),  # Wierzbno — 16 мин
    (52.1988637, 21.0122349),  # Racławicka — 15 мин
    (52.2087775, 21.0079298),  # Pole Mokotowskie — 14 мин
    (52.2186581, 21.0153031),  # Politechnika — 8 мин
    (52.2310069, 21.0101860),  # Centrum (wspólna)
    (52.2452163, 21.0008823),  # Ratusz-Arsenał — 17 мин
    (52.2580586, 20.9941857),  # Dworzec Gdański — 22 мин
    (52.2692619, 20.9844973),  # Plac Wilsona — 19 мин
    (52.2715768, 20.9719399),  # Marymont — 22 мин
    (52.2768261, 20.9601259),  # Słodowiec — 25 мин
    (52.2818277, 20.9493511),  # Stare Bielany — 23 мин
    (52.2907703, 20.9298678),  # Młociny — 30 мин
]

# ── Центр города ──────────────────────────────────────────────────────────────
CENTER = (52.2310069, 21.0101860)  # Centrum M1+M2

# ── Университеты (захардкожены) ───────────────────────────────────────────────
UNIVERSITIES = [
    {"name": "Uniwersytet Warszawski",              "lat": 52.2394, "lon": 21.0150},
    {"name": "Politechnika Warszawska",             "lat": 52.2197, "lon": 21.0115},
    {"name": "SGH",                                 "lat": 52.2081, "lon": 21.0011},
    {"name": "Uniwersytet Kardynała Wyszyńskiego",  "lat": 52.2453, "lon": 20.9853},
    {"name": "Akademia Leona Koźmińskiego",         "lat": 52.2562, "lon": 21.0444},
    {"name": "SWPS",                                "lat": 52.2275, "lon": 21.0297},
    {"name": "Warszawski Uniwersytet Medyczny",     "lat": 52.2213, "lon": 21.0154},
    {"name": "Akademia Sztuk Pięknych",             "lat": 52.2481, "lon": 21.0136},
    {"name": "Uniwersytet Muzyczny",                "lat": 52.2302, "lon": 21.0175},
    {"name": "Akademia Teatralna",                  "lat": 52.2390, "lon": 21.0120},
    {"name": "Collegium Civitas",                   "lat": 52.2310, "lon": 21.0102},
    {"name": "ALK Kampus Bemowo",                   "lat": 52.2392, "lon": 20.9155},
]

# ── Параметры POI ─────────────────────────────────────────────────────────────
POI_RADIUS_M      = 2000
POI_EXCLUDE_NAMES = ["żabka"]

# ── Скоринг ───────────────────────────────────────────────────────────────────
SCORING_WEIGHTS = {
    "price_m2_eff": 0.40,
    "center_dist":  0.08,
    "build_year":   0.10,
    "floor":        0.10,
    "poi":          0.06,
    "material":     0.05,
    "market":       0.05,
    "desc":         0.08,
    "district":     0.08,
}

POI_WEIGHTS = {
    "supermarket": 0.45,
    "school":      0.20,
    "university":  0.35,
}

DISTRICT_SCORE = {
    "Śródmieście":            1.00,
    "Śródmieście Północne":   1.00,
    "Śródmieście Południowe": 1.00,
    "Centrum":                1.00,
    "Powiśle":                1.00,
    "Mokotów":                0.90,
    "Górny Mokotów":          0.90,
    "Żoliborz":               0.90,
    "Sady Żoliborskie":       0.90,
    "Muranów":                0.90,
    "Wola":                   0.85,
    "Czyste":                 0.85,
    "Marymont":               0.85,
    "Ursynów":                0.75,
    "Bielany":                0.75,
    "Stare Bielany":          0.75,
    "Służew":                 0.75,
    "Natolin":                0.75,
    "Imielin":                0.75,
    "Targówek":               0.75,
    "Stare Miasto":           0.70,
    "Praga-Północ":           0.65,
    "Nowa Praga":             0.65,
    "Stara Praga":            0.65,
    "Praga-Południe":         0.65,
    "Wrzeciono":              0.65,
}

# ── Полигон ───────────────────────────────────────────────────────────────────
RADIUS_M = 900  # радиус вокруг каждой транзитной точки
