# Conversation Prompts for `architectural-environment-production`

Ready-to-paste Master Prompts for starting a new Google Antigravity conversation with Blender MCP connected.

---

## Template A — Full Multi-Zone Master Prompt (English, Canonical Stage 00–05 Pipeline)

Replace the bracketed `[...]` placeholders and paste directly into a new Antigravity conversation (tip: pair with `/goal` for unattended multi-pass builds):

```text
Build a complete multi-zone 3D architectural reconstruction of [a historic Japanese temple complex with a 3-tier pagoda, main hall, stone courtyard, torii gate, moss garden, and koi pond] in Blender using the `architectural-environment-production` skill (OpenBIM + CAD Hybrid pipeline + Mandatory Studio Polish).

Create a working folder `./arch_build_[slug]/` and follow all 6 stages strictly in metric scale (1 BU = 1m):

0. **Stage 00 & 01 (OpenBIM + CAD Hybrid Blueprints & 1:1 BMesh Compilation)**:
   - Author `00_blueprints/spec.json` locking exact zone coordinates, real-world dimensions, structural grid, and Z-datum elevations.
   - Compile single-source-of-truth structural solids (`Manifold3D` + `IfcOpenShell` `.ifc` + `ezdxf` 4-panel ANSI31 section-hatched CAD blueprint `.dxf`/`.svg`/`.png` if installed, or pure Blender orthographic 4-panel fallback) and build 1:1 into organized Blender collections with `bmesh.ops.bisect_plane` horizontal Z-datum imprinting and `UVMap_Metric_1m` box projection.
   - Inspect solid massing and grounding (`get_scene_info` + `look`) before moving on.

1. **Stage 02 (4-Tile Photorealistic Reference Contact Sheet & 5-Channel PBR Datums)**:
   - Generate a `16:9` 2x2 4-tile photorealistic reference contact sheet (`01_references/reference_contact_sheet_2x2.png`) matching the blueprint from 4 angles: (TL) Hero 3/4 exterior, (TR) Aerial site overview, (BL) Eye-level threshold/detail, (BR) Atmospheric courtyard/interior.
   - Inspect the contact sheet to lock proportions, silhouettes, lighting mood ([golden hour late afternoon sunlight filtering through cedar foliage]), and source 5-channel PBR textures mapped to `UVMap_Metric_1m`.

2. **Stage 03 (4-Subagent Specialist Gauntlet Loop)**:
   - Spawn 4 parallel specialist subagents (`Model="inherit"`, one per reference domain: 1. Primary Architecture & Joinery, 2. Site Terrain & Hardscape, 3. Threshold Details, Props & Foliage, 4. LookDev, Studio Polish, Lighting & Cameras).
   - Each specialist must write an independent, idempotent zone Python script (`03_scripts/zone_01..04.py`) without calling `execute_blender_code` concurrently; the Master Orchestrator executes scripts sequentially in Blender and saves checkpoints.

3. **Stage 04 (Adversarial Visual Critique Loop)**:
   - Capture "Before" baseline renders first (`04_renders/before_*.png`).
   - Run iterative critique passes comparing live Blender renders against `01_references/reference_contact_sheet_2x2.png`, fixing proportion, recessed opening depth, scale, grounding, and material contrast until reaching >= 8.5/10.

4. **Mandatory Studio Polish (All 5 Blender-Native Visual Strengths)**:
   - Execute all 5 imperfection layers: (1) `Light_Gobo_Canopy` overhead dappled cutout + `light.use_nodes = True` procedural Emission noise (`Scale = 6.0`) on Area/Spot lights; (2) Roughness stacking (`ShaderNodeMix` `LINEAR_LIGHT`, `Factor = 0.28`) + `Pointiness` edge-wear & `AmbientOcclusion` crevice dirt; (3) Full-Frame 35mm physical cameras with DoF (`f/1.8–f/2.8`) & Focus Empties; (4) Micro-bevels + `ObjectInfo.Random` per-instance macro-variation; (5) Bounded `VolumeScatter` haze, `AgX` color management, and subtle Compositor `FOG_GLOW` + lens dispersion.

5. **Stage 05 (6-Camera Cycles Showcase, World-Space BMesh Section A-A Cutaway & Progression Matrix)**:
   - Render 6 physical cameras (`Cam_01_Hero_3Q` through `Cam_06_Section_AA_Cutaway`) in Cycles, including a non-destructive world-space `bmesh.ops.bisect_plane` Section A-A cutaway with capped ANSI31 45-degree hatched cut faces.
   - Stitch `05_deliverables/progression_matrix.png` (Before vs. After) and `05_deliverables/showcase_6cam_sheet.png`, visually verify both sheets, and save the final `.blend`.
```

