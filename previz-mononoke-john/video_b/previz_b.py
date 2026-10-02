"""Previz del video B: John contra un solo monstruo, con la cámara de la referencia.

Uso: python previz_b.py salida_dir [frame_ini frame_fin]
Variables: RES=0.5 baja la resolución; FRAMES=a,b,c renderiza solo esos cuadros;
NORENDER=1 solo arma la escena, guarda los .blend y revisa el encuadre.

Son 12 planos con los mismos cortes y movimientos que la referencia (ref_curvas.json,
pasada de 30 a 25 fps). Cada plano tiene una cámara base y encima el paneo, la
inclinación, el zoom y el giro medidos en la referencia. La acción cambia en tres
puntos respecto de la referencia:
  - al final del plano 3 se ve a la sombra lanzarse y la cámara la sigue;
  - durante la transformación (plano 10) John queda siempre al fondo, en cuadro;
  - en el plano 12 se atacan a la vez y un destello termina el video.
"""
import json, math, os, random, sys
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

OUT = sys.argv[1]
F0, F1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 749)
FPS, SENSOR = 25, 36.0
RES = float(os.environ.get("RES", "1"))
W, H = round(1260 * RES) // 2 * 2, round(540 * RES) // 2 * 2
AQUI = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
random.seed(5)


def T(s):
    return round(s * FPS)


def respaldo(etapa):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"previz_b_{etapa}.blend"), compress=True)


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
sc.world.color = (0.02, 0.04, 0.06)
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"
sc.view_settings.exposure = 0.6
sc.frame_start, sc.frame_end = 0, 749

