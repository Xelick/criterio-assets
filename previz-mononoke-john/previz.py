"""Previz en Blender de los 29 planos del clip (4 s - 34 s) con John y Dark-John.

Uso: python previz.py kf.json salida_dir [frame_ini frame_fin]
Cada plano tiene una cámara base (posición, objetivo, lente) y encima el
movimiento extraído del clip: paneo, inclinación, zoom y giro, interpolados
cuadro a cuadro. Los cortes caen en el mismo cuadro que en el original.
"""
import json, math, os, sys
import bpy
from mathutils import Matrix, Vector

KF, OUT = sys.argv[1], sys.argv[2]
F0, F1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 749)
FPS, W, H = 25, 960, 402
SENSOR = 36.0

# ---------------------------------------------------------------- escena
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light, sh.color_type = "STUDIO", "OBJECT"
sh.show_shadows, sh.show_cavity, sh.show_object_outline = True, True, True
sc.display.shadow_focus = 0.6
sc.world = bpy.data.worlds.new("w")
sc.world.color = (0.035, 0.09, 0.09)
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"
sc.view_settings.exposure = 0.7

COL = {
    "suelo": (0.13, 0.17, 0.14), "mar": (0.08, 0.2, 0.42), "torii": (0.85, 0.22, 0.12),
    "rojo": (0.55, 0.03, 0.06), "abrigo": (0.75, 0.05, 0.08), "piel": (0.85, 0.66, 0.52),
    "pelo": (0.05, 0.04, 0.04), "lente": (0.02, 0.02, 0.02), "oro": (0.85, 0.65, 0.2),
    "azul": (0.1, 0.2, 0.9), "blanco": (0.92, 0.92, 0.9), "negro": (0.015, 0.015, 0.02),
    "cian": (0.1, 1.0, 1.0), "magenta": (1.0, 0.1, 0.8), "llama": (1.0, 0.35, 0.05),
    "acero": (0.65, 0.68, 0.72), "carta_n": (1.0, 0.45, 0.08), "carta_a": (0.15, 0.2, 0.95),
    "morado": (0.68, 0.35, 0.85), "funda": (0.04, 0.04, 0.04),
}


def mk(prim, name, col, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), parent=None, **kw):
    getattr(bpy.ops.mesh, "primitive_" + prim + "_add")(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object
    o.name, o.scale = name, scale
    o.color = (*COL[col], 1) if isinstance(col, str) else (*col, 1)
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None)
    sc.collection.objects.link(e)
    e.location = loc
    if parent:
        e.parent = parent
    return e


def humano(nombre, loc, yaw, c):
    """Maniquí mirando a +Y local. c: colores. Devuelve (raíz, pivote brazo derecho, mano)."""
    r = empty(nombre, loc)
    r.rotation_euler.z = yaw
    for x in (-0.1, 0.1):
        mk("cylinder", nombre + "_pierna", c["piel_baja"], (x, 0, 0.42), radius=0.08, depth=0.84, parent=r)
    mk("cylinder", nombre + "_torso", c["traje"], (0, 0, 1.13), scale=(1, 0.7, 1), radius=0.2, depth=0.6, parent=r)
    mk("cone", nombre + "_abrigo", c["abrigo"], (0, -0.02, 0.86), radius1=0.4, radius2=0.22, depth=1.15, parent=r)
    mk("uv_sphere", nombre + "_cabeza", c["piel"], (0, 0, 1.62), radius=0.12, parent=r)
    mk("cube", nombre + "_pelo", c["pelo"], (0, -0.05, 1.5), scale=(0.15, 0.06, 0.2), parent=r)
    mk("uv_sphere", nombre + "_pelo2", c["pelo"], (0, -0.015, 1.66), scale=(1.1, 1.05, 1.0), radius=0.125, parent=r)
    for x in (-0.045, 0.045):
        mk("torus", nombre + "_lente", c["lente"], (x, 0.11, 1.64), (math.pi / 2, 0, 0),
           major_radius=0.028, minor_radius=0.007, parent=r)
        mk("cylinder", nombre + "_cristal", c["cristal"], (x, 0.112, 1.64), (math.pi / 2, 0, 0),
           radius=0.025, depth=0.004, parent=r)
    mk("cube", nombre + "_mono", c["mono"], (0, 0.14, 1.43), scale=(0.05, 0.015, 0.022), parent=r)
    mk("cylinder", nombre + "_brazoL", c["abrigo"], (-0.27, 0, 1.12), radius=0.055, depth=0.6, parent=r)
    piv = empty(nombre + "_hombroR", (0.27, 0, 1.42), r)
    mk("cylinder", nombre + "_brazoR", c["abrigo"], (0, 0, -0.3), radius=0.055, depth=0.6, parent=piv)
    mano = empty(nombre + "_mano", (0, 0, -0.62), piv)
    return r, piv, mano


