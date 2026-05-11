# ── Город ────────────────────────────────────────────────────────────────────
CITY        = "krakow"
VOIVODESHIP = "malopolskie"

# ── Параметры поиска Otodom ───────────────────────────────────────────────────
TRANSACTION   = "wynajem"
PROPERTY_TYPE = "mieszkanie"

SEARCH_PARAMS = {
    "areaMin": 45,
    "areaMax": 60,
}

# ── Скрапер ───────────────────────────────────────────────────────────────────
DELAY_MIN = 3.0
DELAY_MAX = 6.0

# ── Транзитные точки (трамвай / автобус — метро в Кракове нет) ────────────────
# TODO: заполнить координатами ключевых остановок
TRANSIT_POINTS = [
    (50.0647, 19.9450),  # Rynek Główny
    (50.0614, 19.9366),  # Cracovia / al. 3 Maja
    (50.0682, 19.9048),  # AGH / al. Mickiewicza
    (50.0574, 19.9511),  # Kazimierz / Starowiślna
    (50.0780, 19.9900),  # Nowa Huta Centrum
]

# ── Центр города ──────────────────────────────────────────────────────────────
CENTER = (50.0647, 19.9450)  # Rynek Główny

# ── Университеты ─────────────────────────────────────────────────────────────
UNIVERSITIES = [
    {"name": "Uniwersytet Jagielloński",    "lat": 50.0614, "lon": 19.9336},
    {"name": "AGH",                         "lat": 50.0682, "lon": 19.9048},
    {"name": "Politechnika Krakowska",      "lat": 50.0653, "lon": 19.9237},
    {"name": "Uniwersytet Ekonomiczny",     "lat": 50.0680, "lon": 19.9450},
    {"name": "Uniwersytet Pedagogiczny",    "lat": 50.0700, "lon": 19.9380},
]

# ── Параметры POI ─────────────────────────────────────────────────────────────
POI_RADIUS_M      = 1500
POI_EXCLUDE_NAMES = ["żabka"]

# ── Скоринг (аренда: цена важнее года постройки и рынка) ─────────────────────
SCORING_WEIGHTS = {
    "price_m2_eff": 0.45,
    "center_dist":  0.10,
    "build_year":   0.05,
    "floor":        0.10,
    "poi":          0.08,
    "material":     0.04,
    "market":       0.02,
    "desc":         0.08,
    "district":     0.08,
}

POI_WEIGHTS = {
    "supermarket": 0.40,
    "school":      0.15,
    "university":  0.45,  # аренда — студенческий спрос выше
}

DISTRICT_SCORE = {
    "Stare Miasto":   1.00,
    "Kazimierz":      0.95,
    "Krowodrza":      0.85,
    "Grzegórzki":     0.85,
    "Podgórze":       0.80,
    "Bronowice":      0.75,
    "Prądnik Biały":  0.70,
    "Prądnik Czerwony": 0.70,
    "Nowa Huta":      0.60,
}

# ── Полигон ───────────────────────────────────────────────────────────────────
RADIUS_M = 800
