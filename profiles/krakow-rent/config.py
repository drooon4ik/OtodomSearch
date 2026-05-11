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

# ── Транзитные точки — тихие зелёные районы + набережная Вислы + парки ────────
TRANSIT_POINTS = [
    # Krowodrza / Bronowice — жилые кварталы, дворовые парковки, рядом Błonia и AGH/UJ
    (50.0682, 19.9048),  # AGH / al. Mickiewicza
    (50.0720, 19.9150),  # Krowodrza Górka
    (50.0750, 19.9200),  # Bronowice Małe
    (50.0770, 19.9050),  # Bronowice Wielkie
    # Zwierzyniec / Salwator — Błonia, Las Wolski
    (50.0600, 19.9100),  # Salwator
    (50.0630, 19.9050),  # Zwierzyniec
    # Las Wolski и Park Decjusza — лесной массив к западу
    (50.0680, 19.8700),  # Las Wolski / Park Decjusza
    (50.0720, 19.8600),  # Las Wolski głębiej
    # Wola Justowska / Przegorzały — элитный, лесистый
    (50.0720, 19.8850),  # Wola Justowska centrum
    (50.0680, 19.8750),  # Przegorzały
    # Набережная Вислы — левый берег, от Zwierzyniec до Dębniki
    (50.0550, 19.9150),  # Wisła / Bielany (przy rzece)
    (50.0500, 19.9200),  # Wisła / Dębniki północ
    (50.0450, 19.9250),  # Dębniki centrum
    (50.0400, 19.9300),  # Dębniki południe / Wisła
    # Kobierzyn — тихо, зелено, Park Jerzmanowskiego
    (50.0350, 19.9100),  # Kobierzyn
    # Łagiewniki — лес, тихо
    (50.0200, 19.9350),  # Łagiewniki
    # Park Bednarskiego / Podgórze Skałka — правый берег, зелёный
    (50.0430, 19.9450),  # Park Bednarskiego
    (50.0480, 19.9530),  # Podgórze / Plac Bohaterów Getta
    # Prądnik Czerwony — долина Prądnika, зелёная
    (50.0900, 19.9600),  # Prądnik Czerwony
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
    "supermarket": 0.45,  # ежедневные покупки
    "park":        0.35,  # прогулки
    "university":  0.20,  # студенческая среда
}

DISTRICT_SCORE = {
    # Топ — тихие, зелёные, престижные
    "Wola Justowska":   1.00,  # лес, элитный, тихо
    "Przegorzały":      0.98,  # над Вислой, лесистый
    "Zwierzyniec":      0.97,  # Błonia, Las Wolski
    "Salwator":         0.95,
    # Хорошие жилые
    "Krowodrza":        0.90,
    "Bronowice":        0.88,
    "Dębniki":          0.87,
    "Kobierzyn":        0.85,  # тихо, зелено, доступно
    "Łagiewniki":       0.82,  # лес, санктуарий, тихо
    # Спальные зелёные
    "Prądnik Czerwony": 0.75,
    "Prądnik Biały":    0.73,
    # Оживлённее
    "Grzegórzki":       0.60,  # шум от Tauron Arena и трасс
    "Podgórze":         0.75,
    "Zabłocie":         0.72,
    # Туристические — шум
    "Kazimierz":        0.60,
    "Stare Miasto":     0.50,
    # Далеко
    "Nowa Huta":        0.40,
    "Mistrzejowice":    0.45,
    "Bieńczyce":        0.43,
}

# ── Полигон ───────────────────────────────────────────────────────────────────
RADIUS_M = 900
