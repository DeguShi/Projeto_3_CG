"""
SCC0250 - Computação Gráfica - Projeto 3

Felipe Azambuja - 14675437
Luiz Fellipe Catuzzi Araujo Hotoshi - 11871198


Nós tentamos fazer uma ilha e uma casa que remetessem a sensação de tranquilidade com que o Mestre Kame (DB) vivia.
Claro, dadas as limitações do projeto e a baixa diversidade de modelos gratuitos com textura disponíveis para essa construção,
fizemos mudanças cabíveis, mas mantivemos a essência. No lugar das revistas que o Kame costumava ler, adicionamos outra forma de
entretenimento, um notebook com segundo monitor e uma cadeira ergonomica para garantir a gameplay. Porém, assim como no anime, o maior
lazer é ficar em uma cadeira de praia do lado de fora, aproveitando a vista para o mar sob a sombra de um guarda sol (e uma garrafinha de água, para ficar hidratado).

Adicionamos também muitos outros objetos. O objetivo não era fazer o mínimo entregavel, mas sim construir um ambiente coerente e que
fosse interessante de explorar.

O Projeto 3 adiciona iluminação Phong completa: 3 fontes de luz com separação indoor/outdoor, normais por face por fragmento,
parâmetros de material (ka, kd, ks, shininess) definidos manualmente por objeto e controles interativos de iluminação.

Controles:
  WASD e mouse: mover a câmera
  Shift + WASD: mover a câmera mais rápido
  Shift + qualquer comando de alteração nos objetos também acelera o movimento.
  Setas: mover a cadeira de praia (a luz externa segue junto)
  Q e E: girar a cadeira interna
  Z e X: mudar o tamanho do guarda-sol
  Scroll: mudar o zoom
  P: alternar malha (wireframe)
  ESC: sair

Iluminação (Projeto 3):
  1: ligar/desligar luz ambiente global
  2: ligar/desligar luz externa (segue a cadeira de praia)
  3: ligar/desligar abajur (luz interna quente)
  4: ligar/desligar luz de teto (luz interna fria)
  J / K: diminuir / aumentar intensidade da luz ambiente
  N / M: diminuir / aumentar multiplicador difuso
  U / I: diminuir / aumentar multiplicador especular
  Shift + J/K/N/M/U/I: ajuste 3x mais rápido
"""

import ctypes
import json
import math
import os
from dataclasses import dataclass, field
from typing import Callable

import glfw
import glm
import numpy as np
from OpenGL.GL import *
from PIL import Image

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(globals().get("__file__", os.getcwd())))
if not os.path.exists(os.path.join(BASE, "assets")):
    candidate_base = os.path.join(BASE, "Projeto_2_CG")
    if os.path.exists(os.path.join(candidate_base, "assets")):
        BASE = candidate_base
ASSETS = os.path.join(BASE, "assets")
MODELS = os.path.join(ASSETS, "models")
TEXTURES = os.path.join(ASSETS, "textures")
SKY = os.path.join(ASSETS, "sky")

BED_OBJ = os.path.join(MODELS, "bed", "bed.obj")
BED_TEX = os.path.join(MODELS, "bed", "bed_diffuse.png")

CARPET_OBJ = os.path.join(MODELS, "carpet", "carpet.obj")
CARPET_TEX = os.path.join(MODELS, "carpet", "carpet_diffuse.png")

DESK_OBJ = os.path.join(MODELS, "desk", "desk.obj")
DESK_TEX = os.path.join(MODELS, "desk", "desk_diffuse.png")

UMBRELLA_OBJ = os.path.join(MODELS, "beach_umbrella", "beach_umbrella.obj")
UMBRELLA_PANEL_RED_TEX = os.path.join(MODELS, "beach_umbrella", "panel_red.png")
UMBRELLA_PANEL_YELLOW_TEX = os.path.join(MODELS, "beach_umbrella", "panel_yellow.png")
UMBRELLA_PANEL_BLUE_TEX = os.path.join(MODELS, "beach_umbrella", "panel_blue.png")

TABLE_OBJ = os.path.join(MODELS, "round_table", "round_table.obj")
TABLE_TEX = os.path.join(MODELS, "round_table", "round_table_diffuse.png")

CHAIR_OBJ = os.path.join(MODELS, "office_chair", "office_chair.obj")
CHAIR_LEATHER_TEX = os.path.join(MODELS, "office_chair", "leather_diffuse.jpg")
CHAIR_FABRIC_TEX = os.path.join(MODELS, "office_chair", "fabric_diffuse.jpg")

LAMP_OBJ = os.path.join(MODELS, "lamp", "lamp.obj")
LAMP_TEX = os.path.join(MODELS, "lamp", "lamp_diffuse.png")

LAPTOP_OBJ = os.path.join(MODELS, "laptop", "laptop.obj")
LAPTOP_TEX = os.path.join(MODELS, "laptop", "laptop_diffuse.png")

PILLOW_OBJ = os.path.join(MODELS, "pillow", "pillow.obj")
PILLOW_TEX = os.path.join(MODELS, "pillow", "pillow_diffuse.jpg")

PC_OBJ = os.path.join(MODELS, "pc", "pc.obj")
PC_TEX = os.path.join(MODELS, "pc", "pc_diffuse.jpg")

ROOM_OBJ = os.path.join(MODELS, "room", "room.obj")
ROOM_WALL_TEX = os.path.join(MODELS, "room", "wall_diffuse.jpg")
ROOM_DOOR_TEX = os.path.join(MODELS, "room", "door_diffuse.jpg")
ROOM_GLASS_TEX = os.path.join(MODELS, "room", "glass_diffuse.jpg")
ROOM_HANDLE_TEX = os.path.join(MODELS, "room", "handle_diffuse.jpg")
ROOM_HANDLE_PLASTIC_TEX = os.path.join(MODELS, "room", "window_handle_diffuse.jpg")

BEACH_CHAIR_OBJ = os.path.join(MODELS, "beach_chair", "beach_chair.obj")
BEACH_CHAIR_WOOD_TEX = os.path.join(MODELS, "beach_chair", "wood_diffuse.png")
BEACH_CHAIR_FABRIC_TEX = os.path.join(MODELS, "beach_chair", "fabric_diffuse.png")

BOTTLE_OBJ = os.path.join(MODELS, "bottle", "bottle.obj")
BOTTLE_TEX = os.path.join(MODELS, "bottle", "bottle_diffuse.png")

WELL_OBJ = os.path.join(MODELS, "well", "well.obj")
WELL_STONE_TEX = os.path.join(MODELS, "well", "stone_diffuse.png")
WELL_WOOD_TEX = os.path.join(MODELS, "well", "wood_diffuse.png")
WELL_ROOF_TEX = os.path.join(MODELS, "well", "roof_diffuse.png")
WELL_ROPE_TEX = os.path.join(MODELS, "well", "rope_diffuse.png")

HANGER_OBJ = os.path.join(MODELS, "hanger", "hanger.obj")
HANGER_TEX = os.path.join(MODELS, "hanger", "hanger_diffuse.png")

BOAT_OBJ = os.path.join(MODELS, "boat", "boat.obj")
BOAT_BODY_TEX = os.path.join(MODELS, "boat", "body_diffuse.jpg")
BOAT_PADDLE_TEX = os.path.join(MODELS, "boat", "paddle_diffuse.jpg")

HAT_OBJ = os.path.join(MODELS, "hat", "hat.obj")
HAT_TEX = os.path.join(MODELS, "hat", "hat_diffuse.jpg")

TILE_OBJ = os.path.join(MODELS, "roof_tile", "roof_tile.obj")

WOOD_TEX = os.path.join(TEXTURES, "floor_wood.jpg")
CEILING_TEX = os.path.join(TEXTURES, "ceiling_wood.jpg")
SAND_TEX = os.path.join(TEXTURES, "sand.jpg")
WATER_TEX = os.path.join(TEXTURES, "water.jpg")
SKY_PANO = os.path.join(SKY, "panorama.jpg")

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
WIN_W, WIN_H = 1280, 720
SKYBOX_HALF  = 48.0
CAM_SPEED    = 8.0
MOUSE_SENS   = 0.15

ROOM_SCALE = 1.5
ROOM_TX    = -3.0
ROOM_TZ    = 3.0
ROOM_FLOOR_Y = 0.51
ROOM_BASE_STRIP_H = 0.12
ROOM_TY = ROOM_FLOOR_Y - ROOM_BASE_STRIP_H
ROOM_CEIL_Y = ROOM_TY + 2.4
ROOM_DOOR_HINGE_X = 0.061
ROOM_DOOR_HINGE_Z = -1.664
ROOM_DOOR_OPEN_DEG = 45.0
ROOM_LOCAL_CENTER_X = 2.0
ROOM_LOCAL_CENTER_Z = -2.0
ROOF_TILE_COLS = 3
ROOF_TILE_ROWS = 4
ROOF_TILE_SPACING_X = 2.85
ROOF_TILE_SPACING_Z = 1.70
ROOF_TILE_Y = ROOM_CEIL_Y + 0.025
BEACH_CHAIR_MIN_X = -8.4
BEACH_CHAIR_MAX_X = -5.8
BEACH_CHAIR_MIN_Z = 1.3
BEACH_CHAIR_MAX_Z = 4.0
UMBRELLA_INDEX = 7
INDOOR_CHAIR_INDEX = 9
BEACH_CHAIR_INDEX = 10

# ---------------------------------------------------------------------------
# Listas globais da cena
# ---------------------------------------------------------------------------
vertices_list:  list = []
texcoords_list: list = []
normals_list:   list = []

# ---------------------------------------------------------------------------
# Lighting state
# ---------------------------------------------------------------------------
INDOOR  = 0
OUTDOOR = 1

