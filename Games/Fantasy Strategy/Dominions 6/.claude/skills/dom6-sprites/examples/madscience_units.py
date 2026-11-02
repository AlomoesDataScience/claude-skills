
# ================================================================ troops and commanders
def trooper_legs(R):
    def plates(g, s, hip, knee, ankle):
        g.add(limb(lerp(hip, knee, 0.2), lerp(hip, knee, 0.85), 0.084, 0.072), TWHITE)   # thigh plate
        g.add(sphere(knee, 0.064), TWHITE)                                                 # knee cop
    legs(R, UNDER, TWHITE, BOOT, lt=1.04, boot_top=0.22, extra=plates)


def trooper_torso(R, trim=None):
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), UNDER)                               # hips
    t.add(box((0, 0.9, 0.085), (0.05, 0.06, 0.02), rnd=0.015), TWHITE)                    # cup plate
    t.add(box((0, 0.995, 0), (0.15, 0.028, 0.105), rnd=0.025), TWHITE)                    # belt
    for x in (-0.09, 0.09):
        t.add(box((x, 0.99, 0.11), (0.03, 0.025, 0.018), rnd=0.008), UNDER)               # pouches
    t.add(box((0, 1.12, 0), (0.12, 0.09, 0.09), rnd=0.03), UNDER)                         # midriff
    t.add(grooves(box((0, 1.12, 0.05), (0.085, 0.075, 0.035), rnd=0.015),
                  (0, 0, 0), (0, 1, 0), 0.04, 0.008), TWHITE)                              # ab plate
    t.add(box((0, 1.3, 0.005), (0.165, 0.11, 0.11), rnd=0.045), TWHITE)                   # chest plate
    t.add(box((0, 1.27, -0.13), (0.12, 0.12, 0.045), rnd=0.02), TWHITE)                   # back pack
    t.add(capsule((-0.1, 1.44, 0), (0.1, 1.44, 0), 0.05), UNDER)                          # collar
    for s in (1, -1):
        pd = ellipsoid((0.215 * s, 1.41, 0), (0.088, 0.062, 0.09))
        t.add(pd, TWHITE)                                                                   # pauldron
        if trim:
            t.add(shell(pd, 0.006, 1.37, 1.385), trim)
    if trim:
        t.add(shell(box((0, 1.3, 0.005), (0.165, 0.11, 0.11), rnd=0.045), 0.006, 1.38, 1.395), trim)
        t.add(box((0, 0.995, 0.13), (0.025, 0.022, 0.01), rnd=0.005), trim)              # buckle
    R.body(t)


def trooper_helmet(R):
    h = Group("head")
    face(h, UNDER, nose=False)
    h.add(ellipsoid((0, 1.625, 0.0), (0.086, 0.1, 0.095)), TWHITE)                       # dome
    h.add(box((0, 1.612, 0.074), (0.066, 0.019, 0.03), rnd=0.012), VISOR)                 # eye slit
    h.add(ellipsoid((0, 1.545, 0.05), (0.06, 0.05, 0.048)), TWHITE)                       # jaw guard
    h.add(box((0, 1.538, 0.094), (0.024, 0.016, 0.008), rnd=0.004), UNDER)                # breather
    for s in (1, -1):
        h.add(disc((0.086 * s, 1.6, 0.0), (1, 0, 0), 0.03, 0.02), TWHITE)                 # ear pods
    R.head(h)


def armoured_arm(R, s, hand, glove=UNDER, trim=None):
    def bracer(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(limb(lerp(elbow, wrist, 0.1), lerp(elbow, wrist, 0.85), 0.052, 0.046), TWHITE)
        if trim:
            g.add(limb(lerp(elbow, wrist, 0.82), lerp(elbow, wrist, 0.9), 0.05, 0.05), trim)
    return arm(R, s, hand, UNDER, UNDER, glove, at=1.04, extra=bracer)


def b_stormtrooper(R):
    P = R.P
    trooper_legs(R)
    trooper_torso(R)
    trooper_helmet(R)
    d = P["gun"]
    armoured_arm(R, -1, P["grip"])
    armoured_arm(R, 1, add(P["grip"], mul(d, P["fore"])))
    g = Group("rifle")
    muzzle = rifle(g, P["grip"], d, body=BOOT, furn=GUN, k=P.get("k", 1.0))
    if P.get("fire"):
        flash(g, muzzle, d)
    R.world(g)


def b_swordtrooper(R):
    P = R.P
    trooper_legs(R)
    trooper_torso(R)
    trooper_helmet(R)
    d = norm(P["blade"])
    armoured_arm(R, -1, P["grip"])
    armoured_arm(R, 1, sub(P["grip"], mul(d, 0.12)))
    g = Group("sword")
    sword(g, P["grip"], d, blen=0.95, width=0.034, hilt=0.24, guard=GUN, wrap=UNDER, gw=0.08)
    R.world(g)


def militia_body(R, coat=False):
    legs(R, MGREY, MGREY, BOOT, boot_top=0.5)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), MGREY)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), MGREY)
    t.add(ellipsoid((0, 1.31, 0), (0.165, 0.12, 0.108)), MGREY)
    t.add(capsule((-0.17, 1.41, -0.005), (0.17, 1.41, -0.005), 0.058), MGREY)
    t.add(box((0, 0.99, 0), (0.148, 0.026, 0.104), rnd=0.02), BOOT)                      # belt
    if coat:
        t.add(cone_skirt((0, 1.02, 0), (0, 0.6, -0.01), 0.155, 0.2, -0.15, 0.13), MGREY)  # coat skirt
        t.add(box((0, 0.995, 0.125), (0.022, 0.02, 0.008), rnd=0.004), GOLD)             # buckle
        for s in (1, -1):
            t.add(box((0.19 * s, 1.455, 0), (0.05, 0.008, 0.035), rnd=0.004), GOLD)      # shoulder boards
    else:
        t.add(box((0, 1.24, 0.0), (0.14, 0.13, 0.08), rnd=0.04), MDARK)                  # vest
        for x in (-0.07, 0.0, 0.07):
            t.add(box((x, 1.16, 0.115), (0.026, 0.03, 0.016), rnd=0.006), MDARK)        # mag pouches
    R.body(t)


def militia_arm(R, s, hand, extra=None):
    return arm(R, s, hand, MGREY, MGREY, BOOT, extra=extra)


def b_militia(R):
    P = R.P
    militia_body(R)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BR)
    h.add(ellipsoid((0, 1.676, -0.004), (0.083, 0.06, 0.09)), MGREY)                     # helmet
    h.add(disc((0, 1.652, 0.0), (0, 1, 0), 0.097, 0.011), MGREY)                          # brim
    h.add(shell(ellipsoid((0, 1.676, -0.004), (0.083, 0.06, 0.09)), 0.006, 1.68, 1.7), BOOT)  # goggle band
    for s in (1, -1):
        h.add(disc((0.035 * s, 1.69, 0.08), (0, 0.4, 1), 0.016, 0.012), LENS)           # goggles
    R.head(h)
    d = P["gun"]
    militia_arm(R, -1, P["hand_r"])
    militia_arm(R, 1, P["hand_l"])
    g = Group("rifle")
    rifle(g, P["grip"], d)
    R.world(g)


def b_cyborg(R):
    P = R.P

    def mech_leg(g, s, hip, knee, ankle):
        g.add(sphere(knee, 0.06), MECHD)
        g.add(capsule(lerp(knee, ankle, 0.2), lerp(knee, ankle, 0.75), 0.022), G_RED if s > 0 else MECHD)
    legs(R, MECHD, MECH, MECHD, lt=1.05, boot_top=0.3, extra=mech_leg)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), MECHD)
    t.add(ellipsoid((0, 1.14, 0), (0.12, 0.13, 0.085)), PALE)                             # bare belly
    for x in (-0.05, 0.05):
        t.add(capsule((x, 1.04, 0.07), (x * 1.6, 1.24, 0.09), 0.013), MECHD)              # tubes
    t.add(box((0, 1.31, 0.01), (0.15, 0.1, 0.1), rnd=0.04), MECH)                         # chest casing
    t.add(box((0, 1.33, 0.115), (0.07, 0.05, 0.01), rnd=0.008), MECHD)
    t.add(sphere((0.0, 1.33, 0.125), 0.02), G_RED)                                         # core light
    t.add(box((0, 1.25, -0.11), (0.06, 0.2, 0.04), rnd=0.02), MECHD)                      # spine
    t.add(ellipsoid((-0.22, 1.42, 0), (0.1, 0.075, 0.1)), MECH)                           # gun shoulder
    t.add(ellipsoid((0.19, 1.41, 0), (0.07, 0.055, 0.075)), PALE)
    R.body(t)
    h = Group("head")
    face(h, PALE)
    h.add(ellipsoid((0.025, 1.645, -0.005), (0.062, 0.062, 0.08)), MECH)                 # skull plate
    h.add(box((0.0, 1.548, 0.06), (0.05, 0.022, 0.03), rnd=0.01), MECHD)                  # jaw grille
    h.add(sphere((0.034, 1.612, 0.074), 0.016), G_RED)                                     # optic
    h.add(capsule((0.05, 1.6, -0.06), (0.08, 1.45, -0.1), 0.014), MECHD)                  # cable
    R.head(h)

    def gun_arm(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(capsule(wrist, add(wrist, mul(d, 0.16)), 0.045), MECHD)                     # cannon
        g.add(capsule(add(wrist, mul(d, 0.14)), add(wrist, mul(d, 0.2)), 0.03), MECH)
        g.add(sphere(add(wrist, mul(d, 0.21)), 0.022), G_RED)
        if P.get("fire"):
            flash(g, add(wrist, mul(d, 0.22)), d, 1.0, G_RED)
    arm(R, -1, P["hand_r"], MECH, MECH, MECHD, at=1.25, extra=gun_arm, sh_w=0.21)

    def brace(g, s, J):
        g.add(sphere(J[1], 0.05), MECHD)
    arm(R, 1, P["hand_l"], PALE, PALE, MECHD, extra=brace)


def b_militiacaptain(R):
    P = R.P
    militia_body(R, coat=True)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BR)
    h.add(ellipsoid((0.0, 1.69, -0.005), (0.085, 0.032, 0.092)), MGREY)                  # cap crown
    h.add(box((0, 1.665, 0.0), (0.074, 0.02, 0.082), rnd=0.02), BOOT)                     # cap band
    h.add(box((0, 1.652, 0.085), (0.058, 0.006, 0.03),
              (norm((1, 0, 0)), norm((0, 1, -0.4)), norm((0, 0.4, 1))), rnd=0.004), BOOT)  # peak
    h.add(sphere((0, 1.672, 0.095), 0.012), GOLD)                                          # badge
    R.head(h)
    militia_arm(R, -1, P["hand_r"])
    militia_arm(R, 1, P["hand_l"])
    g = Group("weapons")
    sword(g, P["hand_r"], P["blade"], blen=0.68, width=0.022)
    muzzle = pistol(g, P["hand_l"], P["gun"])
    if P.get("fire"):
        flash(g, muzzle, P["gun"], 0.7)
    R.world(g)


def b_general(R):
    P = R.P
    trooper_legs(R)
    trooper_torso(R, trim=GOLD)
    c = Group("cape")
    c.add(lumpy(cone_skirt((0, 1.42, -0.1), (0, 0.45, -0.17), 0.16, 0.27, -1.0, -0.1), 0.006, 40), CRED)
    R.body(c)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_GR)
    h.add(ellipsoid((0, 1.555, 0.07), (0.04, 0.012, 0.016)), HAIR_GR)                     # moustache
    h.add(ellipsoid((0.0, 1.69, -0.005), (0.088, 0.032, 0.095)), BOOT)                    # cap crown
    h.add(box((0, 1.665, 0.0), (0.074, 0.02, 0.082), rnd=0.02), CRED)                     # cap band
    h.add(box((0, 1.652, 0.085), (0.058, 0.006, 0.03),
              (norm((1, 0, 0)), norm((0, 1, -0.4)), norm((0, 0.4, 1))), rnd=0.004), BOOT)  # peak
    h.add(sphere((0, 1.674, 0.095), 0.013), GOLD)
    R.head(h)
    armoured_arm(R, -1, P["hand_r"], trim=GOLD)
    armoured_arm(R, 1, P["hand_l"], trim=GOLD)
    g = Group("weapons")
    sword(g, P["hand_r"], P["blade"], blen=0.72, width=0.026)
    muzzle = pistol(g, P["hand_l"], P["gun"])
    if P.get("fire"):
        flash(g, muzzle, P["gun"], 0.7)
    R.world(g)


FEET = lambda fr, fl, dr=-0.04, dl=0.05: (W(fr, 0.085, dr), W(fl, 0.085, dl))


def two_hand(grip, d, k):
    return add(grip, mul(norm(d), k))


UNITS = {
    # rifle at port arms / shouldered and firing                    (rotterland rostelmmark)
    "stormtrooper": dict(build=b_stormtrooper, poses={
        "1": dict(feet=FEET(0.07, -0.07), grip=W(0.16, 0.96, 0.4), gun=aim(128, 0.15), fore=0.4, k=1.5),
        "2": dict(feet=FEET(0.2, -0.16, 0.0, 0.04), body=(0, -0.02, 0), lean=6, twist=-15, nod=4,
                  grip=W(0.3, 1.36, 0.02), gun=aim(1), fore=0.33, fire=True, halo=True)}),
    # two-handed sword held low / raised overhead                   (fennoscandia fsbearwar)
    "swordtrooper": dict(build=b_swordtrooper, poses={
        "1": dict(feet=FEET(0.17, -0.15, 0.02, 0.03), body=(0, -0.04, 0), lean=6,
                  grip=W(0.2, 1.02, 0.12), blade=aim(-5)),
        "2": dict(feet=FEET(0.2, -0.17, 0.02, 0.03), body=(0, -0.03, 0), lean=-8,
                  grip=W(-0.1, 1.92, 0.04), blade=aim(150), pole_r=(-1, 0.2, -0.3), pole_l=(1, 0.2, -0.3))}),
    # rifle grounded at the side / bayonet thrust                   (greatarrada spearhalfplate)
    "militia": dict(build=b_militia, poses={
        "1": dict(feet=FEET(0.04, -0.04, -0.06, 0.06), grip=W(0.22, 0.38, 0.07), gun=aim(90),
                  hand_r=W(0.21, 0.95, 0.07), hand_l=W(-0.12, 0.86, 0.1)),
        "2": dict(feet=FEET(0.26, -0.22, 0.02, 0.0), body=(0, -0.07, 0.03), lean=12, twist=-20,
                  grip=W(0.12, 1.08, 0.04), gun=aim(3),
                  hand_r=W(0.12, 1.08, 0.04), hand_l=two_hand(W(0.12, 1.08, 0.04), aim(3), 0.34))}),
    # hunched, cannon arm low / cannon thrust out and firing        (rotterland rmudman)
    "cyborg": dict(build=b_cyborg, poses={
        "1": dict(feet=FEET(0.12, -0.12, 0.02, 0.02), body=(0, -0.07, 0), lean=34, nod=-26,
                  hand_r=W(0.3, 1.0, 0.0), hand_l=W(0.05, 0.95, 0.15)),
        "2": dict(feet=FEET(0.24, -0.16, 0.0, 0.02), body=(0, -0.08, 0.02), lean=36, twist=-20, nod=-30,
                  hand_r=W(0.62, 1.25, 0.0), hand_l=W(0.1, 1.05, 0.12), fire=True, halo=True)}),
    # sabre low, pistol at the hip / sabre raised                   (rotterland rcapt)
    "militiacaptain": dict(build=b_militiacaptain, poses={
        "1": dict(feet=FEET(0.14, -0.12, 0.02, 0.04), lean=4, hand_r=W(0.22, 1.0, 0.1), blade=aim(-38),
                  hand_l=W(-0.1, 1.0, 0.14), gun=aim(-60, 0.3)),
        "2": dict(feet=FEET(0.2, -0.14, 0.02, 0.04), body=(0, -0.04, 0), lean=8,
                  hand_r=W(0.3, 1.32, 0.08), blade=aim(62), hand_l=W(-0.12, 1.02, 0.12), gun=aim(-30, 0.3))}),
    # sword level / sword raised high while firing the pistol       (fennoscandia fskuningas)
    "general": dict(build=b_general, poses={
        "1": dict(feet=FEET(0.15, -0.13, 0.02, 0.04), hand_r=W(0.18, 1.12, 0.12), blade=aim(10),
                  hand_l=W(-0.12, 0.95, 0.1), gun=aim(-75, 0.2)),
        "2": dict(feet=FEET(0.18, -0.14, 0.02, 0.04), body=(0, -0.03, 0), lean=4,
                  hand_r=W(0.18, 1.62, 0.06), blade=aim(80), hand_l=W(0.1, 1.2, 0.2), gun=aim(0),
                  fire=True, halo=True)}),
}

# ================================================================ mages
def robe_body(R, top, skirt, under=None, skirt_to=0.55, legs_mat=TROUS, shoes=BOOT, extra=None):
    """Torso with a coat or gown skirt hanging to skirt_to."""
    legs(R, legs_mat, legs_mat, shoes, boot_top=0.2)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.155, 0.1, 0.1)), skirt)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), top)
    t.add(ellipsoid((0, 1.31, 0), (0.162, 0.12, 0.106)), top)
    t.add(capsule((-0.165, 1.41, -0.005), (0.165, 1.41, -0.005), 0.056), top)
    t.add(cone_skirt((0, 1.05, 0), (0, skirt_to, -0.01), 0.15, 0.21, -0.15, 0.14), skirt)
    if under:
        t.add(box((0, 1.36, 0.108), (0.032, 0.06, 0.008), rnd=0.006), under)                # shirt front
    if extra:
        extra(t)
    R.body(t)


def flask(g, hand, mat=GLASS, goo=G_GREEN, flame=None, size=1.0):
    b = add(hand, (0, 0.05 * size, 0))
    g.add(sphere(b, 0.045 * size), goo)
    g.add(capsule(add(b, (0, 0.03 * size, 0)), add(b, (0, 0.11 * size, 0)), 0.014 * size), mat)
    if flame:
        top = add(b, (0, 0.11 * size, 0))
        g.add(roundcone(top, add(top, (0.0, 0.1 * flame, 0.0)), 0.03 * flame, 0.004), G_FIRE)
        g.add(roundcone(add(top, (0.02 * flame, 0.0, 0)), add(top, (0.05 * flame, 0.08 * flame, 0.01)),
                        0.018 * flame, 0.003), G_FIRE)
        g.add(roundcone(add(top, (-0.02 * flame, 0.0, 0)), add(top, (-0.045 * flame, 0.07 * flame, 0.0)),
                        0.016 * flame, 0.003), G_FIRE)


def goggles(h, y=1.665, band=BOOT, rim=BRASS, lens=LENS):
    h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.006, 0.006, 0.006))), 0.005, y - 0.012, y + 0.012), band)
    for s in (1, -1):
        h.add(disc((0.033 * s, y, 0.086), (0.0, 0.25, 1.0), 0.024, 0.022), rim)
        h.add(disc((0.033 * s, y + 0.002, 0.098), (0.0, 0.25, 1.0), 0.016, 0.006), lens)


def b_roboticist(R):
    P = R.P

    def belt(t):
        t.add(box((0, 0.99, 0), (0.15, 0.026, 0.104), rnd=0.02), BELT)
        for x in (-0.1, 0.1):
            t.add(box((x, 0.95, 0.1), (0.028, 0.04, 0.02), rnd=0.006), BELT)              # tool pouches
        t.add(box((0, 1.24, 0.1), (0.09, 0.08, 0.012), rnd=0.006), OVERALL)                # bib
    legs(R, OVERALL, OVERALL, BOOT, boot_top=0.3)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), OVERALL)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), OVERALL)
    t.add(ellipsoid((0, 1.31, 0), (0.162, 0.12, 0.106)), OVERALL)
    t.add(capsule((-0.165, 1.41, -0.005), (0.165, 1.41, -0.005), 0.056), OVERALL)
    belt(t)
    R.body(t)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BR, 0.009)
    goggles(h, lens=VISOR)
    R.head(h)
    arm(R, -1, P["hand_r"], OVERALL, SKIN, BELT)
    arm(R, 1, P["hand_l"], OVERALL, SKIN, BELT)
    g = Group("tools")
    hr, hl = (P["hand_r"], P["hand_l"]) if P.get("wrench_in", "r") == "r" else (P["hand_l"], P["hand_r"])
    wd = norm(P["wrench"])                                                 # big wrench
    g.add(capsule(add(hr, mul(wd, -0.06)), add(hr, mul(wd, 0.34)), 0.018), STEEL)
    g.add(box(add(hr, mul(wd, 0.37)), (0.055, 0.014, 0.04), blade_basis(wd), rnd=0.012), STEEL)
                                                                           # radio remote in the other hand
    g.add(box(hl, (0.04, 0.055, 0.026), rnd=0.01), MECHD)
    tip = add(hl, (0.0, 0.22, 0.0))
    g.add(capsule(add(hl, (0.02, 0.04, 0)), tip, 0.007), STEEL)
    g.add(sphere(tip, 0.02), G_CYAN)
    R.world(g)
    dg = Group("drone")                                                    # helper drone
    c = P["drone"]
    dg.add(sphere(c, 0.085), MECH)
    dg.add(capsule(add(c, (-0.13, 0.05, 0)), add(c, (0.13, 0.05, 0)), 0.014), MECHD)
    for s in (1, -1):
        dg.add(disc(add(c, (0.14 * s, 0.075, 0)), (0, 1, 0), 0.07, 0.01), MECHD)       # rotors
    dg.add(sphere(add(c, mul(norm(add(SL, OUT)), 0.07)), 0.032), G_CYAN)               # eye
    dg.add(capsule(add(c, (0, -0.07, 0)), add(c, (0.03, -0.14, 0.02)), 0.01), MECHD)   # grabber
    if P.get("zap"):
        bolt(dg, tip, add(c, mul(SL, -0.06)), G_CYAN, 0.01, 4, 0.04)
    R.world(dg)


def b_reviver(R):
    P = R.P

    def stains(t):
        for p, r in (((0.05, 1.12, 0.1), 0.03), ((-0.06, 0.92, 0.13), 0.035), ((0.08, 0.75, 0.15), 0.025)):
            t.add(ellipsoid(p, (r, r * 1.3, 0.012)), BLOOD)
        t.add(box((0, 0.99, 0), (0.15, 0.024, 0.104), rnd=0.02), BELT)
    robe_body(R, SURG, SURG, skirt_to=0.38, extra=stains)
    h = Group("head")
    face(h, SKIN)
    for prim in (ellipsoid((0, 1.6, -0.055), (0.074, 0.06, 0.045)),
                 ellipsoid((0.065, 1.6, -0.01), (0.022, 0.035, 0.045)),
                 ellipsoid((-0.065, 1.6, -0.01), (0.022, 0.035, 0.045))):
        h.add(lumpy(prim, 0.006, 80), HAIR_GR)                                             # grey fringe
    h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.005, 0.005, 0.005))), 0.004, 1.645, 1.66), BOOT)
    h.add(disc((0.02, 1.665, 0.09), (0.2, 0.2, 1.0), 0.03, 0.006), STEEL)                 # head mirror
    h.add(box((0, 1.52, 0.07), (0.05, 0.03, 0.012), rnd=0.008), SURG)                     # mask, pulled down
    R.head(h)
    arm(R, -1, P["hand_r"], SURG, SURG, BOOT)
    arm(R, 1, P["hand_l"], SURG, SURG, BOOT)
    g = Group("rod")
    d = norm(P["rod"])
    hr = P["hand_r"]
    g.add(capsule(add(hr, mul(d, -0.1)), add(hr, mul(d, 0.45)), 0.013), BRASS)
    g.add(grooves(capsule(add(hr, mul(d, 0.22)), add(hr, mul(d, 0.38)), 0.022), hr, d, 0.03, 0.008), BRASS)
    tip = add(hr, mul(d, 0.48))
    g.add(sphere(tip, 0.035 if P.get("arc") else 0.024), G_SPARK)
    if P.get("arc"):
        for k, v in enumerate((aim(20), aim(70, 0.3), aim(130), aim(-30, -0.2))):
            bolt(g, tip, add(tip, mul(v, 0.22)), G_SPARK, 0.009, 4, 0.035, seed=k + 1)
    R.world(g)


def syringe(g, hand, d, goo=G_GREEN):
    d = norm(d)
    g.add(capsule(add(hand, mul(d, -0.04)), add(hand, mul(d, 0.16)), 0.028), GLASS)
    g.add(capsule(add(hand, mul(d, 0.0)), add(hand, mul(d, 0.13)), 0.02), goo)
    g.add(capsule(add(hand, mul(d, -0.13)), add(hand, mul(d, -0.04)), 0.008), STEEL)      # plunger
    g.add(disc(add(hand, mul(d, -0.14)), d, 0.026, 0.008), STEEL)
    g.add(capsule(add(hand, mul(d, 0.16)), add(hand, mul(d, 0.27)), 0.004), STEEL)        # needle


