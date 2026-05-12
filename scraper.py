"""
Otodom scraper — парсит все страницы, сохраняет в CSV, сортирует по цене/м².
"""
import json, csv, re, time, random, sys
from playwright.sync_api import sync_playwright
from profile_loader import load_profile, profile_arg
from metro_url import build_url

cfg, data_dir = load_profile(profile_arg())

single    = "--single" in sys.argv
limit_arg = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--limit=")), None)
pages_arg = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--pages=")), None)

stations = cfg.TRANSIT_POINTS[:1] if single else list(cfg.TRANSIT_POINTS)
url, _ = build_url(cfg, stations)
print(f"{'[TEST: одна точка] ' if single else ''}URL: {url[:80]}...\n")


def parse_num(text):
    digits = re.sub(r"[^\d,.]", "", text).replace(",", ".")
    try:
        return float(digits)
    except ValueError:
        return None


seen_urls = {}

def collect(page, new_items):
    for art in page.query_selector_all("article"):
        link_el = art.query_selector("a[href*='/oferta/']")
        if not link_el:
            continue
        href = link_el.get_attribute("href")
        if not href or href in seen_urls:
            continue
        spans = [s.inner_text().strip().replace("\xa0", " ")
                 for s in art.query_selector_all("span")]
        price_txt = next((s for s in spans if s.endswith("zł") or "zł/mies" in s), "?")
        area_txt  = next((s for s in spans if s.endswith("m²") and "/" not in s), "?")
        ppm_txt   = next((s for s in spans if "zł/m²" in s), "?")
        czynsz_txt = next((s for s in spans if "czynsz" in s.lower()), "")
        rent_num   = parse_num(price_txt)
        czynsz_num = parse_num(czynsz_txt) if czynsz_txt else None
        item = {
            "price":          price_txt,
            "czynsz":         czynsz_txt,
            "rent_num":       rent_num,
            "czynsz_num":     czynsz_num,
            "total_rent_num": (rent_num + czynsz_num) if (rent_num and czynsz_num) else rent_num,
            "area":           area_txt,
            "price_m2":       ppm_txt,
            "price_m2_num":   parse_num(ppm_txt),
            "url":            f"https://www.otodom.pl{href}",
        }
        seen_urls[href] = item
        new_items.append(item)

PANEL = "[data-cy='search.map.listing.organic']"

def scroll_and_collect(page):
    new_items = []
    while len(new_items) < 36:
        prev_count = len(new_items)
        page.evaluate(f'document.querySelector("{PANEL}").scrollTop += 3000')
        page.evaluate('window.scrollBy(0, 1000)')
        page.wait_for_timeout(1200)
        collect(page, new_items)
        if len(new_items) == prev_count:
            break
    return new_items

def get_total_pages(page):
    all_btns = page.query_selector_all("button, a[aria-label]")
    nums = [int(b.inner_text().strip()) for b in all_btns if b.inner_text().strip().isdigit()]
    return max(nums) if nums else 1

def accept_cookies(page):
    try:
        btn = page.query_selector("button#onetrust-accept-btn-handler")
        if not btn:
            btn = page.query_selector("button[data-testid='accept-all-button']")
        if btn:
            btn.click()
            page.wait_for_timeout(1000)
    except Exception:
        pass


listings = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless="--headless" in sys.argv)
    pg = browser.new_page(user_agent=(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ))

    pg.goto(url, wait_until="domcontentloaded", timeout=30000)
    pg.wait_for_timeout(2000)
    accept_cookies(pg)

    items = scroll_and_collect(pg)
    total = get_total_pages(pg)
    listings.extend(items)
    print(f"Страниц: {total}")
    print(f"  стр. 1 — {len(items)} объявлений")

    for p_num in range(2, total + 1):
        if limit_arg and len(listings) >= limit_arg:
            break
        if pages_arg and p_num > pages_arg:
            break
        delay = random.uniform(cfg.DELAY_MIN, cfg.DELAY_MAX)
        print(f"  пауза {delay:.1f}с...", end=" ", flush=True)
        time.sleep(delay)

        pg.goto(url + f"&page={p_num}", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(2000)
        items = scroll_and_collect(pg)
        listings.extend(items)
        print(f"стр. {p_num} — {len(items)} объявлений")

    browser.close()

listings.sort(key=lambda x: x["price_m2_num"] or float("inf"))

with open(data_dir / "listings.json", "w", encoding="utf-8") as f:
    json.dump(listings, f, ensure_ascii=False, indent=2)

with open(data_dir / "listings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["price", "czynsz", "rent_num", "czynsz_num", "total_rent_num", "area", "price_m2", "price_m2_num", "url"])
    writer.writeheader()
    writer.writerows(listings)

print(f"\nИтого: {len(listings)} объявлений → {data_dir}/listings.json")
