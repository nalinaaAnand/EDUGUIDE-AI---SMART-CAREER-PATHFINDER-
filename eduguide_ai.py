"""
╔══════════════════════════════════════════════════════════════════╗
║   EduGuide AI  –  Asgardian Career Pathfinder  v2.0            ║
║   Thor-Themed Streamlit App  |  Register + Login  |  Career AI ║
╚══════════════════════════════════════════════════════════════════╝
Run:  streamlit run eduguide_thor_streamlit.py
"""

import streamlit as st
import json, os, hashlib, random

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚡ EduGuide AI – Asgardian Pathfinder",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
#  USER DATABASE  (JSON file)
# ══════════════════════════════════════════════════════════════════
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def _load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}

def _save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, email=""):
    db = _load_db()
    u = username.strip().lower()
    if len(u) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    if u in db:
        return False, "⚔ Warrior name already taken. Choose another."
    db[u] = {"password": _hash(password), "display": username.strip(), "email": email}
    _save_db(db)
    return True, username.strip()

def login_user(username, password):
    db = _load_db()
    u = username.strip().lower()
    if u not in db:
        return False, "⚔ Warrior not found. Register first."
    if db[u]["password"] != _hash(password):
        return False, "⚔ Wrong secret rune. Try again."
    return True, db[u]["display"]

# ══════════════════════════════════════════════════════════════════
#  CAREER DATABASE
# ══════════════════════════════════════════════════════════════════
CAREERS = {
    "Software Engineer": {
        "skills":  ["python","java","c++","javascript","git","data structures","algorithms","sql","linux"],
        "desc":    "Forge scalable software systems across the nine realms.",
        "salary":  "₹8–30 LPA", "growth": "Very High", "emoji": "⚙️",
        "courses": ["CS50 (Harvard)", "DSA – Coursera", "System Design Primer"],
    },
    "Data Scientist": {
        "skills":  ["python","machine learning","statistics","sql","pandas","numpy","data visualization","deep learning","r"],
        "desc":    "Read the runes of data to reveal hidden truths.",
        "salary":  "₹10–35 LPA", "growth": "Very High", "emoji": "🔮",
        "courses": ["Andrew Ng ML", "Fast.ai", "Kaggle Learn"],
    },
    "Web Developer": {
        "skills":  ["html","css","javascript","react","node.js","sql","git","rest api","typescript"],
        "desc":    "Weave the digital tapestry of the mortal web.",
        "salary":  "₹5–20 LPA", "growth": "High", "emoji": "🌐",
        "courses": ["The Odin Project", "freeCodeCamp", "Full Stack Open"],
    },
    "Cybersecurity Analyst": {
        "skills":  ["networking","linux","python","ethical hacking","firewalls","cryptography","sql","bash"],
        "desc":    "Guard the Bifrost of digital infrastructure.",
        "salary":  "₹7–25 LPA", "growth": "High", "emoji": "🛡️",
        "courses": ["CompTIA Security+", "TryHackMe", "CEH Certification"],
    },
    "UI/UX Designer": {
        "skills":  ["figma","wireframing","user research","prototyping","adobe xd","html","css","design thinking"],
        "desc":    "Craft realms of beauty that mortals can navigate.",
        "salary":  "₹5–18 LPA", "growth": "High", "emoji": "🎨",
        "courses": ["Google UX Cert", "IxDF Foundation", "Figma Masterclass"],
    },
    "Cloud Engineer": {
        "skills":  ["aws","azure","gcp","docker","kubernetes","linux","networking","terraform","python"],
        "desc":    "Command the clouds like Thor commands the storm.",
        "salary":  "₹10–40 LPA", "growth": "Very High", "emoji": "☁️",
        "courses": ["AWS Solutions Architect", "GCP Professional", "Docker & K8s"],
    },
    "Data Analyst": {
        "skills":  ["excel","sql","python","tableau","power bi","statistics","data visualization","pandas"],
        "desc":    "Translate the All-Speak of raw numbers into wisdom.",
        "salary":  "₹4–15 LPA", "growth": "High", "emoji": "📊",
        "courses": ["Google Data Analytics", "SQL for DA", "Tableau Training"],
    },
    "AI/ML Engineer": {
        "skills":  ["python","tensorflow","pytorch","deep learning","machine learning","mathematics","statistics","nlp"],
        "desc":    "Breathe intelligence into stone — like Odin himself.",
        "salary":  "₹12–45 LPA", "growth": "Very High", "emoji": "🤖",
        "courses": ["Deep Learning Spec.", "Hugging Face Course", "MLOps Zoomcamp"],
    },
    "DevOps Engineer": {
        "skills":  ["linux","docker","kubernetes","ci/cd","git","aws","python","bash","monitoring"],
        "desc":    "Bridge Asgard and Midgard — dev and production as one.",
        "salary":  "₹8–28 LPA", "growth": "Very High", "emoji": "🔧",
        "courses": ["DevOps Bootcamp", "GitHub Actions", "Prometheus & Grafana"],
    },
    "Business Analyst": {
        "skills":  ["excel","sql","communication","data analysis","reporting","power bi","project management","presentation"],
        "desc":    "Counsel the king with wisdom, foresight and data.",
        "salary":  "₹5–18 LPA", "growth": "Moderate", "emoji": "📋",
        "courses": ["BA Fundamentals", "CBAP Certification", "Excel for Business"],
    },
}

