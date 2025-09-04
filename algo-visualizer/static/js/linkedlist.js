// LinkedList UI
const runBtn = document.getElementById('run');
const initialEl = document.getElementById('initial');
const actionEl = document.getElementById('action');
const validxEl = document.getElementById('validx');
const outputEl = document.getElementById('ll-output');

async function postLinked(action, payload){
  const res = await fetch('/api/linkedlist',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({action, payload})});
  return await res.json();
}

runBtn.onclick = async ()=>{
  const initial = (initialEl.value||'').split(',').map(x=>x.trim()).filter(x=>x).map(Number);
  const action = actionEl.value;
  const vi = validxEl.value;
  let payload = {initial};
  if(action.startsWith('insert')) payload.value = Number(vi);
  if(action==='insert_at' || action==='delete_at') payload.index = Number(vi);
  if(action==='search') payload.value = Number(vi);
  const res = await postLinked(action, {initial, ...payload});
  outputEl.innerText = JSON.stringify(res, null, 2);
};