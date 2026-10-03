"""Previz en un solo plano (30 s, sin cortes): John contra seis Dark-John, cuerpo a cuerpo.

Uso: python previz_onetake.py salida_dir [frame_ini frame_fin]
Variables: RES=0.5 baja la resolución; FRAMES=a,b,c renderiza solo esos cuadros;
NORENDER=1 solo arma la escena, guarda los .blend y revisa el encuadre.
BLOQUES=1 cambia los maniquíes por figuras rígidas de caja y esfera y quita la utilería.

La pelea sigue la lógica de "HERO VS SIX WHITE NINJA": John avanza por un pasillo de
cartas talismán hacia el torii; los Dark-John le salen al paso de a uno y él los
derriba de cerca (barrida, codo, rodilla, patada) y los remata con la espada de llama.
La cámara sigue a John en un solo recorrido continuo, con aceleraciones y pausas.
Después de cada etapa se guarda una copia del .blend.
"""
import math, os, random, sys
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

OUT = sys.argv[1]
F0, F1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 749)
FPS, SENSOR = 25, 36.0
RES = float(os.environ.get("RES", "1"))
W, H = round(1260 * RES) // 2 * 2, round(540 * RES) // 2 * 2
os.makedirs(OUT, exist_ok=True)
random.seed(11)


def T(s):
    return round(s * FPS)


def respaldo(etapa):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"previz_onetake_{etapa}.blend"), compress=True)


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
sc.display.render_aa = "FXAA"
sc.world = bpy.data.worlds.new("w")
sc.world.color = (0.035, 0.09, 0.09)
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"
sc.view_settings.exposure = 0.7
sc.frame_start, sc.frame_end = 0, 749

COL = {
    "suelo": (0.13, 0.17, 0.14), "mar": (0.08, 0.2, 0.42), "torii": (0.85, 0.22, 0.12),
    "rojo": (0.55, 0.03, 0.06), "abrigo": (0.75, 0.05, 0.08), "piel": (0.85, 0.66, 0.52),
    "pelo": (0.05, 0.04, 0.04), "lente": (0.02, 0.02, 0.02), "oro": (0.85, 0.65, 0.2),
    "azul": (0.1, 0.2, 0.9), "blanco": (0.92, 0.92, 0.9), "negro": (0.015, 0.015, 0.02),
    "cian": (0.1, 1.0, 1.0), "magenta": (1.0, 0.1, 0.8), "llama": (1.0, 0.35, 0.05),
    "acero": (0.65, 0.68, 0.72), "carta_n": (1.0, 0.45, 0.08), "carta_a": (0.15, 0.2, 0.95),
    "morado": (0.68, 0.35, 0.85), "funda": (0.04, 0.04, 0.04), "piedra": (0.32, 0.33, 0.3),
    "madera": (0.3, 0.16, 0.08), "teja": (0.12, 0.13, 0.15), "violeta": (0.5, 0.15, 1.0),
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


def visible(o, on_frames):
    """on_frames: lista de (ini, fin) en cuadros donde se ve."""
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=-30)
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


# patio de piedra que termina en el mar; el torii está en el borde (y = 20)
TORII_Y = 20.0
mk("plane", "suelo", "suelo", (0, -7.5, 0), scale=(100, 30, 1))
mk("plane", "mar", "mar", (0, 222.5, -0.4), scale=(200, 200, 1))
for x, y in [(-14, 40), (12, 44), (-6, 55), (20, 60), (-22, 58), (4, 34), (-9, 31)]:
    mk("cone", "ola", "azul", (x, y, 0.2), radius1=3.5, radius2=0, depth=1.2)
for x in (-3.0, 3.0):
    mk("cylinder", "torii_pilar", "torii", (x, TORII_Y, 3.0), radius=0.32, depth=6.0)
    mk("cylinder", "torii_base", "negro", (x, TORII_Y, 0.25), radius=0.42, depth=0.5)
mk("cube", "torii_kasagi", "torii", (0, TORII_Y, 6.2), scale=(4.4, 0.42, 0.25))
mk("cube", "torii_kasagi_n", "negro", (0, TORII_Y, 6.55), scale=(4.7, 0.46, 0.1))
mk("cube", "torii_nuki", "torii", (0, TORII_Y, 5.0), scale=(3.6, 0.2, 0.18))
# santuario detrás del punto de partida, faroles de piedra a los lados del camino
mk("cube", "haiden", "madera", (0, -19, 1.8), scale=(5, 3, 1.8))
mk("cone", "haiden_techo", "teja", (0, -19, 4.8), (0, 0, math.pi / 4), (1, 0.62, 1), vertices=4,
   radius1=8.5, radius2=0, depth=2.6)
for y in (-14, -10, -6):
    for x in (-2.6, 2.6):
        mk("cylinder", "farol", "piedra", (x, y, 0.6), radius=0.12, depth=1.2)
        mk("cube", "farol_caja", "piedra", (x, y, 1.35), scale=(0.25, 0.25, 0.22))
# círculos rituales: donde espera John y donde aterriza el último Dark-John
for cx, cy in ((0, 0), (0, 14.6)):
    for rr, cc in ((1.6, "rojo"), (2.0, "blanco"), (2.4, "rojo"), (2.8, "blanco")):
        mk("torus", "anillo", cc, (cx, cy, 0.02), major_radius=rr, minor_radius=0.06)

# pasillo de cartas talismán: dos muros flotantes a los lados del camino
muros = []
for lado in (-1, 1):
    m = empty("cartas_" + ("izq" if lado < 0 else "der"), (lado * 4.8, 0, 0))
    for i in range(20):
        for j in range(5):
            y, z = -1.0 + i * 0.92, 0.7 + j * 1.15
            col = "carta_n" if (i + j) % 3 else "carta_a"
            mk("cube", "carta", col, ((i % 2) * 0.25 * lado, y, z), (0, 0, math.pi / 2 + (i - 10) * 0.02),
               (0.38, 0.02, 0.5), parent=m)
            mk("torus", "ojo", "oro" if col == "carta_n" else "cian", ((i % 2) * 0.25 * lado - 0.03 * lado, y, z),
               (math.pi / 2, 0, math.pi / 2), major_radius=0.13, minor_radius=0.025, parent=m)
    muros.append(m)
orbe = mk("uv_sphere", "orbe", "morado", (3.9, 12.0, 5.2), radius=0.9)
respaldo("01_escena")

# ---------------------------------------------------------------- personajes
CJ = {"piel_baja": "negro", "traje": "rojo", "abrigo": "abrigo", "piel": "piel", "pelo": "pelo",
      "lente": "oro", "cristal": "lente", "mono": "azul"}
CD = {"piel_baja": "negro", "traje": "negro", "abrigo": (0.03, 0.01, 0.05), "piel": "negro", "pelo": "negro",
      "lente": "magenta", "cristal": "cian", "mono": "magenta"}


