# Original bus reconstruction prompt

Credit: **vietlinhh02**. This is the prompt supplied for the [Sugi no Eki bus case study](../case-studies/sugi-no-eki/README.md).

If you installed the [public architecture skill](../../skills/architectural-environment-production/SKILL.md), replace `architectural_environment_production` with `architectural-environment-production` in the copied prompt. The original run used `/teamwork` in Antigravity. The prompt requests four subagents and a shared Blender session, so check that your client provides the required tools before starting.

```text
Build a complete multi-zone 3D architectural reconstruction of bus model  in Blender
    using the `architectural_environment_production` skill (OpenBIM + CAD Hybrid pipeline + Mandatory Studio Polish).

    Create a working folder `./arch_build_[slug]/` and follow all 6 stages strictly in metric scale (1 BU = 1m):

    0. **Stage 00 & 01 (OpenBIM + CAD Hybrid Blueprints & 1:1 BMesh Compilation)**:
       - Author `00_blueprints/spec.json` locking exact zone coordinates, real-world dimensions, structural grid, and Z-datum elevations.
       - Compile single-source-of-truth structural solids (`Manifold3D` + `IfcOpenShell` `.ifc` + `ezdxf` 4-panel ANSI31 section-hatched CAD blueprint `.dxf`/`.svg`/`.png` if installed, or pure Blender
       orthographic 4-panel fallback) and build 1:1 into organized Blender collections with `bmesh.ops.bisect_plane` horizontal Z-datum imprinting and `UVMap_Metric_1m` box projection.
       - Inspect solid massing and grounding (`get_scene_info` + `look`) before moving on.

    1. **Stage 02 (4-Tile Photorealistic Reference Contact Sheet & 5-Channel PBR Datums)**:
       - Generate a `16:9` 2x2 4-tile photorealistic reference contact sheet (`01_references/reference_contact_sheet_2x2.png`) matching the blueprint from 4 angles: (TL) Hero 3/4 exterior, (TR) Aerial site
       overview, (BL) Eye-level threshold/detail, (BR) Atmospheric courtyard/interior.
       - Inspect the contact sheet to lock proportions, silhouettes, lighting mood ([golden hour late afternoon sunlight filtering through cedar foliage]), and source 5-channel PBR textures mapped to
       `UVMap_Metric_1m`.

    2. **Stage 03 (4-Subagent Specialist Gauntlet Loop)**:
       - Spawn 4 parallel specialist subagents (`Model="inherit"`, one per reference domain: 1. Primary Architecture & Joinery, 2. Site Terrain & Hardscape, 3. Threshold Details, Props & Foliage, 4.
       LookDev, Studio Polish, Lighting & Cameras).
       - Each specialist must write an independent, idempotent zone Python script (`03_scripts/zone_01..04.py`) without calling `execute_blender_code` concurrently; the Master Orchestrator executes scripts
       sequentially in Blender and saves checkpoints.

    3. **Stage 04 (Adversarial Visual Critique Loop)**:
       - Capture "Before" baseline renders first (`04_renders/before_*.png`).
       - Run iterative critique passes comparing live Blender renders against `01_references/reference_contact_sheet_2x2.png`, fixing proportion, recessed opening depth, scale, grounding, and material
       contrast until reaching >= 8.5/10.

    4. **Mandatory Studio Polish (All 5 Blender-Native Visual Strengths)**:
       - Execute all 5 imperfection layers: (1) `Light_Gobo_Canopy` overhead dappled cutout + `light.use_nodes = True` procedural Emission noise (`Scale = 6.0`) on Area/Spot lights; (2) Roughness stacking
       (`ShaderNodeMix` `LINEAR_LIGHT`, `Factor = 0.28`) + `Pointiness` edge-wear & `AmbientOcclusion` crevice dirt; (3) Full-Frame 35mm physical cameras with DoF (`f/1.8?f/2.8`) & Focus Empties; (4)
       Micro-bevels + `ObjectInfo.Random` per-instance macro-variation; (5) Bounded `VolumeScatter` haze, `AgX` color management, and subtle Compositor `FOG_GLOW` + lens dispersion.

    5. **Stage 05 (6-Camera Cycles Showcase, World-Space BMesh Section A-A Cutaway & Progression Matrix)**:
       - Render 6 physical cameras (`Cam_01_Hero_3Q` through `Cam_06_Section_AA_Cutaway`) in Cycles, including a non-destructive world-space `bmesh.ops.bisect_plane` Section A-A cutaway with capped ANSI31
       45-degree hatched cut faces.
       - Stitch `05_deliverables/progression_matrix.png` (Before vs. After) and `05_deliverables/showcase_6cam_sheet.png`, visually verify both sheets, and save the final `.blend`.
```
