"""
tracker.py — отслеживает изменения между прогонами.

  python3 tracker.py --profile=warsaw-buy
  python3 tracker.py --profile=warsaw-buy --save
"""
import json, re, hashlib, sys
from datetime import datetime
from pathlib import Path
from profile_loader import load_profile, profile_arg


def otodom_id(url: str) -> str:
    m = re.search(r"-(ID\w+)$", url)
    return m.group(1) if m else url


def fingerprint(item: dict) -> str | None:
    lat, lon = item.get("lat"), item.get("lon")
    if lat is None or lon is None:
        return None
    key = f"{lat:.5f}|{lon:.5f}|{item.get('area','')}|{item.get('rooms','')}|{item.get('floor','')}"
    return hashlib.md5(key.encode()).hexdigest()[:10]


def load_enriched(data_dir: Path) -> dict:
    data = json.load(open(data_dir / "enriched.json", encoding="utf-8"))
    return {otodom_id(item["url"]): {**item, "_id": otodom_id(item["url"]), "_fp": fingerprint(item)}
            for item in data}


def last_snapshot(snapshots_dir: Path) -> dict | None:
    files = sorted(snapshots_dir.glob("snapshot_*.json"))
    if not files:
        return None
    return json.load(open(files[-1], encoding="utf-8"))


def save_snapshot(current: dict, snapshots_dir: Path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = snapshots_dir / f"snapshot_{ts}.json"
    json.dump(list(current.values()), path.open("w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"Снапшот сохранён: {path}")


def compare(prev_list: list, curr: dict):
    prev = {item["_id"]: item for item in prev_list}
    prev_fps = {item["_fp"]: item for item in prev_list if item.get("_fp")}

    added_ids   = set(curr) - set(prev)
    removed_ids = set(prev) - set(curr)

    reposted, truly_new = [], []
    for oid in added_ids:
        fp = curr[oid].get("_fp")
        if fp and fp in prev_fps:
            reposted.append((prev_fps[fp], curr[oid]))
        else:
            truly_new.append(curr[oid])

    reposted_old_ids = {old["_id"] for old, _ in reposted}
    truly_gone = [prev[oid] for oid in removed_ids if oid not in reposted_old_ids]

    price_changed = [(prev[oid], curr[oid]) for oid in set(curr) & set(prev)
                     if prev[oid].get("price") != curr[oid].get("price")]

    print(f"\n{'='*55}")
    print(f"  Всего сейчас: {len(curr)}  |  Было: {len(prev)}")
    print(f"{'='*55}")
    print(f"\n🆕 Новые: {len(truly_new)}")
    for item in truly_new[:10]:
        print(f"   {item['_id']}  {item.get('price','')}  {item.get('district','')}  {item['url'][-30:]}")
    print(f"\n🔄 Пересозданные: {len(reposted)}")
    for old, new in reposted[:10]:
        print(f"   {old['_id']} → {new['_id']}  {new.get('price','')}  {new.get('district','')}")
    print(f"\n❌ Снятые: {len(truly_gone)}")
    for item in truly_gone[:10]:
        print(f"   {item['_id']}  {item.get('price','')}  {item.get('district','')}  {item['url'][-30:]}")
    print(f"\n💰 Изменилась цена: {len(price_changed)}")
    for old, new in price_changed[:10]:
        print(f"   {old['_id']}  {old.get('price','')} → {new.get('price','')}  {new.get('district','')}")
    print()


def run(current: dict | None = None, data_dir: Path | None = None):
    if data_dir is None:
        _, data_dir = load_profile(profile_arg())
    snapshots_dir = data_dir / "snapshots"
    snapshots_dir.mkdir(exist_ok=True)
    if current is None:
        current = load_enriched(data_dir)
    prev = last_snapshot(snapshots_dir)
    if prev is None:
        print("Предыдущий снапшот не найден — сохраняю текущий как базовый.")
    else:
        compare(prev, current)
    save_snapshot(current, snapshots_dir)


if __name__ == "__main__":
    _, data_dir = load_profile(profile_arg())
    if "--save" in sys.argv:
        save_snapshot(load_enriched(data_dir), data_dir / "snapshots")
    else:
        run(data_dir=data_dir)
