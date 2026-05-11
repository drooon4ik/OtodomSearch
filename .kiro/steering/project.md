# OtodomSearch — Project Context

## Goal
Multi-city, multi-purpose real estate search tool built on Otodom. Supports buy and rent scenarios across Polish cities.

## Architecture: Profiles
Each search scenario is a **profile** in `profiles/{name}/`:
```
profiles/
  warsaw-buy/
    config.py    # all profile-specific parameters
    data/        # listings, enriched, scored, snapshots
  krakow-rent/
    config.py
    data/
```

Run any script with `--profile=NAME` (default: `warsaw-buy`):
```bash
python scraper.py --profile=warsaw-buy
python score.py --profile=krakow-rent
```

## Pipeline
```
scraper.py → listings.json/csv
fetch_poi.py → poi.json
enrich.py → enriched.json/csv  (+ calls tracker automatically)
score.py → scored.json/csv
tracker.py → data/snapshots/
```

## Module Responsibilities
- **profile_loader.py** — `load_profile(name)` returns (config_module, data_dir); `profile_arg()` reads `--profile=` from argv
- **config_base.py** — shared constants across all profiles: `RENOVATION_COST`, `CONDITION_SCORE`, `MATERIAL_SCORE`, `DESC_SIGNALS`
- **profiles/*/config.py** — profile-specific: city, voivodeship, transaction type, transit points, scoring weights, district scores, search params
- **metro_url.py** — builds Otodom search URL from profile; path and query params fully dynamic via `CITY`, `VOIVODESHIP`, `TRANSACTION`, `PROPERTY_TYPE`, `SEARCH_PARAMS`
- **scraper.py** — Playwright sync scraper; uses `build_url()` from metro_url, writes to profile's data dir
- **fetch_poi.py** — Overpass API for POI near transit points; writes to profile's data dir
- **enrich.py** — fetches listing details, writes enriched.json/csv, calls tracker
- **score.py** — computes investment_score using profile weights + config_base constants
- **tracker.py** — snapshots enriched.json, detects price changes / new / removed listings

## Profile Config Keys
```python
CITY, VOIVODESHIP          # e.g. "warszawa", "mazowieckie"
TRANSACTION                # "sprzedaz" | "wynajem"
PROPERTY_TYPE              # "mieszkanie"
SEARCH_PARAMS              # dict → URL query params (only present keys are added)
TRANSIT_POINTS             # list of (lat, lon) — metro stops, tram stops, etc.
RADIUS_M                   # polygon radius around each transit point
CENTER                     # (lat, lon) reference point for center_dist scoring
UNIVERSITIES               # list of {name, lat, lon}
POI_RADIUS_M, POI_EXCLUDE_NAMES
SCORING_WEIGHTS            # sum = 1.0
POI_WEIGHTS                # supermarket / school / university
DISTRICT_SCORE             # {district_name: 0.0–1.0}
DELAY_MIN, DELAY_MAX       # scraper delays in seconds
```

## Scoring Sub-scores
| Factor | Notes |
|---|---|
| price_m2_eff | price/m² + renovation cost (from config_base.RENOVATION_COST) |
| build_year | parabolic, peak 2010–2020 |
| floor | ground/top floor penalized |
| desc | balcony, loggia, terrace, quiet, two-sided (from config_base.DESC_SIGNALS) |
| district | quality-of-life per district (profile-specific) |
| center_dist | distance to CENTER point |
| poi | weighted distance to supermarket/school/university |
| material | from config_base.MATERIAL_SCORE |
| market | secondary > primary (buy profiles) |

## Conventions
- All profile parameters → `profiles/*/config.py`, never hardcode in modules
- Shared/universal constants → `config_base.py`
- `profile_loader.load_profile()` is the single entry point for config + data path
- Playwright: sync_playwright patterns in scraper.py
- Data files always in `profiles/{name}/data/`
