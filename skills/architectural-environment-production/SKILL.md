---
name: architectural-environment-production
description: Build Blender architecture and environments. Use the game-asset workflow for game levels and stylized scenes, and the studio workflow for detailed architectural reconstructions, photoreal presentations, or explicit OpenBIM/CAD requirements. Also routes other Blender game assets when invoked by name.
license: Apache-2.0
---

# Architectural Environment Production

Choose the workflow from the user's goal and deliverables before inspecting Blender or spawning agents.

- For game or stylized work, blockouts, single props, vehicles, characters, creatures, and modular kits, follow [Blender Game Assets](../blender-game-assets/SKILL.md). Use the brief's art direction and platform requirements.
- For detailed architectural reconstruction, or when the user requests OpenBIM/CAD, a photoreal architectural showcase, or the existing full studio workflow, follow [Architecture Studio](architecture-studio.md). Architecture-focused prompts from `architectural-prompt-builder` use this workflow.
- For a vague request to build a named environment or building, use the brief step in Blender Game Assets to define the footprint, key spaces, scale, art direction, and intended view. Proceed with a compact scene when the request leaves the deliverables open. Apply any requested realism or presentation shots at the appropriate scale.
- For a studio run, infer a workable site layout, scale, and lighting from the brief and supplied references before the full workflow begins. Label assumed dimensions. Ask for a plan or dimensions only when fidelity to a real site depends on them.
- When the user asks only for a prompt, use [Architectural Prompt Builder](../architectural-prompt-builder/SKILL.md) for a studio prompt or Blender Game Assets for a game asset prompt.
