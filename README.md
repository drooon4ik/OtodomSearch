# Otodom Investment Search

Инструмент для поиска и оценки недвижимости на Otodom. Поддерживает несколько городов и типов сделок (покупка / аренда) через систему профилей.

## Flow

```
profiles/{name}/config.py
        │
        ▼
metro_url.py → scraper.py → profiles/{name}/data/listings.json
                                        │
             fetch_poi.py →             ▼
             data/poi.json → enrich.py → enriched.json  ──→ tracker.py → snapshots/
                                        │
                                        ▼
                                   score.py → scored.json / scored.csv
```

## Профили

| Профиль | Город | Тип | Площадь |
|---|---|---|---|
| `warsaw-buy` | Варшава | покупка | 35–60 м² |
| `krakow-rent` | Краков | аренда | 45–60 м² |

Каждый профиль — отдельная папка `profiles/{name}/` со своим `config.py` и `data/`.

## Использование

```bash
pip install -r requirements.txt
python3 -m playwright install chromium

# Запуск для конкретного профиля (по умолчанию warsaw-buy)
python3 scraper.py --profile=warsaw-buy          # собрать объявления
python3 scraper.py --profile=warsaw-buy --pages=2  # тест на 2 страницах

python3 fetch_poi.py --profile=warsaw-buy        # загрузить POI из OSM (один раз)

python3 enrich.py --profile=warsaw-buy           # обогатить + вызвать tracker
python3 score.py --profile=warsaw-buy            # пересчитать скоры

python3 tracker.py --profile=warsaw-buy          # отчёт об изменениях
```

`enrich.py` автоматически вызывает `tracker.py` в конце.

## Структура проекта

```
├── config_base.py          # общие константы (ремонт, материалы, сигналы)
├── profile_loader.py       # load_profile(name) → (config, data_dir)
├── profiles/
│   ├── warsaw-buy/
│   │   ├── config.py       # параметры профиля
│   │   └── data/           # данные профиля (не в git)
│   └── krakow-rent/
│       ├── config.py
│       └── data/
├── scraper.py              # парсер Otodom (Playwright)
├── metro_url.py            # генерация URL с полигоном
├── enrich.py               # обогащение деталями + features + description
├── fetch_poi.py            # инфраструктура из OpenStreetMap
├── score.py                # инвестиционный скоринг
├── tracker.py              # отслеживание изменений между прогонами
└── .env                    # GOOGLE_API_KEY (не в git)
```

## Конфигурация профиля

Каждый `profiles/{name}/config.py` содержит:

| Параметр | Описание |
|---|---|
| `CITY`, `VOIVODESHIP` | город и воеводство для URL Otodom |
| `TRANSACTION` | `sprzedaz` или `wynajem` |
| `SEARCH_PARAMS` | словарь фильтров поиска (только нужные ключи) |
| `TRANSIT_POINTS` | координаты станций / остановок |
| `RADIUS_M` | радиус полигона вокруг каждой точки |
| `CENTER` | точка отсчёта для `center_dist` |
| `SCORING_WEIGHTS` | веса скоринга (сумма = 1.0) |
| `DISTRICT_SCORE` | качество жизни по районам |
| `DELAY_MIN/MAX` | паузы между страницами скрапера |

Общие константы (`RENOVATION_COST`, `MATERIAL_SCORE`, `DESC_SIGNALS`) — в `config_base.py`.

## Веса скоринга (warsaw-buy)

| Фактор | Вес | Примечание |
|---|---|---|
| Эффективная цена/м² | 0.40 | цена + стоимость ремонта, лог. нормализация |
| Этаж | 0.10 | партер 0.3 / 1-й 0.5 / последний 0.4 / остальные 1.0 |
| Год постройки | 0.10 | плато 2010–2020, спад к старым и строящимся |
| Расстояние до центра | 0.08 | слабый сигнал — все у метро |
| Район | 0.08 | Śródmieście 1.0 / Mokotów 0.90 / Wola 0.85 / Praga 0.65 |
| Бонусы из объявления | 0.08 | балкон, терраса, двусторонняя, тихий двор |
| Близость к POI | 0.06 | супермаркет×0.45 + университет×0.35 + школа×0.20 |
| Материал стен | 0.05 | кирпич 1.0 / силикат 0.8 / бетон 0.7 / панель 0.6 |
| Тип рынка | 0.05 | вторичный 1.0 / первичный 0.6 |

## Технические особенности Otodom

- Полигон работает **только** в `viewType=map` — в режиме листинга игнорируется
- Виртуальный список рендерится при скролле, данные уже в DOM
- Пагинация через `&page=N`, максимум 36 объявлений на странице
- `features` (балкон, лифт и др.) живут в `ad.features[]`, не в `characteristics`
- Для автоматических прогонов: `--headless` флаг в scraper.py