ambient_enabled:  int   = 1
light_enabled:    list  = [1, 1, 1]   # [outdoor, abajur, ceiling]
ambient_strength: float = 0.5
ambient_color:    list  = [1.0, 0.96, 0.88]   # warm daylight white — sky environment tint
diffuse_mult:     float = 1.0
specular_mult:    float = 1.0

# Sandbox / light tuning mode  (F1 to toggle, F5 to save)
sandbox_mode:  bool = False
sandbox_light: int  = 0   # 0=outdoor, 1=abajur, 2=ceiling

# Mutable light positions  (loaded from lighting_config.json if present)
outdoor_offset:        list = [0.0, 3.0, -60.0]        # sunset sun: 180 deg from the door-facing reference
abajur_pos:            list = [2.4, 1.85, 2.4]
ceiling_pos:           list = [0.0, ROOM_CEIL_Y - 0.20, 0.0]  # centre of ceiling quad
light_intensities_cfg:  list  = [1.0, 0.8, 0.6]      # [outdoor, abajur, ceiling]
sky_brightness:         float = 1.5                   # emissiveMult for the sky sphere
sandbox_marker_scale:   float = 0.14                  # edge length of sandbox light cubes

# ---------------------------------------------------------------------------
# Câmera
# ---------------------------------------------------------------------------
camera_pos   = glm.vec3(0.0, 1.7, 1.5)
camera_front = glm.vec3(0.0, 0.0, -1.0)
camera_up    = glm.vec3(0.0, 1.0, 0.0)
yaw          = -90.0
pitch        = 0.0
fov          = 45.0
first_mouse  = True
last_x       = WIN_W / 2.0
last_y       = WIN_H / 2.0
delta_time   = 0.0
last_frame   = 0.0
wireframe    = False

@dataclass
class MatConfig:
    tex_path:     str | None = None
    color:        tuple[float, float, float, float] = (0.85, 0.85, 0.85, 1.0)
    double_sided: bool  = False
    force_planar: bool  = False
    min_y:        float | None = None

@dataclass
class ObjState:
    name:     str
    obj_path: str
    tex_path: str | None = None
    mat_configs: dict[str, MatConfig] | None = None
    tex_id:   int   = 0
    start:    int   = 0
    count:    int   = 0
    tx: float = 0.0
    ty: float = 0.0
    tz: float = 0.0
    angle_y: float = 0.0
    angle_x: float = 0.0
    scale:   float = 1.0
    parts: list = field(default_factory=list)
    # Lighting / material
    zone:      int   = OUTDOOR
    ka:        float = 0.25
    kd:        float = 0.75
    ks:        float = 0.20
    shininess: float = 16.0

objects: list[ObjState] = [
    ObjState("Cama",         BED_OBJ,      BED_TEX,
             tx=-1.746, ty=0.5, tz=-1.7, scale=0.008279299465445972),
    ObjState("Tapete",       CARPET_OBJ,   CARPET_TEX,
             tx=0.9,  ty=ROOM_FLOOR_Y, tz=-1.2, scale=1.0),
    ObjState("Escrivaninha", DESK_OBJ,     DESK_TEX,
             tx=2.2,  ty=0.5,  tz=1.8, angle_x=270.0, scale=1.0),
    ObjState("Abajur",       LAMP_OBJ,     LAMP_TEX,
             tx=2.4,  ty=1.17, tz=2.4, angle_y=198.0, scale=1.0),
    ObjState("Laptop",       LAPTOP_OBJ,   LAPTOP_TEX,
             tx=2.0,  ty=1.165, tz=1.8, angle_y=270.0, scale=0.08508543750000001),
    ObjState("Travesseiro",  PILLOW_OBJ,   PILLOW_TEX,
             tx=-1.402, ty=0.986, tz=-2.3, angle_x=93.0,
             scale=0.007106813301301213),
    ObjState("PC",           PC_OBJ,       tex_path=None,
             mat_configs={
                 "Material.001": MatConfig(color=(0.85, 0.85, 0.85, 1.0)),
                 "Material.002": MatConfig(tex_path=PC_TEX),
             },
             tx=2.2,  ty=1.17, tz=1.3, angle_y=294.0, scale=0.5303213506452944),
    ObjState("Guarda-sol",   UMBRELLA_OBJ, tex_path=None,
             mat_configs={
                 "Material.001": MatConfig(tex_path=UMBRELLA_PANEL_RED_TEX),
                 "Material.002": MatConfig(tex_path=UMBRELLA_PANEL_YELLOW_TEX),
                 "Material.003": MatConfig(tex_path=UMBRELLA_PANEL_BLUE_TEX),
                 "Material.004": MatConfig(tex_path=UMBRELLA_PANEL_RED_TEX),
                 "Material.006": MatConfig(tex_path=UMBRELLA_PANEL_YELLOW_TEX),
             },
             tx=-7.6, ty=1.5, tz=2.7, scale=0.38783205399462906),
    ObjState("Mesa redonda", TABLE_OBJ,    TABLE_TEX,
             tx=-7.0, ty=0.5, tz=2.2, scale=0.22),
    ObjState("Cadeira",      CHAIR_OBJ,    tex_path=None,
             mat_configs={
                 "Black_Fabric":  MatConfig(tex_path=CHAIR_FABRIC_TEX),
                 "Black_Leather": MatConfig(tex_path=CHAIR_LEATHER_TEX),
                 "Black_Plasic":  MatConfig(color=(0.1, 0.1, 0.1, 1.0)),
                 "Chrome":        MatConfig(color=(0.9, 0.9, 0.9, 1.0)),
                 "Grey_Plasic":   MatConfig(color=(0.5, 0.5, 0.5, 1.0)),
             },
             tx=1.6,  ty=0.51, tz=2.1, angle_y=156.0, scale=1.0),
    ObjState("Cadeira de Praia", BEACH_CHAIR_OBJ, tex_path=None,
             mat_configs={
                 "__default__":   MatConfig(tex_path=BEACH_CHAIR_FABRIC_TEX),
                 "madera":        MatConfig(tex_path=BEACH_CHAIR_WOOD_TEX),
                 "Material":      MatConfig(color=(0.1, 0.1, 0.1, 1.0)),
                 "Material.001":  MatConfig(color=(0.1, 0.1, 0.1, 1.0)),
                 "Material.002":  MatConfig(color=(0.1, 0.1, 0.1, 1.0)),
                 "Material.003":  MatConfig(color=(0.25, 0.25, 0.25, 1.0)),
                 "Material.004":  MatConfig(color=(0.47, 0.47, 0.47, 1.0)),
                 "Material.005":  MatConfig(color=(0.47, 0.47, 0.47, 1.0)),
                 "Material.006":  MatConfig(color=(0.5, 0.5, 0.5, 1.0)),
             },
             tx=-7.0, ty=0.67, tz=3.2, angle_y=177.0, angle_x=0.5,
             scale=0.0681858183272711),
    ObjState("Garrafa",      BOTTLE_OBJ,   BOTTLE_TEX,
             tx=-7.094, ty=1.142, tz=2.208, scale=0.019413948597220235),
    ObjState("Poco",         WELL_OBJ,     tex_path=None,
             mat_configs={
                 "VR_well_part1SG": MatConfig(tex_path=WELL_STONE_TEX),
                 "VR_well_part2SG": MatConfig(tex_path=WELL_WOOD_TEX),
                 "VR_well_part3SG": MatConfig(tex_path=WELL_ROOF_TEX),
                 "VR_well_part4SG": MatConfig(tex_path=WELL_ROPE_TEX),
             },
             tx=-0.458, ty=0.5, tz=6.368, angle_y=-20.0,
             scale=0.06677524164760051),
    ObjState("Cabide",       HANGER_OBJ,   HANGER_TEX,
             tx=1.842, ty=1.362, tz=-2.23, angle_y=90.0, scale=0.8765242952014003),
    ObjState("Barco",        BOAT_OBJ,     tex_path=None,
             mat_configs={
                 r"E:\BlackDesert\character\texture\RS_02_Ship_0002.dds":
                     MatConfig(tex_path=BOAT_PADDLE_TEX),
                 r"E:\BlackDesert\character\texture\PRS_01_body_0006.dds":
                     MatConfig(tex_path=BOAT_BODY_TEX),
                 r"E:\BlackDesert\character\texture\PRS_01_body_0006.dds_Mesh_001_LOD_0":
                     MatConfig(tex_path=BOAT_BODY_TEX),
                 r"E:\BlackDesert\character\texture\PRS_01_body_0006.dds_Mesh_003_LOD_0":
                     MatConfig(tex_path=BOAT_BODY_TEX),
             },
             tx=-12.602, ty=0.25, tz=-6.88, angle_y=35.0, angle_x=350.0,
             scale=0.0052723831644418346),
    ObjState("Chapeu",       HAT_OBJ,      HAT_TEX,
             tx=1.76, ty=1.83, tz=-2.12, angle_y=-25.0, angle_x=67.3,
             scale=0.011854604134553292),
    ObjState("Travesseiro 2", PILLOW_OBJ,   PILLOW_TEX,
             tx=-2.12, ty=0.872, tz=-2.32, angle_y=2.0, angle_x=272.0,
             scale=0.008114301686507872),
]