def humano(nombre, loc, c):
    """Maniquí mirando a +Y local, con caderas y hombros articulados."""
    r = empty(nombre, loc)
    pier = []
    for x in (-0.1, 0.1):
        cad = empty(nombre + "_cadera", (x, 0, 0.84), r)
        mk("cylinder", nombre + "_pierna", c["piel_baja"], (0, 0, -0.42), radius=0.08, depth=0.84, parent=cad)
        pier.append(cad)
    mk("cylinder", nombre + "_torso", c["traje"], (0, 0, 1.13), scale=(1, 0.7, 1), radius=0.2, depth=0.6, parent=r)
    mk("cone", nombre + "_abrigo", c["abrigo"], (0, -0.02, 0.9), radius1=0.36, radius2=0.22, depth=1.05, parent=r)
    mk("uv_sphere", nombre + "_cabeza", c["piel"], (0, 0, 1.62), radius=0.12, parent=r)
    mk("cube", nombre + "_pelo", c["pelo"], (0, -0.05, 1.5), scale=(0.15, 0.06, 0.2), parent=r)
    mk("uv_sphere", nombre + "_pelo2", c["pelo"], (0, -0.015, 1.66), scale=(1.1, 1.05, 1.0), radius=0.125, parent=r)
    for x in (-0.045, 0.045):
        mk("torus", nombre + "_lente", c["lente"], (x, 0.11, 1.64), (math.pi / 2, 0, 0),
           major_radius=0.028, minor_radius=0.007, parent=r)
        mk("cylinder", nombre + "_cristal", c["cristal"], (x, 0.112, 1.64), (math.pi / 2, 0, 0),
           radius=0.025, depth=0.004, parent=r)
    mk("cube", nombre + "_mono", c["mono"], (0, 0.14, 1.43), scale=(0.05, 0.015, 0.022), parent=r)
    hom = []
    for x in (-0.27, 0.27):
        piv = empty(nombre + "_hombro", (x, 0, 1.42), r)
        mk("cylinder", nombre + "_brazo", c["abrigo"], (0, 0, -0.3), radius=0.055, depth=0.6, parent=piv)
        hom.append(piv)
    mano = empty(nombre + "_mano", (0, 0, -0.62), hom[1])
    return {"r": r, "hL": hom[0], "hR": hom[1], "mano": mano, "pL": pier[0], "pR": pier[1]}


J = humano("John", (0, 0, 0), CJ)
aura_j = mk("torus", "aura_john", "llama", (0, 0, 0.05), major_radius=0.8, minor_radius=0.04, parent=J["r"])
# funda en la cadera izquierda y empuñadura enfundada
funda = empty("funda", (-0.37, 0.1, 1.0), J["r"])
funda.rotation_euler = (math.radians(-60), 0, 0)
mk("cube", "saya", "funda", (0, -0.45, 0), scale=(0.025, 0.45, 0.035), parent=funda)
hilt_enf = empty("empunadura_enfundada", (0, 0.02, 0), funda)
mk("cylinder", "tsuba", "oro", (0, 0.02, 0), (math.pi / 2, 0, 0), radius=0.06, depth=0.015, parent=hilt_enf)
mk("cube", "tsuka", "rojo", (0, 0.16, 0), scale=(0.02, 0.13, 0.022), parent=hilt_enf)
# katana y espada de llama en la mano (eje -Z local de la mano = hacia donde apunta el brazo)
katana = empty("katana", (0, 0, 0), J["mano"])
mk("cube", "k_tsuka", "rojo", (0, 0, 0), scale=(0.022, 0.022, 0.13), parent=katana)
mk("cylinder", "k_tsuba", "oro", (0, 0, -0.14), radius=0.06, depth=0.015, parent=katana)
mk("cube", "k_hoja", "acero", (0, 0, -0.62), scale=(0.008, 0.03, 0.48), parent=katana)
llama = empty("espada_llama", (0, 0, 0), J["mano"])
mk("cube", "l_tsuka", "rojo", (0, 0, 0), scale=(0.025, 0.025, 0.15), parent=llama)
mk("uv_sphere", "l_boca", "oro", (0, 0, 0.17), radius=0.045, parent=llama)
mk("cylinder", "l_tsuba", "oro", (0, 0, -0.16), radius=0.08, depth=0.02, parent=llama)
mk("cube", "l_hoja", "negro", (0, 0, -1.3), scale=(0.012, 0.09, 1.12), parent=llama)
mk("cube", "l_runa", "llama", (0, 0.0, -1.3), scale=(0.016, 0.02, 1.0), parent=llama)
for k in range(9):
    s = 1 if k % 2 else -1
    mk("cone", "l_pua", "negro", (0, s * 0.13, -0.4 - k * 0.24), (s * math.radians(-35), 0, 0),
       parent=llama, radius1=0.05, radius2=0, depth=0.22)

# seis Dark-John: cinco esperan en el camino, uno en un hueco cada uno; el sexto (el más
# grande) agazapado sobre el torii hasta su caída
DJ_ESPERA = [(0.3, 3.8), (-0.6, 5.9), (0.6, 8.1), (-0.5, 10.3), (0.5, 12.5), (0.0, TORII_Y)]
DJ_ESC = [1.0, 1.05, 0.95, 1.1, 1.0, 1.3]
DJ = []
for i in range(6):
    d = humano(f"DarkJohn{i + 1}", (*DJ_ESPERA[i], 0), CD)
    mk("torus", "aura_dark", "magenta", (0, 0, 0.05), major_radius=0.6, minor_radius=0.035, parent=d["r"])
    mk("torus", "aura_dark2", "cian", (0, 0, 0.9), major_radius=0.45, minor_radius=0.02, parent=d["r"])
    d["s"] = DJ_ESC[i]
    DJ.append(d)
respaldo("02_personajes")


# ---------------------------------------------------------------- utilidades de animación
def key_rot(o, t, eul):
    o.rotation_euler = eul
    o.keyframe_insert("rotation_euler", frame=T(t))


def apunta(v):
    """Rotación que lleva un miembro (-Z local) hacia v (en el espacio del cuerpo)."""
    return Vector((0, 0, -1)).rotation_difference(Vector(v).normalized()).to_euler()


def pose(o, t, x, y, z=0.0, yaw=0.0, tilt=0.0):
    """tilt > 0 inclina hacia atrás (cabeza hacia -Y local), tilt < 0 hacia adelante."""
    o.location = (x, y, z)
    o.keyframe_insert("location", frame=T(t))
    o.rotation_euler = (tilt, 0, yaw)
    o.keyframe_insert("rotation_euler", frame=T(t))


REPOSO = (0, 0, 0)
ANCHA = (apunta((-0.2, 0, -1)), apunta((0.2, 0, -1)))
GUARDIA_P = (apunta((-0.15, 0.25, -1)), apunta((0.15, -0.25, -1)))


def piernas(P, t, par):
    key_rot(P["pL"], t, par[0])
    key_rot(P["pR"], t, par[1])


