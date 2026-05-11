# OtodomSearch — Project Context

## Goal
Warsaw real estate investment tool. Investor context: live first → rent/sell. Horizon 10+ years. Budget ~560k zł + mortgage. Priority: capital appreciation.

## Pipeline
```
scraper.py → listings.json/csv
fetch_poi.py → poi.json
enrich.py → enriched.json/csv
score.py → scored.json/csv
tracker.py → data/snapshots/
```

## Module Responsibilities
- **config.py** — single source of truth for all parameters (weights, thresholds, station coords, district scores)
- **scraper.py** — Playwright async scraper; builds polygon URLs via `metro_url.py`, scrapes Otodom listing pages
- **metro_url.py** — generates Otodom search URLs with polygon around each metro station
- **fetch_poi.py** — queries Overpass API for POI (supermarkets, schools, universities) within `POI_RADIUS_M` of each station
- **enrich.py** — joins listings with nearest metro station + POI counts; adds `dist_to_metro`, `dist_to_center`, POI fields
- **score.py** — computes `investment_score` (0–1) using weighted sub-scores; all weights in `SCORING_WEIGHTS`
- **tracker.py** — snapshots `enriched.json` daily; detects price changes, new/removed listings

## Key Data Fields (enriched/scored)
`id`, `url`, `price`, `price_m2`, `area`, `floor`, `total_floors`, `build_year`, `condition`, `material`, `market` (primary/secondary), `district`, `features[]`, `description`, `dist_to_metro`, `dist_to_center`, `poi_supermarket`, `poi_school`, `poi_university`, `investment_score`

## Scoring Sub-scores (config.SCORING_WEIGHTS)
| Factor | Weight | Notes |
|---|---|---|
| price_m2_eff | 0.40 | price/m² + renovation cost |
| build_year | 0.10 | parabolic, peak 2010–2020 |
| floor | 0.10 | penultimate/ground floor penalized |
| desc | 0.08 | balcony, loggia, terrace, quiet, two-sided |
| district | 0.08 | quality-of-life score per district |
| center_dist | 0.08 | distance to Centrum station |
| poi | 0.06 | supermarket 0.45, university 0.35, school 0.20 |
| material | 0.05 | brick=1.0, silikat=0.8, concrete=0.7, panel=0.6 |
| market | 0.05 | secondary > primary |

## Conventions
- All parameters → `config.py`, never hardcode in modules
- Playwright: async/await patterns, use `async with async_playwright()`
- Data files in `data/`, snapshots in `data/snapshots/`
- Metro stations filtered to ≤30 min walk+metro to Centrum