# (zone, ka, kd, ks, shininess)  — set manually, not from .mtl
_OBJ_MAT: dict[str, tuple] = {
    "Cama":            (INDOOR,  0.25, 0.85, 0.08,   8.0),
    "Tapete":          (INDOOR,  0.25, 0.90, 0.04,   6.0),
    "Escrivaninha":    (INDOOR,  0.25, 0.75, 0.25,  24.0),
    "Abajur":          (INDOOR,  0.25, 0.65, 0.35,  32.0),
    "Laptop":          (INDOOR,  0.20, 0.55, 0.70,  64.0),
    "Travesseiro":     (INDOOR,  0.25, 0.85, 0.08,   8.0),
    "PC":              (INDOOR,  0.20, 0.45, 0.80,  96.0),
    "Guarda-sol":      (OUTDOOR, 0.25, 0.85, 0.15,  16.0),
    "Mesa redonda":    (OUTDOOR, 0.25, 0.70, 0.45,  48.0),
    "Cadeira":         (INDOOR,  0.25, 0.65, 0.35,  32.0),
    "Cadeira de Praia":(OUTDOOR, 0.25, 0.65, 0.35,  32.0),
    "Garrafa":         (OUTDOOR, 0.15, 0.35, 0.95, 128.0),
    "Poco":            (OUTDOOR, 0.25, 0.70, 0.25,  24.0),
    "Cabide":          (INDOOR,  0.25, 0.65, 0.25,  24.0),
    "Barco":           (OUTDOOR, 0.25, 0.70, 0.40,  48.0),
    "Chapeu":          (INDOOR,  0.25, 0.80, 0.10,  10.0),
    "Travesseiro 2":   (INDOOR,  0.25, 0.85, 0.08,   8.0),
}
for _obj in objects:
    if _obj.name in _OBJ_MAT:
        _obj.zone, _obj.ka, _obj.kd, _obj.ks, _obj.shininess = _OBJ_MAT[_obj.name]

# ---------------------------------------------------------------------------
# Leitura de OBJ
# ---------------------------------------------------------------------------

def _project2d(pts3d: list) -> list:
    dx = max(p[0] for p in pts3d) - min(p[0] for p in pts3d)
    dy = max(p[1] for p in pts3d) - min(p[1] for p in pts3d)
    dz = max(p[2] for p in pts3d) - min(p[2] for p in pts3d)
    if dx <= dy and dx <= dz:
        return [(p[1], p[2]) for p in pts3d]
    if dy <= dx and dy <= dz:
        return [(p[0], p[2]) for p in pts3d]
    return [(p[0], p[1]) for p in pts3d]


def _ear_clip(pts2d: list) -> list:
    """Triangula polígonos simples."""
    n = len(pts2d)
    if n < 3:
        return []
    if n == 3:
        return [0, 1, 2]

    def cross2d(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def in_tri(p, a, b, c):
        d1 = cross2d(a, b, p); d2 = cross2d(b, c, p); d3 = cross2d(c, a, p)
        return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))

    area = sum(cross2d(pts2d[0], pts2d[i], pts2d[i + 1]) for i in range(1, n - 1))
    remain = list(range(n)) if area >= 0 else list(range(n - 1, -1, -1))

    result: list = []
    for _ in range(n * n):
        if len(remain) <= 3:
            break
        m = len(remain)
        for i in range(m):
            pi = remain[(i - 1) % m]; ci = remain[i]; ni = remain[(i + 1) % m]
            a, b, c = pts2d[pi], pts2d[ci], pts2d[ni]
            if cross2d(a, b, c) <= 1e-10:
                continue
            if all(j in (pi, ci, ni) or not in_tri(pts2d[j], a, b, c) for j in remain):
                result += [pi, ci, ni]
                remain.pop(i)
                break
        else:
            # Caso degenerado: usa leque simples.
            for i in range(1, len(remain) - 1):
                result += [remain[0], remain[i], remain[i + 1]]
            remain = []
            break

    result += remain
    return result


def _emit_face(fv: list, ft: list, vertices: list, tex_coords: list,
               has_uv: bool, planar_fn=None,
               fn: list | None = None, obj_normals: list | None = None) -> None:
    """Adiciona uma face OBJ triangulada nas listas globais.

    Usa normais do OBJ (vn) quando disponíveis; caso contrário calcula normal
    plana por produto vetorial.
    """
    dummy = ["0.0", "0.0"]
    n = len(fv)
    if n < 3:
        return
    if n == 3:
        local_ids = [0, 1, 2]
    else:
        pts3d = [(float(vertices[vi - 1][0]), float(vertices[vi - 1][1]),
                  float(vertices[vi - 1][2])) for vi in fv]
        local_ids = _ear_clip(_project2d(pts3d))

    have_vn = fn is not None and obj_normals is not None and len(obj_normals) > 0

    for t in range(0, len(local_ids), 3):
        tri = local_ids[t:t + 3]
        if len(tri) < 3:
            continue
        if not have_vn:
            raw3 = [vertices[fv[li] - 1] for li in tri]
            flat_n = _face_normal(raw3)
        for li in tri:
            v = vertices[fv[li] - 1]
            vertices_list.append(v)
            if have_vn and fn[li] > 0:
                on = obj_normals[fn[li] - 1]
                normals_list.append([on[0], on[1], on[2]])
            else:
                nx, ny, nz = flat_n if not have_vn else _face_normal(
                    [vertices[fv[x] - 1] for x in tri])
                normals_list.append([str(nx), str(ny), str(nz)])
            if planar_fn is not None:
                texcoords_list.append(planar_fn(v))
            else:
                ti = ft[li]
                texcoords_list.append(tex_coords[ti - 1] if has_uv and ti > 0 else dummy)


def load_model_from_file(filename: str) -> dict:
    vertices, tex_coords, normals, faces = [], [], [], []
    for line in open(filename, "r", encoding="utf-8", errors="ignore"):
        vals = line.split()
        if not vals or vals[0].startswith("#"):
            continue
        if vals[0] == "v":
            vertices.append(vals[1:4])
        elif vals[0] == "vt":
            tex_coords.append(vals[1:3])
        elif vals[0] == "vn":
            normals.append(vals[1:4])
        elif vals[0] == "f":
            fv, ft, fn = [], [], []
            for tok in vals[1:]:
                parts = tok.split("/")
                fv.append(int(parts[0]))
                ft.append(int(parts[1]) if len(parts) >= 2 and parts[1] else 0)
                fn.append(int(parts[2]) if len(parts) >= 3 and parts[2] else 0)
            faces.append((fv, ft, fn))
    return {"vertices": vertices, "texture": tex_coords, "normals": normals, "faces": faces}


_texture_cache = {}
def get_texture(img_path: str) -> int:
    if img_path in _texture_cache:
        return _texture_cache[img_path]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_path).convert("RGB")
    
    # Reduz texturas grandes antes de enviar para a GPU.
    MAX_TEX_SIZE = 2048
    
    def _pot(v):
        return 2 ** round(math.log(v, 2))
        
    new_w = min(_pot(img.width), MAX_TEX_SIZE)
    new_h = min(_pot(img.height), MAX_TEX_SIZE)
    
    if new_w != img.width or new_h != img.height:
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.LANCZOS
        img = img.resize((new_w, new_h), resample_filter)
        
    w, h = img.size
    data = img.tobytes("raw", "RGB", 0, -1)   # -1 inverte para OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    _texture_cache[img_path] = tex_id
    return tex_id


def _load_model_with_groups(filename: str) -> tuple[list, list, list, list]:
    """Lê OBJ e separa faces por objeto e material."""
    vertices, tex_coords, normals = [], [], []
    groups: list[tuple[str, str, list]] = []
    cur_obj = "__default_obj__"
    cur_mat = "__default__"
    cur_faces: list = []
    for line in open(filename, "r", encoding="utf-8", errors="ignore"):
        vals = line.split()
        if not vals or vals[0].startswith("#"):
            continue
        if vals[0] == "v":
            vertices.append(vals[1:4])
        elif vals[0] == "vt":
            tex_coords.append(vals[1:3])
        elif vals[0] == "vn":
            normals.append(vals[1:4])
        elif vals[0] == "o":
            if cur_faces:
                groups.append((cur_obj, cur_mat, cur_faces))
                cur_faces = []
            cur_obj = vals[1] if len(vals) > 1 else "__default_obj__"
        elif vals[0] == "usemtl":
            if cur_faces:
                groups.append((cur_obj, cur_mat, cur_faces))
                cur_faces = []
            cur_mat = vals[1] if len(vals) > 1 else "__default__"
        elif vals[0] == "f":
            fv, ft, fn = [], [], []
            for tok in vals[1:]:
                p = tok.split("/")
                fv.append(int(p[0]))
                ft.append(int(p[1]) if len(p) >= 2 and p[1] else 0)
                fn.append(int(p[2]) if len(p) >= 3 and p[2] else 0)
            cur_faces.append((fv, ft, fn))
    if cur_faces:
        groups.append((cur_obj, cur_mat, cur_faces))
    return vertices, tex_coords, normals, groups


_PLANAR_TILE = 0.4


def _face_normal(verts_raw: list) -> tuple[float, float, float]:
    """Calcula a normal da face."""
    ax, ay, az = float(verts_raw[0][0]), float(verts_raw[0][1]), float(verts_raw[0][2])
    bx, by, bz = float(verts_raw[1][0]), float(verts_raw[1][1]), float(verts_raw[1][2])
    cx, cy, cz = float(verts_raw[2][0]), float(verts_raw[2][1]), float(verts_raw[2][2])
    e1x, e1y, e1z = bx - ax, by - ay, bz - az
    e2x, e2y, e2z = cx - ax, cy - ay, cz - az
    nx = e1y * e2z - e1z * e2y
    ny = e1z * e2x - e1x * e2z
    nz = e1x * e2y - e1y * e2x
    mag = (nx**2 + ny**2 + nz**2) ** 0.5 + 1e-9
    return nx / mag, ny / mag, nz / mag


