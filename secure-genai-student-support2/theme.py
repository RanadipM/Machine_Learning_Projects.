"""
UI theme — premium 'security operations console' design system.

Aesthetic: refined technical / SOC-dashboard.
- Deep slate-navy canvas, electric cyan + sky-blue accents, signal colors.
- Display font 'Space Grotesk', body 'Inter', mono 'JetBrains Mono'.
- Glassmorphic cards, gradient mesh background, grain, staggered reveals.

All helpers use Python 3.9+ compatible typing (no PEP 604 unions).
"""

from typing import Optional, List, Tuple
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --bg:#13102a; --bg-2:#1a1640; --panel:#221c4d; --panel-2:#1d1843;
  --line:rgba(167,150,255,.20); --line-2:rgba(167,150,255,.36);
  --ink:#f6f3ff; --muted:#c2b8e8; --faint:#8b7fc0;
  --cyan:#2ee6c6; --sky:#7c6cff; --amber:#ffb347; --rose:#ff6f91;
  --green:#3fe0a0; --violet:#a78bfa;
  --teal:#2ee6c6; --coral:#ff6f91;
}

html, body, [class*="css"], .stApp{ font-family:'Inter',system-ui,sans-serif; }

.stApp{
  background:
    radial-gradient(1200px 640px at 5% -12%, rgba(124,108,255,.28), transparent 56%),
    radial-gradient(1100px 600px at 100% -8%, rgba(46,230,198,.18), transparent 52%),
    radial-gradient(900px 700px at 60% 120%, rgba(255,111,145,.14), transparent 58%),
    radial-gradient(700px 500px at 85% 60%, rgba(167,139,250,.12), transparent 60%),
    linear-gradient(165deg,#13102a 0%, #181340 55%, #14112e 100%);
  color:var(--ink);
}
.stApp::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.4;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.025'/%3E%3C/svg%3E");
}
.block-container{padding-top:1.2rem; max-width:1240px; position:relative; z-index:1;}

h1,h2,h3,h4{font-family:'Space Grotesk',sans-serif; letter-spacing:-.02em; color:var(--ink);}
.block-container h2{font-size:25px!important;} .block-container h3{font-size:20px!important;}
p, li, span, label{color:var(--ink);}
.stCaption, .stMarkdown small{color:var(--muted)!important;}
a{color:var(--sky);}

/* HERO */
.hero{position:relative; overflow:hidden; border:1px solid var(--line-2); border-radius:26px;
  padding:46px 46px 40px;
  background:
    radial-gradient(680px 260px at 92% -34%, rgba(46,230,198,.30), transparent 62%),
    radial-gradient(560px 240px at 8% 128%, rgba(255,111,145,.22), transparent 60%),
    radial-gradient(520px 300px at 50% 140%, rgba(124,108,255,.20), transparent 62%),
    linear-gradient(135deg, rgba(34,28,77,.95), rgba(26,22,64,.95));
  box-shadow:0 30px 70px -34px rgba(0,0,0,.8), inset 0 1px 0 rgba(255,255,255,.05);
  animation:rise .7s cubic-bezier(.2,.7,.2,1) both;}
.hero::after{content:""; position:absolute; inset:0; pointer-events:none;
  background:repeating-linear-gradient(135deg, rgba(255,255,255,.016) 0 2px, transparent 2px 10px);}
.hero .eyebrow{font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.26em;
  text-transform:uppercase; color:var(--cyan); display:inline-flex; align-items:center; gap:9px;}
.hero .eyebrow::before{content:""; width:7px; height:7px; border-radius:50%; background:var(--cyan);
  box-shadow:0 0 0 4px rgba(53,224,210,.16); animation:pulse 2.4s ease-in-out infinite;}