def camina(P, t0, t1, final, paso=0.27, amp=0.45, brazo=False):
    """Ciclo de pasos entre t0 y t1, termina en la postura 'final'."""
    piernas(P, t0, final)
    t, k = t0 + paso / 2, 0
    while t < t1 - paso / 3:
        s = 1 if k % 2 else -1
        piernas(P, t, (apunta((0, s * amp, -1)), apunta((0, -s * amp, -1))))
        if brazo:
            key_rot(P["hL"], t, apunta((0.1, -s * amp * 0.8, -1)))
        t, k = t + paso, k + 1
    piernas(P, t1, final)


def estalla(nombre, pos, t, cols=("negro", "cian", "magenta", "violeta", "oro"), n=18, dur=10, tam=0.035):
    """Escamas que salen volando: un Dark-John que se deshace, o chispas de un choque."""
    k = T(t)
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


def chispas(nombre, pos, t):
    estalla(nombre, pos, t, ("llama", "oro"), n=10, dur=5, tam=0.03)


def muere(i, t, pos, n=20):
    d = DJ[i]
    d["r"].scale = d["S"]
    d["r"].keyframe_insert("scale", frame=T(t) - 1)
    d["r"].scale = (0.01, 0.01, 0.01)
    d["r"].keyframe_insert("scale", frame=T(t) + 2)
    estalla(f"muerte{i + 1}", pos, t, n=n, dur=12)


# ---------------------------------------------------------------- John
TAU = 2 * math.pi
JOHN = [  # (t, x, y, z, yaw, tilt)
    (-1.0, 0, -6.6, 0, 0, 0), (0.0, 0, -5.0, 0, 0, 0), (2.6, 0, -0.4, 0, 0, 0), (3.1, 0, 0, 0, 0, 0),
    (4.3, 0, 0, -0.08, 0, 0.05), (4.6, 0, 0.05, -0.05, 0, 0), (6.4, 0, 0.05, 0, 0, 0),
    (7.0, 0, 0.3, -0.05, 0.1, 0),
    # DJ1: bloqueo, esquiva, parada, barrida y remate
    (8.4, 0, 0.5, -0.05, 0.1, 0), (8.7, 0, 0.4, -0.08, 0.15, 0), (9.4, -0.35, 0.5, -0.05, 0.35, 0),
    (10.2, -0.15, 0.6, -0.05, 0.1, 0), (10.5, 0, 0.9, -0.05, 0, 0), (11.4, 0, 0.95, -0.05, 0, 0),
    (11.7, 0.1, 1.0, -0.45, -0.3, -0.25), (11.95, 0.1, 1.05, -0.45, 0.6, -0.25),
    (12.1, 0.1, 1.1, -0.1, 0.2, -0.15), (12.3, 0.1, 1.4, 0, 0, 0),
    # DJ2: codo ascendente y corte
    (12.75, 0, 2.4, -0.05, -0.15, 0), (12.85, 0, 2.5, -0.1, -0.2, -0.1), (13.0, 0.05, 2.6, -0.05, 0.1, 0),
    # DJ3: un corte limpio
    (13.5, 0.1, 4.2, 0, 0, 0), (14.0, 0.15, 4.4, -0.1, -0.2, -0.08), (14.4, 0.1, 4.6, 0, 0, 0),
    # DJ4: combinación codo, rodilla, pomo, corte
    (15.2, 0, 5.8, 0, 0, 0), (15.4, 0, 5.95, -0.08, 0.3, -0.1), (15.6, 0, 6.05, 0, 0.1, -0.05),
    (15.8, 0, 6.1, -0.05, -0.15, 0), (16.0, 0, 6.2, -0.1, 0.35, -0.1),
    # DJ5: amagues y patada
    (16.8, 0, 7.6, 0, 0, 0), (17.8, -0.2, 7.8, -0.05, 0.2, 0), (18.6, 0.2, 7.9, -0.05, -0.2, 0),
    (19.4, 0, 8.0, -0.05, 0, 0), (19.6, 0, 8.1, 0, 0, 0.15), (19.9, 0, 8.2, 0, 0, 0), (20.6, 0, 8.4, 0, 0, 0),
    # DJ6: el duelo largo
    (22.4, 0, 12.0, 0, 0, 0), (22.7, 0, 12.1, -0.05, 0.15, 0), (23.0, -0.3, 12.1, -0.05, 0.35, 0),
    (23.3, -0.15, 12.2, -0.05, 0.1, 0), (23.7, 0, 12.6, -0.05, -0.2, -0.05), (24.0, 0, 13.0, -0.05, 0.25, -0.08),
    (24.4, 0, 13.2, -0.4, 0, -0.2), (24.7, 0.1, 13.6, -0.05, -0.2, 0), (25.1, 0.1, 14.0, -0.05, 0, 0),
    (25.4, 0.45, 14.2, -0.05, 0, 0), (25.8, 0.4, 14.5, -0.05, -TAU, 0),
    (26.0, 0.3, 14.8, -0.1, -TAU - 0.3, -0.1), (26.6, 0.3, 15.2, 0, -TAU, 0),
    # sale caminando bajo el torii hacia el mar
    (30.0, 0, 21.0, 0, -TAU, 0), (31.0, 0, 22.6, 0, -TAU, 0),
]
for k in JOHN:
    pose(J["r"], *k)


def jpos(t):
    for a, b in zip(JOHN, JOHN[1:]):
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0])
            return a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
    return JOHN[-1][1], JOHN[-1][2]


def hacia_john(x, y, t):
    jx, jy = jpos(t)
    return math.atan2(-(jx - x), jy - y)


# brazo de la espada
a_empunadura, guardia = apunta((-0.63, 0.2, -0.34)), apunta((0.7, 0.35, 0.55))
bloque, en_alto, al_frente = apunta((-0.2, 0.5, 0.8)), apunta((0.1, 0.25, 1)), apunta((0, 1, 0.15))
for t, rot in [
    (0, REPOSO), (2.0, REPOSO), (2.6, a_empunadura), (4.3, a_empunadura), (4.45, apunta((-0.3, 0.6, -0.2))),
    (4.65, al_frente), (5.2, apunta((0.6, 0.9, 0.4))), (6.4, guardia),
    (8.4, guardia), (8.7, bloque), (9.0, guardia), (9.4, guardia), (10.2, bloque), (10.5, al_frente),
    (11.4, guardia), (11.7, apunta((0.8, 0.3, 0.2))), (11.95, apunta((0.8, 0.3, 0.2))), (12.05, en_alto),
    (12.2, apunta((0.1, 0.6, -1))), (12.6, guardia), (12.85, guardia), (13.0, apunta((-0.9, 0.8, 0))),
    (13.4, guardia), (13.85, en_alto), (14.0, apunta((-0.4, 1, -0.7))), (14.4, guardia), (15.3, guardia),
    (15.7, guardia), (15.8, apunta((0.2, 0.6, 0.8))), (16.0, apunta((-0.9, 0.7, 0.1))), (16.6, guardia),
    (19.6, guardia), (22.4, guardia), (22.7, bloque), (23.0, guardia), (23.5, en_alto),
    (23.7, apunta((-0.6, 1, -0.3))), (24.0, guardia), (24.4, apunta((0.6, 0.4, 0.6))),
    (24.7, apunta((0.2, 0.8, 0.9))), (25.1, guardia), (25.4, guardia), (25.8, en_alto),
    (26.0, apunta((-0.5, 1, -0.7))), (26.6, apunta((-0.5, 1, -0.7))), (27.4, apunta((0.3, 0.4, -1))),
    (28.0, a_empunadura), (28.5, REPOSO), (30.0, REPOSO)]:
    key_rot(J["hR"], t, rot)
