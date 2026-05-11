# OtodomSearch — Project Context

## Goal
Multi-city, multi-purpose real estate search tool built on Otodom. Supports buy and rent scenarios across Polish cities.

## Architecture: Profiles
Each search scenario is a **profile** in `profiles/{name}/`:
```
profiles/
  warsaw-buy/    # покупка, Варшава, метро M1+M2
  krakow-rent/   # аренда, Краков, тихие зелёные районы с паркоместом
```

Run any script with `--profile=NAME` (default: `warsaw-buy`):
```bash
./run.sh warsaw-buy          # полный прогон
./run.sh krakow-rent
python3 scraper.py --profile=warsaw-buy --headless  # без GUI
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
- **config_base.py** — shared constants: `RENOVATION_COST`, `CONDITION_SCORE`, `MATERIAL_SCORE`, `DESC_SIGNALS`
- **profiles/*/config.py** — all profile-specific parameters
- **metro_url.py** — builds Otodom search URL; path and query params fully dynamic from profile
- **scraper.py** — Playwright sync scraper; `--headless` flag for automated runs; price parsing handles both `zł` (buy) and `zł/mies.` (rent) formats
- **fetch_poi.py** — Overpass API; categories driven by `POI_WEIGHTS` keys in profile (supermarket, park, school, university)
- **enrich.py** — fetches listing details, writes enriched.json/csv, calls tracker
- **score.py** — computes score using profile weights; `APPLY_RENOVATION_COST=False` skips renovation cost for rent profiles; `DESC_SIGNALS_EXTRA` in profile merges with base signals
- **tracker.py** — snapshots enriched.json, detects price changes / new / removed listings

## Profile Config Keys
```python
CITY, VOIVODESHIP              # URL path components
TRANSACTION                    # "sprzedaz" | "wynajem"
PROPERTY_TYPE                  # "mieszkanie"
APPLY_RENOVATION_COST          # True (buy) | False (rent)
SEARCH_PARAMS                  # dict → URL query params
TRANSIT_POINTS                 # list of (lat, lon)
RADIUS_M                       # polygon radius per point
CENTER                         # (lat, lon) reference for center_dist
UNIVERSITIES                   # list of {name, lat, lon}
POI_RADIUS_M, POI_EXCLUDE_NAMES
SCORING_WEIGHTS                # sum = 1.0
POI_WEIGHTS                    # {category: weight} — drives both fetch_poi and score
DISTRICT_SCORE                 # {district_name: 0.0–1.0}
DESC_SIGNALS_EXTRA             # optional profile-specific desc signals (merged over base)
DELAY_MIN, DELAY_MAX
```

## Key Scoring Notes
- `price_m2_eff`: for buy = (price + reno*area)/area; for rent = price/area (no reno)
- Floor: ground/1st floor with garden (`ogródek` in features/desc) → score 1.0 instead of penalty
- POI scoring is fully dynamic — iterates `POI_WEIGHTS` keys, works with any categories
- `DESC_SIGNALS_EXTRA` in profile merges with `config_base.DESC_SIGNALS`

## Conventions
- All profile parameters → `profiles/*/config.py`
- Shared constants → `config_base.py`
- `profile_loader.load_profile()` is the single entry point
- Playwright: sync_playwright, `--headless` flag in scraper
- Data always in `profiles/{name}/data/`
- After structural changes → update this file
