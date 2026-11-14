// node zoom.js sheet x0 y0 x1 y1 pxwidth out.png  -> renders region with grid every step units
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [sh,x0,y0,x1,y1,pw,out,step]=process.argv.slice(2);const X0=+x0,Y0=+y0,X1=+x1,Y1=+y1,PW=+pw,ST=+(step||100);
const ph=Math.round(PW*(Y1-Y0)/(X1-X0));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:PW,height:ph}});
let svg=fs.readFileSync(`tag/${sh}.svg`,'utf8').replace(/<\?xml[^>]*>/,'');
await p.setContent('<body style="margin:0;background:#ccc">'+svg+'</body>');
await p.evaluate(([X0,Y0,X1,Y1,PW,ph,ST])=>{const s=document.querySelector('svg');s.setAttribute('viewBox',`${X0} ${Y0} ${X1-X0} ${Y1-Y0}`);s.setAttribute('width',PW);s.setAttribute('height',ph);s.setAttribute('preserveAspectRatio','none');s.style.display='block';
const NS='http://www.w3.org/2000/svg';const g=document.createElementNS(NS,'g');
for(let x=Math.ceil(X0/ST)*ST;x<X1;x+=ST){const l=document.createElementNS(NS,'line');l.setAttribute('x1',x);l.setAttribute('x2',x);l.setAttribute('y1',Y0);l.setAttribute('y2',Y1);l.setAttribute('stroke',x%(ST*5)?'rgba(0,0,255,.25)':'rgba(255,0,0,.6)');l.setAttribute('stroke-width',(X1-X0)/PW);g.appendChild(l);
 if(x%(ST*5)==0){const t=document.createElementNS(NS,'text');t.setAttribute('x',x+3*(X1-X0)/PW);t.setAttribute('y',Y0+14*(X1-X0)/PW);t.setAttribute('font-size',12*(X1-X0)/PW);t.setAttribute('fill','red');t.textContent=x;g.appendChild(t);}}
for(let y=Math.ceil(Y0/ST)*ST;y<Y1;y+=ST){const l=document.createElementNS(NS,'line');l.setAttribute('y1',y);l.setAttribute('y2',y);l.setAttribute('x1',X0);l.setAttribute('x2',X1);l.setAttribute('stroke',y%(ST*5)?'rgba(0,0,255,.25)':'rgba(255,0,0,.6)');l.setAttribute('stroke-width',(X1-X0)/PW);g.appendChild(l);
 if(y%(ST*5)==0){const t=document.createElementNS(NS,'text');t.setAttribute('x',X0+3*(X1-X0)/PW);t.setAttribute('y',y-3*(X1-X0)/PW);t.setAttribute('font-size',12*(X1-X0)/PW);t.setAttribute('fill','red');t.textContent=y;g.appendChild(t);}}
s.appendChild(g);},[X0,Y0,X1,Y1,PW,ph,ST]);
await p.screenshot({path:out});await b.close();})();
