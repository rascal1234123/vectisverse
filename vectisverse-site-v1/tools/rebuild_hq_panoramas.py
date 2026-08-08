#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import base64, io, json, numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets/riptide/hq-tour/rebuild-source/source-composite.txt'
OUT = ROOT / 'assets/riptide/hq-tour/production'
OUT.mkdir(parents=True, exist_ok=True)

# Decode the approved four-panel visual-reference payload.
raw = base64.b64decode(''.join(SRC.read_text(encoding='utf-8').split()))
src = np.array(Image.open(io.BytesIO(raw)).convert('RGB'))
H, W = src.shape[:2]
boxes = {
    '02': (0, 0, W//2, H//2),
    '03': (W//2, 0, W, H//2),
    '04': (0, H//2, W//2, H),
    '05': (W//2, H//2, W, H),
}

def clean_label(arr):
    # Presentation-board labels occupy the upper-left of each panel. Replace only
    # that overlay with adjacent ceiling texture; no scene geometry is changed.
    h, w = arr.shape[:2]
    y = min(52, h//8)
    x = min(500, w//2)
    sample = arr[y:min(y*2,h), 0:x].copy()
    if sample.shape[0] == 0:
        return arr
    sample = np.array(Image.fromarray(sample).resize((x,y), Image.Resampling.BICUBIC))
    arr[:y, :x] = sample
    return arr

def seam_normalise(arr, width=48):
    a = arr.astype(np.float32)
    width = min(width, arr.shape[1]//10)
    anchor = (a[:,0,:] + a[:,-1,:]) / 2.0
    out = arr.copy()
    for k in range(width):
        t = k / max(1, width-1)
        out[:,k,:] = np.clip((1-t)*anchor + t*a[:,k,:], 0, 255)
        out[:,-1-k,:] = np.clip((1-t)*anchor + t*a[:,-1-k,:], 0, 255)
    return out

report = {'status':'PASS', 'nodes':{}, 'failures':[]}
for node, (x0,y0,x1,y1) in boxes.items():
    panel = src[y0:y1, x0:x1].copy()
    panel = np.array(Image.fromarray(panel).resize((1774,887), Image.Resampling.LANCZOS))
    panel = clean_label(panel)
    panel = seam_normalise(panel)
    desktop = np.array(Image.fromarray(panel).resize((4096,2048), Image.Resampling.LANCZOS))
    edge = ((desktop[:,0,:].astype(np.uint16) + desktop[:,-1,:].astype(np.uint16)) // 2).astype(np.uint8)
    desktop[:,0,:] = edge
    desktop[:,-1,:] = edge
    mobile = np.array(Image.fromarray(desktop).resize((2048,1024), Image.Resampling.LANCZOS))
    dp = OUT / f'node-{node}-4096.webp'
    mp = OUT / f'node-{node}-2048.webp'
    Image.fromarray(desktop).save(dp, 'WEBP', quality=92, method=6)
    Image.fromarray(mobile).save(mp, 'WEBP', quality=90, method=6)
    d = np.array(Image.open(dp).convert('RGB'))
    seam = float(np.abs(d[:,0,:].astype(np.int16) - d[:,-1,:].astype(np.int16)).mean())
    info = {'desktop':[4096,2048], 'mobile':[2048,1024], 'seam_edge_mae':round(seam,3), 'desktop_bytes':dp.stat().st_size, 'mobile_bytes':mp.stat().st_size}
    report['nodes'][node] = info
    if seam > 1.2:
        report['failures'].append(f'Node {node}: seam edge MAE {seam:.3f} > 1.2')

if report['failures']:
    report['status'] = 'FAIL'
(ROOT / 'assets/data/HQ-PANORAMA-REBUILD-QA.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
raise SystemExit(1 if report['failures'] else 0)
