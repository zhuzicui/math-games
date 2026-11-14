const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const [src,out]=process.argv.slice(2);
for(const f of fs.readdirSync(src).filter(f=>f.endsWith('.svg'))){
 const svg=fs.readFileSync(path.join(src,f),'utf8').replace(/<\?xml[^>]*>/,'');
 await p.setContent('<body style="margin:0">'+svg+'</body>');
 const res=await p.evaluate(()=>{
  const s=document.querySelector('svg'); const vb=s.viewBox.baseVal;
  s.setAttribute('width',vb.width); s.setAttribute('height',vb.height); s.style.display='block';
  const o=s.getBoundingClientRect();
  function clipBox(el){ // intersect ancestors' clip-path boxes
    let box=null; let a=el;
    while(a && a!==s){
      const cp=a.getAttribute && a.getAttribute('clip-path');
      if(cp){ const id=cp.match(/#([^)]+)/)[1]; const c=document.getElementById(id);
        const m0=a.getScreenCTM();
        for(const ch of c.children){ if(!ch.getBBox) continue; const bb=ch.getBBox(); let m=m0;
          if(ch.transform && ch.transform.baseVal.numberOfItems){ m=m0.multiply(ch.transform.baseVal.consolidate().matrix);} 
          const pts=[[bb.x,bb.y],[bb.x+bb.width,bb.y],[bb.x,bb.y+bb.height],[bb.x+bb.width,bb.y+bb.height]].map(([x,y])=>{const P=new DOMPoint(x,y).matrixTransform(m);return [P.x-o.left,P.y-o.top]});
          const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]); const r=[Math.min(...xs),Math.min(...ys),Math.max(...xs),Math.max(...ys)];
          box=box?[Math.max(box[0],r[0]),Math.max(box[1],r[1]),Math.min(box[2],r[2]),Math.min(box[3],r[3])]:r; }
      }
      a=a.parentNode;
    }
    return box;
  }
  return [vb.width,vb.height,[...s.querySelectorAll('[data-k]')].map(el=>{
    const r=el.getBoundingClientRect(); let bx=[r.left-o.left,r.top-o.top,r.right-o.left,r.bottom-o.top];
    const c=clipBox(el); if(c) bx=[Math.max(bx[0],c[0]),Math.max(bx[1],c[1]),Math.min(bx[2],c[2]),Math.min(bx[3],c[3])];
    const cs=getComputedStyle(el);
    return [+el.dataset.k,bx.map(v=>Math.round(v*10)/10),cs.fill,cs.stroke,cs.strokeWidth,el.tagName];
  })];
 });
 fs.writeFileSync(path.join(out,f.replace('.svg','.json')),JSON.stringify(res));
 console.log(f,res[2].length);
}
await b.close();})();
