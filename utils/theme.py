CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');
/* Force light mode */
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    color-scheme: light !important;
}

/* ─── ROOT ─────────────────────────────────────── */
:root {
    --navy:    #0B1F3A;
    --teal:    #0E7B6C;
    --teal-lt: #15A898;
    --sky:     #4CB8C4;
    --cream:   #F5F4F0;
    --white:   #FFFFFF;
    --muted:   #6B7A8D;
    --border:  #DDE3EA;
    --danger:  #C0392B;
    --warn:    #D4850A;
    --good:    #1A7F4B;
    --shadow:  0 2px 16px rgba(11,31,58,0.10);
    --shadow-md: 0 4px 24px rgba(11,31,58,0.14);
}

/* ─── BASE ─────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--navy);
    background: var(--cream);
}

/* ─── SIDEBAR ──────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label {
    padding: 8px 12px;
    border-radius: 8px;
    transition: background 0.2s;
    cursor: pointer;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* ─── MAIN CONTENT ─────────────────────────────── */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ─── HERO SECTION ─────────────────────────────── */
.hero-section {
    background: linear-gradient(135deg, #0B1F3A 0%, #0E3D5A 50%, #0E7B6C 100%);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(76,184,196,0.12);
}
.hero-section::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(21,168,152,0.10);
}
.hero-badge {
    display: inline-block;
    background: rgba(76,184,196,0.20);
    border: 1px solid rgba(76,184,196,0.40);
    color: #4CB8C4 !important;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    color: #FFFFFF !important;
    line-height: 1.15;
    margin: 0 0 0.5rem 0;
}
.hero-title span { color: #4CB8C4 !important; }
.hero-subtitle {
    font-size: 1.05rem;
    color: #94A3B8 !important;
    max-width: 680px;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}
.hero-quote {
    background: rgba(255,255,255,0.06);
    border-left: 3px solid #4CB8C4;
    padding: 1rem 1.4rem;
    border-radius: 0 10px 10px 0;
    color: #CBD5E1 !important;
    font-style: italic;
    font-size: 0.95rem;
    max-width: 720px;
}

/* ─── METRIC CARDS ─────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: var(--white);
    border-radius: 14px;
    padding: 1.4rem 1.2rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}
.metric-icon {
    font-size: 1.6rem;
    margin-bottom: 0.6rem;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: var(--navy);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ─── SECTION HEADERS ──────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 2rem 0 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 2px solid var(--border);
}
.section-pill {
    width: 6px; height: 32px;
    background: linear-gradient(180deg, #0E7B6C, #4CB8C4);
    border-radius: 3px;
    flex-shrink: 0;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--navy);
    margin: 0;
}
.section-sub {
    font-size: 0.88rem;
    color: var(--muted);
    margin: 0.2rem 0 0;
}

/* ─── INFO CARDS ───────────────────────────────── */
.info-card {
    background: var(--white);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
    height: 100%;
}
.info-card-accent {
    border-top: 4px solid var(--teal);
}
.info-card h4 {
    font-size: 1rem;
    font-weight: 700;
    color: var(--navy);
    margin: 0 0 0.5rem;
}
.info-card p {
    font-size: 0.88rem;
    color: var(--muted);
    line-height: 1.65;
    margin: 0;
}

/* ─── CLUSTER BADGES ───────────────────────────── */
.badge-resilient {
    display: inline-block;
    background: #D1FAE5; color: #065F46;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-transitional {
    display: inline-block;
    background: #FEF3C7; color: #92400E;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-vulnerable {
    display: inline-block;
    background: #FEE2E2; color: #991B1B;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.04em;
}

/* ─── FORMULA BOX ──────────────────────────────── */
.formula-box {
    background: var(--navy);
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin: 1rem 0;
    color: #E2E8F0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.92rem;
    border-left: 4px solid var(--teal-lt);
}

/* ─── PLACEHOLDER BOX ──────────────────────────── */
.placeholder-box {
    border: 2px dashed #94A3B8;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    background: rgba(11,31,58,0.03);
    margin: 1rem 0;
}
.placeholder-box code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    color: var(--teal);
    background: rgba(14,123,108,0.08);
    padding: 2px 8px;
    border-radius: 6px;
}

/* ─── RECOMMENDATION CARDS ─────────────────────── */
.rec-card {
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-width: 1px;
    border-style: solid;
}
.rec-resilient { background: #F0FDF4; border-color: #86EFAC; }
.rec-transitional { background: #FFFBEB; border-color: #FCD34D; }
.rec-vulnerable { background: #FFF1F2; border-color: #FCA5A5; }

/* ─── INSIGHT BOX ──────────────────────────────── */
.insight-box {
    background: linear-gradient(135deg, #EFF8FF, #F0FDF4);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border-left: 4px solid var(--teal);
    margin: 1rem 0;
}
.insight-box p { margin: 0; font-size: 0.92rem; color: #1E3A5F; line-height: 1.65; }

/* ─── TABLE STYLING ────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
}

/* ─── TABS ─────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--white);
    border-radius: 10px;
    padding: 4px;
    border: 1px solid var(--border);
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--muted);
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: var(--navy) !important;
    color: white !important;
}

/* ─── BUTTONS ──────────────────────────────────── */
.stButton > button {
    background: var(--teal) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.03em !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: var(--navy) !important;
}

/* ─── HIDE DEFAULT STREAMLIT ELEMENTS ──────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
</style>
"""

def hero_html(badge, title, title_accent, subtitle, quote):
    return f"""
    <div class="hero-section">
        <div class="hero-badge">{badge}</div>
        <h1 class="hero-title">{title} <span>{title_accent}</span></h1>
        <p class="hero-subtitle">{subtitle}</p>
        <div class="hero-quote">{quote}</div>
    </div>
    """

def section_header(title, subtitle=""):
    sub = f'<p class="section-sub">{subtitle}</p>' if subtitle else ""
    return f"""
    <div class="section-header">
        <div class="section-pill"></div>
        <div>
            <h2 class="section-title">{title}</h2>
            {sub}
        </div>
    </div>
    """

def metric_card(icon, value, label):
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def cluster_badge(label):
    mapping = {
        "Resilient": "badge-resilient",
        "Transitional": "badge-transitional",
        "Vulnerable": "badge-vulnerable",
    }
    cls = mapping.get(label, "badge-transitional")
    return f'<span class="{cls}">{label}</span>'

def placeholder_box(label):
    return f"""
    <div class="placeholder-box">
        <p style="font-size:1.4rem;margin:0 0 0.4rem">📎</p>
        <p style="font-weight:700;color:#334155;margin:0 0 0.3rem">{label}</p>
        <p style="color:#94A3B8;font-size:0.85rem;margin:0">
            Tempelkan kode analisis Anda di sini — ganti blok ini dengan
            <code>st.code()</code> atau Python snippet Anda.
        </p>
    </div>
    """

def insight_box(text):
    return f'<div class="insight-box"><p>💡 <strong>Insight:</strong> {text}</p></div>'