def visible(o, on_frames):
    """on_frames: lista de (ini, fin) en cuadros de video (0-based) donde se ve."""
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=0)
    for a, b in on_frames:
        o.hide_render = False
        o.keyframe_insert("hide_render", frame=a)
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=b + 1)
    for fc in (o.animation_data.action.fcurves if o.animation_data else []):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT"


def visible_tree(o, on):
    visible(o, on)
    for ch in o.children_recursive:
        visible(ch, on)


# ---------------------------------------------------------------- decorado
mk("plane", "suelo", "suelo", (0, 0, 0), size=400)
mk("plane", "mar", "mar", (0, 140, -0.02), size=240)
for x in (-4.2, 4.2):
    mk("cylinder", "torii_pilar", "torii", (x, 30, 4.5), radius=0.45, depth=9)
mk("cube", "torii_kasagi", "torii", (0, 30, 9.3), scale=(6.2, 0.6, 0.35))
mk("cube", "torii_kasagi_n", "negro", (0, 30, 9.75), scale=(6.6, 0.65, 0.12))
mk("cube", "torii_nuki", "torii", (0, 30, 7.4), scale=(5.0, 0.3, 0.25))
for i, (x, y) in enumerate([(-14, 40), (12, 44), (-6, 55), (20, 60), (-22, 58)]):
    mk("cone", "ola", "azul", (x, y, 0.6), radius1=3.5, radius2=0, depth=1.6)
# círculo ritual bajo John y bajo Dark-John
for cx, cy in ((0, 0), (0, 6)):
    for rr, cc in ((1.6, "rojo"), (2.0, "blanco"), (2.4, "rojo"), (2.8, "blanco")):
        mk("torus", "anillo", cc, (cx, cy, 0.02), major_radius=rr, minor_radius=0.06)

# muro de cartas talismán (aparece con Dark-John)
cartas = empty("cartas", (0, 10.5, 0))
for i in range(14):
    for j in range(6):
        x, z = -6.0 + i * 0.92, 0.7 + j * 1.15
        col = "carta_n" if (i + j) % 3 else "carta_a"
        c = mk("cube", "carta", col, (x, (i % 2) * 0.25, z), (0, (i - 7) * 0.02, 0), (0.38, 0.02, 0.5), parent=cartas)
        mk("torus", "ojo", "oro" if col == "carta_n" else "cian", (x, -0.03 + (i % 2) * 0.25, z),
           (math.pi / 2, 0, 0), major_radius=0.13, minor_radius=0.025, parent=cartas)
carta_sola = mk("cube", "carta_sola", "carta_n", (0.9, 0.9, 1.6), (0, 0.15, 0.3), (0.19, 0.01, 0.27))
mk("torus", "carta_sola_ojo", "oro", (0.9, 0.88, 1.6), (math.pi / 2, 0, 0.3), major_radius=0.07,
   minor_radius=0.012, parent=None)
