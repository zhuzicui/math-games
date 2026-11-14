const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1200}});
const [S,out,...files]=process.argv.slice(2);
const html=path.resolve('_rbox.html');
for(const f of files){
 const abs=path.resolve(f);
 fs.writeFileSync(html,`<body style="margin:0;background:transparent"><img id=i style="width:${S}px;height:${S}px;object-fit:contain;display:block" src="${path.relative(path.dirname(html),abs)}"></body>`);
 await p.goto('file://'+html);
 await p.waitForFunction(()=>document.getElementById('i').complete);
 const name=path.basename(path.dirname(abs))+'_'+path.basename(abs,'.svg')+'.png';
 await (await p.$('#i')).screenshot({path:path.join(out,name),omitBackground:true});
}
await b.close();})();
