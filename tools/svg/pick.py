import json,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from export import export
def pick(sh,rect,tol=2,hide_big=0.2,extra_ex=lambda b,f:False):
    W,H,items=json.load(open(f'bb/{sh}.json'))
    ks=[];bbs=[]
    for k,b,fill,st,sw,tag in items:
        if (b[2]-b[0])*(b[3]-b[1])>hide_big*W*H or b[2]<=b[0] or b[3]<=b[1]: continue
        if b[0]>=rect[0]-tol and b[1]>=rect[1]-tol and b[2]<=rect[2]+tol and b[3]<=rect[3]+tol and not extra_ex(b,fill):
            ks.append(k); bbs.append(b)
    bb=[min(b[0] for b in bbs),min(b[1] for b in bbs),max(b[2] for b in bbs),max(b[3] for b in bbs)]
    return ks,bb
if __name__=='__main__':
    sh=sys.argv[1]; rects=json.load(open(sys.argv[2])); os.makedirs(f'el/{sh}s',exist_ok=True)
    for name,r in rects.items():
        ks,bb=pick(sh,r); export(sh,ks,bb,f'el/{sh}s/{name}.svg'); print(name,len(ks),bb)
