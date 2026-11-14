# Flatten an SVG (from export.py) : bake all transforms into path data, normalise viewBox to max dim S, compact output.
import re,sys,os,math
from lxml import etree
NS='{http://www.w3.org/2000/svg}'
S=1000.0
def mul(a,b): # a*b, matrices as (a,b,c,d,e,f)
    return (a[0]*b[0]+a[2]*b[1], a[1]*b[0]+a[3]*b[1], a[0]*b[2]+a[2]*b[3], a[1]*b[2]+a[3]*b[3], a[0]*b[4]+a[2]*b[5]+a[4], a[1]*b[4]+a[3]*b[5]+a[5])
I=(1,0,0,1,0,0)
def ptf(t):
    m=I
    if not t: return m
    for name,args in re.findall(r'(\w+)\s*\(([^)]*)\)',t):
        v=[float(x) for x in re.split(r'[\s,]+',args.strip()) if x]
        if name=='matrix': n=tuple(v)
        elif name=='translate': n=(1,0,0,1,v[0],v[1] if len(v)>1 else 0)
        elif name=='scale': n=(v[0],0,0,v[1] if len(v)>1 else v[0],0,0)
        elif name=='rotate':
            a=math.radians(v[0]); c,s=math.cos(a),math.sin(a); n=(c,s,-s,c,0,0)
            if len(v)==3: n=mul(mul((1,0,0,1,v[1],v[2]),n),(1,0,0,1,-v[1],-v[2]))
        else: raise Exception(name)
        m=mul(m,n)
    return m
def ap(m,x,y): return (m[0]*x+m[2]*y+m[4], m[1]*x+m[3]*y+m[5])
TOK=re.compile(r'[MmLlHhVvCcSsQqTtZzAa]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')
def parse(d):
    toks=TOK.findall(d); i=0; cmd=None; out=[]; cx=cy=sx=sy=0
    def num():
        nonlocal i; v=float(toks[i]); i+=1; return v
    while i<len(toks):
        if toks[i].isalpha(): cmd=toks[i]; i+=1
        elif cmd is None: raise Exception('bad')
        c=cmd; rel=c.islower(); C=c.upper()
        if C=='Z': out.append(('Z',)); cx,cy=sx,sy; continue
        if C=='M':
            x,y=num(),num()
            if rel: x+=cx;y+=cy
            out.append(('M',x,y)); cx,cy=sx,sy=x,y; cmd='l' if rel else 'L'; continue
        if C=='L':
            x,y=num(),num()
            if rel: x+=cx;y+=cy
            out.append(('L',x,y)); cx,cy=x,y; continue
        if C=='H':
            x=num(); x=x+cx if rel else x; out.append(('L',x,cy)); cx=x; continue
        if C=='V':
            y=num(); y=y+cy if rel else y; out.append(('L',cx,y)); cy=y; continue
        if C=='C':
            p=[num() for _ in range(6)]
            if rel: p=[p[j]+(cx if j%2==0 else cy) for j in range(6)]
            out.append(('C',*p)); cx,cy=p[4],p[5]; continue
        if C=='S':
            p=[num() for _ in range(4)]
            if rel: p=[p[j]+(cx if j%2==0 else cy) for j in range(4)]
            prev=out[-1] if out else None
            if prev and prev[0]=='C': x1,y1=2*cx-prev[3],2*cy-prev[4]
            else: x1,y1=cx,cy
            out.append(('C',x1,y1,*p)); cx,cy=p[2],p[3]; continue
        if C=='Q':
            p=[num() for _ in range(4)]
            if rel: p=[p[j]+(cx if j%2==0 else cy) for j in range(4)]
            out.append(('Q',*p)); cx,cy=p[2],p[3]; continue
        raise Exception('unsupported '+C)
    return out
def fmt(v,dec):
    s=f'{v:.{dec}f}' if dec else str(int(round(v)))
    if '.' in s: s=s.rstrip('0').rstrip('.')
    if s.startswith('0.'): s=s[1:]
    elif s.startswith('-0.'): s='-'+s[2:]
    if s in ('-0',''): s='0'
    return s
