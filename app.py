import os
import anthropic
import streamlit as st
from system_prompt import SYSTEM_PROMPT

# ── API Client (uses Streamlit secrets for cloud deployment) ──────────────────
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.set_page_config(page_title="CrystalInk Technologies AI Assistant", page_icon="🌐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
html,body,[class*="css"]{font-family:'Share Tech Mono',monospace !important;background-color:#080808 !important;color:#4da3ff !important;}
.stApp{background-color:#080808 !important;}
section[data-testid="stSidebar"]{background-color:#050505 !important;border-right:1px solid #0d3a6e !important;}
section[data-testid="stSidebar"] *{color:#4da3ff !important;font-family:'Share Tech Mono',monospace !important;}
.stChatMessage{background:transparent !important;}
.stChatMessage[data-testid*="user"] .stChatMessageContent{background:#0d3a6e !important;border:1px solid #1a6fd4 !important;color:#cce4ff !important;font-family:'Share Tech Mono',monospace !important;border-radius:6px !important;}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent{background:#0a140a !important;border:1px solid #003b0f !important;color:#4da3ff !important;font-family:'Share Tech Mono',monospace !important;border-radius:6px !important;}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent p{color:#4da3ff !important;}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent li{color:#4da3ff !important;}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent ul{color:#4da3ff !important;}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent ol{color:#4da3ff !important;}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent strong{color:#00ff41 !important;}
.stChatInputContainer{background:#050505 !important;border-top:1px solid #0d3a6e !important;}
.stChatInputContainer textarea{background:#0d0d0d !important;color:#00ff41 !important;font-family:'Share Tech Mono',monospace !important;border:1px solid #0d3a6e !important;}
.stButton button{background:transparent !important;border:1px solid #0d3a6e !important;color:#4da3ff !important;font-family:'Share Tech Mono',monospace !important;font-size:10px !important;letter-spacing:1px !important;}
.stButton button:hover{background:#0d3a6e !important;border-color:#1a6fd4 !important;}
div[data-testid="stMarkdownContainer"] p{color:#4da3ff !important;}
div[data-testid="stMarkdownContainer"] li{color:#4da3ff !important;}
div[data-testid="stMarkdownContainer"] ul li::marker{color:#4da3ff !important;}
div[data-testid="stMarkdownContainer"] ol li::marker{color:#4da3ff !important;}
h1,h2,h3{color:#4da3ff !important;font-family:'Share Tech Mono',monospace !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#060d1a;border-bottom:2px solid #1a6fd4;padding:14px 20px;margin-bottom:16px;
display:flex;align-items:center;justify-content:space-between;border-radius:8px;">
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:34px;height:34px;border-radius:7px;background:#0d3a6e;border:1.5px solid #1a6fd4;
        display:flex;align-items:center;justify-content:center;font-size:16px;">🌐</div>
        <div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:16px;color:#4da3ff;letter-spacing:3px;">CRYSTALINK TECHNOLOGIES</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#00aa2a;letter-spacing:2px;">CONNECTING YOUR WORLD, ONE NETWORK AT A TIME</div>
        </div>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#00ff41;letter-spacing:2px;">● AI ASSISTANT ONLINE // 24/7</div>
</div>
""", unsafe_allow_html=True)

chat_col, anim_col = st.columns([1.1, 0.9])

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greeted = False
if "last_msg" not in st.session_state:
    st.session_state.last_msg = ""

if not st.session_state.greeted:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "// CRYSTALINK.AI ONLINE\n\nWelcome. I'm your CrystalInk Technologies assistant. "
                   "Describe your project and watch the matrix build your network diagram in real time.\n\n"
                   "We cover network installation, WiFi infrastructure, security cameras, AV systems, "
                   "structured cabling, smart home, and IT consulting across the DMV and beyond.\n\nWhat can I help you with today?"
    })
    st.session_state.greeted = True

with chat_col:
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:9px;color:#1a6fd4;letter-spacing:2px;margin-bottom:6px;'>// QUICK SELECT</div>", unsafe_allow_html=True)
    q1,q2,q3,q4 = st.columns(4)
    with q1:
        if st.button("🏨 HOTEL", use_container_width=True):
            st.session_state.last_msg = "I need WiFi and full tech upgrade for a 50 room hotel"; st.rerun()
    with q2:
        if st.button("📷 CCTV", use_container_width=True):
            st.session_state.last_msg = "Security cameras for my office building"; st.rerun()
    with q3:
        if st.button("🏠 HOME", use_container_width=True):
            st.session_state.last_msg = "Smart home setup with WiFi and automation"; st.rerun()
    with q4:
        if st.button("🏫 SCHOOL", use_container_width=True):
            st.session_state.last_msg = "Network infrastructure for my school campus"; st.rerun()

    st.markdown("<div style='border-top:1px solid #111;margin:8px 0;'></div>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🌐" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    if st.session_state.last_msg:
        user_input = st.session_state.last_msg
        st.session_state.last_msg = ""
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🌐"):
            with st.spinner("// PROCESSING..."):
                api_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] in ["user","assistant"]]
                response = client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=1024, system=SYSTEM_PROMPT, messages=api_msgs)
                reply = response.content[0].text
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if user_input := st.chat_input("> DESCRIBE YOUR PROJECT OR ASK A QUESTION..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🌐"):
            with st.spinner("// PROCESSING..."):
                api_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] in ["user","assistant"]]
                response = client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=1024, system=SYSTEM_PROMPT, messages=api_msgs)
                reply = response.content[0].text
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

with anim_col:
    last_user = ""
    for m in reversed(st.session_state.messages):
        if m["role"] == "user":
            last_user = m["content"]
            break

    st.components.v1.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:transparent;overflow:hidden;}}
.wrap{{font-family:'Share Tech Mono',monospace;background:#050505;border:1px solid #0d3a6e;border-radius:8px;overflow:hidden;height:840px;display:flex;flex-direction:column;}}
.ah{{padding:8px 12px;background:#060d1a;border-bottom:1px solid #0d3a6e;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}}
.at{{font-size:9px;color:#1a6fd4;letter-spacing:2px;}}
.as{{font-size:9px;color:#00ff41;letter-spacing:1px;}}
.cw{{flex:1;position:relative;min-height:0;}}
canvas{{position:absolute;top:0;left:0;width:100%;height:100%;}}
.leg{{padding:6px 12px;background:#060d1a;border-top:1px solid #0d3a6e;display:none;gap:10px;flex-wrap:wrap;flex-shrink:0;}}
.li{{display:flex;align-items:center;gap:4px;font-size:8px;letter-spacing:1px;}}
.ld{{width:7px;height:7px;border-radius:50%;border:1.5px solid;}}
.il{{padding:6px 12px;background:#030303;border-top:1px solid #0a0a0a;font-size:8px;color:#1a4a1a;letter-spacing:1px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
</style>
<div class="wrap">
  <div class="ah">
    <div class="at" id="lbl">// AWAITING INPUT</div>
    <div class="as" id="sts">STANDBY</div>
  </div>
  <div class="cw" id="cw">
    <canvas id="rc"></canvas>
    <canvas id="nc"></canvas>
  </div>
  <div class="leg" id="leg">
    <div class="li"><div class="ld" style="border-color:#4da3ff;background:#0d1a2e;"></div><span style="color:#4da3ff;">CORE</span></div>
    <div class="li"><div class="ld" style="border-color:#00cc33;background:#001a00;"></div><span style="color:#00cc33;">ACCESS</span></div>
    <div class="li"><div class="ld" style="border-color:#c0a000;background:#1a1400;"></div><span style="color:#c0a000;">DEVICE</span></div>
    <div class="li"><div class="ld" style="border-color:#cc3300;background:#1a0500;"></div><span style="color:#cc3300;">SECURITY</span></div>
  </div>
  <div class="il">{('> ' + last_user) if last_user else '> WAITING FOR PROJECT DESCRIPTION...'}</div>
</div>
<script>
const LAST='{last_user.replace("'", "\\'")}';
const cw=document.getElementById('cw');
const rc=document.getElementById('rc');
const nc=document.getElementById('nc');
const rx=rc.getContext('2d');
const nx=nc.getContext('2d');
const lbl=document.getElementById('lbl');
const sts=document.getElementById('sts');
const leg=document.getElementById('leg');

function rsz(){{const w=cw.offsetWidth,h=cw.offsetHeight;rc.width=nc.width=w;rc.height=nc.height=h;}}
rsz();window.addEventListener('resize',rsz);

const CH='アイウエオカキクケコ0123456789ABCDEF<>[]|/\\\\▸►';
let drops=[],rT=null,nT=null,pT=null,rph=0,cfg=null,prog=0,pp=0;

function iRain(){{const c=Math.floor(rc.width/11);drops=Array(c).fill(0).map(()=>Math.floor(Math.random()*-30));}}

function dRain(){{
  const w=rc.width,h=rc.height;
  rx.fillStyle='rgba(4,4,4,0.14)';rx.fillRect(0,0,w,h);
  drops.forEach((y,i)=>{{
    const ch=CH[Math.floor(Math.random()*CH.length)],x=i*11,r=Math.random();
    rx.fillStyle=r>.97?'#ffffff':r>.9?'#4da3ff':r>.55?'#00ff41':'#005511';
    rx.font='11px Share Tech Mono';rx.fillText(ch,x,y*13);
    if(y*13>h&&Math.random()>.97)drops[i]=0;else drops[i]++;
  }});
  rph++;
  if(rph===85){{clearInterval(rT);sts.textContent='RESOLVING...';setTimeout(()=>{{rx.clearRect(0,0,rc.width,rc.height);bNet();}},350);}}
}}

const EC={{core:'rgba(77,163,255,0.55)',access:'rgba(0,204,51,0.45)',device:'rgba(0,136,42,0.35)',security:'rgba(204,51,0,0.5)'}};
const NC={{core:'#4da3ff',access:'#00cc33',device:'#c0a000',security:'#cc3300'}};
const NB={{core:'#060d1a',access:'#030f03',device:'#0d0a00',security:'#0f0200'}};

const NETS={{
  hotel:{{label:'// HOTEL INFRASTRUCTURE',
    spine:[{{y:.07,t:'INTERNET UPLINK',c:'core',w:.30}},{{y:.17,t:'CORE ROUTER',c:'core',w:.25}},{{y:.27,t:'MANAGED SWITCH',c:'core',w:.25}}],
    rows:[
      {{y:.40,nodes:[{{x:.18,t:'FL 1\\nWIFI AP',c:'access'}},{{x:.50,t:'FL 2\\nWIFI AP',c:'access'}},{{x:.82,t:'FL 3\\nWIFI AP',c:'access'}}]}},
      {{y:.57,nodes:[{{x:.12,t:'ROOMS\\n1-15',c:'device'}},{{x:.35,t:'ROOMS\\n16-30',c:'device'}},{{x:.58,t:'ROOMS\\n31-50',c:'device'}},{{x:.82,t:'CONF\\nROOM',c:'device'}}]}},
      {{y:.75,nodes:[{{x:.22,t:'CCTV\\nNVR',c:'security'}},{{x:.50,t:'AV\\nSYSTEM',c:'device'}},{{x:.78,t:'ACCESS\\nCTRL',c:'security'}}]}}
    ],
    links:[[0,1],[1,2],[2,'r0n0'],[2,'r0n1'],[2,'r0n2'],['r0n0','r1n0'],['r0n1','r1n1'],['r0n1','r1n2'],['r0n2','r1n3'],[2,'r2n0'],[2,'r2n1'],[2,'r2n2']]
  }},
  cctv:{{label:'// CCTV SECURITY SYSTEM',
    spine:[{{y:.08,t:'NVR SERVER',c:'core',w:.24}},{{y:.20,t:'NETWORK SWITCH',c:'core',w:.26}}],
    rows:[
      {{y:.34,nodes:[{{x:.20,t:'ZONE A',c:'security'}},{{x:.50,t:'ZONE B',c:'security'}},{{x:.80,t:'ZONE C',c:'security'}}]}},
      {{y:.54,nodes:[{{x:.10,t:'ENTRY\\nCAM',c:'security'}},{{x:.28,t:'LOBBY\\nCAM',c:'security'}},{{x:.46,t:'HALL\\nCAM',c:'security'}},{{x:.64,t:'OFFICE\\nCAM',c:'security'}},{{x:.82,t:'EXIT\\nCAM',c:'security'}}]}},
      {{y:.76,nodes:[{{x:.28,t:'MONITOR\\nSTATION',c:'core'}},{{x:.72,t:'MOBILE\\nALERTS',c:'device'}}]}}
    ],
    links:[[0,1],[1,'r0n0'],[1,'r0n1'],[1,'r0n2'],['r0n0','r1n0'],['r0n0','r1n1'],['r0n1','r1n2'],['r0n2','r1n3'],['r0n2','r1n4'],[0,'r2n0'],[0,'r2n1']]
  }},
  home:{{label:'// SMART HOME SYSTEM',
    spine:[{{y:.07,t:'INTERNET / ISP',c:'core',w:.28}},{{y:.18,t:'HOME GATEWAY',c:'core',w:.24}}],
    rows:[
      {{y:.32,nodes:[{{x:.25,t:'SMART\\nHUB',c:'access'}},{{x:.75,t:'MESH\\nWIFI AP',c:'access'}}]}},
      {{y:.52,nodes:[{{x:.12,t:'SMART\\nLIGHTS',c:'device'}},{{x:.30,t:'THERMO-\\nSTAT',c:'device'}},{{x:.50,t:'DOOR\\nCAM',c:'security'}},{{x:.70,t:'SMART\\nLOCK',c:'security'}},{{x:.88,t:'SMART\\nTV/AV',c:'device'}}]}},
      {{y:.74,nodes:[{{x:.33,t:'MOBILE\\nAPP',c:'core'}},{{x:.67,t:'VOICE\\nASSIST',c:'core'}}]}}
    ],
    links:[[0,1],[1,'r0n0'],[1,'r0n1'],['r0n0','r1n0'],['r0n0','r1n1'],['r0n0','r1n2'],['r0n0','r1n3'],['r0n1','r1n4'],[1,'r2n0'],[1,'r2n1']]
  }},
  school:{{label:'// CAMPUS NETWORK',
    spine:[{{y:.07,t:'ISP UPLINK',c:'core',w:.22}},{{y:.18,t:'CAMPUS FIREWALL',c:'security',w:.26}},{{y:.29,t:'CORE SWITCH',c:'core',w:.22}}],
    rows:[
      {{y:.42,nodes:[{{x:.18,t:'CLASS\\nAP ZONE',c:'access'}},{{x:.50,t:'LIBRARY\\nAP ZONE',c:'access'}},{{x:.82,t:'ADMIN\\nAP ZONE',c:'access'}}]}},
      {{y:.60,nodes:[{{x:.12,t:'STUDENT\\nVLAN',c:'device'}},{{x:.35,t:'STAFF\\nVLAN',c:'device'}},{{x:.58,t:'CCTV\\nNET',c:'security'}},{{x:.82,t:'ADMIN\\nVLAN',c:'device'}}]}},
      {{y:.80,nodes:[{{x:.33,t:'PRINT\\nSERVER',c:'device'}},{{x:.67,t:'FILE\\nSERVER',c:'device'}}]}}
    ],
    links:[[0,1],[1,2],[2,'r0n0'],[2,'r0n1'],[2,'r0n2'],['r0n0','r1n0'],['r0n1','r1n1'],['r0n2','r1n2'],['r0n2','r1n3'],[2,'r2n0'],[2,'r2n1']]
  }},
  office:{{label:'// OFFICE INFRASTRUCTURE',
    spine:[{{y:.07,t:'INTERNET UPLINK',c:'core',w:.28}},{{y:.18,t:'UTM FIREWALL',c:'security',w:.24}},{{y:.29,t:'CORE SWITCH',c:'core',w:.22}}],
    rows:[
      {{y:.42,nodes:[{{x:.20,t:'OFFICE\\nWIFI AP',c:'access'}},{{x:.50,t:'SERVER\\nRACK',c:'core'}},{{x:.80,t:'CONF ROOM\\nAV',c:'access'}}]}},
      {{y:.60,nodes:[{{x:.15,t:'WORK-\\nSTATIONS',c:'device'}},{{x:.38,t:'NAS\\nSTORAGE',c:'device'}},{{x:.60,t:'IP\\nPHONES',c:'device'}},{{x:.83,t:'VIDEO\\nCONF',c:'device'}}]}},
      {{y:.80,nodes:[{{x:.28,t:'CCTV\\nSYSTEM',c:'security'}},{{x:.72,t:'ACCESS\\nCONTROL',c:'security'}}]}}
    ],
    links:[[0,1],[1,2],[2,'r0n0'],[2,'r0n1'],[2,'r0n2'],['r0n0','r1n0'],['r0n1','r1n1'],['r0n1','r1n2'],['r0n2','r1n3'],[2,'r2n0'],[2,'r2n1']]
  }},
  default:{{label:'// NETWORK INFRASTRUCTURE',
    spine:[{{y:.08,t:'INTERNET',c:'core',w:.20}},{{y:.22,t:'ROUTER / FIREWALL',c:'core',w:.28}}],
    rows:[
      {{y:.38,nodes:[{{x:.28,t:'SWITCH A',c:'access'}},{{x:.72,t:'SWITCH B',c:'access'}}]}},
      {{y:.58,nodes:[{{x:.14,t:'GROUP 1',c:'device'}},{{x:.38,t:'GROUP 2',c:'device'}},{{x:.62,t:'GROUP 3',c:'device'}},{{x:.86,t:'GROUP 4',c:'device'}}]}}
    ],
    links:[[0,1],[1,'r0n0'],[1,'r0n1'],['r0n0','r1n0'],['r0n0','r1n1'],['r0n1','r1n2'],['r0n1','r1n3']]
  }}
}};

function dType(m){{
  const s=(m||'').toLowerCase();
  if(s.includes('hotel')||s.includes('motel')||s.includes('hospitality')) return 'hotel';
  if(s.includes('camera')||s.includes('cctv')||s.includes('surveillance')) return 'cctv';
  if(s.includes('home')||s.includes('smart home')||s.includes('house')||s.includes('residential')) return 'home';
  if(s.includes('school')||s.includes('university')||s.includes('campus')||s.includes('college')) return 'school';
  if(s.includes('office')||s.includes('corporate')||s.includes('business')||s.includes('company')) return 'office';
  return 'default';
}}

function gPos(id,c,w,h){{
  if(typeof id==='number') return {{x:.5*w,y:c.spine[id].y*h}};
  const m=id.match(/r(\d+)n(\d+)/);
  if(m){{const r=c.rows[+m[1]],n=r.nodes[+m[2]];return {{x:n.x*w,y:r.y*h}};}}
  return {{x:.5*w,y:.5*h}};
}}

function draw(p){{
  const w=nc.width,h=nc.height;
  nx.clearRect(0,0,w,h);
  if(!cfg) return;
  const sf=cfg.spine.length,sr=cfg.rows.reduce((a,r)=>a+r.nodes.length,0),sl=cfg.links.length;
  const tot=sf+sr+sl;
  const sf2=Math.min(sf,Math.floor(p*tot*.45));
  const sr2=Math.min(sr,Math.floor(p*tot*.75)-sf);
  const sl2=Math.min(sl,Math.floor(p*sl*1.1));
  const gp=(pp%80)/80;

  cfg.links.slice(0,sl2).forEach(([a,b])=>{{
    try{{
      const pa=gPos(a,cfg,w,h),pb=gPos(b,cfg,w,h);
      const at=typeof a==='number'?cfg.spine[a].c:(cfg.rows[+String(a).match(/r(\d+)/)[1]].nodes[+String(a).match(/n(\d+)/)[1]].c);
      const cpx=(pa.x+pb.x)/2,cpy=(pa.y+pb.y)/2;
      nx.beginPath();nx.moveTo(pa.x,pa.y);
      nx.quadraticCurveTo(cpx,cpy,pb.x,pb.y);
      nx.strokeStyle=EC[at]||'rgba(0,255,65,.3)';
      nx.lineWidth=1.2;nx.setLineDash([4,6]);nx.stroke();nx.setLineDash([]);
      nx.fillStyle=EC[at];nx.font='9px Share Tech Mono';nx.textAlign='center';nx.fillText('▸',cpx,cpy+3);
    }}catch(e){{}}
  }});

  cfg.spine.slice(0,sf2).forEach((s)=>{{
    const x=.5*w,y=s.y*h,bw=s.w*w,bh=24;
    nx.shadowColor=NC[s.c];nx.shadowBlur=10*gp;
    nx.beginPath();nx.roundRect(x-bw/2,y-bh/2,bw,bh,5);
    nx.fillStyle=NB[s.c];nx.fill();
    nx.strokeStyle=NC[s.c];nx.lineWidth=1.5;nx.stroke();
    nx.shadowBlur=0;
    nx.fillStyle=NC[s.c];nx.font='8px Share Tech Mono';nx.textAlign='center';nx.fillText(s.t,x,y+3);
  }});

  let ni=0;
  cfg.rows.forEach((row)=>{{
    row.nodes.forEach((n)=>{{
      if(ni<sr2){{
        const x=n.x*w,y=row.y*h;
        nx.shadowColor=NC[n.c];nx.shadowBlur=8*gp;
        nx.beginPath();nx.arc(x,y,17,0,Math.PI*2);
        nx.fillStyle=NB[n.c];nx.fill();
        nx.strokeStyle=NC[n.c];nx.lineWidth=1.5;nx.stroke();
        nx.shadowBlur=0;
        nx.fillStyle=NC[n.c];nx.font='7px Share Tech Mono';nx.textAlign='center';
        const ls=n.t.split('\\n');
        if(ls.length>1){{nx.fillText(ls[0],x,y-2);nx.fillText(ls[1],x,y+7);}}
        else nx.fillText(n.t,x,y+3);
      }}
      ni++;
    }});
  }});
}}

function bNet(){{
  const t=dType(LAST);
  cfg=NETS[t];
  lbl.textContent=cfg.label;
  sts.textContent='BUILDING...';
  leg.style.display='flex';
  prog=0;
  nT=setInterval(()=>{{
    prog=Math.min(1,prog+.014);
    draw(prog);
    if(prog>=1){{clearInterval(nT);sts.textContent='COMPLETE';pT=setInterval(()=>{{pp++;draw(1);}},50);}}
  }},40);
}}

if(LAST){{sts.textContent='ANALYZING...';iRain();rph=0;rT=setInterval(dRain,40);}}
else{{lbl.textContent='// AWAITING INPUT';sts.textContent='STANDBY';}}
</script>
""", height=900, scrolling=False)

with st.sidebar:
    st.markdown("### 🌐 CRYSTALINK TECHNOLOGIES")
    st.markdown("**📍 DMV Area & Neighboring States**")
    st.markdown("**🌐** [crystalinktechnologies.com](https://crystalinktechnologies.com)")
    st.markdown("---")
    st.markdown("**// SERVICES ONLINE**")
    for s in ["📡 Network Installation","🔧 Network Upgrades & Repairs","📶 WiFi Infrastructure",
              "📷 Security Cameras / CCTV","🔌 Structured Cabling","🎬 AV Systems",
              "🏠 Smart Home / Automation","💼 IT Consulting"]:
        st.markdown(f"- {s}")
    st.markdown("---")
    st.markdown("**// WE SERVE**")
    st.markdown("Homeowners · Businesses · Hotels · Offices · Schools · Government · Retail")
    st.markdown("---")
    if st.button("🗑️ CLEAR CHAT", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted = False
        st.session_state.last_msg = ""
        st.rerun()
