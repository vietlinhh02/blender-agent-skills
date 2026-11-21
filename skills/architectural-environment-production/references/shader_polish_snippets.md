# Blender 4.x / 5.x Studio Polish & Section Cutaway Snippets

Portable `bpy` / `bmesh` helpers compatible with Blender 4.2+ and 5.x. All node lookups use `node.type` (never localized node names), and enum assignments use safe capability checks.

---

## 1. Metric UV Projection (`UVMap_Metric_1m`) & Horizontal Z-Datum Imprinting

```python
import bpy
import bmesh
from mathutils import Vector

def apply_metric_box_uv_and_z_datums(obj, z_datums=None, uv_name="UVMap_Metric_1m"):
    """
    1) Imprints clean horizontal Z-datum edge loops via bmesh.ops.bisect_plane.
    2) Generates 1 BU = 1 UV unit triplanar/box UV coordinates on `UVMap_Metric_1m`.
    """
    if obj.type != "MESH" or not obj.data:
        return
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)

    if z_datums:
        inv_mw = obj.matrix_world.inverted()
        local_no = (obj.matrix_world.to_3x3().transposed() @ Vector((0.0, 0.0, 1.0))).normalized()
        for z_val in z_datums:
            local_co = inv_mw @ Vector((0.0, 0.0, float(z_val)))
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            if geom:
                bmesh.ops.bisect_plane(
                    bm,
                    geom=geom,
                    dist=1e-4,
                    plane_co=local_co,
                    plane_no=local_no,
                    use_snap_center=False,
                    clear_outer=False,
                    clear_inner=False,
                )

    uv_layer = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)
    mw = obj.matrix_world
    n_rot = mw.to_3x3()
    for face in bm.faces:
        n = (n_rot @ face.normal)
        ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
        for loop in face.loops:
            wp = mw @ loop.vert.co
            if az >= ax and az >= ay:
                loop[uv_layer].uv = (wp.x, wp.y)
            elif ax >= ay and ax >= az:
                loop[uv_layer].uv = (wp.y, wp.z)
            else:
                loop[uv_layer].uv = (wp.x, wp.z)

    bm.to_mesh(me)
    bm.free()
    me.update()
    if uv_name in me.uv_layers:
        me.uv_layers[uv_name].active = True
        me.uv_layers[uv_name].active_render = True
```

---

## 2. Gobo Canopy (`Light_Gobo_Canopy`) & Procedural Light Emission Noise