def b_geneticist(R):
    P = R.P
    robe_body(R, COAT, COAT, under=GGREEN, skirt_to=0.42)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BK, 0.003)
    h.add(ellipsoid((0.0, 1.664, 0.02), (0.08, 0.04, 0.08)), HAIR_BK)                     # slicked top
    for s in (1, -1):
        h.add(disc((0.03 * s, 1.612, 0.084), (0, 0, 1), 0.017, 0.006), GLASS)             # spectacles
    R.head(h)
    arm(R, -1, P["hand_r"], COAT, COAT, GGREEN)
    arm(R, 1, P["hand_l"], COAT, COAT, GGREEN)
    g = Group("kit")
    syringe(g, P["hand_r"], P["needle"])
    if P.get("vial"):
        flask(g, P["hand_l"], goo=G_GREEN, size=1.2)
    R.world(g)


def b_chemist(R):
    P = R.P

    def apron(t):
        t.add(box((0, 1.15, 0.1), (0.13, 0.25, 0.012), rnd=0.008), RUBBER)
        t.add(cone_skirt((0, 1.0, 0.04), (0, 0.42, 0.06), 0.15, 0.19, 0.05, 0.16), RUBBER)
    robe_body(R, MDARK, TROUS, skirt_to=0.75, extra=apron)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BR)
    h.add(ellipsoid((0, 1.585, 0.05), (0.068, 0.06, 0.05)), BOOT)                        # gas mask
    for s in (1, -1):
        h.add(disc((0.03 * s, 1.612, 0.088), (0.2 * s, 0, 1), 0.021, 0.014), BRASS)
        h.add(disc((0.03 * s, 1.612, 0.095), (0.2 * s, 0, 1), 0.014, 0.006), LENS)
    h.add(capsule((0, 1.55, 0.09), (0, 1.52, 0.13), 0.026), GUN)                         # filter can
    h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.005, 0.005, 0.005))), 0.004, 1.62, 1.635), BOOT)
    R.head(h)

    def glove(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(limb(lerp(elbow, wrist, 0.45), wrist, 0.046, 0.045), BOOT)                  # long rubber gloves
    arm(R, -1, P["hand_r"], MDARK, MDARK, BOOT, extra=glove)
    arm(R, 1, P["hand_l"], MDARK, MDARK, BOOT, extra=glove)
    g = Group("flask")
    flask(g, P["hand_r"], goo=G_FIRE, flame=P.get("flame", 1.0), size=1.1)
    R.world(g)


def b_cyberneticist(R):
    P = R.P
    robe_body(R, FCOAT, FCOAT, under=SHIRT, skirt_to=0.5)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_GR, 0.004)
    h.add(disc((-0.03, 1.612, 0.08), (0, 0, 1), 0.022, 0.016), MECH)                     # eyepiece
    h.add(sphere((-0.03, 1.612, 0.09), 0.013), G_CYAN)
    h.add(capsule((-0.07, 1.62, 0.02), (-0.1, 1.46, -0.04), 0.008), MECHD)                # cable
    R.head(h)

    def cyber(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(sphere(elbow, 0.05), MECHD)
        g.add(sphere(lerp(elbow, wrist, 0.5), 0.02), G_CYAN)
    arm(R, -1, P["hand_r"], MECH, MECH, MECH, at=1.1, extra=cyber)
    arm(R, 1, P["hand_l"], FCOAT, FCOAT, BOOT)
    g = Group("probe")
    d, hr = norm(P["probe"]), P["hand_r"]
    g.add(capsule(add(hr, mul(d, -0.25)), add(hr, mul(d, 0.5)), 0.012), MECHD)
    g.add(sphere(add(hr, mul(d, 0.53)), 0.034 if P.get("cast") else 0.022), G_CYAN)
    g.add(disc(add(hr, mul(d, 0.45)), d, 0.03, 0.012), MECH)
    if P.get("cast"):
        tip = add(hr, mul(d, 0.53))
        for k, v in enumerate((aim(0), aim(35, 0.2), aim(-30, -0.2))):
            bolt(g, tip, add(tip, mul(v, 0.2)), G_CYAN, 0.009, 3, 0.03, seed=k + 3)
    R.world(g)


def b_cyberassassin(R):
    P = R.P

    def plates(g, s, hip, knee, ankle):
        g.add(limb(lerp(knee, ankle, 0.1), lerp(knee, ankle, 0.8), 0.06, 0.052), MECH)
        g.add(sphere(knee, 0.055), MECHD)
    legs(R, NAVY, NAVY, MECHD, boot_top=0.2, extra=plates)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.14, 0.1, 0.1)), NAVY)
    t.add(ellipsoid((0, 1.17, 0), (0.13, 0.2, 0.095)), NAVY)
    t.add(box((0, 1.3, 0.005), (0.15, 0.1, 0.1), rnd=0.045), MECHD)
    t.add(box((0, 1.3, 0.1), (0.02, 0.07, 0.012), rnd=0.006), G_CYAN)                     # spine-light
    t.add(box((0, 0.99, 0), (0.142, 0.022, 0.1), rnd=0.02), MECHD)
    for s in (1, -1):
        t.add(ellipsoid((0.2 * s, 1.41, 0), (0.075, 0.055, 0.08)), MECH)
    R.body(t)
    c = Group("cloak")
    c.add(lumpy(cone_skirt((0, 1.44, -0.08), (0, 0.42, -0.2), 0.18, 0.28, -1.0, -0.08), 0.007, 40), NAVY)
    R.body(c)
    h = Group("head")
    face(h, MECHD, nose=False)
    h.add(ellipsoid((0, 1.615, 0.0), (0.078, 0.098, 0.09)), MECHD)                       # helmet
    h.add(box((0, 1.615, 0.078), (0.06, 0.012, 0.02), rnd=0.008), G_CYAN)                 # visor strip
    R.head(h)
    hd = Group("hood")
    hd.add(lumpy(ellipsoid((0, 1.64, -0.02), (0.1, 0.1, 0.105)), 0.006, 50), NAVY)
    hd.cut(box((0, 1.6, 0.15), (0.075, 0.08, 0.08)), NAVY)
    R.head(hd)

    def blade_arm(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(limb(lerp(elbow, wrist, 0.1), wrist, 0.05, 0.046), MECH)
        bd = norm(P["blade"])
        sb = blade_basis(bd)
        base = add(wrist, mul(bd, 0.02))
        g.add(box(add(base, mul(bd, 0.3)), (0.026, 0.005, 0.3), sb, rnd=0.005), STEEL)
    arm(R, -1, P["hand_r"], NAVY, NAVY, MECHD, extra=blade_arm)

    def bracer(g, s, J):
        g.add(limb(lerp(J[1], J[2], 0.1), J[2], 0.05, 0.046), MECH)
    arm(R, 1, P["hand_l"], NAVY, NAVY, MECHD, extra=bracer)


# ================================================================ summons
def b_zombie(R):
    P = R.P

    def rot_leg(g, s, hip, knee, ankle):
        g.add(ellipsoid(lerp(knee, ankle, 0.5), (0.03, 0.05, 0.03)), BLOOD if s > 0 else ZOMB)
    legs(R, ZOMB, ZOMB, ZOMB, lt=0.9, bare=True, extra=rot_leg)
    t = Group("torso")
    t.add(ellipsoid((0, 1.17, 0), (0.13, 0.2, 0.095)), ZOMB)
    t.add(ellipsoid((0, 1.31, 0), (0.155, 0.11, 0.1)), ZOMB)
    t.add(capsule((-0.16, 1.41, -0.005), (0.16, 1.41, -0.005), 0.05), ZOMB)
    t.add(lumpy(cone_skirt((0, 1.38, 0), (0, 0.62, 0.0), 0.15, 0.2, -0.13, 0.13), 0.012, 45), HOSP)  # gown
    t.add(ellipsoid((0.05, 1.05, 0.13), (0.035, 0.05, 0.012)), BLOOD)
    t.add(ellipsoid((-0.06, 1.25, 0.115), (0.03, 0.035, 0.012)), BLOOD)
    R.body(t)
    h = Group("head")
    face(h, ZOMB)
    h.add(lumpy(ellipsoid((0.02, 1.66, -0.03), (0.06, 0.04, 0.07)), 0.01, 90), HAIR_BK)  # patchy hair
    for s in (1, -1):
        h.add(sphere((0.028 * s, 1.612, 0.07), 0.016), BOOT)                               # sunken eyes
    h.add(ellipsoid((0, 1.548, 0.075), (0.026, 0.02 if P.get("roar") else 0.008, 0.012)), BLOOD)  # mouth
    R.head(h)
    arm(R, -1, P["hand_r"], ZOMB, ZOMB, ZOMB, at=0.9)
    arm(R, 1, P["hand_l"], ZOMB, ZOMB, ZOMB, at=0.9)


def b_frankenstein(R):
    P = R.P

    def boot(g, s, hip, knee, ankle):
        g.add(box(add(ankle, (0, -0.07, 0.04)), (0.06, 0.02, 0.12), yaw_basis(0), rnd=0.01), BOOT)  # sole
    legs(R, TROUS, TROUS, BOOT, lt=1.3, boot_top=0.4, extra=boot)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.17, 0.11, 0.11)), TROUS)
    t.add(ellipsoid((0, 1.17, 0), (0.17, 0.2, 0.12)), FCOAT)
    t.add(ellipsoid((0, 1.32, 0), (0.2, 0.13, 0.13)), FCOAT)
    t.add(capsule((-0.19, 1.41, -0.005), (0.19, 1.41, -0.005), 0.075), FCOAT)
    t.add(lumpy(cone_skirt((0, 1.05, 0), (0, 0.7, -0.01), 0.17, 0.21, -0.16, 0.15), 0.008, 40), FCOAT)
    t.add(box((0, 1.33, 0.13), (0.04, 0.08, 0.01), rnd=0.006), FRANK)                      # bare chest
    R.body(t)
    h = Group("head")
    h.add(capsule((0, 1.44, -0.005), (0, 1.54, 0.005), 0.05), FRANK)
    h.add(box((0, 1.61, 0.012), (0.066, 0.088, 0.078), rnd=0.025), FRANK)                 # square head
    h.add(box((0, 1.64, 0.088), (0.06, 0.012, 0.012), rnd=0.006), FRANK)                  # brow
    h.add(ellipsoid((0, 1.6, 0.092), (0.013, 0.02, 0.016)), FRANK)
    h.add(box((0, 1.705, -0.004), (0.07, 0.026, 0.084), rnd=0.008), HAIR_BK)              # flat top
    h.add(box((0, 1.66, 0.09), (0.06, 0.02, 0.01), rnd=0.004), HAIR_BK)                   # fringe
    for s in (1, -1):
        h.add(capsule((0.04 * s, 1.49, -0.0), (0.075 * s, 1.49, -0.0), 0.013), STEEL)     # neck bolts
    h.add(capsule((-0.05, 1.67, 0.08), (0.03, 1.69, 0.086), 0.005), BOOT)                 # stitches
    R.head(h)

    def bare(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(limb(sh, lerp(sh, elbow, 0.9), 0.08, 0.072), FCOAT)                         # torn sleeve
    arm(R, -1, P["hand_r"], FRANK, FRANK, FRANK, at=1.35, extra=bare, sh_w=0.22)
    arm(R, 1, P["hand_l"], FRANK, FRANK, FRANK, at=1.35, extra=bare, sh_w=0.22)
    g = Group("pipe")
    d, gp = norm(P["pipe"]), P["hand_r"]
    a, b = add(gp, mul(d, -0.22)), add(gp, mul(d, 0.75))
    g.add(capsule(a, b, 0.03), GUN)
    for p in (a, b):
        g.add(disc(p, d, 0.05, 0.03), GUN)                                                # flanges
    R.world(g)


def b_imperfect(R):
    P = R.P
    legs(R, PALE, PALE, PALE, lt=0.85, bare=True)
    t = Group("torso")
    t.add(lumpy(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), 0.01, 50), RAG)               # loin rags
    t.add(ellipsoid((0, 1.15, 0), (0.12, 0.2, 0.09)), PALE)
    t.add(ellipsoid((0.02, 1.3, -0.01), (0.15, 0.12, 0.1)), PALE)
    t.add(ellipsoid((0.11, 1.42, -0.09), (0.13, 0.12, 0.1)), PALE)                        # hump
    t.add(capsule((-0.15, 1.38, -0.005), (0.2, 1.42, -0.005), 0.05), PALE)
    t.add(capsule((-0.07, 1.26, 0.1), (0.06, 1.12, 0.105), 0.006), BLOOD)                 # stitched scar
    R.body(t)
    h = Group("head")
    face(h, PALE)
    h.add(ellipsoid((0.045, 1.65, -0.02), (0.06, 0.055, 0.065)), PALE)                    # swollen skull
    h.add(sphere((0.032, 1.615, 0.07), 0.018), BOOT)                                       # bulging eye
    h.add(sphere((-0.028, 1.6, 0.075), 0.009), BOOT)
    h.add(lumpy(ellipsoid((-0.03, 1.66, -0.03), (0.04, 0.035, 0.05)), 0.01, 90), HAIR_BK)
    R.head(h)
    arm(R, -1, P["hand_r"], PALE, PALE, PALE, at=0.85)
    arm(R, 1, P["hand_l"], PALE, PALE, PALE, at=1.65, sh_w=0.22)                         # overgrown arm
    g = Group("knife")
    sword(g, P["hand_r"], P["knife"], blen=0.24, width=0.02, hilt=0.07, guard=GUN, wrap=WOOD, gw=0.02)
    R.world(g)


def b_perfect(R):
    P = R.P

    def boots(g, s, hip, knee, ankle):
        g.add(limb(lerp(ankle, knee, 0.42), lerp(ankle, knee, 0.36), 0.066, 0.066), GOLD)  # boot trim
    legs(R, SUIT, SUIT, SUIT, boot_top=0.4, extra=boots)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), SUIT)
    t.add(ellipsoid((0, 1.17, 0), (0.135, 0.2, 0.095)), SUIT)
    t.add(ellipsoid((0, 1.31, 0), (0.17, 0.12, 0.105)), SUIT)
    t.add(capsule((-0.17, 1.41, -0.005), (0.17, 1.41, -0.005), 0.058), SUIT)
    t.add(box((0, 0.99, 0), (0.146, 0.022, 0.102), rnd=0.02), GOLD)                       # belt
    t.add(capsule((0, 1.4, 0.09), (0, 1.02, 0.1), 0.008), GOLD)                           # seam
    t.add(capsule((-0.1, 1.44, 0.03), (0.1, 1.44, 0.03), 0.02), GOLD)                     # collar
    R.body(t)
    h = Group("head")
    face(h, PSKIN)
    hair_short(h, HAIR_BL, 0.004)
    h.add(ellipsoid((0.01, 1.668, 0.03), (0.074, 0.036, 0.07)), HAIR_BL)
    R.head(h)
    arm(R, -1, P["hand_r"], SUIT, SUIT, SUIT)
    arm(R, 1, P["hand_l"], SUIT, SUIT, SUIT)
    g = Group("sword")
    sword(g, P["hand_r"], P["blade"], blen=0.72, width=0.022, guard=GOLD, wrap=SUIT)
    R.world(g)


UNITS.update({
    # standing with wrench and remote / remote raised, drone sparks (venedia alchemist)
    "roboticist": dict(build=b_roboticist, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), wrench_in="l", hand_l=W(-0.1, 1.2, 0.18),
                  wrench=aim(108, 0.25), pole_l=(1, -0.8, 0.1), hand_r=W(0.08, 1.04, 0.22),
                  drone=W(-0.38, 1.74, -0.05)),
        "2": dict(feet=FEET(0.07, -0.07, -0.04, 0.05), wrench_in="l", hand_l=W(-0.14, 0.92, 0.12),
                  wrench=aim(-75, 0.3), hand_r=W(0.32, 1.4, 0.15), drone=W(0.76, 1.76, 0.1),
                  zap=True, halo=True)}),
    # electro-rod held low / raised high and arcing                  (rotterland rpuritan)
    "reviver": dict(build=b_reviver, poses={
        "1": dict(feet=FEET(0.08, -0.08), hand_r=W(0.25, 1.05, 0.1), rod=aim(50),
                  hand_l=W(-0.12, 0.95, 0.12)),
        "2": dict(feet=FEET(0.12, -0.12), lean=4, hand_r=W(0.14, 1.78, 0.05), rod=aim(80),
                  hand_l=W(0.05, 1.15, 0.2), arc=True, halo=True)}),
    # syringe held forward / both arms raised with a glowing vial    (albion albdryw)
    "geneticist": dict(build=b_geneticist, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.24, 1.12, 0.1), needle=aim(40),
                  hand_l=W(-0.13, 0.92, 0.08)),
        "2": dict(feet=FEET(0.07, -0.07, -0.04, 0.05), hand_r=W(0.18, 1.84, 0.02), needle=aim(85),
                  hand_l=W(-0.16, 1.82, 0.06), pole_r=(-1, 0, -0.3), pole_l=(1, 0, -0.3),
                  vial=True, halo=True)}),
    # burning flask held out / raised to throw                       (fennoscandia fsvainamoinen)
    "chemist": dict(build=b_chemist, poses={
        "1": dict(feet=FEET(0.1, -0.1), hand_r=W(0.3, 1.16, 0.08), hand_l=W(-0.12, 0.92, 0.1),
                  flame=0.8),
        "2": dict(feet=FEET(0.14, -0.12), lean=-4, hand_r=W(0.32, 1.74, 0.04), hand_l=W(0.12, 1.3, 0.2),
                  pole_r=(-1, -0.3, -0.4), flame=1.6, halo=True)}),
    # probe held low / mechanical arm pointing, probe crackling      (fennoscandia fslouhi)
    "cyberneticist": dict(build=b_cyberneticist, poses={
        "1": dict(feet=FEET(0.06, -0.06, -0.05, 0.05), hand_r=W(0.2, 1.0, 0.1), probe=aim(-55),
                  hand_l=W(-0.12, 0.95, 0.1)),
        "2": dict(feet=FEET(0.14, -0.14), twist=-15, lean=5, hand_r=W(0.52, 1.38, 0.02), probe=aim(2),
                  hand_l=W(-0.32, 1.1, -0.1), cast=True, halo=True)}),
    # arm blade raised / blade high overhead                         (fennoscandia un_fsruohtta)
    "cyberassassin": dict(build=b_cyberassassin, poses={
        "1": dict(feet=FEET(0.12, -0.12), hand_r=W(0.22, 1.3, 0.1), blade=aim(55),
                  hand_l=W(-0.1, 1.05, 0.12)),
        "2": dict(feet=FEET(0.14, -0.12), lean=-3, hand_r=W(0.1, 1.78, 0.04), blade=aim(95),
                  hand_l=W(0.05, 1.15, 0.15), pole_r=(-1, 0, -0.3))}),
    # arms reaching / lunging with arms up                           (domdaniel shiqq)
    "zombie": dict(build=b_zombie, poses={
        "1": dict(feet=FEET(0.1, -0.1), lean=14, nod=15, hand_r=W(0.36, 1.3, -0.02),
                  hand_l=W(0.28, 1.26, 0.14)),
        "2": dict(feet=FEET(0.24, -0.18), body=(0, -0.04, 0), lean=20, nod=-5, hand_r=W(0.32, 1.85, -0.04),
                  hand_l=W(0.2, 1.8, 0.12), pole_r=(-1, -0.2, -0.3), pole_l=(1, -0.2, -0.3), roar=True)}),
    # pipe on the shoulder / swung low                               (albion albgiantsmallsparth)
    "frankenstein": dict(build=b_frankenstein, scale=1.28, shadow=(20, 44), poses={
        "1": dict(feet=FEET(0.17, -0.16, 0.0, 0.04), hand_r=W(0.12, 1.15, 0.18), pipe=aim(125, -0.1),
                  hand_l=W(0.0, 1.32, 0.16)),
        "2": dict(feet=FEET(0.22, -0.2, 0.0, 0.04), body=(0, -0.04, 0), lean=8, twist=-15,
                  hand_r=W(0.36, 1.12, 0.14), pipe=aim(-8), hand_l=W(0.22, 1.12, 0.14))}),
    # crouched with the knife up / lunging stab                      (greatarrada specchamp)
    "imperfect": dict(build=b_imperfect, poses={
        "1": dict(feet=FEET(0.15, -0.14), body=(0, -0.14, 0), lean=25, nod=-15, hand_r=W(0.12, 1.42, 0.05),
                  knife=aim(100), hand_l=W(0.25, 0.95, 0.12)),
        "2": dict(feet=FEET(0.28, -0.18), body=(0, -0.16, 0.02), lean=32, twist=-20, nod=-22,
                  hand_r=W(0.55, 1.12, 0.02), knife=aim(0), hand_l=W(-0.05, 0.9, 0.12))}),
    # sword low in a wide stance / sword raised                      (fennoscandia fsscout)
    "perfect": dict(build=b_perfect, scale=1.06, poses={
        "1": dict(feet=FEET(0.2, -0.16), body=(0, -0.06, 0), lean=6, hand_r=W(0.26, 1.05, 0.1),
                  blade=aim(-35), hand_l=W(0.02, 1.12, 0.18)),
        "2": dict(feet=FEET(0.22, -0.16), body=(0, -0.05, 0), lean=8, hand_r=W(0.3, 1.42, 0.08),
                  blade=aim(55), hand_l=W(-0.12, 1.1, 0.12))}),
})

# ================================================================ heroes
def oriented_ellipsoid(c, r, bas):
    cx, cy, cz = c
    (e0, e1, e2), (rx, ry, rz) = bas, r
    k = min(r)

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        u = (px * e0[0] + py * e0[1] + pz * e0[2]) / rx
        v = (px * e1[0] + py * e1[1] + pz * e1[2]) / ry
        w = (px * e2[0] + py * e2[1] + pz * e2[2]) / rz
        return (sqrt(u * u + v * v + w * w) - 1.0) * k
    return f, c, max(r)


def b_chaosscientist(R):
    """Chaos scientist (hero, no blue anywhere on him): lanky, slouching genius in a lab coat, grey hair hanging down, portal gun."""
    P = R.P
    legs(R, BELT, BELT, SHOE_BR, boot_top=0.15)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), BELT)                                # brown trousers
    t.add(box((0, 1.0, 0), (0.152, 0.032, 0.106), rnd=0.02), SHOE_BR)                     # leather belt
    t.add(box((0, 1.0, 0.13), (0.03, 0.026, 0.01), rnd=0.005), BRASS)                     # buckle
    t.add(ellipsoid((0, 1.17, 0), (0.12, 0.2, 0.085)), LABW)
    t.add(ellipsoid((0, 1.31, 0), (0.145, 0.115, 0.095)), LABW)
    t.add(capsule((-0.15, 1.4, -0.005), (0.15, 1.4, -0.005), 0.05), LABW)
    t.add(box((0, 1.2, 0.082), (0.055, 0.2, 0.01), rnd=0.008), BONE)                    # open coat, shirt
    t.add(cone_skirt((0, 1.08, -0.02), (0, 0.66, -0.06), 0.13, 0.19, -0.2, -0.035), LABW)  # coat tails, open in front
    for s in (1, -1):
        t.add(box((0.075 * s, 1.32, 0.09), (0.02, 0.09, 0.006),
                  (norm((1, 0, 0)), norm((0.3 * s, 1, 0)), (0, 0, 1)), rnd=0.004), LABW)  # lapels
    R.body(t)

    h = Group("head")
    h.add(capsule((0, 1.46, -0.005), (0, 1.54, 0.005), 0.036), SKIN)                     # neck
    h.add(ellipsoid((0, 1.605, 0.012), (0.064, 0.104, 0.08)), SKIN)                       # long face
    h.add(ellipsoid((0, 1.53, 0.04), (0.04, 0.04, 0.045)), SKIN)                          # chin
    h.add(ellipsoid((0, 1.59, 0.09), (0.013, 0.022, 0.018)), SKIN)                        # nose
    for prim in (ellipsoid((0, 1.68, -0.035), (0.084, 0.06, 0.086)),                      # swept back
                 roundcone((0, 1.64, -0.07), (0, 1.42, -0.11), 0.09, 0.11),               # hangs down the back
                 ellipsoid((0.09, 1.6, -0.035), (0.058, 0.095, 0.066)),
                 ellipsoid((-0.09, 1.6, -0.035), (0.058, 0.095, 0.066)),
                 sphere((0.125, 1.5, -0.06), 0.052),                                      # tufts at the shoulders
                 sphere((-0.125, 1.5, -0.06), 0.052),
                 sphere((0.125, 1.68, -0.05), 0.042),                                     # wild wings
                 sphere((-0.125, 1.68, -0.05), 0.042),
                 sphere((0.06, 1.74, -0.05), 0.036),
                 sphere((-0.06, 1.74, -0.05), 0.036)):
        h.add(lumpy(prim, 0.016, 55), HAIR_GR)
    R.head(h)

    arm(R, -1, P["hand_r"], LABW, LABW, SKIN, at=0.85)
    arm(R, 1, P["hand_l"], LABW, LABW, SKIN, at=0.85)

    g = Group("gadgets")
    hr, d = P["hand_r"], norm(P["gun"])
    gb = bar_basis(d)

    def gl(a, b):
        return add(hr, add(mul(d, a), mul(gb[1], b)))
    g.add(box(gl(0.05, 0.04), (0.032, 0.036, 0.085), gb, rnd=0.014), MGREY)              # portal gun body
    g.add(box(gl(0.0, -0.01), (0.016, 0.04, 0.02), gb, rnd=0.006), BOOT)               # grip
    g.add(capsule(gl(0.0, 0.085), gl(0.0, 0.14), 0.024), MGREY)                         # fluid canister
    g.add(capsule(gl(0.0, 0.09), gl(0.0, 0.125), 0.017), G_GREEN)
    g.add(sphere(gl(0.15, 0.04), 0.028), G_GREEN)                                       # emitter
    hl = P["hand_l"]
    g.add(box(add(hl, (0, 0.035, 0)), (0.028, 0.045, 0.012), yaw_basis(-30), rnd=0.008), MGREY)  # hip flask
    R.world(g)
    if P.get("portal"):
        pg = Group("portal")
        c = P["portal"]
        n = norm(add(OUT, mul(SL, 0.7)))
        up = (0, 1, 0)
        side = norm(cross(up, n))
        pg.add(oriented_ellipsoid(c, (0.19, 0.29, 0.035), (side, up, n)), G_GREEN)
        pg.add(capsule(gl(0.17, 0.04), c, 0.012), G_GREEN)                             # beam
        R.world(pg)


