import math, urllib.parse, sys, subprocess
from shapely.geometry import Polygon
from shapely.ops import unary_union
from profile_loader import load_profile, profile_arg

TARGET_POINTS = 200


def make_circle(lat, lon, radius_m, n=32):
    lat_deg = radius_m / 111320
    lon_deg = radius_m / (111320 * math.cos(math.radians(lat)))
    return Polygon([(lon + lon_deg * math.sin(2*math.pi*i/n),
                     lat + lat_deg * math.cos(2*math.pi*i/n)) for i in range(n)])


def encode_polyline(points):
    def enc(v):
        v = v << 1
        if v < 0: v = ~v
        s = ''
        while v >= 0x20:
            s += chr((0x20 | (v & 0x1f)) + 63); v >>= 5
        return s + chr(v + 63)
    res = ''
    pl, pn = 0, 0
    ipts = [(round(lat * 1e5), round(lng * 1e5)) for lat, lng in points]
    for ilat, ilng in ipts:
        res += enc(ilat - pl) + enc(ilng - pn)
        pl, pn = ilat, ilng
    res += enc(ipts[0][0] - pl) + enc(ipts[0][1] - pn)
    return res


def build_url(cfg, stations):
    union = unary_union([make_circle(lat, lon, cfg.RADIUS_M) for lat, lon in stations])
    if union.geom_type != 'Polygon':
        for buf in [0.0001, 0.0003, 0.0005, 0.001, 0.003, 0.005, 0.01]:
            merged = union.buffer(buf).buffer(-buf)
            if merged.geom_type == 'Polygon':
                union = merged
                break
        else:
            union = union.convex_hull

    tol = 0.0001
    coords = [(y, x) for x, y in union.exterior.coords]
    for _ in range(30):
        s = union.simplify(tol)
        if s.geom_type == 'Polygon':
            c = [(y, x) for x, y in s.exterior.coords]
            coords = c
            if len(c) <= TARGET_POINTS:
                break
        tol *= 1.5

    def signed_area(pts):
        return sum((pts[i][1]-pts[i-1][1])*(pts[i][0]+pts[i-1][0]) for i in range(len(pts))) / 2
    if signed_area(coords) < 0:
        coords = coords[::-1]

    coords = coords[:-1]
    encoded = encode_polyline(coords)
    lats = [p[0] for p in coords]; lons = [p[1] for p in coords]
    bbox = f"{min(lons)},{max(lats)},{max(lons)},{min(lats)}"

    # Строим параметры из SEARCH_PARAMS профиля
    sp = cfg.SEARCH_PARAMS
    parts = ["ownerTypeSingleSelect=ALL", "viewType=map"]
    for key, val in sp.items():
        if isinstance(val, list):
            parts.append(f"{key}={urllib.parse.quote('[' + ','.join(val) + ']')}")
        else:
            parts.append(f"{key}={val}")
    parts.append(f"mapBounds={urllib.parse.quote(bbox)}")
    parts.append(f"geometry={urllib.parse.quote(encoded)}")

    city = cfg.CITY
    voi  = cfg.VOIVODESHIP
    base = (f"https://www.otodom.pl/pl/wyniki/{cfg.TRANSACTION}/{cfg.PROPERTY_TYPE}"
            f"/{voi}/{city}/{city}/{city}")
    return f"{base}?{'&'.join(parts)}", len(coords)


if __name__ == "__main__":
    cfg, _ = load_profile(profile_arg())
    stations = cfg.TRANSIT_POINTS[:1] if "--single" in sys.argv else list(cfg.TRANSIT_POINTS)
    url, pts = build_url(cfg, stations)
    print(f"Points: {pts}")
    print(url)
    subprocess.run("pbcopy", input=url.encode(), check=True)
    print("URL copied to clipboard")