def _planar_uv(vx: float, vy: float, vz: float,
               nx: float, ny: float, nz: float,
               tile: float) -> tuple[float, float]:
    """Gera coordenadas UV planares."""
    anx, any_, anz = abs(nx), abs(ny), abs(nz)
    if anx >= any_ and anx >= anz:
        return vz * tile, vy * tile   # parede em X
    elif anz >= anx and anz >= any_:
        return vx * tile, vy * tile   # parede em Z
    else:
        return vx * tile, vz * tile   # piso ou teto


def load_obj_multi(obj_path: str,
                   mat_configs: dict[str, MatConfig]) -> list[tuple]:
    """
    Carrega OBJ com materiais separados.
    Materiais texturizados sem UV usam mapeamento planar.
    """
    vertices, tex_coords, obj_normals, groups = _load_model_with_groups(obj_path)
    has_uv = len(tex_coords) > 0
    parts = []
    for obj_name, mat_name, faces in groups:
        cfg = mat_configs.get(f"{obj_name}:{mat_name}") or mat_configs.get(mat_name)
        if cfg is None:
            continue
        group_vertices = vertices
        if cfg.min_y is not None:
            group_vertices = [
                [v[0], str(max(float(v[1]), cfg.min_y)), v[2]]
                for v in vertices
            ]
        use_planar = cfg.tex_path is not None and (not has_uv or cfg.force_planar)
        start = len(vertices_list)
        for fv, ft, fn in faces:
            if use_planar:
                raw3 = [group_vertices[fv[i] - 1] for i in range(min(3, len(fv)))]
                flat_fn = _face_normal(raw3)
                def _mk_planar(flat_fn=flat_fn):
                    def planar(v):
                        u, t = _planar_uv(float(v[0]), float(v[1]), float(v[2]),
                                          *flat_fn, _PLANAR_TILE)
                        return [str(u), str(t)]
                    return planar
                _emit_face(fv, ft, group_vertices, tex_coords, has_uv, planar_fn=_mk_planar(),
                           fn=fn, obj_normals=obj_normals)
            else:
                _emit_face(fv, ft, group_vertices, tex_coords, has_uv,
                           fn=fn, obj_normals=obj_normals)
        count = len(vertices_list) - start
        if cfg.tex_path is not None:
            tid = get_texture(cfg.tex_path)
            parts.append((start, count, tid, True,  cfg.color, cfg.double_sided))
        else:
            parts.append((start, count, 0,   False, cfg.color, cfg.double_sided))
    return parts


def _room_face_zone(fv: list, vertices: list) -> int:
    """Classifica faces do quarto: normais apontando para o centro sao internas."""
    raw3 = [vertices[fv[i] - 1] for i in range(min(3, len(fv)))]
    nx, _ny, nz = _face_normal(raw3)
    cx = sum(float(vertices[vi - 1][0]) for vi in fv) / len(fv)
    cz = sum(float(vertices[vi - 1][2]) for vi in fv) / len(fv)
    to_center_x = ROOM_LOCAL_CENTER_X - cx
    to_center_z = ROOM_LOCAL_CENTER_Z - cz
    if abs(nx) + abs(nz) < 1e-6:
        return INDOOR
    return INDOOR if nx * to_center_x + nz * to_center_z > 0.0 else OUTDOOR


def load_obj_multi_zoned(obj_path: str,
                         mat_configs: dict[str, MatConfig],
                         zone_fn: Callable[[list, list], int]) -> list[tuple]:
    """
    Carrega OBJ com materiais separados e uma zona por face.
    Usado no quarto para separar faces internas e externas do mesmo material.
    """
    vertices, tex_coords, obj_normals, groups = _load_model_with_groups(obj_path)
    has_uv = len(tex_coords) > 0
    parts = []
    for obj_name, mat_name, faces in groups:
        cfg = mat_configs.get(f"{obj_name}:{mat_name}") or mat_configs.get(mat_name)
        if cfg is None:
            continue
        group_vertices = vertices
        if cfg.min_y is not None:
            group_vertices = [
                [v[0], str(max(float(v[1]), cfg.min_y)), v[2]]
                for v in vertices
            ]
        faces_by_zone: dict[int, list] = {INDOOR: [], OUTDOOR: []}
        for face in faces:
            fv, _ft, _fn = face
            faces_by_zone[zone_fn(fv, group_vertices)].append(face)

        use_planar = cfg.tex_path is not None and (not has_uv or cfg.force_planar)
        for zone, zone_faces in faces_by_zone.items():
            if not zone_faces:
                continue
            start = len(vertices_list)
            for fv, ft, fn in zone_faces:
                if use_planar:
                    raw3 = [group_vertices[fv[i] - 1] for i in range(min(3, len(fv)))]
                    flat_fn = _face_normal(raw3)
                    def _mk_planar(flat_fn=flat_fn):
                        def planar(v):
                            u, t = _planar_uv(float(v[0]), float(v[1]), float(v[2]),
                                              *flat_fn, _PLANAR_TILE)
                            return [str(u), str(t)]
                        return planar
                    _emit_face(fv, ft, group_vertices, tex_coords, has_uv,
                               planar_fn=_mk_planar(), fn=fn, obj_normals=obj_normals)
                else:
                    _emit_face(fv, ft, group_vertices, tex_coords, has_uv,
                               fn=fn, obj_normals=obj_normals)
            count = len(vertices_list) - start
            if cfg.tex_path is not None:
                tid = get_texture(cfg.tex_path)
                parts.append((start, count, tid, True, cfg.color, cfg.double_sided, zone))
            else:
                parts.append((start, count, 0, False, cfg.color, cfg.double_sided, zone))
    return parts


def load_obj(obj_path: str, tex_path: str) -> tuple[int, int, int]:
    model  = load_model_from_file(obj_path)
    start  = len(vertices_list)
    has_uv = len(model["texture"]) > 0
    obj_normals = model["normals"]
    for fv, ft, fn in model["faces"]:
        _emit_face(fv, ft, model["vertices"], model["texture"], has_uv,
                   fn=fn, obj_normals=obj_normals)
    tid = get_texture(tex_path)
    return start, len(vertices_list) - start, tid

# ---------------------------------------------------------------------------
# Geometria da cena
# ---------------------------------------------------------------------------

def _append_quad(corners: list, uvs: list) -> tuple[int, int]:
    start = len(vertices_list)
    # Winding (0,2,1),(0,3,2) gives +y for floor, -y for ceiling (correct for Phong).
    for tri_idx in ((0, 2, 1), (0, 3, 2)):
        raw = [corners[i] for i in tri_idx]
        nx, ny, nz = _face_normal(raw)
        for i in tri_idx:
            x, y, z = corners[i]
            vertices_list.append([str(x), str(y), str(z)])
            normals_list.append([str(nx), str(ny), str(nz)])
            texcoords_list.append([str(uvs[i][0]), str(uvs[i][1])])
    return start, 6


def build_floor(cx: float, cz: float, hw: float, hd: float,
                y: float, tile: float, tex_path: str) -> tuple[int, int, int]:
    corners = [
        (cx - hw, y, cz - hd), (cx + hw, y, cz - hd),
        (cx + hw, y, cz + hd), (cx - hw, y, cz + hd),
    ]
    t = tile
    uvs = [(0, 0), (t, 0), (t, t), (0, t)]
    s, n = _append_quad(corners, uvs)
    tid = get_texture(tex_path)
    return s, n, tid


def build_circle_floor(cx: float, cz: float, radius: float, y: float, 
                       tile_scale: float, tex_path: str, segments: int = 32) -> tuple[int, int, int]:
    """Cria piso circular."""
    start = len(vertices_list)
    
    # Pontos do círculo
    points = []
    uvs = []
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        z = cz + radius * math.sin(angle)
        points.append((x, y, z))
        
        # UV pela posição no plano
        u = (x - cx) / tile_scale + 0.5
        v = (z - cz) / tile_scale + 0.5
        uvs.append((u, v))
        
    center_uv = (0.5, 0.5)
    
    # Triângulos
    for i in range(segments):
        next_i = (i + 1) % segments

        # Winding swapped (next_i before i) so normal faces +y (upward).
        tri_pts = [(cx, y, cz), points[next_i], points[i]]
        nx, ny, nz = _face_normal(tri_pts)
        n_str = [str(nx), str(ny), str(nz)]

        vertices_list.extend([[str(cx), str(y), str(cz)],
                              [str(points[next_i][0]), str(points[next_i][1]), str(points[next_i][2])],
                              [str(points[i][0]), str(points[i][1]), str(points[i][2])]])
        normals_list.extend([n_str, n_str, n_str])
        texcoords_list.extend([[str(center_uv[0]), str(center_uv[1])],
                               [str(uvs[next_i][0]), str(uvs[next_i][1])],
                               [str(uvs[i][0]), str(uvs[i][1])]])
                               
    tid = get_texture(tex_path)
    return start, segments * 3, tid