.hero h1{font-size:50px; line-height:1.02; margin:18px 0 14px; font-weight:700;}
.hero h1 .grad{background:linear-gradient(95deg,var(--teal),var(--violet) 55%,var(--coral));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;}
.hero p.sub{color:var(--muted); font-size:17px; margin:0; max-width:760px; line-height:1.6;}
.pillrow{margin-top:18px; display:flex; flex-wrap:wrap; gap:8px;}
.pill{font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:.03em; color:var(--ink);
  background:rgba(46,230,198,.10); border:1px solid var(--line-2); padding:7px 14px; border-radius:999px;
  transition:.25s; backdrop-filter:blur(4px);}
.pill:hover{transform:translateY(-2px); border-color:rgba(53,224,210,.5); background:rgba(53,224,210,.15);}
.live-badge{position:absolute; top:22px; right:26px; font-family:'JetBrains Mono',monospace;
  font-size:10.5px; letter-spacing:.12em; color:var(--green); border:1px solid rgba(70,224,138,.4);
  background:rgba(70,224,138,.08); padding:5px 11px 5px 9px; border-radius:999px; display:flex;
  align-items:center; gap:7px;}
.live-badge .dot{width:7px; height:7px; border-radius:50%; background:var(--green);
  box-shadow:0 0 0 0 rgba(70,224,138,.6); animation:ping 1.8s ease-out infinite;}

@keyframes rise{from{opacity:0; transform:translateY(16px);} to{opacity:1; transform:none;}}
@keyframes pulse{0%,100%{opacity:1;} 50%{opacity:.45;}}
@keyframes ping{0%{box-shadow:0 0 0 0 rgba(70,224,138,.5);} 70%{box-shadow:0 0 0 8px rgba(70,224,138,0);} 100%{box-shadow:0 0 0 0 rgba(70,224,138,0);}}

/* STAT GRID */
.statgrid{display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:18px 0 6px;}
.stat{position:relative; border:1px solid var(--line-2); border-radius:18px; padding:22px 22px;
  background:linear-gradient(150deg, rgba(20,33,57,.8), rgba(12,20,36,.7));
  transition:.28s; animation:rise .55s ease both; overflow:hidden;}
.stat::before{content:""; position:absolute; left:0; top:0; bottom:0; width:4px;
  background:linear-gradient(180deg,var(--teal),var(--violet)); opacity:1;}
.stat:hover{transform:translateY(-5px); border-color:var(--teal);
  box-shadow:0 22px 48px -24px rgba(46,230,198,.55);}
.stat .num{font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:21px; white-space:nowrap;
  background:linear-gradient(95deg,var(--teal),var(--violet));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;}
.stat .lbl{font-size:12.5px; color:var(--muted); letter-spacing:.02em; margin-top:5px;}
.stat:nth-child(2){animation-delay:.06s} .stat:nth-child(3){animation-delay:.12s} .stat:nth-child(4){animation-delay:.18s}

/* PIPELINE */
.pipe{display:flex; align-items:stretch; gap:0; margin:10px 0 2px; flex-wrap:wrap;}
.pipe-step{position:relative; flex:1; min-width:120px; border:1px solid var(--line); border-radius:13px;
  padding:11px 12px 10px; margin:3px; background:linear-gradient(150deg, rgba(18,30,52,.6), rgba(11,19,34,.5));
  transition:.25s;}
.pipe-step .k{font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:.16em;
  color:var(--faint); text-transform:uppercase;}
.pipe-step .t{font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:12.5px; margin-top:3px; color:var(--ink);}
.pipe-step.done{border-color:rgba(70,224,138,.4); background:rgba(70,224,138,.06);}
.pipe-step.done .k{color:var(--green);}
.pipe-step.act{border-color:var(--teal); background:rgba(46,230,198,.12);
  box-shadow:0 0 0 3px rgba(46,230,198,.14); animation:glow 1.4s ease-in-out infinite;}
.pipe-step.act .k{color:var(--cyan);}
@keyframes glow{0%,100%{box-shadow:0 0 0 3px rgba(46,230,198,.1);} 50%{box-shadow:0 0 0 6px rgba(46,230,198,.2);}}

