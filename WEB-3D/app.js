import * as THREE from 'three';
import { skins, applySkin } from './skins.js';
import { toggleParty } from './party.js';

// ---------- Audio-reactive Ring Visualizer (like music visualizer frames) ----------
const ringCanvas = document.getElementById('ringCanvas');
const ringCtx = ringCanvas.getContext('2d');
let audioContext=null, analyser=null, micStream=null, audioData=null;
let ringTime=0;
let state='idle';
const orbWrap=document.getElementById('orbWrap');
const waveform=document.getElementById('waveform');
const footerState=document.getElementById('footerState');
function setState(s){
  state=s;
  if(orbWrap) orbWrap.className='orb-wrap '+s;
  if(waveform) waveform.classList.toggle('show', s==='listening' || s==='speaking');
  if(footerState){ footerState.textContent=s; footerState.style.color = s==='listening' ? 'var(--accent2)' : s==='speaking' ? 'var(--accent3)' : s==='thinking' ? '#f5c542' : 'rgba(255,255,255,0.3)'; }
  const sl=document.getElementById('statusLabel');
  if(sl) sl.innerHTML =
    s==='listening' ? '<i class="fa-solid fa-waveform" style="color:var(--accent2)"></i> listening...' :
    s==='thinking' ? '<i class="fa-solid fa-brain" style="color:#f5c542"></i> thinking...' :
    s==='speaking' ? '<i class="fa-solid fa-volume-high" style="color:var(--accent3)"></i> speaking...' :
    '<i class="fa-solid fa-circle" style="color:var(--green);font-size:8px"></i> say <b>hi aura</b> to wake';
  const ht=document.getElementById('hintText');
  if(ht){
    if(s==='idle') ht.textContent='listening continuously — 2s silence to send';
    if(s==='listening') ht.textContent='hearing you... keep talking';
  }
}
async function initAudioAnalyser(){
  try{
    if(!audioContext){
      audioContext = new (window.AudioContext||window.webkitAudioContext)();
      analyser = audioContext.createAnalyser();
      analyser.fftSize=256;
      analyser.smoothingTimeConstant=0.8;
      audioData=new Uint8Array(analyser.frequencyBinCount);
      const stream=await navigator.mediaDevices.getUserMedia({audio:true});
      micStream=stream;
      audioContext.createMediaStreamSource(stream).connect(analyser);
    }
    if(audioContext.state==='suspended') await audioContext.resume();
  }catch(e){ console.log('mic analyser fail',e); }
}
function getAudioLevel(){
  if(!analyser || !audioData) return 0;
  analyser.getByteFrequencyData(audioData);
  let sum=0; for(let i=0;i<64;i++) sum+=audioData[i];
  return sum/64/255; // 0..1
}
function drawRing(){
  requestAnimationFrame(drawRing);
  ringTime+=0.02;
  const w=ringCanvas.width, h=ringCanvas.height;
  const cx=w/2, cy=h/2;
  const baseR=92;
  const level = state==='listening' ? getAudioLevel() : state==='speaking' ? (0.5+Math.sin(ringTime*3)*0.3) : state==='thinking' ? (0.3+Math.sin(ringTime*2)*0.2) : 0.08;
  ringCtx.clearRect(0,0,w,h);
  // glow
  const g=ringCtx.createRadialGradient(cx,cy,baseR-20,cx,cy,baseR+50);
  if(state==='listening'){ g.addColorStop(0,'rgba(45,212,255,0.0)'); g.addColorStop(0.5,'rgba(45,212,255,0.18)'); g.addColorStop(1,'rgba(45,212,255,0)'); }
  else if(state==='speaking'){ g.addColorStop(0,'rgba(255,92,138,0.0)'); g.addColorStop(0.5,'rgba(255,92,138,0.22)'); g.addColorStop(1,'rgba(255,92,138,0)'); }
  else if(state==='thinking'){ g.addColorStop(0,'rgba(255,210,80,0.0)'); g.addColorStop(0.5,'rgba(255,210,80,0.15)'); g.addColorStop(1,'rgba(255,92,138,0)'); }
  else { g.addColorStop(0,'rgba(124,92,255,0.0)'); g.addColorStop(0.5,'rgba(124,92,255,0.12)'); g.addColorStop(1,'rgba(124,92,255,0)'); }
  ringCtx.fillStyle=g;
  ringCtx.beginPath(); ringCtx.arc(cx,cy,baseR+40,0,Math.PI*2); ringCtx.fill();

  // main ring with distortions - like frames: smooth -> cat ears (2 peaks) -> wavy multi-peaks -> symmetrical flare
  ringCtx.save();
  ringCtx.translate(cx,cy);
  for(let layer=0; layer<2; layer++){
    const isInner=layer===0;
    const lw=isInner? 2.5:1.2;
    const alpha=isInner? (0.9+level*0.5): (0.35+level*0.3);
    const col= isInner ? (state==='listening'?'rgba(45,212,255,': state==='speaking'?'rgba(255,92,138,': state==='thinking'?'rgba(255,210,80,':'rgba(124,92,255,') : (state==='listening'?'rgba(124,92,255,':'rgba(255,255,255,');
    ringCtx.strokeStyle=col+alpha+')';
    ringCtx.lineWidth=lw;
    ringCtx.shadowBlur=isInner? 16:8;
    ringCtx.shadowColor= isInner ? (state==='listening'?'#2dd4ff': state==='speaking'?'#ff5c8a': '#7c5cff') : 'transparent';
    ringCtx.lineJoin='round'; ringCtx.lineCap='round';
    ringCtx.beginPath();
    const points=72; // reduced from 128 for perf
    for(let i=0;i<=points;i++){
      const angle=(i/points)*Math.PI*2;
      // frequency-mapped distortion: bass-> bottom flare, mids-> sides, highs-> cat ears top
      let amp=0;
      if(analyser && audioData && state==='listening'){
        const idx=Math.floor((angle/(Math.PI*2))*64);
        amp=audioData[idx]/255;
      } else {
        // simulated for idle/speaking/thinking
        if(state==='speaking'){
          amp=0.4+0.6*Math.sin(angle*3+ringTime*4)*0.5+0.3*Math.sin(angle*7-ringTime*6)*0.5;
          amp=Math.max(0,amp);
        } else if(state==='thinking'){
          amp=0.2+0.4*Math.sin(angle*2+ringTime*2);
        } else if(state==='listening'){
          amp=level*0.8;
        } else {
          amp=0.1+0.08*Math.sin(angle*2+ringTime*0.8);
        }
      }
      // frame logic: Frame1 smooth (low), Frame2 cat ears (2 peaks up), Frame3 wavy multi-peaks, Frame4 symmetrical sides
      // blend based on level
      const peakCat = Math.max(0, Math.cos(angle - Math.PI/2))*0.9; // top cat ears at -90deg
      const peakCat2 = Math.max(0, Math.cos(angle - Math.PI/2 -0.4))*0.7 + Math.max(0, Math.cos(angle - Math.PI/2 +0.4))*0.7;
      const wavy = (Math.sin(angle*5+ringTime*1.2)*0.5+0.5)*0.6 + (Math.sin(angle*3-ringTime)*0.3);
      const sideFlare = Math.max(0, Math.cos(angle))*0.5 + Math.max(0, Math.cos(angle+Math.PI))*0.5;
      let shapeMix;
      if(level<0.15) shapeMix= amp*0.3; // Frame1 smooth
      else if(level<0.35) shapeMix= peakCat2*amp*1.2; // Frame2 cat ears
      else if(level<0.6) shapeMix= wavy*amp*1.0; // Frame3 wavy
      else shapeMix= (wavy*0.6+sideFlare*0.6)*amp*1.1; // Frame4 symmetrical

      const r= baseR + (isInner? shapeMix*38 : shapeMix*22) + (isInner?0:4);
      const x=Math.cos(angle)*r, y=Math.sin(angle)*r;
      if(i===0) ringCtx.moveTo(x,y); else ringCtx.lineTo(x,y);
    }
    ringCtx.closePath(); ringCtx.stroke();
    // white flare at bottom for Frame1 style - bright spot
    if(isInner && level>0.1){
      const flareY= baseR+8;
      const flareG=ringCtx.createRadialGradient(0, flareY, 0, 0, flareY, 18);
      flareG.addColorStop(0,'rgba(255,255,255,'+(0.9*level)+')'); flareG.addColorStop(1,'rgba(255,255,255,0)');
      ringCtx.fillStyle=flareG;
      ringCtx.beginPath(); ringCtx.arc(0, flareY, 12*level+4, 0, Math.PI*2); ringCtx.fill();
    }
  }
  ringCtx.restore();
}
drawRing();