```python
import bpy

def create_light_gobo_canopy(
    name="Light_Gobo_Canopy",
    location=(0.0, 0.0, 14.0),
    size=24.0,
    rotation_euler=(0.35, 0.25, 0.2),
    scale=1.8,
    collection_name="05_Lighting_Atmosphere",
):
    """Creates an invisible-to-camera overhead foliage/slat gobo plane casting dappled shadows."""
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    half = size * 0.5
    mesh.from_pydata(
        [(-half, -half, 0.0), (half, -half, 0.0), (half, half, 0.0), (-half, half, 0.0)],
        [],
        [(0, 1, 2, 3)],
    )
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation_euler

    col = bpy.data.collections.get(collection_name) or bpy.context.scene.collection
    col.objects.link(obj)

    # Invisible to camera & reflections; casts real dappled shadows only
    obj.visible_camera = False
    obj.visible_diffuse = False
    obj.visible_glossy = False
    obj.visible_transmission = False
    obj.visible_volume_scatter = False
    obj.visible_shadow = True

    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix_sh = nt.nodes.new("ShaderNodeMixShader")
    transp = nt.nodes.new("ShaderNodeBsdfTransparent")
    diffuse = nt.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse.inputs["Color"].default_value = (0.02, 0.02, 0.02, 1.0)

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)  # open light
    ramp.color_ramp.elements[1].position = 0.56
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)  # occluded shadow

    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = scale
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale * 2.2
    noise.inputs["Detail"].default_value = 4.0

    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    mix_vec = nt.nodes.new("ShaderNodeMix")
    mix_vec.data_type = "VECTOR"
    mix_vec.inputs[0].default_value = 0.35

    nt.links.new(tex_coord.outputs["Object"], mix_vec.inputs[4])
    nt.links.new(noise.outputs["Color"], mix_vec.inputs[5])
    nt.links.new(tex_coord.outputs["Object"], noise.inputs["Vector"])
    nt.links.new(mix_vec.outputs[1], vor.inputs["Vector"])
    nt.links.new(vor.outputs["Distance"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix_sh.inputs["Fac"])
    nt.links.new(transp.outputs["BSDF"], mix_sh.inputs[1])
    nt.links.new(diffuse.outputs["BSDF"], mix_sh.inputs[2])
    nt.links.new(mix_sh.outputs["Shader"], out.inputs["Surface"])

    obj.data.materials.append(mat)
    return obj


def add_procedural_emission_noise_to_light(light_obj, noise_scale=6.0, strength_min=0.72, strength_max=1.18):
    """Enables light.use_nodes = True on Area/Spot lights and adds ShaderNodeTexNoise (Scale=6.0) variation."""
    if not light_obj or light_obj.type != "LIGHT":
        return
    light = light_obj.data
    if light.type not in {"AREA", "SPOT", "POINT"}:
        return

    light.use_nodes = True
    nt = light.node_tree
    nodes = nt.nodes
    links = nt.links

    out = next((n for n in nodes if n.type == "OUTPUT_LIGHT"), None) or nodes.new("ShaderNodeOutputLight")
    emis = next((n for n in nodes if n.type == "EMISSION"), None) or nodes.new("ShaderNodeEmission")
    links.new(emis.outputs["Emission"], out.inputs["Surface"])

    base_strength = emis.inputs["Strength"].default_value
    tex_coord = nodes.new("ShaderNodeTexCoord")
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = float(noise_scale)
    noise.inputs["Detail"].default_value = 3.0

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = (strength_min, strength_min, strength_min, 1.0)
    ramp.color_ramp.elements[1].position = 0.78
    ramp.color_ramp.elements[1].color = (strength_max, strength_max, strength_max, 1.0)

    mult = nodes.new("ShaderNodeMath")
    mult.operation = "MULTIPLY"
    mult.inputs[1].default_value = base_strength

    links.new(tex_coord.outputs["Normal"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mult.inputs[0])
    links.new(mult.outputs["Value"], emis.inputs["Strength"])
```

---

## 3. Roughness Stacking (`LINEAR_LIGHT`, `Factor = 0.28`), Pointiness/AO Wear & Per-Instance Variation

> **Blender 4.x/5.x `ShaderNodeMix` socket cheat-sheet:**
> - When `mix.data_type == 'FLOAT'`: inputs `[0]` Factor, `[2]` A, `[3]` B -> output `[0]` Result.
> - When `mix.data_type == 'RGBA'`: inputs `[0]` Factor, `[6]` A, `[7]` B -> output `[2]` Result.

