# Architectural Environment Production

End-to-end production pipeline for orchestrating coherent, real-world-scale 3D architectural environments in Blender via **Blender MCP** (and optional headless Blender CLI for heavy Cycles passes).

## 1. Environment Preflight & Execution Rules

1. **Inspect Blender First:** Call `get_addon_status` and `get_scene_info` (with verbatim `user_prompt`) to check Blender version, available asset libraries (`polyhaven`, `sketchfab`, `polypizza`), 3D generators, and existing scene contents.
2. **Enforce Blender MCP Portability Rules:**
   - Look up shader/compositor nodes strictly by `node.type` (never localized display names), e.g. `next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")`.
   - Never hardcode enum identifiers; query `bl_rna.properties[...].enum_items` or assign `scene.render.engine` inside `try/except TypeError` to discover valid identifiers.
   - Drive material colors via shader node inputs (`Base Color`), never `material.diffuse_color` alone.
   - Pass the user's request verbatim in `user_prompt` on every Blender MCP call.
   - Set scene units explicitly to Metric (`scene.unit_settings.system = 'METRIC'`, `scale_length = 1.0`, `1 BU = 1m`).
3. **Create a Structured Build Workspace:** Under the current project directory, create `./arch_build_<slug>/` with:
   - `00_blueprints/` (`spec.json`, `.ifc`, `.dxf`, `.svg`, blueprint PNGs)
   - `01_references/` (4-tile photorealistic reference contact sheet + crop notes)
   - `02_textures/` (5-channel PBR maps & procedural configs)
   - `03_scripts/` (modular, idempotent `bpy`/`bmesh` zone scripts)
   - `04_renders/` (`before_*.png`, critique passes, 6-camera Cycles renders)
   - `05_deliverables/` (`progression_matrix.png`, `showcase_6cam_sheet.png`, final `.blend`)
   - `checkpoints/` (`pass_00_massing.blend`, `pass_01.blend`, ...)
4. **Check Optional OpenBIM/CAD Libraries:** Test whether `manifold3d`, `ifcopenshell`, `ezdxf`, and `PIL` are installed in the Python runtime. If available, run the full OpenBIM + CAD Hybrid path; if missing, immediately use the zero-dependency pure `bpy`/`bmesh` orthographic blueprint fallback documented in [references/openbim_cad_pipeline.md](references/openbim_cad_pipeline.md) without stalling.

---

## 2. Six-Stage Production Pipeline (Stages 00–05)

### Stage 00 — Master Program & Z-Datum Spec
- Author `00_blueprints/spec.json` before creating geometry. Lock:
  - Site bounding dimensions and terrain datum (`Z = 0.0m`).
  - Multi-zone spatial coordinates and circulation paths (courtyard, main hall, tower/pagoda, perimeter walls, threshold steps, water/landscape).
  - Exact architectural **Z-datum elevations** (foundation plinth, ground floor finish, window sills, lintels, eave overhangs, multi-tier roof ridges).
  - Structural grid spacing (`bay_x`, `bay_y`), wall thicknesses, roof overhang ratios, and 6 named camera anchors.
  - Material palette mapped to real-world metric UV scales (`UVMap_Metric_1m`).

### Stage 01 — OpenBIM + CAD Hybrid Blueprints & 1:1 BMesh Compilation
- Follow [references/openbim_cad_pipeline.md](references/openbim_cad_pipeline.md) to compile single-source-of-truth structural solids:
  - **Hybrid Path:** Generate watertight CSG solids (`manifold3d`), author `.ifc` spatial hierarchy (`ifcopenshell`), and export a 4-panel ANSI31 section-hatched CAD blueprint sheet (`.dxf` / `.svg` / `.png` via `ezdxf`).
  - **Blender-Native Fallback:** Compile parametric structural solids directly in `bmesh` and render a 4-panel orthographic blueprint (Plan, Front Elevation, Section A-A, Axonometric).
- Compile the massing **1:1 into Blender collections**:
  - `00_Site_Terrain`, `01_Primary_Structure`, `02_Secondary_Architecture`, `03_Threshold_Details`, `04_Foliage_Props`, `05_Lighting_Atmosphere`, `06_Cameras`, `99_Cutaway_Section` (hidden in main render).