COL = {
    "suelo": (0.11, 0.14, 0.13), "mar": (0.06, 0.15, 0.32), "torii": (0.85, 0.22, 0.12),
    "rojo": (0.55, 0.03, 0.06), "abrigo": (0.75, 0.05, 0.08), "piel": (0.85, 0.66, 0.52),
    "pelo": (0.05, 0.04, 0.04), "lente": (0.02, 0.02, 0.02), "oro": (0.85, 0.65, 0.2),
    "azul": (0.1, 0.2, 0.9), "blanco": (0.95, 0.95, 0.95), "negro": (0.015, 0.015, 0.02),
    "cian": (0.1, 1.0, 1.0), "magenta": (1.0, 0.1, 0.8), "llama": (1.0, 0.35, 0.05),
    "acero": (0.65, 0.68, 0.72), "funda": (0.04, 0.04, 0.04), "piedra": (0.32, 0.33, 0.3),
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
mk("cube", "haiden", "madera", (0, -24, 1.8), scale=(5, 3, 1.8))
mk("cone", "haiden_techo", "teja", (0, -24, 4.8), (0, 0, math.pi / 4), (1, 0.62, 1), vertices=4,
   radius1=8.5, radius2=0, depth=2.6)
for y in (-16, -12, -8, 10, 14):
    for x in (-2.8, 2.8):
        mk("cylinder", "farol", "piedra", (x, y, 0.6), radius=0.12, depth=1.2)
        mk("cube", "farol_caja", "piedra", (x, y, 1.35), scale=(0.25, 0.25, 0.22))
# círculos rituales: donde se planta John y donde espera la sombra
for cx, cy in ((0, -2.5), (0, 6)):
    for rr, cc in ((1.6, "rojo"), (2.0, "blanco"), (2.4, "rojo"), (2.8, "blanco")):
        mk("torus", "anillo", cc, (cx, cy, 0.02), major_radius=rr, minor_radius=0.06)
respaldo("01_escena")

# ---------------------------------------------------------------- personajes
CJ = {"piel_baja": "negro", "traje": "rojo", "abrigo": "abrigo", "piel": "piel", "pelo": "pelo",
      "lente": "oro", "cristal": "lente", "mono": "azul"}
CD = {"piel_baja": "negro", "traje": "negro", "abrigo": (0.03, 0.01, 0.05), "piel": "negro", "pelo": "negro",
      "lente": "magenta", "cristal": "cian", "mono": "magenta"}


def humano(nombre, loc, c):
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


J = humano("John", (0, -15, 0), CJ)
aura_j = mk("torus", "aura_john", "llama", (0, 0, 0.05), major_radius=0.8, minor_radius=0.04, parent=J["r"])
funda = empty("funda", (-0.37, 0.1, 1.0), J["r"])
funda.rotation_euler = (math.radians(-60), 0, 0)
mk("cube", "saya", "funda", (0, -0.45, 0), scale=(0.025, 0.45, 0.035), parent=funda)
hilt_enf = empty("empunadura_enfundada", (0, 0.02, 0), funda)
mk("cylinder", "tsuba", "oro", (0, 0.02, 0), (math.pi / 2, 0, 0), radius=0.06, depth=0.015, parent=hilt_enf)
mk("cube", "tsuka", "rojo", (0, 0.16, 0), scale=(0.02, 0.13, 0.022), parent=hilt_enf)
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

D = humano("Sombra", (0, 6, 0), CD)
mk("torus", "aura_dark", "magenta", (0, 0, 0.05), major_radius=0.6, minor_radius=0.035, parent=D["r"])
mk("torus", "aura_dark2", "cian", (0, 0, 0.9), major_radius=0.45, minor_radius=0.02, parent=D["r"])
destello = mk("uv_sphere", "destello", "blanco", (0, 1.25, 1.7), radius=1.0)
respaldo("02_personajes")


# ---------------------------------------------------------------- animación
def key_rot(o, t, eul):
    o.rotation_euler = eul
    o.keyframe_insert("rotation_euler", frame=T(t))


def apunta(v):
    return Vector((0, 0, -1)).rotation_difference(Vector(v).normalized()).to_euler()


def pose(o, t, x, y, z=0.0, yaw=0.0, tilt=0.0):
    o.location = (x, y, z)
    o.keyframe_insert("location", frame=T(t))
    o.rotation_euler = (tilt, 0, yaw)
    o.keyframe_insert("rotation_euler", frame=T(t))


REPOSO = (0, 0, 0)
GUARDIA_P = (apunta((-0.15, 0.25, -1)), apunta((0.15, -0.25, -1)))
ANCHA = (apunta((-0.25, 0, -1)), apunta((0.25, 0, -1)))


def piernas(P, t, par):
    key_rot(P["pL"], t, par[0])
    key_rot(P["pR"], t, par[1])


def camina(P, t0, t1, final, paso=0.27, amp=0.45, brazo=False):
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
    estalla(nombre, pos, t, ("llama", "oro"), n=12, dur=5, tam=0.025)


# John: llega corriendo, se planta, desenvaina; espera; al final carga
for k in [(-1.0, 0, -17.6, 0, 0, -0.1), (0.0, 0, -15.0, 0, 0, -0.12), (3.6, 0, -5.4, 0, 0, -0.1),
          (4.27, 0, -3.6, 0, 0, -0.05), (4.9, 0, -2.6, -0.05, 0, 0.05), (5.2, 0, -2.5, -0.06, 0, 0),
          (6.4, 0, -2.5, -0.05, 0.1, 0), (14.6, 0, -2.5, -0.05, 0.1, 0), (15.27, 0, -1.9, -0.1, 0.0, -0.08),
          (15.43, 0, -1.85, -0.12, 0.05, -0.05), (16.0, 0, -1.6, -0.08, -0.1, -0.1), (16.23, 0, -1.7, -0.05, 0, 0),
          (21.57, 0, -1.6, -0.05, 0.05, 0), (25.5, 0, -1.5, -0.25, 0, -0.1), (26.0, 0, -1.4, -0.2, 0, -0.15),
          (27.3, 0, 0.75, -0.15, -0.2, -0.2), (27.5, 0.05, 0.95, -0.2, -0.5, -0.15), (30.0, 0.05, 0.95, -0.2, -0.5, -0.15)]:
    pose(J["r"], *k)
camina(J, -1.0, 4.27, GUARDIA_P, paso=0.17, amp=0.8, brazo=True)
camina(J, 4.27, 4.95, ANCHA, paso=0.22, amp=0.4)
piernas(J, 6.4, GUARDIA_P)
camina(J, 14.6, 15.27, GUARDIA_P, paso=0.2, amp=0.5)
piernas(J, 25.5, ANCHA)
camina(J, 26.0, 27.3, GUARDIA_P, paso=0.16, amp=0.8)
a_empunadura, guardia = apunta((-0.63, 0.2, -0.34)), apunta((0.7, 0.35, 0.55))
bloque, en_alto, al_frente = apunta((-0.2, 0.5, 0.8)), apunta((0.1, 0.25, 1)), apunta((0, 1, 0.15))
for t, rot in [(0, apunta((0.1, -0.4, -1))), (4.27, REPOSO), (4.9, REPOSO), (5.2, a_empunadura),
               (5.6, a_empunadura), (5.75, apunta((-0.3, 0.6, -0.2))), (5.95, al_frente),
               (6.4, apunta((0.6, 0.9, 0.4))), (6.9, guardia), (15.0, guardia), (15.35, bloque), (15.6, bloque),
               (15.85, al_frente), (16.2, guardia), (25.6, guardia), (26.0, apunta((0.8, -0.3, 0.6))),
               (27.0, en_alto), (27.3, apunta((-0.4, 1, -0.6))), (30.0, apunta((-0.4, 1, -0.6)))]:
    key_rot(J["hR"], t, rot)
for t, rot in [(4.27, REPOSO), (6.4, apunta((-0.3, 0.5, -0.6))), (15.5, apunta((-0.3, 0.5, -0.6))),
               (15.85, apunta((0.2, 1, 0.3))), (16.2, apunta((-0.3, 0.5, -0.6)))]:
    key_rot(J["hL"], t, rot)
visible_tree(hilt_enf, [(-30, T(5.75) - 1)])
visible_tree(katana, [(T(5.75), T(5.9))])
visible_tree(llama, [(T(5.9) + 1, 780)])
visible(aura_j, [(T(5.9) + 1, 780)])
chispas("chispas_desenvaine", (0.35, -1.9, 1.4), 5.9)
estalla("chispas_desenvaine2", (0.3, -1.1, 1.5), 5.95, ("llama", "oro", "rojo"), n=22, dur=10, tam=0.025)

# la sombra: acecha, se agazapa y se lanza (se ve de dónde sale el ataque); choque;
# sale despedida; se retuerce y se transforma en el monstruo; ruge; carga; golpe a la vez
S = D["r"]
for k in [(7.3, 0, 6.0, 0, math.pi, 0), (9.0, 0.15, 6.0, 0, math.pi, -0.05), (10.6, -0.15, 6.1, 0, math.pi, 0),
          (12.2, 0.1, 6.0, 0, math.pi, -0.05), (13.5, 0, 6.0, -0.25, math.pi, -0.35),
          (14.3, 0, 5.8, -0.3, math.pi, -0.45), (14.9, 0, 2.2, 0.25, math.pi, -0.4),
          (15.27, 0, 0.0, 0.45, math.pi, -0.3), (15.43, 0, -0.6, 0.3, math.pi, -0.2),
          (15.6, 0, -0.5, 0.15, math.pi, 0.1), (16.0, 0, 1.6, 0.5, math.pi, 0.7), (16.23, 0, 4.6, 0.3, math.pi, 1.2),
          (16.6, 0, 5.2, -0.4, math.pi, -0.9), (16.97, 0, 5.2, -0.4, math.pi, -0.85)]:
    pose(S, *k)
camina(D, 14.3, 15.2, GUARDIA_P, paso=0.13, amp=0.8)
garras = lambda lado: apunta((lado * 0.4, 0.6, -0.3))
arriba = lambda lado: apunta((lado * 0.2, 1, 0.7))
for t in (7.3, 13.4):
    key_rot(D["hL"], t, garras(-1))
    key_rot(D["hR"], t, garras(1))
for t, l, r in [(14.3, apunta((-0.3, -0.6, -0.4)), apunta((0.3, -0.6, -0.4))), (15.1, arriba(-1), arriba(1)),
                (15.43, apunta((0, 1, 0.2)), apunta((0, 1, 0.2))), (16.0, apunta((-0.6, -0.4, 0.8)), apunta((0.6, -0.4, 0.8))),
                (16.6, apunta((-0.3, 0.8, -0.8)), apunta((0.3, 0.8, -0.8)))]:
    key_rot(D["hL"], t, l)
    key_rot(D["hR"], t, r)
chispas("choque_a", (0.05, -1.15, 1.75), 15.43)
chispas("choque_b", (0.0, -1.0, 1.6), 15.6)
estalla("polvo_caida", (0, 4.8, 0.2), 16.23, ("negro", "violeta", "cian"), n=12, dur=8)

# transformación (17 - 21.6 s): se retuerce, crece, se alargan los brazos
for j, t in enumerate([t / 10 for t in range(170, 216, 2)]):
    w = 0.25 if j % 2 else -0.25
    z = -0.4 + min(1.0, max(0.0, (t - 18.0) / 3.0)) * 0.4
    pose(S, t, 0.05 * (1 if j % 3 else -1), 5.2, z, math.pi + w * 0.4, -0.85 + min(1.0, (t - 17) / 4.3) * 0.85 + w)
    key_rot(D["hL"], t, apunta((-0.8, 0.3 * (1 if j % 2 else -1), 0.2 * (1 if j % 3 else -1))))
    key_rot(D["hR"], t, apunta((0.8, -0.3 * (1 if j % 2 else -1), 0.3)))
S.scale = (1, 1, 1)
S.keyframe_insert("scale", frame=T(18.2))
S.scale = (1.25, 1.25, 1.8)
S.keyframe_insert("scale", frame=T(21.3))
for h in (D["hL"], D["hR"]):
    h.scale = (1, 1, 1)
    h.keyframe_insert("scale", frame=T(18.2))
    h.scale = (1.3, 1.3, 1.7)
    h.keyframe_insert("scale", frame=T(21.3))
for t in (18.4, 19.3, 20.2, 21.0):
    estalla(f"capullo_{t}", (0, 5.2, 1.6), t, ("negro", "violeta", "cian", "magenta"), n=16, dur=12, tam=0.04)
# ya es el monstruo: se yergue, ruge, avanza y se agazapa para la carga
for k in [(21.57, 0, 5.2, 0, math.pi, 0), (22.6, 0, 5.2, 0, math.pi, 0.25), (23.4, 0, 5.1, 0, math.pi, 0.35),
          (24.2, 0.1, 4.6, 0, math.pi, -0.05), (25.2, -0.1, 4.1, 0, math.pi, -0.1), (25.8, 0, 4.0, -0.2, math.pi, -0.45),
          (26.0, 0, 3.9, -0.2, math.pi, -0.45), (27.3, 0, 1.75, 0.1, math.pi, -0.35), (27.5, -0.05, 1.6, 0.1, math.pi + 0.4, -0.3),
          (30.0, -0.05, 1.6, 0.1, math.pi + 0.4, -0.3)]:
    pose(S, *k)
camina(D, 24.0, 25.4, GUARDIA_P, paso=0.35, amp=0.5)
camina(D, 26.0, 27.3, GUARDIA_P, paso=0.2, amp=0.8)
for t, l, r in [(21.6, apunta((-1, 0.2, 0.3)), apunta((1, 0.2, 0.3))), (22.8, apunta((-1, 0.3, 0.8)), apunta((1, 0.3, 0.8))),
                (24.0, garras(-1), garras(1)), (26.0, arriba(-1), arriba(1)),
                (27.3, apunta((0.3, 1, -0.3)), apunta((-0.3, 1, -0.3)))]:
    key_rot(D["hL"], t, l)
    key_rot(D["hR"], t, r)
# golpe simultáneo y destello que termina el video
destello.scale = (0.05, 0.05, 0.05)
destello.keyframe_insert("scale", frame=T(27.3))
destello.scale = (7, 7, 7)
destello.keyframe_insert("scale", frame=T(27.9))
visible(destello, [(T(27.3), 780)])
chispas("choque_final", (0, 1.25, 1.7), 27.3)
respaldo("03_accion")

# ---------------------------------------------------------------- cámara: los 12 planos de la referencia
REF = json.load(open(os.path.join(AQUI, "ref_curvas.json")))["planos"]
SH = []
for i, (n, a30, b30, pts) in enumerate(REF):
    a = round(a30 * FPS / 30)
    b = round(REF[i + 1][1] * FPS / 30) - 1 if i + 1 < len(REF) else 749
    SH.append((n, a, b, pts))

# cámara base de cada plano: (posición, objetivo, lente mm)
BASE = {
    1: ((0.5, 1.0, 0.9), (2.6, -8.0, 1.2), 22),       # John llega corriendo hacia cámara
    2: ((1.4, -0.4, 1.7), (0, -2.5, 1.6), 35),     # primer plano: desenvaina, la cámara baja a la espada
    3: ((-7.0, 3.5, 0.9), (0, 5.8, 1.0), 30),       # la sombra; órbita con giro; al final sigue su ataque
    4: ((5.5, -0.9, 1.2), (0, -1.0, 1.3), 24),      # general lateral: llega el ataque
    5: ((0.9, -1.0, 1.8), (0.05, -1.2, 1.7), 45),   # garra contra la hoja
    6: ((-0.8, -3.8, 1.5), (0, -1.6, 1.4), 30),     # sobre el hombro: John empuja
    7: ((1.8, -0.5, 0.4), (0, 3.4, 0.9), 26),       # la sombra sale despedida
    8: ((0.9, -5.6, 0.9), (0, 3.0, 1.2), 30),       # quieta: John de espaldas, la sombra caída al fondo
    9: ((0.65, -3.4, 1.65), (0, 5.2, 1.0), 45),     # empuje lento: empieza a retorcerse
    10: ((-2.0, 9.8, 0.8), (0, 3.4, 1.5), 26),      # transformación; John siempre al fondo
    11: ((0.8, -4.6, 0.4), (0, 5.0, 1.2), 24),     # el monstruo se alza; panea hacia arriba
    12: ((9.5, 1.2, 1.3), (0, 1.2, 1.6), 24),       # cargan, golpe a la vez, destello
}

cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.sensor_fit, cam.data.sensor_width = "HORIZONTAL", SENSOR
cam.data.clip_end = 600
cam.rotation_mode = "QUATERNION"


def interp(pts, t):
    xs = [0, 0.25, 0.5, 0.75, 1.0]
    i = min(int(t / 0.25), 3)
    u = (t - xs[i]) / 0.25
    p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, 4)]
    m1, m2 = (p2 - p0) / 2, (p3 - p1) / 2
    h00, h10, h01, h11 = 2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2
    return h00 * p1 + h10 * m1 + h01 * p2 + h11 * m2


