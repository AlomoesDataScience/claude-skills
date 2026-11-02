"""Sort the Greyhawk picture's pixels into terrain classes (blur, nearest sampled colour, block vote)."""
from collections import Counter
from PIL import Image, ImageFilter

CLASSES = ["sea", "forest", "plains", "hills", "mountains", "waste", "swamp", "frame"]
# blurred colours sampled at spots whose terrain is clear on the map
PROTO = {"sea": [(68, 133, 180), (98, 142, 176), (111, 145, 176), (78, 127, 166), (102, 136, 166), (128, 176, 209)],
         "forest": [(92, 150, 93), (105, 156, 110), (85, 145, 85), (78, 140, 81)],
         "plains": [(200, 213, 159), (175, 206, 175), (189, 190, 151), (206, 221, 171), (171, 205, 152), (191, 213, 148)],
         "hills": [(230, 225, 158), (200, 186, 155), (220, 207, 171)],
         "mountains": [(189, 166, 135), (182, 144, 101), (154, 123, 87), (164, 159, 142)],
         "waste": [(229, 220, 174), (210, 204, 181)],
         "swamp": [(186, 205, 190), (176, 191, 178)],
         "frame": []}
BLOCK = 8


def feat(c):
    r, g, b = c
    return (r - g, g - b, (r + g + b) / 3, b - r)


def classify(path):
    return classify_image(Image.open(path).convert("RGB"))


