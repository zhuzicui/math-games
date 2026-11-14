import json,sys,os,copy
from lxml import etree
NS='{http://www.w3.org/2000/svg}'
def export(sh,ks,bb,out,margin=0.01,recolor=None):
    t=etree.parse(f'tag/{sh}.svg'); r=t.getroot(); ks=set(map(str,ks))
    for el in list(r.iter('{*}metadata')): el.getparent().remove(el)
    for el in list(r.xpath('//*[@data-k]')):
        if el.get('data-k') not in ks: el.getparent().remove(el)
        else: del el.attrib['data-k']
    changed=True
    while changed:
        changed=False
        for g in list(r.iter(NS+'g')):
            if len(g)==0 and g.getparent() is not None and not any(a.tag==NS+'clipPath' for a in g.iterancestors()):
                g.getparent().remove(g); changed=True
    w=bb[2]-bb[0]; h=bb[3]-bb[1]; m=max(w,h)*margin
    r.set('viewBox',f'{bb[0]-m:.1f} {bb[1]-m:.1f} {w+2*m:.1f} {h+2*m:.1f}')
    for a in ('width','height','id','version','{http://www.w3.org/XML/1998/namespace}space'):
        if a in r.attrib: del r.attrib[a]
    s=etree.tostring(r).decode()
    if recolor: s=recolor(s)
    open(out,'w').write(s)
if __name__=='__main__':
    for sh in sys.argv[1:]:
        cl=json.load(open(f'cl/{sh}.json'))
        os.makedirs(f'el/{sh}',exist_ok=True)
        for i,c in enumerate(cl): export(sh,c['ks'],c['bb'],f'el/{sh}/{i:03d}.svg')
        print(sh,len(cl))