def build_ring_slope(cx: float, cz: float, r_inner: float, r_outer: float, 
                     y_inner: float, y_outer: float, tile_scale: float, 
                     tex_path: str, segments: int = 32) -> tuple[int, int, int]:
    """Cria anel entre dois círculos."""
    start = len(vertices_list)
    
    for i in range(segments):
        angle1 = 2.0 * math.pi * i / segments
        angle2 = 2.0 * math.pi * (i + 1) / segments
        
        # Pontos internos
        px1i = cx + r_inner * math.cos(angle1)
        pz1i = cz + r_inner * math.sin(angle1)
        px2i = cx + r_inner * math.cos(angle2)
        pz2i = cz + r_inner * math.sin(angle2)
        
        # Pontos externos
        px1o = cx + r_outer * math.cos(angle1)
        pz1o = cz + r_outer * math.sin(angle1)
        px2o = cx + r_outer * math.cos(angle2)
        pz2o = cz + r_outer * math.sin(angle2)
        
        # UV ao redor do anel
        circ = 2.0 * math.pi * max(r_inner, r_outer)
        u_scale = circ / tile_scale
        u1 = (i / segments) * u_scale
        u2 = ((i + 1) / segments) * u_scale
        
        dist = math.sqrt((r_outer - r_inner)**2 + (y_outer - y_inner)**2)
        v_inner = 0.0
        v_outer = dist / tile_scale
        
        u1i, v1i = u1, v_inner
        u2i, v2i = u2, v_inner
        u1o, v1o = u1, v_outer
        u2o, v2o = u2, v_outer
        
        # Winding: outer-first gives normals facing outward+upward.
        t1 = [(px1o, y_outer, pz1o), (px1i, y_inner, pz1i), (px2i, y_inner, pz2i)]
        t2 = [(px1o, y_outer, pz1o), (px2i, y_inner, pz2i), (px2o, y_outer, pz2o)]
        n1x, n1y, n1z = _face_normal(t1)
        n2x, n2y, n2z = _face_normal(t2)
        ns1 = [str(n1x), str(n1y), str(n1z)]
        ns2 = [str(n2x), str(n2y), str(n2z)]

        vertices_list.extend([[str(px1o), str(y_outer), str(pz1o)],
                              [str(px1i), str(y_inner), str(pz1i)],
                              [str(px2i), str(y_inner), str(pz2i)]])
        normals_list.extend([ns1, ns1, ns1])
        texcoords_list.extend([[str(u1o), str(v1o)], [str(u1i), str(v1i)], [str(u2i), str(v2i)]])

        vertices_list.extend([[str(px1o), str(y_outer), str(pz1o)],
                              [str(px2i), str(y_inner), str(pz2i)],
                              [str(px2o), str(y_outer), str(pz2o)]])
        normals_list.extend([ns2, ns2, ns2])
        texcoords_list.extend([[str(u1o), str(v1o)], [str(u2i), str(v2i)], [str(u2o), str(v2o)]])

    tid = get_texture(tex_path)
    return start, segments * 6, tid


def build_rounded_slope(cx: float, cz: float, r_inner: float, r_outer: float, 
                        y_inner: float, y_outer: float, tile_scale: float, 
                        tex_path: str, radial_segments: int = 64, 
                        curve_steps: int = 10) -> tuple[int, int, int]:
    """Cria borda arredondada."""
    start = len(vertices_list)
    
    # Anéis concêntricos criam a curva.
    for step in range(curve_steps):
        t1 = step / curve_steps
        t2 = (step + 1) / curve_steps
        
        # Raio e altura no início do passo.
        r1 = r_inner + (r_outer - r_inner) * math.sin(t1 * math.pi / 2)
        y1 = y_outer + (y_inner - y_outer) * math.cos(t1 * math.pi / 2)
        
        # Raio e altura no fim do passo.
        r2 = r_inner + (r_outer - r_inner) * math.sin(t2 * math.pi / 2)
        y2 = y_outer + (y_inner - y_outer) * math.cos(t2 * math.pi / 2)
        
        # V acompanha a descida da curva.
        v_start = (t1 * math.pi / 2) * (r_outer - r_inner) / tile_scale
        v_end   = (t2 * math.pi / 2) * (r_outer - r_inner) / tile_scale
        
        for i in range(radial_segments):
            angle1 = 2.0 * math.pi * i / radial_segments
            angle2 = 2.0 * math.pi * (i + 1) / radial_segments
            
            # Pontos internos
            px1i = cx + r1 * math.cos(angle1)
            pz1i = cz + r1 * math.sin(angle1)
            px2i = cx + r1 * math.cos(angle2)
            pz2i = cz + r1 * math.sin(angle2)
            
            # Pontos externos
            px1o = cx + r2 * math.cos(angle1)
            pz1o = cz + r2 * math.sin(angle1)
            px2o = cx + r2 * math.cos(angle2)
            pz2o = cz + r2 * math.sin(angle2)
            
            # UV
            circ = 2.0 * math.pi * r_inner # base horizontal pelo raio interno
            u_scale = circ / tile_scale
            u1 = (i / radial_segments) * u_scale
            u2 = ((i + 1) / radial_segments) * u_scale
            
            u1i, v1i = u1, v_start
            u2i, v2i = u2, v_start
            u1o, v1o = u1, v_end
            u2o, v2o = u2, v_end
            
            # Winding: outer-first gives normals facing outward.
            ta = [(px1o, y2, pz1o), (px1i, y1, pz1i), (px2i, y1, pz2i)]
            tb = [(px1o, y2, pz1o), (px2i, y1, pz2i), (px2o, y2, pz2o)]
            nax, nay, naz = _face_normal(ta)
            nbx, nby, nbz = _face_normal(tb)
            nsa = [str(nax), str(nay), str(naz)]
            nsb = [str(nbx), str(nby), str(nbz)]

            vertices_list.extend([[str(px1o), str(y2), str(pz1o)],
                                  [str(px1i), str(y1), str(pz1i)],
                                  [str(px2i), str(y1), str(pz2i)]])
            normals_list.extend([nsa, nsa, nsa])
            texcoords_list.extend([[str(u1o), str(v1o)], [str(u1i), str(v1i)], [str(u2i), str(v2i)]])

            vertices_list.extend([[str(px1o), str(y2), str(pz1o)],
                                  [str(px2i), str(y1), str(pz2i)],
                                  [str(px2o), str(y2), str(pz2o)]])
            normals_list.extend([nsb, nsb, nsb])
            texcoords_list.extend([[str(u1o), str(v1o)], [str(u2i), str(v2i)], [str(u2o), str(v2o)]])
            
    tid = get_texture(tex_path)
    # Cada passo adiciona seis vértices por segmento radial.
    return start, radial_segments * curve_steps * 6, tid



def build_skysphere_geometry(radius: float, lat_bands: int = 40, long_bands: int = 40) -> tuple[int, int]:
    start = len(vertices_list)
    
    sphere_verts = []
    sphere_uvs = []
    for lat in range(lat_bands + 1):
        theta = lat * math.pi / lat_bands
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        for lon in range(long_bands + 1):
            phi = lon * 2 * math.pi / long_bands
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)
            
            x = radius * cos_phi * sin_theta
            y = radius * cos_theta
            z = radius * sin_phi * sin_theta
            
            u = 1.0 - (lon / long_bands)
            v = 1.0 - (lat / lat_bands)
            
            sphere_verts.append([str(x), str(y), str(z)])
            sphere_uvs.append([str(u), str(v)])
            
    tri_count = 0
    for lat in range(lat_bands):
        for lon in range(long_bands):
            first = (lat * (long_bands + 1)) + lon
            second = first + long_bands + 1
            
            _zero_n = ["0.0", "1.0", "0.0"]
            # Triângulo 1
            vertices_list.extend([sphere_verts[first], sphere_verts[second], sphere_verts[first + 1]])
            normals_list.extend([_zero_n, _zero_n, _zero_n])
            texcoords_list.extend([sphere_uvs[first], sphere_uvs[second], sphere_uvs[first + 1]])
            tri_count += 3

            # Triângulo 2
            vertices_list.extend([sphere_verts[second], sphere_verts[second + 1], sphere_verts[first + 1]])
            normals_list.extend([_zero_n, _zero_n, _zero_n])
            texcoords_list.extend([sphere_uvs[second], sphere_uvs[second + 1], sphere_uvs[first + 1]])
            tri_count += 3
            
    return start, tri_count

def build_unit_cube() -> tuple[int, int]:
    """Cubo unitário centrado na origem — usado como marcador de fonte de luz."""
    h = 0.5
    faces = [
        [(-h,-h,-h),( h,-h,-h),( h,-h, h),(-h,-h, h)],  # bottom
        [(-h, h,-h),(-h, h, h),( h, h, h),( h, h,-h)],  # top
        [(-h,-h, h),( h,-h, h),( h, h, h),(-h, h, h)],  # front
        [( h,-h,-h),(-h,-h,-h),(-h, h,-h),( h, h,-h)],  # back
        [(-h,-h,-h),(-h,-h, h),(-h, h, h),(-h, h,-h)],  # left
        [( h,-h, h),( h,-h,-h),( h, h,-h),( h, h, h)],  # right
    ]
    start = len(vertices_list)
    for face in faces:
        for tri_idx in ((0, 1, 2), (0, 2, 3)):
            raw = [face[i] for i in tri_idx]
            nx, ny, nz = _face_normal(raw)
            n_str = [str(nx), str(ny), str(nz)]
            for i in tri_idx:
                x, y, z = face[i]
                vertices_list.append([str(x), str(y), str(z)])
                normals_list.append(n_str)
                texcoords_list.append(["0.0", "0.0"])
    return start, len(vertices_list) - start


# ---------------------------------------------------------------------------
# Envio para GPU
# ---------------------------------------------------------------------------