def classify_image(im):
    W, H = im.size
    bl = im.filter(ImageFilter.BoxBlur(6))
    protos = [(feat(c), i) for i, k in enumerate(CLASSES) for c in PROTO[k]]
    cache = {}

    def near(c):
        c = (c[0] // 4 * 4, c[1] // 4 * 4, c[2] // 4 * 4)
        if c not in cache:
            f = feat(c)
            cache[c] = min(protos, key=lambda p: (p[0][0] - f[0]) ** 2 + (p[0][1] - f[1]) ** 2
                           + 0.3 * (p[0][2] - f[2]) ** 2 + (p[0][3] - f[3]) ** 2)[1]
        return cache[c]

    px = bl.load()
    gw, gh = W // BLOCK, H // BLOCK
    grid = []
    for by in range(gh):
        row = []
        for bx in range(gw):
            votes = Counter(near(px[bx * BLOCK + i, by * BLOCK + j]) for i in (1, 4, 7) for j in (1, 4, 7))
            row.append(votes.most_common(1)[0][0])
        grid.append(row)
    # fill forests hollowed out by their text labels
    fo = CLASSES.index("forest")
    for _ in range(3):
        new = [row[:] for row in grid]
        for y in range(1, gh - 1):
            for x in range(1, gw - 1):
                if grid[y][x] != fo and sum(grid[y + j][x + i] == fo for i in (-1, 0, 1) for j in (-1, 0, 1)) >= 5:
                    new[y][x] = fo
        grid = new
    # the picture frame: a few pixels at the left and right edge
    for row in grid:
        row[0] = row[-1] = CLASSES.index("frame")
    return grid, (W, H)


TITLE = "The Flanaess (World of Greyhawk)"
NAME_SCALE_W = 1920          # NAMES are in picture pixels (1920 wide), read off the labels
# (name, x, y) in priority order: realms first, then forests, mountains and hills, then small
# features. Every label seeds a province unless an earlier one is too close (then it only names
# the province it falls in, if that one has no name yet).
NAMES = [
    # realms and lands
    ("Kingdom of Furyondy", 813, 473), ("Kingdom of Keoland", 667, 817), ("The Great Kingdom", 1477, 683),
    ("Kingdom of Nyrond", 1200, 513), ("Iuz", 810, 203), ("Ket", 480, 413), ("Veluna", 627, 513),
    ("Bissel", 533, 567), ("Perrenland", 527, 270), ("Sultanate of Ekbir", 293, 277),
    ("Pashalik of Tusmit", 353, 347), ("Sultanate of Zeif", 187, 360), ("Ull", 220, 600),
    ("Gran March", 577, 633), ("Grand Duchy of Geoff", 390, 663), ("Sterich", 453, 770),
    ("Celene", 780, 653), ("Duchy of Ulek", 680, 697), ("County of Ulek", 750, 753),
    ("Principality of Ulek", 793, 803), ("The Pomarj", 940, 787), ("Wild Coast", 850, 650),
    ("Duchy of Urnst", 1017, 567), ("County of Urnst", 1093, 477), ("Shield Lands", 933, 413),
    ("Horned Society", 873, 323), ("Bandit Kingdoms", 1040, 303), ("Duchy of Tenh", 1167, 250),
    ("Theocracy of the Pale", 1300, 340), ("Ratik", 1450, 303), ("Bone March", 1480, 373),
    ("Prelacy of Almor", 1347, 643), ("Onnwal", 1107, 817), ("Ahlissa", 1267, 797), ("Idee", 1250, 900),
    ("Sunndi", 1413, 923), ("Medegia", 1620, 853), ("Aerdiaak", 1580, 457), ("Sea Baronies", 1787, 670),
    ("Lordship of the Isles", 1537, 1040), ("The Yeomanry", 513, 913), ("Hold of the Sea Princes", 613, 987),
    ("Hold of Stonefist", 1267, 13), ("North Kingdom of the Fruzti", 1450, 157),
    ("North Kingdom of the Schnai", 1677, 113), ("Chakyik", 407, 97), ("Wegwiur", 587, 127),
    ("The Hunting Lands", 1020, 140), ("Valley of the Mage", 387, 610),
    ("Plains of the Ulakandar", 227, 477), ("Dry Steppes", 147, 817),
    # forests
    ("Vesve Forest", 693, 303), ("Fellreev Forest", 1007, 207), ("Burneal Forest", 540, 20),
    ("Bramblewood Forest", 487, 460), ("Dim Forest", 480, 617), ("Dreadwood", 667, 887),
    ("Celadon Forest", 1107, 607), ("Gamboge Forest", 1253, 430), ("Adri Forest", 1457, 597),
    ("Grandwood Forest", 1607, 740), ("Rieuwood", 1333, 880), ("Udgru Forest", 333, 220),
    ("Hornwood", 363, 713), ("Phostwood", 1180, 313), ("Nutherwood", 1193, 353), ("Forlorn Forest", 1113, 100),
    ("Gnarley Forest", 827, 567), ("Welkwood", 820, 633), ("Suss Forest", 853, 747), ("Silverwood", 687, 767),
    ("Oytwood", 447, 683), ("Menowood", 1340, 963), ("Hraak Forest", 1357, 43), ("Sable Wood", 1807, 27),
    ("Spikey Forest", 1577, 73), ("Timberway Forest", 1387, 233), ("Loftwood", 1520, 340), ("Tangles", 1027, 337),
    # mountains, hills and other land
    ("Yatil Mountains", 467, 313), ("Rakers", 1383, 313), ("Griff Mountains", 1340, 113),
    ("Corusk Mountains", 1673, 27), ("Barrier Peaks", 353, 580), ("Crystalmist Mountains", 340, 807),
    ("Lortmil Mountains", 680, 633), ("Sulhaut Mountains", 287, 977), ("Jotens", 467, 840),
    ("Hellfurnaces", 500, 1060), ("Ulsprue", 163, 600), ("Flinty Hills", 1330, 487), ("Cairn Hills", 950, 530),
    ("Abbor-Alz", 960, 620), ("Bright Desert", 1007, 673), ("Kron Hills", 740, 610), ("Iron Hills", 1240, 847),
    ("Hestmark Highlands", 1413, 860), ("Hollow Highlands", 1320, 927), ("Blemu Hills", 1433, 460),
    ("Bluff Hills", 1113, 207), ("Howling Hills", 800, 140), ("Yecha Hills", 320, 143),
    ("Tusman Hills", 393, 390), ("Mounds of Dawn", 493, 243), ("Stark Mounds", 433, 733),
    ("Good Hills", 547, 787), ("Little Hills", 567, 873), ("Gull Cliffs", 1673, 633), ("Drachensgrab", 927, 797),
    ("Rift Canyon", 1047, 377), ("Barren Wastes", 973, 47), ("Cold Marshes", 817, 83), ("Rushmoors", 540, 693),
    ("Hool Marshes", 593, 943), ("Gnatmarsh", 1107, 673), ("Vast Swamp", 1420, 987), ("Lone Heath", 1677, 727),
    ("Jetsam Island", 743, 940), ("Fairwind Isle", 770, 967), ("Flotsam Island", 707, 987),
    ("Spindrift Isles", 1807, 907),
    # water
    ("Nyr Dyv", 967, 477), ("Lake Quag", 547, 213), ("Whyestil Lake", 800, 303), ("Azure Sea", 993, 987),
    ("Sea of Gearnat", 1060, 760), ("Relmor Bay", 1233, 717), ("Woolly Bay", 900, 680),
    ("Grendep Bay", 1573, 213), ("Aerdi Sea", 1613, 933), ("Spindrift Sound", 1740, 847),
    ("Solnor Ocean", 1787, 427), ("Dramidj Ocean", 153, 113), ("White Fanged Bay", 1187, 73),
]
WATER_NAMES = {"Nyr Dyv", "Lake Quag", "Whyestil Lake", "Azure Sea", "Sea of Gearnat", "Relmor Bay",
               "Woolly Bay", "Grendep Bay", "Aerdi Sea", "Spindrift Sound", "Solnor Ocean", "Dramidj Ocean",
               "White Fanged Bay"}
# words in a name that set the province's terrain when that terrain is present at all
NAME_TERRAIN = [(("Forest", "wood", "Tangles"), "forest", "forest", 0.12),
                (("Mountains", "Peaks", "Rakers", "Jotens", "Hellfurnaces", "Ulsprue"), "mountain", "mountains", 0.2),
                (("Hills", "Highlands", "Mounds", "Cliffs", "Abbor-Alz", "Drachensgrab"), "highland", "hills", 0.0),
                (("Marsh", "Swamp", "moors"), "swamp", "swamp", 0.1),
                (("Wastes", "Steppes", "Desert", "Heath", "Canyon"), "waste", "waste", 0.1)]

COLOURS = [(40, 90, 170), (30, 110, 40), (170, 210, 120), (220, 200, 90), (130, 80, 40), (235, 225, 190),
           (120, 180, 170), (0, 0, 0)]

if __name__ == "__main__":
    import sys
    grid, (W, H) = classify(sys.argv[1])
    img = Image.new("RGB", (len(grid[0]), len(grid)))
    img.putdata([COLOURS[c] for row in grid for c in row])
    img.resize((W // 2, H // 2), Image.NEAREST).save(sys.argv[2])
    print(Counter(CLASSES[c] for row in grid for c in row))