/* TABS */
.stTabs [data-baseweb="tab-list"]{gap:6px; background:rgba(16,27,48,.55); padding:6px;
  border-radius:14px; border:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{height:50px; border-radius:11px; color:var(--muted);
  font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:15px; padding:0 22px;
  background:transparent; transition:.2s;}
.stTabs [data-baseweb="tab"]:hover{color:var(--ink); background:rgba(53,224,210,.06);}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg, rgba(46,230,198,.26), rgba(124,108,255,.24))!important;
  color:#fff!important; border:1px solid rgba(46,230,198,.45);}

/* SIDEBAR */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a1322,#080f1c);
  border-right:1px solid var(--line);}
section[data-testid="stSidebar"] .stMarkdown h3{color:var(--cyan);}
.role-badge{display:flex; align-items:center; gap:10px; border:1px solid var(--line-2);
  border-radius:12px; padding:10px 13px; margin:2px 0 4px;
  background:linear-gradient(135deg, rgba(20,33,57,.7), rgba(12,20,36,.6));}
.role-badge .ic{width:30px; height:30px; border-radius:8px; display:flex; align-items:center;
  justify-content:center; font-size:15px;}
.role-badge .nm{font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:13.5px;}
.role-badge .pr{font-family:'JetBrains Mono',monospace; font-size:9.5px; letter-spacing:.08em; color:var(--muted);}

/* INPUTS */
.stTextInput input, .stSelectbox div[data-baseweb="select"]>div, .stChatInput textarea{
  background:rgba(8,15,28,.7)!important; color:var(--ink)!important;
  border:1px solid var(--line)!important; border-radius:10px!important;}
.stTextInput input:focus, .stChatInput textarea:focus{
  border-color:var(--teal)!important; box-shadow:0 0 0 3px rgba(46,230,198,.18)!important;}

/* BUTTONS */
.stButton>button{background:linear-gradient(135deg, rgba(46,230,198,.16), rgba(124,108,255,.14));
  color:var(--ink); border:1px solid var(--line-2); border-radius:12px;
  font-family:'Inter',sans-serif; font-weight:500; font-size:13px; text-align:left;
  transition:.22s; box-shadow:0 8px 22px -14px rgba(124,108,255,.7); padding:11px 15px;}