# esfera morada y tentáculo
orbe = mk("uv_sphere", "orbe", "morado", (2.8, 9.0, 3.4), radius=1.0)
bpy.ops.curve.primitive_bezier_curve_add(location=(0, 0, 0))
tent = bpy.context.active_object
tent.name = "tentaculo"
sp = tent.data.splines[0]
sp.bezier_points[0].co, sp.bezier_points[0].handle_right = (2.8, 9.0, 3.4), (1.0, 7.0, 4.5)
sp.bezier_points[1].co, sp.bezier_points[1].handle_left = (-4.0, 4.0, 1.5), (-1.0, 6.0, 3.0)
tent.data.bevel_depth = 0.18
tent.color = (*COL["morado"], 1)
# estallido radial (plano 20) y mandala (plano 21)
burst = empty("estallido", (0, 6, 1.5))
for k in range(16):
    a = k / 16 * 2 * math.pi
    mk("cone", "rayo", "llama" if k % 2 else "magenta", (math.cos(a) * 1.6, -0.4, math.sin(a) * 1.6),
       (0, -a + math.pi / 2, 0), (1, 1, 1), parent=burst, radius1=0.12, radius2=0, depth=2.6)
mandala = empty("mandala", (0, 6, 3.2))
for rr, cc in ((0.6, "blanco"), (1.0, "rojo"), (1.4, "blanco"), (1.8, "rojo")):
    mk("torus", "mandala_anillo", cc, (0, 0, 0), (math.pi / 2, 0, 0), parent=mandala, major_radius=rr, minor_radius=0.07)
mk("cylinder", "mandala_estrella", "oro", (0, 0, 0), (math.pi / 2, 0, 0), parent=mandala, vertices=8, radius=0.45, depth=0.05)

# ---------------------------------------------------------------- personajes
CJ = {"piel_baja": "negro", "traje": "rojo", "abrigo": "abrigo", "piel": "piel", "pelo": "pelo",
      "lente": "oro", "cristal": "lente", "mono": "azul"}
CD = {"piel_baja": "negro", "traje": "negro", "abrigo": (0.03, 0.01, 0.05), "piel": "negro", "pelo": "negro",
      "lente": "magenta", "cristal": "cian", "mono": "magenta"}
john, j_hombro, j_mano = humano("John", (0, 0, 0), 0.0, CJ)
# cinco Dark-John: aparecen juntos en el giro y atacan de a uno
DJ_POS = [(0, 5.5), (-2.2, 5.0), (2.2, 5.0), (2.6, 7.8), (-0.6, 8.2)]
DJ_ESC = [1.0, 1.0, 1.0, 1.0, 1.3]  # el quinto es el más grande
DJS = []
for i, (x, y) in enumerate(DJ_POS):
    r, h, _ = humano(f"DarkJohn{i + 1}", (x, y, 0), 0.0, CD)
    mk("torus", "aura_dark", "magenta", (0, 0, 0.05), major_radius=0.8, minor_radius=0.04, parent=r)
    mk("torus", "aura_dark2", "cian", (0, 0, 0.9), major_radius=0.55, minor_radius=0.02, parent=r)
    DJS.append((r, h, DJ_ESC[i]))
aura_j = mk("torus", "aura_john", "llama", (0, 0, 0.05), major_radius=0.8, minor_radius=0.04, parent=john)

# funda en la cadera izquierda y empuñadura enfundada
funda = empty("funda", (-0.37, 0.1, 1.0), john)
funda.rotation_euler = (math.radians(-60), 0, 0)
mk("cube", "saya", "funda", (0, -0.45, 0), scale=(0.025, 0.45, 0.035), parent=funda)
hilt_enf = empty("empunadura_enfundada", (0, 0.02, 0), funda)
mk("cylinder", "tsuba", "oro", (0, 0.02, 0), (math.pi / 2, 0, 0), radius=0.06, depth=0.015, parent=hilt_enf)
mk("cube", "tsuka", "rojo", (0, 0.16, 0), scale=(0.02, 0.13, 0.022), parent=hilt_enf)

