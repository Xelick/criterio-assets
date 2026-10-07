# -*- coding: utf-8 -*-
"""
Criterio - Array + UCX (Maya)

Herramienta para piezas modulares (vallas, muros, rieles, etc.):

  1. Activa el snap por pasos del Move Tool (por defecto 5 m) para que al
     mover el mesh salte de 5 en 5 metros.
  2. Duplica el mesh seleccionado N veces, cada copia separada por el paso
     a lo largo del eje elegido.
  3. Estira el collider UCX (convencion de Unreal: UCX_<Mesh> o
     UCX_<Mesh>_00) para que cubra desde el inicio de la primera pieza
     hasta el final de la ultima, solo en ese eje.

Uso:
  - Pegar este archivo en el Script Editor (pestana Python) y ejecutar, o
  - Copiarlo a la carpeta de scripts de Maya y correr:
        import criterio_array_ucx
        criterio_array_ucx.show()
"""

import re

import maya.cmds as cmds

WINDOW = "criterioArrayUcxWin"

# Cuantas unidades de escena hay en 1 metro, segun Preferences > Settings > Linear.
UNITS_PER_METER = {
    "mm": 1000.0,
    "millimeter": 1000.0,
    "cm": 100.0,
    "centimeter": 100.0,
    "m": 1.0,
    "meter": 1.0,
    "km": 0.001,
    "kilometer": 0.001,
    "in": 39.3700787,
    "inch": 39.3700787,
    "ft": 3.2808399,
    "foot": 3.2808399,
    "yd": 1.0936133,
    "yard": 1.0936133,
}

AXES = ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]
AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def scene_units_per_meter():
    unit = cmds.currentUnit(query=True, linear=True)
    return UNITS_PER_METER.get(unit, 100.0)


def default_step():
    """5 metros expresados en las unidades de la escena (500 si la escena esta en cm)."""
    return 5.0 * scene_units_per_meter()


def parse_axis(label):
    """'+X' -> (0, 1.0), '-Z' -> (2, -1.0)"""
    sign = -1.0 if label.startswith("-") else 1.0
    return AXIS_INDEX[label[-1]], sign


def short_name(node):
    return node.split("|")[-1].split(":")[-1]


def is_ucx(node):
    return short_name(node).upper().startswith("UCX_")


def mesh_shapes(transform):
    """Shapes de tipo mesh directamente bajo el transform (sin intermedios)."""
    shapes = cmds.listRelatives(transform, shapes=True, type="mesh",
                                noIntermediate=True, fullPath=True) or []
    return shapes


def selected_meshes():
    """Transforms seleccionados que tienen mesh y no son colliders UCX."""
    sel = cmds.ls(selection=True, type="transform", long=True) or []
    return [n for n in sel if mesh_shapes(n) and not is_ucx(n)]


def find_ucx(mesh):
    """Busca el collider de un mesh: UCX_<Mesh> o UCX_<Mesh>_NN (hijo o en la escena)."""
    name = short_name(mesh)
    pattern = re.compile(r"^UCX_{0}(_\d+)?$".format(re.escape(name)), re.IGNORECASE)

    found = []
    candidates = cmds.ls("UCX_{0}*".format(name), "*:UCX_{0}*".format(name),
                         type="transform", long=True) or []
    for node in candidates:
        if pattern.match(short_name(node)) and mesh_shapes(node):
            found.append(node)
    return sorted(set(found))


def world_bounds(transforms):
    """Bounding box en mundo SOLO de los shapes de los transforms (ignora hijos como UCX)."""
    shapes = []
    for t in transforms:
        shapes.extend(mesh_shapes(t))
    if not shapes:
        return None
    return cmds.exactWorldBoundingBox(shapes)  # xmin, ymin, zmin, xmax, ymax, zmax


# ---------------------------------------------------------------------------
# Snap del Move Tool
# ---------------------------------------------------------------------------

def enable_move_snap(step, relative=False):
    """Hace que el Move Tool avance por pasos de `step` unidades."""
    try:
        cmds.manipMoveContext("Move", edit=True, snap=True, snapValue=step,
                              snapRelative=relative)
    except TypeError:
        cmds.warning("Tu version de Maya no tiene step snap en el Move Tool; "
                     "usa 'Grilla = paso' y mueve con la tecla X.")
        return
    cmds.setToolTo("moveSuperContext")
    cmds.inViewMessage(amg="Move Tool: snap cada <hl>{0:g}</hl> unidades".format(step),
                       pos="topCenter", fade=True)


def disable_move_snap():
    cmds.manipMoveContext("Move", edit=True, snap=False)
    cmds.inViewMessage(amg="Move Tool: snap <hl>desactivado</hl>",
                       pos="topCenter", fade=True)