```python
import bpy

def add_studio_imperfection_stack(
    mat,
    grunge_scale=18.0,
    roughness_factor=0.28,
    edge_tint=(0.82, 0.78, 0.72, 1.0),
    crevice_tint=(0.14, 0.12, 0.11, 1.0),
    ao_distance=0.45,
):
    """
    Upgrades any Principled BSDF material with:
      1) Multi-layer Roughness stacking (ShaderNodeMix LINEAR_LIGHT, Factor=0.28)
      2) Pointiness edge-wear + Ambient Occlusion crevice dirt into Base Color & Roughness
      3) Per-instance Object Info Random macro-variation
    """
    if not mat or not mat.use_nodes:
        return
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
    if not bsdf:
        return

    tex_coord = nodes.new("ShaderNodeTexCoord")
    geom = nodes.new("ShaderNodeNewGeometry")
    obj_info = nodes.new("ShaderNodeObjectInfo")

    # --- A. High-Frequency Roughness Stacking (LINEAR_LIGHT, Factor=0.28) ---
    base_rough_sock = bsdf.inputs["Roughness"]
    existing_rough_link = base_rough_sock.links[0].from_socket if base_rough_sock.is_linked else None
    base_rough_val = base_rough_sock.default_value

    grunge = nodes.new("ShaderNodeTexNoise")
    grunge.inputs["Scale"].default_value = grunge_scale
    grunge.inputs["Detail"].default_value = 8.0
    grunge.inputs["Roughness"].default_value = 0.68

    grunge_ramp = nodes.new("ShaderNodeValToRGB")
    grunge_ramp.color_ramp.elements[0].position = 0.30
    grunge_ramp.color_ramp.elements[0].color = (0.28, 0.28, 0.28, 1.0)
    grunge_ramp.color_ramp.elements[1].position = 0.78
    grunge_ramp.color_ramp.elements[1].color = (0.76, 0.76, 0.76, 1.0)

    mix_rough = nodes.new("ShaderNodeMix")
    mix_rough.data_type = "FLOAT"
    mix_rough.blend_type = "LINEAR_LIGHT"
    mix_rough.clamp_result = True
    mix_rough.inputs[0].default_value = roughness_factor
    if existing_rough_link:
        links.new(existing_rough_link, mix_rough.inputs[2])
    else:
        mix_rough.inputs[2].default_value = base_rough_val

    links.new(tex_coord.outputs["Object"], grunge.inputs["Vector"])
    links.new(grunge.outputs["Fac"], grunge_ramp.inputs["Fac"])
    links.new(grunge_ramp.outputs["Color"], mix_rough.inputs[3])

    # --- B. Pointiness Edge-Wear + Ambient Occlusion Crevice Dirt ---
    point_ramp = nodes.new("ShaderNodeValToRGB")
    point_ramp.color_ramp.elements[0].position = 0.52
    point_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    point_ramp.color_ramp.elements[1].position = 0.64
    point_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(geom.outputs["Pointiness"], point_ramp.inputs["Fac"])

    ao = nodes.new("ShaderNodeAmbientOcclusion")
    ao.samples = 8
    ao.inputs["Distance"].default_value = ao_distance
    ao_ramp = nodes.new("ShaderNodeValToRGB")
    ao_ramp.color_ramp.elements[0].position = 0.15
    ao_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)  # crevice mask = 1
    ao_ramp.color_ramp.elements[1].position = 0.72
    ao_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    links.new(ao.outputs["AO"], ao_ramp.inputs["Fac"])

    # Combine Base Color -> Per-instance variation -> Crevice Dirt -> Edge Wear
    base_col_sock = bsdf.inputs["Base Color"]
    existing_col_link = base_col_sock.links[0].from_socket if base_col_sock.is_linked else None
    base_col_val = tuple(base_col_sock.default_value)

    # Per-instance subtle brightness variation
    rand_ramp = nodes.new("ShaderNodeValToRGB")
    rand_ramp.color_ramp.elements[0].position = 0.0
    rand_ramp.color_ramp.elements[0].color = (0.88, 0.88, 0.88, 1.0)
    rand_ramp.color_ramp.elements[1].position = 1.0
    rand_ramp.color_ramp.elements[1].color = (1.12, 1.12, 1.12, 1.0)
    links.new(obj_info.outputs["Random"], rand_ramp.inputs["Fac"])

    inst_mult = nodes.new("ShaderNodeMix")
    inst_mult.data_type = "RGBA"
    inst_mult.blend_type = "MULTIPLY"
    inst_mult.inputs[0].default_value = 0.65
    if existing_col_link:
        links.new(existing_col_link, inst_mult.inputs[6])
    else:
        inst_mult.inputs[6].default_value = base_col_val
    links.new(rand_ramp.outputs["Color"], inst_mult.inputs[7])

    mix_dirt = nodes.new("ShaderNodeMix")
    mix_dirt.data_type = "RGBA"
    mix_dirt.blend_type = "MIX"
    mix_dirt.inputs[7].default_value = crevice_tint
    dirt_fac = nodes.new("ShaderNodeMath")
    dirt_fac.operation = "MULTIPLY"
    dirt_fac.inputs[1].default_value = 0.55
    links.new(ao_ramp.outputs["Color"], dirt_fac.inputs[0])
    links.new(dirt_fac.outputs["Value"], mix_dirt.inputs[0])
    links.new(inst_mult.outputs[2], mix_dirt.inputs[6])

    mix_edge = nodes.new("ShaderNodeMix")
    mix_edge.data_type = "RGBA"
    mix_edge.blend_type = "MIX"
    mix_edge.inputs[7].default_value = edge_tint
    edge_fac = nodes.new("ShaderNodeMath")
    edge_fac.operation = "MULTIPLY"
    edge_fac.inputs[1].default_value = 0.35
    links.new(point_ramp.outputs["Color"], edge_fac.inputs[0])
    links.new(edge_fac.outputs["Value"], mix_edge.inputs[0])
    links.new(mix_dirt.outputs[2], mix_edge.inputs[6])
    links.new(mix_edge.outputs[2], base_col_sock)

    # Also raise roughness slightly in dirt crevices and subtly polish sharp worn edges
    crevice_rough = nodes.new("ShaderNodeMix")
    crevice_rough.data_type = "FLOAT"
    crevice_rough.blend_type = "MIX"
    crevice_rough.clamp_result = True
    crevice_rough.inputs[3].default_value = 0.92
    links.new(dirt_fac.outputs["Value"], crevice_rough.inputs[0])
    links.new(mix_rough.outputs[0], crevice_rough.inputs[2])
    links.new(crevice_rough.outputs[0], base_rough_sock)
```

