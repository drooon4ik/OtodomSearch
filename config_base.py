# Константы общие для всех профилей

# Комиссия агентства амортизируется на N месяцев (стандарт PL = 1 месяц аренды)
AGENCY_FEE_MONTHS = 12

# Дефолтный чинж если не указан (медиана по рынку)
DEFAULT_CZYNSZ = 800

RENOVATION_COST = {
    "do remontu":      4150,
    "do wykończenia":  3150,
    "do zamieszkania":  500,
}

CONDITION_SCORE = {
    "do zamieszkania": 1.0,
    "do wykończenia":  0.7,
    "do remontu":      0.5,
}

MATERIAL_SCORE = {
    "cegła":              1.0,
    "wielka_płyta":       0.6,
    "beton":              0.7,
    "żelbet":             0.7,
    "silikat":            0.8,
    "pustak":             0.6,
    "breezeblock":        0.6,
    "reinforced_concrete":0.7,
    "brick":              1.0,
}

DESC_SIGNALS = {
    "dwustronne":   ("desc",     r"dwustronn",                 0.50),
}
