# Blender-native structural QA for the Riptide HQ shared scene.
import bpy, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/data/HQ-SHARED-SCENE-GEOMETRY-QA.json'
fail=[]
report={'status':'PASS','checks':{},'failures':fail}

def req(name):
    o=bpy.data.objects.get(name)
    if not o: fail.append(f'Missing required object: {name}')
    return o

def yrange(o):
    pts=[o.matrix_world @ v.co for v in o.data.vertices] if hasattr(o.data,'vertices') else []
    return (min(p.y for p in pts),max(p.y for p in pts)) if pts else (o.location.y,o.location.y)

# Overall shell authority from later orthographic production master.
floor=req('FLOOR')
if floor:
    report['checks']['shell_floor_dimensions_m']=[round(floor.dimensions.x,3),round(floor.dimensions.y,3)]
    if abs(floor.dimensions.x-10.5)>.01 or abs(floor.dimensions.y-24.0)>.01: fail.append('Shell footprint is not 10.50m x 24.00m')
for n in ['LOWER_WALL','UPPER_WALL','ROOF_LOWER','ROOF_UPPER','Q1Q2_GABLE','Q4_SEAWARD_RECT','Q4_SEAWARD_GABLE']:
    req(n)

# Roof slopes must rise from side eaves toward centre ridge: lower negative pitch, upper positive pitch.
rl,ru=bpy.data.objects.get('ROOF_LOWER'),bpy.data.objects.get('ROOF_UPPER')
if rl and ru:
    report['checks']['roof_pitch_y_rotation_rad']=[round(rl.rotation_euler.y,5),round(ru.rotation_euler.y,5)]
    if not (rl.rotation_euler.y < 0 and ru.rotation_euler.y > 0): fail.append('Roof pitch signs do not close at the centre ridge')

# Q1/Q2 is the only internal full-height partition relationship.
partition_names=[o.name for o in bpy.data.objects if 'Q2Q3' in o.name.upper() or 'Q3Q4' in o.name.upper()]
report['checks']['forbidden_transition_partition_objects']=partition_names
if partition_names: fail.append('Forbidden Q2/Q3 or Q3/Q4 partition object exists')

# Exactly one circular seaward window assembly.
glasses=[o.name for o in bpy.data.objects if o.name.startswith('SINGLE_CIRCULAR_SEAWARD_GLASS')]
frames=[o.name for o in bpy.data.objects if o.name.startswith('SINGLE_CIRCULAR_SEAWARD_FRAME')]
report['checks']['seaward_window_glass_count']=len(glasses); report['checks']['seaward_window_frame_count']=len(frames)
if len(glasses)!=1 or len(frames)!=1: fail.append('Seaward circular-window assembly is not unique')

# Five exact camera positions, one shared coordinate system.
expected={'01':(0,4.0,1.675),'02':(0,8.0,1.675),'03':(0,12.0,1.675),'04':(0,16.0,1.675),'05':(0,20.0,1.675)}
cams={}
for node,pos in expected.items():
    c=req('CAM_NODE_'+node)
    if not c: continue
    actual=tuple(round(v,3) for v in c.location); cams[node]=actual
    if any(abs(c.location[i]-pos[i])>.002 for i in range(3)): fail.append(f'Camera {node} position {actual} != {pos}')
    if c.data.type!='PANO' or c.data.panorama_type!='EQUIRECTANGULAR': fail.append(f'Camera {node} is not equirectangular PANO')
report['checks']['cameras']=cams

# Zone containment by authoritative prefix. Bounds touching thresholds are tolerated by 5cm only.
zone_limits={'Q2_':(0.0,8.0),'Q3_':(8.0,16.0),'Q4_':(16.0,24.0)}
zone_results={}
ignore={'Q4_SEAWARD_RECT','Q4_SEAWARD_GABLE'}
for prefix,(lo,hi) in zone_limits.items():
    bad=[]
    for o in bpy.data.objects:
        if not o.name.startswith(prefix) or o.name in ignore or o.type not in {'MESH','CURVE'}: continue
        y0,y1=yrange(o)
        if y0 < lo-.05 or y1 > hi+.05: bad.append({'name':o.name,'y':[round(y0,3),round(y1,3)]})
    zone_results[prefix]=bad
    if bad: fail.append(f'{prefix} content crosses its zone boundary: {bad}')
report['checks']['zone_boundary_violations']=zone_results

report['status']='FAIL' if fail else 'PASS'
OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(1 if fail else 0)