// ---------- 3D Orb ----------
const canvas = document.getElementById('orbCanvas');
const renderer = new THREE.WebGLRenderer({canvas, antialias:false, alpha:true, powerPreference:"high-performance"});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.5));
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, innerWidth/innerHeight, 0.1, 100);
camera.position.z = 5;

const orbGroup = new THREE.Group();
scene.add(orbGroup);

// main sphere with fresnel + wireframe inner
const sphereGeo = new THREE.IcosahedronGeometry(1.2, 4);
const sphereMat = new THREE.MeshStandardMaterial({color:0x7c5cff, emissive:0x2dd4ff, emissiveIntensity:0.2, metalness:0.3, roughness:0.4, wireframe:false});
const sphere = new THREE.Mesh(sphereGeo, sphereMat);
orbGroup.add(sphere);

const wireMat = new THREE.MeshBasicMaterial({color:0xffffff, wireframe:true, transparent:true, opacity:0.06});
const wire = new THREE.Mesh(new THREE.IcosahedronGeometry(1.35, 2), wireMat);
orbGroup.add(wire);

const light = new THREE.PointLight(0x7c5cff, 2, 10);
light.position.set(2,2,3);
scene.add(light);
scene.add(new THREE.AmbientLight(0xffffff,0.4));
scene.add(new THREE.DirectionalLight(0xffffff,0.6).position.set(-2,2,3));

