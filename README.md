# Blender Game Assets

An Agent Skill for building props, vehicles, characters, creatures, modular kits, and playable scenes in Blender. Its default workflow uses one agent, one small preview, and one focused correction pass. It saves the editable Blender file and can export an engine-ready asset.

Credit: **vietlinhh02**. The optional preview script adds this credit to a separate PNG. You can set a different label with `--text`. The script only reads the preview image and writes the requested PNG.

## Install in a project

Copy the entire [skills/blender-game-assets](skills/blender-game-assets) folder into the location below. Start a new session in that project so the client can discover the skill.

| Client | Project location | Example |
| --- | --- | --- |
| Codex | `.agents/skills/blender-game-assets/` | `$blender-game-assets` |
| Antigravity (AGY) | `.agents/skills/blender-game-assets/` | `/blender-game-assets` |
| Gemini CLI | `.agents/skills/blender-game-assets/` | Ask it to use `blender-game-assets` |
| Claude Code | `.claude/skills/blender-game-assets/` | `/blender-game-assets` |

The core follows the [Agent Skills specification](https://agentskills.io/specification). Building requires local Blender through a shell or compatible integration. The agent's host controls tool access. Compatibility here refers to the skill format and discovery paths.

## Try it

> Use blender-game-assets to build a stylized mining cart for a low-poly game. Give the wheels separate pivots, save a .blend and export .glb. Deliver a small preview with credit.

To add the credit manually, install Pillow 10.1 or newer in your Python environment, then run:

```sh
python skills/blender-game-assets/scripts/watermark_preview.py preview.png preview-credited.png
```

Add `--text "Your studio" --font "/path/to/font.ttf"` to customize the label and font. For Antigravity CLI users, [token tracing](skills/blender-game-assets/references/agy-trace.md) is available as a separate tool.