---

## 4. Physical 35mm Camera Rig + Depth of Field Empty

```python
import bpy

def create_physical_camera(
    name,
    location,
    target_location,
    lens_mm=35.0,
    fstop=2.2,
    shift_y=0.0,
    collection_name="06_Cameras",
):
    """Creates a Full-Frame 35mm physical camera aimed at a tracked Focus Target Empty."""
    col = bpy.data.collections.get(collection_name) or bpy.context.scene.collection

    target = bpy.data.objects.new(f"{name}_Target", None)
    target.empty_display_type = "PLAIN_AXES"
    target.empty_display_size = 0.5
    target.location = target_location
    col.objects.link(target)

    cam_data = bpy.data.cameras.new(name)
    cam_data.sensor_fit = "HORIZONTAL"
    cam_data.sensor_width = 36.0
    cam_data.lens = float(lens_mm)
    cam_data.shift_y = float(shift_y)
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = target
    cam_data.dof.aperture_fstop = float(fstop)
    cam_data.clip_start = 0.1
    cam_data.clip_end = 500.0

    cam_obj = bpy.data.objects.new(name, cam_data)
    cam_obj.location = location
    col.objects.link(cam_obj)

    track = cam_obj.constraints.new(type="TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    return cam_obj, target
```

---

## 5. Non-Destructive World-Space BMesh Section A-A Cutaway + ANSI31 Hatch Shader

```python
import bpy
import bmesh
import math
from mathutils import Vector

def get_or_create_ansi31_section_material(name="Mat_Section_Cut_ANSI31"):
    """Procedural 45-degree ANSI31 diagonal hatch shader for Section A-A cut caps."""
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.85

    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Rotation"].default_value = (0.0, math.radians(45.0), math.radians(45.0))

    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"
    wave.bands_direction = "X"
    wave.wave_profile = "SAW"
    wave.inputs["Scale"].default_value = 18.0
    wave.inputs["Distortion"].default_value = 0.0

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.14
    ramp.color_ramp.elements[0].color = (0.08, 0.08, 0.09, 1.0)
    ramp.color_ramp.elements[1].position = 0.18
    ramp.color_ramp.elements[1].color = (0.86, 0.84, 0.80, 1.0)

    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def build_section_aa_cutaway(
    source_collection_names=("01_Primary_Structure", "02_Secondary_Architecture", "03_Threshold_Details"),
    plane_co=(0.0, 0.0, 0.0),
    plane_no=(0.0, -1.0, 0.0),
    cut_collection_name="99_Cutaway_Section",
):
    """
    Duplicates meshes into `cut_collection_name` and slices them in world space
    using bmesh.ops.bisect_plane(clear_outer=True), capping cut faces with ANSI31 hatch.
    """
    cut_col = bpy.data.collections.get(cut_collection_name)
    if cut_col:
        for obj in list(cut_col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        cut_col = bpy.data.collections.new(cut_collection_name)
        bpy.context.scene.collection.children.link(cut_col)

    hatch_mat = get_or_create_ansi31_section_material()
    p_co = Vector(plane_co)
    p_no = Vector(plane_no).normalized()

    for cname in source_collection_names:
        src_col = bpy.data.collections.get(cname)
        if not src_col:
            continue
        for src in src_col.all_objects:
            if src.type != "MESH" or not src.data:
                continue
            dup = src.copy()
            dup.data = src.data.copy()
            dup.name = f"{src.name}_SecAA"
            cut_col.objects.link(dup)

            if hatch_mat.name not in [m.name for m in dup.data.materials if m]:
                dup.data.materials.append(hatch_mat)
            cap_idx = list(dup.data.materials).index(hatch_mat)

            inv_mw = dup.matrix_world.inverted()
            local_co = inv_mw @ p_co
            local_no = (dup.matrix_world.to_3x3().transposed() @ p_no).normalized()

            bm = bmesh.new()
            bm.from_mesh(dup.data)
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            if geom:
                res = bmesh.ops.bisect_plane(
                    bm,
                    geom=geom,
                    dist=1e-4,
                    plane_co=local_co,
                    plane_no=local_no,
                    use_snap_center=False,
                    clear_outer=True,
                    clear_inner=False,
                )
                cut_edges = [g for g in res.get("geom_cut", []) if isinstance(g, bmesh.types.BMEdge)]
                if cut_edges:
                    filled = bmesh.ops.contextual_create(bm, geom=cut_edges)
                    for f in filled.get("faces", []):
                        f.material_index = cap_idx
            bm.to_mesh(dup.data)
            bm.free()
            dup.data.update()
    return cut_col
```