const particles = new THREE.Points(
  new THREE.BufferGeometry(),
  new THREE.PointsMaterial({color:0x7c5cff, size:0.025, transparent:true, opacity:0.35})
);
const pos = new Float32Array(150); // halved for perf
for(let i=0;i<150;i++) pos[i]=(Math.random()-0.5)*6;
particles.geometry.setAttribute('position', new THREE.BufferAttribute(pos,3));
scene.add(particles);

// state already defined above for ring visualizer

let t=0;
function animate(){
  requestAnimationFrame(animate);
  t+=0.01;
  const s = state==='listening' ? 1.08 : state==='speaking' ? 1.12+Math.sin(t*8)*0.04 : state==='thinking' ? 1.05 : 1;
  const scale = THREE.MathUtils.lerp(sphere.scale.x, s, 0.08);
  sphere.scale.set(scale,scale,scale);
  orbGroup.rotation.y += state==='thinking' ? 0.02 : 0.003;
  orbGroup.rotation.x = Math.sin(t*0.5)*0.08;
  wire.rotation.y -= 0.002;
  particles.rotation.y += 0.001;
  renderer.render(scene,camera);
}
animate();
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);});
renderer.setSize(innerWidth,innerHeight);

// ---------- Speech ----------
const liveText=document.getElementById('liveText');
const responseText=document.getElementById('responseText');
const micBtn=document.getElementById('micBtn');
const voiceSelect=document.getElementById('voiceSelect');
const langSelect=document.getElementById('langSelect');
const silenceInput=document.getElementById('silenceInput');

// voices
function loadVoices(){
  const voices=speechSynthesis.getVoices();
  voiceSelect.innerHTML='';
  voices.forEach(v=>{
    const o=document.createElement('option');o.value=v.name;o.textContent=v.name+' ('+v.lang+')';
    if(v.name.includes('Jenny')||v.name.includes('Aria')||v.lang==='en-IN') o.selected=true;
    voiceSelect.appendChild(o);
  });
}
speechSynthesis.onvoiceschanged=loadVoices; loadVoices();

