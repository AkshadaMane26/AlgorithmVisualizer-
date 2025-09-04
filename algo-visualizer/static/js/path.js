// Pathfinding, MST, TSP front-end glue
const modeSel = document.getElementById('mode');
const pathControls = document.getElementById('path-controls');
const graphControls = document.getElementById('graph-controls');
const canvas = document.getElementById('grid');
const ctx = canvas.getContext('2d');
const rowsEl = document.getElementById('rows'); const colsEl = document.getElementById('cols');
const makeGridBtn = document.getElementById('make-grid'); const runPathBtn = document.getElementById('run-path');
const graphOutput = document.getElementById('graph-output');

let rows = Number(rowsEl.value); let cols = Number(colsEl.value);
let grid = []; let cellW, cellH; let start = [2,2]; let goal = [rows-3, cols-3];

function buildGrid(){
  rows = Number(rowsEl.value); cols = Number(colsEl.value);
  grid = new Array(rows).fill(0).map(()=> new Array(cols).fill(0));
  cellW = canvas.width / cols; cellH = canvas.height / rows;
  start = [2,2]; goal = [rows-3, cols-3];
  draw();
}

function drawCell(r,c,fill){
  ctx.fillStyle = fill;
  const x = c*cellW, y = r*cellH;
  ctx.fillRect(x+1,y+1,cellW-2,cellH-2);
}

function draw(){
  ctx.clearRect(0,0,canvas.width, canvas.height);
  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      drawCell(r,c, grid[r][c] ? '#3a1b2a' : '#18224f');
    }
  }
  drawCell(start[0], start[1], '#33d17a');
  drawCell(goal[0], goal[1], '#ff6aa2');
}

canvas.addEventListener('click', (e)=>{
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left; const y = e.clientY - rect.top;
  const c = Math.floor(x / cellW); const r = Math.floor(y / cellH);
  if(e.shiftKey){ start = [r,c]; }
  else if(e.altKey){ goal = [r,c]; }
  else { grid[r][c] = grid[r][c] ? 0 : 1; }
  draw();
});

async function runPath(){
  const algo = document.getElementById('path-algo').value;
  const res = await fetch('/api/graph',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({kind: algo, grid, start, goal})});
  const data = await res.json();
  const visited = data.visited || []; const path = data.path || [];
  for(const [r,c] of visited){
    if((r===start[0]&&c===start[1]) || (r===goal[0]&&c===goal[1])) continue;
    drawCell(r,c,'#3556ff');
    await new Promise(res=> setTimeout(res, 6));
  }
  for(const [r,c] of path){
    drawCell(r,c,'#ffd15a');
    await new Promise(res=> setTimeout(res, 18));
  }
  drawCell(start[0], start[1], '#33d17a'); drawCell(goal[0], goal[1], '#ff6aa2');
}

makeGridBtn.onclick = buildGrid;
runPathBtn.onclick = runPath;

modeSel.onchange = ()=>{
  if(modeSel.value === 'path'){ pathControls.style.display='flex'; graphControls.style.display='none'; }
  else { pathControls.style.display='none'; graphControls.style.display='block'; }
};

document.getElementById('run-prim').onclick = async ()=>{
  const nodes = (document.getElementById('nodes').value||'').split(',').map(x=>x.trim()).filter(x=>x).map(Number);
  const edges = (document.getElementById('edges').value||'').split('\\n').map(l=>l.trim()).filter(l=>l).map(l=>{const p=l.split(',').map(x=>Number(x.trim())); return [p[0],p[1],p[2]];});
  const res = await fetch('/api/graph',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({kind:'prim', nodes, edges})});
  const data = await res.json(); graphOutput.innerText = JSON.stringify(data, null, 2);
};

document.getElementById('run-kruskal').onclick = async ()=>{
  const nodes = (document.getElementById('nodes').value||'').split(',').map(x=>x.trim()).filter(x=>x).map(Number);
  const edges = (document.getElementById('edges').value||'').split('\\n').map(l=>l.trim()).filter(l=>l).map(l=>{const p=l.split(',').map(x=>Number(x.trim())); return [p[0],p[1],p[2]];});
  const res = await fetch('/api/graph',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({kind:'kruskal', nodes, edges})});
  const data = await res.json(); graphOutput.innerText = JSON.stringify(data, null, 2);
};

document.getElementById('gen-tsp').onclick = ()=>{
  const n = Number(document.getElementById('tsp-n').value||4);
  const mat = Array.from({length:n}, (_,i)=> Array.from({length:n}, (_,j)=> i===j?0: 1+Math.floor(Math.random()*20)));
  graphOutput.innerText = JSON.stringify(mat, null, 2);
  window._tsp_mat = mat;
};

document.getElementById('run-tsp').onclick = async ()=>{
  const mat = window._tsp_mat;
  const res = await fetch('/api/graph',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({kind:'tsp', dist_matrix: mat})});
  const data = await res.json(); graphOutput.innerText = JSON.stringify(data, null, 2);
};

buildGrid();