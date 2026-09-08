"""Paste the exact app screen back onto a Higgsfield image generated from a framed phone.
usage: replace_frame.py <generated> <framed_phone_rgba.png> <out.jpg>
Search (scale, rotation, position) for the SCREEN EDGE: score = brightness just
inside the screen boundary minus brightness just outside it (the dark bezel).
That locks the paste to the model's screen instead of the bezel silhouette."""
import sys, os, json, numpy as np
from PIL import Image, ImageFilter
from collections import deque
gen=Image.open(sys.argv[1]).convert('RGB'); fr=Image.open(sys.argv[2]).convert('RGBA')
gen=gen.resize((gen.width*2,gen.height*2),Image.LANCZOS)
gs=np.asarray(gen.convert('L')).astype(float)/255.0
raw=Image.open(os.path.expanduser('~/Desktop/PNG/iPhone 17 Pro/iPhone 17 Pro - Silver - Portrait.png')).convert('RGBA')
fa=np.asarray(raw.split()[3]); hh,ww=fa.shape; hole=(fa==0); seen=np.zeros_like(hole,bool); q=deque([(hh//2,ww//2)]); seen[hh//2,ww//2]=True
while q:
    yy,xx=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=yy+dy,xx+dx
        if 0<=ny<hh and 0<=nx<ww and not seen[ny,nx] and hole[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
screen=Image.fromarray((seen*255).astype('uint8'))
base=gen.width/1536*0.5
def rings(scale,rot,sy=1.0):   # sy: extra vertical stretch — AI phones are rarely drawn at the exact real aspect
    s=screen.resize((int(fr.width*scale),int(fr.height*scale*sy)),Image.BILINEAR).rotate(rot,expand=True,resample=Image.BILINEAR)
    a=np.asarray(s)>127
    e1=np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MinFilter(5)))>127
    e2=np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MinFilter(15)))>127
    d1=np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)))>127
    d2=np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MaxFilter(15)))>127
    rin=e1&~e2; rout=d2&~d1
    skip=float(os.environ.get('TOPSKIP','0'))   # ignore the top N% of the screen edge (dark photo headers)
    if skip>0:
        cut=int(a.shape[0]*skip); rin[:cut,:]=False; rout[:cut,:]=False
    iy,ix=np.where(rin); oy,ox=np.where(rout); return s.size,(iy,ix),(oy,ox)
def score(sz,rin,rout,x,y,sub=1):
    tw,th=sz
    if x<0 or y<0 or x+tw>gen.width or y+th>gen.height: return -9
    iy,ix=rin; oy,ox=rout
    if os.environ.get('MODE')=='bezel':   # dark-bezel only: for screens whose top is a dark photo
        return 1-gs[y+oy[::sub],x+ox[::sub]].mean()
    return gs[y+iy[::sub],x+ix[::sub]].mean()-gs[y+oy[::sub],x+ox[::sub]].mean()
best=None
for scale in np.linspace(base*0.75,base*1.25,11):
    for rot in (-4,-2,0,2,4):
        sz,rin,rout=rings(scale,rot); tw,th=sz
        if tw>=gen.width or th>=gen.height: continue
        for y in range(0,gen.height-th,14):
            for x in range(0,gen.width-tw,14):
                s=score(sz,rin,rout,x,y,9)
                if best is None or s>best[0]: best=(s,x,y,scale,rot)
s,x,y,scale,rot=best
for sc in np.linspace(scale-0.04,scale+0.04,9):
    for r in np.linspace(rot-1.5,rot+1.5,7):
        sz,rin,rout=rings(sc,r)
        for yy in range(y-16,y+17,2):
            for xx in range(x-16,x+17,2):
                s2=score(sz,rin,rout,xx,yy,2)
                if s2>best[0]: best=(s2,xx,yy,sc,r)
s,x,y,scale,rot=best
# aspect pass: keep width, let height breathe ±8% so the paste stops at the drawn bezel top AND bottom
best=(s,x,y,scale,rot,1.0)
for sy in np.linspace(0.92,1.08,17):
    sz,rin,rout=rings(scale,rot,sy)
    for yy in range(y-24,y+25,2):
        for xx in range(x-4,x+5,2):
            s2=score(sz,rin,rout,xx,yy,2)
            if s2>best[0]: best=(s2,xx,yy,scale,rot,sy)
s,x,y,scale,rot,sy=best; print('match score %.3f at x=%d y=%d scale=%.3f rot=%.1f sy=%.3f'%best)
sz=(int(fr.width*scale),int(fr.height*scale*sy))
t=fr.resize(sz,Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
sm=screen.filter(ImageFilter.MaxFilter(5)).resize(sz,Image.BILINEAR).rotate(rot,expand=True,resample=Image.BILINEAR)
out=gen.copy(); out.paste(t,(x,y),sm); out.save(sys.argv[3],quality=93); print('saved',sys.argv[3])
json.dump({'x':x,'y':y,'w':t.width,'h':t.height,'W':out.width,'H':out.height},open(sys.argv[3]+'.json','w'))
