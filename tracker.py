"""
tracker.py — отслеживает изменения между прогонами.

Использование:
  python3 tracker.py          # сравнить enriched.json с последним снапшотом и сохранить новый
  python3 tracker.py --save   # только сохранить снапшот без сравнения (первый запуск)
"""

import json, re, hashlib, sys
from datetime import datetime
from pathlib import Path

ENRICHED = "data/enriched.json"
SNAPSHOTS_DIR = Path("data/snapshots")
SNAPSHOTS_DIR.mkdir(exist_ok=True)


def otodom_id(url: str) -> str:
    m = re.search(r"-(ID\w+)$", url)
    return m.group(1) if m else url


def fingerprint(item: dict) -> str | None:
    """Хэш по физическим характеристикам квартиры — не меняется при пересоздании объявления."""
    lat = item.get("lat")
    lon = item.get("lon")
    area = item.get("area", "")
    rooms = item.get("rooms", "")
    floor = item.get("floor", "")
    if lat is None or lon is None:
        return None
    key = f"{lat:.5f}|{lon:.5f}|{area}|{rooms}|{floor}"
    return hashlib.md5(key.encode()).hexdigest()[:10]


def load_enriched() -> dict:
    data = json.load(open(ENRICHED, encoding="utf-8"))
    result = {}
    for item in data:
        oid = otodom_id(item["url"])
        fp = fingerprint(item)
        result[oid] = {**item, "_id": oid, "_fp": fp}
    return result


def last_snapshot() -> dict | None:
    files = sorted(SNAPSHOTS_DIR.glob("snapshot_*.json"))
    if not files:
        return None
    return json.load(open(files[-1], encoding="utf-8"))


def save_snapshot(current: dict):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SNAPSHOTS_DIR / f"snapshot_{ts}.json"
    json.dump(list(current.values()), path.open("w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"Снапшот сохранён: {path}")


def compare(prev_list: list, curr: dict):
    prev = {item["_id"]: item for item in prev_list}
    prev_fps = {item["_fp"]: item for item in prev_list if item.get("_fp")}

    curr_ids = set(curr.keys())
    prev_ids = set(prev.keys())

    added_ids = curr_ids - prev_ids
    removed_ids = prev_ids - curr_ids

    # Из добавленных — найти пересозданные (fingerprint совпадает с удалённым)
    reposted = []
    truly_new = []
    for oid in added_ids:
        fp = curr[oid].get("_fp")
        if fp and fp in prev_fps:
            old = prev_fps[fp]
            reposted.append((old, curr[oid]))
        else:
            truly_new.append(curr[oid])

    reposted_old_ids = {old["_id"] for old, _ in reposted}
    truly_gone = [prev[oid] for oid in removed_ids if oid not in reposted_old_ids]

    # Изменение цены у существующих
    price_changed = []
    for oid in curr_ids & prev_ids:
        old_p = prev[oid].get("price")
        new_p = curr[oid].get("price")
        if old_p != new_p:
            price_changed.append((prev[oid], curr[oid]))

    print(f"\n{'='*55}")
    print(f"  Всего сейчас: {len(curr)}  |  Было: {len(prev)}")
    print(f"{'='*55}")

    print(f"\n🆕 Новые объявления: {len(truly_new)}")
    for item in truly_new[:10]:
        print(f"   {item['_id']}  {item.get('price','')}  {item.get('area','')}  {item.get('district','')}  {item['url'][-30:]}")

    print(f"\n🔄 Пересозданные (новый ID, то же жильё): {len(reposted)}")
    for old, new in reposted[:10]:
        print(f"   {old['_id']} → {new['_id']}  {new.get('price','')}  {new.get('area','')}  {new.get('district','')}")

    print(f"\n❌ Снятые с продажи: {len(truly_gone)}")
    for item in truly_gone[:10]:
        print(f"   {item['_id']}  {item.get('price','')}  {item.get('area','')}  {item.get('district','')}  {item['url'][-30:]}")

    print(f"\n💰 Изменилась цена: {len(price_changed)}")
    for old, new in price_changed[:10]:
        print(f"   {old['_id']}  {old.get('price','')} → {new.get('price','')}  {new.get('district','')}")

    print()


def run(current: dict | None = None):
    """Сравнить current (или загрузить из enriched.json) с последним снапшотом и сохранить новый."""
    if current is None:
        current = load_enriched()
    prev = last_snapshot()
    if prev is None:
        print("Предыдущий снапшот не найден — сохраняю текущий как базовый.")
    else:
        compare(prev, current)
    save_snapshot(current)


if __name__ == "__main__":
    if "--save" in sys.argv:
        save_snapshot(load_enriched())
    else:
        run()