def upload_to_gpu(program: int) -> None:
    verts = np.zeros(len(vertices_list),  [("position", np.float32, 3)])
    texcs = np.zeros(len(texcoords_list), [("position", np.float32, 2)])
    norms = np.zeros(len(normals_list),   [("position", np.float32, 3)])
    verts["position"] = [(float(v[0]), float(v[1]), float(v[2])) for v in vertices_list]
    texcs["position"] = [(float(t[0]), float(t[1])) for t in texcoords_list]
    norms["position"] = [(float(n[0]), float(n[1]), float(n[2])) for n in normals_list]

    buf = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, buf[0])
    glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 3, GL_FLOAT, False, verts.strides[0], ctypes.c_void_p(0))

    glBindBuffer(GL_ARRAY_BUFFER, buf[1])
    glBufferData(GL_ARRAY_BUFFER, texcs.nbytes, texcs, GL_STATIC_DRAW)
    loc2 = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc2)
    glVertexAttribPointer(loc2, 2, GL_FLOAT, False, texcs.strides[0], ctypes.c_void_p(0))

    glBindBuffer(GL_ARRAY_BUFFER, buf[2])
    glBufferData(GL_ARRAY_BUFFER, norms.nbytes, norms, GL_STATIC_DRAW)
    loc3 = glGetAttribLocation(program, "normals")
    glEnableVertexAttribArray(loc3)
    glVertexAttribPointer(loc3, 3, GL_FLOAT, False, norms.strides[0], ctypes.c_void_p(0))

# ---------------------------------------------------------------------------
# Matrizes
# ---------------------------------------------------------------------------

def mat_model(tx=0.0, ty=0.0, tz=0.0,
              angle_y=0.0, angle_x=0.0,
              sx=1.0, sy=1.0, sz=1.0) -> np.ndarray:
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(tx, ty, tz))
    if angle_y:
        m = glm.rotate(m, glm.radians(angle_y), glm.vec3(0, 1, 0))
    if angle_x:
        m = glm.rotate(m, glm.radians(angle_x), glm.vec3(1, 0, 0))
    m = glm.scale(m, glm.vec3(sx, sy, sz))
    return np.array(m)


def mat_room_door_open() -> np.ndarray:
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(ROOM_TX, ROOM_TY, ROOM_TZ))
    m = glm.scale(m, glm.vec3(ROOM_SCALE, 1.0, ROOM_SCALE))
    m = glm.translate(m, glm.vec3(ROOM_DOOR_HINGE_X, 0.0, ROOM_DOOR_HINGE_Z))
    m = glm.rotate(m, glm.radians(ROOM_DOOR_OPEN_DEG), glm.vec3(0, 1, 0))
    m = glm.translate(m, glm.vec3(-ROOM_DOOR_HINGE_X, 0.0, -ROOM_DOOR_HINGE_Z))
    return np.array(m)


def mat_view() -> np.ndarray:
    return np.array(glm.lookAt(camera_pos, camera_pos + camera_front, camera_up))


def mat_proj() -> np.ndarray:
    return np.array(glm.perspective(glm.radians(fov), WIN_W / WIN_H, 0.1, 200.0))

# ---------------------------------------------------------------------------
# Desenho
# ---------------------------------------------------------------------------

def draw(program: int, tex_id: int, start: int, count: int,
         model: np.ndarray,
         use_tex: bool = True,
         color: tuple = (0.85, 0.85, 0.85, 1.0),
         highlight: bool = False,
         uv_scale: float = 1.0,
         zone: int = OUTDOOR,
         ka: float = 0.25, kd: float = 0.75, ks: float = 0.20, shininess: float = 16.0,
         emissive: bool = False,
         emissive_mult: float = 1.0) -> None:
    glUniformMatrix4fv(glGetUniformLocation(program, "model"), 1, GL_TRUE, model)
    glUniform1f(glGetUniformLocation(program, "uv_scale"), uv_scale)
    glUniform1i(glGetUniformLocation(program, "objectZone"), zone)
    glUniform1f(glGetUniformLocation(program, "ka"), ka)
    glUniform1f(glGetUniformLocation(program, "kd"), kd)
    glUniform1f(glGetUniformLocation(program, "ks"), ks)
    glUniform1f(glGetUniformLocation(program, "ns"), shininess)
    glUniform1i(glGetUniformLocation(program, "emissive"), 1 if emissive else 0)
    glUniform1f(glGetUniformLocation(program, "emissiveMult"), emissive_mult)
    if highlight:
        glUniform1i(glGetUniformLocation(program, "use_texture"), 0)
        glUniform4f(glGetUniformLocation(program, "flat_color"), 1.0, 0.8, 0.2, 1.0)
    elif use_tex:
        glUniform1i(glGetUniformLocation(program, "use_texture"), 1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
    else:
        glUniform1i(glGetUniformLocation(program, "use_texture"), 0)
        glUniform4f(glGetUniformLocation(program, "flat_color"), *color)
    glDrawArrays(GL_TRIANGLES, start, count)

# ---------------------------------------------------------------------------
# Eventos
# ---------------------------------------------------------------------------


def key_event(window, key, scancode, action, mods) -> None:
    global wireframe
    global camera_pos, yaw, pitch
    global ambient_enabled, light_enabled, ambient_strength, diffuse_mult, specular_mult
    global sandbox_mode, sandbox_light, sky_brightness, sandbox_marker_scale

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
        return

    repeat = action in (glfw.PRESS, glfw.REPEAT)
    shift  = bool(mods & glfw.MOD_SHIFT)
    spd    = CAM_SPEED * delta_time * (3.0 if shift else 1.0)

    if key == glfw.KEY_P and action == glfw.PRESS:
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)

    # F1: toggle sandbox mode
    if key == glfw.KEY_F1 and action == glfw.PRESS:
        sandbox_mode = not sandbox_mode
        print(f"[SANDBOX] {'ON' if sandbox_mode else 'OFF'}  "
              f"Tab=cycle  Arrows=X/Z  PgUp/Dn=Y  +/-=intensity  F5=save",
              flush=True)
        if sandbox_mode:
            _sandbox_print()

    # F5: save lighting config
    if key == glfw.KEY_F5 and action == glfw.PRESS:
        save_lighting_config()

    # Sandbox light editing (active while sandbox_mode is on)
    if sandbox_mode:
        if key == glfw.KEY_TAB and action == glfw.PRESS:
            sandbox_light = (sandbox_light + 1) % 3
            _sandbox_print()

        if repeat:
            mvs = 0.2 * (3.0 if shift else 1.0)
            its = 0.05 * (3.0 if shift else 1.0)
            pos = [outdoor_offset, abajur_pos, ceiling_pos][sandbox_light]
            changed = False
            if key == glfw.KEY_LEFT:      pos[0] -= mvs; changed = True
            if key == glfw.KEY_RIGHT:     pos[0] += mvs; changed = True
            if key == glfw.KEY_UP:        pos[2] -= mvs; changed = True
            if key == glfw.KEY_DOWN:      pos[2] += mvs; changed = True
            if key == glfw.KEY_PAGE_UP:   pos[1] += mvs; changed = True
            if key == glfw.KEY_PAGE_DOWN: pos[1] -= mvs; changed = True
            if key == glfw.KEY_EQUAL:     # + key (no shift needed)
                light_intensities_cfg[sandbox_light] = max(0.0, light_intensities_cfg[sandbox_light] + its)
                changed = True
            if key == glfw.KEY_MINUS:
                light_intensities_cfg[sandbox_light] = max(0.0, light_intensities_cfg[sandbox_light] - its)
                changed = True
            # Sky brightness: [ and ] keys
            if key == glfw.KEY_LEFT_BRACKET:
                sky_brightness = max(0.1, sky_brightness - 0.1)
                print(f"[SANDBOX] sky_brightness={sky_brightness:.2f}", flush=True)
            if key == glfw.KEY_RIGHT_BRACKET:
                sky_brightness = min(5.0, sky_brightness + 0.1)
                print(f"[SANDBOX] sky_brightness={sky_brightness:.2f}", flush=True)
            # Marker cube size: V (shrink) / B (grow)
            if key == glfw.KEY_V:
                sandbox_marker_scale = max(0.02, sandbox_marker_scale - 0.02)
                print(f"[SANDBOX] marker_scale={sandbox_marker_scale:.3f}", flush=True)
            if key == glfw.KEY_B:
                sandbox_marker_scale = min(2.0, sandbox_marker_scale + 0.02)
                print(f"[SANDBOX] marker_scale={sandbox_marker_scale:.3f}", flush=True)
            if changed:
                _sandbox_print()
        # In sandbox mode, arrows are consumed by light editing — skip scene controls below
        if key in (glfw.KEY_LEFT, glfw.KEY_RIGHT, glfw.KEY_UP, glfw.KEY_DOWN):
            return

    # Light toggles (PRESS only)
    if action == glfw.PRESS:
        if key == glfw.KEY_1: ambient_enabled        = 1 - ambient_enabled
        if key == glfw.KEY_2: light_enabled[0]       = 1 - light_enabled[0]
        if key == glfw.KEY_3: light_enabled[1]       = 1 - light_enabled[1]
        if key == glfw.KEY_4: light_enabled[2]       = 1 - light_enabled[2]

    # Intensity sliders (PRESS + REPEAT for hold)
    if repeat:
        step = 0.05 * (3.0 if shift else 1.0)
        if key == glfw.KEY_J: ambient_strength = max(0.0, min(1.0, ambient_strength - step))
        if key == glfw.KEY_K: ambient_strength = max(0.0, min(1.0, ambient_strength + step))
        step2 = 0.1 * (3.0 if shift else 1.0)
        if key == glfw.KEY_N: diffuse_mult  = max(0.0, min(2.0, diffuse_mult  - step2))
        if key == glfw.KEY_M: diffuse_mult  = max(0.0, min(2.0, diffuse_mult  + step2))
        if key == glfw.KEY_U: specular_mult = max(0.0, min(2.0, specular_mult - step2))
        if key == glfw.KEY_I: specular_mult = max(0.0, min(2.0, specular_mult + step2))

    if repeat:
        new_pos = glm.vec3(camera_pos)
        if key == glfw.KEY_W: new_pos += spd * camera_front
        if key == glfw.KEY_S: new_pos -= spd * camera_front
        if key == glfw.KEY_A: new_pos -= glm.normalize(glm.cross(camera_front, camera_up)) * spd
        if key == glfw.KEY_D: new_pos += glm.normalize(glm.cross(camera_front, camera_up)) * spd
        camera_pos.x = max(-SKYBOX_HALF+1, min(SKYBOX_HALF-1, new_pos.x))
        camera_pos.y = max(0.3, min(8.0, new_pos.y))
        camera_pos.z = max(-SKYBOX_HALF+1, min(SKYBOX_HALF-1, new_pos.z))

        umbrella = objects[UMBRELLA_INDEX]
        indoor_chair = objects[INDOOR_CHAIR_INDEX]
        beach_chair = objects[BEACH_CHAIR_INDEX]

        scale_rate = 1.04 if not shift else 1.10
        if key == glfw.KEY_Z:
            umbrella.scale = min(1.2, umbrella.scale * scale_rate)
        if key == glfw.KEY_X:
            umbrella.scale = max(0.12, umbrella.scale / scale_rate)

        rot_step = 4.0 if not shift else 12.0
        if key == glfw.KEY_Q:
            indoor_chair.angle_y += rot_step
        if key == glfw.KEY_E:
            indoor_chair.angle_y -= rot_step

        chair_step = 0.04 if not shift else 0.14
        if key == glfw.KEY_UP:
            beach_chair.tz -= chair_step
        if key == glfw.KEY_DOWN:
            beach_chair.tz += chair_step
        if key == glfw.KEY_LEFT:
            beach_chair.tx -= chair_step
        if key == glfw.KEY_RIGHT:
            beach_chair.tx += chair_step
        beach_chair.tx = max(BEACH_CHAIR_MIN_X, min(BEACH_CHAIR_MAX_X, beach_chair.tx))
        beach_chair.tz = max(BEACH_CHAIR_MIN_Z, min(BEACH_CHAIR_MAX_Z, beach_chair.tz))