def join(nums):
    o=''
    for s in nums:
        if o and not (s.startswith('-') or (s.startswith('.') and ('.' in o.split(' ')[-1].split('-')[-1] if o else False))): o+=' '
        o+=s
    return o
def emit(segs,m,dec):
    q=10**dec
    R=lambda v: round(v*q)/q
    out=[];cx=cy=0;sx=sy=0;last=None
    for s in segs:
        if s[0]=='Z': out.append('z'); cx,cy=sx,sy; last='z'; continue
        pts=[ap(m,s[j],s[j+1]) for j in range(1,len(s),2)]
        pts=[(R(x),R(y)) for x,y in pts]
        if s[0]=='M':
            (x,y),=pts; out.append('m'+join([fmt(x-cx,dec),fmt(y-cy,dec)])); cx,cy=sx,sy=x,y; last='l'; continue
        if s[0]=='L':
            (x,y),=pts; dx,dy=x-cx,y-cy
            if abs(dx)<1e-9 and abs(dy)<1e-9: continue
            if abs(dy)<1e-9: out.append('h'+fmt(dx,dec)); last='h'
            elif abs(dx)<1e-9: out.append('v'+fmt(dy,dec)); last='v'
            else:
                t=join([fmt(dx,dec),fmt(dy,dec)]); out.append(('' if last=='l' else 'l')+(' ' if last=='l' and not t.startswith('-') else '')+t); last='l'
            cx,cy=x,y; continue
        if s[0] in 'CQ':
            t=join([fmt(v-(cx if k%2==0 else cy),dec) for k,v in enumerate([c for p in pts for c in p])])
            L=s[0].lower(); out.append(('' if last==L else L)+(' ' if last==L and not t.startswith('-') else '')+t); last=L
            cx,cy=pts[-1]; continue
    return ''.join(out)
def style_of(el):
    st={}
    for k in ('fill','stroke','stroke-width','fill-rule','opacity','fill-opacity','stroke-opacity','stroke-linecap','stroke-linejoin','stroke-miterlimit'):
        if el.get(k) is not None: st[k]=el.get(k)
    if el.get('style'):
        for kv in el.get('style').split(';'):
            if ':' in kv: k,v=kv.split(':',1); st[k.strip()]=v.strip()
    return st
