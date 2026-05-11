# ── Город ────────────────────────────────────────────────────────────────────
CITY        = "krakow"
VOIVODESHIP = "malopolskie"

# ── Параметры поиска Otodom ───────────────────────────────────────────────────
TRANSACTION   = "wynajem"
PROPERTY_TYPE = "mieszkanie"

SEARCH_PARAMS = {
    "areaMin":  45,
    "areaMax":  60,
    "extras":   ["PARKING"],  # только квартиры с паркоместом
}

# ── Скрапер ───────────────────────────────────────────────────────────────────
DELAY_MIN = 3.0
DELAY_MAX = 6.0

# ── Транзитные точки — районы с парковкой, парками и университетами ───────────
TRANSIT_POINTS = [
    # Krowodrza / Bronowice — жилые кварталы, дворовые парковки, рядом Błonia и AGH/UJ
    (50.0682, 19.9048),  # AGH / al. Mickiewicza
    (50.0720, 19.9150),  # Krowodrza Górka
    (50.0750, 19.9200),  # Bronowice Małe
    (50.0770, 19.9050),  # Bronowice Wielkie
    # Zwierzyniec / Salwator — тихий, зелёный, у Błonia и Lasu Wolskiego
    (50.0600, 19.9100),  # Salwator
    (50.0630, 19.9050),  # Zwierzyniec
    # Dębniki — правый берег Вислы, тихо, парковки есть, рядом UJ Ruczaj
    (50.0450, 19.9250),  # Dębniki centrum
    (50.0380, 19.9150),  # Ruczaj — у нового кампуса UJ
    # Grzegórzki — компромисс: близко к центру, есть парковки во дворах
    (50.0600, 19.9600),  # Rondo Grzegórzeckie
    (50.0650, 19.9700),  # Grzegórzki / Mogilska
]

# ── Центр города ──────────────────────────────────────────────────────────────
CENTER = (50.0647, 19.9450)  # Rynek Główny

# ── Университеты ─────────────────────────────────────────────────────────────
UNIVERSITIES = [
    {"name": "AGH",                                        "lat": 50.0682, "lon": 19.9048},
    {"name": "Uniwersytet Jagielloński (Collegium Novum)", "lat": 50.0614, "lon": 19.9336},
    {"name": "UJ Kampus Ruczaj",                           "lat": 50.0270, "lon": 19.9050},
    {"name": "Politechnika Krakowska",                     "lat": 50.0653, "lon": 19.9237},
    {"name": "Uniwersytet Ekonomiczny",                    "lat": 50.0680, "lon": 19.9450},
    {"name": "Akademia Sztuk Pięknych",                    "lat": 50.0620, "lon": 19.9330},
]

# ── Параметры POI ─────────────────────────────────────────────────────────────
POI_RADIUS_M      = 1500
POI_EXCLUDE_NAMES = ["żabka"]

# ── Скоринг (личное проживание: цена, парковка учтена фильтром, POI сбалансирован) ──
SCORING_WEIGHTS = {
    "price_m2_eff": 0.40,
    "center_dist":  0.08,
    "build_year":   0.07,
    "floor":        0.10,
    "poi":          0.10,  # повышен — супермаркет + университет важны
    "material":     0.05,
    "market":       0.02,
    "desc":         0.10,  # балкон/тихий двор важны для жизни
    "district":     0.08,
}

POI_WEIGHTS = {
    "supermarket": 0.40,  # ежедневные покупки
    "park":        0.35,  # прогулки — важно для жизни
    "university":  0.25,  # близость к студенческой среде
}

DISTRICT_SCORE = {
    # Топ — исторический центр, атмосфера, инфраструктура
    "Stare Miasto":     1.00,
    "Kazimierz":        0.98,
    "Zwierzyniec":      0.97,  # тихий, зелёный, у Błonia
    "Salwator":         0.95,
    # Хорошие жилые кварталы у университетов и парков
    "Krowodrza":        0.92,
    "Bronowice":        0.90,
    "Dębniki":          0.88,
    "Ruczaj":           0.85,  # современный, у кампуса UJ
    "Grzegórzki":       0.83,
    "Podgórze":         0.80,
    "Zabłocie":         0.78,
    # Норма
    "Prądnik Czerwony": 0.70,
    "Prądnik Biały":    0.68,
    "Łagiewniki":       0.65,
    # Далеко от центра
    "Nowa Huta":        0.45,
    "Mistrzejowice":    0.50,
    "Bieńczyce":        0.48,
}

# ── Полигон ───────────────────────────────────────────────────────────────────
RADIUS_M = 900
