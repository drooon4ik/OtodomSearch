# ── Станции метро (проверены Google Directions API, пешком 800м + метро ≤ 30 мин) ──
METRO_STATIONS = [
    # M2 (red)
    # (52.2392071, 20.9154991),  # Bemowo — 39 мин ❌
    # (52.2403314, 20.9298652),  # Ulrychów — 34 мин ❌
    (52.2391822, 20.9443771),  # Księcia Janusza — 28 мин ✅
    (52.2376624, 20.9601048),  # Młynów — 18 мин ✅
    (52.2324542, 20.9663847),  # Płocka — 24 мин ✅
    (52.2300827, 20.9828946),  # Rondo Daszyńskiego — 16 мин ✅
    (52.2310069, 21.0101860),  # Centrum
    (52.2350954, 21.0078988),  # Świętokrzyska — 13 мин ✅
    (52.2368196, 21.0168168),  # Nowy Świat-Uniwersytet — 18 мин ✅
    (52.2399148, 21.0317878),  # Centrum Nauki Kopernik — 28 мин ✅
    (52.2468346, 21.0428470),  # Stadion Narodowy — 23 мин ✅
    (52.2537771, 21.0357972),  # Dworzec Wileński — 23 мин ✅
    (52.2634709, 21.0455232),  # Szwedzka — 23 мин ✅
    (52.2692518, 21.0513658),  # Targówek Mieszkaniowy — 28 мин ✅
    # (52.2751021, 21.0550586),  # Trocka — 36 мин ❌
    # (52.2837496, 21.0621480),  # Zacisze — 39 мин ❌
    # (52.2935850, 21.0289387),  # Bródno — 33 мин ❌
    # M1 (blue)
    # (52.1320765, 21.0650711),  # Kabaty — 33 мин ❌
    (52.1411007, 21.0564351),  # Natolin — 28 мин ✅
    (52.1493000, 21.0461062),  # Imielin — 29 мин ✅
    (52.1560759, 21.0347233),  # Stokłosy — 24 мин ✅
    (52.1620456, 21.0276283),  # Ursynów — 19 мин ✅
    (52.1727624, 21.0262866),  # Służew — 16 мин ✅
    (52.1818168, 21.0231452),  # Wilanowska — 18 мин ✅
    (52.1898719, 21.0167966),  # Wierzbno — 16 мин ✅
    (52.1988637, 21.0122349),  # Racławicka — 15 мин ✅
    (52.2087775, 21.0079298),  # Pole Mokotowskie — 14 мин ✅
    (52.2186581, 21.0153031),  # Politechnika — 8 мин ✅
    (52.2310069, 21.0101860),  # Centrum (wspólna)
    (52.2452163, 21.0008823),  # Ratusz-Arsenał — 17 мин ✅
    (52.2580586, 20.9941857),  # Dworzec Gdański — 22 мин ✅
    (52.2692619, 20.9844973),  # Plac Wilsona — 19 мин ✅
    (52.2715768, 20.9719399),  # Marymont — 22 мин ✅
    (52.2768261, 20.9601259),  # Słodowiec — 25 мин ✅
    (52.2818277, 20.9493511),  # Stare Bielany — 23 мин ✅
    # (52.2863474, 20.9395150),  # Wawrzyszew — 31 мин ❌
    (52.2907703, 20.9298678),  # Młociny — 30 мин ✅
]

# ── Крупные университеты Варшавы (захардкожены) ───────────────────────────────
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

# ── Центр города (Rondo Dmowskiego / Centrum M1+M2) ───────────────────────────
CENTER = (52.2310069, 21.0101860)

# ── Параметры поиска Otodom ───────────────────────────────────────────────────
RADIUS_M   = 900    # радиус полигона вокруг каждой станции, метры
AREA_MIN   = 35     # площадь от, м²
AREA_MAX   = 60     # площадь до, м²
YEAR_MIN   = 1950   # год постройки от

BUILDING_MATERIALS = ["BRICK", "BREEZEBLOCK", "SILIKAT", "REINFORCED_CONCRETE"]
EXTRAS             = ["GARAGE"]
TRANSACTION        = "sprzedaz"
PROPERTY_TYPE      = "mieszkanie"
SORT_BY            = "DEFAULT"
SORT_DIR           = "DESC"

# ── Параметры сбора POI ───────────────────────────────────────────────────────
POI_RADIUS_M      = 2000        # радиус от станции для поиска POI
POI_EXCLUDE_NAMES = ["żabka"]   # бренды которые исключаем из supermarket

# ── Стоимость ремонта своими руками (zł/м²) ───────────────────────────────────
RENOVATION_COST = {
    "do remontu":      4150,  # полная переделка
    "do wykończenia":  3150,  # после застройщика (чистовая отделка)
    "do zamieszkania":  500,  # косметика
}

# ── Веса инвестиционного scoring (сумма = 1.0) ────────────────────────────────
SCORING_WEIGHTS = {
    "price_m2_eff": 0.40,  # эффективная цена/м² (с учётом ремонта)
    "center_dist":  0.15,  # расстояние до центра (мягкий штраф — все у метро)
    "build_year":   0.15,  # год постройки
    "floor":        0.05,  # этаж
    "poi":          0.25,  # близость к инфраструктуре (лучший прокси ликвидности)
}

# Веса внутри POI
POI_WEIGHTS = {
    "supermarket": 0.40,  # ежедневная потребность
    "school":      0.35,  # арендаторы с детьми
    "university":  0.25,  # студенты = стабильные арендаторы
}

CONDITION_SCORE = {
    "do zamieszkania": 1.0,
    "do wykończenia":  0.7,
    "do remontu":      0.5,
}
