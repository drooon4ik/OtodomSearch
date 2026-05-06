# Otodom Metro Search URL Generator

Generates an Otodom.pl search URL for apartments within 700m of any Warsaw metro station (M1 + M2 lines).

## What it does

1. Draws a 700m radius circle around each of the 37 metro stations
2. Merges all circles into a single polygon using `shapely`
3. Simplifies the polygon to ≤300 points
4. Encodes it as a Google Encoded Polyline
5. Builds an Otodom search URL with the polygon as a geometry filter

## Output

- Prints the URL and point count to stdout
- Saves the URL to `otodom_metro.txt`

## Search filters (hardcoded)

- Type: sale (`sprzedaz`) / apartment (`mieszkanie`) / Warsaw
- Area: 50–60 m²
- View: map

## Usage

```bash
pip install -r requirements.txt
python metro_url.py
```

Then open the URL from `otodom_metro.txt` in a browser.

## Files

| File | Description |
|------|-------------|
| `metro_url.py` | Main script |
| `otodom_metro.txt` | Last generated URL |
