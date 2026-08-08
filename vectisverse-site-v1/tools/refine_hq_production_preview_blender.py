# Riptide HQ — downstream production-treatment refinement
# Runs only after the locked production-treatment scene has been built.
# It does not alter the validated shell dimensions, zone topology, camera positions,
# Q2/Q3/Q4 relationships, or protected branding assets.
import bpy, math, runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tools' / 'render_hq_production_preview_blender.py'
OUT = ROOT / 'assets' / 'riptide' / 'hq-tour' / 'production-preview-refined'
OUT.mkdir(parents=True, exist_ok=True)

# Build the approved-treatment scene first. The base renderer may emit its diagnostic
# preview; this refinement then operates on the same in-memory deterministic scene.
runpy.run_path(str(BASE), run_name='__main__')
scene = bpy.context.scene

BLACK = bpy.data.materials.get('blackened steel')
SKYGLASS = bpy.data.materials.get('skylight glass')
if BLACK is None or SKYGLASS is None:
    raise RuntimeError('Required approved-treatment materials are missing')

W, EAVES, RIDGE = 10.5, 2.75, 6.2
rise = RIDGE - EAVES
ang = math.atan2(rise, W/2)

# Remove the surface-panel treatment. The skylights become genuine apertures in the
# existing roof planes; this is a treatment correction, not a topology redesign.
for obj in list(bpy.data.objects):
    if obj.name.startswith('SKYLIGHT_FRAME_') or obj.name.startswith('SKYLIGHT_GLASS_'):
        bpy.data.objects.remove(obj, do_unlink=True)

def cube(name, loc, dims, mat=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        o.data.materials.append(mat)
    return o

def cut(target, cutter):
    mod = target.modifiers.new('skylight aperture', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = target
    target.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    target.select_set(False)

for side in (-1, 1):
    roof = bpy.data.objects.get('ROOF_LOWER' if side < 0 else 'ROOF_UPPER')
    if roof is None:
        raise RuntimeError(f'Validated roof plane missing for side {side}')
    for i, y in enumerate((4.5, 9.5, 14.5, 19.5)):
        x = side * 2.55
        z = EAVES + rise * (1 - abs(x)/(W/2))
        rot = (0, side*ang, 0)
        # Cutter passes fully through the 0.16 m roof plane.
        cutter = cube(f'_SKYLIGHT_CUTTER_{side}_{i}', (x, y, z), (1.22, 1.52, .50), rot=rot)
        cut(roof, cutter)
        bpy.data.objects.remove(cutter, do_unlink=True)
        # Recessed black surround and glass pane, slightly below the roof exterior face.
        frame = cube(f'SKYLIGHT_RECESSED_FRAME_{side}_{i}', (x, y, z-.035), (1.46, 1.76, .075), BLACK, rot)
        glass = cube(f'SKYLIGHT_RECESSED_GLASS_{side}_{i}', (x, y, z-.015), (1.16, 1.46, .028), SKYGLASS, rot)
        frame['hq_fixture_class'] = 'approved_skylight_recessed_frame'
        glass['hq_fixture_class'] = 'approved_skylight_glazing'

# Quality refinement only. Do not enable OIDN: Ubuntu CI Blender may not provide it.
scene.render.resolution_x = 2048
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
if hasattr(scene, 'cycles'):
    scene.cycles.samples = 128
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.02

cameras = sorted([o for o in bpy.data.objects if o.type == 'CAMERA'], key=lambda o: o.name)
if len(cameras) != 5:
    raise RuntimeError(f'Expected exactly five locked cameras, found {len(cameras)}')

for idx, cam in enumerate(cameras, start=1):
    scene.camera = cam
    scene.render.filepath = str(OUT / f'node-{idx:02d}-production-treatment-refined.png')
    bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'riptide-hq-production-treatment-refined.blend'))
print('HQ production-treatment refinement complete: true skylight apertures, 5 locked cameras, 2048x1024 previews.')
