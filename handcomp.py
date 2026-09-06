"""Composite an app screenshot onto the green screen of a hand-held phone photo.
usage: handcomp.py <photo.png> <screen.png> <out.png>
Green detection -> quad corners -> PIL perspective transform -> paste with the green mask."""
import sys, numpy as np
from PIL import Image, ImageFilter
photo=Image.open(sys.argv[1]).convert('RGB'); screen=Image.open(sys.argv[2]).convert('RGB')
a=np.asarray(photo).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
mask=(g>110)&(g>r*1.35)&(g>b*1.35)
# keep the largest connected blob (the screen), drop stray greens
from collections import deque
H,W=mask.shape; seen=np.zeros_like(mask,bool); best=None
ys,xs=np.where(mask)
for y0,x0 in zip(ys[::400],xs[::400]):
    if seen[y0,x0]: continue
    q=deque([(y0,x0)]); seen[y0,x0]=True; pts=[]
    while q:
        y,x=q.popleft(); pts.append((y,x))
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and mask[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
    if best is None or len(pts)>len(best): best=pts
blob=np.zeros_like(mask); by,bx=zip(*best); blob[list(by),list(bx)]=True
ys,xs=np.where(blob); P=np.stack([xs,ys],1).astype(float)
# quad corners by extremes of x+y and x-y
tl=P[np.argmin(P[:,0]+P[:,1])]; br=P[np.argmax(P[:,0]+P[:,1])]; tr=P[np.argmax(P[:,0]-P[:,1])]; bl=P[np.argmin(P[:,0]-P[:,1])]
dst=np.array([tl,tr,br,bl]); print('quad',dst.astype(int).tolist(),'blob px',len(best))
sw,sh=screen.size; src=np.array([[0,0],[sw,0],[sw,sh],[0,sh]],float)
# PIL PERSPECTIVE maps OUTPUT (x,y) -> INPUT; solve for coefficients from dst->src
def coeffs(pa,pb):
    M=[]
    for (x,y),(u,v) in zip(pa,pb):
        M.append([x,y,1,0,0,0,-u*x,-u*y]); M.append([0,0,0,x,y,1,-v*x,-v*y])
    A=np.array(M,float); B=np.array(pb,float).reshape(8)
    return np.linalg.solve(A,B)
c=coeffs(dst,src)
warped=screen.transform(photo.size,Image.PERSPECTIVE,c.tolist(),Image.BICUBIC)
m=Image.fromarray((blob*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
# subtle screen glass: darken edges slightly toward the photo's luminance
out=Image.composite(warped,photo,m)
out.save(sys.argv[3],quality=92); print('saved',sys.argv[3],out.size)