- Run horizontal **Z-datum imprinting** via `bmesh.ops.bisect_plane` at every spec elevation and generate `UVMap_Metric_1m` (1 UV unit = 1 meter) on architectural meshes (see [references/shader_polish_snippets.md](references/shader_polish_snippets.md)).
- Inspect `look(mode="angles", shading="solid")` and `get_scene_info(fields=["location", "size", "ground"])` to verify proportions, scale, and grounding before proceeding.

### Stage 02 — 4-Tile Reference Contact Sheet & 5-Channel PBR Datums
- Invoke the `image-generator` subagent to create a **16:9 2×2 4-tile photorealistic reference contact sheet** (`01_references/reference_contact_sheet_2x2.png`) matching the blueprint layout and lighting direction:
  - **Tile 1 (Top-Left):** Hero 3/4 exterior view showing primary massing, roof silhouette, and sun direction.
  - **Tile 2 (Top-Right):** Aerial / elevated site overview showing multi-zone layout and landscape context.
  - **Tile 3 (Bottom-Left):** Eye-level threshold / architectural detail view (joinery, stone plinth, carved brackets, recessed openings).
  - **Tile 4 (Bottom-Right):** Atmospheric courtyard or interior view showing dappled light, volumetrics, and material roughness response.
- Inspect `reference_contact_sheet_2x2.png` with `read_file` to lock proportions, silhouette rhythm, color temperature, and material datums.
- Source **5-channel PBR material sets** (Base Color, Roughness, Normal, Bump/Height, AO) mapped to `UVMap_Metric_1m`:
  - Prefer Poly Haven via `search_assets` (`asset_type="textures"`, `min_size_m=2.0+` for floors/walls/terrain) + `import_asset`.
  - Generate bespoke architectural surfaces/tiles via `image-generator` when Poly Haven lacks an exact cultural or historic match, and supplement missing channels procedurally via Blender nodes.

### Stage 03 — 4-Subagent Specialist Gauntlet Loop
Spawn 4 specialist subagents (`invoke_subagent` with `Model="inherit"`, or `swarm` when coordinating interactively), assigning one reference tile / domain per specialist:
1. **Specialist 1 — Primary Architecture & Structural Joinery:** Walls, pillars, beams, brackets, multi-tier roofs, stairs, and structural trims in `01_Primary_Structure` + `02_Secondary_Architecture`.
2. **Specialist 2 — Site Terrain, Hardscape & Context:** Ground contours, stone paving, retaining walls, water basins, courtyards, and perimeter context in `00_Site_Terrain`.
3. **Specialist 3 — Threshold Details, Props & Foliage:** Doors, shoji/lattice screens, window mullions, lanterns, hardware, moss, rocks, and scatter foliage in `03_Threshold_Details` + `04_Foliage_Props` (using `search_assets`/`import_asset` or `generate_3d` for unique focal hero props, scaled strictly by reported `world_bounding_box`).
4. **Specialist 4 — LookDev, Materials, Lighting & Cameras:** 5-channel PBR node graphs, all 5 Mandatory Studio Polish layers, 6 physical cameras, and compositor setup in `05_Lighting_Atmosphere` + `06_Cameras`.

> **CRITICAL CONCURRENCY RULE:** Live Blender MCP drives one shared Blender session. Parallel subagents MUST author independent, idempotent Python scripts (`03_scripts/zone_01_structure.py` .. `03_scripts/zone_04_lookdev.py`) targeting only their assigned collections. The **Master Orchestrator executes those scripts sequentially** via `execute_blender_code`, checks `get_scene_info`, saves `.blend` checkpoints, and resolves any geometry collisions.

### Stage 04 — Adversarial Visual Critique Loop
1. Capture a **Before baseline** right after Stage 01/initial assembly (`04_renders/before_hero.png`, `04_renders/before_site.png`) so progression is provably documented.
2. Save `checkpoints/pass_0N.blend` before each refinement iteration.
3. Render `look(mode="camera", shading="rendered")` or Cycles preview frames and compare side-by-side against `01_references/reference_contact_sheet_2x2.png`.
4. Run an **Adversarial Critic** pass (either directly or via a dedicated critic `invoke_subagent` inspecting both images) scoring `0–10` across six criteria:
   - Silhouette & Proportions vs. Blueprint/Reference
   - Architectural Depth & Recessed Openings (no flat cards)
   - Material Scale (`UVMap_Metric_1m`) & Micro-Imperfection
   - Lighting Contrast, Gobos & Atmospheric Depth
   - Grounding & Contact (zero floating geometry, clean intersections)
   - Overall Studio Photorealism