def flatten(src,dst,S=S,dec=0,angle=0):
    r=etree.parse(src).getroot()
    vb=[float(v) for v in r.get('viewBox').split()]
    sc=S/max(vb[2],vb[3]); base=(sc,0,0,sc,-vb[0]*sc,-vb[1]*sc)
    if angle:
        a=math.radians(angle); c,s_=math.cos(a),math.sin(a); cx,cy=vb[2]*sc/2,vb[3]*sc/2
        base=mul(mul(mul((1,0,0,1,cx,cy),(c,s_,-s_,c,0,0)),(1,0,0,1,-cx,-cy)),base)
    W_,H_=vb[2]*sc,vb[3]*sc
    ids={el.get('id'):el for el in r.iter() if el.get('id')}
    defs=[]; body=[]; nid=[0]
    def newid():
        nid[0]+=1; return 'c'+str(nid[0])
    def walk(el,m,inh,clip):
        tag=etree.QName(el).localname
        if tag in ('defs','clipPath','metadata','linearGradient','radialGradient','title','desc'): return
        m=mul(m,ptf(el.get('transform')))
        st=dict(inh); st.update({k:v for k,v in style_of(el).items()})
        cl=clip
        if el.get('clip-path'):
            cid=re.search(r'#([^)]+)',el.get('clip-path')).group(1); cp=ids[cid]
            d=''
            for ch in cp:
                if etree.QName(ch).localname=='path':
                    d+=emit(parse(ch.get('d')),mul(m,ptf(ch.get('transform'))),dec+1)
            i=newid(); defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
            cl=(clip or [])+[i]
        if tag=='g':
            for ch in el: walk(ch,m,{k:v for k,v in st.items() if k not in ('opacity',)} if False else st,cl)
            return
        if tag!='path': raise Exception('tag '+tag)
        d=emit(parse(el.get('d')),m,dec)
        if not d: return
        a=[]
        fill=st.get('fill','#000')
        if fill.startswith('url('):
            gid=re.search(r'#([^)]+)',fill).group(1); g=ids[gid]
            gm=mul(m,ptf(g.get('gradientTransform')))
            i=newid(); gtag=etree.QName(g).localname
            if g.get('gradientUnits')!='userSpaceOnUse': raise Exception('grad units')
            stops=''.join(f'<stop offset="{float(s.get("offset")):.3g}" stop-color="{style_of(s).get("stop-color")}"'+(f' stop-opacity="{style_of(s).get("stop-opacity")}"' if style_of(s).get('stop-opacity') not in (None,'1') else '')+'/>' for s in g)
            if not stops and g.get('{http://www.w3.org/1999/xlink}href'):
                g2=ids[g.get('{http://www.w3.org/1999/xlink}href')[1:]]
                stops=''.join(f'<stop offset="{float(s.get("offset")):.3g}" stop-color="{style_of(s).get("stop-color")}"'+(f' stop-opacity="{style_of(s).get("stop-opacity")}"' if style_of(s).get('stop-opacity') not in (None,'1') else '')+'/>' for s in g2)
            gt='matrix('+' '.join(f'{v:.6g}' for v in gm)+')'
            attrs=' '.join(f'{k}="{g.get(k)}"' for k in ('x1','y1','x2','y2','cx','cy','r','fx','fy','spreadMethod') if g.get(k) is not None)
            defs.append(f'<{gtag} id="{i}" gradientUnits="userSpaceOnUse" {attrs} gradientTransform="{gt}">{stops}</{gtag}>')
            fill=f'url(#{i})'
        if fill!='#000' and fill!='#000000' and fill!='black': a.append(f'fill="{fill}"')
        elif fill in ('#000','#000000','black'): pass
        for k in ('fill-rule','fill-opacity','opacity','stroke','stroke-opacity','stroke-linecap','stroke-linejoin','stroke-miterlimit'):
            v=st.get(k)
            if v is None: continue
            if (k,v) in (('fill-rule','nonzero'),('fill-opacity','1'),('opacity','1'),('stroke','none'),('stroke-opacity','1'),('stroke-linecap','butt'),('stroke-linejoin','miter'),('stroke-miterlimit','4'),('stroke-miterlimit','10')): continue
            if k.startswith('stroke-') and st.get('stroke','none')=='none': continue
            a.append(f'{k}="{v}"')
        if st.get('stroke','none')!='none':
            sw=float(re.sub('[a-z]','',st.get('stroke-width','1')))*math.sqrt(abs(m[0]*m[3]-m[1]*m[2]))
            a.append(f'stroke-width="{sw:.3g}"')
        for c in (cl or []): pass
        p=f'<path d="{d}"'+(' '+' '.join(a) if a else '')+'/>'
        if cl:
            p=''.join(f'<g clip-path="url(#{c})">' for c in cl)+p+'</g>'*len(cl)
        body.append(p)
    for ch in r: walk(ch,base,{},None)
    # merge consecutive identical clip wrappers
    out=[];prev=None
    for p in body:
        mm=re.match(r'((?:<g clip-path="url\(#\w+\)">)+)(.*?)((?:</g>)+)$',p)
        if mm and prev and prev[0]==mm.group(1): prev[1].append(mm.group(2)); continue
        if prev: out.append(prev[0]+''.join(prev[1])+prev[2]); prev=None
        if mm: prev=[mm.group(1),[mm.group(2)],mm.group(3)]
        else: out.append(p)
    if prev: out.append(prev[0]+''.join(prev[1])+prev[2])
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(W_,1)} {fmt(H_,1)}">'+(('<defs>'+''.join(defs)+'</defs>') if defs else '')+''.join(out)+'</svg>\n'
    # dedupe identical clipPaths
    open(dst,'w').write(svg)
if __name__=='__main__':
    import json
    src,dst=sys.argv[1:3]; rot=json.load(open('rot.json')) if os.path.exists('rot.json') else {}
    for root,_,fs in os.walk(src):
        for f in fs:
            if f.endswith('.svg'):
                o=os.path.join(dst,os.path.relpath(root,src),f); os.makedirs(os.path.dirname(o),exist_ok=True); flatten(os.path.join(root,f),o,angle=-rot.get(os.path.relpath(os.path.join(root,f),src)[:-4],0))
