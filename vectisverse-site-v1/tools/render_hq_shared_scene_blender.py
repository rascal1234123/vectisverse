# Riptide HQ — deterministic five-node shared-scene validation renderer
# Generated under RIPTIDE HQ Autonomous Production Directive v1.0.
# Purpose: geometry/topology validation only. It does not promote proxy materials as visual masters.

import bpy, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/riptide/hq-tour/validation"
OUT.mkdir(parents=True, exist_ok=True)

W = 9.1
L = 24.0
EAVES = 2.75
RIDGE = 4.9
EYE = 1.675
Q = 8.0
WALL = 0.12

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def mat(name, color, rough=0.6, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color,1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color,1)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metallic
    return m

def cube(name, loc, dims, material, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    return o

def cyl(name, loc, radius, depth, material, rot=(0,0,0), vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; o.data.materials.append(material)
    return o

def chair(name, x,y,angle, dark):
    cube(name+"_seat",(x,y,0.48),(0.55,0.55,0.12),dark,rot=(0,0,angle))
    cube(name+"_back",(x,y-0.23*math.cos(angle),0.9),(0.55,0.12,0.8),dark,rot=(0,0,angle))

def rack(name,x,y,dark):
    cube(name+"_frame",(x,y,1.2),(1.7,0.65,2.4),dark)
    for z in (0.45,1.0,1.55):
        cube(name+f"_shelf{z}",(x,y,z),(1.5,0.7,0.08),dark)
    for ix in (-0.55,0,0.55):
        for iz in (0.62,1.18):
            cyl(name+f"_weight{ix}{iz}",(x+ix,y-0.1,iz),0.17,0.18,dark,rot=(math.pi/2,0,0),vertices=24)

clear()
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=1024
scene.render.resolution_y=512
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False

M_WOOD=mat('Warm timber',(0.30,0.15,0.07),0.72)
M_WOOD2=mat('Light timber',(0.48,0.26,0.12),0.68)
M_DARK=mat('Dark equipment',(0.035,0.045,0.055),0.45,0.15)
M_SOFA=mat('Sofa charcoal',(0.08,0.09,0.10),0.82)
M_RUBBER=mat('Rubber floor',(0.055,0.06,0.065),0.9)
M_SCREEN=mat('Technology screen',(0.01,0.05,0.10),0.25,0.1)
M_GLASS=mat('Sea window',(0.10,0.35,0.52),0.12)

# Continuous shell.
cube('FLOOR',(0,L/2,-0.08),(W,L,0.16),M_WOOD2)
cube('LOWER_WALL',(-W/2,L/2,EAVES/2),(WALL,L,EAVES),M_WOOD)
cube('UPPER_WALL',( W/2,L/2,EAVES/2),(WALL,L,EAVES),M_WOOD)
half=W/2; rise=RIDGE-EAVES; slope=math.hypot(half,rise); ang=math.atan2(rise,half)
cube('ROOF_LOWER',(-W/4,L/2,EAVES+rise/2),(slope,L,0.14),M_WOOD,rot=(0,ang,0))
cube('ROOF_UPPER',( W/4,L/2,EAVES+rise/2),(slope,L,0.14),M_WOOD,rot=(0,-ang,0))

# Q1/Q2 partition with one access opening near upper wall.
door_x=2.8; door_w=1.0; door_h=2.15
cube('Q1Q2_WALL_LEFT',((-W/2+door_x-door_w/2)/2,0,EAVES/2),(door_x-door_w/2+W/2,WALL,EAVES),M_WOOD)
cube('Q1Q2_WALL_RIGHT',((door_x+door_w/2+W/2)/2,0,EAVES/2),(W/2-(door_x+door_w/2),WALL,EAVES),M_WOOD)
cube('Q1Q2_WALL_HEADER',(door_x,0,door_h+(EAVES-door_h)/2),(door_w,WALL,EAVES-door_h),M_WOOD)

# Seaward end: one circular opening relationship only.
win_r=2.0
cube('Q4_END_LEFT',(-(W/2+win_r)/2,L,EAVES/2),(W/2-win_r,WALL,EAVES),M_WOOD)
cube('Q4_END_RIGHT',((W/2+win_r)/2,L,EAVES/2),(W/2-win_r,WALL,EAVES),M_WOOD)
cube('Q4_END_BOTTOM',(0,L,0.45),(2*win_r,WALL,0.9),M_WOOD)
cube('Q4_END_TOP',(0,L,(EAVES+win_r+0.9)/2),(2*win_r,WALL,max(0.2,EAVES-(win_r+0.9))),M_WOOD)
cyl('SINGLE_CIRCULAR_SEAWARD_WINDOW',(0,L+0.04,1.55),win_r,0.04,M_GLASS,rot=(math.pi/2,0,0),vertices=96)

# Q2 Team Area, 0<y<8.
cube('Q2_KITCHEN_BASE',(-W/2+0.45,3.0,0.55),(0.75,4.8,1.1),M_DARK)
cube('Q2_KITCHEN_TOP',(-W/2+0.42,3.0,1.55),(0.65,4.8,0.9),M_DARK)
cube('Q2_EXTERIOR_ENTRY',(W/2-0.08,3.2,1.05),(WALL,1.05,2.1),M_DARK)
cube('Q2_SOFA_A_LONG',(-1.45,4.1,0.45),(2.8,0.85,0.9),M_SOFA)
cube('Q2_SOFA_A_SHORT',(-2.45,4.95,0.45),(0.85,1.7,0.9),M_SOFA)
cube('Q2_SOFA_B_LONG',(1.45,4.1,0.45),(2.8,0.85,0.9),M_SOFA)
cube('Q2_SOFA_B_SHORT',(2.45,3.25,0.45),(0.85,1.7,0.9),M_SOFA)
cyl('Q2_ROUND_COFFEE_TABLE',(0,4.1,0.36),0.72,0.72,M_WOOD2)

# Q3 training content, entirely 8<y<16.
cube('Q3_RUBBER_TILES',(0,12.0,0.025),(7.4,7.2,0.05),M_RUBBER)
rack('Q3_SMITH_MACHINE',-3.55,10.0,M_DARK)
cube('Q3_ADJUSTABLE_BENCH',(-2.2,11.0,0.35),(1.6,0.55,0.25),M_DARK,rot=(0,0,0.15))
rack('Q3_DUMBBELL_RACK',-3.6,13.0,M_DARK)
rack('Q3_KETTLEBELL_RACK',-3.6,15.0,M_DARK)
cube('Q3_RESISTANCE_BANDS',(3.65,10.0,1.35),(0.25,1.2,2.4),M_DARK)
cube('Q3_PLYO_BOXES',(3.2,13.0,0.55),(1.4,1.4,1.1),M_WOOD2)
rack('Q3_MED_BALL_RACK',3.55,15.0,M_DARK)

# Q4 briefing content, entirely 16<y<24.
cube('Q4_SHIELD_TABLE_BODY',(0,20.0,0.48),(3.8,3.7,0.22),M_WOOD2)
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=2.2, depth=0.22, location=(0,22.0,0.48), rotation=(0,0,math.pi))
bpy.context.object.data.materials.append(M_WOOD2); bpy.context.object.name='Q4_SHIELD_TABLE_NOSE'
for i,(x,y,a) in enumerate([(-2.2,18.8,0),(2.2,18.8,0),(-2.3,20.2,0),(2.3,20.2,0),(-1.9,21.6,0),(1.9,21.6,0),(-0.8,22.4,0),(0.8,22.4,0)]):
    chair(f'Q4_CHAIR_{i+1}',x,y,a,M_SOFA)
cube('Q4_TECH_WALL',(W/2-0.10,20.0,1.55),(WALL,5.0,2.2),M_SCREEN)
cube('Q4_BOOKSHELF',(-W/2+0.30,20.0,1.25),(0.55,5.0,2.5),M_DARK)

for y in [2,5,8,11,14,17,20,23]:
    bpy.ops.object.light_add(type='AREA', location=(0,y,4.2))
    lamp=bpy.context.object; lamp.data.energy=420; lamp.data.shape='DISK'; lamp.data.size=2.0
scene.world.color=(0.025,0.025,0.03)

# Five fixed camera positions in one coordinate system. 0° points seaward (+Y).
cams={'01':4.0,'02':8.0,'03':12.0,'04':16.0,'05':20.0}
for node,y in cams.items():
    data=bpy.data.cameras.new(f'CAM_NODE_{node}')
    data.type='PANO'; data.panorama_type='EQUIRECTANGULAR'
    cam=bpy.data.objects.new(f'CAM_NODE_{node}',data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location=(0,y,EYE)
    cam.rotation_euler=(math.radians(90),0,0)
    scene.camera=cam
    scene.render.filepath=str(OUT/f'node-{node}-validation.png')
    bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'riptide-hq-shared-validation.blend'))