5. Iterate targeted fixes per failing zone until the scene scores **≥ 8.5 / 10** (or 3–5 focused passes resolve every defect). Never overwrite or degrade collections that already passed critique.

### Stage 05 — 6-Camera Cycles Showcase, World-Space BMesh Section A-A Cutaway & Progression Matrix
1. Ensure all 6 physical cameras exist in `06_Cameras`:
   - `Cam_01_Hero_3Q` (35mm, `f/2.2`)
   - `Cam_02_Aerial_Site` (28mm, `f/5.6`)
   - `Cam_03_EyeLevel_Threshold` (35mm, `f/2.0`, `shift_y` vertical correction)
   - `Cam_04_Detail_CloseUp` (85mm, `f/1.8`)
   - `Cam_05_Atmospheric_Interior` (24mm, `f/2.2`)
   - `Cam_06_Section_AA_Cutaway` (35mm, `f/4.0`, framing the Section A-A plane)
2. **Non-Destructive World-Space BMesh Section A-A Cutaway:** Duplicate architectural meshes into `99_Cutaway_Section`, slice in world space using `bmesh.ops.bisect_plane(..., clear_outer=True)`, cap open loops with a solid cut-face material featuring procedural **ANSI31 45° diagonal hatching**, toggle `99_Cutaway_Section` visible ONLY when rendering `Cam_06_Section_AA_Cutaway`, and restore original visibility immediately afterward.
3. Render all 6 cameras with Cycles (+ OpenImageDenoise) to `04_renders/cam_01.png` .. `cam_06.png`.
4. Run [scripts/build_progression_matrix.py](scripts/build_progression_matrix.py) to compile:
   - `05_deliverables/progression_matrix.png` (Before vs. After comparison grid)
   - `05_deliverables/showcase_6cam_sheet.png` (3×2 6-camera Cycles showcase sheet)
5. Inspect both final sheets with `read_file` to confirm clean framing, typography, and photoreal output.

---

## 3. Architectural Modeling & Anti-CG Rules

- **Real Thickness & Recessed Openings:** Walls, roofs, slabs, and frames MUST have physical thickness. Windows, doors, alcoves, and vents MUST have recessed jamb depth, frames, mullions, sills, and backing geometry — never flat planes glued onto walls.
- **Zero Floating Geometry:** After placing terrain, plinths, pillars, props, and foliage, run `get_scene_info(fields=["location", "size", "ground"])` to verify every object rests cleanly on its supporting datum (`ground` offset ≈ `0`, intentional sink `1–3cm` for rocks/posts/foliage roots).
- **Real-World Scale:** Respect human scale (`door ≈ 2.1m × 0.9m`, `stair riser ≈ 0.16–0.18m`, `tread ≈ 0.28–0.30m`, `ceiling ≈ 2.8–4.0m`). Resize every imported/generated asset immediately using its reported `world_bounding_box`.

---

## 4. Five Blender-Native Visual Strengths for Breaking Digital Perfection (Mandatory Studio Polish)

Perfect computer-generated geometry looks inherently fake. To achieve true studio photorealism, every build MUST execute these five Blender-native optical and physical imperfection layers (complete `bpy` implementations in [references/shader_polish_snippets.md](references/shader_polish_snippets.md)):

1. **Gobos & Procedural Light Texturing (Breaking Up Uniform Light):**
   - **Gobos (Go-Betweens):** Place an overhead plane (`Light_Gobo_Canopy`) with a black-and-white alpha-cutout procedural foliage/slat shader (`ShaderNodeTexVoronoi` / `ShaderNodeTexNoise` → `ShaderNodeBsdfTransparent` mixed with `ShaderNodeBsdfDiffuse`) directly in front of primary directional/spot lights to cast dappled real-world light occlusion across floors and walls. Set `visible_camera = False`, `visible_glossy = False`, `visible_diffuse = False`, and `visible_shadow = True`.
   - **Procedural Light Emission Noise:** Enable `light.use_nodes = True` on all Area/Spot lights and wire a `ShaderNodeTexNoise` (`Scale = 6.0`) → `ShaderNodeValToRGB` into the light's `Emission` color/strength so light intensity fluctuates naturally across surfaces.