UNITS.update({
    # portal gun held low, hip flask / gun raised firing a portal  (venedia astrologer)
    "chaosscientist": dict(build=b_chaosscientist, scale=1.07, poses={
        "1": dict(feet=FEET(0.05, -0.06, -0.05, 0.05), lean=4, nod=12, hand_r=W(0.18, 0.95, 0.06),
                  gun=aim(-55, 0.2), hand_l=W(-0.02, 1.2, 0.2), pole_l=(1, -0.8, 0.1)),
        "2": dict(feet=FEET(0.07, -0.07, -0.04, 0.05), lean=2, nod=-4, hand_r=W(0.36, 1.42, 0.1),
                  gun=aim(18), hand_l=W(-0.14, 1.58, 0.14), pole_l=(1, -0.3, -0.2),
                  portal=W(0.95, 1.38, 0.15), halo=True)}),
})

# ================================================================ second wave
def torus(c, n, R, r):
    """Ring of radius R and tube radius r around axis n (halos)."""
    cx, cy, cz = c
    nx, ny, nz = norm(n)

    def f(x, y, z):
        qx, qy, qz = x - cx, y - cy, z - cz
        h = qx * nx + qy * ny + qz * nz
        rx, ry, rz = qx - nx * h, qy - ny * h, qz - nz * h
        return sqrt((sqrt(rx * rx + ry * ry + rz * rz) - R) ** 2 + h * h) - r
    return f, c, R + r


def plate(c, n, up, half, rnd=0.01):
    """Flat slab facing n (shields)."""
    n = norm(n)
    side = norm(cross(up, n))
    return box(c, half, (side, cross(n, side), n), rnd)


def b_commandrobot(R):
    """Officer android: white ceramic shell, gold trim, sensor visor, antennae, red cape, energy sabre."""
    P = R.P

    def joints(g, s, hip, knee, ankle):
        g.add(sphere(knee, 0.055), MECHD)
        g.add(limb(lerp(knee, ankle, 0.15), lerp(knee, ankle, 0.8), 0.06, 0.05), SUIT)
    legs(R, MECHD, MECHD, SUIT, lt=0.95, boot_top=0.25, extra=joints)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.14, 0.095, 0.095)), SUIT)
    t.add(grooves(capsule((0, 0.98, 0), (0, 1.18, 0), 0.075), (0, 0, 0), (0, 1, 0), 0.03, 0.01), MECHD)  # spine
    t.add(box((0, 1.3, 0.005), (0.16, 0.115, 0.1), rnd=0.06), SUIT)                       # chest shell
    t.add(shell(box((0, 1.3, 0.005), (0.16, 0.115, 0.1), rnd=0.06), 0.006, 1.24, 1.255), GOLD)
    t.add(sphere((0, 1.31, 0.13), 0.022), G_CYAN)                                          # core
    for s in (1, -1):
        pd = ellipsoid((0.205 * s, 1.41, 0), (0.08, 0.06, 0.085))
        t.add(pd, SUIT)
        t.add(shell(pd, 0.006, 1.37, 1.385), GOLD)
    R.body(t)
    c = Group("cape")
    c.add(lumpy(cone_skirt((0, 1.43, -0.09), (0, 0.42, -0.17), 0.16, 0.26, -1.0, -0.09), 0.006, 40), CRED)
    R.body(c)
    h = Group("head")
    h.add(capsule((0, 1.44, 0), (0, 1.54, 0), 0.03), MECHD)
    h.add(ellipsoid((0, 1.615, 0.005), (0.07, 0.092, 0.082)), SUIT)
    h.add(box((0, 1.618, 0.072), (0.06, 0.014, 0.02), rnd=0.008), G_CYAN)                 # visor band
    h.add(shell(ellipsoid((0, 1.615, 0.005), (0.07, 0.092, 0.082)), 0.005, 1.665, 1.68), GOLD)
    for k, (x, tilt) in enumerate(((-0.05, -0.35), (0.0, 0.0), (0.05, 0.35))):            # antenna array
        a = (x, 1.69, -0.02)
        b = add(a, mul(norm((tilt, 1, -0.2)), 0.12 if k == 1 else 0.08))
        h.add(capsule(a, b, 0.006), GOLD)
        h.add(sphere(b, 0.012), G_RED)
    R.head(h)

    def arm_plates(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(sphere(elbow, 0.045), MECHD)
        g.add(limb(lerp(elbow, wrist, 0.15), lerp(elbow, wrist, 0.85), 0.048, 0.042), SUIT)
    arm(R, -1, P["hand_r"], SUIT, MECHD, MECHD, extra=arm_plates)
    arm(R, 1, P["hand_l"], SUIT, MECHD, MECHD, extra=arm_plates)
    g = Group("sabre")
    d, hr = norm(P["blade"]), P["hand_r"]
    g.add(capsule(add(hr, mul(d, -0.08)), add(hr, mul(d, 0.06)), 0.02), MECHD)
    g.add(disc(add(hr, mul(d, 0.07)), d, 0.035, 0.015), GOLD)
    g.add(capsule(add(hr, mul(d, 0.09)), add(hr, mul(d, 0.72)), 0.017), G_CYAN)
    R.world(g)


def b_warbot(R, mk):
    """Big skeletal war droid (a bigger killbot) with a riot shield and a long blade.
    Mark 1 is the bare chrome frame; Mark 2 is heavier, with dark armour plating over it."""
    P = R.P
    heavy = mk == 2

    def frame(g, s, hip, knee, ankle):
        g.add(sphere(hip, 0.06), MECHD)
        g.add(sphere(knee, 0.065 if heavy else 0.058), MECHD)
        g.add(capsule(lerp(hip, knee, 0.15), lerp(knee, ankle, 0.1), 0.016), STEEL)       # piston
        if heavy:
            g.add(limb(lerp(hip, knee, 0.1), lerp(hip, knee, 0.85), 0.085, 0.07), MECHD)  # thigh armour
            g.add(limb(lerp(knee, ankle, 0.15), lerp(knee, ankle, 0.85), 0.07, 0.058), MECHD)
            g.add(sphere(knee, 0.04), CRED)
        else:
            g.add(limb(lerp(knee, ankle, 0.2), lerp(knee, ankle, 0.85), 0.05, 0.042), MECHD)  # shin guard
    legs(R, MECH, MECH, MECHD, lt=0.62, boot_top=0.12, extra=frame)
    t = Group("torso")
    t.add(box((0, 0.93, 0), (0.12, 0.05, 0.07), rnd=0.025), MECHD)                        # pelvis
    t.add(grooves(capsule((0, 0.96, -0.02), (0, 1.2, -0.02), 0.04), (0, 0, 0), (0, 1, 0), 0.035, 0.012), STEEL)
    t.add(grooves(ellipsoid((0, 1.28, 0.0), (0.15, 0.13, 0.095)), (0, 0, 0), (0, 1, 0), 0.042, 0.012), MECH)  # ribcage
    if heavy:
        t.add(box((0, 1.3, 0.02), (0.17, 0.13, 0.11), rnd=0.04), MECHD)                   # breastplate
        t.add(box((0, 1.3, 0.13), (0.03, 0.09, 0.01), rnd=0.006), CRED)
        t.add(box((0, 1.1, 0.04), (0.11, 0.06, 0.07), rnd=0.03), MECHD)
    else:
        t.add(box((0, 1.33, 0.06), (0.09, 0.07, 0.03), rnd=0.02), MECHD)                  # chest plate
    for s in (1, -1):
        t.add(box((0.21 * s, 1.43, 0), (0.1, 0.06, 0.1) if heavy else (0.08, 0.045, 0.08),
                  rnd=0.03), MECHD)                                                        # shoulder blocks
    R.body(t)
    h = Group("head")
    h.add(capsule((0, 1.42, -0.01), (0, 1.53, 0.0), 0.022), STEEL)
    h.add(ellipsoid((0, 1.6, 0.0), (0.055, 0.07, 0.075)), MECH)                           # skull
    h.add(ellipsoid((0, 1.555, 0.035), (0.04, 0.035, 0.05)), MECHD)                       # jaw
    h.add(box((0, 1.6, 0.066), (0.042, 0.01, 0.012), rnd=0.004), G_RED)                   # eye slit
    if heavy:
        h.add(box((0, 1.665, -0.01), (0.012, 0.03, 0.08), rnd=0.008), CRED)               # crest
    R.head(h)

    def skel_arm(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(sphere(elbow, 0.045), MECHD)
        g.add(capsule(sh, lerp(sh, elbow, 0.85), 0.012), STEEL)
        if heavy:
            g.add(limb(lerp(elbow, wrist, 0.1), lerp(elbow, wrist, 0.9), 0.055, 0.05), MECHD)  # vambrace
    arm(R, -1, P["hand_r"], MECH, MECH, MECHD, at=0.7, extra=skel_arm, sh_w=0.21)
    arm(R, 1, P["hand_l"], MECH, MECH, MECHD, at=0.7, extra=skel_arm, sh_w=0.21)
    s = Group("shield")
    n = norm(add(mul(SL, 0.55), OUT))
    c = add(P["hand_l"], mul(n, 0.06))
    hw, hh = (0.17, 0.32) if heavy else (0.13, 0.27)
    s.add(plate(c, n, (0, 1, 0), (hw, hh, 0.01), 0.01), MECHD)                            # rim
    s.add(plate(add(c, mul(n, 0.012)), n, (0, 1, 0), (hw - 0.03, hh - 0.03, 0.008), 0.006), MECH)
    s.add(plate(add(c, mul(n, 0.026)), n, (0, 1, 0), (0.028, hh - 0.07, 0.005), 0.003), CRED)  # stripe
    s.add(plate(add(c, add(mul(n, 0.026), (0, hh * 0.55, 0))), n, (0, 1, 0), (hw - 0.07, 0.012, 0.005), 0.003),
          MECHD)                                                                            # view slit
    R.world(s)
    g = Group("blade")
    sword(g, P["hand_r"], P["blade"], blen=1.05 if heavy else 0.95, width=0.05 if heavy else 0.04,
          hilt=0.12, blade=STEEL, guard=MECHD, wrap=MECHD, gw=0.06)
    R.world(g)


def b_elitetrooper(R):
    """Sacred heavy-weapons storm trooper: bulkier armour with red markings and a rotary cannon."""
    P = R.P

    def plates(g, s, hip, knee, ankle):
        g.add(limb(lerp(hip, knee, 0.2), lerp(hip, knee, 0.85), 0.094, 0.08), TWHITE)
        g.add(sphere(knee, 0.072), CRED)
    legs(R, UNDER, TWHITE, BOOT, lt=1.15, boot_top=0.22, extra=plates)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.16, 0.1, 0.105)), UNDER)
    t.add(box((0, 0.995, 0), (0.16, 0.03, 0.112), rnd=0.025), TWHITE)
    t.add(box((0, 1.12, 0.0), (0.13, 0.09, 0.095), rnd=0.03), UNDER)
    t.add(grooves(box((0, 1.12, 0.055), (0.09, 0.075, 0.038), rnd=0.015), (0, 0, 0), (0, 1, 0), 0.04, 0.008), TWHITE)
    t.add(box((0, 1.31, 0.01), (0.18, 0.12, 0.12), rnd=0.05), TWHITE)                     # chest plate
    t.add(box((0, 1.3, 0.13), (0.05, 0.08, 0.012), rnd=0.008), CRED)                      # rank stripe
    t.add(box((0, 1.28, -0.15), (0.14, 0.14, 0.06), rnd=0.025), TWHITE)                   # power pack
    t.add(capsule((-0.1, 1.45, 0), (0.1, 1.45, 0), 0.055), UNDER)
    for s in (1, -1):
        pd = ellipsoid((0.235 * s, 1.42, 0), (0.105, 0.075, 0.105))                       # heavy pauldrons
        t.add(pd, CRED if s > 0 else TWHITE)
    R.body(t)
    h = Group("head")
    face(h, UNDER, nose=False)
    h.add(ellipsoid((0, 1.625, 0.0), (0.09, 0.104, 0.098)), TWHITE)
    h.add(box((0, 1.614, 0.076), (0.068, 0.02, 0.03), rnd=0.012), VISOR)
    h.add(ellipsoid((0, 1.545, 0.05), (0.064, 0.052, 0.05)), TWHITE)
    h.add(box((0, 1.69, 0.0), (0.012, 0.03, 0.09), rnd=0.008), CRED)                      # crest ridge
    R.head(h)

    def bracer(g, s, J):
        g.add(limb(lerp(J[1], J[2], 0.1), lerp(J[1], J[2], 0.85), 0.056, 0.05), TWHITE)
    d, gp = norm(P["gun"]), P["grip"]
    arm(R, -1, gp, UNDER, UNDER, UNDER, at=1.12, extra=bracer, sh_w=0.21)
    arm(R, 1, add(gp, mul(d, 0.3)), UNDER, UNDER, UNDER, at=1.12, extra=bracer, sh_w=0.21)
    g = Group("cannon")
    gb = bar_basis(d)

    def gl(a, b, c=0.0):
        return add(gp, add(add(mul(d, a), mul(gb[1], b)), mul(gb[0], c)))
    g.add(box(gl(0.05, 0.05), (0.045, 0.05, 0.2), gb, rnd=0.015), BOOT)                   # receiver
    g.add(box(gl(0.08, -0.06), (0.04, 0.05, 0.05), gb, rnd=0.01), GUN)                    # ammo box
    g.add(box(gl(0.0, -0.02), (0.018, 0.045, 0.022), gb, rnd=0.006), BOOT)                # grip
    g.add(box(gl(0.3, 0.11), (0.012, 0.02, 0.06), gb, rnd=0.006), GUN)                    # top handle
    for k in range(3):                                                                    # rotary barrels
        a = TAU * k / 3
        off_b, off_c = 0.05 + 0.022 * cos(a), 0.022 * sin(a)
        g.add(capsule(gl(0.22, off_b, off_c), gl(0.62, off_b, off_c), 0.013), GUN)
    g.add(disc(gl(0.5, 0.05), d, 0.045, 0.02), BOOT)
    g.add(capsule(gl(0.08, -0.08), add(R.T((0.1, 1.2, -0.17)), (0, 0, 0)), 0.014), GUN)  # ammo feed to pack
    if P.get("fire"):
        flash(g, gl(0.64, 0.05), d, 1.5)
    R.world(g)


def b_priest(R):
    """Prophet of Ascension: white and gold robes, cyber-implanted bald head, glowing halo, helix staff."""
    P = R.P

    def robe(t):
        t.add(box((0, 1.0, 0.0), (0.15, 0.03, 0.105), rnd=0.02), GOLD)                    # sash
        t.add(box((0, 0.72, 0.13), (0.035, 0.3, 0.01), rnd=0.006), GOLD)                  # front panel
        t.add(capsule((-0.12, 1.44, 0.02), (0.12, 1.44, 0.02), 0.03), GOLD)               # collar
    robe_body(R, SUIT, SUIT, skirt_to=0.12, extra=robe)
    h = Group("head")
    face(h, SKIN)
    for s in (1, -1):
        h.add(box((0.07 * s, 1.63, -0.01), (0.012, 0.025, 0.03), rnd=0.006), MECH)       # temple implants
    h.add(capsule((0, 1.7, -0.05), (0, 1.66, 0.04), 0.008), MECH)                         # cranial ridge
    R.head(h)
    hl = Group("halo")
    c = (0, 1.65, -0.12)
    hl.add(torus(c, (0, 0.2, 1), 0.13, 0.012), GOLD)
    for k in range(6):
        a = TAU * k / 6
        hl.add(sphere(add(c, (0.13 * cos(a), 0.13 * sin(a), 0.0)), 0.019), G_CYAN)
    R.head(hl)
    arm(R, -1, P["hand_r"], SUIT, SUIT, SKIN)
    arm(R, 1, P["hand_l"], SUIT, SUIT, SKIN)
    g = Group("staff")
    d, hr = norm(P["staff"]), P["hand_r"]
    lo, top = add(hr, mul(d, -P.get("below", 0.85))), add(hr, mul(d, 0.42))
    g.add(capsule(lo, top, 0.014), GOLD)
    n1, n2 = perp(d, (0, 0, 1))
    for k in range(9):                                                                    # double helix head
        u = k / 8
        a = u * TAU * 1.2
        base = add(top, mul(d, u * 0.2))
        for ph in (0, math.pi):
            g.add(sphere(add(base, add(mul(n1, 0.04 * cos(a + ph)), mul(n2, 0.04 * sin(a + ph)))), 0.014),
                  GOLD if ph == 0 else STEEL)
    g.add(sphere(add(top, mul(d, 0.25)), 0.035 if P.get("cast") else 0.026), G_CYAN)
    R.world(g)


def b_inquisitor(R):
    """Procurement agent: black leather greatcoat, wide-brimmed hat, red goggles, tranquilliser pistol."""
    P = R.P

    def coat(t):
        t.add(box((0, 0.99, 0), (0.15, 0.026, 0.104), rnd=0.02), BELT)
        t.add(torus((0.11, 0.92, 0.07), (0.3, 0.2, 1), 0.035, 0.008), STEEL)             # manacles
        t.add(torus((0.13, 0.86, 0.08), (0.3, -0.3, 1), 0.035, 0.008), STEEL)
        t.add(capsule((-0.1, 1.46, -0.04), (0.1, 1.46, -0.04), 0.045), FCOAT)             # high collar
        t.add(box((0, 1.33, 0.105), (0.03, 0.08, 0.008), rnd=0.004), CRED)                # red vest
    robe_body(R, FCOAT, FCOAT, skirt_to=0.22, legs_mat=TROUS, extra=coat)
    h = Group("head")
    face(h, PALE)
    h.add(disc((0, 1.68, 0.0), (0, 1, 0.05), 0.135, 0.014), BOOT)                        # hat brim
    h.add(roundcone((0, 1.69, -0.005), (0, 1.78, -0.005), 0.082, 0.07), BOOT)             # crown
    h.add(shell(roundcone((0, 1.69, -0.005), (0, 1.78, -0.005), 0.082, 0.07), 0.005, 1.7, 1.725), CRED)
    for s in (1, -1):
        h.add(disc((0.03 * s, 1.612, 0.082), (0, 0, 1), 0.017, 0.012), CRED)              # red goggles
    R.head(h)
    arm(R, -1, P["hand_r"], FCOAT, FCOAT, BOOT)
    arm(R, 1, P["hand_l"], FCOAT, FCOAT, BOOT)
    g = Group("pistol")
    d = norm(P["gun"])
    muzzle = pistol(g, P["hand_r"], d, body=GUN, grip=BOOT)
    g.add(capsule(add(P["hand_r"], add(mul(d, 0.02), (0, 0.075, 0))),
                  add(P["hand_r"], add(mul(d, 0.1), (0, 0.075, 0))), 0.018), G_GREEN)    # dart vial
    if P.get("fire"):
        g.add(capsule(add(muzzle, mul(d, 0.12)), add(muzzle, mul(d, 0.2)), 0.008), STEEL)  # dart in flight
        g.add(sphere(add(muzzle, mul(d, 0.03)), 0.02), G_GREEN)
    R.world(g)


def clone_base(R, armour=False):
    legs(R, CLONE, CLONE, BOOT, boot_top=0.35)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), CLONE)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), CLONE)
    t.add(ellipsoid((0, 1.31, 0), (0.162, 0.12, 0.106)), CLONE)
    t.add(capsule((-0.165, 1.41, -0.005), (0.165, 1.41, -0.005), 0.056), CLONE)
    t.add(box((0, 0.99, 0), (0.148, 0.024, 0.104), rnd=0.02), BOOT)
    t.add(box((0.08, 1.36, 0.105), (0.03, 0.018, 0.006), rnd=0.003), BOOT)               # serial tag
    if armour:
        t.add(box((0, 1.27, 0.01), (0.15, 0.13, 0.11), rnd=0.04), MECH)                   # chest armour
        for s in (1, -1):
            t.add(ellipsoid((0.2 * s, 1.42, 0), (0.08, 0.055, 0.085)), MECH)
    R.body(t)
    h = Group("head")
    face(h, CSKIN)
    h.add(box((0, 1.65, -0.07), (0.025, 0.012, 0.01), rnd=0.003), BOOT)                   # barcode
    if armour:
        h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.006, 0.006, 0.006))), 0.005, 1.6, 1.615), MECHD)  # headset
        h.add(capsule((-0.075, 1.6, 0.0), (-0.05, 1.56, 0.08), 0.007), MECHD)              # mic
    R.head(h)


def b_clone(R):
    """Vat-grown drone: bald, identical, grey-blue jumpsuit, stun baton."""
    P = R.P
    clone_base(R)
    arm(R, -1, P["hand_r"], CLONE, CLONE, CSKIN)
    arm(R, 1, P["hand_l"], CLONE, CLONE, CSKIN)
    g = Group("baton")
    d, hr = norm(P["baton"]), P["hand_r"]
    g.add(capsule(add(hr, mul(d, -0.06)), add(hr, mul(d, 0.36)), 0.017), MECHD)
    g.add(sphere(add(hr, mul(d, 0.38)), 0.026 if P.get("zap") else 0.02), G_SPARK)
    if P.get("zap"):
        tip = add(hr, mul(d, 0.38))
        for k, v in enumerate((aim(40), aim(120, 0.2), aim(-20))):
            bolt(g, tip, add(tip, mul(v, 0.12)), G_SPARK, 0.008, 3, 0.025, seed=k + 5)
    R.world(g)


def b_clonesoldier(R):
    """The same clone in light armour and headset, with a bayonet rifle."""
    P = R.P
    clone_base(R, armour=True)
    arm(R, -1, P["grip"], CLONE, CLONE, BOOT)
    arm(R, 1, add(P["grip"], mul(norm(P["gun"]), 0.34)), CLONE, CLONE, BOOT)
    g = Group("rifle")
    rifle(g, P["grip"], P["gun"], body=BOOT, furn=MECHD, k=1.15)
    R.world(g)


