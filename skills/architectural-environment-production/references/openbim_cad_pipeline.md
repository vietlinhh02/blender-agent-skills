# Stage 00 & Stage 01: OpenBIM + CAD Hybrid Blueprint Pipeline

This reference defines the deterministic blueprint schema (**Stage 00**) and dual-path compilation (**Stage 01**) so the pipeline works cleanly both when optional AEC Python libraries are present and when running purely inside Blender.

---

## 1. Stage 00 — Master Program & Z-Datum Spec (`00_blueprints/spec.json`)

Write `00_blueprints/spec.json` first to lock dimensions, spatial zoning, Z-datums, materials, and camera anchors before any modeling starts:

```json
{
  "project_name": "Japanese_Temple_Complex",
  "slug": "japanese_temple_complex",
  "units": "METRIC_METERS",
  "site_bounds_m": { "width": 48.0, "depth": 56.0, "ground_z": 0.0 },
  "z_datums_m": {
    "ground": 0.0,
    "stone_plinth": 0.60,
    "floor_main": 0.90,
    "veranda_rail": 1.65,
    "eave_tier_1": 4.20,
    "eave_tier_2": 7.60,
    "eave_tier_3": 10.80,
    "spire_finial": 16.50
  },
  "zones": [
    { "id": "Z1_Pagoda", "center": [0.0, 6.0, 0.0], "footprint_m": [8.4, 8.4], "collection": "01_Primary_Structure" },
    { "id": "Z2_MainHall", "center": [-12.0, -4.0, 0.0], "footprint_m": [14.0, 10.0], "collection": "01_Primary_Structure" },
    { "id": "Z3_Courtyard_Gate", "center": [0.0, -18.0, 0.0], "footprint_m": [6.0, 3.2], "collection": "02_Secondary_Architecture" },
    { "id": "Z4_Garden_Pond", "center": [12.0, -6.0, -0.35], "footprint_m": [16.0, 18.0], "collection": "00_Site_Terrain" }
  ],
  "section_aa": {
    "plane_co": [0.0, 0.0, 0.0],
    "plane_no": [0.0, -1.0, 0.0],
    "description": "Longitudinal section slicing cleanly through Pagoda central core and stone plinth"
  },
  "materials": [
    { "id": "Hinoki_Timber_Aged", "uv_scale_m": 1.0, "roughness_base": 0.55 },
    { "id": "Granite_Plinth_Ashlar", "uv_scale_m": 1.0, "roughness_base": 0.72 },
    { "id": "Kawara_Roof_Tile", "uv_scale_m": 1.0, "roughness_base": 0.42 },
    { "id": "Lime_Plaster_Shikkui", "uv_scale_m": 1.0, "roughness_base": 0.78 }
  ]
}
```

---

## 2. Stage 01 — Library Detection & Dual Compilation Paths

Detect optional libraries cleanly before choosing Path A or Path B:

```python
import importlib.util

HAS_MANIFOLD = importlib.util.find_spec("manifold3d") is not None
HAS_IFC = importlib.util.find_spec("ifcopenshell") is not None
HAS_EZDXF = importlib.util.find_spec("ezdxf") is not None
```

### Path A: Full OpenBIM + CAD Hybrid Compilation (`manifold3d` + `ifcopenshell` + `ezdxf`)

Use when all three packages are installed in the Python environment:

1. **Watertight Structural Solids (`manifold3d`):**
   - Build primary slabs, plinths, walls (with explicit boolean door/window voids), columns, and roof tiers as guaranteed watertight `manifold3d.Manifold` solids.
   - Export watertight intermediate meshes (`to_mesh()`) so Blender receives clean non-self-intersecting geometry.
2. **Semantic OpenBIM Model (`ifcopenshell`):**
   - Always use `ifcopenshell.api.run` (never raw orphan entity calls) to create `IfcProject` → `IfcSite` → `IfcBuilding` → `IfcBuildingStorey` matching each Z-datum in `spec.json`.
   - Assign elements to `IfcSlab`, `IfcWall`, `IfcColumn`, `IfcRoof`, `IfcStair` and save `00_blueprints/model.ifc`.
3. **4-Panel ANSI31 Section-Hatched CAD Blueprint (`ezdxf`):**
   - Create `00_blueprints/blueprints_4panel.dxf` with 4 view panels in model space:
     - **Top-Left:** Ground Floor Plan (`Z = floor_main + 1.2m`)
     - **Top-Right:** Front Architectural Elevation with Z-datum callouts
     - **Bottom-Left:** **Section A-A** slice with true **`ANSI31`** 45° diagonal hatch inside cut walls/slabs/plinths
     - **Bottom-Right:** Site Layout & Zone Dimension Grid
   - Export/render to `00_blueprints/blueprints_4panel.svg` and `00_blueprints/blueprints_4panel.png` (via `ezdxf.addons.drawing` + Matplotlib/Pillow when available) and inspect via `read_file`.

### Path B: Zero-Dependency Blender-Native Fallback (`bpy` + `bmesh` only)

Use automatically if any of `manifold3d`, `ifcopenshell`, or `ezdxf` is missing:

1. **Compile Parametric Solids Directly in `bmesh`:**
   - Construct every plinth, slab, thick wall (with recessed openings), column grid, beam, and multi-tier roof directly via `bmesh` into `01_Primary_Structure`, `02_Secondary_Architecture`, and `00_Site_Terrain`.
   - Keep `spec.json` as the single source of truth so all coordinates and Z-datums match 1:1.
2. **Generate a 4-Panel Orthographic Blueprint Sheet Directly from Blender:**
   - Temporarily spin up orthographic cameras (`cam.data.type = 'ORTHO'`) for:
     - **Plan** (`+Z` looking down, optional ceiling clip via `clip_start`)
     - **Front Elevation** (`-Y` looking `+Y`)
     - **Section A-A** (using `build_section_aa_cutaway` with `Mat_Section_Cut_ANSI31` active!)
     - **Isometric Massing** (3/4 orthographic)
   - Render lightweight Workbench / Solid + Wireframe / Freestyle blueprint views to `04_renders/bp_*.png` and stitch into `00_blueprints/blueprints_4panel.png` (or inspect each panel via `look` / `read_file`).
3. **Apply Horizontal Z-Datum Imprinting & Metric UVs:**
   - Regardless of Path A or Path B, pass every compiled architectural mesh through `apply_metric_box_uv_and_z_datums(obj, z_datums=...)` from [shader_polish_snippets.md](shader_polish_snippets.md) before entering Stage 02.