# espadas en la mano (eje -Z local de la mano = hacia donde apunta el brazo)
katana = empty("katana", (0, 0, 0), j_mano)
mk("cube", "k_tsuka", "rojo", (0, 0, 0), scale=(0.022, 0.022, 0.13), parent=katana)
mk("cylinder", "k_tsuba", "oro", (0, 0, -0.14), radius=0.06, depth=0.015, parent=katana)
mk("cube", "k_hoja", "acero", (0, 0, -0.62), scale=(0.008, 0.03, 0.48), parent=katana)
llama = empty("espada_llama", (0, 0, 0), j_mano)
mk("cube", "l_tsuka", "rojo", (0, 0, 0), scale=(0.025, 0.025, 0.15), parent=llama)
mk("uv_sphere", "l_boca", "oro", (0, 0, 0.17), radius=0.045, parent=llama)
mk("cylinder", "l_tsuba", "oro", (0, 0, -0.16), radius=0.08, depth=0.02, parent=llama)
mk("cube", "l_hoja", "negro", (0, 0, -1.3), scale=(0.012, 0.09, 1.12), parent=llama)
mk("cube", "l_runa", "llama", (0, 0.0, -1.3), scale=(0.016, 0.02, 1.0), parent=llama)
for k in range(9):
    s = 1 if k % 2 else -1
    mk("cone", "l_pua", "negro", (0, s * 0.13, -0.4 - k * 0.24), (s * math.radians(-35), 0, 0),
       parent=llama, radius1=0.05, radius2=0, depth=0.22)

# ---------------------------------------------------------------- planos
def plano(n):
    return SH[n - 1]


SH = json.load(open(KF))  # [shot, f_in, f_out, [x,y,z,r] x5]
# cámara base de cada plano: (posición, objetivo, lente mm)
BASE = {
    1: ((0, -16, 2.6), (0, 22, 4.0), 28),        # general: torii y mar, John pequeño
    2: ((0.7, 1.5, 1.66), (0, 0, 1.62), 50),     # plano medio corto de John
    3: ((0.35, 1.0, 1.2), (-0.33, 0.2, 1.05), 50),  # manos sobre la empuñadura
    4: ((-0.9, 0.85, 1.3), (-0.33, 0.2, 1.05), 50),
    5: ((0.0, 0.62, 1.65), (0, 0, 1.64), 60),    # primerísimo plano: ojos
    6: ((0.2, 0.85, 1.05), (-0.33, 0.2, 1.05), 60),
    7: ((7, -9, 1.6), (0, 30, 5), 35),           # general torii y olas
    8: ((0.9, 1.75, 1.62), (0.9, 0.9, 1.6), 50), # carta talismán
    9: ((0, 0.01, 12), (0, 0, 0), 35),           # cenital
    10: ((0.22, 0.65, 1.67), (0, 0, 1.64), 70),
    11: ((-10, -12, 6), (0, 10, 3), 28),
    12: ((0, 6.5, 1.4), (0, 0, 1.1), 40),        # John de pie (desde el lado de Dark-John)
    13: ((0.9, 1.3, 1.35), (0.27, 0.6, 1.4), 35),  # barrido a lo largo de la hoja: desenvaina
    14: ((-2.2, -2.5, 2.6), (1.0, 9.0, 3.0), 35),  # muro de cartas + esfera: aparece el dominio
    15: ((2.5, -2.0, 1.2), (0, 4.0, 2.0), 35),    # giro de cámara 1: aparece Dark-John
    16: ((0, 0.01, 4.5), (0, 0, 0), 28),          # destello: anillos
    17: ((-2.5, 1.0, 0.8), (0, 5.0, 2.5), 35),    # giro de cámara 2
    18: ((0.3, 2.4, 1.7), (0, 0, 1.55), 40),      # revelación: John con la espada grande
    19: ((0.25, 1.0, 1.7), (0, 0, 1.64), 60),
    20: ((0, 1.5, 1.8), (0, 6, 1.6), 35),         # estallido sobre Dark-John
    21: ((0, 2.0, 3.2), (0, 6, 3.2), 35),         # mandala
    22: ((9, 3, 1.6), (0, 3, 1.2), 35),           # general lateral: John vs Dark-John
    23: ((1.1, 1.2, 1.45), (0.3, 0.5, 1.35), 50), # brazo cortando
    24: ((0.6, 0.9, 0.35), (0, 0.2, 0.2), 50),
    25: ((0.4, -2.0, 1.6), (0, 6, 1.4), 35),      # sobre Dark-John, zoom de golpe
    26: ((0.2, 1.1, 1.35), (0, 0, 1.5), 50),
    27: ((0, 3.0, 1.45), (0, 0, 1.3), 50),
    28: ((-1.5, 1.5, 2.4), (2.8, 9.0, 3.4), 40),  # esfera + mano
    29: ((3.2, -1.5, 1.2), (0, 3, 1.4), 35),      # corte final
}

cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.sensor_fit, cam.data.sensor_width = "HORIZONTAL", SENSOR
cam.rotation_mode = "QUATERNION"


def interp(pts, t):
    """pts: 5 valores en t = 0, .25, .5, .75, 1. Catmull-Rom monótona por tramos."""
    xs = [0, 0.25, 0.5, 0.75, 1.0]
    i = min(int(t / 0.25), 3)
    u = (t - xs[i]) / 0.25
    p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, 4)]
    m1, m2 = (p2 - p0) / 2, (p3 - p1) / 2
    h00, h10, h01, h11 = 2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2
    return h00 * p1 + h10 * m1 + h01 * p2 + h11 * m2


for s in SH:
    n, a, b, pts = s[0], s[1], s[2], s[3:]
    L, T, f0 = BASE[n]
    L, T = Vector(L), Vector(T)
    base = (T - L).to_track_quat("-Z", "Y").to_matrix().to_4x4()
    hfov = 2 * math.atan(SENSOR / 2 / f0)
    vfov = 2 * math.atan(SENSOR * H / W / 2 / f0)
    for f in range(a, b + 1):
        t = 0 if b == a else (f - a) / (b - a)
        dx, dy, z, r = (interp([p[k] for p in pts], t) for k in range(4))
        rot = base @ Matrix.Rotation(dx * hfov, 4, "Y") @ Matrix.Rotation(dy * vfov, 4, "X") \
            @ Matrix.Rotation(math.radians(r), 4, "Z")
        cam.location = L
        cam.rotation_quaternion = rot.to_quaternion()
        cam.data.lens = f0 * max(z, 0.2)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_quaternion", frame=f)
        cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- acción
def fr(n, q=0.0):
    a, b = plano(n)[1], plano(n)[2]
    return round(a + (b - a) * q)


def key_rot(o, f, eul):
    o.rotation_euler = eul
    o.keyframe_insert("rotation_euler", frame=f)


def apunta(v):
    """Rotación que lleva el brazo (-Z local) hacia el vector v (en el espacio de John)."""
    return Vector((0, 0, -1)).rotation_difference(Vector(v).normalized()).to_euler()


abajo, a_empunadura = (0, 0, 0), apunta((-0.63, 0.2, -0.34))
guardia = apunta((0.7, 0.35, 0.55))
al_frente, en_alto = apunta((0, 1, 0.15)), apunta((0.1, 0.25, 1))
key_rot(j_hombro, 0, abajo)
key_rot(j_hombro, fr(2, 0.5), abajo)
key_rot(j_hombro, fr(3), a_empunadura)            # mano a la empuñadura
key_rot(j_hombro, fr(12, 1), a_empunadura)
key_rot(j_hombro, fr(13), apunta((-0.3, 0.6, -0.2)))
key_rot(j_hombro, fr(13, 1), al_frente)            # desenvaina en el barrido

