// 8. Orb Skins — premium themes for AURA orb
export const skins={
  neon:{ name:"Neon", sphere:{color:0x7c5cff, emissive:0x2dd4ff, metalness:0.3}, bg:"radial-gradient(900px 600px at 50% -10%, #1a1240 0%, transparent 60%)"},
  crystal:{ name:"Crystal", sphere:{color:0xe0f0ff, emissive:0x88ccff, metalness:0.8, roughness:0.1}, bg:"radial-gradient(900px 600px at 50% -10%, #0a2a4a 0%, transparent 60%)"},
  plasma:{ name:"Plasma", sphere:{color:0xff3b7f, emissive:0xff6b35, metalness:0.2}, bg:"radial-gradient(900px 600px at 50% -10%, #3a0a1a 0%, transparent 60%)"},
  forest:{ name:"Forest", sphere:{color:0x22c55e, emissive:0x4ade80, metalness:0.4}, bg:"radial-gradient(900px 600px at 50% -10%, #0a2a0a 0%, transparent 60%)"},
};
export function applySkin(key, sphereMat){
  const s=skins[key]; if(!s) return;
  sphereMat.color.setHex(s.sphere.color); sphereMat.emissive.setHex(s.sphere.emissive);
  sphereMat.metalness=s.sphere.metalness ?? 0.3; sphereMat.roughness=s.sphere.roughness ?? 0.4;
  document.querySelector('.bg').style.background=s.bg+", linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%)";
  localStorage.setItem('aura_skin', key);
}
