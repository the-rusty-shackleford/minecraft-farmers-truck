"""The Farmer's Pickup's art, as code: nfx's Blockbench project split into what Vanilla Wheels reads, and the profile off it.

Run from the repository root:

    uv run --no-project python devtools/art/build.py

Reads devtools/art/preview/pickup.bbmodel -- nfx's project as saved (his pickup_2seater_Final of 2026-09-11) -- and writes:

  src/main/resources/assets/farmpickup/vanillawheels/mesh/pickup.bbmodel        the body: everything but the wheels
  src/main/resources/assets/farmpickup/vanillawheels/mesh/pickup_wheel.bbmodel  wheel_0_left, recentred on its axle
  src/main/resources/data/farmpickup/vanillawheels/vehicle/pickup.json          the profile, its numbers measured off the cubes
  src/main/resources/assets/farmpickup/lang/en_us.json

nfx's build, ported from his handoff; what it does to the model and why:

- The model was rigged with its own folder names, so cubes are wrapped into the folders the profile's
  selectors name: `lenses` (the headlights), `glass` (the windshield and the cab's rear pane), and a
  `paint` folder inside bed, cab, doors, windshield and front holding every red panel.
- Paint in Vanilla Wheels is a vertex-colour multiply (the protocol's own body texture is near-white);
  this model bakes its red in, so the red texels of the painted faces are greyed to the same brightness
  and the profile's `factory` (the model's red) restores the look, so a dye replaces the red instead of
  multiplying with it. The tailgate's panels are painted too (a door's painted part takes the dye since
  Vanilla Wheels 1.5.0); a patch shared between a painted cube and an unpainted one would be duplicated
  first, though none is now.
- The gauges are moved to the centre of the console: nfx set them behind the wheel, whose rim hides them
  from the driver's seat. The fuel needle is raised so its base sits on the dial's centre, the gauge's pivot.
- The Blockbench animations are dropped; the tailgate swings by the profile's `doors`.

Units are model units, 1/16 block.
"""
from __future__ import annotations

import base64
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from png import png_decode, png_encode  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "devtools/art/preview/pickup.bbmodel"
MODID = "farmpickup"
VEHICLE = "pickup"
ASSETS = ROOT / "src/main/resources/assets" / MODID
DATA = ROOT / "src/main/resources/data" / MODID
MESH = ASSETS / "vanillawheels/mesh"
FACTORY = (178, 33, 37)          # the model's body red; painted texels are greyed relative to it
BASE_LUM = 0.299 * FACTORY[0] + 0.587 * FACTORY[1] + 0.114 * FACTORY[2]

m = json.loads(SRC.read_text(encoding="utf-8"))
gname = {g["uuid"]: g["name"] for g in m["groups"]}
els = {e["uuid"]: e for e in m["elements"]}
# ---------------------------------------------------------------- outliner helpers
def strip(model, names):
    """remove top-level groups by name from outliner + groups array + their elements"""
    drop = set()

    def collect(n):
        if isinstance(n, str):
            drop.add(n); return
        drop.add(n["uuid"])
        for c in n.get("children", []): collect(c)

    keep = []
    for n in model["outliner"]:
        if not isinstance(n, str) and gname[n["uuid"]] in names: collect(n)
        else: keep.append(n)
    model["outliner"] = keep
    model["groups"] = [g for g in model["groups"] if g["uuid"] not in drop]
    model["elements"] = [e for e in model["elements"] if e["uuid"] not in drop]


def find_group(node_list, name):
    for n in node_list:
        if isinstance(n, str): continue
        if gname[n["uuid"]] == name: return n
        r = find_group(n.get("children", []), name)
        if r: return r
    return None


