const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const f of process.argv.slice(2)){
 let s=fs.readFileSync(f,'utf8');
 await p.setContent('<body>'+s+'</body>');
 const vb=await p.evaluate(()=>{const s=document.querySelector("svg");const b=s.getBBox();const o=s.viewBox.baseVal;const x0=Math.max(b.x,o.x),y0=Math.max(b.y,o.y),x1=Math.min(b.x+b.width,o.x+o.width),y1=Math.min(b.y+b.height,o.y+o.height);return [x0,y0,x1-x0,y1-y0];});
 const m=Math.max(vb[2],vb[3])*0.004;
 const r=v=>Math.round(v*10)/10;
 const nv=`${r(vb[0]-m)} ${r(vb[1]-m)} ${r(vb[2]+2*m)} ${r(vb[3]+2*m)}`;
 s=s.replace(/viewBox="[^"]*"/,`viewBox="${nv}"`); fs.writeFileSync(f,s);
}
await b.close();})();
