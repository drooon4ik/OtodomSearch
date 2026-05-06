# Otodom Investment Search — Warsaw

Инструмент для поиска инвестиционных квартир в Варшаве с фильтрацией по транспортной доступности.

## Инвестиционная цель

Найти квартиру в Варшаве с максимальной инвестиционной привлекательностью:
- Купить на собственные ~480,000 zł + ипотека
- Сначала жить самому (экономия на аренде)
- Потом сдавать или перепродать

## Критерии отбора

| Параметр | Значение |
|---|---|
| Площадь | 40–60 м² |
| Транспорт | Только метро или трамвай |
| Пересадки | 0 (только прямой маршрут) |
| Время до центра | ≤ 30 минут |
| Тип сделки | Продажа |

Центр = Rondo Dmowskiego.

## Транспортная зона (полигон)

Полигон покрывает зону в радиусе `RADIUS_M` метров от:
- **Метро M1** (синяя) — Kabaty ↔ Młociny
- **Метро M2** (красная) — Bemowo ↔ Bródno
- **Трамвай 9** — Gocławek ↔ P+R Aleja Krakowska (al. Jerozolimskie, приоритет светофора)
- **Трамвай 15** — Marymont ↔ P+R Aleja Krakowska (Marszałkowska, приоритет светофора)
- **Трамвай 17** — Tarchomin/Winnica ↔ PKP Służewiec (al. Jana Pawła II, приоритет светофора)

Трамвайные остановки обрезаются по bbox метро (не выходят за крайние станции).

Флаги в `metro_url.py`:
```python
USE_METRO = True   # включить метро
USE_TRAMS = True   # включить трамваи 9/15/17
```

## Параметры поиска (metro_url.py)

```python
RADIUS_M      = 900     # радиус вокруг каждой станции/остановки, метры
AREA_MIN      = 35      # площадь от, м²
AREA_MAX      = 60      # площадь до, м²
YEAR_MIN      = 1950    # год постройки от
BUILDING_MATERIALS = ["BRICK", "BREEZEBLOCK", "SILIKAT", "REINFORCED_CONCRETE"]
EXTRAS        = ["GARAGE"]
TRANSACTION   = "sprzedaz"
PROPERTY_TYPE = "mieszkanie"
```

## Файлы

| Файл | Описание |
|---|---|
| `metro_url.py` | Генерирует URL для Otodom с полигоном |
| `scraper_demo.py` | Демо-парсер первой страницы Otodom (Playwright) |
| `requirements.txt` | Зависимости Python |
| `.env` | Google API ключ (не в git) |
| `listings.json` | Последний результат парсера |

## Использование

```bash
pip install -r requirements.txt
python3 metro_url.py        # генерирует URL и копирует в буфер
python3 scraper_demo.py     # парсит первую страницу → listings.json
```

## Следующий шаг (TODO)

Расширить `scraper_demo.py` до полного парсера:
1. Парсить все страницы результатов (не только первую)
2. Собирать: цена, площадь, цена/м², район, ссылка
3. Скоринг: сортировка по цене/м² (чем ниже — тем лучше)
4. Сохранять в CSV для анализа

## Установка

```bash
pip install -r requirements.txt
python3 -m playwright install chromium
```
