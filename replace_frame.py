"""Put the exact framed phone back on top of a Higgsfield image generated from it.
usage: replace_frame.py <generated> <framed_phone_rgba.png> <out.jpg>
Coarse-to-fine search over scale, rotation and position for where the model
put the phone (score = darkness of the bezel ring), then paste the pristine
framed screenshot there."""
import sys, numpy as np
from PIL import Image, ImageFilter
gen=Image.open(sys.argv[1]).convert('RGB'); fr=Image.open(sys.argv[2]).convert('RGBA')
# upscale the generated photo 2x so the pasted frame isn't sharper than its surroundings by a mile
gen=gen.resize((gen.width*2,gen.height*2),Image.LANCZOS)
# the phone was placed at half the frame size on a 1536-wide canvas; the model keeps roughly that layout
base=gen.width/1536*0.5
gs=np.asarray(gen.convert('L')).astype(float)/255.0
alpha=fr.split()[3]
def ring_pts(scale,rot):
    t=fr.resize((int(fr.width*scale),int(fr.height*scale)),Image.BILINEAR).rotate(rot,expand=True,resample=Image.BILINEAR)
    a=np.asarray(t.split()[3])>127
    inner=np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MinFilter(7)))>127
    inner2=np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MinFilter(23)))>127
    ring=inner&~inner2; ry,rx=np.where(ring); return t,ry,rx
def score(ry,rx,x,y,tw,th):
    if x<0 or y<0 or x+tw>gen.width or y+th>gen.height: return -1
    return 1-gs[y+ry,x+rx].mean()
best=None
for scale in np.linspace(base*0.8,base*1.2,9):
    for rot in (-6,-4,-2,0,2,4,6):
        t,ry,rx=ring_pts(scale,rot); tw,th=t.size
        if tw>=gen.width or th>=gen.height or len(ry)==0: continue
        sub=slice(None,None,7)
        for y in range(0,gen.height-th,10):
            for x in range(0,gen.width-tw,10):
                s=score(ry[sub],rx[sub],x,y,tw,th)
                if best is None or s>best[0]: best=(s,x,y,scale,rot)
s,x,y,scale,rot=best
# refine
for sc in np.linspace(scale-0.05,scale+0.05,11):
    for r in np.linspace(rot-2,rot+2,9):
        t,ry,rx=ring_pts(sc,r); tw,th=t.size
        for yy in range(y-12,y+13,3):
            for xx in range(x-12,x+13,3):
                s2=score(ry,rx,xx,yy,tw,th)
                if s2>best[0]: best=(s2,xx,yy,sc,r)
s,x,y,scale,rot=best; print('match score %.3f at x=%d y=%d scale=%.3f rot=%.1f'%best)
t=fr.resize((int(fr.width*scale),int(fr.height*scale)),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
# Paste ONLY the screen (the frame's transparent screen area), not the bezel — so the
# generated bezel and any fingers wrapped over it stay, and the phone reads as held.
from collections import deque
import os
raw=Image.open(os.path.expanduser('~/Desktop/PNG/iPhone 17 Pro/iPhone 17 Pro - Silver - Portrait.png')).convert('RGBA')
fa=np.asarray(raw.split()[3]); hh,ww=fa.shape; hole=(fa==0); seen=np.zeros_like(hole,bool); q=deque([(hh//2,ww//2)]); seen[hh//2,ww//2]=True
while q:
    yy,xx=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=yy+dy,xx+dx
        if 0<=ny<hh and 0<=nx<ww and not seen[ny,nx] and hole[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
screen_mask=Image.fromarray((seen*255).astype('uint8')).filter(ImageFilter.MaxFilter(3))
sm=screen_mask.resize(t.size if rot==0 else (int(fr.width*scale),int(fr.height*scale)),Image.BILINEAR).rotate(rot,expand=True,resample=Image.BILINEAR)
out=gen.copy(); out.paste(t,(x,y),sm); out.save(sys.argv[3],quality=93); print('saved',sys.argv[3])