let history = JSON.parse(localStorage.getItem('aura_history')||'[]');
// dedup old history on load (fix repeating)
history = history.filter((v,i,a)=> i===0 || v.q!==a[i-1].q || v.a!==a[i-1].a);
if(history.length>50) history=history.slice(-50);
const historyCount=document.getElementById('historyCount');
const historyList=document.getElementById('historyList');
function saveHistory(){
  if(history.length>1 && history[history.length-1].q===history[history.length-2].q && history[history.length-1].a===history[history.length-2].a) history.pop();
  if(history.length>50) history=history.slice(-50);
  try{ localStorage.setItem('aura_history',JSON.stringify(history)); }
  catch(e){
    if(e.name==='QuotaExceededError' || e.code===22){
      history=history.slice(-20);
      try{ localStorage.setItem('aura_history',JSON.stringify(history)); }catch(e2){ console.error('quota still exceeded',e2); }
    } else console.error(e);
  }
  historyCount.textContent=history.length;
  requestAnimationFrame(renderHistory);
}
function escapeHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
function renderHistory(){
  if(!history.length){historyList.innerHTML='<div class="empty"><i class="fa-solid fa-comments"></i><span>No conversations yet</span><small>Say "hi aura" and start talking — everything you say is saved here</small></div>';return;}
  historyList.innerHTML=history.slice().reverse().map((h,i)=>{
    const idx=history.length-1-i;
    return `
    <div class="hist-card">
      <div class="meta"><span>${new Date(h.ts).toLocaleDateString()} • ${new Date(h.ts).toLocaleTimeString()}</span><span>#${idx+1} <button onclick="deleteHist(${idx})" class="mini-del" title="Delete"><i class="fa-solid fa-trash"></i></button></span></div>
      <div class="q"><i class="fa-solid fa-user"></i> ${escapeHtml(h.q)}</div>
      <div class="a"><i class="fa-solid fa-wand-magic-sparkles"></i> ${escapeHtml(h.a)}
        <button onclick="replayHist(${idx})" class="mini-play" title="Replay"><i class="fa-solid fa-volume-high"></i></button>
      </div>
    </div>`;
  }).join('');
}
function deleteHist(idx){ history.splice(idx,1); saveHistory(); }
function replayHist(idx){ if(history[idx]) speak(history[idx].a); }
saveHistory();

// TTS with streaming illusion
function speak(text){
  return new Promise(resolve=>{
    setState('speaking');
    responseText.textContent=''; responseText.classList.add('show');
    // typewriter illusion for generated text
    let idx=0;
    const iv=setInterval(()=>{
      responseText.textContent=text.slice(0,idx);
      idx+=2;
      if(idx>=text.length){clearInterval(iv); responseText.textContent=text;}
    },18);

    const utter=new SpeechSynthesisUtterance(text);
    const v=speechSynthesis.getVoices().find(x=>x.name===voiceSelect.value);
    if(v) utter.voice=v;
    utter.rate=1; utter.pitch=1;
    utter.onend=()=>{
      // disappear after speaking but keep in history
      setTimeout(()=>{ responseText.classList.remove('show'); liveText.textContent=''; }, 1800);
      setState('idle');
      resolve();
    };
    utter.onerror=()=>{ setState('idle'); resolve(); };
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
  });
}

// STT wakeword
let recognition=null;
let isListening=false;
let silenceTimer=null;
let transcriptBuffer='';
let wakeArmed=true; // waiting for hi aura