SKILL_POOL = sorted({s for info in CAREERS.values() for s in info["skills"]})

def match_careers(user_skills):
    user_set = {s.strip().lower() for s in user_skills}
    out = []
    for career, info in CAREERS.items():
        req     = set(info["skills"])
        matched = sorted(user_set & req)
        missing = sorted(req - user_set)
        score   = len(matched) / len(req) if req else 0
        out.append({"career": career, "score": score,
                    "matched": matched, "missing": missing, "info": info})
    return sorted(out, key=lambda x: -x["score"])[:6]

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
for k, v in {
    "page": "login",          # login | register | skills | results
    "user": "",
    "results": [],
    "chosen_skills": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
#  THOR CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,400&display=swap');

/* ── global reset ── */
html, body, [class*="css"] {
    font-family: 'Crimson Pro', Georgia, serif;
    background-color: #050f1a !important;
    color: #bdd4e4;
}
.stApp { background-color: #050f1a; }

/* ── hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.thor-topbar {
    background: linear-gradient(90deg, #050f1a 0%, #0e1f30 40%, #050f1a 100%);
    border-bottom: 3px solid #c9980f;
    padding: 14px 32px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0;
}
.thor-topbar-title {
    font-family: 'Cinzel', serif;
    font-size: 1.5rem; font-weight: 900;
    color: #edbb2a;
    text-shadow: 0 0 20px rgba(237,187,42,.35);
    letter-spacing: .08em;
}
.thor-topbar-sub {
    font-family: 'Cinzel', serif;
    font-size: .65rem; font-weight: 400;
    color: #6ea8c0; letter-spacing: .25em;
}
.thor-topbar-user {
    font-family: 'Cinzel', serif;
    font-size: .8rem; color: #c9980f;
    background: rgba(201,152,15,.1);
    border: 1px solid rgba(201,152,15,.3);
    border-radius: 6px; padding: 5px 14px;
}

/* ── HERO (login / register) ── */
.hero-wrap {
    background: linear-gradient(160deg, #0b1c2c 0%, #07131e 60%, #0e1f30 100%);
    border: 1px solid #1c3850;
    border-radius: 18px;
    padding: 3rem 3.5rem;
    text-align: center;
    position: relative; overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero-wrap::before {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(201,152,15,.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute; bottom: -60px; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(61,184,240,.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-hammer { font-size: 4rem; margin-bottom: .5rem; }
.hero-title {
    font-family: 'Cinzel', serif;
    font-size: 2.2rem; font-weight: 900;
    color: #edbb2a;
    text-shadow: 0 0 30px rgba(237,187,42,.3);
    margin-bottom: .2rem;
}
.hero-subtitle {
    font-family: 'Cinzel', serif;
    font-size: .75rem; font-weight: 400;
    color: #6ea8c0; letter-spacing: .3em;
    margin-bottom: 1.2rem;
}
.hero-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 1rem auto; max-width: 280px;
}
.hero-divider-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #c9980f, transparent); }
.hero-divider-icon { color: #c9980f; font-size: .9rem; }

/* ── FORM CARD ── */
.form-card {
    background: linear-gradient(135deg, #0b1c2c 0%, #081522 100%);
    border: 1px solid #1c3850;
    border-top: 3px solid #c9980f;
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.2rem;
}
.form-card-title {
    font-family: 'Cinzel', serif;
    font-size: 1rem; font-weight: 700;
    color: #edbb2a;
    letter-spacing: .15em; text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: .5rem;
}
.form-card-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(201,152,15,.5), transparent);
}

/* ── SECTION HEADER ── */
.section-header {
    font-family: 'Cinzel', serif;
    font-size: .85rem; font-weight: 700;
    color: #c9980f; letter-spacing: .2em; text-transform: uppercase;
    margin-bottom: .6rem;
    padding-bottom: .4rem;
    border-bottom: 1px solid rgba(201,152,15,.25);
}

/* ── CAREER CARD ── */
.career-card {
    background: linear-gradient(135deg, #0b1c2c 0%, #081828 100%);
    border: 1px solid #1c3850;
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
    transition: border-color .2s;
}
.career-card.rank1 {
    border-color: rgba(201,152,15,.6);
    border-left: 4px solid #c9980f;
    box-shadow: 0 0 24px rgba(201,152,15,.08);
}
.career-card.rank2 { border-left: 4px solid #3db8f0; }
.career-card.rank3 { border-left: 4px solid #6ea8c0; }
.career-card.rankN { border-left: 4px solid #1c3850; }
.career-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,152,15,.4), transparent);
}

.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 8px;
    font-family: 'Cinzel', serif; font-size: .85rem; font-weight: 700;
    margin-right: 10px; flex-shrink: 0;
}
.rank-badge.r1 { background: rgba(201,152,15,.2); color: #edbb2a; border: 1px solid #c9980f; }
.rank-badge.r2 { background: rgba(61,184,240,.15); color: #7dd4f8; border: 1px solid #3db8f0; }
.rank-badge.r3 { background: rgba(110,168,192,.15); color: #6ea8c0; border: 1px solid #6ea8c0; }
.rank-badge.rN { background: rgba(28,56,80,.5);    color: #6ea8c0; border: 1px solid #1c3850; }

.career-name {
    font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 700;
    color: #e8f4ff; display: inline;
}
.career-name.r1 { color: #fde98a; }
.career-desc { font-size: .95rem; font-style: italic; color: #6ea8c0; margin: .3rem 0 .8rem; }

.meta-pill {
    display: inline-block;
    padding: .22rem .75rem; border-radius: 99px;
    font-size: .78rem; font-family: 'Cinzel', serif;
    margin-right: .4rem; margin-bottom: .4rem;
}
.meta-gold { background: rgba(201,152,15,.15); border: 1px solid rgba(201,152,15,.5); color: #edbb2a; }
.meta-green { background: rgba(61,171,120,.12); border: 1px solid rgba(61,171,120,.4); color: #3dab78; }
.meta-blue  { background: rgba(61,184,240,.1);  border: 1px solid rgba(61,184,240,.35); color: #7dd4f8; }

/* ── MATCH BAR ── */
.match-wrap { margin: .6rem 0 .8rem; }
.match-label {
    font-family: 'Cinzel', serif; font-size: .8rem;
    color: #6ea8c0; margin-bottom: .35rem;
}
.match-bar-bg {
    background: rgba(28,56,80,.6); border-radius: 99px; height: 8px; overflow: hidden;
}
.match-bar-fill {
    height: 8px; border-radius: 99px;
    background: linear-gradient(90deg, #c9980f, #edbb2a);
    transition: width 1s ease;
}
.match-bar-fill.sky  { background: linear-gradient(90deg, #3db8f0, #7dd4f8); }
.match-bar-fill.rune { background: linear-gradient(90deg, #3d6070, #6ea8c0); }

/* ── SKILL TAGS ── */
.tag { display: inline-block; padding: .22rem .7rem; border-radius: 99px; font-size: .78rem; margin: .2rem; }
.tag-have    { background: rgba(61,171,120,.12); border: 1px solid rgba(61,171,120,.45); color: #3dab78; }
.tag-missing { background: rgba(217,79,79,.1);   border: 1px solid rgba(217,79,79,.4);  color: #e87070; }
.tag-course  { background: rgba(201,152,15,.1);  border: 1px solid rgba(201,152,15,.4); color: #edbb2a; }
.tag-skill   { background: rgba(61,184,240,.08); border: 1px solid rgba(61,184,240,.35); color: #7dd4f8; }

/* ── STAT CARD ── */
.stat-card {
    background: rgba(11,28,44,.8);
    border: 1px solid #1c3850;
    border-radius: 12px; padding: 1rem 1.2rem; text-align: center;
}
.stat-num {
    font-family: 'Cinzel', serif; font-size: 2rem; font-weight: 900; color: #edbb2a;
}
.stat-lbl { font-size: .78rem; color: #6ea8c0; }

/* ── GAP BAR ── */
.gap-row { display: flex; align-items: center; gap: 10px; margin-bottom: .5rem; }
.gap-label { font-size: .88rem; color: #e8981a; min-width: 160px; }
.gap-bar-bg { flex: 1; height: 7px; background: rgba(28,56,80,.6); border-radius: 99px; overflow: hidden; }
.gap-bar-fill { height: 7px; border-radius: 99px; background: linear-gradient(90deg,#e8981a,#f0c040); }
.gap-count { font-size: .78rem; color: #6ea8c0; min-width: 42px; text-align: right; }

/* ── QUOTE ── */
.asgard-quote {
    font-style: italic; color: #3d6070; font-size: .82rem; text-align: center; padding: .5rem 0;
}

/* ── PROGRESS BAR (override streamlit) ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #c9980f, #edbb2a) !important;
}

/* ── INPUT FIELDS ── */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: #0b1c2c !important;
    border: 1px solid #1c3850 !important;
    border-radius: 8px !important;
    color: #bdd4e4 !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #c9980f !important;
    box-shadow: 0 0 0 2px rgba(201,152,15,.18) !important;
}

/* ── MULTISELECT ── */
.stMultiSelect > div > div {
    background: #0b1c2c !important;
    border: 1px solid #1c3850 !important;
    border-radius: 8px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: rgba(201,152,15,.2) !important;
    border: 1px solid #c9980f !important;
    color: #edbb2a !important;
}

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    letter-spacing: .08em !important;
    border-radius: 8px !important;
    border: none !important;
    transition: opacity .18s, transform .12s !important;
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: scale(.97) !important; }

/* primary (gold) */
div[data-testid="stHorizontalBlock"] .stButton > button,
.gold-btn .stButton > button {
    background: linear-gradient(135deg, #b8880d 0%, #edbb2a 50%, #b8880d 100%) !important;
    color: #050f1a !important;
    box-shadow: 0 4px 18px rgba(201,152,15,.3) !important;
}
/* secondary */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(201,152,15,.4) !important;
    color: #edbb2a !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0b1c2c !important;
    border-radius: 10px 10px 0 0 !important;
    border-bottom: 2px solid #c9980f !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    font-size: .82rem !important; font-weight: 700 !important;
    letter-spacing: .1em !important;
    color: #6ea8c0 !important;
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    padding: .6rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(201,152,15,.15) !important;
    color: #edbb2a !important;
    border-bottom: 2px solid #edbb2a !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #081522 !important;
    border: 1px solid #1c3850 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.5rem 1.5rem 1rem !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #0b1c2c !important;
    border: 1px solid #1c3850 !important;
    border-radius: 8px !important;
    color: #edbb2a !important;
    font-family: 'Cinzel', serif !important;
    font-size: .82rem !important;
}
.streamlit-expanderContent {
    background: #081522 !important;
    border: 1px solid #1c3850 !important;
    border-top: none !important;
}

/* ── DIVIDER ── */
hr { border-color: #1c3850 !important; }

/* ── ALERTS ── */
.stSuccess { background: rgba(61,171,120,.1) !important; border-color: #3dab78 !important; color: #3dab78 !important; }
.stError   { background: rgba(217,79,79,.1)  !important; border-color: #d94f4f !important; color: #e87070 !important; }
.stWarning { background: rgba(232,152,26,.1) !important; border-color: #e8981a !important; }
.stInfo    { background: rgba(61,184,240,.08) !important; border-color: #3db8f0 !important; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050f1a; }
::-webkit-scrollbar-thumb { background: #1c3850; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c9980f; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def topbar():
    user_html = (
        f'<span class="thor-topbar-user">⚡ {st.session_state.user}</span>'
        if st.session_state.user else ""
    )
    st.markdown(f"""
    <div class="thor-topbar">
      <div>
        <div class="thor-topbar-title">🔨 EDUGUIDE AI</div>
        <div class="thor-topbar-sub">A S G A R D I A N &nbsp; C A R E E R &nbsp; P A T H F I N D E R</div>
      </div>
      {user_html}
    </div>""", unsafe_allow_html=True)

def gold_divider():
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin:1rem 0;">
      <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#c9980f,transparent);"></div>
      <span style="color:#c9980f;font-size:.8rem;">⚡</span>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#c9980f,transparent);"></div>
    </div>""", unsafe_allow_html=True)

def section_header(txt):
    st.markdown(f'<div class="section-header">{txt}</div>', unsafe_allow_html=True)

def card_open(cls=""):
    st.markdown(f'<div class="form-card {cls}">', unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

RUNE_QUOTES = [
    "Mjolnir chooses the worthy.",
    "Only the skilled may enter Valhalla.",
    "Each skill is a rune of power.",
    "The All-Father sees your potential.",
    "Even gods must train before battle.",
]

# ══════════════════════════════════════════════════════════════════
#  PAGE : LOGIN / REGISTER
# ══════════════════════════════════════════════════════════════════
def page_auth():
    topbar()
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.1, 1], gap="large")

    # ── LEFT: hero panel ──
    with col_l:
        st.markdown("""
        <div class="hero-wrap">
            <div class="hero-hammer">🔨</div>
            <div class="hero-title">EduGuide AI</div>
            <div class="hero-subtitle">A S G A R D I A N &nbsp; C A R E E R &nbsp; P A T H F I N D E R</div>
            <div class="hero-divider">
                <div class="hero-divider-line"></div>
                <div class="hero-divider-icon">⚡</div>
                <div class="hero-divider-line"></div>
            </div>
            <p style="color:#6ea8c0;font-size:.95rem;max-width:340px;margin:0 auto;">
                An AI-powered system that reveals your ideal career path by
                matching your skills against the wisdom of the nine realms.
            </p>
        </div>""", unsafe_allow_html=True)

        # stat row
        sc1, sc2, sc3 = st.columns(3)
        for col, (n, lbl) in zip([sc1, sc2, sc3], [
            ("10", "Careers"), (str(len(SKILL_POOL)), "Skills"), ("AI", "Powered")
        ]):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-num">{n}</div>
                    <div class="stat-lbl">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        for q in RUNE_QUOTES[:3]:
            st.markdown(f'<div class="asgard-quote">「{q}」</div>', unsafe_allow_html=True)

    # ── RIGHT: tabs Login / Register ──
    with col_r:
        tab_login, tab_reg = st.tabs(["⚔  LOGIN", "🛡  REGISTER"])

        # ── LOGIN TAB ──
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            uname = st.text_input("WARRIOR NAME", placeholder="Enter your username", key="li_u")
            passw = st.text_input("SECRET RUNE", placeholder="Enter your password",
                                  type="password", key="li_p")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("⚡  ENTER ASGARD", use_container_width=True, key="btn_login"):
                    if not uname.strip() or not passw.strip():
                        st.error("Fill in both fields, warrior.")
                    else:
                        ok, msg = login_user(uname, passw)
                        if ok:
                            st.session_state.user = msg
                            st.session_state.page = "skills"
                            st.rerun()
                        else:
                            st.error(msg)
            with c2:
                if st.button("Register instead →", use_container_width=True, key="btn_go_reg"):
                    st.session_state.page = "register"
                    st.rerun()

            gold_divider()
            st.markdown('<div class="asgard-quote">Your credentials are stored securely with SHA-256 hashing.</div>',
                        unsafe_allow_html=True)

        # ── REGISTER TAB ──
        with tab_reg:
            st.markdown("<br>", unsafe_allow_html=True)
            r_uname = st.text_input("WARRIOR NAME *", placeholder="At least 3 characters", key="re_u")
            r_email = st.text_input("EMAIL (optional)", placeholder="your@email.com", key="re_e")
            r_pass1 = st.text_input("SECRET RUNE *", placeholder="At least 4 characters",
                                    type="password", key="re_p1")
            r_pass2 = st.text_input("CONFIRM RUNE *", placeholder="Repeat password",
                                    type="password", key="re_p2")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🛡  FORGE ACCOUNT", use_container_width=True, key="btn_reg"):
                    if not r_uname.strip() or not r_pass1 or not r_pass2:
                        st.error("Fill all required fields.")
                    elif r_pass1 != r_pass2:
                        st.error("Secret runes do not match!")
                    else:
                        ok, msg = register_user(r_uname, r_pass1, r_email)
                        if ok:
                            st.success(f"⚡ Welcome, {msg}! Account forged. Login now.")
                        else:
                            st.error(msg)
            with c2:
                if st.button("← Back to Login", use_container_width=True, key="btn_go_login"):
                    st.session_state.page = "login"
                    st.rerun()

            gold_divider()
            st.markdown('<div class="asgard-quote">* Required fields &nbsp;|&nbsp; Data stored locally on your device.</div>',
                        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : SKILLS
# ══════════════════════════════════════════════════════════════════
def page_skills():
    topbar()
    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2.4, 1], gap="large")

    with col_main:
        st.markdown("""
        <div class="form-card">
            <div class="form-card-title">⚡ SELECT YOUR POWERS</div>
        </div>""", unsafe_allow_html=True)

        # search filter
        search = st.text_input("🔍 Search skills", placeholder="Filter skills…", key="skill_search")
        visible = [s for s in SKILL_POOL if search.lower() in s.lower()] if search else SKILL_POOL

        section_header("SKILL CODEX — Click to select")
        chosen = st.multiselect(
            "Select all skills you possess:",
            options=visible,
            default=[s for s in st.session_state.get("selected_skills", []) if s in visible],
            key="skill_multi",
            label_visibility="collapsed",
        )
        st.session_state["selected_skills"] = chosen

        gold_divider()

        # custom skill
        section_header("ADD CUSTOM SKILL")
        cc1, cc2 = st.columns([3, 1])
        with cc1:
            custom = st.text_input("Custom skill name", placeholder="e.g. Blockchain, AutoCAD…",
                                   key="custom_skill", label_visibility="collapsed")
        with cc2:
            if st.button("+ Add", use_container_width=True, key="btn_add_custom"):
                raw = custom.strip().lower()
                if raw and raw not in SKILL_POOL:
                    SKILL_POOL.append(raw); SKILL_POOL.sort()
                if raw and raw not in st.session_state.get("selected_skills", []):
                    cur = st.session_state.get("selected_skills", [])
                    cur.append(raw)
                    st.session_state["selected_skills"] = cur
                    st.rerun()

        # selected preview
        if chosen:
            gold_divider()
            section_header("YOUR ARSENAL")
            tags = "".join(f'<span class="tag tag-skill">{s}</span>' for s in chosen)
            st.markdown(tags, unsafe_allow_html=True)

    with col_side:
        # stat panel
        st.markdown(f"""
        <div class="form-card" style="text-align:center;">
            <div class="form-card-title">⚡ QUEST STATS</div>
            <div class="stat-num">{len(chosen)}</div>
            <div class="stat-lbl" style="margin-bottom:1rem;">skills selected</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:.8rem;">
                <div class="stat-card"><div class="stat-num" style="font-size:1.4rem;">{len(CAREERS)}</div><div class="stat-lbl">Careers</div></div>
                <div class="stat-card"><div class="stat-num" style="font-size:1.4rem;">{len(SKILL_POOL)}</div><div class="stat-lbl">Skills</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button("🔮  REVEAL DESTINY", use_container_width=True, key="btn_analyze"):
            if not chosen:
                st.warning("Select at least one skill, warrior!")
            else:
                st.session_state.chosen_skills = chosen
                st.session_state.results = match_careers(chosen)
                st.session_state.page = "results"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄  Clear All", use_container_width=True, key="btn_clear"):
            st.session_state["selected_skills"] = []
            st.rerun()

        if st.button("🔓  Logout", use_container_width=True, key="btn_logout_s"):
            st.session_state.user = ""
            st.session_state.page = "login"
            st.rerun()

        gold_divider()
        for q in RUNE_QUOTES:
            st.markdown(f'<div class="asgard-quote">「{q}」</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : RESULTS
# ══════════════════════════════════════════════════════════════════
def page_results():
    topbar()
    st.markdown("<br>", unsafe_allow_html=True)

    results = st.session_state.results
    chosen  = st.session_state.chosen_skills

    # toolbar
    tc1, tc2, tc3 = st.columns([1, 4, 1])
    with tc1:
        if st.button("← Refine Skills", use_container_width=True):
            st.session_state.page = "skills"; st.rerun()
    with tc3:
        if st.button("🔓 Logout", use_container_width=True):
            st.session_state.user = ""; st.session_state.page = "login"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # arsenal summary
    st.markdown(f"""
    <div class="form-card">
        <div class="form-card-title">🛡 YOUR ARSENAL — {len(chosen)} Skills</div>
        {"".join(f'<span class="tag tag-skill">{s}</span>' for s in chosen)}
    </div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Career cards ──
    section_header("⚔ TOP CAREER MATCHES")
    st.markdown("<br>", unsafe_allow_html=True)

    rank_class = {1: "rank1", 2: "rank2", 3: "rank3"}
    badge_class = {1: "r1", 2: "r2", 3: "r3"}
    bar_class   = {1: "",    2: "sky", 3: "rune"}

    for rank, r in enumerate(results, 1):
        pct    = int(r["score"] * 100)
        info   = r["info"]
        rc     = rank_class.get(rank, "rankN")
        bc     = badge_class.get(rank, "rN")
        barcls = bar_class.get(rank, "rune")

        growth_icon = "⚡" if "Very High" in info["growth"] else ("🌩" if "High" in info["growth"] else "📈")

        st.markdown(f"""
        <div class="career-card {rc}">
            <div style="display:flex;align-items:center;margin-bottom:.4rem;">
                <span class="rank-badge {bc}">#{rank}</span>
                <span class="career-name {rc if rank==1 else ''}">{info['emoji']} &nbsp;{r['career']}</span>
                <span style="margin-left:auto;">
                    <span class="meta-pill meta-gold">💰 {info['salary']}</span>
                    <span class="meta-pill meta-green">{growth_icon} {info['growth']}</span>
                </span>
            </div>
            <div class="career-desc">{info['desc']}</div>
            <div class="match-wrap">
                <div class="match-label">Match Score: <strong style="color:#edbb2a;">{pct}%</strong></div>
                <div class="match-bar-bg">
                    <div class="match-bar-fill {barcls}" style="width:{pct}%;"></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        with st.expander(f"📋 Details — {r['career']}"):
            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown("**✅ Skills You Have**")
                if r["matched"]:
                    st.markdown("".join(f'<span class="tag tag-have">{s}</span>' for s in r["matched"]),
                                unsafe_allow_html=True)
                else:
                    st.caption("None yet — begin your training!")

            with d2:
                st.markdown("**❌ Skills to Forge**")
                if r["missing"]:
                    st.markdown("".join(f'<span class="tag tag-missing">{s}</span>' for s in r["missing"]),
                                unsafe_allow_html=True)
                else:
                    st.success("All skills mastered! ⚡")

            with d3:
                st.markdown("**📜 Sacred Scrolls (Courses)**")
                for c in info["courses"]:
                    st.markdown(f'<span class="tag tag-course">⚔ {c}</span>', unsafe_allow_html=True)

    # ── Skill Gap Analysis ──
    gold_divider()
    section_header("📉 OVERALL SKILL GAP ANALYSIS")
    st.markdown("<br>", unsafe_allow_html=True)

    all_missing = {}
    for r in results:
        for s in r["missing"]:
            all_missing[s] = all_missing.get(s, 0) + 1

    if not all_missing:
        st.success("⚡ Worthy of Valhalla! Exceptional skill coverage across all paths.")
    else:
        st.markdown("""
        <div style="color:#6ea8c0;font-size:.9rem;margin-bottom:.8rem;">
        Forge these skills to unlock multiple career paths simultaneously:
        </div>""", unsafe_allow_html=True)

        sorted_gaps = sorted(all_missing.items(), key=lambda x: -x[1])[:10]
        for skill, count in sorted_gaps:
            pct = int(count / len(results) * 100)
            st.markdown(f"""
            <div class="gap-row">
                <div class="gap-label">🔩 {skill}</div>
                <div class="gap-bar-bg"><div class="gap-bar-fill" style="width:{pct}%;"></div></div>
                <div class="gap-count">×{count} paths</div>
            </div>""", unsafe_allow_html=True)

        readiness = max(0, int((1 - len(all_missing) / 30) * 100))
        gold_divider()
        st.markdown(f"""
        <div style="text-align:center;padding:1rem;">
            <div style="font-family:'Cinzel',serif;font-size:1rem;color:#6ea8c0;margin-bottom:.4rem;">
                ⚔ &nbsp; ASGARD READINESS SCORE
            </div>
            <div style="font-family:'Cinzel',serif;font-size:2.8rem;font-weight:900;color:#edbb2a;">
                {readiness}%
            </div>
        </div>""", unsafe_allow_html=True)
        st.progress(readiness / 100)

# ══════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════
page = st.session_state.page

if page in ("login", "register"):
    page_auth()
elif page == "skills":
    if not st.session_state.user:
        st.session_state.page = "login"; st.rerun()
    page_skills()
elif page == "results":
    if not st.session_state.user:
        st.session_state.page = "login"; st.rerun()
    page_results()