def wrap(model, parent_name, new_name, cube_names, origin=(0, 0, 0)):
    """move the named cubes of group `parent_name` into a new child group `new_name`
    (format 5.0: the node goes in the outliner, its name/origin in `groups`)"""
    parent = find_group(model["outliner"], parent_name)
    assert parent, parent_name
    wanted = {u for u in parent["children"] if isinstance(u, str) and els[u]["name"] in cube_names}
    assert len(wanted) == len(cube_names), (parent_name, cube_names, [els[u]["name"] for u in parent["children"] if isinstance(u, str)])
    uuid = f"{new_name}-{parent_name}-0000-0000-000000000000"
    node = {"uuid": uuid, "isOpen": False, "children": [u for u in parent["children"] if isinstance(u, str) and u in wanted]}
    parent["children"] = [u for u in parent["children"] if not (isinstance(u, str) and u in wanted)] + [node]
    model["groups"].append({"name": new_name, "uuid": uuid, "origin": list(origin), "rotation": [0, 0, 0],
                            "export": True, "visibility": True, "autouv": 0, "selected": False, "shade": True,
                            "mirror_uv": False, "isOpen": False, "locked": False, "color": 0})
    gname[uuid] = new_name


def cube(model, name):
    r = [e for e in model["elements"] if e["name"] == name]
    assert len(r) == 1, (name, len(r))
    return r[0]


# ---------------------------------------------------------------- common cleanup
assert all(f.get("texture") == 0 for e in m["elements"] for f in e["faces"].values())
m["textures"] = [m["textures"][0]]
m["textures"][0]["name"] = f"{VEHICLE}.png"
m["textures"][0]["id"] = "0"
m.pop("animations", None)          # the loader ignores them; the tailgate swings via the profile's `doors`

# The gauges to the centre of the console: nfx set the binnacle behind the wheel, where the rim hides
# the dials from the driver's seat (Rusty, 2026-09-13). The binnacle, both dials and both needles slide
# along x by the binnacle's own centre, to the centreline; the gauge pivots below are measured after.
def shift_x(model, cube_names, group_names, dx):
    for e in model["elements"]:
        if e["name"] in cube_names:
            e["from"][0] = round(e["from"][0] + dx, 4); e["to"][0] = round(e["to"][0] + dx, 4)
            if "origin" in e: e["origin"][0] = round(e["origin"][0] + dx, 4)
    for g in model["groups"]:
        if g["name"] in group_names:
            g["origin"][0] = round(g["origin"][0] + dx, 4)
binnacle = cube(m, "binnacle")
to_centre = -round((binnacle["from"][0] + binnacle["to"][0]) / 2, 4)
shift_x(m, {"binnacle", "dial_speed", "dial_fuel", "needle_speed", "needle_fuel"},
        {"dial_speed_grp", "dial_fuel_grp", "needle_speed_grp", "needle_fuel_grp"}, to_centre)
print(f"gauges moved {to_centre} along x, to the centre of the console")

# fuel needle: base on the dial centre so the gauge pivot (dial centre) is its root
dial = cube(m, "dial_fuel"); needle = cube(m, "needle_fuel")
dial_cy = (dial["from"][1] + dial["to"][1]) / 2
dy = round(dial_cy - needle["from"][1], 4)
needle["from"][1] = round(needle["from"][1] + dy, 4); needle["to"][1] = round(needle["to"][1] + dy, 4)
print(f"needle_fuel raised {dy} so its base sits on the dial centre y={dial_cy}")

# selector groups
PAINT = {
    "bed": ["bed_side_left", "bed_side_right", "bed_rail_left", "bed_rail_right", "bed_front"],
    "cab": ["cab_rear_lower", "cab_rear_pillar_left", "cab_rear_pillar_right", "cowl"],
    "doors": ["door_left", "door_right"],
    "windshield": ["a_pillar_left", "a_pillar_right", "windshield_header", "windshield_base"],
    "front": ["front_wing_left", "front_wing_right", "hood", "nose_top", "nose_bottom", "nose_side_left", "nose_side_right"],
}
# The tailgate is a door; since Vanilla Wheels 1.5.0 a door's painted panels take the dye like the body's,
# so its two red cubes are painted too (the tail lights are not).
PAINT["tailgate_hinge"] = ["tailgate", "tailgate_rail"]
for parent, names in PAINT.items():
    wrap(m, parent, "paint", names)