# la espada: enfundada hasta el plano 13, katana la primera mitad del barrido,
# a mitad del plano 13 se transforma en la espada de llama (mucho más grande)
visible_tree(hilt_enf, [(0, fr(13) - 1)])
visible_tree(katana, [(fr(13), fr(13, 0.45))])
visible_tree(llama, [(fr(13, 0.45) + 1, 749)])
visible(aura_j, [(fr(13, 0.45) + 1, 749)])
# el dominio de cartas y la esfera llegan con Dark-John
visible_tree(cartas, [(fr(14), 749)])
visible_tree(burst, [(fr(20), fr(20, 1))])
visible_tree(mandala, [(fr(21), fr(21, 1))])
visible(carta_sola, [(fr(8), fr(8, 1))])
visible(bpy.data.objects["carta_sola_ojo"], [(fr(8), fr(8, 1))])


# ---------------------------------------------------------------- pelea (16 s - 30 s)
import random
random.seed(7)


def mira(x, y, tx=0.0, ty=0.0):
    """Giro en Z para que el +Y local mire desde (x, y) hacia (tx, ty)."""
    return math.atan2(-(tx - x), ty - y)


def pose(o, f, x, y, z=0.0, yaw=None):
    o.location = (x, y, z)
    o.keyframe_insert("location", frame=f)
    o.rotation_euler = (0, 0, mira(x, y) if yaw is None else yaw)
    o.keyframe_insert("rotation_euler", frame=f)


def acecha(dj, f0, f1, x, y, amp=0.15):
    """Los que esperan no se quedan quietos: se balancean y amagan."""
    for j, f in enumerate(range(f0, f1, 6)):
        pose(dj[0], f, x + (amp if j % 2 else -amp), y, 0.06 if j % 2 else 0.0)


def estalla(nombre, pos, k, cols=("negro", "cian", "magenta"), n=16, dur=10, tam=0.06):
    """Escamas que salen volando: muerte de un Dark-John o chispas de un choque."""
    e = empty(nombre, pos)
    for j in range(n):
        d = Vector((random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-0.6, 1))).normalized()
        a = random.random() * 3
        mk("cube", nombre + "_e", cols[j % len(cols)], tuple(d * random.uniform(0.15, 0.35)), (a, a, a),
           (tam, tam, tam), parent=e)
    visible_tree(e, [(k, k + dur)])
    e.scale = (0.4, 0.4, 0.4)
    e.keyframe_insert("scale", frame=k)
    e.scale = (3.2, 3.2, 3.2)
    e.keyframe_insert("scale", frame=k + dur)


def muere(i, k, pos):
    r, h, s = DJS[i]
    r.scale = (s, s, s)
    r.keyframe_insert("scale", frame=k - 1)
    r.scale = (0.01, 0.01, 0.01)
    r.keyframe_insert("scale", frame=k + 2)
    estalla(f"muerte{i + 1}", pos, k)


bloque = apunta((-0.2, 0.5, 0.8))
garras_arriba, zarpazo = apunta((0.2, 1, 0.7)), apunta((0.5, 1, -0.2))
K1, K2, K3, K4, K5 = 522, 590, 609, 664, 718   # 20.9 / 23.6 / 24.4 / 26.6 / 28.7 s

# los cinco se forman en el giro (plano 15) uno tras otro y crecen hasta su tamaño
for i, (r, h, s) in enumerate(DJS):
    r.scale = (0.05, 0.05, 0.05)
    r.keyframe_insert("scale", frame=400 + 2 * i)
    r.scale = (s, s, s)
    r.keyframe_insert("scale", frame=412 + 2 * i)
    pose(r, 400, *DJ_POS[i])
    key_rot(h, 400, apunta((0, 0.4, -1)))
    key_rot(h, 430, garras_arriba)