# brazo libre: codos, controles, palma
g_izq = apunta((-0.3, 0.5, -0.6))
codo = apunta((0.2, 1, 0.3))
for t, rot in [
    (2.6, REPOSO), (7.0, g_izq), (12.75, g_izq), (12.85, codo), (13.0, g_izq), (15.3, g_izq),
    (15.4, apunta((0.3, 1, 0.1))), (15.55, g_izq), (23.2, g_izq), (23.3, apunta((0.1, 1, 0.4))),
    (23.5, g_izq), (23.9, g_izq), (24.0, codo), (24.2, g_izq), (26.6, g_izq), (27.0, REPOSO)]:
    key_rot(J["hL"], t, rot)
# piernas: caminata, postura, barrida, rodilla, patada
camina(J, -1.0, 2.9, (REPOSO, REPOSO), brazo=True)
piernas(J, 3.1, (REPOSO, REPOSO))
piernas(J, 4.3, ANCHA)
piernas(J, 6.8, ANCHA)
piernas(J, 7.0, GUARDIA_P)
piernas(J, 11.6, GUARDIA_P)
key_rot(J["pL"], 11.75, apunta((-1, 0.3, -0.15)))
key_rot(J["pL"], 11.95, apunta((0.3, 1, -0.15)))
piernas(J, 12.15, GUARDIA_P)
camina(J, 12.3, 12.75, GUARDIA_P)
camina(J, 13.1, 13.5, GUARDIA_P)
camina(J, 14.4, 15.2, GUARDIA_P)
piernas(J, 15.5, GUARDIA_P)
key_rot(J["pR"], 15.6, apunta((0, 1, -0.35)))
piernas(J, 15.72, GUARDIA_P)
camina(J, 16.1, 16.8, GUARDIA_P)
piernas(J, 19.45, GUARDIA_P)
key_rot(J["pR"], 19.6, apunta((0, 1, 0.2)))
key_rot(J["pR"], 19.75, apunta((0, 1, 0.2)))
piernas(J, 19.9, GUARDIA_P)
camina(J, 20.6, 22.4, GUARDIA_P, paso=0.2, amp=0.7)
piernas(J, 24.3, GUARDIA_P)
piernas(J, 24.4, ANCHA)
piernas(J, 24.6, GUARDIA_P)
camina(J, 26.6, 30.0, (REPOSO, REPOSO), brazo=True)

# la espada: enfundada; katana al salir; a 4.6 s se vuelve la espada de llama (mucho más
# grande); a 27.6 s vuelve a ser katana y la enfunda a 28 s
visible_tree(hilt_enf, [(-30, T(4.45) - 1), (T(28.0), 780)])
visible_tree(katana, [(T(4.45), T(4.6)), (T(27.6), T(28.0) - 1)])
visible_tree(llama, [(T(4.6) + 1, T(27.6) - 1)])
visible(aura_j, [(T(4.6) + 1, T(27.6) - 1)])
chispas("chispas_desenvaine", (0.35, 0.9, 1.4), 4.6)
estalla("chispas_desenvaine2", (0.3, 1.6, 1.5), 4.65, ("llama", "oro", "rojo"), n=24, dur=10, tam=0.025)

# el pasillo de cartas sube del suelo al desenvainar; la esfera late
for m, t0 in zip(muros, (4.6, 4.75)):
    m.location.z = -8
    m.keyframe_insert("location", frame=T(t0))
    m.location.z = 0
    m.keyframe_insert("location", frame=T(t0 + 0.6))
visible(orbe, [(T(4.9), 780)])
for k in range(0, 34):
    s = 1.0 if k % 2 else 1.15
    orbe.scale = (s, s, s)
    orbe.keyframe_insert("scale", frame=T(4.9 + k * 0.75))

# ---------------------------------------------------------------- Dark-John
garras = lambda lado: apunta((lado * 0.4, 0.6, -0.3))         # garras listas
arriba = lambda lado: apunta((lado * 0.2, 1, 0.7))             # garra levantada
zarpazo = lambda lado: apunta((-lado * 0.5, 1, -0.2))          # garra que baja cruzando
KILL = [12.2, 13.0, 14.0, 16.0, 20.12, 26.0]

# se forman de a uno entre escamas mientras la cámara gira (4.8 - 6.6 s)
for i, d in enumerate(DJ):
    tf = 4.8 + 0.3 * i
    x, y = DJ_ESPERA[i]
    z = 6.65 if i == 5 else 0.0
    d["r"].scale = (0.05, 0.05, 0.05)
    d["r"].keyframe_insert("scale", frame=T(tf))
    d["r"].scale = (d["s"],) * 3
    d["r"].keyframe_insert("scale", frame=T(tf + 0.5))
    # metamorfosis: más alto, brazos más largos
    d["S"] = (d["s"] * 1.08, d["s"] * 1.08, d["s"] * 1.4)
    d["r"].scale = d["S"]
    d["r"].keyframe_insert("scale", frame=T(7.4))
    for h in (d["hL"], d["hR"]):
        h.scale = (1, 1, 1)
        h.keyframe_insert("scale", frame=T(tf + 0.5))
        h.scale = (1.2, 1.2, 1.55)
        h.keyframe_insert("scale", frame=T(7.4))
    pose(d["r"], tf, x, y, z, yaw=math.pi, tilt=-0.35 if i == 5 else 0)
    estalla(f"forma{i + 1}", (x, y, z + 1.0), tf, n=14, dur=12)
    key_rot(d["hL"], tf, garras(-1))
    key_rot(d["hR"], tf, garras(1))
    if i == 5:
        piernas(d, tf, (apunta((-0.3, 0.7, -0.5)), apunta((0.3, 0.7, -0.5))))
    visible_tree(d["r"], [(T(tf), T(KILL[i]) + 2)])


def acecha(i, t0, t1, amp=0.15):
    """Los que esperan se balancean y amagan en su sitio, siempre mirando a John."""
    x, y = DJ_ESPERA[i]
    t, k = t0, 0
    while t < t1:
        xx = x + (amp if k % 2 else -amp)
        pose(DJ[i]["r"], t, xx, y + (0.08 if k % 3 == 0 else 0), 0.0, hacia_john(xx, y, t), -0.08)
        t, k = t + 0.26, k + 1