function createRecognition(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){ alert('Web Speech API not supported — use Chrome/Brave'); return null; }
  const r=new SR();
  r.continuous=true; r.interimResults=true;
  r.lang=langSelect.value||'en-IN';
  r.onstart=()=>{ isListening=true; micBtn.classList.add('active'); setState(wakeArmed?'idle':'listening'); }
  r.onend=()=>{
    isListening=false; micBtn.classList.remove('active');
    // only auto-restart if user explicitly started (not idle) — still respects user gesture, but keeps wakeword alive
    if(!wakeArmed && document.visibilityState==='visible' && micBtn.dataset.armed==='1'){
      setTimeout(()=>{ try{ r.start(); }catch(e){} }, 300);
    } else if(wakeArmed && micBtn.dataset.armed==='1' && document.visibilityState==='visible'){
      setTimeout(()=>{ try{ r.start(); }catch(e){} }, 600);
    } else {
      setState('idle');
      document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-power-off" style="color:var(--muted)"></i> tap <b>mic</b> to start again';
    }
  };
  r.onresult=(e)=>{
    let interim='';
    for(let i=e.resultIndex;i<e.results.length;i++){
      const txt=e.results[i][0].transcript;
      if(e.results[i].isFinal) transcriptBuffer+=txt+' ';
      else interim+=txt;
    }
    const full=(transcriptBuffer+interim).trim();

    // wakeword detection - fuzzy for hii aura, hiiii, etc + case + extra spaces
    if(wakeArmed){
      const lower=full.toLowerCase();
      // allow hi with multiple i, hey, hello, with optional aura variations
      const wakeMatch = lower.match(/(h+i+\s*aura|hey\s*aura|hello\s*aura|\baura\b)/i);
      if(wakeMatch){
        wakeArmed=false;
        // remove wakeword and keep rest
        let after = full.substring(full.toLowerCase().indexOf(wakeMatch[0]) + wakeMatch[0].length).trim();
        // if wakeword was at start but user said "hii aura whats capital", keep whats capital
        transcriptBuffer=after || full.replace(/h+i+\s*aura|hey\s*aura|hello\s*aura|aura/gi,'').trim();
        liveText.textContent=transcriptBuffer || 'Listening...';
        setState('listening');
        // visual feedback + debug
        console.log('Wakeword detected:', wakeMatch[0], 'remaining:', transcriptBuffer);
        document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-check" style="color:var(--green)"></i> woke — speak now!';
        clearTimeout(silenceTimer);
        silenceTimer=setTimeout(()=>{ handleSend(transcriptBuffer || full.replace(/h+i+\s*aura|hey\s*aura|hello\s*aura|aura/gi,'').trim()); }, parseInt(silenceInput.value)||2000);
      } else {
        // show faint hearing + hint
        liveText.textContent=full.slice(-60) || '...';
        document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-ear-listen"></i> say <b>hi aura</b> — heard: "'+escapeHtml(full.slice(-30))+'"';
      }
      return;
    }

    // already woken, keep updating and reset 2s silence timer
    liveText.textContent=full;
    setState('listening');
    clearTimeout(silenceTimer);
    silenceTimer=setTimeout(()=>{ handleSend(full); }, parseInt(silenceInput.value)||2000);
  };
  r.onerror=(e)=>{
    console.log('STT error',e);
    const err=e.error||'unknown';
    document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-triangle-exclamation" style="color:var(--accent3)"></i> mic error: '+err;
    if(err==='network'){
      // Brave blocks Google Speech — fallback to Groq Whisper (on-device via Groq)
      console.log('Web Speech network blocked — switching to Groq Whisper fallback');
      document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-wifi" style="color:var(--accent3)"></i> Web Speech blocked — using Groq Whisper...';
      document.getElementById('hintText').textContent='Brave blocks Google Speech — Groq Whisper will listen after tap';
      try{ r.stop(); }catch(e){}
      // switch to whisper mode after 1s
      setTimeout(()=>{ startWhisperFallback(); }, 800);
    }
  };
  r.onaudiostart=()=> console.log('audio start');
  r.onspeechstart=()=> console.log('speech start');
  r.onsoundstart=()=> console.log('sound start');
  return r;
}

