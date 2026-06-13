import os
import anthropic
import streamlit as st
from system_prompt import SYSTEM_PROMPT

# ── API Client ────────────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CrystalInk Technologies AI Assistant",
    page_icon="🌐",
    layout="wide"
)

# ── Full CSS + Matrix UI ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace !important;
    background-color: #080808 !important;
    color: #00cc33 !important;
}
.stApp { background-color: #080808 !important; }
section[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #0d3a6e !important;
}
section[data-testid="stSidebar"] * { color: #4da3ff !important; font-family: 'Share Tech Mono', monospace !important; }
.stChatMessage { background: transparent !important; }
.stChatMessage[data-testid*="user"] .stChatMessageContent {
    background: #0d3a6e !important;
    border: 1px solid #1a6fd4 !important;
    color: #cce4ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 6px !important;
}
.stChatMessage[data-testid*="assistant"] .stChatMessageContent {
    background: #0a140a !important;
    border: 1px solid #003b0f !important;
    color: #00cc33 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 6px !important;
}
.stChatInputContainer {
    background: #050505 !important;
    border-top: 1px solid #0d3a6e !important;
}
.stChatInputContainer textarea {
    background: #0d0d0d !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border: 1px solid #0d3a6e !important;
}
.stButton button {
    background: transparent !important;
    border: 1px solid #0d3a6e !important;
    color: #4da3ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 1px !important;
}
.stButton button:hover {
    background: #0d3a6e !important;
    border-color: #1a6fd4 !important;
}
.stSpinner { color: #00ff41 !important; }
div[data-testid="stMarkdownContainer"] p { color: #00cc33 !important; }
h1,h2,h3 { color: #4da3ff !important; font-family: 'Share Tech Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#060d1a;border-bottom:2px solid #1a6fd4;padding:14px 20px;
margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;
border-radius:8px;">
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:34px;height:34px;border-radius:7px;background:#0d3a6e;
        border:1.5px solid #1a6fd4;display:flex;align-items:center;justify-content:center;font-size:16px;">🌐</div>
        <div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:16px;
            color:#4da3ff;letter-spacing:3px;">CRYSTALINK TECHNOLOGIES</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;
            color:#00aa2a;letter-spacing:2px;">CONNECTING YOUR WORLD, ONE NETWORK AT A TIME</div>
        </div>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#00ff41;letter-spacing:2px;">
        ● AI ASSISTANT ONLINE // 24/7
    </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: Chat left, Matrix animation right ─────────────────────────────────
chat_col, anim_col = st.columns([1.1, 0.9])

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greeted = False
if "last_msg" not in st.session_state:
    st.session_state.last_msg = ""

# ── Greeting ──────────────────────────────────────────────────────────────────
if not st.session_state.greeted:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "// CRYSTALINK.AI ONLINE\n\nWelcome. I'm your CrystalInk Technologies assistant. "
                   "Describe your project and watch the matrix build your network diagram in real time.\n\n"
                   "We cover network installation, WiFi infrastructure, security cameras, AV systems, "
                   "structured cabling, smart home, and IT consulting — across the DMV and beyond.\n\n"
                   "What can I help you with today?"
    })
    st.session_state.greeted = True

# ── CHAT COLUMN ───────────────────────────────────────────────────────────────
with chat_col:
    # Quick buttons
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:9px;color:#1a6fd4;letter-spacing:2px;margin-bottom:6px;'>// QUICK SELECT</div>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("🏨 HOTEL", use_container_width=True):
            st.session_state.last_msg = "I need WiFi and tech upgrade for a 50 room hotel"
            st.rerun()
    with q2:
        if st.button("📷 CCTV", use_container_width=True):
            st.session_state.last_msg = "Security cameras for my office building"
            st.rerun()
    with q3:
        if st.button("🏠 HOME", use_container_width=True):
            st.session_state.last_msg = "Smart home setup with WiFi and automation"
            st.rerun()
    with q4:
        if st.button("🏫 SCHOOL", use_container_width=True):
            st.session_state.last_msg = "Network infrastructure for my school campus"
            st.rerun()

    st.markdown("<div style='border-top:1px solid #111;margin:8px 0;'></div>", unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🌐" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Handle quick button trigger
    if st.session_state.last_msg:
        user_input = st.session_state.last_msg
        st.session_state.last_msg = ""
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🌐"):
            with st.spinner("// PROCESSING..."):
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ["user", "assistant"]
                ]
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=api_messages
                )
                reply = response.content[0].text
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.anim_trigger = user_input
        st.rerun()

    # Chat input
    if user_input := st.chat_input("> DESCRIBE YOUR PROJECT OR ASK A QUESTION..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🌐"):
            with st.spinner("// PROCESSING..."):
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ["user", "assistant"]
                ]
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=api_messages
                )
                reply = response.content[0].text
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.anim_trigger = user_input
        st.rerun()