def mouse_callback(window, xpos: float, ypos: float) -> None:
    global first_mouse, last_x, last_y, yaw, pitch, camera_front
    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False
    dx = (xpos - last_x) * MOUSE_SENS
    dy = (last_y - ypos) * MOUSE_SENS
    last_x, last_y = xpos, ypos
    yaw   += dx
    pitch  = max(-89.0, min(89.0, pitch + dy))
    front  = glm.vec3(
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch)),
    )
    camera_front = glm.normalize(front)


def scroll_callback(window, xoff: float, yoff: float) -> None:
    global fov
    fov = max(1.0, min(90.0, fov - yoff))

# ---------------------------------------------------------------------------
# Lighting config persistence
# ---------------------------------------------------------------------------

_CONFIG_PATH = os.path.join(BASE, "lighting_config.json")

def load_lighting_config() -> None:
    global ambient_strength, ambient_color, diffuse_mult, specular_mult
    global outdoor_offset, abajur_pos, ceiling_pos, light_intensities_cfg
    global sky_brightness, sandbox_marker_scale
    if not os.path.exists(_CONFIG_PATH):
        return
    with open(_CONFIG_PATH) as f:
        cfg = json.load(f)
    ambient_strength      = cfg.get("ambient_strength",    ambient_strength)
    ambient_color         = cfg.get("ambient_color",       ambient_color)
    diffuse_mult          = cfg.get("diffuse_mult",        diffuse_mult)
    specular_mult         = cfg.get("specular_mult",       specular_mult)
    outdoor_offset        = cfg.get("outdoor_offset",      outdoor_offset)
    abajur_pos            = cfg.get("abajur_pos",          abajur_pos)
    ceiling_pos           = cfg.get("ceiling_pos",         ceiling_pos)
    light_intensities_cfg = cfg.get("light_intensities",   light_intensities_cfg)
    sky_brightness        = cfg.get("sky_brightness",      sky_brightness)
    sandbox_marker_scale  = cfg.get("sandbox_marker_scale",sandbox_marker_scale)
    print(f"Loaded {_CONFIG_PATH}", flush=True)


def save_lighting_config() -> None:
    cfg = {
        "ambient_strength":  ambient_strength,
        "ambient_color":     ambient_color,
        "diffuse_mult":      diffuse_mult,
        "specular_mult":     specular_mult,
        "outdoor_offset":    outdoor_offset,
        "abajur_pos":        abajur_pos,
        "ceiling_pos":       ceiling_pos,
        "light_intensities":    light_intensities_cfg,
        "sky_brightness":       sky_brightness,
        "sandbox_marker_scale": sandbox_marker_scale,
    }
    with open(_CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Saved {_CONFIG_PATH}", flush=True)


def _sandbox_print() -> None:
    names = ["outdoor(offset)", "abajur", "ceiling"]
    positions = [outdoor_offset, abajur_pos, ceiling_pos]
    p = [round(v, 3) for v in positions[sandbox_light]]
    i = round(light_intensities_cfg[sandbox_light], 3)
    print(f"[SANDBOX] light={sandbox_light} {names[sandbox_light]}  pos={p}  intensity={i}",
          flush=True)


# ---------------------------------------------------------------------------
# Shaders
# ---------------------------------------------------------------------------

def compile_program(vs_path: str, fs_path: str) -> int:
    with open(vs_path) as f: vs_src = f.read()
    with open(fs_path) as f: fs_src = f.read()
    vs = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vs, vs_src)
    glCompileShader(vs)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(vs).decode())
    fs = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fs, fs_src)
    glCompileShader(fs)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(fs).decode())
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog).decode())
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog

# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------

