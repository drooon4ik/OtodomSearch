import math, urllib.parse, sys, subprocess
from shapely.geometry import Polygon
from shapely.ops import unary_union
from config import (METRO_STATIONS, RADIUS_M, AREA_MIN, AREA_MAX, YEAR_MIN,
                    BUILDING_MATERIALS, EXTRAS, TRANSACTION, PROPERTY_TYPE,
                    SORT_BY, SORT_DIR)

TARGET_POINTS = 200  # макс. точек в полигоне (технический параметр)


def make_circle(lat, lon, n=32):
    lat_deg = RADIUS_M / 111320
    lon_deg = RADIUS_M / (111320 * math.cos(math.radians(lat)))
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


def build_url(stations):
    union = unary_union([make_circle(lat, lon) for lat, lon in stations])
    if union.geom_type != 'Polygon':
        for buf in [0.001, 0.003, 0.005, 0.01]:
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

    materials = urllib.parse.quote("[" + ",".join(BUILDING_MATERIALS) + "]")
    extras    = urllib.parse.quote("[" + ",".join(EXTRAS) + "]")
    params = (
        f"limit=36&ownerTypeSingleSelect=ALL&by={SORT_BY}&direction={SORT_DIR}&viewType=map"
        f"&areaMin={AREA_MIN}&areaMax={AREA_MAX}"
        f"&buildYearMin={YEAR_MIN}"
        f"&buildingMaterial={materials}"
        f"&extras={extras}"
        f"&mapBounds={urllib.parse.quote(bbox)}&geometry={urllib.parse.quote(encoded)}"
    )
    return (f"https://www.otodom.pl/pl/wyniki/{TRANSACTION}/{PROPERTY_TYPE}/mazowieckie/warszawa/warszawa/warszawa?{params}",
            len(coords))


stations = METRO_STATIONS[:1] if "--single" in sys.argv else list(METRO_STATIONS)

url, pts = build_url(stations)
print(f"Points: {pts}")
print(url)

subprocess.run("pbcopy", input=url.encode(), check=True)
print("URL copied to clipboard")