wrap(m, "front", "lenses", ["headlight_left", "headlight_right"])
wrap(m, "windshield", "glass", ["windshield_glass"])
wrap(m, "cab", "glass", ["cab_rear_glass"])

# ---------------------------------------------------------------- grey the painted texels
src = m["textures"][0]["source"]
tw, th, buf = png_decode(base64.b64decode(src.split(",", 1)[1]))
res = m["resolution"]; sx, sy = tw / res["width"], th / res["height"]
painted = {n for names in PAINT.values() for n in names}
rects = {}
for e in m["elements"]:
    for f in e["faces"].values():
        u0, v0, u1, v1 = f["uv"]
        r = (int(round(min(u0, u1) * sx)), int(round(min(v0, v1) * sy)), int(round(max(u0, u1) * sx)), int(round(max(v0, v1) * sy)))
        rects.setdefault(r, set()).add(e["name"])
# a patch shared by a painted cube and an unpainted one (the tailgate reuses the bed side/rail
# patches) is duplicated into free atlas space for the unpainted cube before the greying
def free_slot(w, h):
    used = list(rects)
    for y in range(0, th - h, 2):
        for x in range(0, tw - w, 2):
            if all(x + w <= a or x >= c or y + h <= b or y >= d for a, b, c, d in used):
                return x, y
    raise RuntimeError("atlas full")
for r, names in [(r, n) for r, n in rects.items() if (n & painted) and (n - painted)]:
    w, h = max(r[2] - r[0], 1), max(r[3] - r[1], 1)
    x, y = free_slot(w + 2, h + 2); x += 1; y += 1
    for j in range(h):
        o0, o1 = ((r[1] + j) * tw + r[0]) * 4, ((y + j) * tw + x) * 4
        buf[o1:o1 + w * 4] = buf[o0:o0 + w * 4]
    for e in m["elements"]:
        if e["name"] in names - painted:
            for f in e["faces"].values():
                u0, v0, u1, v1 = f["uv"]
                if (int(round(min(u0, u1) * sx)), int(round(min(v0, v1) * sy)), int(round(max(u0, u1) * sx)), int(round(max(v0, v1) * sy))) == r:
                    du, dv = (x - r[0]) / sx, (y - r[1]) / sy
                    f["uv"] = [round(u0 + du, 4), round(v0 + dv, 4), round(u1 + du, 4), round(v1 + dv, 4)]
    rects[(x, y, x + w, y + h)] = names - painted
    rects[r] = names & painted
    print(f"patch {r} duplicated at ({x},{y}) for {sorted(names - painted)}")
greyed = 0
for r, names in rects.items():
    if not names & painted: continue
    for y in range(r[1], max(r[3], r[1] + 1)):
        for x in range(r[0], max(r[2], r[0] + 1)):
            o = (y * tw + x) * 4
            R, G, B = buf[o], buf[o + 1], buf[o + 2]
            if R > 60 and R > 2.2 * G and R > 2.2 * B:            # red texel -> grey of the same brightness
                g = min(255, int(round(255 * (0.299 * R + 0.587 * G + 0.114 * B) / BASE_LUM)))
                buf[o] = buf[o + 1] = buf[o + 2] = g; greyed += 1
m["textures"][0]["source"] = "data:image/png;base64," + base64.b64encode(png_encode(tw, th, buf)).decode()
print(f"greyed {greyed} texels in {sum(1 for r, n in rects.items() if n & painted)} patches")

# ---------------------------------------------------------------- body mesh
MESH.mkdir(parents=True, exist_ok=True)
body = copy.deepcopy(m)
strip(body, {"wheels"})
body["name"] = VEHICLE; body["model_identifier"] = VEHICLE
(MESH / f"{VEHICLE}.bbmodel").write_text(json.dumps(body, separators=(",", ":")), encoding="utf-8")
print("body: elements", len(body["elements"]), "groups", sorted({g["name"] for g in body["groups"]}))