---

## Template B — Vietnamese Master Prompt (Dùng trực tiếp bằng tiếng Việt)

```text
Hãy dùng skill `architectural-environment-production` để dựng hoàn chỉnh một quần thể kiến trúc 3D đa khu vực trong Blender: [mô tả công trình, bối cảnh và thời điểm ánh sáng — ví dụ: Quần thể chùa Nhật Bản gồm tháp 3 tầng, chính điện, sân đá, cổng Torii và vườn rêu lúc nắng chiều].

Thực hiện đủ toàn bộ quy trình 6 giai đoạn (Stages 00–05) theo đúng hệ mét (1 BU = 1m) trong thư mục `./arch_build_[slug]/`:
0. **Stage 00 & 01:** Viết `00_blueprints/spec.json` khóa tọa độ khu vực và cao độ Z-datum; biên dịch blueprint 4 khung nhìn (hoặc OpenBIM/CAD `.ifc`/`.dxf` nếu có thư viện) và dựng khối 1:1 vào Blender với `bmesh.ops.bisect_plane` khắc Z-datum + UV mét `UVMap_Metric_1m`, kiểm tra không lơ lửng trước khi đi tiếp.
1. **Stage 02:** Tạo ảnh contact sheet tham chiếu 2x2 (16:9, 4 góc: Hero 3/4, Toàn cảnh trên cao, Cận ngưỡng cửa/chi tiết, Sân/nội thất) để khóa tỷ lệ và chuẩn bị vật liệu PBR 5 kênh trên `UVMap_Metric_1m`.
2. **Stage 03:** Điều phối 4 subagent chuyên môn (`Model="inherit"`) viết 4 script Python độc lập (`zone_01..04.py`) rồi chạy tuần tự vào Blender MCP, lưu checkpoint từng bước.
3. **Stage 04:** Chụp ảnh "Before", sau đó chạy vòng lặp tự phê bình trực quan (Adversarial Critic) đối chiếu render Blender với contact sheet cho tới khi đạt >= 8.5/10.
4. **Mandatory Studio Polish:** Bắt buộc áp dụng đủ 5 lớp chống giả CG: `Light_Gobo_Canopy` + noise cho đèn (`Scale=6.0`), Roughness stacking `LINEAR_LIGHT` (`Factor=0.28`) + `Pointiness`/`AmbientOcclusion` edge-wear & crevice dirt, Camera 35mm full-frame DoF (`f/1.8–f/2.8`), Micro-bevel + `ObjectInfo.Random`, và Volumetric Scatter + `AgX` + Compositor Fog Glow.
5. **Stage 05:** Render 6 góc máy Cycles (gồm mặt cắt `Section A-A` non-destructive bằng `bmesh.ops.bisect_plane` phủ hatch ANSI31), xuất `progression_matrix.png` (Before vs. After), `showcase_6cam_sheet.png` và lưu file `.blend` hoàn chỉnh.
```

---

## Template C — Compact Single-Zone Prompt (Dựng nhanh 1 công trình / nội thất, không cần 4 subagent)

Dùng khi bạn muốn dựng nhanh một căn phòng, quán cà phê, sảnh kiến trúc hoặc pavilion trong 1 phiên ngắn:

```text
Build a photorealistic single-zone architectural scene of [a sunlit Kyoto minimalist timber & concrete tea room overlooking a bamboo courtyard] in Blender using the `architectural-environment-production` skill (compact single-orchestrator mode: skip 4-subagent spawning, execute Stages 00–02 directly, run 2 focused visual critique loops against a 2x2 reference contact sheet, apply all 5 Mandatory Studio Polish layers including `Light_Gobo_Canopy`, `LINEAR_LIGHT` 0.28 roughness stacking + `Pointiness`/AO wear, 35mm `f/2.0` DoF, micro-bevels, and `AgX` volumetrics, then render 4 Cycles cameras + Before-vs-After comparison).
```