for i, fin in enumerate([7.6, 12.3, 13.3, 15.0, 16.8]):
    acecha(i, 5.4 + 0.3 * i, fin)


def dj(i, claves):
    """claves: (t, x, y, z, tilt)."""
    for t, x, y, z, tilt in claves:
        pose(DJ[i]["r"], t, x, y, z, hacia_john(x, y, t), tilt)


def garra(i, t, lado, rot):
    key_rot(DJ[i]["hL" if lado < 0 else "hR"], t, rot)


# DJ1 (8-12 s): dos zarpazos, uno bloqueado y otro esquivado, un golpe por arriba que John
# para; amaga, se lanza y John lo barre: cae de espaldas a sus pies y lo remata
dj(0, [(7.6, 0.3, 3.8, 0, -0.1), (8.3, 0.1, 1.5, 0, -0.15), (8.6, 0.1, 1.45, 0, -0.1), (9.3, 0.05, 1.4, -0.1, -0.25),
       (9.6, 0.1, 1.6, 0, 0), (10.2, 0.1, 1.55, 0, -0.1), (10.5, 0.1, 2.0, 0, 0.15), (10.8, 0.1, 1.8, 0, -0.1),
       (11.1, 0.1, 2.0, 0, 0), (11.4, 0.1, 2.0, -0.1, 0.1), (11.7, 0.1, 1.6, 0, -0.3), (11.8, 0.12, 1.65, 0.1, 0.4),
       (12.0, 0.15, 1.7, 0.15, 1.45)])
camina(DJ[0], 7.6, 8.3, GUARDIA_P, paso=0.16, amp=0.75)
for t, l, r in [(8.3, arriba(-1), arriba(1)), (8.6, arriba(-1), zarpazo(1)), (8.8, garras(-1), garras(1)),
                (9.1, arriba(-1), garras(1)), (9.3, apunta((0.5, 1, -0.6)), garras(1)), (9.6, garras(-1), garras(1)),
                (10.0, arriba(-1), arriba(1)), (10.2, apunta((0, 1, 0.2)), apunta((0, 1, 0.2))),
                (10.5, garras(-1), garras(1)), (11.4, arriba(-1), arriba(1)), (11.7, apunta((0, 1, 0)), apunta((0, 1, 0))),
                (12.0, apunta((-0.5, 0, 1)), apunta((0.5, 0, 1)))]:
    garra(0, t, -1, l)
    garra(0, t, 1, r)
piernas(DJ[0], 11.75, GUARDIA_P)
piernas(DJ[0], 11.9, (apunta((-0.2, 1, 0.4)), apunta((0.2, 1, 0.6))))
chispas("choque1a", (0.25, 0.95, 1.6), 8.7)
chispas("choque1b", (0.05, 1.05, 1.75), 10.2)
muere(0, 12.2, (0.15, 1.7, 0.4))

# DJ2 (13 s): se lanza, codo ascendente al estómago, se dobla y el corte lo deshace
dj(1, [(12.3, -0.6, 5.9, 0, -0.1), (12.75, -0.15, 3.25, 0, -0.25), (12.85, -0.15, 3.3, -0.2, -0.6),
       (13.0, -0.15, 3.35, -0.2, -0.5)])
camina(DJ[1], 12.3, 12.75, GUARDIA_P, paso=0.15, amp=0.75)
garra(1, 12.6, -1, arriba(-1))
garra(1, 12.6, 1, arriba(1))
garra(1, 12.85, -1, apunta((0, 0.3, -1)))
garra(1, 12.85, 1, apunta((0, 0.3, -1)))
muere(1, 13.0, (-0.15, 3.35, 0.9))

# DJ3 (14 s): carga de frente con las garras arriba; un solo corte diagonal
dj(2, [(13.3, 0.6, 8.1, 0, -0.1), (13.85, 0.3, 5.3, 0, -0.3), (14.0, 0.3, 5.2, 0, -0.2)])
camina(DJ[2], 13.3, 13.85, GUARDIA_P, paso=0.14, amp=0.8)
garra(2, 13.7, -1, arriba(-1))
garra(2, 13.7, 1, arriba(1))
muere(2, 14.0, (0.3, 5.2, 1.1))

# DJ4 (15-16 s): entra, codo al cuerpo, rodilla a las costillas, pomo a la mandíbula, corte
dj(3, [(15.0, -0.5, 10.3, 0, -0.1), (15.3, -0.15, 7.0, 0, -0.2), (15.4, -0.15, 7.1, 0, 0.2),
       (15.6, -0.15, 7.1, -0.15, -0.5), (15.8, -0.15, 7.2, 0, 0.4), (16.0, -0.15, 7.3, 0, 0.2)])
camina(DJ[3], 15.0, 15.3, GUARDIA_P, paso=0.12, amp=0.8)
garra(3, 15.25, 1, zarpazo(1))
garra(3, 15.4, 1, garras(1))
garra(3, 15.6, -1, apunta((0, 0.3, -1)))
garra(3, 15.8, -1, apunta((-0.6, -0.2, 0.6)))
garra(3, 15.8, 1, apunta((0.6, -0.2, 0.6)))
muere(3, 16.0, (-0.15, 7.3, 1.1))

# DJ5 (17-20 s): presiona con amagues; se compromete y la patada lo manda volando
dj(4, [(16.8, 0.5, 12.5, 0, -0.1), (17.4, 0.3, 9.6, 0, -0.1), (17.8, 0.3, 9.2, 0, -0.3), (18.1, 0.3, 9.7, 0, 0),
       (18.6, 0.3, 9.2, 0, -0.3), (18.9, 0.3, 9.8, 0, 0), (19.3, 0.3, 9.6, -0.1, 0.1), (19.5, 0.2, 9.0, 0, -0.35),
       (19.6, 0.2, 9.1, 0.1, 0.3), (19.8, 0.2, 11.0, 0.7, 1.0), (20.0, 0.2, 12.8, 0.15, 1.5),
       (20.12, 0.2, 13.3, 0.15, 1.5)])
camina(DJ[4], 16.8, 17.4, GUARDIA_P, paso=0.16, amp=0.7)
for t, rot in [(17.7, arriba(1)), (17.8, zarpazo(1)), (18.1, garras(1)), (18.5, arriba(1)), (18.6, zarpazo(1)),
               (18.9, garras(1)), (19.4, arriba(1)), (19.5, zarpazo(1)), (19.7, apunta((0.5, 0, 1)))]:
    garra(4, t, 1, rot)
garra(4, 19.5, -1, arriba(-1))
garra(4, 19.7, -1, apunta((-0.5, 0, 1)))
muere(4, 20.12, (0.2, 13.3, 0.4))