# ---------------------------------------------------------------- wheel mesh
wheel = copy.deepcopy(m)
strip(wheel, {gname[x["uuid"]] for x in wheel["outliner"] if not isinstance(x, str)} - {"wheels"})
wg = [n for n in wheel["outliner"] if not isinstance(n, str)][0]
wg["children"] = [c for c in wg["children"] if gname[c["uuid"]] == "wheel_0_left"]
wels = {e["uuid"]: e for e in wheel["elements"]}
wheel["elements"] = [wels[i] for i in wg["children"][0]["children"]]
wheel["groups"] = [g for g in wheel["groups"] if g["name"] in {"wheels", "wheel_0_left"}]
centres = {tuple(e["origin"]) for e in wheel["elements"] if e.get("rotation") and any(e["rotation"])}
assert len(centres) == 1, centres
cx, cy, cz = centres.pop()
tread = max(abs(e["to"][1] - cy) for e in wheel["elements"] if not any(e.get("rotation", [0, 0, 0])) and e["name"].startswith("tyre"))
def shift(v): return [round(v[0] - cx, 4), round(v[1] - cy, 4), round(v[2] - cz, 4)]
for e in wheel["elements"]:
    e["from"] = shift(e["from"]); e["to"] = shift(e["to"])
    if "origin" in e: e["origin"] = shift(e["origin"])
for g in wheel["groups"]: g["origin"] = [0, 0, 0]
wheel["name"] = f"{VEHICLE}_wheel"; wheel["model_identifier"] = f"{VEHICLE}_wheel"
(MESH / f"{VEHICLE}_wheel.bbmodel").write_text(json.dumps(wheel, separators=(",", ":")), encoding="utf-8")
print(f"wheel: axle centre ({cx}, {cy}, {cz}) tread radius {tread} elements {len(wheel['elements'])}")

# ---------------------------------------------------------------- profile (model units, scale 1/16)
def box(name):
    e = cube(m, name); return e["from"], e["to"]
def centre(name, i):
    f, t = box(name); return round((f[i] + t[i]) / 2, 3)

cushion_top = box("seat_cushion_left")[1][1]
seat_y = round(cushion_top + 0.42, 2)              # Trailblazer: seat point 0.42 above the cushion top
seat_x, seat_z = centre("seat_cushion_left", 0), centre("seat_cushion_left", 2)
hitch_f, hitch_t = box("hitch")
lens_f, lens_t = box("headlight_left")
bumper_rear = min(hitch_f[2], box("bumper_rear")[0][2]); bumper_front = box("bumper_front")[1][2]
roof_top = box("roof")[1][1]
cab_w = box("roof")[1][0]
fender_w = box("flare_fl_2")[1][0]
tyre_top = box("tyre_0_0")[1][1]
tg = find_group(m["outliner"], "tailgate_hinge"); tg_origin = [g for g in m["groups"] if g["uuid"] == tg["uuid"]][0]["origin"]
bed_front_z = box("bed_front")[1][2]
dash_top = box("dash_top")
# The bed's inside: between the side walls, tailgate to front wall, on the floor's top.
bed_x = box("bed_side_left")[0][0]
bed_z = round((box("bed_floor")[0][2] + box("bed_floor")[1][2]) / 2, 2)
bed_floor_top = box("bed_floor")[1][1]
bed_len = box("bed_floor")[1][2] - box("bed_floor")[0][2]
chest_scale = round(min(bed_len / 32.0, (2 * bed_x) / 32.0, (box("bed_side_left")[1][1] - bed_floor_top) / 14.0) * 0.95, 2)