def b_abomination(R):
    """Failed experiment: bloated stitched flesh, a second head, stunted extra arms, a bone-bladed giant arm."""
    P = R.P

    def leg_stitch(g, s, hip, knee, ankle):
        g.add(ellipsoid(lerp(hip, knee, 0.4), (0.1, 0.12, 0.1)), FLESH)
    legs(R, FLESH, FLESH, FLESH, lt=1.35, bare=True, extra=leg_stitch)
    t = Group("torso")
    t.add(lumpy(ellipsoid((0, 0.96, 0), (0.17, 0.12, 0.12)), 0.012, 40), RAG)
    t.add(lumpy(ellipsoid((0, 1.18, 0.02), (0.2, 0.22, 0.17)), 0.02, 30), FLESH)          # bloated belly
    t.add(lumpy(ellipsoid((0.02, 1.36, -0.02), (0.22, 0.14, 0.14)), 0.015, 35), FLESH)
    t.add(ellipsoid((0.12, 1.45, -0.1), (0.13, 0.12, 0.11)), FLESH)                       # hump
    t.add(capsule((-0.08, 1.32, 0.15), (0.06, 1.08, 0.19), 0.008), BLOOD)                 # stitches
    t.add(capsule((-0.12, 1.16, 0.16), (0.1, 1.2, 0.17), 0.008), BLOOD)
    t.add(capsule((0.1, 1.32, 0.12), (0.14, 1.28, 0.2), 0.01), MECHD)                     # tube port
    for s, y in ((1, 1.22), (-1, 1.26)):                                                  # stunted extra arms
        a = (0.17 * s, y, 0.1)
        e = add(a, (0.08 * s, -0.06, 0.08))
        t.add(roundcone(a, e, 0.035, 0.028), FLESH)
        t.add(roundcone(e, add(e, (0.0, -0.08, 0.04)), 0.028, 0.02), FLESH)
    R.body(t)
    h = Group("head")
    face(h, FLESH)
    h.add(sphere((0.03, 1.612, 0.072), 0.016), BOOT)
    h.add(sphere((-0.026, 1.6, 0.078), 0.01), G_RED)                                      # one burning eye
    h.add(ellipsoid((0, 1.54, 0.075), (0.035, 0.016, 0.012)), BLOOD)                      # mouth
    h.add(capsule((-0.05, 1.68, 0.06), (0.06, 1.66, 0.08), 0.006), BLOOD)                 # skull stitches
    R.head(h)
    h2 = Group("head2")                                                                   # second head on the shoulder
    h2.add(ellipsoid((0.2, 1.53, 0.0), (0.05, 0.06, 0.055)), FLESH)
    h2.add(sphere((0.21, 1.54, 0.05), 0.012), BOOT)
    h2.add(ellipsoid((0.2, 1.5, 0.05), (0.02, 0.008, 0.008)), BLOOD)
    R.body(h2)

    def claw(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(lumpy(ellipsoid(lerp(sh, elbow, 0.45), (0.11, 0.12, 0.11)), 0.01, 40), FLESH)  # swollen biceps
        bd = norm(P["claw"])
        sb = blade_basis(bd)
        for k, off in enumerate((-0.035, 0.0, 0.035)):                                    # bone blades
            base = add(hc, mul(sb[0], off))
            ln = 0.32 if k == 1 else 0.24
            g.add(box(add(base, mul(bd, ln / 2 + 0.03)), (0.012, 0.008, ln / 2), sb, rnd=0.006), BONE)
    arm(R, -1, P["hand_r"], FLESH, FLESH, FLESH, at=1.9, extra=claw, sh_w=0.22)
    arm(R, 1, P["hand_l"], FLESH, FLESH, FLESH, at=1.1)


def b_fieldagent(R):
    """Field agent: tan trench coat, fedora, sunglasses, silenced pistol."""
    P = R.P

    def coat(t):
        t.add(box((0, 1.0, 0.0), (0.15, 0.026, 0.104), rnd=0.02), TRENCH)                 # belt
        t.add(box((0, 1.36, 0.105), (0.03, 0.06, 0.008), rnd=0.004), SHIRT)
        t.add(box((0, 1.34, 0.115), (0.01, 0.06, 0.005), rnd=0.003), BOOT)               # tie
        for s in (1, -1):
            t.add(box((0.065 * s, 1.36, 0.11), (0.024, 0.075, 0.008),
                      (norm((1, 0, 0)), norm((0.35 * s, 1, 0)), (0, 0, 1)), rnd=0.004), TRENCH)
    robe_body(R, TRENCH, TRENCH, skirt_to=0.45, legs_mat=TROUS, extra=coat)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BK, 0.003)
    h.add(disc((0, 1.675, 0.005), (0, 1, 0.08), 0.112, 0.01), FCOAT)                     # fedora brim
    h.add(roundcone((0, 1.675, -0.005), (0, 1.75, -0.01), 0.08, 0.068), FCOAT)
    h.add(shell(roundcone((0, 1.675, -0.005), (0, 1.75, -0.01), 0.08, 0.068), 0.005, 1.68, 1.7), BOOT)
    h.add(box((0, 1.61, 0.08), (0.058, 0.014, 0.01), rnd=0.006), BOOT)                   # sunglasses
    R.head(h)
    arm(R, -1, P["hand_r"], TRENCH, TRENCH, BOOT)
    arm(R, 1, P["hand_l"], TRENCH, TRENCH, BOOT)
    g = Group("pistol")
    d = norm(P["gun"])
    muzzle = pistol(g, P["hand_r"], d, body=BOOT, grip=BOOT)
    g.add(capsule(add(muzzle, mul(d, -0.02)), add(muzzle, mul(d, 0.12)), 0.016), GUN)    # silencer
    if P.get("fire"):
        flash(g, add(muzzle, mul(d, 0.12)), d, 0.5)
    R.world(g)


WARBOT_POSES = {
    "1": dict(feet=FEET(0.12, -0.12, 0.0, 0.05), hand_r=W(0.22, 1.42, 0.04), blade=aim(76, -0.1),
              hand_l=W(-0.04, 1.1, 0.3), pole_l=(1, -0.5, -0.2)),
    "2": dict(feet=FEET(0.26, -0.18, 0.0, 0.04), body=(0, -0.05, 0.02), lean=8, twist=-15,
              hand_r=W(0.55, 1.25, 0.05), blade=aim(4), hand_l=W(-0.02, 1.12, 0.3), pole_l=(1, -0.5, -0.2)),
}

UNITS.update({
    # energy sabre low / raised                                      (venedia captain)
    "commandrobot": dict(build=b_commandrobot, poses={
        "1": dict(feet=FEET(0.14, -0.12, 0.02, 0.04), lean=3, hand_r=W(0.22, 1.0, 0.1), blade=aim(-40),
                  hand_l=W(-0.13, 1.0, 0.12)),
        "2": dict(feet=FEET(0.2, -0.14, 0.02, 0.04), body=(0, -0.04, 0), lean=6, hand_r=W(0.28, 1.36, 0.08),
                  blade=aim(64), hand_l=W(-0.13, 1.02, 0.12), halo=True)}),
    # blade up beside the shield / horizontal slash                 (greatarrada swordplate)
    # Mark 1, size 4: bare chrome frame
    "warbotmk1": dict(build=lambda R: b_warbot(R, 1), file="warbot_mk1_", res=128, scale=1.6,
                      shadow=(50, 80), poses=WARBOT_POSES),
    # Mark 2, size 6: armour-plated, bigger shield and blade
    "warbotmk2": dict(build=lambda R: b_warbot(R, 2), file="warbot_mk2_", res=128, scale=2.1,
                      shadow=(44, 86), poses=WARBOT_POSES),
    # cannon carried high / firing from the hip                      (rotterland rarbal)
    "elitetrooper": dict(build=b_elitetrooper, poses={
        "1": dict(feet=FEET(0.1, -0.1, -0.02, 0.05), grip=W(0.12, 1.08, 0.18), gun=aim(48, 0.1)),
        "2": dict(feet=FEET(0.2, -0.16, 0.0, 0.04), body=(0, -0.04, 0), lean=4, twist=-12,
                  grip=W(0.18, 1.12, 0.12), gun=aim(2), fire=True, halo=True)}),
    # staff at the side / staff raised high, hand thrust forward     (greatarrada highpriestess)
    "priest": dict(build=b_priest, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.22, 1.08, 0.1), staff=aim(84),
                  hand_l=W(-0.06, 1.1, 0.18), halo=True),
        "2": dict(feet=FEET(0.07, -0.07, -0.04, 0.05), hand_r=W(0.2, 1.72, 0.06), staff=aim(84), below=0.6,
                  hand_l=W(0.24, 1.32, 0.2), pole_l=(1, -0.6, 0.2), cast=True, halo=True)}),
    # standing, hand on hip / arm thrust out firing a dart           (venedia doctor)
    "inquisitor": dict(build=b_inquisitor, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.18, 0.98, 0.1), gun=aim(-70, 0.2),
                  hand_l=W(-0.2, 1.0, 0.06), pole_l=(1, 0.1, -0.5)),
        "2": dict(feet=FEET(0.07, -0.07, -0.04, 0.05), hand_r=W(0.5, 1.36, 0.08), gun=aim(0),
                  hand_l=W(-0.2, 1.0, 0.06), pole_l=(1, 0.1, -0.5), fire=True)}),
    # standing / baton raised to strike                              (domdaniel mushrik)
    "clone": dict(build=b_clone, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.17, 0.92, 0.06), baton=aim(-75, 0.2),
                  hand_l=W(-0.13, 0.92, 0.08)),
        "2": dict(feet=FEET(0.1, -0.08, -0.02, 0.05), hand_r=W(0.24, 1.62, 0.06), baton=aim(70),
                  hand_l=W(-0.13, 0.95, 0.1), zap=True, halo=True)}),
    # rifle angled up / crouched bayonet thrust                      (venedia cityguard)
    "clonesoldier": dict(build=b_clonesoldier, poses={
        "1": dict(feet=FEET(0.1, -0.1, 0.0, 0.05), grip=W(0.06, 1.0, 0.2), gun=aim(52, 0.1)),
        "2": dict(feet=FEET(0.26, -0.2, 0.02, 0.0), body=(0, -0.08, 0.03), lean=12, twist=-20,
                  grip=W(0.1, 1.08, 0.06), gun=aim(4))}),
    # bone claw raised / swung forward                               (greatarrada eliteplate)
    "abomination": dict(build=b_abomination, scale=1.32, shadow=(18, 46), poses={
        "1": dict(feet=FEET(0.16, -0.15, 0.0, 0.04), body=(0, -0.05, 0), lean=12, nod=-10,
                  hand_r=W(0.3, 1.6, 0.0), claw=aim(118), hand_l=W(-0.05, 0.95, 0.15),
                  pole_r=(-1, -0.6, -0.3)),
        "2": dict(feet=FEET(0.26, -0.18, 0.0, 0.04), body=(0, -0.08, 0.02), lean=22, twist=-15, nod=-18,
                  hand_r=W(0.62, 1.1, 0.0), claw=aim(-8), hand_l=W(0.0, 0.95, 0.15))}),
    # crouched, pistol low / lunging to fire                         (venedia giustiziere)
    "fieldagent": dict(build=b_fieldagent, poses={
        "1": dict(feet=FEET(0.14, -0.12, 0.0, 0.04), body=(0, -0.05, 0), lean=6, hand_r=W(0.24, 1.0, 0.1),
                  gun=aim(-35), hand_l=W(-0.08, 1.02, 0.15)),
        "2": dict(feet=FEET(0.26, -0.2, 0.02, 0.0), body=(0, -0.09, 0.02), lean=12, twist=-15,
                  hand_r=W(0.55, 1.3, 0.04), gun=aim(4), hand_l=W(-0.14, 1.0, 0.1), fire=True, halo=True)}),
})

# ================================================================ the electric faith
def lightning(g, a, b, seed=1, r=0.012, kinks=6, amp=0.06, branches=2, mat=G_SPARK):
    """Forked lightning from a to b: a zig-zag trunk with short side branches."""
    d = sub(b, a)
    L = length(d)
    n1, n2 = perp(norm(d), (0, 0, 1))
    pts = [a]
    for i in range(1, kinks):
        w = amp * sin(seed * 7.3 + i * 2.9)
        pts.append(add(add(a, mul(d, i / kinks)), add(mul(n1, w), mul(n2, w * 0.4))))
    pts.append(b)
    for p, q in zip(pts, pts[1:]):
        g.add(capsule(p, q, r), mat)
    for k in range(branches):
        p = pts[2 + 2 * k] if 2 + 2 * k < len(pts) - 1 else pts[-2]
        side = 1 if (k + int(seed)) % 2 else -1
        tip = add(p, add(mul(norm(d), L * 0.22), mul(n1, side * L * 0.16)))
        bolt(g, p, tip, mat, r * 0.75, 3, amp * 0.5, seed + k + 0.5)


def cable(g, pts, r=0.012, mat=BOOT):
    for p, q in zip(pts, pts[1:]):
        g.add(capsule(p, q, r), mat)


def b_arcadept(R):
    """Hooded lightning caster: black robe, glowing eyes, capacitor pack wired to copper gauntlets."""
    P = R.P

    def robe(t):
        t.add(box((0, 0.99, 0), (0.15, 0.024, 0.104), rnd=0.02), COPPER)                 # copper belt
        t.add(box((0, 1.26, -0.15), (0.11, 0.13, 0.06), rnd=0.02), MECHD)                 # capacitor pack
        for y in (1.18, 1.26, 1.34):
            t.add(torus((0, y, -0.15), (0, 1, 0), 0.115, 0.012), COPPER)
        t.add(sphere((0, 1.42, -0.16), 0.03), G_SPARK)
    robe_body(R, FCOAT, FCOAT, skirt_to=0.1, extra=robe)
    h = Group("head")
    face(h, PALE)
    eyes(h, G_CYAN, r=0.012)
    R.head(h)
    hd = Group("hood")
    hd.add(lumpy(ellipsoid((0, 1.63, -0.015), (0.1, 0.11, 0.105)), 0.005, 50), FCOAT)
    hd.cut(box((0, 1.58, 0.15), (0.068, 0.085, 0.08)), FCOAT)
    hd.add(lumpy(ellipsoid((0, 1.45, -0.02), (0.15, 0.06, 0.12)), 0.006, 50), FCOAT)    # mantle
    R.head(hd)

    def gauntlet(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(limb(lerp(elbow, wrist, 0.35), wrist, 0.047, 0.045), COPPER)
        for t in (0.55, 0.8):
            g.add(torus(lerp(elbow, wrist, t), d, 0.05, 0.008), BOOT)
    Js = {s: arm(R, s, P["hand_r" if s < 0 else "hand_l"], FCOAT, FCOAT, BOOT, extra=gauntlet)
          for s in (-1, 1)}
    c = Group("cables")
    for s in (-1, 1):
        sh, elbow, wrist, d, hc = Js[s]
        pack = R.T((0.09 * s, 1.3, -0.2))
        cable(c, [pack, add(R.T((0.2 * s, 1.36, -0.1)), (0, 0.02, 0)), lerp(elbow, wrist, 0.4)], 0.011, BOOT)
    R.world(c)
    z = Group("lightning")
    for k, s in enumerate((-1, 1)):
        hc = Js[s][4]
        if P.get("cast"):
            lightning(z, add(hc, mul(SL, 0.03)), add(hc, mul(aim(P["bolt"][k]), 0.8)),
                      seed=3 + k, r=0.01, kinks=5, amp=0.1, branches=1)
        else:
            bolt(z, add(hc, (0.0, -0.03, 0.0)), add(hc, (0.04, -0.12, 0.03)), G_SPARK, 0.008, 3, 0.02, seed=k + 2)
            bolt(z, add(hc, (0.02, 0.0, 0.0)), add(hc, mul(SL, 0.09)), G_SPARK, 0.007, 3, 0.02, seed=k + 7)
    R.world(z)


def b_arcmage(R):
    """Hovering, hugely muscular arc mage: bare chest, brown trousers, cables bursting out of him."""
    P = R.P
    legs(R, BELT, BELT, SKIN, lt=1.32, boot_top=0)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.16, 0.105, 0.105)), BELT)
    t.add(box((0, 0.99, 0), (0.155, 0.025, 0.108), rnd=0.02), BOOT)                      # belt
    t.add(ellipsoid((0, 1.1, 0.0), (0.135, 0.13, 0.1)), SKIN)                             # waist
    t.add(grooves(box((0, 1.12, 0.07), (0.07, 0.1, 0.035), rnd=0.03), (0, 0, 0), (0, 1, 0), 0.05, 0.01), SKIN)  # abs
    t.add(ellipsoid((0, 1.26, -0.01), (0.22, 0.15, 0.115)), SKIN)                         # lats, V-taper
    for s in (1, -1):
        t.add(ellipsoid((0.08 * s, 1.31, 0.075), (0.09, 0.068, 0.055)), SKIN)             # pecs
        t.add(ellipsoid((0.085 * s, 1.455, -0.02), (0.08, 0.055, 0.06)), SKIN)            # traps
        t.add(sphere((0.24 * s, 1.41, 0.0), 0.088), SKIN)                                  # deltoids
        t.add(disc((0.12 * s, 1.36, 0.115), (0.3 * s, 0, 1), 0.018, 0.012), COPPER)       # cable sockets
    t.add(disc((0, 1.2, 0.12), (0, 0, 1), 0.022, 0.012), COPPER)
    R.body(t)
    h = Group("head")
    h.add(capsule((0, 1.44, -0.01), (0, 1.54, 0.0), 0.058), SKIN)                         # bull neck
    h.add(ellipsoid(HEAD_C, (0.07, 0.092, 0.084)), SKIN)
    h.add(ellipsoid((0, 1.55, 0.035), (0.058, 0.04, 0.05)), SKIN)                         # square jaw
    h.add(ellipsoid((0, 1.588, 0.092), (0.013, 0.02, 0.018)), SKIN)
    eyes(h, G_CYAN, r=0.012)
    h.add(ellipsoid((0, 1.655, -0.01), (0.072, 0.045, 0.08)), HAIR_BK)                    # shaved stubble
    R.head(h)

    def biceps(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(ellipsoid(lerp(sh, elbow, 0.55), (0.085, 0.085, 0.085)), SKIN)
        g.add(ellipsoid(lerp(elbow, wrist, 0.25), (0.07, 0.07, 0.07)), SKIN)               # forearm
        g.add(torus(lerp(elbow, wrist, 0.7), d, 0.055, 0.01), COPPER)                     # copper cuff
    Js = {s: arm(R, s, P["hand_r" if s < 0 else "hand_l"], SKIN, SKIN, SKIN, at=1.5,
                 extra=biceps, sh_w=0.24) for s in (-1, 1)}
    c = Group("cables")                                                                   # tendrils of cable
    for k, (port, mid, tip) in enumerate((
            ((0.1, 1.38, -0.1), (0.3, 1.7, -0.25), (0.42, 1.95, -0.35)),
            ((-0.1, 1.38, -0.1), (-0.3, 1.72, -0.25), (-0.38, 2.0, -0.3)),
            ((0.14, 1.25, -0.11), (0.42, 1.38, -0.3), (0.62, 1.55, -0.38)),
            ((-0.14, 1.25, -0.11), (-0.42, 1.4, -0.3), (-0.6, 1.6, -0.34)),
            ((0.08, 1.05, -0.1), (0.34, 0.92, -0.3), (0.52, 0.98, -0.42)),
            ((-0.08, 1.05, -0.1), (-0.3, 0.9, -0.32), (-0.48, 1.0, -0.4)))):
        a, m = R.T(port), R.T(mid)
        b = R.T(tip)
        cable(c, [a, lerp(a, m, 0.5), m, lerp(m, b, 0.5), b], 0.013, BOOT)
        c.add(sphere(b, 0.022), G_SPARK)
    for s in (-1, 1):                                                                     # cables into the arms
        sh, elbow, wrist, d, hc = Js[s]
        cable(c, [R.T((0.12 * s, 1.36, 0.115)), add(R.T((0.2 * s, 1.3, 0.16)), (0, -0.03, 0)), lerp(elbow, wrist, 0.7)],
              0.011, BOOT)
    R.world(c)
    z = Group("lightning")
    for k, s in enumerate((-1, 1)):
        hc = Js[s][4]
        if P.get("cast"):
            lightning(z, hc, add(hc, mul(aim(P["bolt"][k]), 0.9)), seed=11 + k, r=0.011, kinks=5, amp=0.11,
                      branches=1)
        else:
            bolt(z, hc, add(hc, (0.05, 0.14, 0.02)), G_SPARK, 0.008, 3, 0.025, seed=k + 4)
    if P.get("cast"):
        for k in range(2):                                                                # arcs between cable tips
            bolt(z, R.T(((0.42, 1.95, -0.35), (-0.38, 2.0, -0.3))[k]), R.T((0.0, 2.05, -0.3)), G_SPARK, 0.008, 3, 0.03,
                 seed=k + 9)
    R.world(z)


def b_teslatrooper(R):
    """Sacred tesla trooper: heavy gunmetal-and-copper power armour, coil pack, tesla rifle."""
    P = R.P

    def plates(g, s, hip, knee, ankle):
        g.add(limb(lerp(hip, knee, 0.15), lerp(hip, knee, 0.85), 0.1, 0.085), MECH)
        g.add(sphere(knee, 0.08), COPPER)
        g.add(limb(lerp(knee, ankle, 0.15), lerp(knee, ankle, 0.9), 0.082, 0.07), MECH)
    legs(R, UNDER, UNDER, MECHD, lt=1.25, boot_top=0.2, extra=plates)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.17, 0.11, 0.11)), UNDER)
    t.add(box((0, 0.99, 0), (0.17, 0.035, 0.12), rnd=0.025), COPPER)
    t.add(box((0, 1.12, 0.0), (0.14, 0.1, 0.1), rnd=0.035), MECHD)
    t.add(box((0, 1.31, 0.01), (0.18, 0.12, 0.12), rnd=0.05), MECH)                       # chest plate
    t.add(shell(box((0, 1.31, 0.01), (0.18, 0.12, 0.12), rnd=0.05), 0.007, 1.2, 1.215), COPPER)
    t.add(box((0, 1.31, 0.14), (0.035, 0.07, 0.012), rnd=0.008), G_SPARK)                 # reactor slit
    t.add(box((0, 1.28, -0.17), (0.15, 0.15, 0.07), rnd=0.03), MECHD)                     # generator pack
    for s in (1, -1):                                                                     # twin coils on the pack
        base = (0.09 * s, 1.42, -0.19)
        t.add(grooves(capsule(base, add(base, (0, 0.18, 0)), 0.035), base, (0, 1, 0), 0.025, 0.008), COPPER)
        t.add(sphere(add(base, (0, 0.22, 0)), 0.035), G_SPARK)
        t.add(ellipsoid((0.25 * s, 1.43, 0), (0.12, 0.085, 0.12)), MECH)                  # huge pauldrons
        t.add(shell(ellipsoid((0.25 * s, 1.43, 0), (0.12, 0.085, 0.12)), 0.007, 1.375, 1.395), COPPER)
    R.body(t)
    h = Group("head")
    h.add(capsule((0, 1.44, 0), (0, 1.54, 0), 0.06), UNDER)
    h.add(box((0, 1.605, 0.0), (0.058, 0.07, 0.068), rnd=0.03), MECH)                     # helm
    h.add(box((0, 1.612, 0.088), (0.06, 0.014, 0.01), rnd=0.006), G_CYAN)                 # visor
    h.add(box((0, 1.545, 0.08), (0.045, 0.03, 0.02), rnd=0.01), COPPER)                   # grille
    h.add(box((0, 1.68, -0.01), (0.014, 0.025, 0.085), rnd=0.008), COPPER)                # crest
    R.head(h)

    def gauntlet(g, s, J):
        g.add(limb(lerp(J[1], J[2], 0.1), lerp(J[1], J[2], 0.9), 0.064, 0.058), MECH)
        g.add(sphere(J[1], 0.06), COPPER)
    d, gp = norm(P["gun"]), P["grip"]
    arm(R, -1, gp, UNDER, UNDER, MECHD, at=1.3, extra=gauntlet, sh_w=0.23)
    arm(R, 1, add(gp, mul(d, 0.32)), UNDER, UNDER, MECHD, at=1.3, extra=gauntlet, sh_w=0.23)
    g = Group("teslagun")
    gb = bar_basis(d)

    def gl(a, b):
        return add(gp, add(mul(d, a), mul(gb[1], b)))
    g.add(box(gl(-0.18, 0.0), (0.03, 0.055, 0.11), gb, rnd=0.015), MECHD)                 # stock
    g.add(box(gl(0.06, 0.05), (0.04, 0.05, 0.16), gb, rnd=0.012), MECHD)                  # body
    g.add(box(gl(0.0, -0.02), (0.018, 0.045, 0.022), gb, rnd=0.006), MECHD)
    g.add(capsule(gl(0.02, 0.11), gl(0.2, 0.11), 0.022), GLASS)                           # capacitor tube
    g.add(capsule(gl(0.04, 0.11), gl(0.18, 0.11), 0.013), G_SPARK)
    g.add(grooves(capsule(gl(0.22, 0.05), gl(0.55, 0.05), 0.04), gp, d, 0.035, 0.012), COPPER)  # coil barrel
    g.add(torus(gl(0.6, 0.05), d, 0.05, 0.016), STEEL)
    tip = gl(0.66, 0.05)
    g.add(sphere(tip, 0.035), G_SPARK)
    if P.get("fire"):
        lightning(g, tip, add(tip, add(mul(d, 1.0), (0, -0.04, 0))), seed=5, r=0.012, kinks=5, amp=0.11, branches=2)
    R.world(g)