# DJ6 (20.5-26 s): salta del torii, cae de pie agazapado, retrocede tanteando y pelea el
# duelo más largo: garra alta bloqueada, garra baja esquivada, patada controlada; John lo
# hace retroceder, se agacha bajo su barrido, gira y lo remata con el corte final
dj(5, [(20.5, 0.0, TORII_Y, 6.65, -0.35), (20.75, 0.0, 17.6, 7.4, -0.2), (21.0, 0.0, 14.6, -0.3, -0.35),
       (21.4, 0.0, 14.6, 0, -0.05), (21.8, 0.15, 14.9, 0, 0), (22.1, -0.1, 14.8, 0, -0.05), (22.4, 0.0, 14.4, 0, -0.1),
       (22.65, 0.0, 13.25, 0, -0.25), (23.0, 0.1, 13.3, -0.1, -0.2), (23.3, 0.0, 13.3, 0, 0.15),
       (23.7, 0.0, 13.9, 0, 0.1), (24.0, 0.0, 14.5, 0, 0.3), (24.4, 0.0, 14.3, -0.05, -0.2), (24.7, 0.0, 15.0, 0, 0.25),
       (25.1, 0.05, 14.95, 0, -0.35), (25.4, -0.1, 14.75, -0.1, -0.4), (25.8, 0.0, 15.3, 0, 0), (26.0, 0.05, 15.4, 0, 0.1)])
piernas(DJ[5], 20.5, (apunta((-0.3, 0.7, -0.5)), apunta((0.3, 0.7, -0.5))))
piernas(DJ[5], 20.75, GUARDIA_P)
piernas(DJ[5], 21.0, (apunta((-0.3, 0.7, -0.5)), apunta((0.3, 0.7, -0.5))))
piernas(DJ[5], 21.4, GUARDIA_P)
camina(DJ[5], 22.4, 22.65, GUARDIA_P, paso=0.12, amp=0.7)
piernas(DJ[5], 23.2, GUARDIA_P)
key_rot(DJ[5]["pR"], 23.3, apunta((0, 1, 0.3)))
piernas(DJ[5], 23.45, GUARDIA_P)
for t, l, r in [(20.5, garras(-1), garras(1)), (22.5, arriba(-1), arriba(1)), (22.7, arriba(-1), zarpazo(1)),
                (22.85, arriba(-1), garras(1)), (23.0, apunta((0.5, 1, -0.6)), garras(1)), (23.3, garras(-1), garras(1)),
                (24.2, arriba(-1), arriba(1)), (24.4, apunta((1, 0.6, 0)), apunta((1, 0.6, 0))),
                (24.7, garras(-1), garras(1)), (25.0, apunta((0, 0.3, 1)), apunta((0, 0.3, 1))),
                (25.4, apunta((0, 1, -0.4)), apunta((0, 1, -0.4))), (25.8, garras(-1), garras(1))]:
    garra(5, t, -1, l)
    garra(5, t, 1, r)
estalla("aterriza6", (0.0, 14.6, 0.1), 21.0, ("negro", "violeta", "cian"), n=12, dur=8, tam=0.05)
chispas("choque6a", (0.15, 12.75, 1.7), 22.7)
chispas("choque6b", (0.25, 13.95, 1.6), 24.7)
muere(5, 26.0, (0.05, 15.4, 1.3), n=34)
chispas("vuelve_katana", (0.4, 15.9, 1.0), 27.6)

# ---------------------------------------------------------------- bloques (BLOQUES=1)
# Como en los ejemplos de Higgsfield: el previz solo lleva posiciones, orientación y cámara.
# Cada personaje es una figura rígida de caja y esfera (cara VERDE = frente, cara ROJA =
# espalda) que solo se traslada y gira; sin espada, chispas, auras ni utilería, y el
# escenario en grises. La coreografía la escribe el prompt.
BLOQUES = bool(os.environ.get("BLOQUES"))
if BLOQUES:
    GRISES = {"suelo": 0.32, "mar": 0.13, "torii_pilar": 0.62, "torii_kasagi": 0.62, "torii_nuki": 0.62,
              "torii_base": 0.4, "torii_kasagi_n": 0.4, "haiden": 0.45, "haiden_techo": 0.28,
              "farol": 0.5, "farol_caja": 0.5, "carta": 0.72}
    for o in list(bpy.data.objects):
        if o.type != "MESH":
            continue
        base = o.name.split(".")[0]
        if base in GRISES:
            g = GRISES[base]
            o.color = (g, g, g, 1)
        else:
            bpy.data.objects.remove(o, do_unlink=True)
    sc.world.color = (0.16, 0.17, 0.19)
    COL.update({"verde": (0.1, 0.85, 0.2), "rojo_codigo": (0.9, 0.08, 0.06),
                "fig_john": (0.9, 0.9, 0.88), "fig_monstruo": (0.06, 0.06, 0.07)})

    # los que miran a John cruzan ±π al girar: sin desenrollar, el bloque daría vueltas falsas
    for d in DJ:
        for fcv in d["r"].animation_data.action.fcurves:
            if fcv.data_path != "rotation_euler" or fcv.array_index != 2:
                continue
            prev = None
            for kp in sorted(fcv.keyframe_points, key=lambda k: k.co[0]):
                v = kp.co[1]
                while prev is not None and v - prev > math.pi:
                    v -= TAU
                while prev is not None and v - prev < -math.pi:
                    v += TAU
                dv = v - kp.co[1]
                kp.co[1] += dv
                kp.handle_left[1] += dv
                kp.handle_right[1] += dv
                prev = v
            fcv.update()

    def figura(nombre, raiz, col, alto=1.5, ancho=0.5, fondo=0.3, cabeza=0.13):
        b = empty(nombre + "_bloque")
        c = b.constraints.new("COPY_LOCATION")
        c.target = raiz
        lim = b.constraints.new("LIMIT_LOCATION")
        lim.use_min_z, lim.min_z = True, 0.0
        r = b.constraints.new("COPY_ROTATION")
        r.target, r.use_x, r.use_y = raiz, False, False
        s = b.constraints.new("COPY_SCALE")
        s.target = raiz
        partes = [mk("cube", nombre + "_caja", col, (0, 0, alto / 2), scale=(ancho / 2, fondo / 2, alto / 2), parent=b),
                  mk("uv_sphere", nombre + "_esfera", col, (0, 0, alto + cabeza), radius=cabeza, parent=b)]
        for lado, cc in ((1, "verde"), (-1, "rojo_codigo")):
            # panel a la altura del pecho, para que en los primeros planos no llene el cuadro
            partes.append(mk("cube", nombre + "_cara", cc, (0, lado * (fondo / 2 + 0.006), alto * 0.65),
                             scale=(ancho / 2 * 0.55, 0.006, alto * 0.28), parent=b))
        return partes

    figura("John", J["r"], "fig_john")
    for i, d in enumerate(DJ):
        for p in figura(f"DarkJohn{i + 1}", d["r"], "fig_monstruo"):
            visible(p, [(T(4.8 + 0.3 * i), T(KILL[i]) + 2)])