visible_tree(DJS[0][0], [(400, K1 + 2)])
visible_tree(DJS[1][0], [(400, K2 + 2)])
visible_tree(DJS[2][0], [(400, K3 + 2)])
visible_tree(DJS[3][0], [(400, 640)])
visible_tree(DJS[4][0], [(400, K5 + 2)])
for i in range(5):
    acecha(DJS[i], 416 + 2 * i, 490, *DJ_POS[i])

# John: base en el centro del círculo
pose(john, 0, 0, 0, yaw=0)
pose(john, 459, 0, 0, yaw=0)

# DJ1: corre hacia John, dos zarpazos (bloqueo y esquiva), cae con el contracorte
d1, h1 = DJS[0][0], DJS[0][1]
pose(d1, 490, 0, 5.5)
pose(d1, 506, 0.1, 1.3)
key_rot(h1, 506, garras_arriba)
key_rot(h1, 510, zarpazo)
key_rot(h1, 513, garras_arriba)
key_rot(h1, 516, apunta((-0.4, 1, -0.1)))
pose(d1, 518, 0.25, 0.9)
estalla("choque1", (0.08, 0.75, 1.45), 510, ("llama", "oro"), n=10, dur=5, tam=0.03)
muere(0, K1, (0.25, 0.9, 1.0))
# DJ2 y DJ3 rodean por los flancos mientras pelea el primero
d2, h2 = DJS[1][0], DJS[1][1]
pose(d2, 490, -2.2, 5.0)
pose(d2, 498, -2.6, 4.2)
pose(d2, 506, -2.6, 3.0)
acecha(DJS[1], 512, 545, -2.6, 3.0, 0.12)
d3, h3 = DJS[2][0], DJS[2][1]
pose(d3, 490, 2.2, 5.0)
pose(d3, 498, 2.6, 4.2)
pose(d3, 506, 2.6, 3.0)
acecha(DJS[2], 512, 597, 2.6, 3.0, 0.12)
acecha(DJS[3], 490, 615, *DJ_POS[3])
acecha(DJS[4], 490, 672, *DJ_POS[4])
# DJ2: carga (zoom de golpe), sus garras chocan contra la barrera, cae con el corte horizontal
pose(d2, 545, -2.6, 3.0)
key_rot(h2, 556, garras_arriba)
pose(d2, 564, -0.75, 0.95)
for j, f in enumerate(range(566, 586, 3)):
    pose(d2, f, -0.72 + (0.04 if j % 2 else 0), 0.92)
    key_rot(h2, f, zarpazo if j % 2 else garras_arriba)
barrera = mk("cylinder", "barrera", "abrigo", (-0.4, 0.5, 1.35), (math.pi / 2, 0, math.radians(38)), radius=0.38, depth=0.02)
mk("torus", "barrera_aro", "oro", (-0.4, 0.5, 1.35), (math.pi / 2, 0, math.radians(38)), major_radius=0.38, minor_radius=0.02)
visible(barrera, [(564, 586)])
visible(bpy.data.objects["barrera_aro"], [(564, 586)])
muere(1, K2, (-0.7, 0.9, 1.0))
# DJ3: salta desde la derecha y lo parte en el aire un corte ascendente
pose(d3, 597, 2.6, 3.0, -0.15)
key_rot(h3, 597, garras_arriba)
pose(d3, 603, 1.6, 1.8, 1.2)
pose(d3, 607, 0.8, 1.0, 0.9)
key_rot(h3, 605, zarpazo)
muere(2, K3, (0.75, 0.95, 1.6))
# DJ4: se funde con la esfera; el tentáculo azota hacia John, él lo corta y la esfera implota
d4 = DJS[3][0]
pose(d4, 615, 2.6, 7.8)
pose(d4, 635, 2.8, 9.0, 2.4)
d4.scale = (1, 1, 1)
d4.keyframe_insert("scale", frame=632)
d4.scale = (0.3, 0.3, 0.3)
d4.keyframe_insert("scale", frame=640)
pt = tent.data.splines[0].bezier_points
for b in pt:
    b.handle_left_type = b.handle_right_type = "AUTO"
