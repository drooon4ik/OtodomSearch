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

# ── Транзитные точки (ключевые трамвайные узлы привлекательных районов) ───────
TRANSIT_POINTS = [
    # Stare Miasto / centrum
    (50.0614, 19.9372),  # Teatr Bagatela (al. 3 Maja) — сердце центра
    (50.0647, 19.9450),  # Plac Wszystkich Świętych — Rynek
    # Kazimierz
    (50.0510, 19.9442),  # Plac Wolnica — центр Казимежа
    (50.0540, 19.9480),  # Starowiślna / Dietla — граница Казимежа
    # Zabłocie (Podgórze) — модный правый берег
    (50.0480, 19.9530),  # Plac Bohaterów Getta
    (50.0460, 19.9600),  # Zabłocie / Lipowa — Cricoteka
    # Grzegórzki — между центром и Płaszów
    (50.0600, 19.9600),  # Rondo Grzegórzeckie
    (50.0630, 19.9650),  # Grzegórzki / Mogilska
    # Krowodrza / Bronowice — тихие жилые кварталы у UJ/AGH
    (50.0682, 19.9048),  # AGH / al. Mickiewicza
    (50.0720, 19.9150),  # Krowodrza Górka
    (50.0750, 19.9200),  # Bronowice Małe
]

# ── Центр города ──────────────────────────────────────────────────────────────
CENTER = (50.0647, 19.9450)  # Rynek Główny

# ── Университеты ─────────────────────────────────────────────────────────────
UNIVERSITIES = [
    {"name": "Uniwersytet Jagielloński (Collegium Novum)", "lat": 50.0614, "lon": 19.9336},
    {"name": "UJ Kampus Ruczaj",                           "lat": 50.0270, "lon": 19.9050},
    {"name": "AGH",                                        "lat": 50.0682, "lon": 19.9048},
    {"name": "Politechnika Krakowska",                     "lat": 50.0653, "lon": 19.9237},
    {"name": "Uniwersytet Ekonomiczny",                    "lat": 50.0680, "lon": 19.9450},
    {"name": "Akademia Sztuk Pięknych",                    "lat": 50.0620, "lon": 19.9330},
]

# ── Параметры POI ─────────────────────────────────────────────────────────────
POI_RADIUS_M      = 1500
POI_EXCLUDE_NAMES = ["żabka"]

# ── Скоринг (аренда: цена и локация важнее года постройки и рынка) ────────────
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
    "university":  0.45,  # студенческий спрос — главный драйвер аренды
}

DISTRICT_SCORE = {
    # Топ — исторический центр и модные кварталы
    "Stare Miasto":    1.00,
    "Kazimierz":       0.98,
    "Zabłocie":        0.90,  # быстро растёт, молодёжь/творческие
    "Podgórze":        0.88,
    # Хорошие жилые кварталы у университетов
    "Krowodrza":       0.88,
    "Bronowice":       0.85,
    "Grzegórzki":      0.85,
    "Zwierzyniec":     0.85,  # тихий, зелёный, у Błonia
    # Норма
    "Prądnik Czerwony": 0.72,
    "Prądnik Biały":   0.68,
    "Dębniki":         0.75,
    "Łagiewniki":      0.65,
    # Далеко / промышленные
    "Nowa Huta":       0.50,
    "Mistrzejowice":   0.55,
    "Bieńczyce":       0.52,
}

# ── Полигон ───────────────────────────────────────────────────────────────────
RADIUS_M = 800