def b_teslapylon(R):
    """Immobile tesla coil tower: plated base, copper coil column, toroid crown throwing lightning."""
    P = R.P
    g = Group("base")
    g.add(box((0, 0.12, 0), (0.42, 0.12, 0.42), yaw_basis(45), rnd=0.03), MECHD)
    g.add(box((0, 0.27, 0), (0.3, 0.05, 0.3), yaw_basis(45), rnd=0.02), COPPER)
    for k in range(4):                                                                    # lattice legs
        a = TAU * (k + 0.5) / 4
        g.add(capsule((0.3 * cos(a), 0.3, 0.3 * sin(a)), (0.08 * cos(a), 1.9, 0.08 * sin(a)), 0.026), MECH)
    for y in (0.8, 1.35):
        g.add(torus((0, y, 0), (0, 1, 0), 0.24 - (y - 0.3) * 0.1, 0.018), MECH)
    R.world(g)
    c = Group("coil")
    c.add(grooves(capsule((0, 0.3, 0), (0, 2.1, 0), 0.1), (0, 0, 0), (0, 1, 0), 0.04, 0.014), COPPER)
    c.add(roundcone((0, 2.05, 0), (0, 2.25, 0), 0.05, 0.03), MECHD)
    R.world(c)
    t = Group("toroid")
    top = (0, 2.32, 0)
    t.add(torus(top, (0, 1, 0), 0.26, 0.1), STEEL)
    t.add(sphere(add(top, (0, 0.06, 0)), 0.06), G_SPARK)
    R.world(t)
    z = Group("lightning")
    rim = lambda a: add(top, (0.36 * cos(a), 0.0, 0.36 * sin(a)))
    if P.get("fire"):
        for k, (a, target) in enumerate(((2.4, W(1.3, 1.2, 0.1)), (2.9, W(1.0, 0.05, 0.2)),
                                         (1.6, W(0.5, 2.9, 0.0)), (-0.6, W(-0.9, 2.6, 0.0)))):
            lightning(z, rim(a), target, seed=k + 21, r=0.016 if k < 2 else 0.011, amp=0.1, branches=2 if k < 2 else 1)
    else:
        for k, a in enumerate((2.6, 0.4, -1.6)):
            p = rim(a)
            bolt(z, p, add(p, (0.18 * cos(a), 0.12, 0.18 * sin(a))), G_SPARK, 0.01, 3, 0.04, seed=k + 31)
    R.world(z)


def b_highpriest(R):
    """High Conductor: white-and-copper vestments, crown of spark rods, tesla-coil staff."""
    P = R.P

    def vest(t):
        t.add(box((0, 1.0, 0.0), (0.155, 0.032, 0.108), rnd=0.02), GOLD)
        t.add(box((0, 0.7, 0.135), (0.04, 0.32, 0.01), rnd=0.006), GOLD)                  # stole
        t.add(shell(ellipsoid((0, 1.4, 0.0), (0.2, 0.09, 0.14)), 0.008, 1.36, 1.38), GOLD) # mantle edge
        t.add(box((0, 1.3, 0.12), (0.03, 0.05, 0.01), rnd=0.005), G_SPARK)                # sigil
    robe_body(R, SUIT, SUIT, skirt_to=0.1, extra=vest)
    h = Group("head")
    face(h, SKIN)
    h.add(ellipsoid((0, 1.54, 0.06), (0.05, 0.06, 0.04)), HAIR_RG)                        # long white beard
    h.add(torus((0, 1.67, 0.005), (0, 1, 0), 0.08, 0.012), COPPER)                        # crown band
    for k in range(5):                                                                    # spark rods
        a = math.pi * (0.15 + 0.7 * k / 4)
        p = (0.08 * cos(a), 1.67, 0.08 * sin(a))
        q = add(p, (0.03 * cos(a), 0.09, 0.03 * sin(a)))
        h.add(capsule(p, q, 0.007), COPPER)
        h.add(sphere(q, 0.014), G_SPARK)
    R.head(h)
    arm(R, -1, P["hand_r"], SUIT, SUIT, SKIN)
    arm(R, 1, P["hand_l"], SUIT, SUIT, SKIN)
    g = Group("staff")
    d, hr = norm(P["staff"]), P["hand_r"]
    lo, top = add(hr, mul(d, -P.get("below", 0.95))), add(hr, mul(d, 0.5))
    g.add(capsule(lo, top, 0.016), COPPER)
    g.add(grooves(capsule(add(top, mul(d, -0.2)), top, 0.03), top, d, 0.025, 0.009), COPPER)  # coil
    tor = add(top, mul(d, 0.06))
    g.add(torus(tor, d, 0.08, 0.03), STEEL)                                              # toroid
    g.add(sphere(add(tor, mul(d, 0.05)), 0.03), G_SPARK)
    if P.get("cast"):
        for k, v in enumerate((aim(100), aim(45), aim(150, 0.2), aim(15, -0.2))):
            lightning(g, add(tor, mul(v, 0.08)), add(tor, mul(v, 0.4)), seed=k + 41, r=0.009, kinks=4, amp=0.06,
                      branches=0)
    else:
        for k, v in enumerate((aim(60), aim(140))):
            bolt(g, add(tor, mul(v, 0.08)), add(tor, mul(v, 0.18)), G_SPARK, 0.008, 3, 0.02, seed=k + 45)
    R.world(g)


def b_tesla(R):
    """The inventor hero: tall and lean, dark three-piece suit, centre-parted hair, moustache,
    a bulb lit in his hand and lightning at his fingertips."""
    P = R.P

    def suit(t):
        t.add(box((0, 1.37, 0.098), (0.034, 0.07, 0.008), rnd=0.005), SUIT)               # shirt front
        t.add(box((0, 1.42, 0.1), (0.03, 0.01, 0.01), rnd=0.004), BOOT)                   # bow tie
        t.add(box((0, 1.2, 0.09), (0.07, 0.12, 0.012), rnd=0.008), FCOAT)                 # waistcoat
        for s in (1, -1):
            t.add(box((0.065 * s, 1.34, 0.105), (0.022, 0.08, 0.007),
                      (norm((1, 0, 0)), norm((0.35 * s, 1, 0)), (0, 0, 1)), rnd=0.004), MDARK)  # lapels
    robe_body(R, MDARK, MDARK, skirt_to=0.72, legs_mat=FCOAT, extra=suit)
    h = Group("head")
    h.add(capsule((0, 1.46, -0.005), (0, 1.54, 0.005), 0.036), SKIN)
    h.add(ellipsoid((0, 1.605, 0.012), (0.064, 0.098, 0.08)), SKIN)                       # long lean face
    h.add(ellipsoid((0, 1.59, 0.09), (0.012, 0.02, 0.017)), SKIN)
    h.add(ellipsoid((0, 1.56, 0.078), (0.032, 0.009, 0.012)), HAIR_BK)                    # moustache
    for s in (1, -1):                                                                     # centre-parted, slicked
        h.add(ellipsoid((0.036 * s, 1.67, 0.0), (0.05, 0.04, 0.088)), HAIR_BK)
    h.add(ellipsoid((0, 1.62, -0.05), (0.068, 0.075, 0.05)), HAIR_BK)
    R.head(h)
    arm(R, -1, P["hand_r"], MDARK, MDARK, SKIN, at=0.9)
    arm(R, 1, P["hand_l"], MDARK, MDARK, SKIN, at=0.9)
    g = Group("bulb")
    hl = P["hand_l"]
    g.add(capsule(add(hl, (0, 0.02, 0)), add(hl, (0, 0.05, 0)), 0.016), BRASS)            # bulb base
    g.add(sphere(add(hl, (0, 0.1, 0)), 0.052), G_FLASH)
    hr = P["hand_r"]
    if P.get("cast"):
        lightning(g, add(hr, mul(SL, 0.04)), add(hr, add(mul(aim(P.get("bolt", -8)), 0.8), (0, 0, 0))),
                  seed=51, r=0.01, kinks=5, amp=0.1, branches=1)
    else:
        bolt(g, add(hr, (0, -0.03, 0)), add(hr, (0.03, -0.12, 0.04)), G_SPARK, 0.007, 3, 0.02, seed=55)
    R.world(g)


UNITS.update({
    # hands low with sparks / both arms thrust out, forked lightning  (shambhala ngagspa)
    "arcadept": dict(build=b_arcadept, poses={
        "1": dict(feet=FEET(0.06, -0.06, -0.04, 0.05), hand_r=W(0.24, 1.08, 0.12), hand_l=W(-0.02, 1.02, 0.18)),
        "2": dict(feet=FEET(0.12, -0.1, -0.02, 0.05), lean=5, twist=-10, hand_r=W(0.52, 1.32, 0.08),
                  hand_l=W(0.38, 1.26, 0.2), pole_l=(1, -0.6, 0.1), cast=True, bolt=(10, -14), halo=True)}),
    # hovering, arm raised crackling / both arms up-forward throwing lightning  (juhera hero_dajjal)
    "arcmage": dict(build=b_arcmage, scale=1.05, poses={
        "1": dict(body=(0, 0.32, 0), feet=(W(0.06, 0.42, -0.12), W(-0.12, 0.36, 0.0)), lean=6,
                  hand_r=W(0.3, 1.62, 0.02), hand_l=W(-0.24, 1.15, 0.12), pole_r=(-1, -0.4, -0.3)),
        "2": dict(body=(0, 0.38, 0.02), feet=(W(-0.02, 0.5, -0.12), W(-0.2, 0.42, 0.0)), lean=12, twist=-10,
                  nod=-8, hand_r=W(0.55, 1.75, 0.04), hand_l=W(0.42, 1.62, 0.18), pole_l=(1, -0.4, 0.1),
                  cast=True, bolt=(42, 8), halo=True)}),
    # tesla rifle held low / aimed, lightning stream                 (nihuala un_bowturquoise)
    "teslatrooper": dict(build=b_teslatrooper, scale=1.15, shadow=(20, 44), poses={
        "1": dict(feet=FEET(0.12, -0.12, 0.0, 0.05), grip=W(0.1, 1.0, 0.24), gun=aim(-30, 0.2)),
        "2": dict(feet=FEET(0.22, -0.18, 0.0, 0.04), body=(0, -0.04, 0), lean=5, twist=-15,
                  grip=W(0.22, 1.32, 0.08), gun=aim(2), fire=True, halo=True)}),
    # humming / throwing lightning                                   (structure, no stance)
    "teslapylon": dict(build=b_teslapylon, res=128, scale=1.15, shadow=(44, 84), poses={
        "1": dict(), "2": dict(fire=True, halo=True)}),
    # staff planted / staff raised and arcing                        (gondwana priest)
    "highpriest": dict(build=b_highpriest, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.24, 1.1, 0.1), staff=aim(84),
                  hand_l=W(-0.06, 1.12, 0.18), halo=True),
        "2": dict(feet=FEET(0.08, -0.07, -0.04, 0.05), hand_r=W(0.3, 1.62, 0.08), staff=aim(66), below=0.7,
                  hand_l=W(-0.1, 1.28, 0.18), cast=True, halo=True)}),
    # bulb held up, sparks at the fingers / arm out, lightning        (juhera hero_alhazen)
    "tesla": dict(build=b_tesla, scale=1.08, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.15, 0.92, 0.05),
                  hand_l=W(0.02, 1.22, 0.2), pole_l=(1, -0.8, 0.1)),
        "2": dict(feet=FEET(0.08, -0.07, -0.04, 0.05), hand_r=W(0.5, 1.2, 0.08), hand_l=W(0.02, 1.22, 0.2),
                  pole_l=(1, -0.8, 0.1), cast=True, bolt=-10, halo=True)}),
})

# ================================================================ lab, clones, beasts, vehicles, flag
QF = norm(add(SL, mul(OUT, 0.3)))        # beasts and vehicles face screen-left, turned a little to the viewer
QS = norm(cross((0, 1, 0), QF))          # their side toward the viewer


def Q(f, y, s=0.0):
    """Point f metres ahead along a beast's or vehicle's heading, at height y, s toward the viewer."""
    return add(add(mul(QF, f), (0, y, 0)), mul(QS, s))


def oe(c, r, d, up=(0, 1, 0)):
    """Ellipsoid with radii (side, up, along) whose long axis follows d."""
    d = norm(d)
    n1, n2 = perp(d, up)
    return oriented_ellipsoid(c, r, (n1, n2, d))


def q_basis():
    return (QS, (0, 1, 0), QF)


def b_labassistant(R):
    """Hunchbacked lab assistant: patched brown smock, stained apron, one magnifying lens,
    a lantern and a brain in a glowing jar."""
    P = R.P
    legs(R, TROUS, TROUS, BOOT, boot_top=0.2)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), RAG)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), RAG)
    t.add(ellipsoid((0, 1.31, 0), (0.16, 0.12, 0.106)), RAG)
    t.add(capsule((-0.16, 1.4, -0.005), (0.16, 1.4, -0.005), 0.056), RAG)
    t.add(lumpy(ellipsoid((0.05, 1.37, -0.1), (0.14, 0.13, 0.11)), 0.007, 40), RAG)      # hump
    t.add(cone_skirt((0, 1.05, 0), (0, 0.74, -0.01), 0.15, 0.19, -0.15, 0.14), RAG)     # smock
    t.add(box((0, 1.0, 0), (0.15, 0.022, 0.104), rnd=0.02), BELT)                       # rope belt
    t.add(box((0, 1.05, 0.12), (0.075, 0.2, 0.01), rnd=0.008), HOSP)                    # stained apron
    R.body(t)
    h = Group("head")
    face(h, SKIN)
    for prim in (ellipsoid((0, 1.62, -0.04), (0.075, 0.07, 0.06)),                      # lank hair, bald crown
                 roundcone((0.05, 1.62, -0.04), (0.07, 1.5, -0.03), 0.03, 0.02),
                 roundcone((-0.05, 1.62, -0.04), (-0.07, 1.5, -0.03), 0.03, 0.02)):
        h.add(lumpy(prim, 0.01, 60), HAIR_BK)
    h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.006, 0.006, 0.006))), 0.005, 1.6, 1.622), BOOT)
    h.add(disc((0.034, 1.612, 0.09), (0.0, 0.2, 1.0), 0.032, 0.03), BRASS)              # magnifier
    h.add(disc((0.034, 1.614, 0.104), (0.0, 0.2, 1.0), 0.022, 0.008), LENS)
    R.head(h)
    arm(R, -1, P["hand_r"], RAG, RAG, SKIN)
    arm(R, 1, P["hand_l"], RAG, RAG, SKIN)
    g = Group("lantern")
    lh = P["hand_l"]
    c = add(lh, (0, -0.13, 0))
    g.add(capsule(lh, add(c, (0, 0.08, 0)), 0.008), BRASS)                               # bail
    g.add(roundcone(add(c, (0, 0.07, 0)), add(c, (0, 0.11, 0)), 0.056, 0.016), BRASS)    # cap
    g.add(disc(add(c, (0, -0.07, 0)), (0, 1, 0), 0.058, 0.016), BRASS)                   # base
    g.add(sphere(c, 0.05), G_FIRE)
    for k in range(4):
        a = TAU * (k + 0.5) / 4
        g.add(capsule(add(c, (0.056 * cos(a), -0.07, 0.056 * sin(a))), add(c, (0.056 * cos(a), 0.07, 0.056 * sin(a))),
                      0.008), BRASS)
    R.world(g)
    j = Group("jar")
    hr = P["hand_r"]
    jc = add(hr, (0, 0.07, 0))
    j.add(capsule(add(jc, (0, -0.04, 0)), add(jc, (0, 0.04, 0)), 0.05), G_GREEN)         # preserving fluid
    j.add(lumpy(ellipsoid(add(jc, mul(OUT, 0.03)), (0.04, 0.032, 0.036)), 0.006, 90), FLESH)  # the brain
    j.add(disc(add(jc, (0, 0.095, 0)), (0, 1, 0), 0.052, 0.018), BRASS)                   # lid
    j.add(disc(add(jc, (0, -0.09, 0)), (0, 1, 0), 0.052, 0.014), BRASS)
    if P.get("cast"):
        for k, v in enumerate((aim(70), aim(120, 0.3), aim(20), aim(160))):
            bolt(j, add(jc, mul(v, 0.06)), add(jc, mul(v, 0.17)), G_SPARK, 0.008, 3, 0.025, seed=k + 61)
    R.world(j)


def b_alphaclone(R):
    """Alpha clone: the same vat face in clone armour, officer's cap, red sash and gold epaulettes, sidearm."""
    P = R.P
    clone_base(R, armour=True)
    t = Group("insignia")
    t.add(box((0, 1.24, 0.122), (0.03, 0.19, 0.012),
              (norm((0.82, 0.57, 0)), norm((-0.57, 0.82, 0)), (0, 0, 1)), rnd=0.006), CRED)  # sash
    for s in (1, -1):
        t.add(ellipsoid((0.2 * s, 1.47, 0.0), (0.075, 0.022, 0.075)), GOLD)                    # epaulettes
    R.body(t)
    h = Group("cap")
    h.add(ellipsoid((0.0, 1.69, -0.005), (0.088, 0.032, 0.095)), MECHD)                         # crown
    h.add(box((0, 1.665, 0.0), (0.074, 0.02, 0.082), rnd=0.02), CRED)                           # band
    h.add(box((0, 1.652, 0.085), (0.058, 0.006, 0.03),
              (norm((1, 0, 0)), norm((0, 1, -0.4)), norm((0, 0.4, 1))), rnd=0.004), BOOT)        # peak
    h.add(sphere((0, 1.674, 0.095), 0.013), GOLD)
    R.head(h)
    arm(R, -1, P["hand_r"], CLONE, CLONE, BOOT)
    arm(R, 1, P["hand_l"], CLONE, CLONE, BOOT)
    g = Group("sidearm")
    muzzle = pistol(g, P["hand_l"], P["gun"])
    if P.get("fire"):
        flash(g, muzzle, P["gun"], 0.7)
    R.world(g)


# ---------------------------------------------------------------- beasts
def qframe(P, k):
    """Body-frame points for a beast: f forward, y up, s toward the viewer (metres at k=1),
    pitched by P['pitch'] degrees about its centre P['c'] = (f, y)."""
    a = math.radians(P.get("pitch", 0))
    cf, cy = P.get("c", (0.0, 0.6))

    def B(f, y, s=0.0):
        return Q(k * (cf + f * cos(a) - y * sin(a)), k * (cy + f * sin(a) + y * cos(a)), k * s)
    return B


def qleg(g, k, top, foot, front, thick, fur, paw):
    """Beast leg from shoulder/hip to paw: front legs bend the elbow back, hind legs bend the
    knee forward with the hock behind it."""
    if front:
        wrist = add(foot, (0, 0.09 * k, 0))
        elbow, wrist = ik(top, wrist, 0.27 * k, 0.24 * k, mul(QF, -1))
    else:
        wrist = add(add(foot, mul(QF, -0.07 * k)), (0, 0.17 * k, 0))                    # hock
        elbow, wrist = ik(top, wrist, 0.27 * k, 0.24 * k, QF)
    g.add(limb(top, elbow, thick * 1.3 * k, thick * 0.85 * k), fur)
    g.add(limb(elbow, wrist, thick * 0.8 * k, thick * 0.6 * k), fur)
    g.add(limb(wrist, foot, thick * 0.6 * k, thick * 0.55 * k), fur)
    g.add(oe(add(foot, mul(QF, 0.025 * k)), (0.035 * k, 0.025 * k, 0.05 * k), QF), paw)


def qhead(g, H, hd, k, mat, jaw=10, jawmat=None, snout=0.2, w=0.07, eye=G_RED, nose=BOOT, ears=True):
    """Muzzled head at H looking along hd; jaw opens by `jaw` degrees."""
    hd = norm(hd)
    hup = norm(sub((0, 1, 0), mul(hd, hd[1])))
    j = math.radians(jaw)
    jd = norm(add(mul(hd, cos(j)), mul(hup, -sin(j))))
    g.add(oe(H, (w * k, w * k, w * 1.2 * k), hd), mat)
    tip = add(H, add(mul(hd, snout * k), mul(hup, -0.1 * w * k)))
    g.add(roundcone(add(H, mul(hd, 0.4 * w * k)), tip, 0.7 * w * k, 0.45 * w * k), mat)
    g.add(sphere(add(tip, mul(hd, 0.35 * w * k)), 0.24 * w * k), nose)
    j0 = add(H, add(mul(hd, 0.2 * w * k), mul(hup, -0.5 * w * k)))
    g.add(roundcone(j0, add(j0, mul(jd, (snout - 0.1 * w) * k)), 0.5 * w * k, 0.32 * w * k), jawmat or mat)
    if jaw > 15:
        g.add(sphere(add(j0, add(mul(hd, 0.5 * snout * k), mul(hup, 0.05 * w * k))), 0.4 * w * k), BLOOD)
    g.add(sphere(add(H, add(add(mul(hd, 0.5 * w * k), mul(hup, 0.4 * w * k)), mul(QS, 0.75 * w * k))),
                 0.22 * w * k), eye)
    if ears:
        for s in (1, -1):
            e0 = add(H, add(add(mul(hup, 0.7 * w * k), mul(hd, -0.2 * w * k)), mul(QS, 0.55 * w * k * s)))
            g.add(roundcone(e0, add(e0, add(mul(hup, 0.9 * w * k), mul(hd, -0.5 * w * k))),
                            0.35 * w * k, 0.08 * w * k), mat)
    return hup, jd, j0


def look(elev):
    e = math.radians(elev)
    return norm(add(mul(QF, cos(e)), (0, sin(e), 0)))


def chain(g, pts, r0, r1, mat):
    n = len(pts) - 1
    for i, (p, q) in enumerate(zip(pts, pts[1:])):
        g.add(limb(p, q, r0 + (r1 - r0) * i / n, r0 + (r1 - r0) * (i + 1) / n), mat)


def beast(R, k, fur, paw, bulk=1.0):
    """Shared quadruped body: chest, waist, haunches, four legs. Returns the frame and its axes."""
    P = R.P
    B = qframe(P, k)
    ax, up = norm(sub(B(1, 0), B(0, 0))), norm(sub(B(0, 1), B(0, 0)))
    b = bulk
    g = Group("body")
    g.add(oe(B(0.2, 0.02), (0.13 * b * k, 0.17 * b * k, 0.24 * k), ax, up), fur)            # chest
    g.add(oe(B(-0.03, 0.04), (0.1 * b * k, 0.12 * b * k, 0.2 * k), ax, up), fur)            # waist
    g.add(oe(B(-0.27, 0.02), (0.115 * b * k, 0.14 * b * k, 0.17 * k), ax, up), fur)         # haunches
    R.world(g)
    lg = Group("legs")
    feet = [Q(k * f, k * y, k * s) for f, y, s in P["feet"]]
    tops = (B(0.28, -0.06, 0.085), B(0.28, -0.06, -0.085), B(-0.3, -0.02, 0.08), B(-0.3, -0.02, -0.08))
    for i in range(4):
        qleg(lg, k, tops[i], feet[i], i < 2, 0.05 * b, fur, paw)
    R.world(lg)
    return B, ax, up


def b_genehound(R):
    """Gene-spliced attack hound: mangy hide, steel cyber-jaw, red optic, green vials along the spine."""
    P = R.P
    k = 1.0
    B, ax, up = beast(R, k, FUR, BOOT, bulk=1.45)
    g = Group("head")
    H, hd = B(*P["hp"]), look(P["look"])
    g.add(limb(B(0.3, 0.1), H, 0.11, 0.08), FUR)                                           # bull neck
    g.add(torus(lerp(B(0.3, 0.1), H, 0.45), sub(H, B(0.3, 0.1)), 0.095, 0.018), COPPER)    # collar
    qhead(g, H, hd, k, FUR, jaw=P["jaw"], jawmat=MECH, snout=0.2, w=0.08)
    R.world(g)
    s = Group("spine")
    for f in (-0.22, 0.0):
        a, b_ = B(f, 0.2), B(f + 0.16, 0.22)
        s.add(capsule(a, b_, 0.026), G_GREEN)
        for p in (a, b_):
            s.add(disc(p, sub(b_, a), 0.034, 0.016), COPPER)
    s.add(oe(B(-0.3, 0.06, 0.15), (0.02, 0.06, 0.07), ax, up), FLESH)                      # stitched patch
    cable(s, [B(0.16, 0.22), B(0.3, 0.24), lerp(B(0.3, 0.1), H, 0.6)], 0.013, BOOT)
    chain(s, [B(*p) for p in P["tail"]], 0.035, 0.014, FUR)
    R.world(s)