# posiciones de los personajes cuadro a cuadro (para apuntar cada plano)
jt, st = bpy.data.objects["John_torso"], bpy.data.objects["Sombra_torso"]
POS = {}
for f in range(0, 750):
    sc.frame_set(f)
    POS[f] = (jt.matrix_world.translation.copy(), st.matrix_world.translation.copy())

# quién tiene que verse en cada plano: (obligatorio, deseable)
QUIEN = {1: ("J", ""), 2: ("J", ""), 3: ("S", "J"), 4: ("JS", ""), 5: ("", ""), 6: ("J", "S"), 7: ("S", ""),
         8: ("JS", ""), 9: ("S", "J"), 10: ("JS", ""), 11: ("S", "J"), 12: ("JS", "")}


def curva(n, pts, a, b, f, f0, hfov, vfov):
    t = 0 if b == a else (f - a) / (b - a)
    dx, dy, z, r = (interp([p[k] for p in pts], t) for k in range(4))
    if n == 1:
        z = max(z, 0.2) ** 0.5   # parte del zoom ya lo da John acercándose a la carrera
    zl = max(z, 0.2)             # el paneo y la inclinación se midieron sobre el cuadro ya con zoom
    rot = Matrix.Rotation(dx * hfov / zl, 4, "Y") @ Matrix.Rotation(dy * vfov / zl, 4, "X") \
        @ Matrix.Rotation(math.radians(r), 4, "Z")
    return rot, f0 * zl


