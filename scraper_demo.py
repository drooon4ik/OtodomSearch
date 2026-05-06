"""
Otodom scraper demo — берёт URL из metro_url.py и парсит первую страницу объявлений.
Выводит: цена, площадь, цена/м², ссылка.
"""
import subprocess, json
from playwright.sync_api import sync_playwright

result = subprocess.run(["python3", "metro_url.py"], capture_output=True, text=True)
url = [l for l in result.stdout.splitlines() if l.startswith("https://")][0]
print(f"URL: {url[:80]}...\n")

listings = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent=(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ))
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)

    articles = page.query_selector_all("article[data-cy='listing-item']")
    print(f"Найдено объявлений: {len(articles)}\n")

    for art in articles:
        spans = [s.inner_text().strip().replace("\xa0", " ")
                 for s in art.query_selector_all("span")]

        price_txt = next((s for s in spans if s.endswith("zł")), "?")
        area_txt  = next((s for s in spans if s.endswith("m²") and "/" not in s), "?")
        ppm_txt   = next((s for s in spans if "zł/m²" in s), "?")

        link_el = art.query_selector("a[href*='/oferta/']")
        href    = link_el.get_attribute("href") if link_el else "?"

        listings.append({
            "price":    price_txt,
            "area":     area_txt,
            "price/m²": ppm_txt,
            "url":      f"https://www.otodom.pl{href}" if href != "?" else "?"
        })

    browser.close()

print(f"{'Цена':>15}  {'Площадь':>8}  {'zł/м²':>14}  Ссылка")
print("-" * 90)
for l in listings:
    print(f"{l['price']:>15}  {l['area']:>8}  {l['price/m²']:>14}  {l['url'][:50]}")

with open("listings.json", "w", encoding="utf-8") as f:
    json.dump(listings, f, ensure_ascii=False, indent=2)
print(f"\nСохранено в listings.json ({len(listings)} объявлений)")