// ---------- Groq Whisper Fallback (when Web Speech network fails) ----------
let whisperRecorder=null, whisperChunks=[], whisperSilence=null;
async function startWhisperFallback(){
  const key=localStorage.getItem('aura_groq_key')||'';
  if(!key){ 
    document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-key" style="color:var(--accent3)"></i> set Groq key in Settings for Whisper';
    document.getElementById('hintText').textContent='Settings → paste Groq gsk_... → tap mic again';
    return; 
  }
  try{
    const stream=await navigator.mediaDevices.getUserMedia({audio:true});
    if(audioContext && audioContext.state==='suspended') await audioContext.resume();
    // connect to analyser for ring
    if(analyser && audioContext) try{ audioContext.createMediaStreamSource(stream).connect(analyser); }catch(e){}
    whisperRecorder=new MediaRecorder(stream, {mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : 'audio/webm'});
    whisperChunks=[];
    whisperRecorder.ondataavailable=e=>{ if(e.data.size>0) whisperChunks.push(e.data); };
    whisperRecorder.onstop=async ()=>{
      const blob=new Blob(whisperChunks, {type: whisperRecorder.mimeType});
      if(blob.size<2000){ document.getElementById('statusLabel').innerHTML='too short — tap again and say "hi aura"'; setState('idle'); return; }
      setState('thinking');
      document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-cloud-arrow-up"></i> transcribing with Groq Whisper...';
      const fd=new FormData();
      fd.append('file', blob, 'audio.webm');
      fd.append('model', 'whisper-large-v3-turbo');
      fd.append('response_format','json');
      // Groq needs language auto; we can pass prompt
      try{
        const res=await fetch('https://api.groq.com/openai/v1/audio/transcriptions',{method:'POST', headers:{'Authorization':'Bearer '+key}, body: fd});
        const j=await res.json();
        const text=(j.text||'').trim();
        console.log('Whisper text:',text);
        if(!text){ document.getElementById('statusLabel').innerHTML='no speech heard — try again'; setState('idle'); return; }
        // check wakeword in whisper text too
        let clean=text;
        const m=text.toLowerCase().match(/(h+i+\s*aura|hey\s*aura|hello\s*aura|\baura\b)/i);
        if(m){ clean=text.substring(text.toLowerCase().indexOf(m[0])+m[0].length).trim() || text.replace(/h+i+\s*aura|hey\s*aura|hello\s*aura|aura/gi,'').trim(); }
        if(!clean) clean=text;
        liveText.textContent=clean;
        handleSend(clean);
      }catch(e){ console.error(e); document.getElementById('statusLabel').innerHTML='Whisper failed: '+e.message; setState('idle'); }
    };
    whisperRecorder.start();
    setState('listening');
    document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-microphone" style="color:var(--accent2)"></i> Whisper listening — say "hi aura ..." (5s)';
    // auto-stop after 5s or 2s silence via analyser level
    let silenceStart=null;
    const checkSilence=setInterval(()=>{
      const lvl=getAudioLevel();
      if(lvl<0.08){
        if(!silenceStart) silenceStart=Date.now();
        if(Date.now()-silenceStart>2000 && whisperRecorder && whisperRecorder.state==='recording'){
          clearInterval(checkSilence); try{ whisperRecorder.stop(); }catch(e){} stream.getTracks().forEach(t=>t.stop());
        }
      } else silenceStart=null;
      if(whisperRecorder && whisperRecorder.state!=='recording') clearInterval(checkSilence);
    },200);
    setTimeout(()=>{ if(whisperRecorder && whisperRecorder.state==='recording'){ clearInterval(checkSilence); try{ whisperRecorder.stop(); }catch(e){} stream.getTracks().forEach(t=>t.stop()); } }, 7000);
  }catch(e){ console.error('whisper fallback fail',e); document.getElementById('statusLabel').innerHTML='mic permission denied'; }
}

