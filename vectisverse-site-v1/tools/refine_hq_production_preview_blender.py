# Riptide HQ — downstream production-treatment refinement
# Corrects only production-treatment fixtures/materials after the validated shared shell is built.
# Spatial authority: Definitive Floor Plan v1.2 / 3D Block-out Master v1.0.
# Fidelity gate: rerender after material, wall-assignment, gym-window and skylight corrections.
import bpy, math, runpy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools'/'render_hq_production_preview_blender.py'
OUT=ROOT/'assets'/'riptide'/'hq-tour'/'production-preview-refined'
OUT.mkdir(parents=True,exist_ok=True)
runpy.run_path(str(BASE),run_name='__main__')
scene=bpy.context.scene
W,EAVES,RIDGE=10.5,2.75,6.2
rise=RIDGE-EAVES; ang=math.atan2(rise,W/2)

BLACK=bpy.data.materials.get('blackened steel'); SKYGLASS=bpy.data.materials.get('skylight glass')
TIMBER=bpy.data.materials.get('treated warm timber'); OAK=bpy.data.materials.get('oak furniture')
PLASTER=bpy.data.materials.get('warm lime plaster'); LEATHER=bpy.data.materials.get('brown leather')
if None in (BLACK,SKYGLASS,TIMBER,OAK,PLASTER,LEATHER): raise RuntimeError('Required production materials missing')

def cube(name,loc,dims,mat=None,rot=(0,0,0),bevel=0):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if mat:o.data.materials.append(mat)
    if bevel:
        m=o.modifiers.new('edge softening','BEVEL'); m.width=bevel; m.segments=3
    return o

def cut(target,cutter):
    m=target.modifiers.new('production aperture','BOOLEAN'); m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=cutter
    bpy.context.view_layer.objects.active=target; target.select_set(True); bpy.ops.object.modifier_apply(modifier=m.name); target.select_set(False)

def mirror_x(prefixes):
    for o in bpy.data.objects:
        if any(o.name.startswith(p) for p in prefixes): o.location.x=-o.location.x

def delete_prefix(prefix):
    for o in list(bpy.data.objects):
        if o.name.startswith(prefix): bpy.data.objects.remove(o,do_unlink=True)

# LOCKED WALL ASSIGNMENTS — Floor Plan v1.2 wins over earlier preview placement.
mirror_x(('Q2_KITCHEN_','Q2_FRIDGE','Q2_OVEN','Q2_SINK','Q2_OPEN_SHELF_','Q2_SHELF_PLANT_','Q2_EXTERIOR_ENTRY'))
mirror_x(('Q4_BOOKSHELF_BASE','Q4_ARTEFACT_','Q4_TECH_CABINET','Q4_WIDESCREEN','Q4_PLANT_'))
for p in ('Q3_POWER_RACK_12.1','Q3_POWER_RACK_14.6'): delete_prefix(p)
mirror_x(('Q3_POWER_RACK_9.6',))

left_wall=bpy.data.objects.get('LOWER_WALL')
if left_wall is None: raise RuntimeError('Validated left wall missing')
for i,y in enumerate((10.7,13.4)):
    z=1.48
    cutter=cube(f'_Q3_WINDOW_CUT_{i}',(-W/2,y,z),(.55,1.55,1.35))
    cut(left_wall,cutter); bpy.data.objects.remove(cutter,do_unlink=True)
    cube(f'Q3_LEFT_WINDOW_GLASS_{i}',(-W/2+.005,y,z),(.035,1.38,1.18),SKYGLASS)
    for yy in (y-.735,y+.735): cube(f'Q3_LEFT_WINDOW_H_{i}_{yy}',(-W/2+.025,yy,z),(.12,.09,1.34),BLACK)
    for zz in (z-.63,z+.63): cube(f'Q3_LEFT_WINDOW_V_{i}_{zz}',(-W/2+.025,y,zz),(.12,1.56,.09),BLACK)

# TRUE SKYLIGHTS
for o in list(bpy.data.objects):
    if o.name.startswith('SKYLIGHT_FRAME_') or o.name.startswith('SKYLIGHT_GLASS_'):
        bpy.data.objects.remove(o,do_unlink=True)
for side in (-1,1):
    roof=bpy.data.objects.get('ROOF_LOWER' if side<0 else 'ROOF_UPPER')
    if roof is None: raise RuntimeError('Validated roof plane missing')
    for i,y in enumerate((4.5,9.5,14.5,19.5)):
        x=side*2.55; z=EAVES+rise*(1-abs(x)/(W/2)); rot=(0,side*ang,0)
        cutter=cube(f'_SKYLIGHT_CUT_{side}_{i}',(x,y,z),(1.25,1.55,.52),rot=rot)
        cut(roof,cutter); bpy.data.objects.remove(cutter,do_unlink=True)
        cube(f'SKYLIGHT_TOP_{side}_{i}',(x,y+.79,z-.025),(1.47,.10,.075),BLACK,rot)
        cube(f'SKYLIGHT_BOTTOM_{side}_{i}',(x,y-.79,z-.025),(1.47,.10,.075),BLACK,rot)
        cube(f'SKYLIGHT_LEFT_{side}_{i}',(x-side*.66,y,z-.025),(.10,1.50,.075),BLACK,rot)
        cube(f'SKYLIGHT_RIGHT_{side}_{i}',(x+side*.66,y,z-.025),(.10,1.50,.075),BLACK,rot)
        g=cube(f'SKYLIGHT_GLAZING_{side}_{i}',(x,y,z-.035),(1.18,1.42,.025),SKYGLASS,rot); g['hq_fixture_class']='approved_skylight_glazing'