def set_grid(step):
    """Grilla con una linea cada `step` unidades (sirve para snap con la tecla X)."""
    cmds.grid(spacing=step, divisions=1, size=max(step * 20, cmds.grid(query=True, size=True)))


def align_to_step(step, axis_label):
    """Redondea la posicion de la seleccion al multiplo de `step` mas cercano en el eje."""
    axis, _ = parse_axis(axis_label)
    meshes = selected_meshes()
    if not meshes:
        cmds.warning("Selecciona al menos un mesh.")
        return
    cmds.undoInfo(openChunk=True, chunkName="criterioAlignToStep")
    try:
        for node in meshes:
            pos = cmds.xform(node, query=True, worldSpace=True, translation=True)
            pos[axis] = round(pos[axis] / step) * step
            cmds.xform(node, worldSpace=True, translation=pos)
    finally:
        cmds.undoInfo(closeChunk=True)


# ---------------------------------------------------------------------------
# UCX
# ---------------------------------------------------------------------------

def fit_ucx_along_axis(ucx, start, end, axis):
    """
    Estira los vertices del UCX (en espacio mundo) para que en `axis` vaya de
    `start` a `end`. Es un estiramiento lineal en un solo eje, asi que el
    collider sigue siendo convexo y los otros dos ejes no cambian.
    """
    flat = cmds.xform("{0}.vtx[*]".format(ucx), query=True, worldSpace=True, translation=True)
    points = [flat[i:i + 3] for i in range(0, len(flat), 3)]
    values = [p[axis] for p in points]
    old_min, old_max = min(values), max(values)
    old_len = old_max - old_min
    if old_len < 1e-6:
        cmds.warning("{0} no tiene largo en ese eje; no se puede estirar.".format(short_name(ucx)))
        return False

    scale = (end - start) / old_len
    for i, p in enumerate(points):
        p[axis] = start + (p[axis] - old_min) * scale
        cmds.xform("{0}.vtx[{1}]".format(ucx, i), worldSpace=True, translation=p)
    return True


def fit_ucx_to_pieces(pieces, axis, ucx_nodes=None):
    """Ajusta los UCX del primer mesh para que cubran todas las piezas en el eje."""
    if ucx_nodes is None:
        ucx_nodes = find_ucx(pieces[0])
    if not ucx_nodes:
        cmds.warning("No encontre UCX_{0} ni UCX_{0}_00.".format(short_name(pieces[0])))
        return []

    bounds = world_bounds(pieces)
    start, end = bounds[axis], bounds[axis + 3]
    fitted = []
    for ucx in ucx_nodes:
        if fit_ucx_along_axis(ucx, start, end, axis):
            fitted.append(ucx)
    return fitted


def fit_ucx_to_selection(axis_label):
    """Boton: selecciona todas las piezas (y opcionalmente el UCX) y ajusta."""
    axis, _ = parse_axis(axis_label)
    sel = cmds.ls(selection=True, type="transform", long=True) or []
    pieces = [n for n in sel if mesh_shapes(n) and not is_ucx(n)]
    ucx_nodes = [n for n in sel if is_ucx(n) and mesh_shapes(n)] or None
    if not pieces:
        cmds.warning("Selecciona las piezas (mesh) que debe cubrir el UCX.")
        return
    cmds.undoInfo(openChunk=True, chunkName="criterioFitUcx")
    try:
        fitted = fit_ucx_to_pieces(pieces, axis, ucx_nodes)
    finally:
        cmds.undoInfo(closeChunk=True)
    if fitted:
        print("UCX ajustado: {0}".format(", ".join(short_name(u) for u in fitted)))


# ---------------------------------------------------------------------------
# Array
# ---------------------------------------------------------------------------

def _duplicate_one(mesh, as_instance):
    if as_instance:
        # Se instancia solo el shape bajo un transform nuevo, asi la instancia
        # no comparte los hijos (UCX) del original.
        parent = cmds.listRelatives(mesh, parent=True, fullPath=True)
        kwargs = {"parent": parent[0]} if parent else {}
        new = cmds.createNode("transform", name="{0}_inst1".format(short_name(mesh)),
                              skipSelect=True, **kwargs)
        new = cmds.ls(new, long=True)[0]
        cmds.xform(new, worldSpace=True,
                   matrix=cmds.xform(mesh, query=True, worldSpace=True, matrix=True))
        cmds.parent(mesh_shapes(mesh)[0], new, addObject=True, shape=True)
        return new

    new = cmds.ls(cmds.duplicate(mesh, returnRootsOnly=True)[0], long=True)[0]
    # Las copias no llevan su propio UCX: el collider del original cubre todo.
    children = cmds.listRelatives(new, children=True, type="transform", fullPath=True) or []
    ucx_children = [c for c in children if is_ucx(c)]
    if ucx_children:
        cmds.delete(ucx_children)
    return new


