# Architectural studio prompts

Use this reference with architectural-environment-production for requested CAD/BIM, measured reconstruction, or a photoreal studio showcase. Keep the chosen compact or full scope and specify only the project-specific differences.

## Workflow

1. **Gather or Infer Inputs:**
   - Extract from the user's request:
     - **Subject & Multi-Zone Program** (e.g., temple complex, brutalist museum, Mediterranean villa, Parisian café street, Gothic cathedral).
     - **Architectural Style, Era & Primary Materials** (timber, cast concrete, limestone, brick, terracotta, copper, glass).
     - **Time of Day, Lighting & Gobo Source** (golden hour through cedar canopy, overcast Nordic skylight, noon courtyard slats, dusk lantern glow).
     - **Scope Mode:** Use `compact` for a small or loosely defined project. Reserve `full` for requested studio deliverables, an explicit four-agent run, or a complex program that genuinely needs separate workstreams.
   - With a short but recognizable idea, infer a compact program, plausible metric dimensions, and sensible Z-datums. State the assumptions inside the prompt. Ask one focused question if the subject is missing or accuracy to a real site depends on a source the user has not provided.

2. **Read Canonical Prompt Templates:**
   - Read [conversation_prompts.md](../../architectural-environment-production/resources/conversation_prompts.md) so the generated prompt mirrors the exact stage names, file paths, and Mandatory Studio Polish directives expected by `architectural-environment-production`.

3. **Design Project-Specific Specs Inside the Prompt:**
   Tailor these concrete elements to the requested architecture instead of leaving generic placeholders:
   - **Slug & Workspace:** `./arch_build_<slug>/`
   - **Footprint and Z-datum targets:** Define dimensions and levels for the named spaces. Keep compact prompts to the main space and its necessary surroundings. Name structural zones for larger programs.
   - **Tailored 2×2 Reference Contact Sheet Angles (Stage 02):** Specify exact framing for TL (Hero 3/4), TR (Aerial Site), BL (Eye-level Threshold/Detail), BR (Atmospheric Courtyard/Interior).
   - **Tailored 4-Specialist Assignments (Stage 03, if `full` mode):** Map each of the 4 specialists to concrete structures, terrain features, cultural props/foliage, and lighting/gobo elements for this exact project.
   - **Tailored 5-Channel PBR Palette & Gobo Type:** Name authentic materials and specify whether the Stage 04/Polish gobo should be organic foliage (`Voronoi`/`Noise` canopy) or architectural slats/pergola/window mullions.
   - **Section A-A Cut Plane:** Specify which axis/landmark the world-space `bmesh.ops.bisect_plane` Section A-A slices through to reveal the richest interior structure.

4. **Deliver Copy-Paste Output:**
   - Output the final prompt inside a **single clean fenced code block** (`text`) with zero leftover `[placeholder]` brackets, written in English by default for highest Blender/image-generation accuracy (or in Vietnamese if the user explicitly asks for a Vietnamese prompt).
   - Directly below the code block, include a brief 2-bullet usage tip:
     - Paste into a fresh conversation with Blender MCP running.
     - Suggest typing `/goal` (or `/teamwork` for multi-subagent runs) if they want autonomous multi-pass refinement to run uninterrupted.
