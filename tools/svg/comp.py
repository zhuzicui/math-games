import json,sys,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
from collections import Counter
def run(sh,dil=3,minpx=150):
    sc,samp=json.load(open(f'samp/{sh}.json'))
    W,H,items=json.load(open(f'bb/{sh}.json'))
    bbs={k:b for k,b,*_ in items}
    im=Image.open(f'mask/{sh}.png'); a=np.array(im)[:,:,3]>8
    if dil: a=ndimage.binary_dilation(a,iterations=dil)
    lab,n=ndimage.label(a)
    groups={}
    for k,pts in samp.items():
        v=[lab[y,x] for x,y in pts if 0<=x<lab.shape[1] and 0<=y<lab.shape[0] and lab[y,x]>0]
        if not v: continue
        g=Counter(v).most_common(1)[0][0]; groups.setdefault(g,[]).append(int(k))
    cl=[]
    for g,ks in groups.items():
        ys,xs=np.where(lab==g)
        if len(xs)<minpx: continue
        bb=[xs.min()/sc,ys.min()/sc,(xs.max()+1)/sc,(ys.max()+1)/sc]
        # shrink by dilation
        d=dil/sc; bb=[bb[0]+d,bb[1]+d,bb[2]-d,bb[3]-d]
        cl.append({'ks':sorted(ks),'bb':[round(v,1) for v in bb]})
    cl.sort(key=lambda c:(round(((c['bb'][1]+c['bb'][3])/2)/(H/8)),c['bb'][0]))
    json.dump(cl,open(f'cl/{sh}.json','w'))
    pv=Image.open(f'prev/{sh}.png').convert('RGB'); s=pv.width/W; d=ImageDraw.Draw(pv)
    for i,c in enumerate(cl):
        b=[v*s for v in c['bb']]; d.rectangle(b,outline=(255,0,0)); d.text((b[0]+3,b[1]+3),str(i),fill=(200,0,0))
    pv.save(f'cl/{sh}.png'); print(sh,n,'labels',len(cl),'clusters')
if __name__=='__main__':
    dil=int(sys.argv[1])
    for sh in sys.argv[2:]: run(sh,dil)
