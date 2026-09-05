// 9. Party Mode — music-driven orb + ring
let party=false, partyInt=null;
export function toggleParty(getLevel, setState){
  party=!party;
  if(party){
    setState('speaking');
    document.body.style.filter="saturate(1.4) brightness(1.05)";
    partyInt=setInterval(()=>{
      const lvl=getLevel();
      document.querySelector('.orb-wrap').style.filter=`hue-rotate(${Date.now()/20%360}deg) brightness(${1+lvl*0.5})`;
    },50);
    // auto off after 30s
    setTimeout(()=>{ if(party) toggleParty(getLevel,setState); },30000);
  } else {
    clearInterval(partyInt);
    document.body.style.filter="";
    document.querySelector('.orb-wrap').style.filter="";
    setState('idle');
  }
  return party;
}
