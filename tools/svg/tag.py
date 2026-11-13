import sys,glob,os
from lxml import etree
NS='{http://www.w3.org/2000/svg}'
src,out=sys.argv[1:3]
for f in sorted(glob.glob(src+'/*.svg')):
    t=etree.parse(f); r=t.getroot(); k=0
    for el in r.iter(NS+'path',NS+'image',NS+'rect',NS+'circle',NS+'ellipse',NS+'polygon',NS+'polyline',NS+'line'):
        if any(a.tag in (NS+'clipPath',NS+'defs',NS+'mask',NS+'pattern',NS+'metadata') for a in el.iterancestors()): continue
        el.set('data-k',str(k)); k+=1
    t.write(os.path.join(out,os.path.basename(f)))
    print(os.path.basename(f),k)
