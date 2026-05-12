# ── Город ────────────────────────────────────────────────────────────────────
CITY        = "krakow"
VOIVODESHIP = "malopolskie"

# ── Параметры поиска Otodom ───────────────────────────────────────────────────
TRANSACTION   = "wynajem"
PROPERTY_TYPE = "mieszkanie"
APPLY_RENOVATION_COST = False  # для аренды ремонт не учитываем

SEARCH_PARAMS = {
    "areaMin":  45,
    "areaMax":  80,
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
    "price_m2_eff": 0.20,
    "center_dist":  0.15,  # транспортная доступность важнее для жизни
    "build_year":   0.00,
    "floor":        0.10,
    "poi":          0.18,  # супермаркет + парк + университет
    "material":     0.05,
    "market":       0.02,
    "desc":         0.18,  # балкон/тихий двор/сад важны для жизни
    "district":     0.12,  # район важен для качества жизни
}

POI_WEIGHTS = {
    "supermarket": 0.45,  # ежедневные покупки
    "park":        0.35,  # прогулки
    "university":  0.20,  # студенческая среда
}

DISTRICT_SCORE = {
    # 💎 Элитный
    "Wola Justowska":          0.98,
    "Salwator":                0.96,
    "Zwierzyniec":             0.94,
    "Zakrzówek":               0.92,
    # ✨ Высокий
    "Czarna Wieś":             0.88,
    "Stara Krowodrza":         0.89,
    "Bronowice Małe":          0.87,
    "Wesoła":                  0.88,
    "Dębniki":                 0.86,
    "Bronowice":               0.85,
    "Zabłocie":                0.82,
    # 🏙️ Современный
    "Stare Podgórze":          0.81,
    "Ludwinów":                0.81,
    "Prądnik Biały":           0.78,
    "Prądnik Czerwony":        0.78,
    # ✅ Хороший средний
    "Olsza":                   0.75,
    "Rakowice":                0.75,
    "Łobzów":                  0.73,
    "Nowa Wieś":               0.73,
    "Pychowice":               0.74,
    "Krowodrza":               0.70,
    "Krowodrza Górka":         0.71,
    "Żabiniec":                0.70,
    "Grzegórzki":              0.72,
    # 🧱 Базовый
    "Podgórze Duchackie":      0.68,
    "Bonarka":                 0.68,
    "Ruczaj":                  0.66,
    # 🏰 Исторический
    "Stare Miasto":            0.64,
    "Centrum":                 0.64,
    "Śródmieście":             0.56,
    "Nowy Świat":              0.56,
    "Kazimierz":               0.60,
    "Górka Narodowa":          0.62,
    "Azory":                   0.58,
    # 🏭 Промышленный / Удалённый
    "Łagiewniki":              0.55,
    "Łagiewniki-Borek Fałęcki":0.55,
    "Swoszowice":              0.50,
    "Borek Fałęcki":           0.48,
    # Остальные краковские
    "Podgórze":                0.69,
    "Bieżanów-Prokocim":       0.72,
    "Mistrzejowice":           0.67,
    "Bieńczyce":               0.64,
    "Czyżyny":                 0.59,
    "Nowa Huta":               0.74,
}

# ── Сигналы из объявления (дополнение к config_base.DESC_SIGNALS) ────────────
# Переопределяет config_base при наличии — score.py мёржит профильные поверх базовых
DESC_SIGNALS_EXTRA = {}

# ── Полигон ───────────────────────────────────────────────────────────────────
RADIUS_M = 900
