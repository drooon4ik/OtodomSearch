# Константы общие для всех профилей

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
    "balkon":       ("features", r"balkon",                    0.30),
    "loggia":       ("features", r"loggi",                     0.20),
    "taras":        ("features", r"taras",                     0.35),
    "komorka":      ("features", r"piwnic|kom[oó]rk",          0.20),
    "klimatyzacja": ("features", r"klimatyz",                  0.20),
    "dwustronne":   ("desc",     r"dwustronn",                 0.25),
    "ciche":        ("desc",     r"cich[ae]|spokojna|spokojn", 0.20),
}