async function handleSend(text){
  const clean=text.trim();
  if(!clean || clean.length<2){ wakeArmed=true; liveText.textContent=''; transcriptBuffer=''; setState('idle'); return; }
  // fix history repeating: ignore if same as last q
  if(history.length && history[history.length-1].q===clean){ console.log('duplicate ignored'); wakeArmed=true; liveText.textContent=''; setState('idle'); return; }
  wakeArmed=true;
  liveText.textContent=clean;
  transcriptBuffer='';
  clearTimeout(silenceTimer);
  setState('thinking');

  const reply=await getAIReply(clean);
  // dedup reply repeating prompt
  let finalReply=reply;
  if(finalReply.toLowerCase().trim()===clean.toLowerCase().trim()) finalReply="I heard you — "+clean+" — how can I help further?";
  history.push({q:clean, a:finalReply, ts:Date.now()});
  saveHistory();
  await speak(finalReply);
  liveText.textContent=''; // disappear after speaking, history keeps it
}

// Groq live if key saved, else mock - fixed hallucination: no echo, concise, no repeat
async function getAIReply(prompt){
  const key=localStorage.getItem('aura_groq_key')||'';
  if(!key){
    // mock - direct answer, no echo loop
    const p=prompt.toLowerCase();
    if(p.includes('capital') && p.includes('india')) return 'New Delhi is the capital of India.';
    if(p.includes('hello')||p.includes('hi')) return 'Hello! I am AURA — how can I help you today?';
    if(p.includes('time')) return new Date().toLocaleTimeString() + ' — local time.';
    if(p.includes('date')) return new Date().toLocaleDateString() + ' — today.';
    return 'Heard you — I am AURA, your voice companion. Ask me anything!';
  }
  try{
    const res=await fetch('https://api.groq.com/openai/v1/chat/completions',{
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':'Bearer '+key},
      body:JSON.stringify({
        model:'openai/gpt-oss-20b',
        messages:[
          {role:'system',content:'You are AURA, a helpful voice assistant. Answer directly and concisely in 1-2 sentences. Do NOT repeat or echo the user prompt. Do NOT say "You said". Just answer.'},
          {role:'user',content:prompt}
        ],
        max_tokens:80, temperature:0.6, top_p:0.9, presence_penalty:0.6, frequency_penalty:0.5
      })
    });
    const j=await res.json();
    let txt=j.choices?.[0]?.message?.content?.replace('\u202f',' ').replace(/\u00a0/g,' ').trim() || '';
    // de-duplicate hallucination: if response repeats prompt verbatim, strip it
    if(txt.toLowerCase().includes(prompt.toLowerCase().slice(0,20)) && txt.length < prompt.length+30){
      txt=txt.replace(new RegExp(prompt.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'i'),'').trim() || txt;
    }
    return txt || 'Sorry, I could not think.';
  }catch(e){ return 'Groq error: '+e.message; }
}

// controls + keyboard — explicit arm, no auto-listen until click
micBtn.onclick=async ()=>{
  if(!recognition) recognition=createRecognition();
  if(isListening){
    micBtn.dataset.armed='0';
    try{ recognition.stop(); }catch(e){}
    wakeArmed=true; liveText.textContent=''; setState('idle');
    document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-power-off" style="color:var(--muted)"></i> tap <b>mic</b> to start';
  } else {
    micBtn.dataset.armed='1';
    transcriptBuffer=''; wakeArmed=true;
    recognition.lang=langSelect.value||'en-US';
    // don't block STT with getUserMedia — visualizer will use simulated level if mic analyser fails
    initAudioAnalyser().catch(()=>{});
    try{ recognition.start(); setState('idle'); console.log('recognition started, lang', recognition.lang); }catch(e){ alert('Mic permission needed: '+e.message+' — Brave: brave://settings/content/microphone allow localhost:5173'); console.error(e); }
  }
};
addEventListener('keydown',e=>{
  if(e.code==='Space' && !e.target.matches('input,textarea,select')){ e.preventDefault(); micBtn.click(); }
  if(e.code==='Escape'){ drawer.classList.remove('open'); overlay.classList.remove('show'); settingsModal.classList.remove('show'); }
});
// text fallback — bypasses mic entirely, also tests wakeword
const textFallback=document.getElementById('textFallback');
const sendTextBtn=document.getElementById('sendTextBtn');
function handleTextFallback(){
  const val=textFallback.value.trim();
  if(!val) return;
  console.log('text fallback:',val);
  // simulate wakeword stripping like STT
  let clean=val.replace(/h+i+\s*aura|hey\s*aura|hello\s*aura|aura/gi,'').trim() || val;
  textFallback.value='';
  handleSend(clean);
}
sendTextBtn.onclick=handleTextFallback;
textFallback.addEventListener('keydown',e=>{ if(e.key==='Enter') handleTextFallback(); });

