# Riptide HQ — deterministic five-node shared-scene validation renderer
# Geometry/topology validation only; proxy materials are not visual masters.
import bpy, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/riptide/hq-tour/validation'; OUT.mkdir(parents=True,exist_ok=True)
# Later approved orthographic production master controls overall shell dimensions.
W,L,EAVES,RIDGE,EYE,WALL=10.5,24.0,2.75,6.2,1.675,0.12

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(name,c,rough=.6,metal=.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; m.diffuse_color=(*c,1)
    b=m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    # Small self-illumination makes proxy geometry readable without artistic lighting decisions.
    if 'Emission Color' in b.inputs: b.inputs['Emission Color'].default_value=(*c,1)
    if 'Emission Strength' in b.inputs: b.inputs['Emission Strength'].default_value=.18
    return m
def cube(name,loc,dims,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m); return o
def cyl(name,loc,r,d,m,rot=(0,0,0),vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d,location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.data.materials.append(m); return o
def chair(name,x,y,a,m):
    cube(name+'_seat',(x,y,.48),(.55,.55,.12),m,rot=(0,0,a)); cube(name+'_back',(x,y-.23*math.cos(a),.9),(.55,.12,.8),m,rot=(0,0,a))
def rack(name,x,y,m):
    cube(name+'_frame',(x,y,1.2),(1.7,.65,2.4),m)
    for z in (.45,1.0,1.55): cube(name+f'_shelf{z}',(x,y,z),(1.5,.7,.08),m)
    for ix in (-.55,0,.55):
        for iz in (.62,1.18): cyl(name+f'_weight{ix}{iz}',(x+ix,y-.1,iz),.17,.18,m,rot=(math.pi/2,0,0),vertices=24)

clear(); s=bpy.context.scene; s.unit_settings.system='METRIC'; s.render.resolution_x=1024; s.render.resolution_y=512; s.render.resolution_percentage=100; s.render.image_settings.file_format='PNG'; s.render.film_transparent=False
s.view_settings.look='AgX - Medium High Contrast'; s.view_settings.exposure=.6
s.world.use_nodes=True; bg=s.world.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value=(.055,.055,.065,1); bg.inputs['Strength'].default_value=.35
WOOD=mat('Warm timber',(.30,.15,.07),.72); WOOD2=mat('Light timber',(.48,.26,.12),.68); DARK=mat('Dark equipment',(.07,.08,.095),.45,.15); SOFA=mat('Sofa charcoal',(.12,.13,.14),.82); RUBBER=mat('Rubber floor',(.09,.095,.10),.9); SCREEN=mat('Technology screen',(.015,.09,.18),.25,.1); GLASS=mat('Sea window',(.10,.42,.62),.12)
# Continuous shell.
cube('FLOOR',(0,L/2,-.08),(W,L,.16),WOOD2); cube('LOWER_WALL',(-W/2,L/2,EAVES/2),(WALL,L,EAVES),WOOD); cube('UPPER_WALL',(W/2,L/2,EAVES/2),(WALL,L,EAVES),WOOD)
half=W/2; rise=RIDGE-EAVES; slope=math.hypot(half,rise); ang=math.atan2(rise,half); cube('ROOF_LOWER',(-W/4,L/2,EAVES+rise/2),(slope,L,.14),WOOD,rot=(0,ang,0)); cube('ROOF_UPPER',(W/4,L/2,EAVES+rise/2),(slope,L,.14),WOOD,rot=(0,-ang,0))
# Q1/Q2 partition with one access opening; there are no partitions at Q2/Q3 or Q3/Q4.
dx,dw,dh=3.2,1.0,2.15; cube('Q1Q2_WALL_LEFT',((-W/2+dx-dw/2)/2,0,EAVES/2),(dx-dw/2+W/2,WALL,EAVES),WOOD); cube('Q1Q2_WALL_RIGHT',((dx+dw/2+W/2)/2,0,EAVES/2),(W/2-(dx+dw/2),WALL,EAVES),WOOD); cube('Q1Q2_WALL_HEADER',(dx,0,dh+(EAVES-dh)/2),(dw,WALL,EAVES-dh),WOOD)
# Single seaward circular-window relationship.
wr=2.0; cube('Q4_END_LEFT',(-(W/2+wr)/2,L,EAVES/2),(W/2-wr,WALL,EAVES),WOOD); cube('Q4_END_RIGHT',((W/2+wr)/2,L,EAVES/2),(W/2-wr,WALL,EAVES),WOOD); cube('Q4_END_BOTTOM',(0,L,.45),(2*wr,WALL,.9),WOOD); cube('Q4_END_TOP',(0,L,(EAVES+wr+.9)/2),(2*wr,WALL,max(.2,EAVES-(wr+.9))),WOOD); cyl('SINGLE_CIRCULAR_SEAWARD_WINDOW',(0,L+.04,1.55),wr,.04,GLASS,rot=(math.pi/2,0,0),vertices=96)
# Q2 content only.
cube('Q2_KITCHEN_BASE',(-W/2+.45,3,.55),(.75,4.8,1.1),DARK); cube('Q2_KITCHEN_TOP',(-W/2+.42,3,1.55),(.65,4.8,.9),DARK); cube('Q2_EXTERIOR_ENTRY',(W/2-.08,3.2,1.05),(WALL,1.05,2.1),DARK); cube('Q2_SOFA_A_LONG',(-1.45,4.1,.45),(2.8,.85,.9),SOFA); cube('Q2_SOFA_A_SHORT',(-2.45,4.95,.45),(.85,1.7,.9),SOFA); cube('Q2_SOFA_B_LONG',(1.45,4.1,.45),(2.8,.85,.9),SOFA); cube('Q2_SOFA_B_SHORT',(2.45,3.25,.45),(.85,1.7,.9),SOFA); cyl('Q2_ROUND_COFFEE_TABLE',(0,4.1,.36),.72,.72,WOOD2)
# Q3 content only.
cube('Q3_RUBBER_TILES',(0,12,.025),(8.6,7.2,.05),RUBBER); rack('Q3_SMITH_MACHINE',-4.15,10,DARK); cube('Q3_ADJUSTABLE_BENCH',(-2.6,11,.35),(1.6,.55,.25),DARK,rot=(0,0,.15)); rack('Q3_DUMBBELL_RACK',-4.2,13,DARK); rack('Q3_KETTLEBELL_RACK',-4.2,15,DARK); cube('Q3_RESISTANCE_BANDS',(4.35,10,1.35),(.25,1.2,2.4),DARK); cube('Q3_PLYO_BOXES',(3.7,13,.55),(1.4,1.4,1.1),WOOD2); rack('Q3_MED_BALL_RACK',4.2,15,DARK)
# Q4 content only.
cube('Q4_SHIELD_TABLE_BODY',(0,20,.48),(3.8,3.7,.22),WOOD2); bpy.ops.mesh.primitive_cone_add(vertices=3,radius1=2.2,depth=.22,location=(0,22,.48),rotation=(0,0,math.pi)); bpy.context.object.data.materials.append(WOOD2); bpy.context.object.name='Q4_SHIELD_TABLE_NOSE'
for i,(x,y,a) in enumerate([(-2.2,18.8,0),(2.2,18.8,0),(-2.3,20.2,0),(2.3,20.2,0),(-1.9,21.6,0),(1.9,21.6,0),(-.8,22.4,0),(.8,22.4,0)]): chair(f'Q4_CHAIR_{i+1}',x,y,a,SOFA)
cube('Q4_TECH_WALL',(W/2-.10,20,1.55),(WALL,5,2.2),SCREEN); cube('Q4_BOOKSHELF',(-W/2+.30,20,1.25),(.55,5,2.5),DARK)
# Neutral validation light only; scene topology and object positions do not depend on it.
for y in [2,5,8,11,14,17,20,23]:
    bpy.ops.object.light_add(type='POINT',location=(0,y,2.7)); l=bpy.context.object; l.data.energy=500; l.data.shadow_soft_size=1.4
s.render.engine='CYCLES'; s.cycles.samples=12; s.cycles.use_denoising=False
for node,y in {'01':4.,'02':8.,'03':12.,'04':16.,'05':20.}.items():
    d=bpy.data.cameras.new('CAM_NODE_'+node); d.type='PANO'; d.panorama_type='EQUIRECTANGULAR'; c=bpy.data.objects.new('CAM_NODE_'+node,d); s.collection.objects.link(c); c.location=(0,y,EYE); c.rotation_euler=(math.radians(90),0,0); s.camera=c; s.render.filepath=str(OUT/f'node-{node}-validation.png'); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'riptide-hq-shared-validation.blend'))
