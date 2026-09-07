"""Adaptive 4:5 crop around the phone box saved by replace_frame.py.
usage: crop45.py <rep.jpg> <out.webp>  — margins: 24% of phone width each side, 6% of height top/bottom."""
import sys, json
from PIL import Image
im=Image.open(sys.argv[1]).convert('RGB'); j=json.load(open(sys.argv[1]+'.json'))
x,y,w,h,W,H=j['x'],j['y'],j['w'],j['h'],j['W'],j['H']
cx,cy=x+w/2,y+h/2
cw=w*1.48; ch=cw*5/4
if ch<h*1.12: ch=h*1.12; cw=ch*4/5
l=max(0,cx-cw/2); t=max(0,cy-ch/2); r=min(W,l+cw); b=min(H,t+ch); l=max(0,r-cw); t=max(0,b-ch)
c=im.crop((int(l),int(t),int(r),int(b))).resize((1100,1375),Image.LANCZOS); c.save(sys.argv[2],quality=88,method=6); print('crop',(int(l),int(t),int(r),int(b)))
