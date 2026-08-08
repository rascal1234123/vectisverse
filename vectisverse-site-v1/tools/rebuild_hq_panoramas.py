#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import json, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/riptide/hq-tour/validation'
REPORT = ROOT / 'assets/data/HQ-PANORAMA-REBUILD-QA.json'
failures=[]
rows={}

blend = OUT / 'riptide-hq-shared-validation.blend'
if not blend.exists() or blend.stat().st_size < 10000:
    failures.append('Shared Blender scene file missing or unexpectedly small')

for n in range(1,6):
    node=f'{n:02d}'
    p=OUT/f'node-{node}-validation.png'
    if not p.exists():
        failures.append(f'Node {node}: missing validation render')
        continue
    try:
        im=Image.open(p); im.load()
    except Exception as e:
        failures.append(f'Node {node}: decode failure: {e}')
        continue
    if im.size != (1024,512):
        failures.append(f'Node {node}: dimensions {im.size}, expected 1024x512')
    rgb=im.convert('RGB')
    strip=4
    diff=ImageChops.difference(rgb.crop((0,0,strip,512)),rgb.crop((1024-strip,0,1024,512)))
    seam=sum(ImageStat.Stat(diff).mean)/3.0
    thumb=rgb.resize((128,64))
    px=list(thumb.getdata())
    blank=sum(1 for r,g,b in px if (r<3 and g<3 and b<3) or (r>252 and g>252 and b>252))/len(px)
    extrema=rgb.getextrema()
    dynamic=max(v[1]-v[0] for v in extrema)
    rows[node]={
        'file':str(p.relative_to(ROOT)),
        'dimensions':list(im.size),
        'bytes':p.stat().st_size,
        'seam_edge_mae':round(seam,3),
        'extreme_blank_ratio':round(blank,6),
        'dynamic_range':dynamic
    }
    if blank > 0.40:
        failures.append(f'Node {node}: extreme blank ratio {blank:.3f} > 0.40')
    if dynamic < 20:
        failures.append(f'Node {node}: render appears near-uniform / blank')

report={
    'stage':'shared-scene geometry validation',
    'status':'FAIL' if failures else 'PASS',
    'projection':'equirectangular 2:1',
    'orientation':'0 degrees = seaward',
    'nodes':rows,
    'failures':failures,
    'note':'These 1024x512 proxy-material renders validate shared geometry only; they are not release-final visual assets.'
}
REPORT.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(1 if failures else 0)