def main() -> None:
    global delta_time, last_frame

    load_lighting_config()

    if not glfw.init():
        raise RuntimeError("Erro ao iniciar GLFW")
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(WIN_W, WIN_H, "Projeto 3 - SCC0250", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Erro ao criar janela")
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    prog = compile_program(
        os.path.join(BASE, "vertex_shader.vs"),
        os.path.join(BASE, "fragment_shader.fs"),
    )
    glUseProgram(prog)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    print("Preparando céu", flush=True)
    sky_tid = get_texture(SKY_PANO)

    print("Carregando modelos", flush=True)
    for obj in objects:
        print(f"  {obj.name}", flush=True)
        if obj.mat_configs:
            obj.parts = load_obj_multi(obj.obj_path, obj.mat_configs)
        else:
            obj.start, obj.count, obj.tex_id = load_obj(obj.obj_path, obj.tex_path)

    print("  Quarto", flush=True)
    _ROOM_MATS: dict[str, MatConfig] = {
        "Wall_material":           MatConfig(tex_path=ROOM_WALL_TEX, force_planar=True, double_sided=True),
        "Baseboard_material":      MatConfig(tex_path=ROOM_WALL_TEX, force_planar=True, double_sided=True),
        "DoorFrame:Door_material": MatConfig(tex_path=ROOM_DOOR_TEX, force_planar=True, double_sided=True),
        "Floor_material":          MatConfig(color=(0.711, 0.668, 0.668, 1.0)),
        "Glass_material":          MatConfig(tex_path=ROOM_GLASS_TEX, force_planar=True, double_sided=True),
        "Plastic_Handle_material": MatConfig(tex_path=ROOM_HANDLE_PLASTIC_TEX, force_planar=True, double_sided=True),
        "Sill_material":           MatConfig(tex_path=ROOM_WALL_TEX, force_planar=True, double_sided=True),
        "Window_material":         MatConfig(color=(0.780, 0.820, 0.900, 1.0), double_sided=True),
    }
    room_parts = load_obj_multi_zoned(ROOM_OBJ, _ROOM_MATS, _room_face_zone)
    _DOOR_MATS: dict[str, MatConfig] = {
        "Door:Door_material": MatConfig(tex_path=ROOM_DOOR_TEX, force_planar=True,
                                        double_sided=True, min_y=ROOM_BASE_STRIP_H),
        "Handle_Front:Handle_material": MatConfig(tex_path=ROOM_HANDLE_TEX, force_planar=True,
                                                  double_sided=True),
        "Handle_Back:Handle_material": MatConfig(tex_path=ROOM_HANDLE_TEX, force_planar=True,
                                                 double_sided=True),
    }
    door_parts = load_obj_multi_zoned(ROOM_OBJ, _DOOR_MATS, _room_face_zone)
    _handle_color = (0.02, 0.02, 0.02, 1.0)
    _inner_handle_z = -0.130
    for hx0, hx1 in ((0.861, 0.877), (1.913, 1.929)):
        hs, hn = _append_quad(
            [
                (hx0, 1.470, _inner_handle_z),
                (hx1, 1.470, _inner_handle_z),
                (hx1, 1.595, _inner_handle_z),
                (hx0, 1.595, _inner_handle_z),
            ],
            [(0, 0), (1, 0), (1, 1), (0, 1)],
        )
        room_parts.append((hs, hn, 0, False, _handle_color, True, INDOOR))

    print("  Telhas do teto", flush=True)
    _TILE_MATS: dict[str, MatConfig] = {
        "Plane_Plane.004:Material.002": MatConfig(color=(0.32, 0.33, 0.34, 1.0),
                                                  double_sided=True),
    }
    roof_tile_parts = load_obj_multi(TILE_OBJ, _TILE_MATS)

    water_s, water_n, water_tid = build_circle_floor(0, 0, SKYBOX_HALF, 0.0, 3.2, WATER_TEX, 96)
    sand_s, sand_n, sand_tid    = build_rounded_slope(0, 0, 10.0, 14.0, 0.5, 0.0, 10.0, SAND_TEX, 64, 15)
    grass_s, grass_n, grass_tid = build_circle_floor(0, 0, 10.0, 0.5, 10.0, SAND_TEX, 64)
    wood_s, wood_n, wood_tid    = build_floor(0.0, 0.0, 2.925, 2.925, ROOM_FLOOR_Y, 2.0, WOOD_TEX)

    _cx, _cz, _hw, _hd = 0.0, 0.0, 3.0, 3.0
    _tile_uv = 2.0
    ceiling_corners = [
        (_cx - _hw, ROOM_CEIL_Y, _cz - _hd),
        (_cx - _hw, ROOM_CEIL_Y, _cz + _hd),
        (_cx + _hw, ROOM_CEIL_Y, _cz + _hd),
        (_cx + _hw, ROOM_CEIL_Y, _cz - _hd),
    ]
    ceil_s, ceil_n = _append_quad(ceiling_corners,
                                   [(0,0),(0,_tile_uv),(_tile_uv,_tile_uv),(_tile_uv,0)])
    ceil_tid = get_texture(CEILING_TEX)

    sky_start, sky_count = build_skysphere_geometry(SKYBOX_HALF)

    # Unit cube for sandbox light markers (built once, repositioned per frame via model matrix)
    cube_s, cube_n = build_unit_cube()

    print("Enviando dados para GPU", flush=True)
    upload_to_gpu(prog)

    # Marker colors match each light's color (rgba)
    _marker_colors = [
        (1.00, 0.80, 0.35, 1.0),   # outdoor — warm yellow-orange
        (1.00, 0.85, 0.45, 1.0),   # abajur  — warm orange-yellow
        (0.80, 0.90, 1.00, 1.0),   # ceiling — cool white-blue
    ]

    # Pre-cache uniform locations
    loc_view           = glGetUniformLocation(prog, "view")
    loc_proj           = glGetUniformLocation(prog, "projection")
    loc_light_pos      = glGetUniformLocation(prog, "lightPos")
    loc_light_color    = glGetUniformLocation(prog, "lightColor")
    loc_light_intensity= glGetUniformLocation(prog, "lightIntensity")
    loc_light_enabled  = glGetUniformLocation(prog, "lightEnabled")
    loc_light_zone     = glGetUniformLocation(prog, "lightZone")
    loc_ambient_en     = glGetUniformLocation(prog, "ambientEnabled")
    loc_ambient_str    = glGetUniformLocation(prog, "ambientStrength")
    loc_diffuse_mult   = glGetUniformLocation(prog, "diffuseMult")
    loc_specular_mult  = glGetUniformLocation(prog, "specularMult")
    loc_view_pos       = glGetUniformLocation(prog, "viewPos")
    loc_ambient_color  = glGetUniformLocation(prog, "ambientColor")

    # Static light color + zone (never changes)
    _light_colors = np.array([
        [1.00, 0.45, 0.05],   # outdoor  — deep orange-red (sunset)
        [1.00, 0.85, 0.45],   # abajur   — warm orange-yellow
        [0.80, 0.90, 1.00],   # ceiling  — cool white-blue
    ], dtype=np.float32)
    _light_zones = np.array([OUTDOOR, INDOOR, INDOOR], dtype=np.int32)

    glfw.show_window(window)
    print("Cena pronta", flush=True)
    print("Iluminação: 1=ambient 2=luz-ext 3=abajur 4=teto | J/K=ambient N/M=difuso U/I=especular", flush=True)
    print("Sandbox:    F1=toggle  Tab=luz  Setas=X/Z  PgUp/Dn=Y  +/-=intensidade  [/]=céu  F5=salvar", flush=True)

    while not glfw.window_should_close(window):
        now        = glfw.get_time()
        delta_time = now - last_frame
        last_frame = now

        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.52, 0.80, 0.98, 1.0)

        view = mat_view()
        proj = mat_proj()
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_proj, 1, GL_TRUE, proj)

        # Outdoor sun — position is beach-chair world pos + outdoor_offset
        bc = objects[BEACH_CHAIR_INDEX]
        outdoor_lpos = np.array([bc.tx + outdoor_offset[0],
                                  bc.ty + outdoor_offset[1],
                                  bc.tz + outdoor_offset[2]], dtype=np.float32)

        light_positions = np.array([
            outdoor_lpos,
            abajur_pos,
            ceiling_pos,
        ], dtype=np.float32)

        # Send per-frame lighting uniforms
        glUniform3fv(loc_light_pos,       3, light_positions.flatten())
        glUniform3fv(loc_light_color,     3, _light_colors.flatten())
        glUniform1fv(loc_light_intensity, 3, np.array(light_intensities_cfg, dtype=np.float32))
        glUniform1iv(loc_light_enabled,   3, np.array(light_enabled, dtype=np.int32))
        glUniform1iv(loc_light_zone,      3, _light_zones)
        glUniform1i(loc_ambient_en,    ambient_enabled)
        glUniform1f(loc_ambient_str,   ambient_strength)
        glUniform1f(loc_diffuse_mult,  diffuse_mult)
        glUniform1f(loc_specular_mult, specular_mult)
        glUniform3f(loc_view_pos, camera_pos.x, camera_pos.y, camera_pos.z)
        glUniform3f(loc_ambient_color, *ambient_color)

        # Sky sphere — panorama texture, brightness-boosted via emissiveMult
        glDepthMask(GL_FALSE)
        sky_m = mat_model(tx=camera_pos.x, ty=camera_pos.y, tz=camera_pos.z)
        draw(prog, sky_tid, sky_start, sky_count, sky_m,
             emissive=True, emissive_mult=sky_brightness)
        glDepthMask(GL_TRUE)

        # Outdoor terrain
        draw(prog, water_tid, water_s, water_n, mat_model(),
             zone=OUTDOOR, ka=0.30, kd=0.40, ks=0.60, shininess=32.0)
        draw(prog, sand_tid, sand_s, sand_n, mat_model(),
             zone=OUTDOOR, ka=0.30, kd=0.80, ks=0.05, shininess=6.0)
        draw(prog, grass_tid, grass_s, grass_n, mat_model(),
             zone=OUTDOOR, ka=0.30, kd=0.80, ks=0.05, shininess=6.0)

        # Indoor room walls / door
        if room_parts:
            room_m = mat_model(tx=ROOM_TX, ty=ROOM_TY, tz=ROOM_TZ,
                               sx=ROOM_SCALE, sy=1.0, sz=ROOM_SCALE)
            for pstart, pcount, ptex_id, puse_tex, pcolor, _pdouble, pzone in room_parts:
                draw(prog, ptex_id, pstart, pcount, room_m,
                     use_tex=puse_tex, color=pcolor,
                     zone=pzone, ka=0.30, kd=0.80, ks=0.10, shininess=12.0)
        if door_parts:
            door_m = mat_room_door_open()
            for pstart, pcount, ptex_id, puse_tex, pcolor, _pdouble, pzone in door_parts:
                draw(prog, ptex_id, pstart, pcount, door_m,
                     use_tex=puse_tex, color=pcolor,
                     zone=pzone, ka=0.30, kd=0.80, ks=0.10, shininess=12.0)

        # Indoor floor + ceiling
        draw(prog, wood_tid, wood_s, wood_n, mat_model(),
             zone=INDOOR, ka=0.25, kd=0.75, ks=0.25, shininess=24.0)
        draw(prog, ceil_tid, ceil_s, ceil_n, mat_model(),
             zone=INDOOR, ka=0.30, kd=0.80, ks=0.10, shininess=12.0)

        # Roof tiles (outdoor)
        for col in range(ROOF_TILE_COLS):
            tx = (col - (ROOF_TILE_COLS - 1) / 2.0) * ROOF_TILE_SPACING_X
            for row in range(ROOF_TILE_ROWS):
                tz = (row - (ROOF_TILE_ROWS - 1) / 2.0) * ROOF_TILE_SPACING_Z
                tile_m = mat_model(tx=tx, ty=ROOF_TILE_Y, tz=tz)
                for pstart, pcount, ptex_id, puse_tex, pcolor, _pdouble in roof_tile_parts:
                    draw(prog, ptex_id, pstart, pcount, tile_m,
                         use_tex=puse_tex, color=pcolor,
                         zone=OUTDOOR, ka=0.25, kd=0.50, ks=0.15, shininess=12.0)

        # Scene objects (each carries its own zone + material)
        for obj in objects:
            s = obj.scale
            m = mat_model(tx=obj.tx, ty=obj.ty, tz=obj.tz,
                          angle_y=obj.angle_y, angle_x=obj.angle_x,
                          sx=s, sy=s, sz=s)
            mat_kw = dict(zone=obj.zone, ka=obj.ka, kd=obj.kd,
                          ks=obj.ks, shininess=obj.shininess)
            if obj.parts:
                for pstart, pcount, ptex_id, puse_tex, pcolor, _ds in obj.parts:
                    draw(prog, ptex_id, pstart, pcount, m,
                         use_tex=puse_tex, color=pcolor, **mat_kw)
            else:
                draw(prog, obj.tex_id, obj.start, obj.count, m,
                     use_tex=True, **mat_kw)

        # Sandbox light markers — emissive cubes shown only in sandbox mode
        if sandbox_mode:
            marker_positions = [
                outdoor_lpos,
                np.array(abajur_pos,   dtype=np.float32),
                np.array(ceiling_pos,  dtype=np.float32),
            ]
            for idx, (lpos, lcolor) in enumerate(zip(marker_positions, _marker_colors)):
                s = sandbox_marker_scale * (1.5 if idx == sandbox_light else 1.0)
                mm = mat_model(tx=float(lpos[0]), ty=float(lpos[1]), tz=float(lpos[2]),
                               sx=s, sy=s, sz=s)
                draw(prog, 0, cube_s, cube_n, mm,
                     use_tex=False, color=lcolor, emissive=True)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