PROFILE = {
    "mesh": f"{MODID}:{VEHICLE}",
    "wheel_mesh": f"{MODID}:{VEHICLE}_wheel",
    "scale": 0.0625,
    "handedness": "right",
    "body": {                                       # cab width x bumper-to-hitch length x roof height, in blocks
        "width": round(2 * cab_w / 16, 2), "length": round((bumper_front - bumper_rear) / 16, 2), "height": round(roof_top / 16, 2),
        "parts": [{"at": [0, cy, cz], "width": round(2 * fender_w / 16, 2), "height": round(tyre_top / 16, 2)},
                  {"at": [0, cy, -cz], "width": round(2 * fender_w / 16, 2), "height": round(tyre_top / 16, 2)}]},
    "seats": [{"at": [seat_x, seat_y, seat_z], "driver": True}, {"at": [-seat_x, seat_y, seat_z]}],
    "wheels": {"radius": tread, "positions": [
        {"forward": cz, "right": cx, "up": cy, "steers": True}, {"forward": cz, "right": -cx, "up": cy, "steers": True},
        {"forward": -cz, "right": cx, "up": cy}, {"forward": -cz, "right": -cx, "up": cy}]},
    # driving numbers identical to the Trailblazer's (climb 1.0: two-block climbs lurch worst)
    "engine": {"max_speed": 0.9, "acceleration": 0.02, "reverse_speed": 0.3, "brake": 0.05, "drag": 0.01},
    "handling": {"grip": 0.85, "steer_degrees": 32, "drift_grip": 0.12, "drift_boost": 0.3, "drift_charge_ticks": 40},
    "climb": 1.0,
    "mass": 1.45,
    "fuel": {"capacity": 24000},
    # Two double chests in the bed, one along each side, facing inward, scaled to fit the bed's floor
    # side by side (a double chest is two blocks long and one deep before the scale); six rows each.
    "storage": {"chests": [
        {"at": [round(bed_x - 8 * chest_scale, 2), bed_floor_top, bed_z], "yaw": 90, "scale": chest_scale, "rows": 6},
        {"at": [round(-(bed_x - 8 * chest_scale), 2), bed_floor_top, bed_z], "yaw": -90, "scale": chest_scale, "rows": 6}]},
    "gauges": [
        {"kind": "speed", "part": {"group": "needle_speed_grp"},
         "pivot": [centre("needle_speed", 0), centre("dial_speed", 1), centre("needle_speed", 2)],
         "axis": [0, 0, 1], "zero": -2.094, "sweep": 4.189},
        {"kind": "fuel", "part": {"group": "needle_fuel_grp"},
         "pivot": [centre("needle_fuel", 0), centre("dial_fuel", 1), centre("needle_fuel", 2)],
         "axis": [0, 0, 1], "zero": -2.094, "sweep": 4.189}],
    "headlights": {"at": [[centre("headlight_left", 0), centre("headlight_left", 1), round(lens_t[2] + 0.5, 2)],
                          [-centre("headlight_left", 0), centre("headlight_left", 1), round(lens_t[2] + 0.5, 2)]],
                   "part": {"group": "lenses"}, "range": 10},
    "horn": "vanillawheels:horn.truck",
    "radio": {"at": [-9, dash_top[1][1], round((dash_top[0][2] + dash_top[1][2]) / 2, 2)]},   # passenger side of the dash top
    "hitch": {"rear": [0, round((hitch_f[1] + hitch_t[1]) / 2, 2), hitch_f[2]]},               # ball centre, rear face
    "doors": [{"part": {"group": "tailgate_hinge"}, "hinge": tg_origin, "axis": [1, 0, 0], "open": -1.5708}],  # -90 deg drops the tailgate
    "paint": {"part": {"group": "paint"}, "default": "red", "factory": "#%02x%02x%02x" % FACTORY},
    "glass": {"group": "glass"},
    "sounds": {"engine": "vanillawheels:engine.petrol"},
}
pdir = DATA / "vanillawheels/vehicle"
pdir.mkdir(parents=True, exist_ok=True)
(pdir / f"{VEHICLE}.json").write_text(json.dumps(PROFILE, indent=2) + "\n", encoding="utf-8")
(ASSETS / "lang").mkdir(parents=True, exist_ok=True)
(ASSETS / "lang/en_us.json").write_text(json.dumps({f"vehicle.{MODID}.{VEHICLE}": "Farmer's Pickup"}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: PROFILE[k] for k in ("body", "seats", "wheels", "storage", "gauges", "headlights", "hitch", "doors")}, indent=1))