2. **High-Frequency Roughness Stacking & Pointiness/AO Imperfection Stacking:**
   - **Multi-Layer Roughness Stacking:** Never use a single flat roughness map. Stack the base Nano Banana / PBR roughness texture with a secondary procedural grunge/micro-noise map using a `ShaderNodeMix` set to `LINEAR_LIGHT` (`Factor = 0.28`) so surfaces catch specular glints across grazing angles.
   - **Procedural Edge-Wear & Crevice Dirt:** Plug `ShaderNodeNewGeometry.outputs['Pointiness']` and `ShaderNodeAmbientOcclusion` through `ShaderNodeValToRGB` into Base Color and Roughness so Blender automatically detects sharp edges for subtle edge-wear and crevice dirt where objects meet.
3. **Physical Camera Simulation, Full-Frame 35mm Sensor & True Depth of Field (`f/1.8–f/2.8`):**
   - Configure every camera with `sensor_fit = 'HORIZONTAL'`, `sensor_width = 36.0`, true architectural focal lengths (`24/35/50/85mm`), `dof.use_dof = True`, `aperture_fstop = 1.8–2.8` for hero/threshold/detail shots (`4.0–5.6` for aerial site overviews) driven by dedicated Focus Target empties, and `shift_y` vertical perspective control.
4. **Micro-Beveling & Per-Instance Organic Macro-Variation:**
   - Add a subtle `Bevel` modifier (`width = 0.005–0.015`, `segments = 2`, `limit_method = 'ANGLE'`) or Cycles `ShaderNodeBevel` so edges catch natural specular highlights instead of razor-sharp CG lines.
   - Drive subtle per-instance hue/value/roughness variation via `ShaderNodeObjectInfo.outputs['Random']` + world-space macro noise on all modular tiles, planks, bricks, stones, and foliage.
5. **Volumetric Atmosphere, AgX Color Management & Optical Compositing:**
   - Enclose the hero lighting zone in a bounded volume cube (`Atmosphere_Volume_Domain`, `visible_shadow = False` or low density) with `ShaderNodeVolumeScatter` (`Density = 0.001–0.006`, `Anisotropy = 0.65`) to reveal subtle light shafts through gobos.
   - Use **AgX** color management (`view_transform = 'AgX'`) and add restrained Compositor polish (`Glare` set to `FOG_GLOW` + subtle `Lens Distortion` dispersion `0.003–0.005`).

---

## 5. Final Verification & Deliverables Checklist

Before finishing and reporting to the user, verify every item:
- [ ] Saved final clean `.blend` inside `05_deliverables/` (with textures packed via `bpy.ops.file.pack_all()` if external maps are used).
- [ ] `get_scene_info(fields=["location", "size", "ground"])` confirms zero unintended floating objects or broken scales.
- [ ] All **5 Mandatory Studio Polish layers** are active on materials, lights, cameras, and compositor.
- [ ] All 6 Cycles showcase cameras (`04_renders/cam_01.png` .. `cam_06.png`) rendered and visually inspected.
- [ ] World-space BMesh **Section A-A cutaway** rendered cleanly without altering the main scene collection.
- [ ] `05_deliverables/progression_matrix.png` (Before vs. After) and `05_deliverables/showcase_6cam_sheet.png` generated and visually verified with `read_file`.

---

## Supporting References & Prompt Resources

- OpenBIM + CAD Hybrid compilation & zero-dependency fallback: [references/openbim_cad_pipeline.md](references/openbim_cad_pipeline.md)
- Blender 4.x/5.x `bpy`/`bmesh` helpers for Studio Polish & Cutaway: [references/shader_polish_snippets.md](references/shader_polish_snippets.md)
- Progression Matrix & 6-Cam Showcase Stitcher: [scripts/build_progression_matrix.py](scripts/build_progression_matrix.py)
- Ready-to-paste Master Conversation Prompts: [resources/conversation_prompts.md](resources/conversation_prompts.md)
