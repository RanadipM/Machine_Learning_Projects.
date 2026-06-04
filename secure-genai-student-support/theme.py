"""
UI theme — custom CSS + reusable HTML components for a premium,
'security operations console' aesthetic. Imported by app.py.

Design direction: refined technical / fintech-SOC.
- Deep slate-navy canvas with an electric cyan accent.
- Display font 'Sora' paired with body 'Inter' (loaded from Google Fonts).
- Glassmorphic cards, soft depth, restrained motion (staggered fade-in).
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
  --navy-900:#0b1220;
  --navy-800:#111c30;
  --navy-700:#16243d;
  --line:rgba(120,160,210,.16);
  --ink:#e8eef7;
  --muted:#9fb1c9;
  --cyan:#3ad1c8;
  --cyan-2:#37b6f6;
  --amber:#f6b73c;
  --rose:#f87a7a;
  --green:#4ad991;
}

/* ---------- base ---------- */
html, body, [class*="css"], .stApp{
  font-family:'Inter',system-ui,sans-serif;
}
.stApp{
  background:
    radial-gradient(900px 500px at 12% -8%, rgba(55,182,246,.10), transparent 60%),
    radial-gradient(900px 500px at 100% 0%, rgba(58,209,200,.08), transparent 55%),
    linear-gradient(180deg,#0b1220 0%, #0d1626 100%);
  color:var(--ink);
}
.block-container{padding-top:1.4rem; max-width:1180px;}

h1,h2,h3,h4{font-family:'Sora',sans-serif; letter-spacing:-.01em; color:var(--ink);}
p, li, span, label{color:var(--ink);}
.stCaption, .stMarkdown small{color:var(--muted)!important;}
a{color:var(--cyan-2);}

/* ---------- hero ---------- */
.hero{
  position:relative; overflow:hidden;
  border:1px solid var(--line);
  border-radius:20px;
  padding:30px 34px;
  background:
    radial-gradient(700px 240px at 88% -40%, rgba(58,209,200,.22), transparent 60%),
    linear-gradient(135deg, rgba(22,36,61,.92), rgba(13,22,38,.92));
  box-shadow:0 24px 60px -28px rgba(0,0,0,.7), inset 0 1px 0 rgba(255,255,255,.04);
  animation:rise .6s cubic-bezier(.2,.7,.2,1) both;
}
.hero::after{
  content:""; position:absolute; inset:0;
  background:repeating-linear-gradient(135deg, rgba(255,255,255,.018) 0 2px, transparent 2px 9px);
  pointer-events:none;
}
.hero .eyebrow{
  font-family:'JetBrains Mono',monospace; font-size:11.5px; letter-spacing:.22em;
  text-transform:uppercase; color:var(--cyan);
  display:inline-flex; align-items:center; gap:8px;
}
.hero .eyebrow::before{content:""; width:8px; height:8px; border-radius:50%;
  background:var(--cyan); box-shadow:0 0 0 4px rgba(58,209,200,.18); display:inline-block;}
.hero h1{font-size:34px; line-height:1.08; margin:12px 0 8px; font-weight:800;}
.hero h1 .grad{
  background:linear-gradient(90deg,var(--cyan),var(--cyan-2));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.hero p.sub{color:var(--muted); font-size:15px; margin:0; max-width:680px;}
.pillrow{margin-top:16px; display:flex; flex-wrap:wrap; gap:8px;}
.pill{
  font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.04em;
  color:var(--ink); background:rgba(58,209,200,.08);
  border:1px solid var(--line); padding:5px 11px; border-radius:999px;
  transition:.25s; backdrop-filter:blur(4px);
}
.pill:hover{transform:translateY(-2px); border-color:rgba(58,209,200,.5); background:rgba(58,209,200,.16);}

@keyframes rise{from{opacity:0; transform:translateY(14px);} to{opacity:1; transform:none;}}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"]{
  gap:6px; background:rgba(17,28,48,.6); padding:6px; border-radius:14px;
  border:1px solid var(--line);
}
.stTabs [data-baseweb="tab"]{
  height:42px; border-radius:10px; color:var(--muted);
  font-family:'Sora',sans-serif; font-weight:600; font-size:14px; padding:0 16px;
  background:transparent; transition:.2s;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--ink); background:rgba(58,209,200,.07);}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg, rgba(58,209,200,.22), rgba(55,182,246,.18))!important;
  color:#fff!important; border:1px solid rgba(58,209,200,.4);
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0c1626,#0a1322);
  border-right:1px solid var(--line);
}
section[data-testid="stSidebar"] .stMarkdown h3{color:var(--cyan);}

/* ---------- inputs ---------- */
.stTextInput input, .stSelectbox div[data-baseweb="select"]>div, .stChatInput textarea{
  background:rgba(11,18,32,.7)!important; color:var(--ink)!important;
  border:1px solid var(--line)!important; border-radius:10px!important;
}
.stTextInput input:focus, .stChatInput textarea:focus{
  border-color:var(--cyan)!important; box-shadow:0 0 0 3px rgba(58,209,200,.15)!important;
}

/* ---------- buttons ---------- */
.stButton>button{
  background:linear-gradient(135deg, rgba(58,209,200,.16), rgba(55,182,246,.12));
  color:var(--ink); border:1px solid var(--line); border-radius:11px;
  font-family:'Sora',sans-serif; font-weight:600; font-size:13px;
  transition:.22s; box-shadow:0 6px 18px -12px rgba(58,209,200,.6);
}
.stButton>button:hover{
  transform:translateY(-2px); border-color:rgba(58,209,200,.55);
  background:linear-gradient(135deg, rgba(58,209,200,.28), rgba(55,182,246,.2));
  color:#fff;
}

/* ---------- chat ---------- */
[data-testid="stChatMessage"]{
  background:rgba(17,28,48,.55); border:1px solid var(--line);
  border-radius:14px; padding:6px 14px; backdrop-filter:blur(6px);
  animation:rise .4s ease both;
}

/* ---------- expanders & dataframes ---------- */
.streamlit-expanderHeader, details summary{
  background:rgba(17,28,48,.6)!important; border-radius:10px!important;
  color:var(--ink)!important; border:1px solid var(--line)!important;
}
[data-testid="stExpander"]{border:none;}
[data-testid="stDataFrame"]{border:1px solid var(--line); border-radius:12px; overflow:hidden;}

/* ---------- generic card + stat ---------- */
.card{
  border:1px solid var(--line); border-radius:16px; padding:18px 20px;
  background:linear-gradient(135deg, rgba(22,36,61,.7), rgba(13,22,38,.7));
  box-shadow:0 18px 44px -30px rgba(0,0,0,.8);
}
.statgrid{display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:4px 0 6px;}
.stat{
  border:1px solid var(--line); border-radius:14px; padding:14px 16px;
  background:linear-gradient(135deg, rgba(22,36,61,.7), rgba(13,22,38,.6));
  transition:.25s; animation:rise .5s ease both;
}
.stat:hover{transform:translateY(-3px); border-color:rgba(58,209,200,.4);}
.stat .num{font-family:'Sora',sans-serif; font-weight:800; font-size:24px;
  background:linear-gradient(90deg,var(--cyan),var(--cyan-2));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;}
.stat .lbl{font-size:11.5px; color:var(--muted); letter-spacing:.03em; margin-top:3px;}
.stat:nth-child(2){animation-delay:.06s} .stat:nth-child(3){animation-delay:.12s} .stat:nth-child(4){animation-delay:.18s}

.flowstep{display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin:8px 0 4px;}
.chip{font-family:'JetBrains Mono',monospace; font-size:11.5px; color:var(--ink);
  border:1px solid var(--line); border-radius:999px; padding:5px 12px;
  background:rgba(58,209,200,.08);}
.chip.act{background:linear-gradient(135deg, rgba(58,209,200,.26), rgba(55,182,246,.2)); border-color:rgba(58,209,200,.5); color:#fff;}
.arrow{color:var(--cyan); font-weight:700;}

/* footer */
.foot{color:var(--muted); font-size:12px; text-align:center; margin-top:22px;
  font-family:'JetBrains Mono',monospace; letter-spacing:.04em;}
[data-testid="stHeader"]{background:transparent;}
#MainMenu, footer{visibility:hidden;}
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def hero():
    st.markdown(
        """
        <div class="hero">
          <span class="eyebrow">AI · Cybersecurity · System Design</span>
          <h1>Secure <span class="grad">GenAI Student-Support</span> Platform</h1>
          <p class="sub">A multi-agent + RAG assistant with security guardrails engineered in —
          input defense, RBAC, PII redaction, and live audit logging. Designed, built, and
          deployable on HuggingFace Spaces &amp; Streamlit Cloud.</p>
          <div class="pillrow">
            <span class="pill">Supervisor Routing</span>
            <span class="pill">RAG Grounding</span>
            <span class="pill">Prompt-Injection Defense</span>
            <span class="pill">RBAC</span>
            <span class="pill">TLS / Zero-Trust</span>
            <span class="pill">SIEM Logging</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def flow_strip(active: str | None = None):
    steps = [("Guardrail", "guardrail"), ("Route", "route"),
             ("RAG", "rag"), ("Generate", "gen"), ("Redact", "redact")]
    html = '<div class="flowstep">'
    for i, (label, key) in enumerate(steps):
        cls = "chip act" if key == active else "chip"
        html += f'<span class="{cls}">{label}</span>'
        if i < len(steps) - 1:
            html += '<span class="arrow">→</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def stat_grid(items):
    """items: list of (number, label)."""
    cells = "".join(
        f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>'
        for n, l in items
    )
    st.markdown(f'<div class="statgrid">{cells}</div>', unsafe_allow_html=True)