def b_chimera(R):
    """Vat-made chimera: lion body and roaring head, a goat head grafted onto the back behind a steel
    collar, a serpent for a tail, green vat tubes along the spine."""
    P = R.P
    k = 1.7
    B, ax, up = beast(R, k, LION, LION, bulk=1.5)
    g = Group("lion")
    H, hd = B(*P["hp"]), look(P["look"])
    g.add(limb(B(0.3, 0.08), H, 0.09 * k, 0.07 * k), LION)
    g.add(lumpy(oe(lerp(B(0.3, 0.1), H, 0.6), (0.13 * k, 0.15 * k, 0.15 * k), sub(H, B(0.3, 0.1))),
                0.012, 30), MANE)                                                         # mane
    g.add(lumpy(oe(add(H, mul(hd, -0.05 * k)), (0.12 * k, 0.13 * k, 0.07 * k), hd), 0.01, 30), MANE)
    qhead(g, H, hd, k, LION, jaw=P["jaw"], snout=0.16, w=0.075, eye=G_FIRE)
    R.world(g)
    gt = Group("goat")
    base, G, gd = B(0.0, 0.16), B(*P["gp"]), look(P["glook"])
    gt.add(limb(base, G, 0.07 * k, 0.055 * k), HAIR_GR)
    gt.add(torus(lerp(base, G, 0.15), sub(G, base), 0.075 * k, 0.018 * k), MECH)             # graft collar
    gh = qhead(gt, G, gd, k, HAIR_GR, jaw=P["gjaw"], snout=0.16, w=0.068, eye=G_GREEN, nose=BOOT)
    hup = gh[0]
    for s in (1, -1):                                                                        # swept horns
        o = add(G, add(mul(hup, 0.04 * k), mul(QS, 0.025 * k * s)))
        chain(gt, [o, add(o, add(mul(gd, -0.05 * k), mul(hup, 0.08 * k))),
                   add(o, add(mul(gd, -0.13 * k), mul(hup, 0.08 * k))),
                   add(o, add(mul(gd, -0.17 * k), mul(hup, 0.01 * k)))], 0.024 * k, 0.009 * k, BONE)
    gt.add(roundcone(add(gh[2], mul(gd, 0.05 * k)), add(gh[2], add(mul(gd, 0.04 * k), (0, -0.07 * k, 0))),
                     0.016 * k, 0.006 * k), HAIR_GR)                                         # beard
    if P.get("gas"):
        mouth = add(G, mul(gd, 0.17 * k))
        for i in range(5):
            gt.add(lumpy(sphere(add(mouth, add(mul(gd, (0.06 + 0.1 * i) * k), (0, -0.02 * i * k, 0))),
                                (0.025 + 0.018 * i) * k), 0.008 * k, 40), G_GREEN)
    R.world(gt)
    sp = Group("tail")
    pts = [B(*p) for p in P["tail"]]
    chain(sp, pts, 0.05 * k, 0.03 * k, GGREEN)
    qhead(sp, add(pts[-1], mul(look(P["slook"]), 0.04 * k)), look(P["slook"]), k, GGREEN, jaw=P["sjaw"],
          snout=0.08, w=0.04, eye=G_RED, nose=GGREEN, ears=False)
    for f in (-0.24, -0.02):                                                                 # vat tubes
        a, b_ = B(f, 0.18), B(f + 0.17, 0.2)
        sp.add(capsule(a, b_, 0.028 * k), G_GREEN)
        for p in (a, b_):
            sp.add(disc(p, sub(b_, a), 0.036 * k, 0.014 * k), COPPER)
    cable(sp, [B(0.15, 0.2), lerp(base, G, 0.3)], 0.012 * k, BOOT)
    R.world(sp)


# ---------------------------------------------------------------- vehicles
def wheel(g, c, r, tire=BOOT, hub=MECHD, glow=G_SPARK):
    g.add(torus(c, QS, r - 0.06, 0.06), tire)
    g.add(disc(c, QS, r - 0.09, 0.07), hub)
    g.add(torus(add(c, mul(QS, 0.04)), QS, (r - 0.1) * 0.62, 0.014), glow)                   # coil ring
    g.add(disc(add(c, mul(QS, 0.02)), QS, 0.055, 0.1), COPPER)


def b_motorcycle(R):
    """Electro-punk motorcycle: coil engine, glowing wheel rings, twin tesla coils behind the seat;
    goggled rider in a leather jacket and red scarf with a tesla pistol."""
    P = R.P
    bas = q_basis()
    m = Group("bike")
    for c in (Q(-0.62, 0.32), Q(0.72, 0.32)):
        wheel(m, c, 0.32)
    for s in (1, -1):
        m.add(capsule(Q(-0.62, 0.32, 0.08 * s), Q(-0.1, 0.5, 0.08 * s), 0.028), MECHD)      # swingarm
        m.add(capsule(Q(0.72, 0.32, 0.07 * s), Q(0.5, 0.96, 0.07 * s), 0.024), STEEL)       # fork
    m.add(grooves(capsule(Q(-0.14, 0.42), Q(0.24, 0.42), 0.13), Q(0, 0.42), QF, 0.04, 0.012), COPPER)  # coil engine
    m.add(capsule(Q(0.02, 0.36, 0.15), Q(0.2, 0.36, 0.15), 0.03), G_SPARK)                 # capacitor
    m.add(oe(Q(0.26, 0.7), (0.12, 0.08, 0.22), QF), MECH)                                   # tank
    m.add(shell(oe(Q(0.26, 0.7), (0.12, 0.08, 0.22), QF), 0.006, 0.69, 0.72), COPPER)
    m.add(oe(Q(-0.2, 0.68), (0.12, 0.045, 0.2), QF), BELT)                                  # seat
    m.add(box(Q(-0.58, 0.66), (0.1, 0.03, 0.2), bas, rnd=0.02), MECH)                       # rear fender
    m.add(box(Q(0.74, 0.62), (0.08, 0.025, 0.18), bas, rnd=0.02), MECH)                     # front fender
    m.add(capsule(Q(0.5, 0.98, -0.26), Q(0.5, 0.98, 0.26), 0.018), MECHD)                   # handlebar
    m.add(sphere(Q(0.62, 0.86), 0.06), G_CYAN)                                              # headlamp
    for s in (1, -1):                                                                       # twin coils
        b0 = Q(-0.5, 0.68, 0.1 * s)
        m.add(grooves(capsule(b0, add(b0, (0, 0.28, 0)), 0.035), b0, (0, 1, 0), 0.025, 0.008), COPPER)
        m.add(sphere(add(b0, (0, 0.33, 0)), 0.04), G_SPARK)
    cable(m, [Q(-0.14, 0.45, 0.1), Q(-0.3, 0.6, 0.14), Q(-0.5, 0.7, 0.1)], 0.012, BOOT)
    bolt(m, Q(-0.5, 1.01, 0.1), Q(-0.5, 1.01, -0.1), G_SPARK, 0.008, 3, 0.02, seed=71)
    R.world(m)
    legs(R, TROUS, TROUS, BOOT, boot_top=0.4)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), TROUS)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), BELT)
    t.add(ellipsoid((0, 1.31, 0), (0.162, 0.12, 0.106)), BELT)
    t.add(capsule((-0.165, 1.41, -0.005), (0.165, 1.41, -0.005), 0.056), BELT)
    t.add(box((0, 0.99, 0), (0.15, 0.024, 0.104), rnd=0.02), BOOT)
    t.add(torus((0, 1.46, 0.0), (0, 1, 0), 0.07, 0.03), CRED)                               # scarf
    chain(t, [(0.03, 1.45, -0.07), (0.07, 1.4, -0.22), (0.05, 1.42, -0.36)], 0.03, 0.018, CRED)
    R.body(t)
    h = Group("head")
    face(h, SKIN)
    h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.012, 0.012, 0.012))), 0.016, 1.6, 1.75), BELT)  # leather cap
    goggles(h, y=1.645)
    R.head(h)
    arm(R, -1, P["hand_r"], BELT, BELT, BOOT)
    arm(R, 1, P["hand_l"], BELT, BELT, BOOT)
    if P.get("gun"):
        g = Group("pistol")
        muzzle = pistol(g, P["hand_l"], P["gun"], body=MECHD, grip=COPPER)
        if P.get("fire"):
            lightning(g, muzzle, add(muzzle, mul(P["gun"], 0.8)), seed=73, r=0.01, kinks=5, amp=0.09, branches=1)
        R.world(g)


def b_truck(R):
    """Electro-punk war truck: armoured cab with a copper coil ram, capacitor bank and a great
    tesla coil on the bed that throws lightning."""
    P = R.P
    bas = q_basis()
    w = Group("wheels")
    for f in (1.45, -1.0, -1.75):
        for s in (0.8, -0.8):
            wheel(w, Q(f, 0.48, s), 0.48)
    R.world(w)
    c = Group("hull")
    c.add(box(Q(0, 0.72), (0.74, 0.16, 2.1), bas, rnd=0.03), MECHD)                        # chassis
    c.add(box(Q(1.4, 1.35), (0.76, 0.48, 0.58), bas, rnd=0.06), MECH)                      # cab
    c.add(box(Q(2.0, 1.02), (0.72, 0.24, 0.34), bas, rnd=0.05), MECH)                      # armoured hood
    c.add(box(Q(1.98, 1.55), (0.6, 0.07, 0.03), bas, rnd=0.01), VISOR)                     # vision slit
    c.add(box(Q(1.45, 1.55, 0.77), (0.01, 0.08, 0.3), bas, rnd=0.01), VISOR)               # side slit
    c.add(box(Q(0.6, 0.95, 0.75), (0.02, 0.04, 1.5), bas, rnd=0.01), COPPER)               # trim stripe
    c.add(grooves(capsule(Q(2.38, 0.78, -0.62), Q(2.38, 0.78, 0.62), 0.17), Q(2.38, 0.78), QS, 0.07, 0.02),
          COPPER)                                                                          # coil ram
    c.add(box(Q(-0.95, 1.0), (0.76, 0.2, 1.2), bas, rnd=0.03), MECHD)                      # bed
    c.add(box(Q(-0.95, 1.2, 0.74), (0.03, 0.04, 1.2), bas, rnd=0.01), COPPER)              # bed rail
    for s in (0.55, -0.55):                                                                # exhaust stacks
        c.add(capsule(Q(0.72, 1.1, s), Q(0.72, 2.2, s), 0.06), STEEL)
        c.add(sphere(Q(0.72, 2.26, s), 0.06), G_SPARK)
    R.world(c)
    t = Group("coil")
    t.add(box(Q(-1.15, 1.3), (0.4, 0.1, 0.4), bas, rnd=0.03), MECH)
    t.add(grooves(capsule(Q(-1.15, 1.35), Q(-1.15, 2.55), 0.18), Q(-1.15, 0), (0, 1, 0), 0.06, 0.02), COPPER)
    top = Q(-1.15, 2.75)
    t.add(torus(top, (0, 1, 0), 0.4, 0.13), STEEL)
    t.add(sphere(add(top, (0, 0.08, 0)), 0.1), G_SPARK)
    for f in (-0.35, -1.95):                                                               # capacitor bank
        for s in (0.45, -0.45):
            p = Q(f, 1.2, s)
            t.add(capsule(p, add(p, (0, 0.42, 0)), 0.09), G_SPARK)
            t.add(disc(add(p, (0, 0.47, 0)), (0, 1, 0), 0.11, 0.05), COPPER)
            t.add(disc(add(p, (0, -0.03, 0)), (0, 1, 0), 0.11, 0.05), COPPER)
    cable(t, [Q(-0.35, 1.67, 0.45), Q(-0.7, 1.85, 0.3), Q(-1.0, 1.7, 0.15)], 0.03, BOOT)
    cable(t, [Q(-1.95, 1.67, 0.45), Q(-1.6, 1.85, 0.3), Q(-1.3, 1.7, 0.15)], 0.03, BOOT)
    R.world(t)
    z = Group("lightning")
    rim = lambda a: add(top, mul(add(mul(QF, cos(a)), mul(QS, sin(a))), 0.55))
    if P.get("fire"):
        for i, (a, tgt) in enumerate(((0.3, Q(3.6, 0.1, 0.3)), (0.6, Q(3.2, 1.8, 0.4)), (2.6, Q(-2.8, 3.5, 0)))):
            lightning(z, rim(a), tgt, seed=81 + i, r=0.03 if i < 2 else 0.02, kinks=6, amp=0.22,
                      branches=2 if i < 2 else 1)
    else:
        for i, a in enumerate((0.4, 2.5, -1.4)):
            p = rim(a)
            bolt(z, p, add(p, add(mul(sub(p, top), 0.6), (0, 0.18, 0))), G_SPARK, 0.018, 3, 0.06, seed=91 + i)
    R.world(z)


# ---------------------------------------------------------------- flag
def b_flag(R):
    """Nation banner: indigo swallowtail with copper border, a brass gear struck by a lightning bolt,
    a small tesla coil topping the pole."""
    g = Group("pole")
    g.add(capsule((0, 0, 0), (0, 5.0, 0), 0.075), WOOD)
    g.add(capsule((-1.85, 4.7, 0.05), (1.85, 4.7, 0.05), 0.07), WOOD)
    for x in (-1.9, 1.9):
        g.add(sphere((x, 4.7, 0.05), 0.11), BRASS)
    g.add(grooves(capsule((0, 4.95, 0), (0, 5.45, 0), 0.09), (0, 0, 0), (0, 1, 0), 0.06, 0.02), COPPER)
    g.add(torus((0, 5.55, 0), (0, 1, 0), 0.24, 0.08), STEEL)
    g.add(sphere((0, 5.68, 0), 0.13), G_SPARK)
    for i, v in enumerate(((0.8, 0.5, 0), (-0.8, 0.6, 0), (0.3, 1, 0))):
        bolt(g, add((0, 5.68, 0), mul(norm(v), 0.13)), add((0, 5.68, 0), mul(norm(v), 0.42)), G_SPARK, 0.035, 3,
             0.06, seed=101 + i)
    R.world(g)
    notch = lambda h: box((0, 1.4, 0.1), (h, h, 0.3), ((0.7071, 0.7071, 0), (-0.7071, 0.7071, 0), (0, 0, 1)))
    b = Group("border")
    b.add(box((0, 3.05, 0.1), (1.72, 1.6, 0.025), rnd=0.02), COPPER)
    b.cut(notch(0.75))
    R.world(b)
    c = Group("cloth")
    c.add(grooves(box((0, 3.1, 0.125), (1.5, 1.42, 0.025), rnd=0.02), (0, 0, 0), (1, 0, 0), 0.6, 0.008), NAVY)
    c.cut(notch(0.97))
    R.world(c)
    e = Group("emblem")
    gc = (0, 3.25, 0.16)
    e.add(torus(gc, (0, 0, 1), 0.6, 0.11), BRASS)
    for i in range(10):
        a = TAU * i / 10
        e.add(box(add(gc, (0.76 * cos(a), 0.76 * sin(a), 0)), (0.1, 0.1, 0.05),
                  ((cos(a), sin(a), 0), (-sin(a), cos(a), 0), (0, 0, 1)), rnd=0.02), BRASS)
    pts = [(0.5, 4.3), (-0.08, 3.38), (0.3, 3.32), (-0.45, 2.15)]
    for p, q in zip(pts, pts[1:]):
        e.add(capsule((p[0], p[1], 0.3), (q[0], q[1], 0.3), 0.11), G_SPARK)
    R.world(e)


UNITS.update({
    # hunched, lantern low and jar hugged / jar held up crackling   (cyborg hunch; magicenhanced humanslave)
    "labassistant": dict(build=b_labassistant, poses={
        "1": dict(feet=FEET(0.12, -0.1, -0.04, 0.05), lean=30, nod=-26, hand_r=W(0.18, 1.08, 0.24),
                  hand_l=W(0.3, 0.98, 0.12), pole_r=(-1, -0.6, 0.4)),
        "2": dict(feet=FEET(0.14, -0.1, -0.04, 0.05), lean=24, nod=-14, hand_r=W(0.3, 1.58, 0.16),
                  hand_l=W(0.32, 1.0, 0.1), pole_r=(-1, -0.3, 0.2), cast=True, halo=True)}),
    # pistol held low and ready, other hand behind / arm out firing   (greatarrada officer)
    "alphaclone": dict(build=b_alphaclone, poses={
        "1": dict(feet=FEET(0.06, -0.06), hand_l=W(0.3, 1.04, 0.2), gun=aim(-38), pole_l=(1, -0.6, 0.3),
                  hand_r=W(-0.12, 1.0, -0.12), pole_r=(-1, -0.6, -0.4)),
        "2": dict(feet=FEET(0.14, -0.1, -0.02, 0.05), twist=-12, hand_l=W(0.5, 1.38, 0.12), gun=aim(2),
                  hand_r=W(-0.1, 1.0, -0.1), pole_r=(-1, -0.6, -0.4), fire=True, halo=True)}),
    # standing, head low snarling / lunging, jaw wide               (magicenhanced eehellhound)
    "genehound": dict(build=b_genehound, scale=1.3, shadow=(16, 48), poses={
        "1": dict(c=(0.0, 0.56), feet=[(0.32, 0.03, 0.12), (0.22, 0.03, -0.1), (-0.28, 0.03, 0.11),
                                       (-0.38, 0.03, -0.1)],
                  hp=(0.54, 0.06), look=-18, jaw=18, tail=[(-0.42, 0.06), (-0.56, 0.12), (-0.66, 0.08)]),
        "2": dict(c=(0.06, 0.6), pitch=9, feet=[(0.66, 0.2, 0.1), (0.52, 0.03, -0.08), (-0.4, 0.03, 0.09),
                                                (-0.3, 0.03, -0.08)],
                  hp=(0.56, 0.14), look=4, jaw=40, tail=[(-0.42, 0.06), (-0.58, 0.16), (-0.7, 0.24)])}),
    # prowling / clawing and roaring, goat spewing gas, serpent striking   (magicenhanced eediretiger)
    "chimera": dict(build=b_chimera, res=128, scale=1.5, shadow=(26, 104), poses={
        "1": dict(c=(0.0, 0.52), feet=[(0.38, 0.03, 0.1), (0.2, 0.03, -0.09), (-0.24, 0.03, 0.09),
                                       (-0.4, 0.03, -0.09)],
                  hp=(0.56, 0.14), look=-6, jaw=8, gp=(0.1, 0.48), glook=12, gjaw=6,
                  tail=[(-0.42, 0.06), (-0.6, 0.2), (-0.66, 0.42), (-0.56, 0.6), (-0.42, 0.66)], slook=-20, sjaw=8),
        "2": dict(c=(0.04, 0.55), pitch=8, feet=[(0.62, 0.3, 0.1), (0.4, 0.03, -0.09), (-0.3, 0.03, 0.09),
                                                 (-0.44, 0.03, -0.09)],
                  hp=(0.6, 0.16), look=8, jaw=40, gp=(0.14, 0.52), glook=2, gjaw=32, gas=True,
                  tail=[(-0.42, 0.06), (-0.58, 0.24), (-0.55, 0.5), (-0.35, 0.7), (-0.12, 0.74)], slook=-25,
                  sjaw=40, halo=True)}),
    # riding / firing the tesla pistol forward                      (goldenhorde horseman)
    "motorcycle": dict(build=b_motorcycle, shadow=(12, 52), poses={
        "1": dict(feet=(Q(0.1, 0.3, 0.2), Q(0.1, 0.3, -0.2)), knee=add(QF, (0, 0.6, 0)), body=Q(-0.18, -0.1),
                  lean=16, twist=-43, nod=-6, hand_r=Q(0.48, 0.98, -0.24), hand_l=Q(0.48, 0.98, 0.24)),
        "2": dict(feet=(Q(0.1, 0.3, 0.2), Q(0.1, 0.3, -0.2)), knee=add(QF, (0, 0.6, 0)), body=Q(-0.18, -0.1),
                  lean=12, twist=-43, nod=-4, hand_r=Q(0.48, 0.98, -0.24), hand_l=Q(0.62, 1.32, 0.3),
                  gun=look(4), fire=True, halo=True)}),
    # coil humming / lightning thrown forward                       (zion chariot)
    "truck": dict(build=b_truck, res=128, scale=1.15, shadow=(14, 112), poses={
        "1": dict(), "2": dict(fire=True, halo=True)}),
    # the nation banner                                             (albion flag)
    "flag": dict(build=b_flag, res=128, yaw=0.0, pitch=6.0, shadow=None, free_rows=False, poses={
        "": dict(halo=True)}),
})

# ================================================================ heroes, third wave
(ALBINO, ALIEN, SILVER, RUST) = range(58, 62)
PALETTE.update({
    ALBINO: ((248, 244, 242), (212, 204, 206), (162, 154, 160)),
    ALIEN: ((178, 214, 188), (130, 168, 144), (90, 122, 104)),
    SILVER: ((214, 218, 226), (160, 166, 178), (108, 114, 128)),
    RUST: ((156, 76, 52), (114, 54, 38), (80, 38, 30)),
})


def wrench(g, hand, d, k=1.0):
    g.add(capsule(add(hand, mul(d, -0.06 * k)), add(hand, mul(d, 0.34 * k)), 0.018 * k), STEEL)
    g.add(box(add(hand, mul(d, 0.37 * k)), (0.055 * k, 0.014 * k, 0.04 * k), blade_basis(d), rnd=0.012), STEEL)


def clank(P):
    """The Spark's robot: a knee-to-chest high brass boiler on stubby legs, furnace glowing in its
    belly, one lens eye, a smokestack, long arms with big fists."""
    b, punch = P["clank"], P.get("punch")
    f = norm(add(SL, mul(OUT, 0.4)))                      # it faces screen-left, a little to the viewer
    sd = norm(cross((0, 1, 0), f))

    def at(fw, y, s=0.0):
        return add(add(b, mul(f, fw)), add((0, y, 0), mul(sd, s)))
    g = Group("clank")
    g.add(capsule(at(0, 0.42), at(0, 0.72), 0.19), BRASS)                                # upright boiler
    for y in (0.36, 0.57, 0.8):
        g.add(torus(at(0, y), (0, 1, 0), 0.19, 0.016), COPPER)                           # riveted bands
    g.add(disc(at(0.18, 0.47), f, 0.08, 0.03), MECHD)                                     # furnace door
    g.add(disc(at(0.205, 0.47), f, 0.055, 0.012), G_FIRE)                                 # glowing grate
    g.add(box(at(0.02, 0.98), (0.09, 0.075, 0.1), basis(f), rnd=0.03), MECHD)            # iron head
    g.add(sphere(at(0.12, 0.99), 0.04), G_CYAN)                                           # lens eye
    g.add(capsule(at(-0.1, 0.86), at(-0.12, 1.12), 0.028), COPPER)                        # smokestack
    g.add(sphere(at(-0.14, 1.2), 0.045), MGREY)                                           # puffs of smoke
    g.add(sphere(at(-0.2, 1.28, 0.02), 0.06), MGREY)
    for s in (1, -1):                                                                     # stubby legs
        g.add(capsule(at(0.0, 0.3, 0.1 * s), at(0.02, 0.08, 0.11 * s), 0.05), MECHD)
        g.add(box(at(0.05, 0.04, 0.11 * s), (0.07, 0.04, 0.09), basis(f), rnd=0.02), BRASS)
    for s in (1, -1):                                                                     # long arms, big fists
        sh = at(0.0, 0.78, 0.22 * s)
        if punch and s > 0:
            el, fist = at(0.22, 0.74, 0.26), at(0.48, 0.74, 0.22)
        else:
            el, fist = at(0.05, 0.52, 0.27 * s), at(0.09, 0.3, 0.26 * s)
        g.add(sphere(sh, 0.055), COPPER)
        g.add(capsule(sh, el, 0.034), MECHD)
        g.add(capsule(el, fist, 0.034), MECHD)
        g.add(sphere(fist, 0.07), BRASS)
    if punch:
        tip = at(0.55, 0.74, 0.22)
        for k in range(3):
            bolt(g, tip, add(tip, mul(norm(add(f, (0, 0.6 * (k - 1), 0))), 0.13)), G_SPARK, 0.008, 3, 0.025, seed=k + 21)
    return g


