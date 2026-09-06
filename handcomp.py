"""Composite an app screenshot onto the green screen of a hand-held phone photo.
usage: handcomp.py <photo> <screen> <out>
1. green mask -> largest blob
2. fit a straight line to each of the four edges (robust least squares over the
   middle 80% of the edge), intersect them -> exact corners even when the AI drew
   a status bar / island inside the green
3. PIL perspective warp; mask = quad ∩ dilated blob (keeps the rounded corners,
   fills text holes)"""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
from collections import deque
photo=Image.open(sys.argv[1]).convert('RGB'); screen=Image.open(sys.argv[2]).convert('RGB')
a=np.asarray(photo).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
mask=(g>100)&(g>r*1.3)&(g>b*1.3)
Hh,Ww=mask.shape; seen=np.zeros_like(mask,bool); best=None
ys,xs=np.where(mask)
for y0,x0 in zip(ys[::500],xs[::500]):
    if seen[y0,x0]: continue
    q=deque([(y0,x0)]); seen[y0,x0]=True; pts=[]
    while q:
        y,x=q.popleft(); pts.append((y,x))
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<Hh and 0<=nx<Ww and mask[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
    if best is None or len(pts)>len(best): best=pts
blob=np.zeros_like(mask); by,bx=zip(*best); blob[list(by),list(bx)]=True
rows=np.where(blob.any(1))[0]; cols=np.where(blob.any(0))[0]
r0,r1=rows.min(),rows.max(); c0,c1=cols.min(),cols.max()
def fit(points):  # points: (x,y) -> line ax+by=c via total least squares
    P=np.array(points,float); m=P.mean(0); u,s,vt=np.linalg.svd(P-m); n=vt[1]; return n[0],n[1],n@m
def robust(points):
    a_,b_,c_=fit(points); P=np.array(points,float); d=np.abs(P@[a_,b_]-c_); keep=d<np.percentile(d,80); return fit(P[keep])
# left/right edges: leftmost/rightmost green per row, middle 70% of rows
rr=[y for y in range(r0,r1+1) if blob[y].any()]; rr=rr[int(len(rr)*.15):int(len(rr)*.85)]
L=robust([(np.where(blob[y])[0].min(),y) for y in rr]); R=robust([(np.where(blob[y])[0].max(),y) for y in rr])
cc=[x for x in range(c0,c1+1) if blob[:,x].any()]; cc=cc[int(len(cc)*.15):int(len(cc)*.85)]
T=robust([(x,np.where(blob[:,x])[0].min()) for x in cc]); B=robust([(x,np.where(blob[:,x])[0].max()) for x in cc])
def X(l1,l2):
    A=np.array([[l1[0],l1[1]],[l2[0],l2[1]]]); return np.linalg.solve(A,[l1[2],l2[2]])
tl,tr,br,bl=X(T,L),X(T,R),X(B,R),X(B,L)
dst=np.array([tl,tr,br,bl]); print('quad',dst.astype(int).tolist())
sw,sh=screen.size; src=np.array([[0,0],[sw,0],[sw,sh],[0,sh]],float)
M=[]
for (x,y),(u,v) in zip(dst,src):
    M.append([x,y,1,0,0,0,-u*x,-u*y]); M.append([0,0,0,x,y,1,-v*x,-v*y])
coef=np.linalg.solve(np.array(M,float),src.reshape(8))
warped=screen.transform(photo.size,Image.PERSPECTIVE,coef.tolist(),Image.BICUBIC)
# --- key: the green blob IS the screen shape (rounded corners and all). The only
# fix-ups are holes the AI painted inside the green (a fake status bar, glare):
# fill any hole that does not touch the blob's outer edge, except a large one
# near the top centre — the phone's real Dynamic Island, which stays a hole.
quad=Image.new('L',photo.size,0); ImageDraw.Draw(quad).polygon([tuple(p) for p in dst],fill=255)
Q=np.asarray(quad)>0
inner=np.asarray(quad.filter(ImageFilter.MinFilter(9)))>0     # quad eroded 4px: anything outside this touches the edge
holes=Q&~blob; hseen=np.zeros_like(holes,bool); fill=np.zeros_like(holes,bool)
hy,hx=np.where(holes); qh=dst[:,1].max()-dst[:,1].min(); qtop=dst[:,1].min(); qcx=dst[:,0].mean(); qw=dst[:,0].max()-dst[:,0].min()
for y0,x0 in zip(hy[::150],hx[::150]):
    if hseen[y0,x0]: continue
    q=deque([(y0,x0)]); hseen[y0,x0]=True; pts=[]
    while q:
        y,x=q.popleft(); pts.append((y,x))
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<Hh and 0<=nx<Ww and holes[ny,nx] and not hseen[ny,nx]: hseen[ny,nx]=True; q.append((ny,nx))
    P=np.array(pts); cy,cx=P[:,0].mean(),P[:,1].mean()
    touches_edge=(~inner[P[:,0],P[:,1]]).any()
    is_island=len(pts)>1500 and cy<qtop+qh*0.09 and abs(cx-qcx)<qw*0.2
    if touches_edge or is_island:
        if is_island: print('island hole kept',len(pts))
        continue
    fill[P[:,0],P[:,1]]=True
final=blob|fill
m=Image.fromarray((final*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
out=Image.composite(warped,photo,m); out.save(sys.argv[3],quality=92); print('saved',sys.argv[3])