# LOCKED SHIELD TABLE
ph=bpy.data.objects.get('Q4_SHIELD_TABLE_EXACT_OUTLINE_PENDING')
if ph is None: raise RuntimeError('Q4 shield table placeholder missing')
bpy.data.objects.remove(ph,do_unlink=True)
pts=[(484,119),(394,129),(329,158),(332,329),(354,471),(389,526),(465,591),(514,554),(569,491),(590,405),(600,296),(601,155)]
minx,maxx=min(x for x,y in pts),max(x for x,y in pts); miny,maxy=min(y for x,y in pts),max(y for x,y in pts)
cx,cy=(minx+maxx)/2,(miny+maxy)/2; TW,TL=3.55,4.55
xy=[(((px-cx)/(maxx-minx))*TW,20.45-((py-cy)/(maxy-miny))*TL) for px,py in pts]
z0,z1=.52,.70; n=len(xy); verts=[(x,y,z0) for x,y in xy]+[(x,y,z1) for x,y in xy]
faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
me=bpy.data.meshes.new('Q4_SHIELD_TABLE_LOCKED_MESH'); me.from_pydata(verts,[],faces); me.update()
t=bpy.data.objects.new('Q4_SHIELD_TABLE_LOCKED_OUTLINE',me); bpy.context.collection.objects.link(t); t.data.materials.append(OAK)
t['hq_fixture_class']='locked_exact_shield_table_outline'; t['source_master']='Riptide HQ Table Silhouette Correction Board.png'
bpy.context.view_layer.objects.active=t; t.select_set(True); b=t.modifiers.new('table edge softening','BEVEL'); b.width=.045; b.segments=3; bpy.ops.object.modifier_apply(modifier=b.name); t.select_set(False)

# VISUAL-FIDELITY PASS
def base(mat,rgba,rough=None,metal=None):
    bs=mat.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*rgba,1)
    if rough is not None: bs.inputs['Roughness'].default_value=rough
    if metal is not None: bs.inputs['Metallic'].default_value=metal
base(TIMBER,(.20,.095,.035),.58); base(OAK,(.36,.17,.055),.48); base(PLASTER,(.72,.70,.64),.82); base(LEATHER,(.16,.055,.018),.42)
for mat in (TIMBER,OAK):
    nt=mat.node_tree; bs=nt.nodes.get('Principled BSDF'); tex=nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=5.0; tex.inputs['Detail'].default_value=2.0; tex.inputs['Roughness'].default_value=.6
    ramp=nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color=(.035,.012,.004,1); ramp.color_ramp.elements[1].color=(.32,.13,.035,1)
    nt.links.new(tex.outputs['Fac'],ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'],bs.inputs['Base Color'])
scene.view_settings.exposure=-.55
world=scene.world.node_tree.nodes.get('Background'); world.inputs['Color'].default_value=(.07,.11,.17,1); world.inputs['Strength'].default_value=.48
for o in bpy.data.objects:
    if o.type=='LIGHT':
        if o.data.type=='POINT': o.data.energy=190; o.data.color=(1.0,.83,.68); o.data.shadow_soft_size=1.25
        elif o.data.type=='AREA': o.data.energy=260; o.data.color=(.72,.84,1.0)
for y in (5,10,15,20):
    bpy.ops.object.light_add(type='AREA',location=(0,y,4.75)); l=bpy.context.object; l.name=f'DAYLIGHT_SKYLIGHT_FILL_{y}'; l.data.energy=320; l.data.color=(.64,.78,1.0); l.data.shape='RECTANGLE'; l.data.size=4.0; l.data.size_y=2.2

scene.render.resolution_x=2048; scene.render.resolution_y=1024; scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'
scene.render.engine='CYCLES'; scene.cycles.samples=128; scene.cycles.use_denoising=False; scene.cycles.use_adaptive_sampling=True; scene.cycles.adaptive_threshold=.02
cams=sorted([o for o in bpy.data.objects if o.type=='CAMERA'],key=lambda o:o.name)
if len(cams)!=5: raise RuntimeError(f'Expected 5 locked cameras, found {len(cams)}')
for idx,cam in enumerate(cams,1):
    scene.camera=cam; scene.render.filepath=str(OUT/f'node-{idx:02d}-production-treatment-refined.png'); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'riptide-hq-production-treatment-refined.blend'))
print('HQ refinement complete: locked wall assignments corrected; paired gym windows added; skylight black-panel defect removed; shield table retained; neutral photoreal treatment applied.')
