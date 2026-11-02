"""from_image.py config for "Greyhawk HD.png" (flat-colour Flanaess map with an adventure key).

Flat colours make this easy: every pixel is matched to the palette below, symbols and text (black,
white, red) do not vote, and each 8 px block takes the most common class.
"""
from collections import Counter

from PIL import Image

TITLE = "The Flanaess (World of Greyhawk, adventure map)"
CROP = (0, 0, 3201, 2398)            # the key below y 2400 is not map
WORK = 3                             # provinces are grown on a 1/3 size grid
PLAYERS = 12
LAND_SP, SEA_SP = 52, 80             # province spacing on the work grid

CLASSES = ["sea", "forest", "plains", "hills", "mountains", "waste", "swamp", "frame", "desert", "jungle", "ice"]
PALETTE = {
    "sea": [(0, 150, 255), (0, 205, 255), (152, 255, 253), (107, 255, 254), (0, 145, 254)],
    "plains": [(178, 255, 149), (173, 255, 142)],
    "forest": [(104, 255, 104), (0, 188, 188), (0, 189, 189)],
    "hills": [(254, 202, 0)],
    "mountains": [(215, 172, 64), (216, 173, 65), (218, 174, 58), (209, 183, 52)],
    "desert": [(255, 230, 148), (255, 228, 141)],
    "waste": [(178, 153, 63), (187, 108, 0), (190, 105, 0)],
    "swamp": [(146, 255, 0)],
    "jungle": [(111, 135, 80)],
    "ice": [(185, 187, 184)],
}
# how each class plays: province terrain kind, and extra mask bits (colder 2^31, warmer 2^30)
TERRAIN_OF = {"plains": "plain", "forest": "forest", "jungle": "forest", "hills": "highland",
              "mountains": "mountain", "waste": "waste", "desert": "waste", "ice": "waste",
              "swamp": "swamp", "sea": "plain", "frame": "plain"}
EXTRA_BITS = {"ice": 2 ** 31, "jungle": 2 ** 30, "desert": 2 ** 30}
BLOCK = 8
RIVER_COLOURS = [(0, 150, 255), (0, 145, 254), (0, 205, 255)]
CITY_COLOUR = (254, 255, 107)        # the yellow inside every town and capital symbol


def classify_image(im):
    W, H = im.size
    lut = {}
    for c, cols in PALETTE.items():
        for col in cols:
            lut[col] = CLASSES.index(c)
    data = im.getdata()
    gw, gh = W // BLOCK, H // BLOCK
    grid = [[0] * gw for _ in range(gh)]
    plains = CLASSES.index("plains")
    for by in range(gh):
        for bx in range(gw):
            votes = Counter()
            for j in range(0, BLOCK, 2):
                base = (by * BLOCK + j) * W + bx * BLOCK
                for i in range(0, BLOCK, 2):
                    c = lut.get(data[base + i])
                    if c is not None:
                        votes[c] += 1
            grid[by][bx] = votes.most_common(1)[0][0] if votes else -1
    # blocks of pure symbol (black hatching, text) take their neighbours' class
    for _ in range(6):
        todo = False
        for by in range(gh):
            for bx in range(gw):
                if grid[by][bx] < 0:
                    nb = Counter(grid[y][x] for y in (by - 1, by, by + 1) for x in (bx - 1, bx, bx + 1)
                                 if 0 <= y < gh and 0 <= x < gw and grid[y][x] >= 0)
                    if nb:
                        grid[by][bx] = nb.most_common(1)[0][0]
                    else:
                        todo = True
        if not todo:
            break
    for row in grid:
        for i, v in enumerate(row):
            if v < 0:
                row[i] = plains
    return grid, (W, H)


def water_mask(im):
    """255 where the picture is water-coloured."""
    seacols = set(PALETTE["sea"])
    return Image.frombytes("L", im.size, bytes(255 if p in seacols else 0 for p in im.getdata()))


