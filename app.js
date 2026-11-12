const hotspots=[
  {name:'ITO Junction',lat:28.628,lng:77.241,risk:'High',incidents:284,reason:'Multi-leg junction and peak-hour congestion'},
  {name:'AIIMS Flyover',lat:28.567,lng:77.21,risk:'High',incidents:247,reason:'High-speed merging and rain sensitivity'},
  {name:'Dhaula Kuan',lat:28.593,lng:77.162,risk:'High',incidents:219,reason:'Complex interchange movement'},
  {name:'Kashmere Gate',lat:28.667,lng:77.228,risk:'Medium',incidents:178,reason:'Pedestrian and bus traffic'},
  {name:'Lajpat Nagar',lat:28.568,lng:77.244,risk:'Medium',incidents:151,reason:'Mixed commercial corridor'},
  {name:'Noida Sector 18',lat:28.57,lng:77.326,risk:'Low',incidents:89,reason:'Moderate traffic flow'}
];
const colors={High:'#d7463d',Medium:'#ee7c42',Low:'#96bd24'};
const map=L.map('map',{zoomControl:false}).setView([28.6139,77.209],11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(map);
L.control.zoom({position:'bottomright'}).addTo(map);
hotspots.forEach(h=>{L.circle([h.lat,h.lng],{radius:h.incidents*4,color:colors[h.risk],fillColor:colors[h.risk],fillOpacity:.25,weight:2}).bindPopup(`<b>${h.name}</b><br>${h.risk} risk · ${h.incidents} incidents<br><small>${h.reason}</small>`).addTo(map);});
const level=['Low','Moderate','High'];
const el=id=>document.getElementById(id);
function volumeLabel(v){return ['Very low','Low','Moderate','High','Very high'][v-1]}
function display(score,status,factors){const color=score>=65?'#ee7c42':score>=42?'#d8bd41':'#9cc63d';el('score').textContent=score;el('meterFill').style.width=score+'%';el('meterFill').style.background=color;el('riskBadge').textContent=status.toUpperCase()+' RISK';el('riskBadge').style.background=score>=65?'#633326':score>=42?'#5e541c':'#2c5a32';el('riskText').textContent=score>=65?'Conditions call for additional caution and targeted monitoring.':score>=42?'Use routine monitoring and consider local speed-calming measures.':'Current conditions are relatively favorable; continue standard monitoring.';el('factors').innerHTML=factors.map(x=>`<span>${x}</span>`).join('');}
async function predict(){const record={hour:+el('hour').value,weather:el('weather').value,road:el('road').value,traffic:+el('traffic').value,speed:+el('speed').value};const api=(location.port==='8001'||location.hostname.endsWith('onrender.com'))?'/predict':'http://localhost:8001/predict';try{const response=await fetch(api,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(record)});if(!response.ok)throw Error();const data=await response.json();display(data.risk_score,data.risk_level,data.factors);}catch{let score=20+record.traffic*7+(record.speed-30)*.35;if(record.hour===8||record.hour===18)score+=17;if(record.hour===23)score+=9;if(record.weather==='rain')score+=14;if(record.weather==='fog')score+=18;if(record.road==='junction')score+=18;if(record.road==='highway')score+=10;if(record.road==='arterial')score+=7;score=Math.round(Math.min(96,score));let factors=[];if(record.hour===8||record.hour===18)factors.push('Peak commute');if(record.weather!=='clear')factors.push(record.weather==='rain'?'Rainfall':'Low visibility');if(record.traffic>=4)factors.push('High traffic');if(record.speed>=70)factors.push('Higher speed');if(record.road==='junction')factors.push('Complex junction');display(score,score>=65?'High':score>=42?'Moderate':'Low',factors.length?factors:['Stable conditions']);}}
el('riskForm').addEventListener('submit',e=>{e.preventDefault();predict();});el('traffic').addEventListener('input',e=>el('trafficOut').textContent=volumeLabel(+e.target.value));el('resetBtn').addEventListener('click',()=>{el('riskForm').reset();el('trafficOut').textContent='High';predict();});predict();