def b_spark(R):
    """The Spark: a young genius in goggles, white blouse, leather corset and long rust skirt,
    a big wrench in her hand and her boiler-bellied robot at her side."""
    P = R.P
    legs(R, TROUS, TROUS, BOOT, lt=0.9, boot_top=0.6)
    t = Group("torso")
    t.add(ellipsoid((0, 0.96, 0), (0.15, 0.1, 0.1)), RUST)                                # hips
    t.add(ellipsoid((0, 1.15, 0), (0.112, 0.17, 0.084)), SHOE_BR)                         # leather corset
    t.add(ellipsoid((0, 1.31, -0.005), (0.13, 0.105, 0.088)), LABW)                       # blouse
    for s in (1, -1):
        t.add(ellipsoid((0.05 * s, 1.28, 0.055), (0.054, 0.05, 0.045)), LABW)
        t.add(sphere((0.03 * s, 1.12, 0.083), 0.009), BRASS)                              # corset buckles
    t.add(capsule((-0.138, 1.4, -0.005), (0.138, 1.4, -0.005), 0.048), LABW)
    t.add(cone_skirt((0, 1.0, 0), (0, 0.44, -0.01), 0.15, 0.21, -0.2, 0.17), RUST)        # skirt to mid-calf
    t.add(box((0, 1.0, 0), (0.158, 0.022, 0.11), rnd=0.02), BELT)                          # tool belt
    for x in (-0.11, 0.11):
        t.add(box((x, 0.95, 0.105), (0.03, 0.04, 0.02), rnd=0.006), BELT)
    R.body(t)
    h = Group("head")
    face(h, PSKIN)
    for prim in (ellipsoid((0, 1.655, -0.012), (0.08, 0.06, 0.09)),                       # blonde hair, tied up
                 ellipsoid((0, 1.6, -0.055), (0.078, 0.088, 0.055)),
                 sphere((0, 1.67, -0.12), 0.05),                                          # bun
                 ellipsoid((0.07, 1.555, 0.0), (0.022, 0.07, 0.035)),                     # loose strands
                 ellipsoid((-0.07, 1.555, 0.0), (0.022, 0.07, 0.035))):
        h.add(lumpy(prim, 0.008, 70), HAIR_BL)
    goggles(h, y=1.698, band=SHOE_BR, rim=BRASS, lens=LENS)                               # pushed up on the brow
    R.head(h)
    arm(R, -1, P["hand_r"], LABW, PSKIN, BELT, at=0.88, sh_w=0.165)                       # sleeves rolled up
    arm(R, 1, P["hand_l"], LABW, PSKIN, BELT, at=0.88, sh_w=0.165)
    g = Group("wrench")
    wrench(g, P["hand_r"], norm(P["wrench"]), 1.1)
    R.world(g)
    R.world(clank(P))


def ray_gun(g, hand, d, fire=False):
    """1950s ray gun: finned body, rings, a flared emitter; firing throws a beam of rings."""
    gb = bar_basis(d)

    def gl(a, b=0.0):
        return add(hand, add(mul(d, a), mul(gb[1], b)))
    g.add(box(gl(0.0, -0.01), (0.016, 0.04, 0.02), gb, rnd=0.006), MDARK)                 # grip
    g.add(capsule(gl(-0.05, 0.045), gl(0.12, 0.045), 0.03), SILVER)                       # body
    for a in (0.02, 0.07):
        g.add(torus(gl(a, 0.045), d, 0.032, 0.009), CRED)                                 # rings
    g.add(roundcone(gl(-0.04, 0.05), gl(-0.07, 0.11), 0.018, 0.006), CRED)                # tail fin
    g.add(roundcone(gl(0.12, 0.045), gl(0.19, 0.045), 0.012, 0.03), SILVER)               # flared muzzle
    g.add(sphere(gl(0.2, 0.045), 0.02), G_CYAN)
    if fire:
        a, b = gl(0.22, 0.045), gl(1.0, 0.045)
        g.add(capsule(a, b, 0.012), G_CYAN)
        for k in range(1, 5):
            g.add(torus(lerp(a, b, k / 5), d, 0.03 + 0.012 * k, 0.008), G_CYAN)


def b_visitor(R):
    """The Visitor: a pale green stranger with a domed skull and black almond eyes, in a silver
    suit with a glowing belt, a glass bubble helmet and a ray gun."""
    P = R.P
    legs(R, SILVER, SILVER, MDARK, boot_top=0.55)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.14, 0.1, 0.095)), SILVER)
    t.add(ellipsoid((0, 1.17, 0), (0.12, 0.2, 0.088)), SILVER)
    t.add(ellipsoid((0, 1.31, 0), (0.15, 0.115, 0.098)), SILVER)
    t.add(capsule((-0.155, 1.4, -0.005), (0.155, 1.4, -0.005), 0.05), SILVER)
    t.add(box((0, 1.0, 0), (0.145, 0.024, 0.1), rnd=0.02), MDARK)                          # belt
    t.add(disc((0, 1.0, 0.1), (0, 0, 1), 0.026, 0.01), G_CYAN)                            # glowing buckle
    t.add(shell(ellipsoid((0, 1.31, 0), (0.152, 0.117, 0.1)), 0.006, 1.37, 1.4), MDARK)  # yoke seam
    R.body(t)
    h = Group("head")
    h.add(capsule((0, 1.46, -0.005), (0, 1.54, 0.005), 0.036), ALIEN)                     # thin neck
    h.add(ellipsoid((0, 1.62, 0.0), (0.075, 0.112, 0.088)), ALIEN)                        # tall domed skull
    h.add(ellipsoid((0, 1.555, 0.04), (0.035, 0.035, 0.04)), ALIEN)                       # small chin
    for s in (1, -1):                                                                     # big black almond eyes
        h.add(ellipsoid((0.03 * s, 1.61, 0.075), (0.021, 0.013, 0.011)), HAIR_BK)
    c, n = (0, 1.62, 0.01), norm(add(OUT, (0, 0.15, 0)))
    bub = sphere(c, 0.16)

    def back(x, y, z, f=bub[0]):          # the glass shows as a ring: only the half away from the viewer
        return max(abs(f(x, y, z)) - 0.004, dot((x - c[0], y - c[1], z - c[2]), n) + 0.03)
    h.add((back, c, 0.17), GLASS)
    h.add(sphere(add(c, mul(norm(add(add(n, SL), (0, 1.2, 0))), 0.152)), 0.012), GLASS)  # glint
    h.add(torus((0, 1.47, 0.0), (0, 1, 0), 0.13, 0.022), SILVER)                          # helmet collar ring
    R.head(h)
    arm(R, -1, P["hand_r"], SILVER, SILVER, MDARK, at=0.92)
    arm(R, 1, P["hand_l"], SILVER, SILVER, ALIEN if P.get("palm") else MDARK, at=0.92)
    g = Group("raygun")
    ray_gun(g, P["hand_r"], norm(P["gun"]), P.get("fire"))
    R.world(g)


def cutlery(g, c, d, kind):
    """A spoon, fork or key hanging in the air (the prophet pulls metal to him)."""
    e = norm(d)
    g.add(capsule(c, add(c, mul(e, 0.16)), 0.012), STEEL)
    tip = add(c, mul(e, 0.19))
    if kind == 0:
        g.add(ellipsoid(tip, (0.03, 0.03, 0.03)), STEEL)                                  # spoon bowl
    elif kind == 1:
        side = norm(cross(e, OUT))
        for k in (-1, 1):
            g.add(capsule(add(tip, mul(side, 0.016 * k)), add(add(tip, mul(side, 0.016 * k)), mul(e, 0.06)), 0.008),
                  STEEL)                                                                  # fork tines
    else:
        g.add(torus(add(c, mul(e, -0.02)), OUT, 0.03, 0.009), BRASS)                      # key ring


def b_lightningprophet(R):
    """The lightning prophet: a slight young man, hairless and chalk white, in an oversized grey
    suit; spoons, forks and keys float around him, and lightning finds him."""
    P = R.P
    legs(R, TROUS, TROUS, SHOE_BR, boot_top=0.12)

    def jacket(t):
        t.add(box((0, 1.25, 0.082), (0.04, 0.16, 0.01), rnd=0.008), LABW)                 # white shirt, open collar
        for s in (1, -1):
            t.add(box((0.07 * s, 1.32, 0.092), (0.022, 0.09, 0.006),
                      (norm((1, 0, 0)), norm((0.3 * s, 1, 0)), (0, 0, 1)), rnd=0.004), MDARK)  # lapels
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.14, 0.1, 0.095)), TROUS)
    t.add(ellipsoid((0, 1.17, 0), (0.13, 0.2, 0.09)), MGREY)                              # baggy jacket
    t.add(ellipsoid((0, 1.31, 0), (0.15, 0.115, 0.095)), MGREY)
    t.add(capsule((-0.16, 1.4, -0.005), (0.16, 1.4, -0.005), 0.05), MGREY)
    t.add(cone_skirt((0, 1.08, -0.01), (0, 0.84, -0.03), 0.13, 0.16, -0.2, -0.02), MGREY)  # jacket hem
    jacket(t)
    R.body(t)
    h = Group("head")
    face(h, ALBINO)
    h.add(ellipsoid((0, 1.645, -0.01), (0.074, 0.075, 0.086)), ALBINO)                   # smooth bald dome
    for s in (1, -1):
        h.add(ellipsoid((0.071 * s, 1.6, -0.005), (0.012, 0.022, 0.016)), ALBINO)         # ears
    eyes(h, G_SPARK if P.get("cast") else LENS, r=0.01)                                   # pale eyes, lit when struck
    R.head(h)
    Js = {s: arm(R, s, P["hand_r" if s < 0 else "hand_l"], MGREY, MGREY, ALBINO, at=0.9) for s in (-1, 1)}
    g = Group("metal")
    for k, (pos, d) in enumerate(P["metal"]):                                             # floating cutlery
        cutlery(g, pos, d, k % 3)
        if P.get("cast") and k % 2 == 0:
            bolt(g, pos, add(pos, (0.03, 0.08, 0.02)), G_SPARK, 0.006, 3, 0.02, seed=k + 31)
    R.world(g)
    z = Group("lightning")
    if P.get("cast"):
        top = R.T((0.02, 3.2, 0.0))
        lightning(z, top, R.T((0.0, 1.76, 0.02)), seed=7, r=0.012, kinks=5, amp=0.15, branches=1)  # strike from above
        for k, s in enumerate((-1, 1)):
            hc = Js[s][4]
            bolt(z, R.T((0.0, 1.74, 0.02)), hc, G_SPARK, 0.009, 3, 0.03, seed=k + 3)        # through the body
        hr = Js[1][4]
        lightning(z, hr, add(hr, mul(aim(P.get("bolt", 10)), 0.75)), seed=13, r=0.011, kinks=5, amp=0.1,
                  branches=1)
    else:
        for k, s in enumerate((-1, 1)):                                                   # static at the fingertips
            hc = Js[s][4]
            bolt(z, hc, add(hc, (0.02 * s, -0.1, 0.03)), G_SPARK, 0.006, 3, 0.02, seed=k + 41)
    R.world(z)


UNITS.update({
    # wrench on the shoulder, robot waiting / wrench pointed, robot punching   (venedia alchemist)
    "spark": dict(build=b_spark, shadow=(10, 42), poses={
        "1": dict(feet=FEET(0.04, -0.06, -0.06, 0.05), hand_r=W(-0.02, 1.36, 0.16), wrench=aim(118, 0.2),
                  pole_r=(-1, -0.7, 0.2), hand_l=W(-0.04, 1.0, 0.16), pole_l=(1, -0.6, -0.4),
                  clank=W(0.5, 0, 0.36)),
        "2": dict(feet=FEET(0.1, -0.08, -0.04, 0.05), lean=4, twist=-8, hand_r=W(0.42, 1.36, 0.1),
                  wrench=aim(25, 0.1), hand_l=W(-0.04, 1.0, 0.16), pole_l=(1, -0.6, -0.4),
                  clank=W(0.54, 0, 0.38), punch=True, halo=True)}),
    # ray gun lowered, open hand raised in greeting / ray gun fired      (juhera hero_sulaiman)
    "visitor": dict(build=b_visitor, scale=1.04, poses={
        "1": dict(feet=FEET(0.05, -0.05, -0.05, 0.05), hand_r=W(0.12, 0.96, 0.08), gun=aim(-60, 0.2),
                  hand_l=W(0.3, 1.52, 0.2), pole_l=(1, -0.8, 0.0), palm=True),
        "2": dict(feet=FEET(0.1, -0.08, -0.04, 0.05), twist=-12, hand_r=W(0.5, 1.36, 0.08), gun=aim(2),
                  hand_l=W(-0.08, 1.0, 0.14), fire=True, halo=True)}),
    # calm, metal floating around him / arms flung up, struck by lightning   (juhera hero_sinan)
    "lightningprophet": dict(build=b_lightningprophet, poses={
        "1": dict(feet=FEET(0.04, -0.04, -0.05, 0.05), nod=6, hand_r=W(-0.1, 0.9, 0.06), hand_l=W(0.14, 0.92, 0.2),
                  pole_r=(-0.3, -0.2, -1), pole_l=(0.3, -0.2, -1),
                  metal=[(W(0.42, 1.2, 0.14), (0.3, 1, 0.2)), (W(0.38, 1.56, 0.02), (-0.6, 0.5, 0.3)),
                         (W(-0.38, 1.36, 0.1), (0.2, -1, 0.3)), (W(-0.34, 1.0, 0.2), (1, 0.4, 0)),
                         (W(0.04, 1.86, 0.0), (0.7, 0.6, 0.1))]),
        "2": dict(feet=FEET(0.06, -0.06, -0.04, 0.05), nod=-14, lean=-3, hand_r=W(-0.34, 1.84, 0.0),
                  hand_l=W(0.38, 1.86, 0.12), pole_r=(-1, -0.2, -0.3), pole_l=(1, -0.2, -0.3), cast=True, bolt=8,
                  metal=[(W(0.56, 1.4, 0.12), (0.3, 1, 0.2)), (W(0.5, 2.06, 0.02), (-0.6, 0.4, 0.3)),
                         (W(-0.5, 1.6, 0.1), (0.2, -1, 0.3)), (W(-0.42, 1.18, 0.2), (1, 0.3, 0)),
                         (W(-0.16, 2.18, 0.0), (0.7, 0.6, 0.1))], halo=True)}),
})

# ================================================================ fourth wave: rider on foot, pretenders, item icons
def b_voltrider(R):
    """The Volt Rider on foot (#unmountedspr): leather jacket, red scarf, leather cap and goggles,
    short sword and tesla pistol."""
    P = R.P
    legs(R, TROUS, TROUS, BOOT, boot_top=0.4)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), TROUS)
    t.add(ellipsoid((0, 1.17, 0), (0.14, 0.2, 0.1)), BELT)
    t.add(ellipsoid((0, 1.31, 0), (0.162, 0.12, 0.106)), BELT)
    t.add(capsule((-0.165, 1.41, -0.005), (0.165, 1.41, -0.005), 0.056), BELT)
    t.add(cone_skirt((0, 1.05, 0), (0, 0.86, -0.01), 0.15, 0.18, -0.15, 0.14), BELT)      # jacket hem
    t.add(box((0, 0.99, 0), (0.15, 0.024, 0.104), rnd=0.02), BOOT)
    t.add(torus((0, 1.46, 0.0), (0, 1, 0), 0.07, 0.03), CRED)                               # scarf
    chain(t, [(0.04, 1.45, -0.07), (0.07, 1.34, -0.12), (0.06, 1.2, -0.13)], 0.03, 0.018, CRED)
    R.body(t)
    h = Group("head")
    face(h, SKIN)
    h.add(shell(ellipsoid(HEAD_C, add(HEAD_R, (0.012, 0.012, 0.012))), 0.016, 1.6, 1.75), BELT)  # leather cap
    goggles(h, y=1.645)
    R.head(h)
    arm(R, -1, P["hand_r"], BELT, BELT, BOOT)
    arm(R, 1, P["hand_l"], BELT, BELT, BOOT)
    g = Group("weapons")
    sword(g, P["hand_r"], P["blade"], blen=0.5, width=0.024, guard=BRASS, wrap=BOOT)
    d = norm(P["gun"])
    muzzle = pistol(g, P["hand_l"], d, body=MECHD, grip=COPPER)
    g.add(sphere(muzzle, 0.018), G_SPARK)
    if P.get("fire"):
        lightning(g, muzzle, add(muzzle, mul(d, 0.8)), seed=73, r=0.01, kinks=5, amp=0.09, branches=1)
    R.world(g)


def b_dynamo(R):
    """The Great Dynamo (pretender): a stepped brass shrine, four corner coils, and a giant coil
    column with a caged blue core and a steel crown that throws lightning."""
    P = R.P
    g = Group("plinth")
    for y, r, h, mat in ((0.08, 0.64, 0.08, MECHD), (0.22, 0.54, 0.07, BRASS), (0.34, 0.44, 0.05, GOLD)):
        for a in (0, 45):
            g.add(box((0, y, 0), (r * 0.92, h, r * 0.92), yaw_basis(a), rnd=0.02), mat)
    R.world(g)
    c = Group("coils")
    tops = []
    for k in range(4):
        a = TAU * (k + 0.5) / 4
        b0 = (0.42 * cos(a), 0.38, 0.42 * sin(a))
        c.add(grooves(capsule(b0, add(b0, (0, 0.5, 0)), 0.06), b0, (0, 1, 0), 0.035, 0.01), COPPER)
        top = add(b0, (0, 0.58, 0))
        c.add(torus(add(b0, (0, 0.52, 0)), (0, 1, 0), 0.07, 0.025), STEEL)
        c.add(sphere(top, 0.05), G_SPARK)
        tops.append(top)
    c.add(grooves(capsule((0, 0.4, 0), (0, 1.02, 0), 0.15), (0, 0, 0), (0, 1, 0), 0.045, 0.014), COPPER)
    c.add(torus((0, 1.04, 0), (0, 1, 0), 0.17, 0.035), GOLD)
    for k in range(6):                                                                     # cage around the core
        a = TAU * k / 6
        c.add(capsule((0.2 * cos(a), 1.04, 0.2 * sin(a)), (0.2 * cos(a), 1.5, 0.2 * sin(a)), 0.018), BRASS)
    c.add(torus((0, 1.5, 0), (0, 1, 0), 0.17, 0.035), GOLD)
    c.add(grooves(capsule((0, 1.52, 0), (0, 2.12, 0), 0.12), (0, 0, 0), (0, 1, 0), 0.04, 0.012), COPPER)
    R.world(c)
    e = Group("core")
    e.add(sphere((0, 1.27, 0), 0.15), G_CYAN)
    R.world(e)
    t = Group("crown")
    top = (0, 2.26, 0)
    t.add(torus(top, (0, 1, 0), 0.34, 0.12), STEEL)
    for k in range(8):                                                                     # gold studs
        a = TAU * k / 8
        t.add(sphere(add(top, (0.34 * cos(a), 0.1, 0.34 * sin(a))), 0.04), GOLD)
    t.add(sphere(add(top, (0, 0.1, 0)), 0.08), G_SPARK)
    R.world(t)
    z = Group("lightning")
    rim = lambda a: add(top, (0.48 * cos(a), 0.0, 0.48 * sin(a)))
    if P.get("fire"):
        for k, (a, tgt) in enumerate(((2.4, W(1.6, 1.0, 0.1)), (2.9, W(1.2, 0.05, 0.2)), (1.7, W(0.6, 3.6, 0.0)),
                                      (-0.5, W(-1.3, 3.2, 0.0)))):
            lightning(z, rim(a), tgt, seed=k + 121, r=0.022 if k < 2 else 0.016, kinks=6, amp=0.14,
                      branches=2 if k < 2 else 1)
        for k, p in enumerate(tops):                                                       # coils feed the crown
            bolt(z, p, rim(TAU * (k + 0.5) / 4), G_SPARK, 0.012, 4, 0.06, seed=k + 131)
    else:
        for k, p in enumerate(tops):
            bolt(z, p, add(p, (0.0, 0.16, 0.0)), G_SPARK, 0.01, 3, 0.03, seed=k + 141)
        for k, a in enumerate((2.6, 0.5)):
            p = rim(a)
            bolt(z, p, add(p, (0.2 * cos(a), 0.14, 0.2 * sin(a))), G_SPARK, 0.012, 3, 0.04, seed=k + 151)
    R.world(z)