def river_mask(im):
    rc = set(RIVER_COLOURS)
    return Image.frombytes("L", im.size, bytes(255 if p in rc else 0 for p in im.getdata()))


def find_cities(im):
    """Town and capital symbols: clusters of the yellow fill. A town is one yellow ring; a capital
    star splits its yellow into several wedges."""
    W, H = im.size
    data = im.getdata()
    yel = bytearray(1 if p == CITY_COLOUR else 0 for p in data)
    seen = bytearray(W * H)
    pieces = []
    for s in range(W * H):
        if not yel[s] or seen[s]:
            continue
        seen[s] = 1
        q, pts = [s], []
        while q:
            i = q.pop()
            pts.append(i)
            x = i % W
            for j in ((i - 1) if x else -1, (i + 1) if x < W - 1 else -1, i - W, i + W):
                if 0 <= j < W * H and yel[j] and not seen[j]:
                    seen[j] = 1
                    q.append(j)
        xs = [i % W for i in pts]
        ys = [i // W for i in pts]
        if max(xs) - min(xs) <= 14 and max(ys) - min(ys) <= 14:
            pieces.append((sum(xs) / len(xs), sum(ys) / len(ys), len(pts)))
    cities = []
    used = [False] * len(pieces)
    for a, (x, y, n) in enumerate(pieces):
        if used[a]:
            continue
        group = [b for b, (u, v, _) in enumerate(pieces) if not used[b] and abs(u - x) <= 7 and abs(v - y) <= 7]
        for b in group:
            used[b] = True
        gx = sum(pieces[b][0] for b in group) / len(group)
        gy = sum(pieces[b][1] for b in group) / len(group)
        if sum(pieces[b][2] for b in group) >= 6:
            cities.append((round(gx), round(gy), "capital" if len(group) >= 3 else "town"))
    return cities


NAMES = [
    # realms and lands
    ("Kingdom of Furyondy", 1272, 930), ("Kingdom of Keoland", 940, 1560), ("The Great Kingdom", 2524, 1355),
    ("Kingdom of Nyrond", 2067, 1000), ("Iuz", 1312, 500), ("Ket", 630, 895), ("Veluna", 910, 1100),
    ("Bissel", 760, 1165), ("Perrenland", 700, 630), ("Caliphate of Ekbir", 265, 655),
    ("Sultinate of Zeif", 95, 795), ("Plains of the Paynims", 200, 995), ("Ull", 155, 1215),
    ("Gran March", 850, 1290), ("Geoff", 520, 1312), ("Sterich", 565, 1550), ("Celene", 1187, 1335),
    ("Duchy of Ulek", 975, 1390), ("County of Ulek", 1117, 1490), ("Principality of Ulek", 1257, 1580),
    ("The Pomarj", 1407, 1550), ("Wild Coast", 1352, 1300), ("Duchy of Urnst", 1682, 1150),
    ("County of Urnst", 1887, 960), ("Shield Lands", 1530, 810), ("Horned Society", 1452, 720),
    ("Bandit Kingdoms", 1682, 675), ("Tenh", 1987, 615), ("Theocracy of the Pale", 2204, 735),
    ("Ratik", 2474, 680), ("Bone March", 2474, 855), ("North Province", 2739, 952), ("South Province", 2236, 1600),
    ("Ahlissa", 2204, 1560), ("Onnwal", 1882, 1610), ("Idee", 2154, 1745), ("County of Sundi", 2439, 1780),
    ("Sea Barons", 3149, 1340), ("Lordship of the Isles", 2609, 1955), ("Lendore Isles", 3134, 1740),
    ("The Scarlet Brotherhood", 2172, 2217), ("The Yeomanry", 725, 1755), ("Hold of the Sea Princes", 900, 1900),
    ("Hold of Stonefist", 2080, 115), ("Frost Barbarians", 2479, 370), ("Snow Barbarians", 2889, 310),
    ("Ice Barbarians", 3024, 55), ("Blackmoor", 1222, 90), ("Wolf Nomads", 980, 355), ("Tiger Nomads", 545, 295),
    ("The Barrens", 1692, 390), ("Valley of the Mage", 470, 1225), ("Land of Black Ice", 660, 15),
    ("Dry Steppes", 180, 1675), ("Sea of Dust", 195, 2115), ("Amedio Jungle", 1127, 2375),
    ("Hepmonaland", 2554, 2390), ("Olman Islands", 1657, 2378),
    # forests
    ("Vesve Forest", 1052, 743), ("Fellreev Forest", 1667, 545), ("Burneal Forest", 660, 180),
    ("Bramblewood Forest", 650, 960), ("Dim Forest", 665, 1235), ("Dreadwood", 960, 1670),
    ("Celadon Forest", 1937, 1230), ("Gamboge Forest", 2164, 870), ("Adri Forest", 2474, 1170),
    ("The Grandwood Forest", 2849, 1425), ("Rieuwood", 2284, 1730), ("Udgru Forest", 330, 530),
    ("Hornwood", 480, 1405), ("Phostwood", 1997, 705), ("Forlorn Forest", 1847, 300), ("Gnarley Forest", 1327, 1160),
    ("Welkwood", 1277, 1265), ("Suss Forest", 1317, 1488), ("Oyt Wood", 590, 1365), ("Menowood", 2304, 1825),
    ("Hraak Forest", 2329, 225), ("Sable Wood", 3149, 125), ("Spikey Forest", 2734, 275),
    ("Timberway Forest", 2334, 550), ("Loftwood", 2564, 755), ("Tangles", 1677, 740),
    # mountains, hills, marsh, desert
    ("Yatil Mountains", 490, 460), ("Rakers", 2344, 690), ("Griff Mountains", 2204, 430),
    ("Corusk Mountains", 2704, 150), ("Barrier Peaks", 480, 1150), ("Crystalmist Mountains", 380, 1480),
    ("Lortmil Mountains", 960, 1260), ("Sulhaut Mountains", 160, 1905), ("Hellfurnaces", 720, 1980),
    ("Spine Ridge", 2374, 2110), ("Yecha Hills", 350, 375), ("Mounds of Dawn", 700, 570),
    ("Sepia Uplands", 960, 550), ("Tusman Hills", 480, 885), ("Lorridges", 840, 1125), ("Stark Mounds", 610, 1475),
    ("Good Hills", 755, 1510), ("Little Hills", 825, 1710), ("Kron Hills", 1127, 1225), ("Cairn Hills", 1542, 1090),
    ("Abbor-Alz", 1527, 1250), ("Drachensgrab Hills", 1467, 1585), ("Flinty Hills", 2269, 978),
    ("Blemu Hills", 2424, 940), ("Bluff Hills", 1882, 500), ("Howling Hills", 1337, 370), ("Gull Cliffs", 2959, 1270),
    ("Iron Hills", 2140, 1680), ("The Headlands", 1967, 1690), ("Hestmark Highlands", 2574, 1745),
    ("Bright Desert", 1652, 1335), ("Rift Canyon", 1747, 812), ("Cold Marshes", 1327, 260), ("Troll Fens", 2184, 575),
    ("Rushmoors", 750, 1390), ("Hool Marshes", 770, 1855), ("Gnatmarsh", 1897, 1348), ("Vast Swamp", 2464, 1880),
    ("Lone Heath", 2989, 1410), ("Pelisso Swamp", 2654, 2330),
    ("Jetsam Island", 1107, 1808), ("Fairwind Isle", 1142, 1838), ("Flotsam Island", 1082, 1890),
    # water
    ("Nyr Dyv", 1567, 940), ("Lake Quag", 735, 515), ("Whyestil Lake", 1302, 700), ("Azure Sea", 1352, 1845),
    ("Sea of Gearnat", 1892, 1550), ("Relmor Bay", 2110, 1420), ("Woolly Bay", 1490, 1400),
    ("Aerdi Sea", 2779, 1785), ("Spindrift Sound", 3064, 1590), ("Solonor Ocean", 2774, 660),
    ("Grendep Bay", 2734, 520), ("Dramidj Ocean", 80, 80), ("White Fanged Bay", 1937, 225), ("Icy Sea", 1675, 60),
    ("Jerlea Bay", 1010, 2090), ("Densac Gulf", 1857, 2320), ("Oljatt Sea", 3034, 2200), ("Tilva Strait", 2374, 2320),
]
WATER_NAMES = {"Nyr Dyv", "Lake Quag", "Whyestil Lake", "Azure Sea", "Sea of Gearnat", "Relmor Bay", "Woolly Bay",
               "Aerdi Sea", "Spindrift Sound", "Solonor Ocean", "Grendep Bay", "Dramidj Ocean", "White Fanged Bay",
               "Icy Sea", "Jerlea Bay", "Densac Gulf", "Oljatt Sea", "Tilva Strait"}
NAME_TERRAIN = [(("Forest", "wood", "Wood", "Tangles", "Jungle", "Hepmonaland"), "forest", "forest", 0.12),
                (("Mountains", "Peaks", "Rakers", "Hellfurnaces", "Ridge"), "mountain", "mountains", 0.2),
                (("Hills", "Highlands", "Mounds", "Cliffs", "Abbor-Alz", "Uplands", "Lorridges", "Headlands"),
                 "highland", "hills", 0.0),
                (("Marsh", "Swamp", "moors", "Fens"), "swamp", "swamp", 0.1),
                (("Steppes", "Desert", "Heath", "Canyon", "Dust", "Barrens", "Black Ice"), "waste", "desert", 0.1)]

# the numbered adventure boxes and the key at the bottom of the picture
SITES = [
    (1, 1477, 1155, "Domain of Greyhawk: Castle Greyhawk, Greyhawk Ruins"),
    (2, 1567, 1202, "Mordenkainen's Fantastic Adventure (Maure Castle)"),
    (3, 1752, 1282, "Abbor-Alz Hills: Ghost Tower of Inverness, Star Cairns"),
    (4, 1595, 1338, "Rary the Traitor"),
    (5, 1592, 812, "White Plume Mountain"),
    (6, 1227, 1190, "Village of Hommlet, Temple of Elemental Evil"),
    (7, 1392, 620, "Empire of Iuz: City of Skulls, Border Watch"),
    (8, 1927, 325, "Five Shall Be One, Howl From The North"),
    (9, 770, 790, "Perrenland: Lost Caverns of Tsojcanth"),
    (10, 488, 1183, "Barrier Peaks: Expedition to the Barrier Peaks, Vale of the Mage"),
    (11, 1352, 1133, "Puppets"),
    (12, 805, 1367, "Against The Cult Of The Reptile God"),
    (13, 1040, 1690, "Sinister Secret of Saltmarsh"),
    (14, 1452, 1528, "Slave Lords: Darkshelf Quarry, Slave Pits of the Undercity"),
    (15, 975, 1907, "Holds of the Sea Princes: Beyond The Crystal Cave, The Sentinel"),
    (16, 640, 1790, "The Yeomanry: Keep on the Borderlands, Gargoyle"),
    (17, 455, 1328, "Duchy of Geoff: Steading of the Hill Giant Chief"),
    (18, 355, 1473, "Glacial Rift of the Frost Giant Jarl"),
    (19, 660, 2008, "Hall of the Fire Giant King"),
    (20, 1172, 2277, "Hidden Shrine of Tamoachan"),
    (21, 2194, 658, "Theocracy of the Pale: In Search of the Unknown, The Fright at Tristor"),
    (22, 2274, 1670, "Tomb of Horrors"),
    (23, 2519, 2310, "Dwellers of the Forbidden City"),
    (24, 2734, 2025, "Lendore Isles: Secret of Bone Hill, The Assassins Knot, Deep Dwarven Delve"),
    (26, 1205, 1575, "The Shattered Circle"),
    (26, 2107, 1690, "The Shattered Circle"),
]
