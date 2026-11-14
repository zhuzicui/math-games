const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:2000}});
const sheets=process.argv.slice(2);
for(const sh of sheets){
 const svg=fs.readFileSync(`tag/${sh}.svg`,'utf8').replace(/<\?xml[^>]*>/,'');
 const hide=JSON.parse(fs.readFileSync(`samp/${sh}.hide.json`,'utf8'));
 await p.setContent('<body style="margin:0;background:transparent">'+svg+'</body>');
 const res=await p.evaluate((hide)=>{
  const s=document.querySelector('svg'); const vb=s.viewBox.baseVal; const sc=2000/Math.max(vb.width,vb.height);
  s.setAttribute('width',vb.width*sc); s.setAttribute('height',vb.height*sc); s.style.display='block';
  for(const k of hide){ const e=document.querySelector(`[data-k="${k}"]`); if(e) e.style.display='none'; }
  const o=s.getBoundingClientRect(); const out={};
  for(const el of s.querySelectorAll('[data-k]')){
    if(el.style.display==='none') continue;
    const m=el.getScreenCTM(); const pts=[];
    if(el.getTotalLength){ let L=0; try{L=el.getTotalLength();}catch(e){}
      const N=24; for(let i=0;i<N;i++){ try{const q=el.getPointAtLength(L*i/N).matrixTransform(m); pts.push([Math.round(q.x-o.left),Math.round(q.y-o.top)]);}catch(e){} } }
    const r=el.getBoundingClientRect(); pts.push([Math.round((r.left+r.right)/2-o.left),Math.round((r.top+r.bottom)/2-o.top)]);
    out[el.dataset.k]=pts;
  }
  return [sc,out];
 },hide);
 await p.screenshot({path:`mask/${sh}.png`,omitBackground:true,fullPage:true});
 fs.writeFileSync(`samp/${sh}.json`,JSON.stringify(res)); console.log(sh,Object.keys(res[1]).length);
}
await b.close();})();
