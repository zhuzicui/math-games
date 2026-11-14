import json,sys,glob,os,numpy as np
from PIL import Image
R='/home/user/math-games/'
def norm(im,n=48):
    im=im.convert('RGBA'); a=np.array(im)
    ys,xs=np.where(a[:,:,3]>40)
    if len(xs)==0: return None,1
    im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    ar=im.width/im.height
    im=im.resize((n,n),Image.LANCZOS)
    a=np.array(im).astype(float)/255
    return a,ar
def score(A,B):
    (a,ara),(b,arb)=A,B
    if a is None or b is None: return 9
    ma=a[:,:,3:]; mb=b[:,:,3:]
    rgb=np.abs(a[:,:,:3]*ma-b[:,:,:3]*mb).mean()
    return rgb+abs(np.log(ara/arb))*0.3
pngs={}
for d in sys.argv[2:]:
    for f in sorted(glob.glob(R+d+'/*.png')): pngs[d+'/'+os.path.basename(f)[:-4]]=norm(Image.open(f))
sheets=sys.argv[1].split(',')
els={}
for sh in sheets:
    for f in sorted(glob.glob(f'elr/{sh}_*.png')):
        im=Image.open(f); els[os.path.basename(f)[:-4]]=(norm(im),norm(im.transpose(Image.FLIP_LEFT_RIGHT)))
res={}
for k,P in pngs.items():
    sc=sorted(((float(min(score(P,e[0]),score(P,e[1]))),n,bool(score(P,e[1])<score(P,e[0]))) for n,e in els.items()))
    res[k]=sc[:3]
    print(k, ' | '.join(f'{n}{"F" if fl else ""} {s:.3f}' for s,n,fl in sc[:3]))
json.dump({k:v[0] for k,v in res.items()},open('match_'+sys.argv[2]+'.json','w'))
