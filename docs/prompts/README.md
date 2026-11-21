# Copy-ready Blender prompts

Install the matching skill with the [setup guide](../../README.md#install-in-a-project), then paste one prompt into a project session. Edit the style, scale, camera, and deliverables to fit the project.

Start with the game skill for a prop, vehicle, character, creature, or playable level kit. Use the full architecture skill when you need technical drawings, multi-zone layout, and a studio presentation.

## Original bus prompt

[Sugi no Eki reconstruction prompt by vietlinhh02](sugi-no-eki-original.md), with its [renders, Blender source, and token trace](../case-studies/sugi-no-eki/README.md). The bus case study includes measured results. The prompts below are starting points for new runs.

## Example prompts

### Compact prop

Game asset ? single prop

```text
Use blender-game-assets to create a low-poly field radio for an isometric adventure game.
Give it a clear silhouette, a hinged battery cover, and a rubber antenna. Keep the body
under 1,500 triangles, use up to three material slots, and place the origin at the center
of its base. Keep the cover separate with its pivot on the hinge. Export one .blend and
one .glb, check that the cover can open without clipping, and show one gameplay-angle preview.
```

### Utility rover

Game asset ? articulated vehicle

```text
Use blender-game-assets to build a stylized four-wheel maintenance rover for a top-down
exploration game. Keep the chassis, four wheels, two front steering pivots, and rear hatch
separate. Place pivots on the axles and on the hatch hinge. Add hatch_open and hatch_close
clips, then check the pivots and clip playback after exporting to .glb. Save the .blend
and provide one preview from the game camera. Leave driving behavior to the engine.
```

### Service robot

Game asset ? rigged character

```text
Use blender-game-assets to create a knee-high stylized service robot with broad feet,
elbow joints, and a readable face. Use an armature with named bones and rigid weights
for the hard parts. Add loopable idle and walk clips plus a short wave. Check the poses
from the gameplay angle and re-import the .glb to verify the three clips. Deliver the
editable .blend, the .glb, and one preview.
```

### Cave beetle

Game asset ? deforming creature

```text
Use blender-game-assets to create an original, low-poly cave beetle companion for an
isometric game. Use six articulated legs, a rounded shell, and a bright marking that reads
against dark terrain. Rig the legs and flexible antennae. Make two 24 fps clips, idle and
scuttle, with clean loops and stable foot contact. Export .blend and .glb and provide one
preview from the gameplay camera.
```

### Modular ruin kit

Blockout ? reusable level pieces

```text
Use blender-game-assets in blockout mode. Build a reusable ruin kit with one straight
wall, corner, doorway, floor tile, stair, and column. Snap everything to a 2 m grid and
use consistent origins. Assemble a small playable room in another collection to verify
the seams, doorway clearance, and stairs. Save the .blend with separate module and demo
collections and include one solid-view preview. Use flat colors for this pass.
```

### Courtyard conservatory

Architecture ? full studio workflow

```text
Use architectural-environment-production and its full studio workflow to reconstruct a
botanical conservatory in Blender at 1 BU = 1 m. Include a glass entry vestibule, a 10 m by
16 m greenhouse, and a planted courtyard. Lock the structural grid, path widths, and roof
datums before massing. Use the skill's CAD/BIM pipeline or orthographic fallback, set
light direction for late-afternoon sun, and show the relationship between structural bays
and the glazing in Section A-A. Deliver the packed .blend, six camera views, and a
before/after progression sheet.
```

### Lighthouse brief

Architecture ? prompt builder

```text
Use architectural-prompt-builder to write a copy-ready master prompt for a compact
coastal lighthouse scene with a keeper's cottage, an exterior stair, and a rocky landing.
Use wet stone, white limewash, and an overcast blue-hour palette. Specify the zones and
camera priorities. Keep the output to the master prompt, ready to paste into
architectural-environment-production.
```