def b_primeconstruct(R):
    """The Prime Construct (pretender): a towering chrome war machine with gold trim, a blue reactor
    heart, twin back coils, a crowned skull, a giant blade and a rotary cannon arm."""
    P = R.P

    def frame(g, s, hip, knee, ankle):
        g.add(sphere(hip, 0.06), MECHD)
        g.add(capsule(lerp(hip, knee, 0.15), lerp(knee, ankle, 0.1), 0.016), STEEL)       # piston
        g.add(limb(lerp(hip, knee, 0.1), lerp(hip, knee, 0.85), 0.088, 0.072), MECH)      # thigh armour
        g.add(limb(lerp(knee, ankle, 0.15), lerp(knee, ankle, 0.85), 0.074, 0.06), MECH)
        g.add(sphere(knee, 0.066), GOLD)
    legs(R, MECHD, MECHD, MECHD, lt=0.62, boot_top=0.14, extra=frame)
    t = Group("torso")
    t.add(box((0, 0.93, 0), (0.13, 0.055, 0.075), rnd=0.025), MECHD)                      # pelvis
    t.add(grooves(capsule((0, 0.96, -0.02), (0, 1.2, -0.02), 0.045), (0, 0, 0), (0, 1, 0), 0.035, 0.012), STEEL)
    t.add(box((0, 1.1, 0.03), (0.12, 0.065, 0.075), rnd=0.03), MECHD)
    t.add(box((0, 1.3, 0.02), (0.18, 0.135, 0.115), rnd=0.045), MECH)                     # breastplate
    t.add(shell(box((0, 1.3, 0.02), (0.18, 0.135, 0.115), rnd=0.045), 0.007, 1.405, 1.425), GOLD)
    t.add(torus((0, 1.3, 0.13), (0, 0, 1), 0.05, 0.014), GOLD)                            # reactor housing
    t.add(sphere((0, 1.3, 0.13), 0.04), G_CYAN)                                           # reactor heart
    t.add(box((0, 1.27, -0.15), (0.13, 0.13, 0.06), rnd=0.03), MECHD)                     # power pack
    for s in (1, -1):
        base = (0.08 * s, 1.36, -0.17)
        t.add(grooves(capsule(base, add(base, (0, 0.2, -0.02)), 0.035), base, (0, 1, 0), 0.025, 0.008), COPPER)
        t.add(sphere(add(base, (0, 0.25, -0.02)), 0.035), G_SPARK)
        pd = ellipsoid((0.23 * s, 1.43, 0), (0.1, 0.07, 0.1))                             # pauldrons
        t.add(pd, MECH)
        t.add(shell(pd, 0.007, 1.44, 1.46), GOLD)
    R.body(t)
    h = Group("head")
    h.add(capsule((0, 1.42, -0.01), (0, 1.53, 0.0), 0.024), STEEL)
    h.add(ellipsoid((0, 1.6, 0.0), (0.056, 0.07, 0.076)), MECH)                           # skull
    h.add(ellipsoid((0, 1.555, 0.035), (0.042, 0.035, 0.05)), MECHD)                      # jaw
    h.add(box((0, 1.6, 0.068), (0.044, 0.01, 0.012), rnd=0.004), G_CYAN)                  # eye slit
    h.add(torus((0, 1.655, -0.005), (0, 1, 0), 0.058, 0.012), GOLD)                       # crown band
    for k in range(5):                                                                    # crown spikes
        a = math.pi * (0.1 + 0.8 * k / 4)
        p = (0.058 * cos(a), 1.655, 0.058 * sin(a))
        h.add(roundcone(p, add(p, (0.01 * cos(a), 0.06, 0.01 * sin(a))), 0.014, 0.004), GOLD)
    R.head(h)

    def skel_arm(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(sphere(elbow, 0.048), MECHD)
        g.add(capsule(sh, lerp(sh, elbow, 0.85), 0.012), STEEL)
        g.add(limb(lerp(elbow, wrist, 0.1), lerp(elbow, wrist, 0.9), 0.056, 0.05), MECH)

    def cannon_arm(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(sphere(elbow, 0.05), MECHD)
        g.add(capsule(sh, lerp(sh, elbow, 0.85), 0.012), STEEL)
        g.add(limb(lerp(elbow, wrist, 0.05), add(wrist, mul(d, 0.08)), 0.07, 0.064), MECHD)  # cannon housing
        g.add(torus(lerp(elbow, wrist, 0.5), d, 0.068, 0.012), GOLD)
        n1, n2 = perp(d, (0, 1, 0))
        for k in range(3):                                                                # rotary barrels
            a = TAU * k / 3
            o = add(mul(n1, 0.028 * cos(a)), mul(n2, 0.028 * sin(a)))
            g.add(capsule(add(wrist, o), add(add(wrist, mul(d, 0.34)), o), 0.014), GUN)
        g.add(disc(add(wrist, mul(d, 0.28)), d, 0.05, 0.02), MECHD)
        if P.get("fire"):
            flash(g, add(wrist, mul(d, 0.36)), d, 1.4)
    arm(R, -1, P["hand_r"], MECH, MECH, MECHD, at=0.7, extra=skel_arm, sh_w=0.22)
    arm(R, 1, P["hand_l"], MECH, MECH, MECHD, at=0.7, extra=cannon_arm, sh_w=0.22, pole=P.get("pole_l"))
    g = Group("blade")
    sword(g, P["hand_r"], P["blade"], blen=0.95, width=0.055, hilt=0.12, blade=STEEL, guard=GOLD, wrap=MECHD,
          gw=0.07)
    R.world(g)


def b_brain(R):
    """The Patient Brain (pretender): a brain in glowing fluid under a glass jar, on a hovering brass
    base with a red ocular, two little claws and electrodes on the lid."""
    P = R.P
    lift = P.get("lift", 0.3)

    def at(x, y, z=0.0):
        return (x, y + lift, z)
    b = Group("base")
    b.add(disc(at(0, 0.02), (0, 1, 0), 0.25, 0.07), BRASS)
    b.add(torus(at(0, 0.02), (0, 1, 0), 0.25, 0.03), COPPER)
    b.add(roundcone(at(0, -0.04), at(0, -0.16), 0.13, 0.05), MECHD)                         # hover coil
    b.add(sphere(at(0, -0.19), 0.05), G_CYAN)
    b.add(disc(at(0, 0.09), (0, 1, 0), 0.21, 0.04), MECHD)                                 # jar seat
    for s in (1, -1):                                                                      # little claws
        sh = at(0.2 * s, 0.05, 0.08)
        el = add(sh, (0.1 * s, -0.08, 0.1))
        tip = add(el, (0.02 * s, -0.12, 0.06))
        b.add(capsule(sh, el, 0.018), MECHD)
        b.add(capsule(el, tip, 0.015), MECHD)
        b.add(sphere(el, 0.022), BRASS)
        for k in (-1, 1):
            b.add(capsule(tip, add(tip, (0.025 * k, -0.04, 0.02)), 0.008), STEEL)
    R.world(b)
    jar(R, at(0, 0.11), P.get("cast"), eye=True)


def jar(R, base, cast=False, eye=False, k=1.0):
    """Glass jar of glowing fluid with a brain in it, brass lid and electrodes. Only the far half of
    the glass and the fluid is drawn, so the brain shows through."""
    c = add(base, (0, 0.28 * k, 0))
    n = norm(add(OUT, (0, 0.2, 0)))
    j = Group("jar")
    glass = capsule(add(base, (0, 0.12 * k, 0)), add(base, (0, 0.44 * k, 0)), 0.2 * k)
    fluid = capsule(add(base, (0, 0.12 * k, 0)), add(base, (0, 0.4 * k, 0)), 0.185 * k)

    def back(f, w, cut):
        def g(x, y, z):
            return max(abs(f(x, y, z)) - w, dot((x - c[0], y - c[1], z - c[2]), n) + cut)
        return g
    j.add((back(glass[0], 0.006 * k, 0.03 * k), c, 0.5 * k), GLASS)
    j.add((back(fluid[0], 0.012 * k, 0.06 * k), c, 0.5 * k), G_GREEN)
    for y in (0.0, 0.62):                                                                  # brass rims
        j.add(torus(add(base, (0, y * k, 0)), (0, 1, 0), 0.2 * k, 0.025 * k), BRASS)
    j.add(disc(add(base, (0, 0.66 * k, 0)), (0, 1, 0), 0.19 * k, 0.05 * k), BRASS)        # lid
    j.add(lumpy(ellipsoid(add(c, (0, 0.0, 0.02 * k)), (0.14 * k, 0.11 * k, 0.15 * k)), 0.012 * k, 60), FLESH)
    j.add(capsule(add(c, (0, -0.08 * k, -0.02 * k)), add(base, (0, 0.02 * k, -0.02 * k)), 0.025 * k), FLESH)
    tips = []
    for s in (1, -1):                                                                      # electrodes
        p = add(base, (0.1 * s * k, 0.7 * k, 0))
        q = add(p, (0.03 * s * k, 0.14 * k, 0))
        j.add(capsule(p, q, 0.016 * k), COPPER)
        j.add(sphere(q, 0.028 * k), G_SPARK)
        tips.append(q)
    if eye:                                                                                # ocular on a stalk
        a = add(base, (0.05 * k, 0.66 * k, 0.12 * k))
        m = add(a, mul(add(SL, (0, 0.6, 0)), 0.1 * k))
        e = add(m, mul(add(SL, OUT), 0.07 * k))
        j.add(capsule(a, m, 0.014 * k), BRASS)
        j.add(capsule(m, e, 0.014 * k), BRASS)
        j.add(disc(e, add(SL, OUT), 0.04 * k, 0.03 * k), BRASS)
        j.add(sphere(add(e, mul(norm(add(SL, OUT)), 0.012 * k)), 0.026 * k), G_RED)
    R.world(j)
    z = Group("arcs")
    if cast:
        bolt(z, tips[0], tips[1], G_SPARK, 0.01 * k, 4, 0.03 * k, seed=161)
        lightning(z, tips[0], add(tips[0], mul(aim(12), 0.9)), seed=163, r=0.011, kinks=5, amp=0.1, branches=1)
        for i, v in enumerate((aim(60), aim(150, 0.2))):
            bolt(z, add(c, mul(v, 0.12 * k)), add(c, mul(v, 0.22 * k)), G_SPARK, 0.007 * k, 3, 0.02 * k,
                 seed=i + 165)
    else:
        bolt(z, tips[0], tips[1], G_SPARK, 0.009 * k, 4, 0.03 * k, seed=161)
    R.world(z)


# ---------------------------------------------------------------- item icons (64x64, item <= 40 px, centred)
def i_gauntlet(R):
    """Tesla Gauntlet: copper forearm with coil bands, dark iron hand, sparks at the fingertips."""
    a, w = (0.36, -0.42, 0.0), (0.0, 0.0, 0.05)                                            # elbow -> wrist
    d = norm(sub(w, a))
    g = Group("gauntlet")
    g.add(limb(a, w, 0.15, 0.12), COPPER)
    for t in (0.2, 0.45, 0.7):
        g.add(torus(lerp(a, w, t), d, 0.15 - 0.03 * t, 0.025), BRASS)
    g.add(torus(a, d, 0.16, 0.035), BRASS)
    hc = add(w, mul(d, 0.12))
    g.add(box(hc, (0.15, 0.07, 0.13), basis(d, (0, 0, 1)), rnd=0.05), MECHD)              # back of the hand
    n1, n2 = perp(d, (0, 0, 1))
    tips = []
    for k in range(4):                                                                     # fingers
        o = mul(n1, 0.11 * (k - 1.5) / 1.5)
        f0 = add(add(hc, mul(d, 0.11)), o)
        f1 = add(f0, mul(norm(add(add(d, mul(n2, 0.3)), mul(n1, 0.35 * (k - 1.5) / 1.5))), 0.22))
        g.add(capsule(f0, f1, 0.04), MECHD)
        g.add(sphere(f1, 0.04), COPPER)
        tips.append(f1)
    th = add(add(hc, mul(n1, -0.15)), mul(d, -0.02))
    g.add(capsule(th, add(th, mul(norm(add(d, mul(n1, -0.9))), 0.17)), 0.04), MECHD)       # thumb
    g.add(capsule(add(a, (0.0, 0.0, -0.14)), add(lerp(a, w, 0.7), (0, 0.0, -0.13)), 0.025), GLASS)  # capacitor
    g.add(capsule(add(a, (0.0, 0.0, -0.14)), add(lerp(a, w, 0.7), (0, 0.0, -0.13)), 0.014), G_SPARK)
    R.world(g)
    z = Group("sparks")
    for k, p in enumerate(tips):
        if k < 3:                                                                          # arcs between fingers
            bolt(z, p, tips[k + 1], G_SPARK, 0.014, 3, 0.03, seed=k + 175)
        bolt(z, p, add(p, mul(norm(add(d, (0.1 * k - 0.15, 0.3, 0))), 0.16)), G_SPARK, 0.016, 3, 0.04, seed=k + 171)
    R.world(z)


def i_jar(R):
    """Brain in a Jar, as an item."""
    b = Group("stand")
    b.add(disc((0, -0.5, 0), (0, 1, 0), 0.24, 0.06), BRASS)
    b.add(disc((0, -0.44, 0), (0, 1, 0), 0.21, 0.04), MECHD)
    R.world(b)
    jar(R, (0, -0.42, 0), cast=False, eye=False, k=1.25)


def i_capacitor(R):
    """Capacitor Pack: a riveted backpack with two glowing glass capacitors and a coil on top."""
    g = Group("pack")
    g.add(box((0, 0.0, 0), (0.3, 0.36, 0.14), rnd=0.05), MECHD)
    for y in (-0.22, 0.22):
        g.add(shell(box((0, 0.0, 0), (0.3, 0.36, 0.14), rnd=0.05), 0.012, y - 0.03, y + 0.03), COPPER)
    for s in (1, -1):
        b0 = (0.15 * s, -0.3, 0.17)
        g.add(capsule(b0, add(b0, (0, 0.56, 0)), 0.075), GLASS)                           # capacitor tubes
        g.add(capsule(b0, add(b0, (0, 0.56, 0)), 0.05), G_SPARK)
        g.add(disc(add(b0, (0, -0.04, 0)), (0, 1, 0), 0.09, 0.05), COPPER)
        g.add(disc(add(b0, (0, 0.6, 0)), (0, 1, 0), 0.09, 0.05), COPPER)
        g.add(capsule((0.18 * s, 0.32, -0.16), (0.18 * s, -0.3, -0.2), 0.03), BELT)       # straps
    g.add(grooves(capsule((0, 0.36, 0), (0, 0.56, 0), 0.06), (0, 0, 0), (0, 1, 0), 0.03, 0.01), COPPER)
    g.add(torus((0, 0.6, 0), (0, 1, 0), 0.09, 0.03), STEEL)
    g.add(sphere((0, 0.63, 0), 0.04), G_SPARK)
    R.world(g)


def i_goggles(R):
    """Precision Goggles: big brass rims, blue lenses, a flip-down magnifier and a leather strap."""
    g = Group("goggles")
    for s in (1, -1):
        c = (0.17 * s, 0.0, 0.1)
        g.add(disc(c, (0, 0, 1), 0.13, 0.1), BRASS)
        g.add(disc(add(c, (0, 0, 0.055)), (0, 0, 1), 0.095, 0.02), LENS)
        g.add(torus(add(c, (0, 0, 0.05)), (0, 0, 1), 0.11, 0.02), BRASS)
    g.add(capsule((-0.05, 0.02, 0.1), (0.05, 0.02, 0.1), 0.03), BRASS)                     # bridge
    sh = shell(ellipsoid((0, 0.0, -0.05), (0.3, 0.3, 0.2)), 0.02, -0.05, 0.05)            # strap loop
    g.add((lambda x, y, z, f=sh[0]: max(f(x, y, z), z - 0.02), (0, 0, -0.05), 0.35), BELT)
    m = (0.17, 0.16, 0.2)                                                                  # flipped-up magnifier
    g.add(capsule((0.27, 0.06, 0.12), add(m, (0.1, 0.0, 0)), 0.015), BRASS)
    g.add(disc(m, (0, 0.6, 1), 0.075, 0.03), BRASS)
    g.add(disc(add(m, (0, 0.01, 0.02)), (0, 0.6, 1), 0.055, 0.012), LENS)
    R.world(g)


def i_coat(R):
    """Insulated Coat: a long yellow rubber coat with black collar, cuffs and copper buttons, on a hook."""
    g = Group("coat")
    g.add(ellipsoid((0, 0.2, 0), (0.24, 0.24, 0.13)), RUBBER)
    g.add(capsule((-0.26, 0.38, 0), (0.26, 0.38, 0), 0.09), RUBBER)                       # shoulders
    g.add(cone_skirt((0, 0.2, 0), (0, -0.42, 0), 0.23, 0.31), RUBBER)
    g.add(capsule((0.0, 0.4, 0.13), (0.0, -0.42, 0.2), 0.012), BOOT)                     # front seam
    for s in (1, -1):
        g.add(capsule((0.3 * s, 0.36, 0.02), (0.4 * s, -0.12, 0.08), 0.075), RUBBER)      # hanging sleeves
        g.add(torus((0.4 * s, -0.12, 0.08), (0.2 * s, -1, 0.1), 0.07, 0.03), BOOT)        # black cuffs
    g.add(torus((0, 0.44, 0.0), (0, 1, 0.2), 0.12, 0.05), BOOT)                           # collar
    for y in (0.24, 0.06, -0.12):
        g.add(sphere((0.05, y, 0.15 + 0.03 * (y < 0)), 0.035), COPPER)                    # buttons
    g.add(capsule((0, 0.4, -0.02), (0, 0.56, -0.02), 0.015), STEEL)                       # hook
    g.add(torus((0, 0.6, -0.02), (1, 0, 0), 0.05, 0.015), STEEL)
    R.world(g)


def i_portalgun(R):
    """Portal Gun: grey blaster body, a green fluid canister on top, a glowing green emitter."""
    d = norm(SL)
    gb = bar_basis(d)

    def gl(a, b):
        return add((0.0, 0.0, 0.0), add(mul(d, a), mul(gb[1], b)))
    g = Group("gun")
    g.add(box(gl(0.05, 0.05), (0.09, 0.1, 0.26), gb, rnd=0.04), MGREY)                   # body
    g.add(box(gl(-0.05, -0.15), (0.05, 0.12, 0.06), gb, rnd=0.02), BOOT)                 # grip
    g.add(box(gl(0.05, 0.05), (0.095, 0.03, 0.2), gb, rnd=0.01), BOOT)                   # side stripe
    for a in (-0.1, 0.16):
        g.add(disc(gl(a, 0.27), (0, 1, 0), 0.07, 0.03), MDARK)                            # canister caps
    g.add(capsule(gl(-0.1, 0.27), gl(0.16, 0.27), 0.06), G_GREEN)                        # fluid canister
    g.add(roundcone(gl(0.28, 0.05), gl(0.38, 0.05), 0.07, 0.1), MDARK)                   # flared emitter
    g.add(sphere(gl(0.5, 0.05), 0.085), G_GREEN)
    g.add(torus(gl(0.18, 0.05), d, 0.1, 0.02), STEEL)
    R.world(g)


ITEM = dict(res=64, cx=32, y0=32, shadow=None, free_rows=False, pitch=16.0)
UNITS.update({
    # sabre low, pistol ready / pistol fired, lightning               (greatarrada officer, like the alpha clone)
    "voltrider": dict(build=b_voltrider, poses={
        "1": dict(feet=FEET(0.1, -0.08, -0.02, 0.05), hand_r=W(0.18, 1.0, 0.1), blade=aim(-40),
                  hand_l=W(0.3, 1.04, 0.2), gun=aim(-38), pole_l=(1, -0.6, 0.3)),
        "2": dict(feet=FEET(0.14, -0.1, -0.02, 0.05), twist=-12, hand_r=W(0.12, 1.0, 0.06), blade=aim(-40),
                  hand_l=W(0.5, 1.38, 0.12), gun=aim(2), fire=True, halo=True)}),
    # humming / throwing lightning                                  (structure, like the tesla pylon)
    "dynamo": dict(build=b_dynamo, res=128, scale=1.55, shadow=(34, 94), poses={
        "1": dict(halo=True), "2": dict(fire=True, halo=True)}),
    # blade up, cannon ready / horizontal slash                    (greatarrada swordplate, like the war droids)
    "primeconstruct": dict(build=b_primeconstruct, res=128, scale=2.45, shadow=(38, 92), poses={
        "1": dict(feet=FEET(0.14, -0.14, 0.0, 0.05), body=(0, -0.03, 0), hand_r=W(0.2, 1.34, 0.04),
                  blade=aim(62, -0.1), hand_l=W(0.4, 1.16, 0.28), pole_l=(1, -0.8, -0.2)),
        "2": dict(feet=FEET(0.26, -0.18, 0.0, 0.04), body=(0, -0.05, 0.02), lean=8, twist=-15,
                  hand_r=W(0.5, 1.25, 0.05), blade=aim(4), hand_l=W(0.4, 1.12, 0.28), pole_l=(1, -0.8, -0.2))}),
    # hovering, electrodes humming / lightning from the lid         (structure, no stance)
    "brain": dict(build=b_brain, scale=1.2, shadow=(22, 40), poses={
        "1": dict(lift=0.3), "2": dict(lift=0.36, cast=True, halo=True)}),
    "item_teslagauntlet": dict(build=i_gauntlet, scale=1.55, poses={"": dict()}, **ITEM),
    "item_brainjar": dict(build=i_jar, scale=1.5, poses={"": dict()}, **ITEM),
    "item_capacitorpack": dict(build=i_capacitor, scale=1.6, poses={"": dict()}, **ITEM),
    "item_goggles": dict(build=i_goggles, scale=2.8, yaw=-20.0, poses={"": dict()}, **ITEM),
    "item_insulatedcoat": dict(build=i_coat, scale=1.35, poses={"": dict()}, **ITEM),
    "item_portalgun": dict(build=i_portalgun, scale=2.0, poses={"": dict()}, **ITEM),
})


def b_emblem(R):
    """The nation's emblem alone (gear struck by a bolt), for the mod banner."""
    e = Group("emblem")
    gc = (0, 0, 0)
    e.add(torus(gc, (0, 0, 1), 0.6, 0.12), BRASS)
    for i in range(10):
        a = TAU * i / 10
        e.add(box(add(gc, (0.76 * cos(a), 0.76 * sin(a), 0)), (0.1, 0.1, 0.06),
                  ((cos(a), sin(a), 0), (-sin(a), cos(a), 0), (0, 0, 1)), rnd=0.02), BRASS)
    e.add(disc(gc, (0, 0, 1), 0.45, 0.04), NAVY)
    pts = [(0.42, 1.0), (-0.1, 0.12), (0.26, 0.06), (-0.4, -1.0)]
    for p, q in zip(pts, pts[1:]):
        e.add(capsule((p[0], p[1], 0.16), (q[0], q[1], 0.16), 0.11), G_SPARK)
    R.world(e)


UNITS["emblem"] = dict(build=b_emblem, res=64, cx=32, y0=32, scale=1.15, yaw=0.0, pitch=0.0, shadow=None,
                       free_rows=False, poses={"": dict(halo=True)})


# ================================================================ fifth wave: town guard levy
def b_levy(R):
    """Longspear Militia: a town guardsman levy in a tan padded jacket under an indigo tabard with a
    copper bolt, iron kettle hat, two-handed longspear."""
    P = R.P
    legs(R, TROUS, TROUS, SHOE_BR, boot_top=0.36)
    t = Group("torso")
    t.add(ellipsoid((0, 0.95, 0), (0.15, 0.1, 0.1)), TRENCH)
    t.add(ellipsoid((0, 1.17, 0), (0.145, 0.2, 0.105)), TRENCH)
    t.add(ellipsoid((0, 1.31, 0), (0.167, 0.12, 0.11)), TRENCH)
    t.add(capsule((-0.17, 1.41, -0.005), (0.17, 1.41, -0.005), 0.06), TRENCH)
    t.add(cone_skirt((0, 1.0, 0), (0, 0.72, -0.01), 0.155, 0.19, -0.15, 0.14), TRENCH)    # gambeson skirt
    t.add(box((0, 1.12, 0.035), (0.1, 0.29, 0.09), rnd=0.04), NAVY)                     # tabard
    t.add(box((0, 0.84, 0.07), (0.085, 0.1, 0.05), rnd=0.02), NAVY)
    t.add(box((0, 0.745, 0.07), (0.087, 0.014, 0.052), rnd=0.006), COPPER)               # tabard hem
    for x in (-0.1, 0.1):
        t.add(box((x, 1.12, 0.035), (0.012, 0.29, 0.092), rnd=0.006), COPPER)            # tabard edges                        # tabard tail
    t.add(box((0, 0.99, 0), (0.152, 0.024, 0.112), rnd=0.02), BELT)                      # belt
    for p, q in (((0.03, 1.32, 0.122), (-0.02, 1.2, 0.122)), ((-0.02, 1.2, 0.122), (0.02, 1.19, 0.122)),
                 ((0.02, 1.19, 0.122), (-0.03, 1.07, 0.122))):
        t.add(capsule(add(p, (0, 0, 0.008)), add(q, (0, 0, 0.008)), 0.018), COPPER)                                              # copper bolt
    R.body(t)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BR)
    h.add(ellipsoid((0, 1.672, -0.004), (0.08, 0.058, 0.088)), MGREY)                    # kettle hat
    h.add(disc((0, 1.648, -0.004), (0, 1, 0), 0.125, 0.012), MGREY)                      # wide brim
    h.add(capsule((0, 1.668, -0.09), (0, 1.73, 0.0), 0.008), MDARK)                      # comb
    R.head(h)
    d = norm(P["spear"])
    arm(R, -1, P["grip"], TRENCH, TRENCH, SKIN)
    arm(R, 1, add(P["grip"], mul(d, P["fore"])), TRENCH, TRENCH, SKIN)
    g = Group("spear")
    back = add(P["grip"], mul(d, -0.55))
    tip = add(P["grip"], mul(d, 1.55))
    g.add(capsule(back, tip, 0.016), WOOD)
    g.add(box(add(tip, mul(d, 0.12)), (0.034, 0.008, 0.14), blade_basis(d), rnd=0.005), STEEL)  # spearhead
    g.add(capsule(add(tip, mul(d, -0.03)), add(tip, mul(d, 0.02)), 0.02), MDARK)          # socket
    R.world(g)


UNITS.update({
    # spear sloped forward / level thrust                            (goldenhorde footspear)
    "levy": dict(build=b_levy, poses={
        "1": dict(feet=FEET(0.06, -0.06, -0.04, 0.05), grip=W(-0.02, 0.98, 0.14), spear=aim(50), fore=0.4,
                  pole_r=(-1, -0.6, -0.2)),
        "2": dict(feet=FEET(0.26, -0.22, 0.02, 0.0), body=(0, -0.06, 0.03), lean=10, twist=-18,
                  grip=W(-0.1, 1.0, 0.1), spear=aim(2), fore=0.42, pole_r=(-1, -0.6, -0.2))}),
})


# ================================================================ sixth wave: arc apprentice
def b_arcapprentice(R):
    """Arc Apprentice: a young novice of the arc casters, hood down, indigo robe with a copper belt,
    a small capacitor pack and a single copper gauntlet on the casting hand."""
    P = R.P

    def robe(t):
        t.add(box((0, 0.99, 0), (0.15, 0.024, 0.104), rnd=0.02), COPPER)                 # copper belt
        t.add(box((0, 1.24, -0.14), (0.085, 0.1, 0.05), rnd=0.02), MECHD)                 # small pack
        t.add(torus((0, 1.24, -0.14), (0, 1, 0), 0.09, 0.012), COPPER)
        t.add(sphere((0, 1.36, -0.15), 0.024), G_SPARK)
    robe_body(R, NAVY, NAVY, skirt_to=0.12, extra=robe)
    h = Group("head")
    face(h, SKIN)
    hair_short(h, HAIR_BL)
    R.head(h)
    hd = Group("hood")
    hd.add(lumpy(ellipsoid((0, 1.47, -0.07), (0.13, 0.06, 0.1)), 0.006, 50), NAVY)       # hood down
    R.head(hd)

    def gauntlet(g, s, J):
        sh, elbow, wrist, d, hc = J
        g.add(limb(lerp(elbow, wrist, 0.35), wrist, 0.047, 0.045), COPPER)
        g.add(torus(lerp(elbow, wrist, 0.6), d, 0.05, 0.008), BOOT)
    arm(R, -1, P["hand_r"], NAVY, NAVY, SKIN)
    J = arm(R, 1, P["hand_l"], NAVY, NAVY, BOOT, extra=gauntlet, pole=P.get("pole_l"))
    c = Group("cable")
    sh, elbow, wrist, d, hc = J
    cable(c, [R.T((0.07, 1.26, -0.17)), add(R.T((0.19, 1.34, -0.1)), (0, 0.02, 0)), lerp(elbow, wrist, 0.4)],
          0.01, BOOT)
    R.world(c)
    z = Group("lightning")
    if P.get("cast"):
        lightning(z, add(hc, mul(SL, 0.03)), add(hc, mul(aim(P["bolt"]), 0.85)), seed=3, r=0.012, kinks=5,
                  amp=0.09, branches=1)
    else:
        z.add(sphere(add(hc, (0.0, 0.06, 0.0)), 0.032), G_SPARK)                          # spark in the palm
        bolt(z, add(hc, (0.0, 0.06, 0.0)), add(hc, (0.03, 0.17, 0.02)), G_SPARK, 0.009, 3, 0.025, seed=183)
        bolt(z, add(hc, (0.02, 0.0, 0.0)), add(hc, mul(SL, 0.08)), G_SPARK, 0.007, 3, 0.02, seed=185)
    R.world(z)


UNITS.update({
    # calm, palm up with a spark / one-handed bolt                  (like the arc adept)
    "arcapprentice": dict(build=b_arcapprentice, scale=0.97, poses={
        "1": dict(feet=FEET(0.06, -0.06, -0.04, 0.05), hand_r=W(-0.04, 0.92, 0.12), hand_l=W(0.3, 1.16, 0.22),
                  pole_l=(1, -0.6, 0.1)),
        "2": dict(feet=FEET(0.14, -0.1, -0.02, 0.05), lean=6, twist=-12, hand_r=W(0.0, 0.95, 0.1),
                  hand_l=W(0.5, 1.34, 0.12), pole_l=(1, -0.6, 0.1), cast=True, bolt=6, halo=True)}),
})
