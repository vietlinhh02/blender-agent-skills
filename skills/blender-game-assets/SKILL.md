---
name: blender-game-assets
description: Build, edit, or export game assets in Blender, including props, vehicles, characters, creatures, modular kits, and playable scenes. Use for low-poly, stylized, or realistic game art, quick blockouts, and assets that need pivots, rigs, animation, or engine export.
compatibility: Requires access to local Blender through a shell or a Blender integration to build assets. The optional preview watermark script uses Python 3 and Pillow.
metadata:
  credit: vietlinhh02
  version: "0.1.0"
license: Apache-2.0
---

# Blender Game Assets

Choose one asset, reusable kit, or scene from the brief. Use the project's scale, camera distance, and art direction. Default to a stylized game asset when style is open. Reuse supplied references.

- **Blockout:** Build the silhouette, gameplay scale, and layout with simple meshes and a short color palette. Save the editable `.blend`.
- **Game asset (default):** Build and verify the requested asset, save the editable `.blend`, and export the engine format. Use `.glb` when the project has no format preference.
- **Showcase:** Add cinematic lighting, baked textures, turntables, multiple cameras, or animation renders to the extent requested. Match the scope of the requested presentation.

| Asset | Build around |
| --- | --- |
| Prop or foliage | Gameplay silhouette, purposeful pivot, simple material slots, and linked geometry for repeated parts. |
| Vehicle or machine | Separate required moving parts and put their pivots on axles, hinges, or sliders. Add articulation or clips when requested. |
| Character or creature | Readable silhouette and pose, topology around deforming joints, and armature, skin weights, or named clips as needed. Validate from relevant viewing angles and check playback when rigged. |
| Modular kit or level | Consistent grid, snap points, reusable modules, clear gameplay routes, and instances for repeated geometry. |

Keep mesh density, texture size, collision shapes, and LODs appropriate for the target platform and view. Use the project's budgets when given. Prefer simple material colors or a shared atlas when appropriate. Bake Blender-only shader effects when they need to survive export.

Use a connected Blender tool if it provides the required operations. With shell access, run a local script with Blender in background mode, for example `blender --background --factory-startup --python build.py` for a new scene. Load the specified `.blend` before the script for edits. If Blender is unavailable, provide a script or reproducible steps and say what remains unverified.

1. Inspect the relevant Blender selection or scene. Use a dedicated collection or new file and preserve unrelated scene content. Default to one agent. Batch related work into a local Blender Python script or a few Blender MCP calls and print targeted metrics.
2. Build geometry, then add the requested materials, articulation, collision, or clips. Check one small preview from the gameplay angle and verify silhouette, scale, pivots, and any requested motion. Default to one focused correction pass and use further checks to resolve concrete defects.
3. Export the intended objects. Check orientation, materials, and requested clips by importing into the target engine if available, or by clean Blender re-import. Report the files and the import check you ran.

Skip BIM/CAD, generated contact sheets, mandatory PBR stacks, independent critics, and multi-camera Cycles renders for ordinary game work. Read targeted script sections, keep command output concise, and keep full logs and render sequences on disk. For a long follow-up, checkpoint the `.blend` with a brief handoff so that a fresh session can resume the next phase.

When delivering a preview image, add the credit **vietlinhh02** via [watermark_preview.py](scripts/watermark_preview.py) unless the user asks for a clean preview or gives their own credit text. Save a separate PNG. Keep the original image, Blender scene, export, and textures free from the preview overlay. If Pillow is unavailable, use a local image compositing tool if present, or deliver the original preview and report the missing credit.

For optional Antigravity CLI token tracing, see [AGY trace](references/agy-trace.md).