.stButton>button:hover{transform:translateY(-2px); border-color:var(--teal);
  background:linear-gradient(135deg, rgba(46,230,198,.3), rgba(124,108,255,.26)); color:#fff;}

/* CHAT */
[data-testid="stChatMessage"]{background:rgba(16,27,48,.5); border:1px solid var(--line);
  border-radius:14px; padding:6px 14px; backdrop-filter:blur(6px); animation:rise .4s ease both;}

/* EXPANDERS / DATAFRAME */
.streamlit-expanderHeader, details summary{background:rgba(16,27,48,.6)!important;
  border-radius:10px!important; color:var(--ink)!important; border:1px solid var(--line)!important;}
[data-testid="stExpander"]{border:none;}
[data-testid="stDataFrame"]{border:1px solid var(--line); border-radius:12px; overflow:hidden;}

/* CARDS */
.card{border:1px solid var(--line); border-radius:16px; padding:18px 20px;
  background:linear-gradient(150deg, rgba(20,33,57,.7), rgba(12,20,36,.65));
  box-shadow:0 18px 44px -32px rgba(0,0,0,.8);}
.sec-eyebrow{font-family:'JetBrains Mono',monospace; font-size:10.5px; letter-spacing:.22em;
  text-transform:uppercase; color:var(--cyan); margin-bottom:2px; display:block;}

/* FEATURE GRID */
.fgrid{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:6px 0;}
.fcard{border:1px solid var(--line); border-radius:14px; padding:14px 15px;
  background:linear-gradient(150deg, rgba(20,33,57,.7), rgba(12,20,36,.6)); transition:.25s;
  animation:rise .5s ease both;}
.fcard:hover{transform:translateY(-3px); border-color:var(--line-2);}
.fcard .fi{font-size:18px; margin-bottom:7px;}
.fcard .ft{font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:13.5px; color:var(--ink);}
.fcard .fd{font-size:11.5px; color:var(--muted); margin-top:3px; line-height:1.5;}

/* ACCESS MATRIX */
.acc-row{display:flex; align-items:center; gap:8px; padding:7px 0; border-bottom:1px solid var(--line);}
.acc-row:last-child{border-bottom:none;}
.acc-chip{font-family:'JetBrains Mono',monospace; font-size:10px; padding:3px 9px; border-radius:999px; border:1px solid var(--line);}
.acc-on{color:var(--green); background:rgba(70,224,138,.08); border-color:rgba(70,224,138,.35);}
.acc-off{color:var(--rose); background:rgba(248,122,138,.07); border-color:rgba(248,122,138,.3);}

/* FOOTER */
.foot{color:var(--muted); font-size:12px; text-align:center; margin-top:24px;
  font-family:'JetBrains Mono',monospace; letter-spacing:.04em;}
[data-testid="stHeader"]{background:transparent;}
#MainMenu, footer{visibility:hidden;}
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(live=True):
    badge = (
        '<div class="live-badge"><span class="dot"></span>LIVE</div>'
        if live else
        '<div class="live-badge" style="color:var(--amber);border-color:rgba(246,183,60,.4);'
        'background:rgba(246,183,60,.08)"><span class="dot" style="background:var(--amber)"></span>DEMO</div>'
    )
    st.markdown(
        f"""
        <div class="hero">
          {badge}
          <span class="eyebrow">Your AI helpdesk for courses, careers &amp; support</span>
          <h1>Welcome to <span class="grad">Student Support</span></h1>
          <p class="sub">Ask anything about your courses, fees, placements, technical issues, or
          career path &mdash; and get a clear, instant answer. Pick your role, type a question
          (or tap a suggestion), and you're set.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_grid(items):
    cells = "".join(
        f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>'
        for n, l in items
    )
    st.markdown(f'<div class="statgrid">{cells}</div>', unsafe_allow_html=True)


_PIPE = [
    ("01", "Input Guardrail", "guardrail"),
    ("02", "Supervisor Route", "route"),
    ("03", "RAG Retrieve", "rag"),
    ("04", "Generate", "gen"),
    ("05", "Output Redact", "redact"),
]


def pipeline(active=None, done_through=None):
    keys = [k for _, _, k in _PIPE]
    done_idx = keys.index(done_through) if done_through in keys else -1
    html = '<div class="pipe">'
    for i, (num, label, key) in enumerate(_PIPE):
        cls = "pipe-step"
        if key == active:
            cls += " act"
        elif i <= done_idx:
            cls += " done"
        html += f'<div class="{cls}"><div class="k">STEP {num}</div><div class="t">{label}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


_ROLE_META = {
    "Student": ("\U0001F393", "rgba(53,224,210,.16)", "STUDENT \u00b7 least privilege"),
    "Staff":   ("\U0001F9D1\u200D\U0001F3EB", "rgba(58,166,246,.16)", "STAFF \u00b7 departmental"),
    "Admin":   ("\U0001F6E1\uFE0F", "rgba(157,140,245,.16)", "ADMIN \u00b7 elevated visibility"),
}


def role_badge(role):
    ic, bg, pr = _ROLE_META.get(role, ("\U0001F464", "rgba(120,160,210,.12)", role))
    st.markdown(
        f'<div class="role-badge"><div class="ic" style="background:{bg}">{ic}</div>'
        f'<div><div class="nm">{role}</div><div class="pr">{pr}</div></div></div>',
        unsafe_allow_html=True,
    )


def feature_grid(items):
    cells = "".join(
        f'<div class="fcard"><div class="fi">{e}</div><div class="ft">{t}</div>'
        f'<div class="fd">{d}</div></div>'
        for e, t, d in items
    )
    st.markdown(f'<div class="fgrid">{cells}</div>', unsafe_allow_html=True)


def access_matrix(role):
    rows = [
        ("Use the assistant", {"Student": True, "Staff": True, "Admin": True}),
        ("View own profile & courses", {"Student": True, "Staff": True, "Admin": True}),
        ("Manage students / placements", {"Student": False, "Staff": True, "Admin": True}),
        ("View audit logs", {"Student": False, "Staff": False, "Admin": True}),
        ("Change system config", {"Student": False, "Staff": False, "Admin": True}),
        ("Access other students' data", {"Student": False, "Staff": False, "Admin": False}),
    ]
    html = '<div class="card" style="padding:14px 18px;">'
    html += (f'<div style="font-family:Space Grotesk;font-weight:600;font-size:13px;'
             f'margin-bottom:8px;color:var(--ink)">Effective permissions for '
             f'<span style="color:var(--cyan)">{role}</span></div>')
    for label, perms in rows:
        allowed = perms[role]
        chip = ('<span class="acc-chip acc-on">ALLOW</span>' if allowed
                else '<span class="acc-chip acc-off">DENY</span>')
        html += (f'<div class="acc-row"><span style="flex:1;font-size:12.5px;'
                 f'color:var(--ink)">{label}</span>{chip}</div>')
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ---------- onboarding + helpers added for usability pass ----------

_WELCOME_CSS = """
<style>
.welcome{display:flex; gap:14px; align-items:stretch; margin:14px 0 4px; flex-wrap:wrap;}
.wstep{flex:1; min-width:200px; border:1px solid var(--line); border-radius:14px; padding:14px 16px;
  background:linear-gradient(150deg, rgba(23,35,57,.8), rgba(16,26,46,.7)); position:relative;
  animation:rise .5s ease both;}
.wstep:nth-child(2){animation-delay:.08s} .wstep:nth-child(3){animation-delay:.16s}
.wstep .n{font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--cyan);
  border:1px solid var(--line-2); border-radius:8px; width:26px; height:26px; display:flex;
  align-items:center; justify-content:center; margin-bottom:9px;}
.wstep .wt{font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:14px; color:var(--ink);}
.wstep .wd{font-size:12px; color:var(--muted); margin-top:3px; line-height:1.5;}
.hint{border:1px solid var(--line-2); border-left:4px solid var(--cyan); border-radius:0 12px 12px 0;
  padding:11px 14px; margin:6px 0 2px; background:rgba(67,232,218,.07);}
.hint .ht{font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:12.5px; color:var(--ink);}
.hint .hd{font-size:12px; color:var(--muted); margin-top:2px; line-height:1.5;}
</style>
"""


def welcome_strip():
    """Three-step 'how to use this' guide for first-time users."""
    st.markdown(_WELCOME_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="welcome">
          <div class="wstep"><div class="n">1</div>
            <div class="wt">Pick who you are</div>
            <div class="wd">Choose a role in the sidebar — Student, Staff, or Admin. The assistant tailors answers and access to that role.</div></div>
          <div class="wstep"><div class="n">2</div>
            <div class="wt">Ask or tap a suggestion</div>
            <div class="wd">Type a question below, or just click one of the ready-made suggestions to see it in action instantly.</div></div>
          <div class="wstep"><div class="n">3</div>
            <div class="wt">Watch it work</div>
            <div class="wd">The pipeline lights up each step — guardrail, routing, retrieval, generation — so you can see how the answer is built.</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hint(title, desc):
    """Small contextual hint card (e.g. how a background maps to a data career)."""
    st.markdown(
        f'<div class="hint"><div class="ht">{title}</div><div class="hd">{desc}</div></div>',
        unsafe_allow_html=True,
    )
