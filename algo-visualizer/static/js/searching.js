// Searching front-end
const barsEl = document.getElementById('bars');
const algoSel = document.getElementById('algo');
const arrayMode = document.getElementById('array-mode');
const customArray = document.getElementById('custom-array');
const btnGen = document.getElementById('generate');
const btnRun = document.getElementById('run');
const targetEl = document.getElementById('target');
const metaEl = document.getElementById('meta');
const resultEl = document.getElementById('result');

let arr = [];

function renderBars(){ barsEl.innerHTML=''; const w = Math.max(6, Math.floor(barsEl.clientWidth / arr.length) - 4);
  arr.forEach((h,i)=>{ const b=document.createElement('div'); b.className='bar'; b.style.height=(h*2)+'px'; b.style.width=w+'px'; b.dataset.index=i; b.title = h; barsEl.appendChild(b); }); }

btnGen.onclick = ()=>{ if(arrayMode.value==='custom' && customArray.value.trim()){ arr = customArray.value.split(',').map(x=>Number(x.trim())).filter(x=>!Number.isNaN(x)); } else if(arrayMode.value==='preset'){ arr = [1,3,5,7,9,11,13]; } else { arr = []; for(let i=0;i<20;i++) arr.push(1+Math.floor(Math.random()*100)); } if(['binary','jump','interpolation'].includes(algoSel.value)) arr.sort((a,b)=>a-b); renderBars(); metaEl.innerText=''; resultEl.innerText=''; }

btnRun.onclick = async ()=>{ const target = Number(targetEl.value); const res = await fetch('/api/search',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({algorithm: algoSel.value, array: arr, target})}); const data = await res.json(); metaEl.innerText = `${data.meta.name} • TC/SC: ${data.meta.tc} / ${data.meta.sc}`; const steps = data.steps || []; for(const s of steps){ if(s.compare){ const i = s.compare[0]; const el = barsEl.querySelector(`[data-index="${i}"]`); if(el){ el.classList.add('compare'); await new Promise(r=>setTimeout(r,120)); el.classList.remove('compare'); } } if(s.found){ resultEl.innerText = 'Found at index: '+s.found; return; } } resultEl.innerText = 'Not found'; }

window.addEventListener('resize', renderBars);