pt[1].co = (-4.0, 4.0, 1.5)
pt[1].keyframe_insert("co", frame=635)
pt[1].co = (0.4, 0.9, 1.4)
pt[1].keyframe_insert("co", frame=650)
visible(tent, [(fr(14), 652)])
orbe.scale = (1, 1, 1)
orbe.keyframe_insert("scale", frame=652)
orbe.scale = (1.35, 1.35, 1.35)
orbe.keyframe_insert("scale", frame=658)
orbe.scale = (0.02, 0.02, 0.02)
orbe.keyframe_insert("scale", frame=K4)
visible(orbe, [(fr(14), K4)])
estalla("muerte4", (2.8, 9.0, 3.4), K4, n=24, dur=14, tam=0.12)
# DJ5, el más grande: duelo final; bloqueo, agachada, giro de 360° y corte final
d5, h5 = DJS[4][0], DJS[4][1]
pose(d5, 672, -0.6, 8.2)
pose(d5, 690, 0.0, 2.6)
key_rot(h5, 688, garras_arriba)
key_rot(h5, 693, zarpazo)
key_rot(h5, 697, garras_arriba)
key_rot(h5, 700, apunta((-1, 0.6, 0)))
pose(d5, 712, 0.0, 1.9)
estalla("choque5", (0.0, 1.3, 1.65), 693, ("llama", "oro"), n=10, dur=5, tam=0.03)
muere(4, K5, (0.0, 1.9, 1.3))

# John: se mueve con cada atacante (pasos, giros, agachada y giro completo)
for f, x, y, z, yaw in [
    (506, 0, 0, 0, 0), (510, 0, -0.1, 0, 0), (516, -0.2, 0, 0, 0.15), (521, 0.1, 0.3, 0, -0.1),
    (535, 0, 0.1, 0, 0.7), (566, 0, 0.1, 0, 0.72), (588, -0.1, 0.2, 0, 0.75),
    (597, 0, 0.15, 0, -0.7), (609, 0.15, 0.25, 0, -0.7), (640, 0.1, 0.3, 0, -0.3), (653, 0.1, 0.4, 0, -0.3),
    (672, 0, 0.2, 0, 0), (693, 0, 0.1, 0, 0), (700, 0, 0.15, -0.3, 0), (704, 0, 0.2, 0, 0),
    (714, 0, 0.35, 0, -2 * math.pi), (718, 0, 0.45, 0, -2 * math.pi), (749, 0, 0.45, 0, -2 * math.pi)]:
    pose(john, f, x, y, z, yaw)
for f, rot in [
    (427, guardia), (459, guardia), (500, guardia), (510, bloque), (514, guardia), (518, en_alto),
    (522, apunta((0.4, 1, -0.6))), (530, guardia), (566, guardia), (582, apunta((0.9, 0.1, 0.5))),
    (590, apunta((-0.7, 1, -0.1))), (600, apunta((0.4, 0.3, -0.9))), (609, apunta((0.1, 0.7, 1.0))),
    (640, guardia), (648, en_alto), (653, apunta((0.3, 1, -0.5))), (672, guardia), (693, bloque),
    (697, guardia), (700, apunta((0.9, 0.4, 0.0))), (714, en_alto), (718, apunta((-0.5, 1, -0.7))),
    (749, apunta((-0.5, 1, -0.7)))]:
    key_rot(j_hombro, f, rot)

# ---------------------------------------------------------------- render
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "previz_mononoke_john.blend"))
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
FR = [(s[1] + s[2]) // 2 for s in SH] if os.environ.get("MIDS") else range(F0, F1 + 1)
if os.environ.get("FRAMES"):
    FR = [int(x) for x in os.environ["FRAMES"].split(",")]
for f in FR:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(OUT, "frames", f"{f:04d}.png")
    bpy.ops.render.render(write_still=True)
