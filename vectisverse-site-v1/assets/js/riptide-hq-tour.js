(()=>{'use strict';
const cfg=window.RIPTIDE_HQ_TOUR;
if(!cfg||!window.pannellum)return;
const viewport=document.querySelector('[data-tour-viewport]');
const pano=document.querySelector('[data-panorama]');
const loading=document.querySelector('[data-loading]');
const live=document.querySelector('[data-live]');
const locationEl=document.querySelector('[data-location]');
const quarterEl=document.querySelector('[data-quarter]');
const reset=document.querySelector('[data-reset]');
const moves=[...document.querySelectorAll('[data-move]')];
const quarters=[...document.querySelectorAll('[data-q]')];
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
const state={currentNode:cfg.startNode,yaw:0,pitch:cfg.defaultPitch,fov:cfg.defaultFov,transitioning:false,viewer:null,loadedNodes:new Set()};
const node=id=>cfg.nodes.find(n=>n.id===id);
const asset=n=>matchMedia('(max-width:760px)').matches?n.mobile:n.image;
const clamp=(v,min,max)=>Math.min(max,Math.max(min,v));
function updateUI(){
  const n=node(state.currentNode);
  locationEl.textContent=n.label;
  quarterEl.textContent=n.quarter;
  viewport.setAttribute('aria-label',`Riptide HQ virtual tour — ${n.label}`);
  quarters.forEach(q=>q.classList.toggle('is-current',q.dataset.q===n.quarter));
  moves.forEach(b=>{
    const target=b.dataset.move==='next'?n.next:n.previous;
    b.hidden=!target;
    if(target){const t=node(target);b.setAttribute('aria-label',`${b.dataset.move==='next'?'Move forward to':'Move back to'} ${t.label}`)}
  });
}
function preload(id){
  if(!id||state.loadedNodes.has(id))return;
  const img=new Image();
  img.src=asset(node(id));
  img.onload=()=>state.loadedNodes.add(id);
}
function captureView(){
  if(!state.viewer)return;
  state.yaw=state.viewer.getYaw();
  state.pitch=state.viewer.getPitch();
  state.fov=state.viewer.getHfov();
}
function destroyViewer(){
  if(state.viewer){state.viewer.destroy();state.viewer=null;}
  pano.innerHTML='';
}
function buildViewer(n,{resetView=false,announce=true}={}){
  if(resetView){state.yaw=0;state.pitch=0;state.fov=cfg.defaultFov;}
  const src=asset(n);
  state.viewer=pannellum.viewer(pano,{
    type:'equirectangular',panorama:src,autoLoad:true,showControls:false,
    yaw:state.yaw,pitch:state.pitch,hfov:state.fov,
    minPitch:cfg.pitchLimits[0],maxPitch:cfg.pitchLimits[1],
    minHfov:58,maxHfov:88,keyboardZoom:false,mouseZoom:true,
    compass:false,draggable:true,disableKeyboardCtrl:true
  });
  state.viewer.on('load',()=>{
    loading.hidden=true;
    state.transitioning=false;
    state.loadedNodes.add(n.id);
    preload(n.next);preload(n.previous);
    if(announce)live.textContent=`${n.label}, ${n.quarter}`;
  });
  state.viewer.on('error',()=>{
    loading.hidden=true;state.transitioning=false;
    live.textContent='This area could not be loaded. Please try again.';
  });
}
function setNode(id,{resetView=false,announce=true}={}){
  const n=node(id);if(!n||state.transitioning)return;
  state.transitioning=true;loading.hidden=false;
  captureView();
  const change=()=>{destroyViewer();state.currentNode=id;updateUI();buildViewer(n,{resetView,announce});};
  if(reduceMotion)change();else setTimeout(change,180);
}
function move(direction){
  const n=node(state.currentNode);const id=direction==='next'?n.next:n.previous;if(id)setNode(id);
}
moves.forEach(b=>b.addEventListener('click',()=>move(b.dataset.move)));
reset.addEventListener('click',()=>setNode(cfg.startNode,{resetView:true}));
viewport.addEventListener('keydown',e=>{
  if(!state.viewer)return;
  if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','w','W','s','S'].includes(e.key))e.preventDefault();
  if(e.key==='ArrowLeft')state.viewer.setYaw(state.viewer.getYaw()-3,false);
  if(e.key==='ArrowRight')state.viewer.setYaw(state.viewer.getYaw()+3,false);
  if(e.key==='ArrowUp')state.viewer.setPitch(clamp(state.viewer.getPitch()+3,...cfg.pitchLimits),false);
  if(e.key==='ArrowDown')state.viewer.setPitch(clamp(state.viewer.getPitch()-3,...cfg.pitchLimits),false);
  if(e.key==='w'||e.key==='W')move('next');
  if(e.key==='s'||e.key==='S')move('previous');
});
window.addEventListener('resize',()=>state.viewer&&state.viewer.resize());
updateUI();loading.hidden=false;buildViewer(node(cfg.startNode),{resetView:true,announce:false});
})();
