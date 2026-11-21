---
name: architectural-prompt-builder
description: >-
  Write or expand technical Blender prompts from vague or detailed ideas for game
  assets, vehicles, props, characters, creatures, modular levels, environments, and
  architectural scenes. Use for a build brief, a reusable copy-ready prompt,
  stronger art direction, or measurable modeling and export acceptance checks.
license: Apache-2.0
---

# Blender Technical Prompt Builder

Turn a Blender idea into instructions that change the resulting asset. Keep the original requirements and supported capabilities. Use the user's language unless they request another.

## Choose the result

- **Prompt only:** Produce one copy-ready prompt that names the Blender workflow and its acceptance checks.
- **Brief only or review first:** Present the brief and stop before modeling.
- **Build now:** Produce a concise brief as part of the same build session, then continue into the matching Blender workflow. An already specific brief may be reused. Fill only the design or verification gaps that matter.
- Route props, vehicles, characters, creatures, game scenes, and simple generic buildings to [Blender Game Assets](../blender-game-assets/SKILL.md). For measured reconstruction, CAD/BIM, or a studio showcase, use the [studio prompt reference](references/studio-prompts.md) to draft a prompt and the [architecture workflow](../architectural-environment-production/architecture-studio.md) to build. Load only the material needed for the requested result.

## Write a brief that changes the result

1. **Goal and art direction:** Specify the main view and how the object should read in that view. For an open brief, choose a silhouette, a small material palette, and two or three subject-specific details that show the object's purpose. Tie each detail to the reference, use, or camera. For an edit, name the parts to change and preserve the features that already meet the brief.
2. **Build contract:** Define units or approximate bounds, orientation, parts or zones, and any relevant limits from the target project. Label invented numbers as starting assumptions. Keep the design editable and specific to the format being delivered.
3. **Acceptance checks:** Write two or three observable visual checks and the technical checks the build requires. Name the object, pose, angle, or exported property to inspect. A file existing, a clip appearing by name, or a generic request to "make it better" is insufficient evidence for a quality claim.
4. **Delivery:** Name the editable file, requested export, preview camera, and how the build should be verified. Ask one focused question only when missing information blocks a faithful build or changes the result materially. If a named subject leaves reversible details open, state the assumptions and continue.

| Subject | Specify and verify where applicable |
| --- | --- |
| Vehicle or machine | Separate driven parts and steering pivots. Define local axes, hierarchy, motion endpoints, and the clearance test through the movement. For GLB, re-import and check actual clip targets and poses. |
| Character or creature | Readable head/body proportions at game distance, deformation zones, bones, and clip poses. Check silhouettes and joint deformation in a named pose, and foot contact for locomotion. |
| Prop or equipment | Recognizable use from the intended view, size, placement origin, and any moving pieces. Check floor or hand contact and whether the intended details remain legible at game distance. |
| Modular kit or game level | Grid, origins, seams, and traversal widths. Assemble representative modules, verify fit and clearance, and use one gameplay camera. |
| Environment or architecture | Footprint, key spaces, realistic scale if needed, material family, and lighting/view intent. For a studio brief, route by requested deliverables and use the architecture reference. |

For vague or short requests, a small brief or one usable prompt is enough. Generate a technical plan with filenames, named moving parts, clip poses, or measurements only where useful. Deliver checks in the build workflow and report what was actually verified. Default to one agent and one preview for game assets; preserve an explicit studio scope.

Use the [worked rover example](references/rover-example.md) to see how a functional vehicle request becomes an art and acceptance brief. Read it only if the task uses a comparable vehicle or asks for an example.