def make_array(total, step, axis_label, as_instance=False, fit_ucx=True, group=False):
    """
    Crea `total` piezas en fila (la original cuenta como la primera), separadas
    `step` unidades en el eje elegido, y estira el UCX de principio a fin.
    """
    meshes = selected_meshes()
    if len(meshes) != 1:
        cmds.warning("Selecciona un solo mesh (no el UCX).")
        return []
    if total < 2:
        cmds.warning("El total tiene que ser 2 o mas.")
        return []

    mesh = meshes[0]
    axis, sign = parse_axis(axis_label)

    cmds.undoInfo(openChunk=True, chunkName="criterioArray")
    try:
        pieces = [mesh]
        for i in range(1, total):
            new = _duplicate_one(mesh, as_instance)
            offset = [0.0, 0.0, 0.0]
            offset[axis] = sign * step * i
            cmds.move(offset[0], offset[1], offset[2], new, relative=True, worldSpace=True)
            pieces.append(new)

        fitted = fit_ucx_to_pieces(pieces, axis) if fit_ucx else []

        if group:
            grp = cmds.group(pieces[1:], name="{0}_array_grp".format(short_name(mesh)))
            pieces = [mesh] + (cmds.listRelatives(grp, children=True, fullPath=True) or [])

        cmds.select(pieces, replace=True)
    finally:
        cmds.undoInfo(closeChunk=True)

    msg = "{0} piezas cada {1:g} en {2}".format(total, step, axis_label)
    if fitted:
        msg += " | UCX ajustado"
    elif fit_ucx:
        msg += " | <hl>sin UCX</hl>"
    cmds.inViewMessage(amg=msg, pos="topCenter", fade=True)
    return pieces


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def show():
    if cmds.window(WINDOW, exists=True):
        cmds.deleteUI(WINDOW)

    unit = cmds.currentUnit(query=True, linear=True)
    cmds.window(WINDOW, title="Criterio - Array + UCX", sizeable=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnAttach=("both", 8))

    cmds.separator(height=6, style="none")
    step_field = cmds.floatFieldGrp(label="Paso ({0})".format(unit), value1=default_step(),
                                    precision=3, columnWidth2=(110, 120),
                                    annotation="5 m = {0:g} {1}".format(default_step(), unit))
    axis_menu = cmds.optionMenuGrp(label="Eje", columnWidth2=(110, 120))
    for a in AXES:
        cmds.menuItem(label=a)

    def step():
        return cmds.floatFieldGrp(step_field, query=True, value1=True)

    def axis():
        return cmds.optionMenuGrp(axis_menu, query=True, value=True)

    cmds.frameLayout(label="Mover de a pasos", collapsable=False, marginWidth=6, marginHeight=6)
    relative_cb = cmds.checkBox(label="Paso relativo (desde donde esta)", value=False)
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
    cmds.button(label="Activar snap", height=28,
                command=lambda *_: enable_move_snap(
                    step(), cmds.checkBox(relative_cb, query=True, value=True)))
    cmds.button(label="Desactivar", height=28, command=lambda *_: disable_move_snap())
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
    cmds.button(label="Alinear seleccion al paso", height=24,
                command=lambda *_: align_to_step(step(), axis()))
    cmds.button(label="Grilla = paso", height=24, command=lambda *_: set_grid(step()))
    cmds.setParent("..")
    cmds.setParent("..")

    cmds.frameLayout(label="Duplicar en fila", collapsable=False, marginWidth=6, marginHeight=6)
    total_field = cmds.intFieldGrp(label="Total de piezas", value1=10, columnWidth2=(110, 120),
                                   annotation="Incluye la original: 10 = original + 9 copias")
    instance_cb = cmds.checkBox(label="Usar instancias en vez de copias", value=False)
    ucx_cb = cmds.checkBox(label="Estirar UCX de principio a fin", value=True)
    group_cb = cmds.checkBox(label="Agrupar las copias", value=False)
    cmds.button(label="Crear", height=32, backgroundColor=(0.35, 0.55, 0.35),
                command=lambda *_: make_array(
                    cmds.intFieldGrp(total_field, query=True, value1=True),
                    step(), axis(),
                    as_instance=cmds.checkBox(instance_cb, query=True, value=True),
                    fit_ucx=cmds.checkBox(ucx_cb, query=True, value=True),
                    group=cmds.checkBox(group_cb, query=True, value=True)))
    cmds.setParent("..")

    cmds.frameLayout(label="UCX", collapsable=False, marginWidth=6, marginHeight=6)
    cmds.text(label="Selecciona todas las piezas (y el UCX si tiene otro nombre)",
              align="left")
    cmds.button(label="Ajustar UCX a la seleccion", height=28,
                command=lambda *_: fit_ucx_to_selection(axis()))
    cmds.setParent("..")

    cmds.separator(height=6, style="none")
    cmds.showWindow(WINDOW)


if __name__ == "__main__":
    show()
