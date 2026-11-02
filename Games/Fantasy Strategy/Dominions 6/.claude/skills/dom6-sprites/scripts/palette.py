"""Unit sprites for Dominions 6.

Every unit is a signed-distance model on a shared human rig, rendered with
painted cel shading into 24-bit TGA sprites (black = transparent, magenta =
shadow), facing left. Humans are ~35 px tall on a 64x64 canvas with the feet
on row 61; big units use a 128x128 canvas. Each pose copies the stance of a
Dominions Enhanced unit (named next to the unit's POSES).

  <unit>1.tga   normal image   (#spr1)
  <unit>2.tga   attack image   (#spr2)

Model space: metres, y up, x = the unit's left, z = its front.

usage: python3 units.py OUTDIR [unit ...]
"""
import math
import os
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw

sqrt, sin, cos = math.sqrt, math.sin, math.cos
TAU = 2 * math.pi

# materials
(SKIN, PALE, ZOMB, FRANK, PSKIN, HAIR_BR, HAIR_BL, HAIR_GR, HAIR_BK, TWHITE, UNDER, VISOR,
 MGREY, MDARK, BELT, BOOT, GUN, WOOD, STEEL, GOLD, CRED, COAT, SHIRT, TROUS, RUBBER, BRASS,
 LENS, GLASS, SURG, BLOOD, MECH, MECHD, HOSP, RAG, FCOAT, SUIT, NAVY, OVERALL, GGREEN,
 G_RED, G_CYAN, G_GREEN, G_FIRE, G_SPARK, G_FLASH, SHOE_BR, HAIR_RG, FLESH, BONE, TRENCH,
 CLONE, CSKIN, COPPER, FUR, LION, MANE, LABW) = range(1, 58)
CHROME, DARK = STEEL, BOOT    # default material names used by the shared SDF helpers

# painted cel palette per material: (lit, shade, deep)
PALETTE = {
    SKIN: ((228, 176, 140), (186, 132, 104), (136, 94, 76)),
    PALE: ((224, 228, 212), (176, 182, 166), (124, 130, 120)),
    ZOMB: ((158, 172, 134), (114, 128, 98), (80, 90, 72)),
    FRANK: ((140, 172, 118), (100, 130, 86), (68, 92, 62)),
    PSKIN: ((242, 204, 174), (204, 160, 132), (154, 114, 96)),
    HAIR_BR: ((112, 72, 48), (78, 50, 34), (54, 36, 26)),
    HAIR_BL: ((244, 222, 150), (200, 170, 98), (146, 120, 70)),
    HAIR_GR: ((204, 204, 200), (154, 154, 156), (106, 106, 112)),
    HAIR_BK: ((66, 62, 66), (44, 42, 46), (30, 28, 32)),
    TWHITE: ((238, 240, 244), (186, 192, 204), (128, 136, 152)),
    UNDER: ((92, 96, 108), (64, 68, 78), (44, 46, 56)),
    VISOR: ((52, 62, 84), (32, 38, 54), (22, 24, 36)),
    MGREY: ((152, 156, 162), (112, 116, 124), (80, 84, 92)),
    MDARK: ((98, 102, 110), (70, 74, 80), (50, 52, 58)),
    BELT: ((124, 96, 64), (90, 68, 46), (62, 48, 34)),
    BOOT: ((66, 62, 64), (46, 44, 46), (32, 30, 32)),
    GUN: ((96, 100, 110), (64, 68, 76), (42, 44, 52)),
    WOOD: ((152, 102, 62), (110, 72, 44), (76, 50, 32)),
    STEEL: ((234, 238, 246), (172, 180, 194), (118, 124, 140)),
    GOLD: ((240, 198, 82), (186, 142, 50), (132, 98, 34)),
    CRED: ((202, 46, 42), (148, 30, 32), (102, 22, 26)),
    COAT: ((240, 242, 244), (190, 196, 208), (132, 140, 158)),
    SHIRT: ((176, 206, 234), (130, 160, 196), (96, 118, 150)),
    TROUS: ((88, 86, 98), (60, 58, 68), (42, 40, 48)),
    RUBBER: ((206, 184, 82), (154, 134, 52), (106, 92, 36)),
    BRASS: ((232, 184, 76), (176, 126, 44), (120, 84, 30)),
    LENS: ((150, 226, 236), (90, 170, 190), (60, 120, 140)),
    GLASS: ((206, 232, 236), (150, 184, 194), (106, 134, 146)),
    SURG: ((150, 194, 172), (108, 148, 130), (76, 108, 96)),
    BLOOD: ((156, 32, 32), (110, 22, 24), (76, 14, 18)),
    MECH: ((172, 182, 196), (120, 130, 146), (82, 90, 104)),
    MECHD: ((86, 90, 102), (60, 62, 72), (42, 44, 52)),
    HOSP: ((168, 178, 172), (124, 134, 130), (88, 96, 94)),
    RAG: ((132, 112, 86), (96, 80, 60), (68, 56, 42)),
    FCOAT: ((74, 70, 74), (50, 48, 52), (34, 32, 36)),
    SUIT: ((248, 248, 252), (206, 208, 218), (152, 156, 170)),
    NAVY: ((62, 72, 100), (44, 50, 72), (30, 34, 50)),
    OVERALL: ((76, 98, 142), (54, 70, 104), (38, 50, 76)),
    GGREEN: ((90, 170, 90), (60, 124, 64), (42, 88, 46)),
    SHOE_BR: ((92, 66, 46), (64, 46, 32), (44, 32, 24)),
    HAIR_RG: ((178, 184, 194), (128, 134, 148), (90, 94, 108)),
    FLESH: ((218, 164, 152), (172, 118, 112), (122, 80, 78)),
    BONE: ((236, 226, 196), (190, 178, 146), (138, 128, 102)),
    TRENCH: ((180, 152, 106), (134, 112, 76), (94, 78, 54)),
    CLONE: ((172, 188, 200), (126, 142, 156), (90, 102, 116)),
    CSKIN: ((226, 196, 176), (184, 152, 134), (134, 108, 96)),
    COPPER: ((224, 140, 86), (172, 98, 58), (120, 66, 42)),
    FUR: ((150, 128, 108), (108, 90, 76), (74, 62, 54)),
    LION: ((222, 170, 96), (176, 126, 66), (124, 86, 46)),
    MANE: ((150, 92, 48), (108, 64, 34), (74, 44, 26)),
    LABW: ((244, 242, 238), (200, 197, 190), (146, 142, 134)),
}
# glowing materials: (edge colour, core colour)
EMISSIVE = {
    G_RED: ((230, 40, 30), (255, 210, 180)),
    G_CYAN: ((40, 200, 255), (225, 250, 255)),
    G_GREEN: ((80, 225, 70), (225, 255, 195)),
    G_FIRE: ((245, 116, 24), (255, 244, 150)),
    G_SPARK: ((140, 196, 255), (248, 252, 255)),
    G_FLASH: ((255, 186, 40), (255, 255, 222)),
}