respaldo("03_pelea")

# ---------------------------------------------------------------- cámara: un solo plano
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.sensor_fit, cam.data.sensor_width = "HORIZONTAL", SENSOR
cam.data.clip_end = 600
cam.rotation_mode = "QUATERNION"

Z, X = (0, 0, 1), (1, 0, 0)
# (t, posición relativa a John, objetivo relativo, lente, vector arriba, giro°, pausa)
# las posiciones son relativas a la trayectoria suavizada de John: lo sigue sin perderlo
CAM = [
    # Lenguaje de la cinemática de referencia, sin el giro falso que dio la medición automática:
    # la cámara se mantiene derecha (inclinación holandesa de pocos grados) y a distancia legible.
    # ref. plano 1 (0-4.3 s): John camina hacia cámara; empuje fuerte hasta la mano en la empuñadura
    (0.0, (0.6, 5.0, 1.4), (0, 0, 1.3), 24, Z, 0, 0),
    (2.0, (0.8, 3.0, 1.35), (-0.1, 0, 1.2), 30, Z, -4, 0),
    (3.4, (0.9, 1.4, 1.5), (-0.25, 0.15, 1.1), 44, Z, -8, 0),
    (4.25, (0.75, 1.0, 1.45), (-0.3, 0.15, 1.05), 60, Z, -10, 0),  # la mano en la empuñadura
    # ref. plano 2 (4.3-7.3 s): latigazo con el desenvaine, luego ángulo bajo que sube con las cartas
    (4.6, (1.4, 1.5, 1.3), (0.2, 0.6, 1.35), 36, Z, -4, 0),
    (5.5, (1.8, 0.6, 1.1), (-0.1, 0.5, 1.4), 30, Z, 0, 0),
    (7.3, (1.9, -0.8, 1.0), (-0.1, 0.8, 1.5), 28, Z, 0, 0),
    # ref. plano 3 (7.3-15.3 s): un movimiento largo y derecho que rodea a John mientras pelea
    (7.6, (1.9, -1.6, 1.5), (0, 1.4, 1.1), 28, Z, -2, 0),
    (9.3, (0.2, -3.2, 1.6), (0, 0.8, 1.1), 28, Z, -4, 0),
    (11.3, (-2.6, -2.0, 1.4), (0, 0.4, 1.0), 28, Z, -5, 0),
    (12.3, (-3.4, 0.0, 1.1), (0, 0.4, 0.9), 26, Z, -3, 0),       # la barrida, a ras
    (13.3, (-3.4, 0.8, 1.3), (0, 0.4, 1.1), 28, Z, 0, 0),
    (14.3, (-3.2, 0.2, 1.4), (0, 0.6, 1.15), 30, Z, 3, 0),
    (15.27, (-3.3, 0.3, 1.4), (0, 0.6, 1.15), 32, Z, 4, 0),
    # ref. planos 4-7 (15.3-16.2 s): ráfaga de acercamientos bruscos en la combinación
    (15.6, (-2.8, 0.3, 1.35), (0, 0.6, 1.15), 46, Z, 2, 0),
    (15.85, (-3.1, 0.3, 1.35), (0, 0.6, 1.15), 38, Z, -3, 0),
    (16.0, (-2.9, 0.3, 1.35), (0, 0.6, 1.15), 44, Z, 0, 0),
    # ref. plano 8 (16.2-17 s): quieta; plano 9 (17-18.1 s): empuje lento con leve inclinación
    (16.23, (-3.2, 0.4, 1.45), (0, 0.7, 1.1), 32, Z, 0, 1),
    (16.97, (-3.2, 0.4, 1.45), (0, 0.7, 1.1), 32, Z, 0, 1),
    (18.07, (-2.8, 0.5, 1.45), (0, 0.8, 1.15), 36, Z, -4, 0),
    (18.6, (-2.4, -1.0, 1.5), (0, 1.6, 1.2), 32, Z, -3, 0),
    # ref. plano 10 (18.1-21.6 s): empuje lento por detrás de John hacia el torii; la patada y
    # la caída del sexto se ven al fondo
    (19.0, (-1.5, -2.4, 1.6), (0, 2.6, 1.3), 30, Z, -2, 0),
    (21.57, (-1.1, -2.7, 1.6), (0, 3.2, 1.4), 33, Z, 0, 0),
    # ref. plano 11 (21.6-26 s): sigue el duelo empujando y subiendo la mirada al monstruo
    (23.0, (-1.2, -3.4, 1.5), (0, 2.4, 1.5), 30, Z, 0, 0),
    (24.5, (1.2, -3.3, 1.4), (0, 2.4, 1.6), 31, Z, 2, 0),
    (26.0, (0.8, -3.2, 1.4), (0.1, 2.4, 1.8), 32, Z, 0, 0),
    # ref. plano 12 (26-30 s): se aleja despacio mientras John cruza el torii
    (26.6, (0.4, -2.8, 1.5), (0, 2.5, 1.5), 32, Z, 0, 0),
    (30.0, (0.2, -5.2, 1.8), (0, 3, 1.4), 28, Z, 0, 1),
]
if BLOQUES:
    # con bloques no hay mano ni empuñadura que enseñar: el empuje termina en un plano cercano
    # de la cadera en vez de pegarse a la caja
    CAM[2] = (3.4, (1.3, 2.5, 1.5), (-0.2, 0.1, 1.15), 34, Z, -8, 0)
    CAM[3] = (4.25, (1.2, 2.0, 1.4), (-0.3, 0.1, 1.05), 40, Z, -10, 0)
# golpes: pequeño zoom de acento y sacudida
IMPACTOS = [(8.7, 0.5), (10.2, 0.4), (12.0, 1.0), (12.2, 0.6), (12.85, 0.7), (13.0, 0.8), (14.0, 0.9),
            (15.4, 0.5), (15.6, 0.5), (15.8, 0.5), (16.0, 0.9), (19.6, 1.0), (20.12, 0.6), (21.0, 0.6),
            (22.7, 0.5), (23.3, 0.5), (24.0, 0.6), (24.7, 0.6), (26.0, 1.2), (28.0, 0.25)]