// DO NOT auto-start — wait for user gesture (browser blocks auto mic)
window.addEventListener('load',()=>{
  loadVoices();
  setState('idle');
  document.getElementById('statusLabel').innerHTML='<i class="fa-solid fa-power-off" style="color:var(--muted)"></i> tap <b>mic</b> or press <b>Space</b> to start';
  document.getElementById('hintText').textContent='AURA will only listen after you tap — then say "hi aura"';
  micBtn.classList.remove('active');
  // load saved settings
  const k=localStorage.getItem('aura_groq_key'); if(k) document.getElementById('groqKeyInput').value=k;
  const s=localStorage.getItem('aura_silence'); if(s) silenceInput.value=s;
  const l=localStorage.getItem('aura_lang'); if(l) langSelect.value=l;
});

// 8 Orb skins + 9 Party wiring
const skinSelect=document.getElementById('skinSelect');
const partyBtn=document.getElementById('partyBtn');
if(skinSelect){
  const savedSkin=localStorage.getItem('aura_skin')||'neon';
  skinSelect.value=savedSkin;
  // wait for sphereMat defined below, apply after init
  setTimeout(()=>{ try{ applySkin(savedSkin, sphereMat); }catch(e){} },500);
  skinSelect.onchange=()=>{ try{ applySkin(skinSelect.value, sphereMat); }catch(e){} };
}
if(partyBtn) partyBtn.onclick=()=>{ const on=toggleParty(getAudioLevel, setState); partyBtn.innerHTML= on ? '<i class="fa-solid fa-stop"></i> Stop' : '<i class="fa-solid fa-music"></i> Party'; };

// drawer
const drawer=document.getElementById('historyDrawer'), overlay=document.getElementById('overlay');
document.getElementById('historyBtn').onclick=()=>{ drawer.classList.add('open'); overlay.classList.add('show'); renderHistory(); };
document.getElementById('closeHistory').onclick=()=>{ drawer.classList.remove('open'); overlay.classList.remove('show'); };
overlay.onclick=()=>{ drawer.classList.remove('open'); overlay.classList.remove('show'); document.getElementById('settingsModal').classList.remove('show'); };
document.getElementById('clearBtn').onclick=()=>{ liveText.textContent=''; responseText.textContent=''; responseText.classList.remove('show'); };
document.getElementById('clearHistoryBtn').onclick=()=>{ if(confirm('Clear all history?')){ history=[]; saveHistory(); } };
document.getElementById('exportBtn').onclick=()=>{
  const blob=new Blob([JSON.stringify(history,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='aura-history.json'; a.click();
};

// settings
const settingsModal=document.getElementById('settingsModal');
document.getElementById('settingsBtn').onclick=()=> settingsModal.classList.add('show');
document.getElementById('closeSettings').onclick=()=> settingsModal.classList.remove('show');
document.getElementById('saveSettings').onclick=()=>{
  localStorage.setItem('aura_groq_key', document.getElementById('groqKeyInput').value.trim());
  localStorage.setItem('aura_lang', langSelect.value);
  localStorage.setItem('aura_silence', silenceInput.value);
  settingsModal.classList.remove('show');
  if(recognition){ try{ recognition.stop(); }catch(e){} recognition.lang=langSelect.value; try{ recognition.start(); }catch(e){} }
};
langSelect.onchange=()=>{ localStorage.setItem('aura_lang', langSelect.value); if(recognition) recognition.lang=langSelect.value; };
