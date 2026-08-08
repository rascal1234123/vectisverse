# Riptide HQ — production-treatment preview renderer
# Builds on the validated shared topology. Visual fidelity preview only until exact locked
# Riptide shield decal + exact shield-table outline are available as source assets.
import bpy, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/riptide/hq-tour/production-preview'; OUT.mkdir(parents=True,exist_ok=True)
W,L,EAVES,RIDGE,EYE,WALL=10.5,24.0,2.75,6.2,1.675,0.12


def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def mat(name,c,rough=.55,metal=0.0,emission=None,estr=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    if emission and 'Emission Color' in b.inputs:
        b.inputs['Emission Color'].default_value=(*emission,1); b.inputs['Emission Strength'].default_value=estr
    return m

def glass_mat(name,c):
    m=mat(name,c,.12,0.0)
    b=m.node_tree.nodes.get('Principled BSDF')
    if 'Transmission Weight' in b.inputs: b.inputs['Transmission Weight'].default_value=.72
    if 'IOR' in b.inputs: b.inputs['IOR'].default_value=1.45
    return m

def cube(name,loc,dims,m,rot=(0,0,0),bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('soft edges','BEVEL'); mod.width=bevel; mod.segments=3
    return o

def cyl(name,loc,r,d,m,rot=(0,0,0),vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d,location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; o.data.materials.append(m); return o

def gable(name,y,t,m):
    y0,y1=y-t/2,y+t/2
    vs=[(-W/2,y0,EAVES),(W/2,y0,EAVES),(0,y0,RIDGE),(-W/2,y1,EAVES),(W/2,y1,EAVES),(0,y1,RIDGE)]
    fs=[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]
    me=bpy.data.meshes.new(name+'_MESH'); me.from_pydata(vs,[],fs); me.update(); o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o

def boolean_cut(target,cutter):
    mod=target.modifiers.new('cut','BOOLEAN'); mod.operation='DIFFERENCE'; mod.solver='EXACT'; mod.object=cutter
    bpy.context.view_layer.objects.active=target; target.select_set(True); bpy.ops.object.modifier_apply(modifier=mod.name); target.select_set(False)

def shelf(name,x,y,z,w,h,depth,frame_m,wood_m,rows=3):
    cube(name+'_back',(x,y,z),(depth,w,h),frame_m)
    for i in range(rows+1):
        zz=z-h/2+i*h/rows
        cube(name+f'_shelf_{i}',(x-depth*.58,y,zz),(depth*1.35,w,.055),wood_m)
    for side in (-1,1): cube(name+f'_side_{side}',(x-depth*.58,y+side*w/2, z),(depth*1.35,.06,h),wood_m)

def chair(name,x,y,a,m):
    cube(name+'_seat',(x,y,.47),(.62,.62,.13),m,rot=(0,0,a),bevel=.08)
    cube(name+'_back',(x-.25*math.sin(a),y-.25*math.cos(a),.92),(.62,.14,.82),m,rot=(0,0,a),bevel=.08)
    cyl(name+'_stem',(x,y,.25),.055,.40,m,vertices=20)

def rack(name,x,y,m):
    cube(name+'_left',(x,y-.72,1.25),(.10,.10,2.5),m); cube(name+'_right',(x,y+.72,1.25),(.10,.10,2.5),m)
    cube(name+'_top',(x,y,2.45),(.10,1.55,.10),m)
    for yy in (-.58,.58):
        for z in (.55,1.05,1.55): cyl(name+f'_plate_{yy}_{z}',(x+.08,y+yy,z),.20,.16,m,rot=(0,math.pi/2,0),vertices=24)

def plant(name,x,y,z,leaf_m,pot_m):
    cyl(name+'_pot',(x,y,z+.22),.24,.44,pot_m,vertices=28)
    for i,a in enumerate(range(0,360,45)):
        rad=math.radians(a); cube(name+f'_leaf{i}',(x+.18*math.cos(rad),y+.18*math.sin(rad),z+.75),(.07,.38,.72),leaf_m,rot=(0,.35*math.sin(rad),rad),bevel=.03)

clear(); s=bpy.context.scene; s.unit_settings.system='METRIC'
s.render.resolution_x=1536; s.render.resolution_y=768; s.render.resolution_percentage=100; s.render.image_settings.file_format='PNG'; s.render.film_transparent=False
s.view_settings.look='AgX - Medium High Contrast'; s.view_settings.exposure=.25
s.world.use_nodes=True; bg=s.world.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value=(.025,.055,.085,1); bg.inputs['Strength'].default_value=.28

TIMBER=mat('treated warm timber',(.32,.16,.065),.64); TIMBER_LIGHT=mat('oak furniture',(.50,.27,.11),.55)
PLASTER=mat('warm lime plaster',(.62,.57,.48),.84); BLACK=mat('blackened steel',(.025,.03,.035),.32,.65)
CABINET=mat('charcoal cabinetry',(.035,.04,.045),.54,.15); LEATHER=mat('brown leather',(.22,.085,.035),.48)
RUBBER=mat('black rubber tile',(.035,.04,.045),.92); BLUE=mat('Riptide screen blue',(.01,.06,.11),.27,.15,emission=(.02,.25,.48),estr=.35)
GLASS=glass_mat('seaward glass',(.18,.48,.67)); SKYGLASS=glass_mat('skylight glass',(.24,.46,.60)); GREEN=mat('plant leaf',(.08,.22,.055),.78); POT=mat('plant pot',(.10,.08,.065),.78)
STEEL=mat('appliance steel',(.30,.32,.33),.28,.68); COUNTER=mat('stone worktop',(.38,.39,.38),.38); WHITE=mat('warm ceramic',(.70,.68,.62),.72)

# VALIDATED SHELL — topology and dimensions are unchanged from the geometry master.
cube('FLOOR',(0,L/2,-.075),(W,L,.15),TIMBER)
cube('LOWER_WALL',(-W/2,L/2,EAVES/2),(WALL,L,EAVES),PLASTER); cube('UPPER_WALL',(W/2,L/2,EAVES/2),(WALL,L,EAVES),PLASTER)
half=W/2; rise=RIDGE-EAVES; slope=math.hypot(half,rise); ang=math.atan2(rise,half)
cube('ROOF_LOWER',(-W/4,L/2,EAVES+rise/2),(slope,L,.16),TIMBER,rot=(0,-ang,0)); cube('ROOF_UPPER',(W/4,L/2,EAVES+rise/2),(slope,L,.16),TIMBER,rot=(0,ang,0))
# Exposed timber posts / roof bays.
for y in [0,3,6,9,12,15,18,21,24]:
    for x in (-W/2+.12,W/2-.12): cube(f'TIMBER_POST_{x}_{y}',(x,y,EAVES/2),(.22,.20,EAVES),TIMBER_LIGHT)
    cube(f'RIDGE_TIE_{y}',(0,y,RIDGE-.10),(W,.18,.16),TIMBER_LIGHT,rot=(0,0,0))
# Dark-framed skylight panels: four bays per roof slope. These are production-treatment fixtures, not new wall openings.
for side in (-1,1):
    for i,y in enumerate((4.5,9.5,14.5,19.5)):
        x=side*2.55; z=EAVES+rise*(1-abs(x)/(W/2))+.07; r=(0, side*ang,0)
        cube(f'SKYLIGHT_FRAME_{side}_{i}',(x,y,z),(1.45,1.75,.10),BLACK,rot=r)
        cube(f'SKYLIGHT_GLASS_{side}_{i}',(x-side*.02,y,z+.035),(1.20,1.50,.035),SKYGLASS,rot=r)
# Q1/Q2 closed partition and door.
dx,dw,dh=3.2,1.0,2.15
cube('Q1Q2_WALL_LEFT',((-W/2+dx-dw/2)/2,0,EAVES/2),(dx-dw/2+W/2,WALL,EAVES),PLASTER)
cube('Q1Q2_WALL_RIGHT',((dx+dw/2+W/2)/2,0,EAVES/2),(W/2-(dx+dw/2),WALL,EAVES),PLASTER)
cube('Q1Q2_WALL_HEADER',(dx,0,dh+(EAVES-dh)/2),(dw,WALL,EAVES-dh),PLASTER); gable('Q1Q2_GABLE',0,WALL,PLASTER)
cube('Q1_ACCESS_DOOR',(dx,.07,dh/2),(dw-.06,.10,dh-.04),TIMBER_LIGHT,bevel=.04)
# Seaward gable and one circular opening.
end_rect=cube('Q4_SEAWARD_RECT',(0,L,EAVES/2),(W,WALL,EAVES),PLASTER); end_gable=gable('Q4_SEAWARD_GABLE',L,WALL,PLASTER)
window_z,wr=2.75,1.95
bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=wr,depth=WALL*5,location=(0,L,window_z),rotation=(math.pi/2,0,0)); cutter=bpy.context.object
boolean_cut(end_rect,cutter); boolean_cut(end_gable,cutter); bpy.data.objects.remove(cutter,do_unlink=True)
cyl('SINGLE_CIRCULAR_SEAWARD_GLASS',(0,L+.018,window_z),wr*.965,.035,GLASS,rot=(math.pi/2,0,0),vertices=128)
bpy.ops.mesh.primitive_torus_add(major_radius=wr-.07,minor_radius=.075,major_segments=128,minor_segments=16,location=(0,L-.07,window_z),rotation=(math.pi/2,0,0)); bpy.context.object.name='SINGLE_CIRCULAR_SEAWARD_FRAME'; bpy.context.object.data.materials.append(BLACK)
# Window mullions from Q4 technical master.
cube('Q4_WINDOW_VERTICAL_MULLION',(0,L-.10,window_z),(.09,.08,wr*1.86),TIMBER_LIGHT)
cube('Q4_WINDOW_HORIZONTAL_MULLION',(0,L-.10,window_z),(wr*1.86,.08,.09),TIMBER_LIGHT)
# Simple sea / horizon outside the only window.
cube('EXTERIOR_SEA',(0,L+5,.35),(18,9,.12),mat('sea',(.025,.20,.34),.24,0,emission=(.015,.11,.20),estr=.18))
cube('EXTERIOR_HORIZON',(0,L+8,3.4),(18,.12,5.2),mat('sky',(.15,.40,.63),.35,0,emission=(.12,.32,.55),estr=.25))

# Q2 — Living / Team Area. Full lower-wall kitchen, opposed leather sofas, round coffee table, upper-wall entrance.
# Kitchen run y=1.0..7.0 along lower long wall.
cube('Q2_KITCHEN_BASE',(-W/2+.43,4.0,.48),(.72,5.8,.96),CABINET)
cube('Q2_KITCHEN_COUNTER',(-W/2+.39,4.0,1.00),(.82,5.9,.10),COUNTER)
cube('Q2_FRIDGE',(-W/2+.46,1.45,1.10),(.76,1.00,2.20),STEEL,bevel=.04)
cube('Q2_OVEN',(-W/2+.36,4.45,.68),(.10,.68,.74),BLACK)
cube('Q2_SINK',(-W/2+.32,5.55,1.07),(.08,.82,.46),STEEL)
for yy in (2.5,3.3,5.1,6.0):
    cube(f'Q2_OPEN_SHELF_{yy}',(-W/2+.30,yy,1.72),(.48,.76,.06),TIMBER_LIGHT)
for yy in (2.55,3.35,5.15,5.95): plant(f'Q2_SHELF_PLANT_{yy}',-W/2+.05,yy,1.77,GREEN,POT)
# Entrance is a fixture on upper wall, not a new window.
cube('Q2_EXTERIOR_ENTRY',(W/2-.07,3.10,1.08),(WALL,.98,2.16),TIMBER_LIGHT,bevel=.03)
# Opposed sofas with L returns.
cube('Q2_SOFA_LOWER_LONG',(-1.65,4.25,.47),(3.0,.92,.92),LEATHER,bevel=.13); cube('Q2_SOFA_LOWER_RETURN',(-2.72,5.15,.47),(.92,1.80,.92),LEATHER,bevel=.13)
cube('Q2_SOFA_UPPER_LONG',(1.65,4.25,.47),(3.0,.92,.92),LEATHER,bevel=.13); cube('Q2_SOFA_UPPER_RETURN',(2.72,3.35,.47),(.92,1.80,.92),LEATHER,bevel=.13)
cyl('Q2_ROUND_COFFEE_TABLE',(0,4.25,.39),.78,.10,TIMBER_LIGHT,vertices=64); cyl('Q2_TABLE_LEG',(0,4.25,.19),.11,.38,BLACK,vertices=24)
plant('Q2_PLANT_UPPER',W/2-.62,6.6,0,GREEN,POT)

# Q3 — rubber flooring wholly inside Q3; equipment arranged against long walls, central sightline clear.
cube('Q3_RUBBER_TILES',(0,12,.028),(8.65,7.82,.055),RUBBER)
for yy in (9.6,12.1,14.6): rack(f'Q3_POWER_RACK_{yy}',-W/2+.62,yy,BLACK)
# Dumbbell / kettlebell racks on opposing wall.
for yy,label in ((10.0,'DUMBBELL'),(12.7,'KETTLEBELL')):
    cube(f'Q3_{label}_RACK',(W/2-.63,yy,.88),(.72,2.05,1.45),BLACK)
    for iz,z in enumerate((.52,.88,1.20)):
        for j in range(5):
            cyl(f'Q3_{label}_{iz}_{j}',(W/2-.98,yy-.76+j*.38,z),.105,.14,BLACK,rot=(0,math.pi/2,0),vertices=20)
# Resistance bands, medicine balls and plyo boxes.
for j in range(5): cube(f'Q3_BAND_{j}',(W/2-.14,14.4+j*.22,1.42),(.08,.08,1.25),mat(f'band{j}',(.15+.06*j,.20,.10+.04*j),.75))
for j,z in enumerate((.42,.82,1.22,1.62)): cyl(f'Q3_MEDBALL_{j}',(W/2-.55,15.35,z),.22,.42,BLACK,rot=(0,math.pi/2,0),vertices=24)
cube('Q3_PLYO_BOX_A',(W/2-1.25,15.1,.35),(1.0,1.0,.70),TIMBER_LIGHT); cube('Q3_PLYO_BOX_B',(W/2-2.10,15.45,.25),(.75,.75,.50),TIMBER_LIGHT)
# Adjustable bench near lower wall but inside Q3.
cube('Q3_ADJUSTABLE_BENCH',(-3.2,11.3,.38),(1.85,.58,.22),LEATHER,rot=(0,0,.12),bevel=.06)

# Q4 — treated timber remains visible; artefact wall lower, technology wall upper, central table and eight seats.
# Interactive / artefact bookshelf wall.
cube('Q4_BOOKSHELF_BASE',(-W/2+.42,20,.52),(.72,6.3,1.04),CABINET)
for yy in (17.7,19.0,20.3,21.6,22.9):
    cube(f'Q4_ARTEFACT_SHELF_{yy}',(-W/2+.32,yy,1.42),(.58,1.05,.07),TIMBER_LIGHT)
    cube(f'Q4_ARTEFACT_FRAME_{yy}',(-W/2+.25,yy,1.82),(.10,.66,.48),BLACK)
# Technology wall opposite: display plus low cabinetry. No approximate logo is created.
cube('Q4_TECH_CABINET',(W/2-.42,20,.46),(.72,6.0,.92),CABINET)
cube('Q4_WIDESCREEN',(W/2-.18,20,1.62),(.10,3.55,1.32),BLUE,bevel=.03)
for yy in (17.65,22.35): plant(f'Q4_PLANT_{yy}',W/2-.60,yy,0,GREEN,POT)
# Table placeholder is deliberately named and visually neutral: exact shield outline replacement remains required.
cube('Q4_SHIELD_TABLE_EXACT_OUTLINE_PENDING',(0,20.45,.61),(3.55,4.55,.18),TIMBER_LIGHT,bevel=.42)
# Eight seats around the table.
positions=[(-2.15,19.05,math.pi/2),(2.15,19.05,-math.pi/2),(-2.25,20.55,math.pi/2),(2.25,20.55,-math.pi/2),(-1.65,22.05,math.pi/2),(1.65,22.05,-math.pi/2),(-.70,18.15,0),(.70,18.15,0)]
for i,(x,y,a) in enumerate(positions): chair(f'Q4_CHAIR_{i+1}',x,y,a,LEATHER)
# Small seaward consoles from technical elevation; preserve clear central window sightline.
cube('Q4_SEAWARD_CONSOLE_LOWER',(-2.85,23.55,.48),(1.35,.52,.96),CABINET); cube('Q4_SEAWARD_CONSOLE_UPPER',(2.85,23.55,.48),(1.35,.52,.96),CABINET)

# Warm architectural lighting plus cool daylight accents.
for y in (2,5,8,11,14,17,20,23):
    bpy.ops.object.light_add(type='POINT',location=(0,y,3.15)); li=bpy.context.object; li.data.energy=420; li.data.color=(1.0,.70,.42); li.data.shadow_soft_size=1.0
for x in (-2.7,2.7):
    for y in (5,10,15,20):
        bpy.ops.object.light_add(type='AREA',location=(x,y,4.15)); li=bpy.context.object; li.data.energy=210; li.data.shape='RECTANGLE'; li.data.size=1.4; li.data.size_y=1.0; li.rotation_euler=(0,0,0)
# Daylight behind seaward window.
bpy.ops.object.light_add(type='AREA',location=(0,L+1.5,window_z)); dl=bpy.context.object; dl.data.energy=850; dl.data.color=(.52,.72,1.0); dl.data.size=5.5; dl.rotation_euler=(math.pi/2,0,0)

s.render.engine='CYCLES'; s.cycles.samples=20; s.cycles.use_denoising=False
for node,y in {'01':4.,'02':8.,'03':12.,'04':16.,'05':20.}.items():
    d=bpy.data.cameras.new('CAM_NODE_'+node); d.type='PANO'; d.panorama_type='EQUIRECTANGULAR'
    c=bpy.data.objects.new('CAM_NODE_'+node,d); s.collection.objects.link(c); c.location=(0,y,EYE); c.rotation_euler=(math.radians(90),0,0); s.camera=c
    s.render.filepath=str(OUT/f'node-{node}-production-preview.png'); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'riptide-hq-production-preview.blend'))