# ── ANIMATION COLUMN ──────────────────────────────────────────────────────────
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
.wrap{{font-family:'Share Tech Mono',monospace;background:#050505;border:1px solid #0d3a6e;
border-radius:8px;overflow:hidden;height:580px;display:flex;flex-direction:column;}}
.anim-header{{padding:8px 12px;background:#060d1a;border-bottom:1px solid #0d3a6e;
display:flex;align-items:center;justify-content:space-between;}}
.anim-title{{font-size:9px;color:#1a6fd4;letter-spacing:2px;}}
.anim-status{{font-size:9px;color:#00ff41;letter-spacing:1px;}}
.canvas-wrap{{flex:1;position:relative;}}
canvas{{position:absolute;top:0;left:0;width:100%;height:100%;}}
.net-canvas{{z-index:5;}}
.rain-canvas{{z-index:4;}}
.input-label{{padding:8px 12px;background:#060d1a;border-top:1px solid #0d3a6e;
font-size:9px;color:#00aa2a;letter-spacing:1px;min-height:36px;}}
</style>
<div class="wrap">
  <div class="anim-header">
    <div class="anim-title" id="diagLabel">// AWAITING INPUT</div>
    <div class="anim-status" id="diagStatus">STANDBY</div>
  </div>
  <div class="canvas-wrap" id="canvasWrap">
    <canvas id="rainCanvas"></canvas>
    <canvas id="netCanvas" class="net-canvas"></canvas>
  </div>
  <div class="input-label" id="inputLabel">{'> ' + last_user if last_user else '> WAITING FOR PROJECT DESCRIPTION...'}</div>
</div>
<script>
const LAST_MSG = {repr(last_user)};
const wrap = document.getElementById('canvasWrap');
const rainC = document.getElementById('rainCanvas');
const netC = document.getElementById('netCanvas');
const rCtx = rainC.getContext('2d');
const nCtx = netC.getContext('2d');
const labelEl = document.getElementById('diagLabel');
const statusEl = document.getElementById('diagStatus');

function resize(){{
  const w=wrap.offsetWidth, h=wrap.offsetHeight;
  rainC.width=netC.width=w; rainC.height=netC.height=h;
}}
resize();
window.addEventListener('resize', resize);

const CHARS='アイウエオカキクケコ0123456789ABCDEF<>[]{{}}|/\\\\';
let drops=[], rainTimer=null, netTimer=null, rainPhase=0;

function initRain(){{
  const cols=Math.floor(rainC.width/12);
  drops=Array(cols).fill(0).map(()=>Math.floor(Math.random()*rainC.height/14));
}}

function drawRain(){{
  const w=rainC.width, h=rainC.height;
  rCtx.fillStyle='rgba(5,5,5,0.18)';
  rCtx.fillRect(0,0,w,h);
  rCtx.font='12px Share Tech Mono';
  drops.forEach((y,i)=>{{
    const ch=CHARS[Math.floor(Math.random()*CHARS.length)];
    const x=i*12;
    const bright=Math.random()>0.92;
    rCtx.fillStyle=bright?'#4da3ff':'#00ff41';
    rCtx.fillText(ch,x,y*14);
    if(y*14>h&&Math.random()>0.975) drops[i]=0; else drops[i]++;
  }});
  rainPhase++;
  if(rainPhase===70){{
    clearInterval(rainTimer);
    statusEl.textContent='RESOLVING...';
    setTimeout(()=>{{ rCtx.clearRect(0,0,w,h); startNetwork(); }}, 300);
  }}
}}

const NETS={{
  hotel:{{
    label:'// HOTEL NETWORK DIAGRAM',
    nodes:[
      {{x:.5,y:.08,t:'INTERNET',c:'#4da3ff',r:13}},
      {{x:.5,y:.22,t:'CORE ROUTER',c:'#4da3ff',r:11}},
      {{x:.2,y:.38,t:'FLOOR 1 AP',c:'#00cc33',r:9}},
      {{x:.5,y:.38,t:'FLOOR 2 AP',c:'#00cc33',r:9}},
      {{x:.8,y:.38,t:'FLOOR 3 AP',c:'#00cc33',r:9}},
      {{x:.15,y:.6,t:'ROOMS 1-15',c:'#00882a',r:7}},
      {{x:.5,y:.6,t:'ROOMS 16-35',c:'#00882a',r:7}},
      {{x:.85,y:.6,t:'ROOMS 36-50',c:'#00882a',r:7}},
      {{x:.3,y:.82,t:'CCTV NVR',c:'#c0a000',r:8}},
      {{x:.7,y:.82,t:'AV SYSTEM',c:'#c0a000',r:8}},
    ],
    edges:[[0,1],[1,2],[1,3],[1,4],[2,5],[3,6],[4,7],[1,8],[1,9]]
  }},
  cctv:{{
    label:'// CCTV SECURITY DIAGRAM',
    nodes:[
      {{x:.5,y:.1,t:'NVR SERVER',c:'#4da3ff',r:13}},
      {{x:.2,y:.32,t:'ZONE A',c:'#00cc33',r:10}},
      {{x:.5,y:.32,t:'ZONE B',c:'#00cc33',r:10}},
      {{x:.8,y:.32,t:'ZONE C',c:'#00cc33',r:10}},
      {{x:.1,y:.58,t:'ENTRY CAM',c:'#c0a000',r:7}},
      {{x:.3,y:.58,t:'LOBBY CAM',c:'#c0a000',r:7}},
      {{x:.5,y:.58,t:'HALL CAM',c:'#c0a000',r:7}},
      {{x:.7,y:.58,t:'OFFICE CAM',c:'#c0a000',r:7}},
      {{x:.9,y:.58,t:'EXIT CAM',c:'#c0a000',r:7}},
      {{x:.5,y:.82,t:'MONITOR',c:'#4da3ff',r:11}},
    ],
    edges:[[0,1],[0,2],[0,3],[1,4],[1,5],[2,6],[3,7],[3,8],[0,9]]
  }},
  home:{{
    label:'// SMART HOME DIAGRAM',
    nodes:[
      {{x:.5,y:.1,t:'HOME ROUTER',c:'#4da3ff',r:12}},
      {{x:.25,y:.3,t:'SMART HUB',c:'#00cc33',r:10}},
      {{x:.75,y:.3,t:'MESH AP',c:'#00cc33',r:10}},
      {{x:.1,y:.58,t:'LIGHTS',c:'#c0a000',r:7}},
      {{x:.3,y:.58,t:'THERMOSTAT',c:'#c0a000',r:7}},
      {{x:.5,y:.58,t:'DOORBELL',c:'#c0a000',r:7}},
      {{x:.7,y:.58,t:'CAMERAS',c:'#c0a000',r:7}},
      {{x:.9,y:.58,t:'TV/AV',c:'#c0a000',r:7}},
      {{x:.5,y:.82,t:'MOBILE APP',c:'#4da3ff',r:10}},
    ],
    edges:[[0,1],[0,2],[1,3],[1,4],[1,5],[2,6],[2,7],[0,8]]
  }},
  school:{{
    label:'// CAMPUS NETWORK DIAGRAM',
    nodes:[
      {{x:.5,y:.08,t:'ISP UPLINK',c:'#4da3ff',r:12}},
      {{x:.5,y:.24,t:'CORE SWITCH',c:'#4da3ff',r:11}},
      {{x:.2,y:.42,t:'CLASSROOM',c:'#00cc33',r:9}},
      {{x:.5,y:.42,t:'LIBRARY',c:'#00cc33',r:9}},
      {{x:.8,y:.42,t:'ADMIN',c:'#00cc33',r:9}},
      {{x:.15,y:.65,t:'STUDENT NET',c:'#00882a',r:7}},
      {{x:.4,y:.65,t:'STAFF NET',c:'#00882a',r:7}},
      {{x:.65,y:.65,t:'CCTV NET',c:'#c0a000',r:7}},
      {{x:.85,y:.65,t:'ADMIN NET',c:'#00882a',r:7}},
      {{x:.5,y:.85,t:'FIREWALL',c:'#4da3ff',r:11}},
    ],
    edges:[[0,1],[1,2],[1,3],[1,4],[2,5],[3,6],[4,7],[4,8],[1,9]]
  }},
  office:{{
    label:'// OFFICE NETWORK DIAGRAM',
    nodes:[
      {{x:.5,y:.08,t:'INTERNET',c:'#4da3ff',r:13}},
      {{x:.5,y:.24,t:'FIREWALL',c:'#c0a000',r:11}},
      {{x:.5,y:.4,t:'CORE SWITCH',c:'#4da3ff',r:11}},
      {{x:.2,y:.58,t:'OFFICE AP',c:'#00cc33',r:9}},
      {{x:.5,y:.58,t:'SERVER RACK',c:'#4da3ff',r:9}},
      {{x:.8,y:.58,t:'CONF ROOM AV',c:'#00cc33',r:9}},
      {{x:.2,y:.78,t:'WORKSTATIONS',c:'#00882a',r:7}},
      {{x:.5,y:.78,t:'STORAGE NAS',c:'#00882a',r:7}},
      {{x:.8,y:.78,t:'VIDEO SYSTEM',c:'#00882a',r:7}},
    ],
    edges:[[0,1],[1,2],[2,3],[2,4],[2,5],[3,6],[4,7],[5,8]]
  }},
  default:{{
    label:'// NETWORK DIAGRAM',
    nodes:[
      {{x:.5,y:.1,t:'INTERNET',c:'#4da3ff',r:13}},
      {{x:.5,y:.3,t:'ROUTER',c:'#4da3ff',r:11}},
      {{x:.25,y:.5,t:'SWITCH A',c:'#00cc33',r:9}},
      {{x:.75,y:.5,t:'SWITCH B',c:'#00cc33',r:9}},
      {{x:.1,y:.72,t:'DEVICE 1',c:'#00882a',r:7}},
      {{x:.35,y:.72,t:'DEVICE 2',c:'#00882a',r:7}},
      {{x:.65,y:.72,t:'DEVICE 3',c:'#00882a',r:7}},
      {{x:.9,y:.72,t:'DEVICE 4',c:'#00882a',r:7}},
    ],
    edges:[[0,1],[1,2],[1,3],[2,4],[2,5],[3,6],[3,7]]
  }}
}};

function detectType(msg){{
  const m=(msg||'').toLowerCase();
  if(m.includes('hotel')||m.includes('motel')||m.includes('hospitality')) return 'hotel';
  if(m.includes('camera')||m.includes('cctv')||m.includes('surveillance')||m.includes('security cam')) return 'cctv';
  if(m.includes('home')||m.includes('smart')||m.includes('house')||m.includes('apartment')) return 'home';
  if(m.includes('school')||m.includes('university')||m.includes('campus')||m.includes('college')) return 'school';
  if(m.includes('office')||m.includes('corporate')||m.includes('business')||m.includes('conference')) return 'office';
  return 'default';
}}

let netConfig=null, netProgress=0;

function startNetwork(){{
  const type=detectType(LAST_MSG);
  netConfig=NETS[type];
  labelEl.textContent=netConfig.label;
  statusEl.textContent='BUILDING...';
  netProgress=0;
  netTimer=setInterval(()=>{{
    netProgress=Math.min(1,netProgress+0.02);
    drawNet(netProgress);
    if(netProgress>=1){{ clearInterval(netTimer); statusEl.textContent='COMPLETE'; }}
  }},40);
}}

function drawNet(p){{
  const w=netC.width, h=netC.height;
  nCtx.clearRect(0,0,w,h);
  if(!netConfig) return;
  const {{nodes,edges}}=netConfig;
  const total=edges.length+nodes.length;
  const edgesDone=Math.floor(p*edges.length*1.5);
  const nodesDone=Math.floor(p*nodes.length*1.5);

  edges.slice(0,edgesDone).forEach(([a,b])=>{{
    const na=nodes[a], nb=nodes[b];
    const x1=na.x*w, y1=na.y*h, x2=nb.x*w, y2=nb.y*h;
    nCtx.beginPath();
    nCtx.moveTo(x1,y1); nCtx.lineTo(x2,y2);
    nCtx.strokeStyle='rgba(0,255,65,0.25)';
    nCtx.lineWidth=1; nCtx.setLineDash([3,5]); nCtx.stroke();
    nCtx.setLineDash([]);
    const mx=(x1+x2)/2, my=(y1+y2)/2;
    nCtx.fillStyle='rgba(77,163,255,0.7)';
    nCtx.font='9px Share Tech Mono';
    nCtx.textAlign='center';
    nCtx.fillText('▸',mx,my);
  }});

  nodes.slice(0,Math.min(nodesDone+1,nodes.length)).forEach((n)=>{{
    const x=n.x*w, y=n.y*h;
    nCtx.beginPath();
    nCtx.arc(x,y,n.r,0,Math.PI*2);
    nCtx.fillStyle='#080808'; nCtx.fill();
    nCtx.strokeStyle=n.c; nCtx.lineWidth=1.5; nCtx.stroke();
    nCtx.fillStyle=n.c;
    nCtx.font=`${{Math.max(7,n.r*0.75)}}px Share Tech Mono`;
    nCtx.textAlign='center';
    nCtx.fillText(n.t,x,y+n.r+10);
  }});
}}

if(LAST_MSG){{
  statusEl.textContent='ANALYZING...';
  initRain();
  rainPhase=0;
  rainTimer=setInterval(drawRain,40);
}} else {{
  labelEl.textContent='// AWAITING INPUT';
  statusEl.textContent='STANDBY';
}}
</script>
""", height=620, scrolling=False)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 CRYSTALINK TECHNOLOGIES")
    st.markdown("**📍 DMV Area & Neighboring States**")
    st.markdown("**🌐** [crystalinktechnologies.com](https://crystalinktechnologies.com)")
    st.markdown("---")
    st.markdown("**// SERVICES ONLINE**")
    services = [
        "📡 Network Installation",
        "🔧 Network Upgrades & Repairs",
        "📶 WiFi Infrastructure",
        "📷 Security Cameras / CCTV",
        "🔌 Structured Cabling",
        "🎬 AV Systems",
        "🏠 Smart Home / Automation",
        "💼 IT Consulting",
    ]
    for s in services:
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