if os.environ.get("SUAVE"):
    # Cámara suave y planos claros, al estilo de las peleas de espadas de cine de artes marciales:
    # grúa que establece el lugar antes del caos, planos de cuerpo entero con los dos
    # peleadores de perfil (cámara perpendicular a la línea de acción) y el resto de los
    # monstruos esperando al fondo, una grúa alta en la pausa para leer la geografía, y nada de
    # sacudidas ni zooms bruscos. La cámara no pasa de x = 3.6 para no chocar con las cartas.
    CAM = [
        (0.0, (0.0, 9.0, 5.0), (0, 0, 1.0), 24, Z, 0, 0),           # grúa alta y frontal, John al centro
        (3.1, (0.0, 4.6, 1.5), (0, 0, 1.0), 28, Z, 0, 0),           # baja a la altura de los ojos; se detiene
        (4.4, (2.4, 2.6, 1.2), (0, 0.3, 1.0), 24, Z, 0, 0),         # se abre hacia su derecha con la mano en la empuñadura
        (5.6, (3.4, 1.2, 0.9), (0, 2.0, 1.5), 20, Z, 0, 0),         # bajo, mirando arriba: suben las cartas, se forman
        (7.6, (3.6, -0.3, 1.1), (0, 1.2, 1.3), 18, Z, 0, 0),         # tres cuartos de cuerpo entero para el primer duelo
        (9.5, (3.6, -0.4, 1.1), (0, 0.9, 1.25), 18, Z, 0, 0),
        (11.5, (3.5, -0.6, 0.9), (0, 0.6, 1.1), 18, Z, 0, 0),        # más bajo para la barrida y la caída
        (12.3, (3.5, -0.4, 1.0), (0, 0.8, 1.2), 18, Z, 0, 0),
        (14.0, (3.6, -0.3, 1.1), (0, 1.0, 1.3), 20, Z, 0, 0),        # se desliza a su lado en la cadena
        (16.2, (3.4, -0.2, 1.1), (0, 1.0, 1.3), 20, Z, 0, 0),
        (17.4, (2.2, -2.6, 5.0), (0, 2.6, 0.6), 24, Z, 0, 1),       # grúa alta: John, el quinto y el torii
        (18.1, (1.6, -3.0, 3.6), (0, 2.6, 1.0), 24, Z, 0, 0),
        (19.4, (1.0, -3.6, 1.4), (0, 3.0, 1.3), 24, Z, 0, 0),       # bajo detrás de él: la patada sale por el camino
        (21.0, (2.2, -2.6, 1.3), (0, 3.0, 1.5), 26, Z, 0, 0),       # el sexto cae del torii; empieza a rodear
        (22.4, (3.4, -1.0, 1.1), (0, 1.0, 1.4), 18, Z, 0, 0),        # perfil para el último duelo
        (24.0, (3.5, -1.0, 1.1), (0, 1.1, 1.4), 18, Z, 0, 0),
        (25.6, (3.3, -0.8, 1.1), (0, 1.1, 1.4), 20, Z, 0, 0),
        (26.2, (3.0, -0.6, 1.2), (0, 1.0, 1.4), 24, Z, 0, 0),        # leve acercamiento en el corte final
        (27.8, (1.6, -3.0, 1.6), (0, 2.0, 1.4), 28, Z, 0, 0),
        (30.0, (0.3, -6.0, 2.6), (0, 3.0, 1.6), 26, Z, 0, 1),       # se aleja subiendo mientras cruza el torii
    ]
    IMPACTOS = []


def vec(k):
    return [*k[1], *k[2], k[3], *Vector(k[4]).normalized(), k[5]]


def hermite(t):
    ts = [k[0] for k in CAM]
    ps = [vec(k) for k in CAM]
    n = len(ts)

    def tang(i):
        if CAM[i][6] or i in (0, n - 1):
            return [0.0] * len(ps[i])
        return [((ps[i + 1][c] - ps[i][c]) / (ts[i + 1] - ts[i]) + (ps[i][c] - ps[i - 1][c]) / (ts[i] - ts[i - 1])) / 2
                for c in range(len(ps[i]))]

    if t <= ts[0]:
        return ps[0]
    if t >= ts[-1]:
        return ps[-1]
    i = max(j for j in range(n - 1) if ts[j] <= t)
    h = ts[i + 1] - ts[i]
    u = (t - ts[i]) / h
    m0, m1 = tang(i), tang(i + 1)
    h00, h10, h01, h11 = 2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2
    return [h00 * ps[i][c] + h10 * h * m0[c] + h01 * ps[i + 1][c] + h11 * h * m1[c] for c in range(len(ps[i]))]


# trayectoria de John suavizada (para que la cámara no copie cada sacudida del cuerpo)
fc = {f.array_index: f for f in J["r"].animation_data.action.fcurves if f.data_path == "location"}
raw = {f: (fc[0].evaluate(f), fc[1].evaluate(f)) for f in range(-40, 800)}


def ancla(f):
    ws = [(math.exp(-(d / 7.0) ** 2), raw[f + d]) for d in range(-14, 15)]
    s = sum(w for w, _ in ws)
    return Vector((sum(w * p[0] for w, p in ws) / s, sum(w * p[1] for w, p in ws) / s, 0))


def mirar(loc, tgt, up):
    z = -(tgt - loc).normalized()
    x = Vector(up).cross(z)
    x = x.normalized() if x.length > 1e-6 else Vector((1, 0, 0))
    y = z.cross(x)
    return Matrix((x, y, z)).transposed().to_4x4()


for f in range(0, 750):
    t = f / FPS
    v = hermite(t)
    A = ancla(f)
    loc, tgt, lens, up, roll = A + Vector(v[0:3]), A + Vector(v[3:6]), v[6], Vector(v[7:10]), v[10]
    sac, punch = 0.0, 0.0
    for ti, a in IMPACTOS:
        d = f - T(ti)
        if 0 <= d < 12:
            sac += a * 0.6 * math.sin(d * 2.3) * math.exp(-d / 3.5)
            punch += a * 0.07 * math.exp(-d / 3.0)
    rot = mirar(loc, tgt, up) @ Matrix.Rotation(math.radians(roll + sac * 0.6), 4, "Z") \
        @ Matrix.Rotation(math.radians(sac), 4, "X") @ Matrix.Rotation(math.radians(sac * 0.7), 4, "Y")
    cam.location = loc
    cam.rotation_quaternion = rot.to_quaternion()
    cam.data.lens = lens * (1 + punch)
    cam.keyframe_insert("location", frame=f)
    cam.keyframe_insert("rotation_quaternion", frame=f)
    cam.data.keyframe_insert("lens", frame=f)
respaldo("04_camara")

# ---------------------------------------------------------------- control: John siempre en cuadro
torso = bpy.data.objects["John_caja" if BLOQUES else "John_torso"]
malos = []
for f in range(0, 750):
    sc.frame_set(f)
    c = world_to_camera_view(sc, cam, torso.matrix_world.translation + Vector((0, 0, 0.4 if BLOQUES else 0)))
    if not (0.05 < c.x < 0.95 and 0.05 < c.y < 0.95 and c.z > 0.3) and not T(3.3) <= f <= T(4.5):
        malos.append((f, round(c.x, 2), round(c.y, 2), round(c.z, 2)))
print("FUERA_DE_CUADRO", len(malos))
for m in malos[::6]:
    print("  ", m)

if os.environ.get("NORENDER"):
    sys.exit(0)
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
FR = range(F0, F1 + 1)
if os.environ.get("FRAMES"):
    FR = [int(x) for x in os.environ["FRAMES"].split(",")]
for f in FR:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(OUT, "frames", f"{f:04d}.png")
    bpy.ops.render.render(write_still=True)
