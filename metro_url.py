import math, urllib.parse
from shapely.geometry import Polygon
from shapely.ops import unary_union

STATIONS = [
    # M2 (red)
    (52.2392071, 20.9154991),  # Bemowo
    (52.2403314, 20.9298652),  # Ulrychów
    (52.2391822, 20.9443771),  # Księcia Janusza
    (52.2376624, 20.9601048),  # Młynów
    (52.2324542, 20.9663847),  # Płocka
    (52.2300827, 20.9828946),  # Rondo Daszyńskiego
    (52.2310069, 21.0101860),  # Centrum
    (52.2350954, 21.0078988),  # Świętokrzyska
    (52.2368196, 21.0168168),  # Nowy Świat-Uniwersytet
    (52.2399148, 21.0317878),  # Centrum Nauki Kopernik
    (52.2468346, 21.0428470),  # Stadion Narodowy
    (52.2537771, 21.0357972),  # Dworzec Wileński
    (52.2634709, 21.0455232),  # Szwedzka
    (52.2692518, 21.0513658),  # Targówek Mieszkaniowy
    (52.2751021, 21.0550586),  # Trocka
    (52.2837496, 21.0621480),  # Zacisze
    (52.2935850, 21.0289387),  # Bródno
    # M1 (blue)
    (52.1320765, 21.0650711),  # Kabaty
    (52.1411007, 21.0564351),  # Natolin
    (52.1493000, 21.0461062),  # Imielin
    (52.1560759, 21.0347233),  # Stokłosy
    (52.1620456, 21.0276283),  # Ursynów
    (52.1727624, 21.0262866),  # Służew
    (52.1818168, 21.0231452),  # Wilanowska
    (52.1898719, 21.0167966),  # Wierzbno
    (52.1988637, 21.0122349),  # Racławicka
    (52.2087775, 21.0079298),  # Pole Mokotowskie
    (52.2186581, 21.0153031),  # Politechnika
    (52.2310069, 21.0101860),  # Centrum (wspólna)
    (52.2452163, 21.0008823),  # Ratusz-Arsenał
    (52.2580586, 20.9941857),  # Dworzec Gdański
    (52.2692619, 20.9844973),  # Plac Wilsona
    (52.2715768, 20.9719399),  # Marymont
    (52.2768261, 20.9601259),  # Słodowiec
    (52.2818277, 20.9493511),  # Stare Bielany
    (52.2863474, 20.9395150),  # Wawrzyszew
    (52.2907703, 20.9298678),  # Młociny
]

RADIUS_M = 700
TARGET_POINTS = 300
AREA_MIN = 50
AREA_MAX = 60

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
    # Convert all to integer units first
    ipts = [(round(lat * 1e5), round(lng * 1e5)) for lat, lng in points]
    for ilat, ilng in ipts:
        res += enc(ilat - pl) + enc(ilng - pn)
        pl, pn = ilat, ilng
    # Close: delta back to first point
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

    params = (
        f"limit=36&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=map"
        f"&areaMin={AREA_MIN}&areaMax={AREA_MAX}"
        f"&mapBounds={urllib.parse.quote(bbox)}&geometry={urllib.parse.quote(encoded)}"
    )
    return (f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?{params}",
            len(coords))

url, pts = build_url(STATIONS)
print(f"Points: {pts}")
print(url)

with open("otodom_metro.txt", "w") as f:
    f.write(url + "\n")
print("Saved to otodom_metro.txt")