def puntaje(n, a, b, pts, L, base, f0, hfov, vfov):
    req, opt = QUIEN[n]
    tot = 0.0
    for f in range(a, b + 1):
        if f >= T(27.4):
            continue
        rot, lens = curva(n, pts, a, b, f, f0, hfov, vfov)
        R = (base @ rot).to_3x3().transposed()
        for q, p in (("J", POS[f][0]), ("S", POS[f][1])):
            w = 10 if q in req else (1 if q in opt else 0)
            if not w:
                continue
            v = R @ (p - L)
            if v.z > -0.3:
                tot += w
                continue
            x = v.x / -v.z * lens / (SENSOR / 2)
            y = v.y / -v.z * lens / (SENSOR * H / W / 2)
            if abs(x) > 0.9 or abs(y) > 0.9:
                tot += w
            tot += 0.03 * w * (abs(x) + abs(y))
    return tot


for n, a, b, pts in SH:
    L, Tg, f0 = BASE[n]
    L, Tg = Vector(L), Vector(Tg)
    base0 = (Tg - L).to_track_quat("-Z", "Y").to_matrix().to_4x4()
    hfov = 2 * math.atan(SENSOR / 2 / f0)
    vfov = 2 * math.atan(SENSOR * H / W / 2 / f0)
    mejor = (puntaje(n, a, b, pts, L, base0, f0, hfov, vfov), 0, 0)
    if QUIEN[n] != ("", ""):
        for dyaw in range(-36, 37, 4):
            for dpit in range(-30, 31, 3):
                bb = base0 @ Matrix.Rotation(math.radians(dyaw), 4, "Y") @ Matrix.Rotation(math.radians(dpit), 4, "X")
                sco = puntaje(n, a, b, pts, L, bb, f0, hfov, vfov) + 0.02 * (abs(dyaw) + abs(dpit))
                if sco < mejor[0]:
                    mejor = (sco, dyaw, dpit)
    base = base0 @ Matrix.Rotation(math.radians(mejor[1]), 4, "Y") @ Matrix.Rotation(math.radians(mejor[2]), 4, "X")
    print(f"APUNTE plano {n:2d}: giro {mejor[1]:+d}°, inclinación {mejor[2]:+d}°")
    for f in range(a, b + 1):
        rot, lens = curva(n, pts, a, b, f, f0, hfov, vfov)
        cam.location = L
        cam.rotation_quaternion = (base @ rot).to_quaternion()
        cam.data.lens = lens
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_quaternion", frame=f)
        cam.data.keyframe_insert("lens", frame=f)
for fc in cam.animation_data.action.fcurves:
    for k in fc.keyframe_points:
        k.interpolation = "CONSTANT"
respaldo("04_camara")

# ---------------------------------------------------------------- control de encuadre por plano
for n, a, b, _ in SH:
    malos = {"J": 0, "S": 0}
    for f in range(a, b + 1):
        if f >= T(27.4):
            continue
        sc.frame_set(f)
        for q, o in (("J", jt), ("S", st)):
            if q in QUIEN[n][0] + QUIEN[n][1]:
                c = world_to_camera_view(sc, cam, o.matrix_world.translation)
                if not (0.04 < c.x < 0.96 and 0.04 < c.y < 0.96 and c.z > 0.3):
                    malos[q] += 1
    print(f"PLANO {n:2d} {a:3d}-{b:3d} fuera: John {malos['J']}  sombra {malos['S']}  (obligatorio: {QUIEN[n][0] or '-'}, deseable: {QUIEN[n][1] or '-'})")

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
