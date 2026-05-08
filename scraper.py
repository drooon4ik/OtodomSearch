"""
Otodom full scraper — парсит все страницы, сохраняет в CSV, сортирует по цене/м².
"""
import subprocess, json, csv, re, time, random
from playwright.sync_api import sync_playwright

DELAY_MIN = 3.0   # мин. пауза между страницами (сек)
DELAY_MAX = 6.0   # макс. пауза

import sys
single = "--single" in sys.argv
limit_arg = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--limit=")), None)
pages_arg = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--pages=")), None)
cmd = ["python3", "metro_url.py"] + (["--single"] if single else [])
result = subprocess.run(cmd, capture_output=True, text=True)
url = [l for l in result.stdout.splitlines() if l.startswith("https://")][0]
print(f"{'[TEST: одна станция — Bemowo] ' if single else ''}URL: {url[:80]}...\n")


def parse_num(text):
    digits = re.sub(r"[^\d,.]", "", text).replace(",", ".")
    try:
        return float(digits)
    except ValueError:
        return None


seen_urls = {}  # глобальная дедупликация по href

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
        price_txt = next((s for s in spans if s.endswith("zł")), "?")
        area_txt  = next((s for s in spans if s.endswith("m²") and "/" not in s), "?")
        ppm_txt   = next((s for s in spans if "zł/m²" in s), "?")
        item = {
            "price":        price_txt,
            "area":         area_txt,
            "price_m2":     ppm_txt,
            "price_m2_num": parse_num(ppm_txt),
            "url":          f"https://www.otodom.pl{href}",
        }
        seen_urls[href] = item
        new_items.append(item)

PANEL = "[data-cy='search.map.listing.organic']"

def scroll_and_collect(page):
    """Скроллит панель виртуального списка, ждёт рендера новых карточек."""
    new_items = []

    while len(new_items) < 36:
        prev_count = len(new_items)
        page.evaluate(f'document.querySelector("{PANEL}").scrollTop += 3000')
        page.wait_for_timeout(1200)  # ждём рендер виртуального списка
        collect(page, new_items)
        if len(new_items) == prev_count:
            break  # новых нет — конец списка на этой странице

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
    browser = p.chromium.launch(headless=False)
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
        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        print(f"  пауза {delay:.1f}с...", end=" ", flush=True)
        time.sleep(delay)

        pg.goto(url + f"&page={p_num}", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(2000)
        items = scroll_and_collect(pg)
        listings.extend(items)
        print(f"стр. {p_num} — {len(items)} объявлений")

    print("Пауза 20 сек...")
    time.sleep(20)
    browser.close()

listings.sort(key=lambda x: x["price_m2_num"] or float("inf"))

with open("data/listings.json", "w", encoding="utf-8") as f:
    json.dump(listings, f, ensure_ascii=False, indent=2)

with open("data/listings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["price", "area", "price_m2", "price_m2_num", "url"])
    writer.writeheader()
    writer.writerows(listings)

print(f"\nИтого: {len(listings)} объявлений → listings.json, listings.csv")
print(f"\n{'Цена':>15}  {'Площадь':>8}  {'zł/м²':>14}  Ссылка")
print("-" * 95)
for l in listings[:20]:
    print(f"{l['price']:>15}  {l['area']:>8}  {l['price_m2']:>14}  {l['url'][:55]}")
if len(listings) > 20:
    print(f"  ... ещё {len(listings) - 20}")
