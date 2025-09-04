// Sorting front-end glue
const barsEl = document.getElementById('bars');
const algoSel = document.getElementById('algo');
const sizeEl = document.getElementById('size');
const speedEl = document.getElementById('speed');
const btnGen = document.getElementById('generate');
const btnPlay = document.getElementById('play');
const btnPause = document.getElementById('pause');
const btnStep = document.getElementById('step');
const arrayMode = document.getElementById('array-mode');
const customArray = document.getElementById('custom-array');
const metaEl = document.getElementById('meta');
const dryrunEl = document.getElementById('dryrun');

let arr = [];
let steps = [];
let stepIndex = 0; let playing=false; let timer=null;

function randArr(n){ const a=[]; for(let i=0;i<n;i++) a.push(1+Math.floor(Math.random()*100)); return a }

function renderBars(){ barsEl.innerHTML=''; const w = Math.max(6, Math.floor(barsEl.clientWidth / arr.length) - 4);
  arr.forEach((h,i)=>{ const b=document.createElement('div'); b.className='bar'; b.style.height=(h*2)+'px'; b.style.width=w+'px'; b.dataset.index=i; b.title = h; barsEl.appendChild(b); }); }

function applyStep(s){ if(s.compare){ highlightCompare(s.compare[0], s.compare[1]) } if(s.swap){ domSwap(s.swap[0], s.swap[1]) } if(s.set){ domSet(s.set[0], s.set[1]); } }

function highlightCompare(i,j){ const bi = barsEl.querySelector(`[data-index="${i}"]`); const bj = barsEl.querySelector(`[data-index="${j}"]`);
  if(bi) bi.classList.add('compare'); if(bj) bj.classList.add('compare');
  setTimeout(()=>{ if(bi) bi.classList.remove('compare'); if(bj) bj.classList.remove('compare'); }, speed()) }

function domSet(i,val){ arr[i]=val; const b = barsEl.querySelector(`[data-index="${i}"]`); if(!b) return; b.style.height=(val*2)+'px'; b.title=val }

function domSwap(i,j){ const bi = barsEl.querySelector(`[data-index="${i}"]`); const bj = barsEl.querySelector(`[data-index="${j}"]`);
  if(!bi || !bj) return; bi.classList.add('swap'); bj.classList.add('swap');
  const dx = bj.offsetLeft - bi.offsetLeft;
  bi.style.transform = `translateX(${dx}px)`; bj.style.transform = `translateX(${-dx}px)`;
  setTimeout(()=>{ bi.classList.remove('swap'); bj.classList.remove('swap'); bi.style.transform=''; bj.style.transform=''; 
    if (j>i) barsEl.insertBefore(bj, bi); else barsEl.insertBefore(bi, bj);
    [...barsEl.children].forEach((el,idx)=> el.dataset.index = idx);
    const tmp = arr[i]; arr[i]=arr[j]; arr[j]=tmp;
  }, Math.max(80, speed())); }

function speed(){ return Math.max(20, 420 - Number(speedEl.value)); }

async function fetchSteps(){
  const res = await fetch('/api/sort',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({algorithm: algoSel.value, array: arr})});
  const data = await res.json();
  steps = data.steps || []; stepIndex = 0;
  metaEl.innerText = `${data.meta.name} • TC/SC: ${data.meta.tc} / ${data.meta.sc}`;
  dryrunEl.innerText = (data.dryrun||[]).join('\\n');
}

function playLoop(){ if(stepIndex >= steps.length){ playing=false; return } applyStep(steps[stepIndex++]); timer = setTimeout(()=>{ if(playing) playLoop(); }, speed()); }

btnGen.onclick = ()=>{ if(arrayMode.value==='custom' && customArray.value.trim()){ arr = customArray.value.split(',').map(x=>Number(x.trim())).filter(x=>!Number.isNaN(x)); } else if(arrayMode.value==='preset'){ arr = [50,40,30,20,10,5,60,70,15]; } else { arr = randArr(Number(sizeEl.value)); } renderBars(); steps=[]; stepIndex=0; metaEl.innerText=''; dryrunEl.innerText=''; }

btnPlay.onclick = async ()=>{ if(steps.length===0) await fetchSteps(); playing=true; playLoop(); }
btnPause.onclick = ()=>{ playing=false; clearTimeout(timer); }
btnStep.onclick = async ()=>{ if(steps.length===0) await fetchSteps(); if(stepIndex < steps.length) applyStep(steps[stepIndex++]); }

window.addEventListener('resize', renderBars);
arr = randArr(Number(sizeEl.value)); renderBars();