---

## 6. Bounded Volumetric Atmosphere, AgX & Blender 4.x/5.x Compositor

```python
import bpy

def setup_atmosphere_agx_and_compositor(
    volume_center=(0.0, 0.0, 8.0),
    volume_size=(40.0, 40.0, 22.0),
    density=0.0025,
    anisotropy=0.65,
    collection_name="05_Lighting_Atmosphere",
):
    scene = bpy.context.scene

    # 1) AgX Color Management (guarded against version differences)
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        pass
    try:
        valid_looks = [i.identifier for i in scene.view_settings.bl_rna.properties["look"].enum_items]
        for candidate in ("AgX - Medium High Contrast", "Medium High Contrast"):
            if candidate in valid_looks:
                scene.view_settings.look = candidate
                break
    except Exception:
        pass

    # 2) Bounded Volumetric Scatter Domain
    vol_name = "Atmosphere_Volume_Domain"
    if not bpy.data.objects.get(vol_name):
        mesh = bpy.data.meshes.new(f"{vol_name}_Mesh")
        hx, hy, hz = volume_size[0] * 0.5, volume_size[1] * 0.5, volume_size[2] * 0.5
        verts = [
            (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
            (-hx, -hy, hz),  (hx, -hy, hz),  (hx, hy, hz),  (-hx, hy, hz),
        ]
        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7),
            (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
        ]
        mesh.from_pydata(verts, [], faces)
        vol_obj = bpy.data.objects.new(vol_name, mesh)
        vol_obj.location = volume_center
        vol_obj.display_type = "WIRE"
        col = bpy.data.collections.get(collection_name) or scene.collection
        col.objects.link(vol_obj)

        mat = bpy.data.materials.new(f"{vol_name}_Mat")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        vol = nt.nodes.new("ShaderNodeVolumeScatter")
        vol.inputs["Color"].default_value = (1.0, 0.96, 0.90, 1.0)
        vol.inputs["Density"].default_value = density
        vol.inputs["Anisotropy"].default_value = anisotropy
        nt.links.new(vol.outputs["Volume"], out.inputs["Volume"])
        vol_obj.data.materials.append(mat)

    # 3) Version-Safe Compositor (Blender 5.x compositing_node_group vs 4.x node_tree)
    nt = None
    if hasattr(scene, "compositing_node_group"):
        if not scene.compositing_node_group:
            scene.compositing_node_group = bpy.data.node_groups.new("ArchPolishCompositor", "CompositorNodeTree")
        nt = scene.compositing_node_group
    elif hasattr(scene, "node_tree"):
        scene.use_nodes = True
        nt = scene.node_tree

    if not nt:
        return

    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers")
    comp = nt.nodes.new("CompositorNodeComposite")
    glare = nt.nodes.new("CompositorNodeGlare")
    lens = nt.nodes.new("CompositorNodeLensdist")

    if hasattr(glare, "glare_type"):
        glare.glare_type = "FOG_GLOW"
        glare.quality = "HIGH"
        glare.threshold = 1.2
        glare.mix = -0.35
    if hasattr(lens, "inputs") and "Dispersion" in lens.inputs:
        lens.inputs["Dispersion"].default_value = 0.004

    # Link safely across Blender 4.x/5.x output socket names
    rl_out = rl.outputs[0]
    gl_in = glare.inputs[0]
    gl_out = glare.outputs[0]
    ln_in = lens.inputs[0]
    ln_out = lens.outputs[0]
    cp_in = comp.inputs[0]

    nt.links.new(rl_out, gl_in)
    nt.links.new(gl_out, ln_in)
    nt.links.new(ln_out, cp_in)
```
