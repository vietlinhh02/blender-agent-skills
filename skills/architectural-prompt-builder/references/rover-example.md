# Worked example: maintenance rover

The starting request specifies four working wheels, two front steering pivots, a rear hatch, and GLB delivery. The expanded prompt adds a recognizable purpose, a clear camera-angle test, and evidence of actual movement after export. The dimensions and palette below are editable design assumptions.

```text
Use blender-game-assets to build an original, stylized four-wheel maintenance rover for a top-down exploration game. Treat the dimensions and palette below as design assumptions unless the project provides its own conventions.

Art direction
- Build a compact repair rover with a blunt wedge nose, four exposed dark tires, a recessed rear tool bay, and an asymmetric service module on one side.
- Give the body a warm ochre shell, charcoal running gear, and a muted teal panel. Keep the nose, wheel gaps, and tool bay visually distinct when the orthographic game preview is viewed at 320 px. Use a slightly angled top-down camera so the bay and wheel silhouette are visible.
- Start with a footprint near 2.4 m long by 1.6 m wide, including the tires. Use one editable root at the ground center, metric units, and a documented forward axis.

Parts and motion
- Keep Chassis, Wheel_FL, Wheel_FR, Wheel_RL, Wheel_RR, Steering_L, Steering_R, and Rear_Hatch distinct. Parent each front wheel under its steering pivot; wheel rotation is local to the axle. Place the rear hatch origin on the physical upper hinge of the tool bay.
- Add hatch_open and hatch_close with closed and open poses that match at the clip transitions. Aim for about 65 degrees of opening over about one second. Keep the tool bay visible with the hatch open. Leave driving behavior to the engine.

Checks and delivery
- Inspect the preview at 320 px. Check that the front is distinguishable from the rear and that the wheels, service module, and open bay read as separate features.
- In Blender, test both steering pivots to about 25 degrees each way. Inspect the hatch at 0%, 50%, and 100% of both clips for unintended contact with the cabin or cargo.
- Save maintenance_rover.blend, export maintenance_rover.glb, and provide one preview from the game camera with the hatch open. Re-import the GLB into a clean scene to confirm the root, separate moving parts, both named clips, and matching start and end poses. Report triangle count and any check you could not perform.
```
