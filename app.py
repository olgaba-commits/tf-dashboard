import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# ══════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="Traffic & Finance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
# THEME TOGGLE (Light / Dark)  ✅
# ══════════════════════════════════════════════
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"  # default

# We'll render sidebar first toggle, then apply CSS based on it.
# NOTE: We'll re-render CSS after sidebar toggle is set.
# We'll place toggle in sidebar block below.

# ══════════════════════════════════════════════
# THEME STYLES (CSS)
# ══════════════════════════════════════════════
DARK_CSS = """
<style>
/* === GLOBAL === */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root { color-scheme: dark; }

.stApp {
    background: #06080F;
    font-family: 'Outfit', sans-serif;
    color: #E4E6F0;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: #0C0F1A;
    border-right: 1px solid #1E2240;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #E4E6F0;
}
section[data-testid="stSidebar"] label {
    color: #8B90AD !important;
}

/* === HEADER === */
.main-header {
    background: linear-gradient(135deg, #0C0F1A 0%, #131730 100%);
    border: 1px solid #1E2240;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.main-header h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #E4E6F0;
    letter-spacing: -0.5px;
    margin: 0;
}
.main-header .subtitle {
    font-size: 13px;
    color: #565B7A;
    margin-top: 4px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0E2D20;
    color: #3DDFA0;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
}
.live-badge::before {
    content: '';
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3DDFA0;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

/* === SCORECARD === */
.score-card {
    background: #131730;
    border: 1px solid #1E2240;
    border-radius: 14px;
    padding: 18px 20px 16px;
    position: relative;
    overflow: hidden;
    transition: all .3s;
    height: 100%;
}
.score-card:hover {
    border-color: #2A2F55;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0,0,0,.3);
}
.score-card .accent-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
}
.sc-label {
    font-size: 11px;
    color: #565B7A;
    text-transform: uppercase;
    letter-spacing: .9px;
    font-weight: 600;
    margin-bottom: 10px;
}
.sc-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 26px;
    font-weight: 600;
    color: #E4E6F0;
    letter-spacing: -0.8px;
    margin-bottom: 8px;
}
.sc-compare {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 600;
}
.sc-compare.up { color: #3DDFA0; }
.sc-compare.down { color: #F06A6A; }
.sc-sub {
    font-size: 10px;
    color: #565B7A;
    margin-top: 4px;
}

/* === CHART CARD === */
.chart-card {
    background: #131730;
    border: 1px solid #1E2240;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
}
.chart-card:hover {
    border-color: #2A2F55;
}
.chart-title {
    font-size: 15px;
    font-weight: 600;
    color: #E4E6F0;
    margin-bottom: 2px;
}
.chart-subtitle {
    font-size: 11px;
    color: #565B7A;
    margin-bottom: 14px;
}

/* === ALERT === */
.alert-banner {
    background: #2D0E0E;
    border: 1px solid #F06A6A30;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 13px;
    color: #8B90AD;
}
.alert-banner .icon { font-size: 22px; }
.alert-banner b { color: #F06A6A; }
.alert-metric {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: #F06A6A;
}

/* === SECTION LABEL === */
.sec-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #565B7A;
    font-weight: 700;
    margin: 24px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1E2240;
}

/* === KPI PILLS === */
.kpi-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
.kpi-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #131730;
    border: 1px solid #1E2240;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    color: #8B90AD;
}
.kpi-pill .dot { width: 8px; height: 8px; border-radius: 50%; }
.kpi-pill .kv {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 13px;
    color: #E4E6F0;
}

/* === GENERAL OVERRIDES === */
.stTabs [data-baseweb="tab-list"] {
    background: #111528;
    border-radius: 10px;
    padding: 3px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #565B7A;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #131730 !important;
    color: #E4E6F0 !important;
}
div[data-testid="stMetric"] {
    background: #131730;
    border: 1px solid #1E2240;
    border-radius: 12px;
    padding: 16px;
}
div[data-testid="stMetric"] label {
    color: #565B7A !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    color: #E4E6F0;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
"""

LIGHT_CSS = """
<style>
/* === GLOBAL === */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root { color-scheme: light; }

.stApp {
    background: #FFFFFF;
    font-family: 'Outfit', sans-serif;
    color: #111827;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: #F6F7FB;
    border-right: 1px solid #E5E7EB;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #111827;
}
section[data-testid="stSidebar"] label {
    color: #6B7280 !important;
}

/* === HEADER === */
.main-header {
    background: linear-gradient(135deg, #F6F7FB 0%, #FFFFFF 100%);
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.main-header h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.5px;
    margin: 0;
}
.main-header .subtitle {
    font-size: 13px;
    color: #6B7280;
    margin-top: 4px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EAF7F0;
    color: #0F7A52;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #CDEFE0;
}
.live-badge::before {
    content: '';
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #1DBF73;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

/* === SCORECARD === */
.score-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 18px 20px 16px;
    position: relative;
    overflow: hidden;
    transition: all .3s;
    height: 100%;
}
.score-card:hover {
    border-color: #D1D5DB;
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(17,24,39,.08);
}
.score-card .accent-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
}
.sc-label {
    font-size: 11px;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: .9px;
    font-weight: 700;
    margin-bottom: 10px;
}
.sc-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.8px;
    margin-bottom: 8px;
}
.sc-compare {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 700;
}
.sc-compare.up { color: #0F7A52; }
.sc-compare.down { color: #B42318; }
.sc-sub {
    font-size: 10px;
    color: #6B7280;
    margin-top: 4px;
}

/* === CHART CARD === */
.chart-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
}
.chart-card:hover {
    border-color: #D1D5DB;
}
.chart-title {
    font-size: 15px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 2px;
}
.chart-subtitle {
    font-size: 11px;
    color: #6B7280;
    margin-bottom: 14px;
}

/* === ALERT === */
.alert-banner {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 13px;
    color: #6B7280;
}
.alert-banner .icon { font-size: 22px; }
.alert-banner b { color: #B42318; }
.alert-metric {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    color: #B42318;
}

/* === SECTION LABEL === */
.sec-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6B7280;
    font-weight: 800;
    margin: 24px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #E5E7EB;
}

/* === KPI PILLS === */
.kpi-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
.kpi-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    color: #6B7280;
}
.kpi-pill .dot { width: 8px; height: 8px; border-radius: 50%; }
.kpi-pill .kv {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 13px;
    color: #111827;
}

/* === GENERAL OVERRIDES === */
.stTabs [data-baseweb="tab-list"] {
    background: #F3F4F6;
    border-radius: 10px;
    padding: 3px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #6B7280;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #E5E7EB !important;
}
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 16px;
}
div[data-testid="stMetric"] label {
    color: #6B7280 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    color: #111827;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
"""

def apply_theme_css(mode: str):
    st.markdown(DARK_CSS if mode == "dark" else LIGHT_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# PLOTLY THEME (dynamic by mode)
# ══════════════════════════════════════════════
COLORS = {
    'blue': '#5B8DEF', 'green': '#3DDFA0', 'red': '#F06A6A',
    'amber': '#F0B05A', 'purple': '#9B7AEF', 'cyan': '#4FD1D9',
    'pink': '#F06A9B', 'orange': '#FB923C',
}
COLOR_SEQ = list(COLORS.values())

def plotly_layout(mode: str):
    if mode == "dark":
        return dict(
            template='plotly_dark',
            paper_bgcolor='#131730',
            plot_bgcolor='#131730',
            font=dict(family='Outfit, sans-serif', color='#8B90AD', size=12),
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(gridcolor='#1E224040', zerolinecolor='#1E2240'),
            yaxis=dict(gridcolor='#1E224040', zerolinecolor='#1E2240'),
            legend=dict(
                bgcolor='rgba(0,0,0,0)', borderwidth=0,
                font=dict(size=11, color='#8B90AD'),
                orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0
            ),
            colorway=COLOR_SEQ,
            hoverlabel=dict(bgcolor='#1A1E3A', bordercolor='#2A2F55', font_size=12),
        )
    else:
        return dict(
            template='plotly_white',
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            font=dict(family='Outfit, sans-serif', color='#374151', size=12),
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(gridcolor='#E5E7EB', zerolinecolor='#E5E7EB'),
            yaxis=dict(gridcolor='#E5E7EB', zerolinecolor='#E5E7EB'),
            legend=dict(
                bgcolor='rgba(0,0,0,0)', borderwidth=0,
                font=dict(size=11, color='#374151'),
                orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0
            ),
            colorway=COLOR_SEQ,
            hoverlabel=dict(bgcolor='#FFFFFF', bordercolor='#E5E7EB', font_size=12),
        )

def apply_layout(fig, mode: str, **kwargs):
    base = plotly_layout(mode)
    layout = {**base, **kwargs}
    fig.update_layout(**layout)
    return fig


# ══════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_data():
    """Load all sheets from the dataset."""
    path = "TF_Dashboard_Dataset_v2.xlsx"

    traffic = pd.read_excel(path, sheet_name='FACT_Daily_Traffic')
    traffic['date'] = pd.to_datetime(traffic['date'])

    payments = pd.read_excel(path, sheet_name='FACT_Payments')
    payments['date'] = pd.to_datetime(payments['date'])

    agents = pd.read_excel(path, sheet_name='FACT_Agent_Weekly')
    agents['week_start'] = pd.to_datetime(agents['week_start'])

    geo_dim = pd.read_excel(path, sheet_name='DIM_Geo')
    targets = pd.read_excel(path, sheet_name='DIM_KPI_Targets')

    return traffic, payments, agents, geo_dim, targets


try:
    df_traffic, df_payments, df_agents, df_geo, df_targets = load_data()
except FileNotFoundError:
    st.error("⚠️ Файл `TF_Dashboard_Dataset_v2.xlsx` не знайдено. Покладіть його в ту ж папку, що й `app.py`.")
    st.stop()


# ══════════════════════════════════════════════
# SIDEBAR FILTERS + THEME TOGGLE
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 T&F Dashboard")
    st.markdown("---")

    # Theme toggle
    st.markdown("### 🎨 Theme")
    _is_dark = st.toggle("Dark mode", value=(st.session_state.theme_mode == "dark"))
    st.session_state.theme_mode = "dark" if _is_dark else "light"

    st.markdown("---")

    # Date range
    min_date = df_traffic['date'].min().date()
    max_date = df_traffic['date'].max().date()

    date_range = st.date_input(
        "📅 Період",
        value=(max_date - timedelta(days=30), max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    st.markdown("---")

    # Country filter
    all_geos = sorted(df_traffic['geo'].unique())
    selected_geos = st.multiselect("🌍 Країни", all_geos, default=all_geos)

    # Brand filter
    all_brands = sorted(df_traffic['brand'].unique())
    selected_brands = st.multiselect("🏷️ Бренди", all_brands, default=all_brands)

    # Platform filter
    all_platforms = sorted(df_traffic['platform'].unique())
    selected_platforms = st.multiselect("📱 Платформи", all_platforms, default=all_platforms)

    # Traffic source
    all_sources = sorted(df_traffic['traffic_source'].unique())
    selected_sources = st.multiselect("📡 Джерела трафіку", all_sources, default=all_sources)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px;color:#6B7280;text-align:center'>"
        "Traffic & Finance Dashboard v2.0<br>Powered by Streamlit + Plotly</div>",
        unsafe_allow_html=True
    )

# Apply theme CSS after toggle is set
apply_theme_css(st.session_state.theme_mode)
MODE = st.session_state.theme_mode


# ══════════════════════════════════════════════
# FILTER DATA
# ══════════════════════════════════════════════
def filter_traffic(df, start, end, geos, brands, platforms, sources):
    mask = (
        (df['date'].dt.date >= start) &
        (df['date'].dt.date <= end) &
        (df['geo'].isin(geos)) &
        (df['brand'].isin(brands)) &
        (df['platform'].isin(platforms)) &
        (df['traffic_source'].isin(sources))
    )
    return df[mask].copy()

df = filter_traffic(df_traffic, start_date, end_date, selected_geos, selected_brands, selected_platforms, selected_sources)

# Previous period (same length)
period_days = (end_date - start_date).days + 1
prev_start = start_date - timedelta(days=period_days)
prev_end = start_date - timedelta(days=1)
df_prev = filter_traffic(df_traffic, prev_start, prev_end, selected_geos, selected_brands, selected_platforms, selected_sources)


# ══════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════
def safe_div(a, b):
    return a / b if b != 0 else 0

def fmt_num(n):
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif abs(n) >= 1_000:
        return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"

def fmt_pct(n):
    return f"{n*100:.1f}%"

def fmt_money(n):
    if abs(n) >= 1_000_000:
        return f"${n/1_000_000:.1f}M"
    elif abs(n) >= 1_000:
        return f"${n/1_000:.1f}K"
    return f"${n:,.0f}"

def pct_change(current, previous):
    if previous == 0:
        return 0
    return (current - previous) / previous

def change_arrow(pct, invert=False):
    direction = "down" if (pct < 0) != invert else "up"
    symbol = "▲" if direction == "up" else "▼"
    color_class = "up" if direction == "up" else "down"
    return f'<span class="sc-compare {color_class}">{symbol} {abs(pct)*100:.1f}%</span>'

def scorecard_html(label, value, change_pct, sub_text="", accent_color="#5B8DEF"):
    arrow = change_arrow(change_pct)
    return f"""
    <div class="score-card">
        <div class="accent-bar" style="background:{accent_color}"></div>
        <div class="sc-label">{label}</div>
        <div class="sc-value">{value}</div>
        {arrow}
        <div class="sc-sub">{sub_text}</div>
    </div>
    """

def kpi_pill_html(label, value, color):
    return f"""
    <div class="kpi-pill">
        <div class="dot" style="background:{color}"></div>
        {label}
        <div class="kv">{value}</div>
    </div>
    """


# ══════════════════════════════════════════════
# COMPUTE KPIs
# ══════════════════════════════════════════════
def compute_kpis(d):
    regs = d['registrations'].sum()
    ftd_c = d['ftd_count'].sum()
    ftd_a = d['ftd_amount_usd'].sum()
    net_rev = d['net_revenue_usd'].sum()
    ggr = d['ggr_usd'].sum()
    bonus = d['bonus_cost_usd'].sum()
    cpa = d['cpa_cost_usd'].sum()
    p_att = d['payment_attempts'].sum()
    p_ok = d['payment_approved'].sum()
    imp = d['impressions'].sum()
    clk = d['clicks'].sum()
    active = d['active_players'].sum()
    sessions = d['sessions'].sum()
    dep_total = d['deposits_total_usd'].sum()

    return {
        'registrations': regs,
        'ftd_count': ftd_c,
        'ftd_amount': ftd_a,
        'net_revenue': net_rev,
        'ggr': ggr,
        'bonus_cost': bonus,
        'cpa_cost': cpa,
        'reg2dep': safe_div(ftd_c, regs),
        'approval_rate': safe_div(p_ok, p_att),
        'avg_ftd_check': safe_div(ftd_a, ftd_c),
        'effective_cpa': safe_div(cpa, ftd_c),
        'roi': safe_div(net_rev - cpa - bonus, cpa + bonus) if (cpa + bonus) > 0 else 0,
        'margin': net_rev - cpa - bonus,
        'ctr': safe_div(clk, imp),
        'ggr_margin': safe_div(ggr, dep_total),
        'active_players': active,
        'sessions': sessions,
        'impressions': imp,
        'clicks': clk,
        'deposits_total': dep_total,
    }

kpi = compute_kpis(df)
kpi_prev = compute_kpis(df_prev)


# ══════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════
tab_exec, tab_daily, tab_weekly, tab_payments, tab_agents = st.tabs([
    "🏠 Executive Summary",
    "📊 Daily Operations",
    "📈 Weekly Trends",
    "💳 Payment & Conversion Health",
    "👥 Traffic & Agent Efficiency",
])


# ═══════════════════════════════
# TAB 1: EXECUTIVE SUMMARY
# ═══════════════════════════════
with tab_exec:
    st.markdown(f"""
    <div class="main-header">
        <div>
            <h1>Traffic & Finance Dashboard</h1>
            <div class="subtitle">Acquisition Focus · {start_date.strftime('%b %d')} — {end_date.strftime('%b %d, %Y')} vs Previous Period</div>
        </div>
        <div class="live-badge">LIVE</div>
    </div>
    """, unsafe_allow_html=True)

    if kpi['reg2dep'] < 0.10:
        prev_r2d = kpi_prev['reg2dep']
        loss_est = (prev_r2d - kpi['reg2dep']) * kpi['registrations'] * kpi['avg_ftd_check']
        st.markdown(f"""
        <div class="alert-banner">
            <span class="icon">⚡</span>
            <div>
                <b>Conversion Crisis Alert</b> — Reg2Dep dropped from 
                <span class="alert-metric">{fmt_pct(prev_r2d)}</span> to 
                <span class="alert-metric">{fmt_pct(kpi['reg2dep'])}</span>.
                Estimated revenue loss: <span class="alert-metric">{fmt_money(loss_est)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    cols = st.columns(6)
    sc_data = [
        ("Registrations", fmt_num(kpi['registrations']), pct_change(kpi['registrations'], kpi_prev['registrations']), f"vs prev: {fmt_num(kpi_prev['registrations'])}", COLORS['blue']),
        ("FTD Count", fmt_num(kpi['ftd_count']), pct_change(kpi['ftd_count'], kpi_prev['ftd_count']), f"vs prev: {fmt_num(kpi_prev['ftd_count'])}", COLORS['green']),
        ("Reg2Dep", fmt_pct(kpi['reg2dep']), pct_change(kpi['reg2dep'], kpi_prev['reg2dep']), "Target: 18%", COLORS['purple']),
        ("FTD Amount", fmt_money(kpi['ftd_amount']), pct_change(kpi['ftd_amount'], kpi_prev['ftd_amount']), f"Avg Check: {fmt_money(kpi['avg_ftd_check'])}", COLORS['cyan']),
        ("Approval Rate", fmt_pct(kpi['approval_rate']), pct_change(kpi['approval_rate'], kpi_prev['approval_rate']), "Target: 85%", COLORS['amber']),
        ("Net Revenue", fmt_money(kpi['net_revenue']), pct_change(kpi['net_revenue'], kpi_prev['net_revenue']), f"Margin: {fmt_money(kpi['margin'])}", COLORS['red']),
    ]
    for i, (label, value, change, sub, color) in enumerate(sc_data):
        with cols[i]:
            st.markdown(scorecard_html(label, value, change, sub, color), unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Key Ratios</div>', unsafe_allow_html=True)
    pills_html = '<div class="kpi-row">'
    pills_data = [
        ("CTR", fmt_pct(kpi['ctr']), COLORS['blue']),
        ("GGR Margin", fmt_pct(kpi['ggr_margin']), COLORS['green']),
        ("eCPA", fmt_money(kpi['effective_cpa']), COLORS['amber']),
        ("ROI", fmt_pct(kpi['roi']), COLORS['purple']),
        ("Active Players", fmt_num(kpi['active_players']), COLORS['cyan']),
        ("Sessions/Player", f"{safe_div(kpi['sessions'], kpi['active_players']):.1f}", COLORS['pink']),
    ]
    for label, value, color in pills_data:
        pills_html += kpi_pill_html(label, value, color)
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Acquisition Funnel Trends</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        daily = df.groupby('date').agg(
            registrations=('registrations', 'sum'),
            ftd_count=('ftd_count', 'sum'),
        ).reset_index()

        daily_prev = df_prev.groupby('date').agg(
            registrations=('registrations', 'sum'),
        ).reset_index()
        daily_prev['date_shifted'] = daily_prev['date'] + timedelta(days=period_days)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily['date'], y=daily['registrations'],
            name='Registrations', line=dict(color=COLORS['blue'], width=2),
            fill='tozeroy', fillcolor='rgba(91,141,239,0.05)',
        ))
        fig.add_trace(go.Scatter(
            x=daily['date'], y=daily['ftd_count'],
            name='FTD', line=dict(color=COLORS['green'], width=2),
            yaxis='y2', fill='tozeroy', fillcolor='rgba(61,223,160,0.05)',
        ))
        if not daily_prev.empty:
            fig.add_trace(go.Scatter(
                x=daily_prev['date_shifted'], y=daily_prev['registrations'],
                name='Prev Regs', line=dict(color=COLORS['blue'], width=1.5, dash='dot'),
                opacity=0.4,
            ))
        apply_layout(fig, MODE, title='Registrations & FTD',
                     yaxis2=dict(overlaying='y', side='right', gridcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        daily_rev = df.groupby('date').agg(
            net_revenue=('net_revenue_usd', 'sum'),
            cpa_cost=('cpa_cost_usd', 'sum'),
            bonus_cost=('bonus_cost_usd', 'sum'),
        ).reset_index()

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=daily_rev['date'], y=daily_rev['net_revenue'], name='Net Revenue', marker_color=COLORS['green'], opacity=0.7))
        fig2.add_trace(go.Bar(x=daily_rev['date'], y=daily_rev['cpa_cost'], name='CPA Cost', marker_color=COLORS['red'], opacity=0.5))
        fig2.add_trace(go.Bar(x=daily_rev['date'], y=daily_rev['bonus_cost'], name='Bonus', marker_color=COLORS['amber'], opacity=0.4))
        apply_layout(fig2, MODE, title='Revenue vs Costs', barmode='group')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="sec-label">Split Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        plat_data = df.groupby('platform')['ftd_count'].sum().reset_index()
        fig_plat = px.pie(plat_data, values='ftd_count', names='platform', hole=0.65,
                          color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_plat, MODE, title='Platform Split (FTD)', showlegend=True)
        fig_plat.update_traces(textinfo='percent+label', textfont_size=11)
        st.plotly_chart(fig_plat, use_container_width=True, config={'displayModeBar': False})

    with c2:
        src_data = df.groupby('traffic_source')['registrations'].sum().reset_index().sort_values('registrations', ascending=False)
        fig_src = px.pie(src_data, values='registrations', names='traffic_source', hole=0.65,
                         color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_src, MODE, title='Traffic Source (Regs)', showlegend=True)
        fig_src.update_traces(textinfo='percent', textfont_size=11)
        st.plotly_chart(fig_src, use_container_width=True, config={'displayModeBar': False})

    with c3:
        geo_data = df.groupby('geo')['ftd_amount_usd'].sum().reset_index().sort_values('ftd_amount_usd', ascending=False)
        fig_geo = px.pie(geo_data, values='ftd_amount_usd', names='geo', hole=0.65,
                         color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_geo, MODE, title='GEO (FTD Amount)', showlegend=True)
        fig_geo.update_traces(textinfo='percent+label', textfont_size=11)
        st.plotly_chart(fig_geo, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="sec-label">Conversion Deep Dive — Reg2Dep by GEO</div>', unsafe_allow_html=True)

    weekly_conv = df.copy()
    weekly_conv['week'] = weekly_conv['date'].dt.isocalendar().week.astype(int)
    weekly_conv['year'] = weekly_conv['date'].dt.year
    wc = weekly_conv.groupby(['year', 'week', 'geo']).agg(
        regs=('registrations', 'sum'), ftd=('ftd_count', 'sum')
    ).reset_index()
    wc['reg2dep'] = wc['ftd'] / wc['regs'].replace(0, np.nan)
    wc['period'] = wc['year'].astype(str) + '-W' + wc['week'].astype(str).str.zfill(2)

    fig_conv = px.line(wc, x='period', y='reg2dep', color='geo',
                       color_discrete_sequence=COLOR_SEQ)
    fig_conv.update_traces(mode='lines', line_width=2)
    apply_layout(fig_conv, MODE, title='Reg2Dep by GEO — Weekly', yaxis_tickformat='.0%')
    st.plotly_chart(fig_conv, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="sec-label">Country Performance Matrix</div>', unsafe_allow_html=True)

    geo_table = df.groupby('geo').agg(
        Registrations=('registrations', 'sum'),
        FTD=('ftd_count', 'sum'),
        FTD_Amount=('ftd_amount_usd', 'sum'),
        Net_Revenue=('net_revenue_usd', 'sum'),
        Payment_Attempts=('payment_attempts', 'sum'),
        Payment_Approved=('payment_approved', 'sum'),
        CPA_Cost=('cpa_cost_usd', 'sum'),
        Bonus_Cost=('bonus_cost_usd', 'sum'),
    ).reset_index()

    geo_table['Reg2Dep'] = (geo_table['FTD'] / geo_table['Registrations'].replace(0, np.nan) * 100).round(1)
    geo_table['Avg_Check'] = (geo_table['FTD_Amount'] / geo_table['FTD'].replace(0, np.nan)).round(0)
    geo_table['Approval_%'] = (geo_table['Payment_Approved'] / geo_table['Payment_Attempts'].replace(0, np.nan) * 100).round(1)
    geo_table['eCPA'] = (geo_table['CPA_Cost'] / geo_table['FTD'].replace(0, np.nan)).round(0)
    geo_table['ROI'] = ((geo_table['Net_Revenue'] - geo_table['CPA_Cost'] - geo_table['Bonus_Cost']) / (geo_table['CPA_Cost'] + geo_table['Bonus_Cost']).replace(0, np.nan) * 100).round(1)

    display_cols = ['geo', 'Registrations', 'FTD', 'Reg2Dep', 'FTD_Amount', 'Avg_Check', 'Approval_%', 'Net_Revenue', 'eCPA', 'ROI']
    geo_display = geo_table[display_cols].sort_values('FTD_Amount', ascending=False)
    geo_display.columns = ['GEO', 'Regs', 'FTD', 'Reg2Dep %', 'FTD Amt $', 'Avg Check $', 'Approval %', 'Net Rev $', 'eCPA $', 'ROI %']

    st.dataframe(
        geo_display.style
        .format({
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}', 'Reg2Dep %': '{:.1f}%',
            'FTD Amt $': '${:,.0f}', 'Avg Check $': '${:.0f}',
            'Approval %': '{:.1f}%', 'Net Rev $': '${:,.0f}',
            'eCPA $': '${:.0f}', 'ROI %': '{:.1f}%'
        })
        .background_gradient(subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25)
        .background_gradient(subset=['Approval %'], cmap='RdYlGn', vmin=60, vmax=95)
        .background_gradient(subset=['ROI %'], cmap='RdYlGn', vmin=-50, vmax=50),
        use_container_width=True,
        hide_index=True,
    )


# ═══════════════════════════════
# TAB 2: DAILY OPERATIONS
# ═══════════════════════════════
with tab_daily:
    st.markdown('<div class="sec-label">Daily Operations — Granular View</div>', unsafe_allow_html=True)

    cols_d = st.columns(5)
    today = df[df['date'] == df['date'].max()]
    yesterday = df[df['date'] == df['date'].max() - timedelta(days=1)]

    t_kpi = compute_kpis(today)
    y_kpi = compute_kpis(yesterday)

    daily_sc = [
        ("Today Regs", fmt_num(t_kpi['registrations']), pct_change(t_kpi['registrations'], y_kpi['registrations'])),
        ("Today FTD", fmt_num(t_kpi['ftd_count']), pct_change(t_kpi['ftd_count'], y_kpi['ftd_count'])),
        ("Today Reg2Dep", fmt_pct(t_kpi['reg2dep']), pct_change(t_kpi['reg2dep'], y_kpi['reg2dep'])),
        ("Today Approval", fmt_pct(t_kpi['approval_rate']), pct_change(t_kpi['approval_rate'], y_kpi['approval_rate'])),
        ("Today Revenue", fmt_money(t_kpi['net_revenue']), pct_change(t_kpi['net_revenue'], y_kpi['net_revenue'])),
    ]
    accent_colors = [COLORS['blue'], COLORS['green'], COLORS['purple'], COLORS['amber'], COLORS['cyan']]
    for i, (lab, val, chg) in enumerate(daily_sc):
        with cols_d[i]:
            st.markdown(scorecard_html(lab, val, chg, "vs yesterday", accent_colors[i]), unsafe_allow_html=True)

    daily_tbl = df.groupby('date').agg(
        Regs=('registrations', 'sum'),
        FTD=('ftd_count', 'sum'),
        FTD_Amt=('ftd_amount_usd', 'sum'),
        Net_Rev=('net_revenue_usd', 'sum'),
        P_Attempts=('payment_attempts', 'sum'),
        P_Approved=('payment_approved', 'sum'),
    ).reset_index().sort_values('date', ascending=False)

    daily_tbl['Reg2Dep'] = (daily_tbl['FTD'] / daily_tbl['Regs'].replace(0, np.nan) * 100).round(1)
    daily_tbl['Approval'] = (daily_tbl['P_Approved'] / daily_tbl['P_Attempts'].replace(0, np.nan) * 100).round(1)
    daily_tbl['Day'] = daily_tbl['date'].dt.strftime('%a')

    display_daily = daily_tbl[['date', 'Day', 'Regs', 'FTD', 'Reg2Dep', 'FTD_Amt', 'Approval', 'Net_Rev']].head(31)
    display_daily.columns = ['Date', 'Day', 'Regs', 'FTD', 'Reg2Dep %', 'FTD Amt $', 'Approval %', 'Net Rev $']

    st.dataframe(
        display_daily.style
        .format({'Date': lambda x: x.strftime('%Y-%m-%d'), 'Regs': '{:,.0f}', 'FTD': '{:,.0f}',
                 'Reg2Dep %': '{:.1f}%', 'FTD Amt $': '${:,.0f}', 'Approval %': '{:.1f}%', 'Net Rev $': '${:,.0f}'})
        .background_gradient(subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25)
        .background_gradient(subset=['Approval %'], cmap='RdYlGn', vmin=60, vmax=95),
        use_container_width=True, hide_index=True, height=600,
    )

    st.markdown('<div class="sec-label">Registration Methods Breakdown</div>', unsafe_allow_html=True)
    reg_methods = df.groupby('reg_method').agg(
        Regs=('registrations', 'sum'), FTD=('ftd_count', 'sum')
    ).reset_index().sort_values('Regs', ascending=True)

    fig_rm = go.Figure()
    fig_rm.add_trace(go.Bar(y=reg_methods['reg_method'], x=reg_methods['Regs'], name='Registrations', orientation='h', marker_color=COLORS['blue'], opacity=0.7))
    fig_rm.add_trace(go.Bar(y=reg_methods['reg_method'], x=reg_methods['FTD'], name='FTD', orientation='h', marker_color=COLORS['green'], opacity=0.7))
    apply_layout(fig_rm, MODE, title='Registration Methods — Volume & Conversion', barmode='group')
    st.plotly_chart(fig_rm, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════
# TAB 3: WEEKLY TRENDS
# ═══════════════════════════════
with tab_weekly:
    st.markdown('<div class="sec-label">Weekly Trends — 30 Weeks</div>', unsafe_allow_html=True)

    df_full = filter_traffic(df_traffic, min_date, max_date, selected_geos, selected_brands, selected_platforms, selected_sources)

    weekly = df_full.copy()
    weekly['week'] = weekly['date'].dt.isocalendar().week.astype(int)
    weekly['year'] = weekly['date'].dt.year
    wk = weekly.groupby(['year', 'week']).agg(
        regs=('registrations', 'sum'), ftd=('ftd_count', 'sum'),
        ftd_amt=('ftd_amount_usd', 'sum'), net_rev=('net_revenue_usd', 'sum'),
        cpa=('cpa_cost_usd', 'sum'), bonus=('bonus_cost_usd', 'sum'),
    ).reset_index()
    wk['reg2dep'] = wk['ftd'] / wk['regs'].replace(0, np.nan)
    wk['ecpa'] = wk['cpa'] / wk['ftd'].replace(0, np.nan)
    wk['period'] = wk['year'].astype(str) + '-W' + wk['week'].astype(str).str.zfill(2)
    wk = wk.sort_values(['year', 'week'])

    col_w1, col_w2 = st.columns(2)

    with col_w1:
        fig_wv = make_subplots(specs=[[{"secondary_y": True}]])
        fig_wv.add_trace(go.Bar(x=wk['period'], y=wk['regs'], name='Registrations', marker_color=COLORS['blue'], opacity=0.5), secondary_y=False)
        fig_wv.add_trace(go.Scatter(x=wk['period'], y=wk['ftd'], name='FTD', line=dict(color=COLORS['green'], width=2.5), mode='lines+markers', marker_size=4), secondary_y=True)
        apply_layout(fig_wv, MODE, title='Weekly Volume: Regs & FTD')
        fig_wv.update_yaxes(title_text="Registrations", secondary_y=False)
        fig_wv.update_yaxes(title_text="FTD", secondary_y=True, gridcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_wv, use_container_width=True, config={'displayModeBar': False})

    with col_w2:
        fig_wc = make_subplots(specs=[[{"secondary_y": True}]])
        fig_wc.add_trace(go.Scatter(x=wk['period'], y=wk['reg2dep'], name='Reg2Dep %', line=dict(color=COLORS['purple'], width=2.5), fill='tozeroy', fillcolor='rgba(155,122,239,0.08)', mode='lines'), secondary_y=False)
        fig_wc.add_trace(go.Scatter(x=wk['period'], y=wk['ecpa'], name='eCPA $', line=dict(color=COLORS['red'], width=2, dash='dot'), mode='lines'), secondary_y=True)
        apply_layout(fig_wc, MODE, title='Reg2Dep vs eCPA — Weekly')
        fig_wc.update_yaxes(title_text="Conversion %", tickformat='.0%', secondary_y=False)
        fig_wc.update_yaxes(title_text="eCPA $", tickprefix='$', secondary_y=True, gridcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_wc, use_container_width=True, config={'displayModeBar': False})

    wk_display = wk[['period', 'regs', 'ftd', 'reg2dep', 'ftd_amt', 'net_rev', 'ecpa']].copy()
    wk_display.columns = ['Week', 'Regs', 'FTD', 'Reg2Dep', 'FTD Amt $', 'Net Rev $', 'eCPA $']
    wk_display = wk_display.sort_values('Week', ascending=False)

    st.dataframe(
        wk_display.style.format({
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}', 'Reg2Dep': '{:.1%}',
            'FTD Amt $': '${:,.0f}', 'Net Rev $': '${:,.0f}', 'eCPA $': '${:,.0f}'
        }).background_gradient(subset=['Reg2Dep'], cmap='RdYlGn', vmin=0, vmax=0.25),
        use_container_width=True, hide_index=True, height=500,
    )


# ═══════════════════════════════
# TAB 4: PAYMENT & CONVERSION HEALTH
# ═══════════════════════════════
with tab_payments:
    st.markdown('<div class="sec-label">Payment & Conversion Health</div>', unsafe_allow_html=True)

    try:
        _t_appr = float(df_targets.loc[df_targets['kpi_name'] == 'payment_approval_rate', 'target'].iloc[0]) / 100.0
    except Exception:
        _t_appr = 0.85

    pm = df_payments[
        (df_payments['date'].dt.date >= start_date) &
        (df_payments['date'].dt.date <= end_date) &
        (df_payments['geo'].isin(selected_geos))
    ].copy()

    pm_prev = df_payments[
        (df_payments['date'].dt.date >= prev_start) &
        (df_payments['date'].dt.date <= prev_end) &
        (df_payments['geo'].isin(selected_geos))
    ].copy()

    clicks = int(df['clicks'].sum())
    regs = int(df['registrations'].sum())
    attempts = int(df['payment_attempts'].sum())
    approved = int(df['payment_approved'].sum())
    ftd = int(df['ftd_count'].sum())

    click2reg = safe_div(regs, clicks)
    reg2attempt = safe_div(attempts, regs)
    attempt2approved = safe_div(approved, attempts)
    reg2dep = safe_div(ftd, regs)

    st.markdown('<div class="sec-label">Funnel (Clicks → Reg → Attempt → Approved → FTD)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kpi-row">'
        + kpi_pill_html("Clicks", fmt_num(clicks), COLORS['cyan'])
        + kpi_pill_html("Registrations", fmt_num(regs), COLORS['blue'])
        + kpi_pill_html("Click→Reg", fmt_pct(click2reg), COLORS['blue'])
        + kpi_pill_html("Reg→Attempt", fmt_pct(reg2attempt), COLORS['amber'])
        + kpi_pill_html("Attempt→Approved", fmt_pct(attempt2approved), COLORS['green'])
        + kpi_pill_html("Reg→FTD", fmt_pct(reg2dep), COLORS['purple'])
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sec-label">Payment Stability (Daily)</div>', unsafe_allow_html=True)
    trend = df.groupby('date', as_index=False).agg(
        attempts=('payment_attempts', 'sum'),
        approved=('payment_approved', 'sum'),
        regs=('registrations', 'sum'),
        ftd=('ftd_count', 'sum'),
        clicks=('clicks', 'sum'),
    )
    trend['approval_rate'] = trend['approved'] / trend['attempts'].replace(0, np.nan)
    trend['approval_ma7'] = trend['approval_rate'].rolling(7, min_periods=1).mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=trend['date'], y=trend['attempts'], name='Attempts',
        opacity=0.25, marker_color=COLORS['blue']
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=trend['date'], y=trend['approval_rate'], name='Approval Rate',
        line=dict(color=COLORS['green'], width=1), opacity=0.35
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=trend['date'], y=trend['approval_ma7'], name='Approval (7d MA)',
        line=dict(color=COLORS['green'], width=2.6)
    ), secondary_y=False)

    fig.add_hline(y=_t_appr, line_dash="dot", line_color=COLORS['green'],
                  annotation_text=f"Target {int(_t_appr*100)}%")

    apply_layout(fig, MODE, title="Approval Rate & Attempts", yaxis_tickformat=".0%", yaxis_title="Approval Rate", xaxis_title="")
    fig.update_yaxes(title_text="Attempts", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="sec-label">GEO Alerts (Approval % vs Previous Period)</div>', unsafe_allow_html=True)

    geo_cur = pm.groupby('geo', as_index=False).agg(txn=('txn_count','sum'), ok=('approved_count','sum'))
    geo_prev = pm_prev.groupby('geo', as_index=False).agg(txn_prev=('txn_count','sum'), ok_prev=('approved_count','sum'))

    geo = geo_cur.merge(geo_prev, on='geo', how='left').fillna(0)
    geo['approval'] = geo['ok'] / geo['txn'].replace(0, np.nan)
    geo['approval_prev'] = geo['ok_prev'] / geo['txn_prev'].replace(0, np.nan)
    geo['delta_pp'] = (geo['approval'] - geo['approval_prev']) * 100.0

    geo_disp = geo[['geo','txn','ok','approval','delta_pp']].copy()
    geo_disp.columns = ['GEO','Attempts','Approved','Approval %','Δ vs prev (pp)']
    geo_disp = geo_disp.sort_values('Attempts', ascending=False)

    def _status_color(v):
        if pd.isna(v):
            return ''
        if v >= _t_appr:
            return 'background-color: rgba(61,223,160,0.18)'
        if v >= (_t_appr - 0.05):
            return 'background-color: rgba(240,176,90,0.18)'
        return 'background-color: rgba(240,106,106,0.18)'

    st.dataframe(
        geo_disp.style
        .format({'Attempts':'{:,.0f}','Approved':'{:,.0f}','Approval %':'{:.1%}','Δ vs prev (pp)':'{:+.1f}'})
        .applymap(_status_color, subset=['Approval %']),
        use_container_width=True,
        hide_index=True
    )

    st.markdown('<div class="sec-label">Payment Method Health</div>', unsafe_allow_html=True)

    pm_method = pm.groupby('payment_method', as_index=False).agg(
        Attempts=('txn_count','sum'),
        Approved=('approved_count','sum'),
        Declined=('declined_count','sum'),
        Amount=('approved_amount_usd','sum'),
    )
    pm_method['Approval %'] = pm_method['Approved'] / pm_method['Attempts'].replace(0, np.nan)
    pm_method['Benchmark %'] = _t_appr
    pm_method['Δ vs Benchmark (pp)'] = (pm_method['Approval %'] - pm_method['Benchmark %']) * 100.0

    def _band(delta_pp):
        if pd.isna(delta_pp):
            return "No data"
        if delta_pp >= 0:
            return "OK"
        if delta_pp >= -5:
            return "Warning"
        return "Critical"

    pm_method['Status'] = pm_method['Δ vs Benchmark (pp)'].apply(_band)
    pm_method = pm_method.sort_values('Approval %', ascending=True)

    bar_colors = pm_method['Status'].map({
        'OK': COLORS['green'],
        'Warning': COLORS['amber'],
        'Critical': COLORS['red'],
        'No data': COLORS['purple'],
    }).tolist()

    fig_m = go.Figure(go.Bar(
        y=pm_method['payment_method'],
        x=pm_method['Approval %'],
        orientation='h',
        marker_color=bar_colors,
        text=pm_method['Approval %'].apply(lambda x: f"{x:.0%}" if pd.notna(x) else "—"),
        textposition='auto',
        opacity=0.9
    ))
    apply_layout(fig_m, MODE, title="Approval Rate by Payment Method", xaxis_tickformat=".0%", xaxis_range=[0.0, 1.0])
    st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})

    pm_tbl = pm_method.rename(columns={'payment_method':'Method'})
    st.dataframe(
        pm_tbl[['Method','Attempts','Approved','Declined','Approval %','Benchmark %','Δ vs Benchmark (pp)','Amount','Status']]
        .style.format({
            'Attempts':'{:,.0f}','Approved':'{:,.0f}','Declined':'{:,.0f}',
            'Approval %':'{:.1%}','Benchmark %':'{:.0%}','Δ vs Benchmark (pp)':'{:+.1f}',
            'Amount':'${:,.0f}'
        }),
        use_container_width=True, hide_index=True
    )

    st.markdown('<div class="sec-label">Chargebacks (Operational)</div>', unsafe_allow_html=True)
    cb = pm.groupby('payment_method', as_index=False).agg(
        Approved=('approved_count', 'sum'),
        Chargebacks=('chargeback_count', 'sum'),
        CB_Amount_USD=('chargeback_amount_usd', 'sum')
    )
    cb['CB Rate %'] = (cb['Chargebacks'] / cb['Approved'].replace(0, np.nan) * 100).round(2)
    cb = cb.sort_values('CB Rate %', ascending=False)

    st.dataframe(
        cb.rename(columns={'payment_method':'Method'})
        .style.format({'Approved':'{:,.0f}','Chargebacks':'{:,.0f}','CB_Amount_USD':'${:,.0f}','CB Rate %':'{:.2f}%'})
        .background_gradient(subset=['CB Rate %'], cmap='Reds', vmin=0, vmax=3),
        use_container_width=True, hide_index=True
    )


# ═══════════════════════════════
# TAB 5: TRAFFIC & AGENT EFFICIENCY
# ═══════════════════════════════
with tab_agents:
    st.markdown('<div class="sec-label">Traffic & Agent Efficiency</div>', unsafe_allow_html=True)

    a = df.copy()
    if a.empty:
        st.info("Немає даних за вибраними фільтрами.")
        st.stop()

    all_agents = sorted([x for x in a['agent'].dropna().unique().tolist() if str(x).strip() != ""])
    sel_agents = st.multiselect("👥 Agents (optional deep-dive)", all_agents, default=[])

    total_clicks = int(a['clicks'].sum())
    total_regs = int(a['registrations'].sum())
    total_ftd = int(a['ftd_count'].sum())
    total_attempts = int(a['payment_attempts'].sum())
    total_ok = int(a['payment_approved'].sum())

    k_click2reg = safe_div(total_regs, total_clicks)
    k_reg2dep = safe_div(total_ftd, total_regs)
    k_approval = safe_div(total_ok, total_attempts)

    st.markdown('<div class="sec-label">Top KPIs</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Registrations", fmt_num(total_regs))
        st.metric("Clicks", fmt_num(total_clicks))
    with c2:
        st.metric("FTD", fmt_num(total_ftd))
        st.metric("Click→Reg", fmt_pct(k_click2reg))
    with c3:
        st.metric("Reg→FTD", fmt_pct(k_reg2dep))
        st.metric("Attempts", fmt_num(total_attempts))
    with c4:
        st.metric("Approved", fmt_num(total_ok))
        st.metric("Approval Rate", fmt_pct(k_approval))

    st.markdown('<div class="sec-label">Agent Ranking</div>', unsafe_allow_html=True)

    agg = a.groupby('agent', as_index=False).agg(
        Clicks=('clicks','sum'),
        Regs=('registrations','sum'),
        FTD=('ftd_count','sum'),
        FTD_Amt=('ftd_amount_usd','sum'),
        Attempts=('payment_attempts','sum'),
        Approved=('payment_approved','sum'),
        Net_Rev=('net_revenue_usd','sum'),
        CPA=('cpa_cost_usd','sum'),
        Bonus=('bonus_cost_usd','sum'),
    )

    oneclick_regs = a[a['reg_method'] == 'One_Click'].groupby('agent')['registrations'].sum()
    organic_clicks = a[a['traffic_source'] == 'Organic'].groupby('agent')['clicks'].sum()
    affiliate_clicks = a[a['traffic_source'] == 'Affiliate'].groupby('agent')['clicks'].sum()

    agg['Reg2FTD %'] = agg['FTD'] / agg['Regs'].replace(0, np.nan)
    agg['Click2Reg %'] = agg['Regs'] / agg['Clicks'].replace(0, np.nan)
    agg['Approval %'] = agg['Approved'] / agg['Attempts'].replace(0, np.nan)
    agg['OneClick Share %'] = agg['agent'].map(oneclick_regs).fillna(0) / agg['Regs'].replace(0, np.nan)
    agg['Organic Share %'] = agg['agent'].map(organic_clicks).fillna(0) / agg['Clicks'].replace(0, np.nan)
    agg['Affiliate Share %'] = agg['agent'].map(affiliate_clicks).fillna(0) / agg['Clicks'].replace(0, np.nan)

    agg['ROI %'] = ((agg['Net_Rev'] - agg['CPA'] - agg['Bonus']) / (agg['CPA'] + agg['Bonus']).replace(0, np.nan))
    agg = agg.sort_values('FTD_Amt', ascending=False)

    show = agg[['agent','Clicks','Regs','FTD','Click2Reg %','Reg2FTD %','Approval %','OneClick Share %','Organic Share %','Affiliate Share %','FTD_Amt','ROI %']].copy()
    show.columns = ['Agent','Clicks','Regs','FTD','Click→Reg','Reg→FTD','Approval','OneClick%','Organic%','Affiliate%','FTD Amt $','ROI']

    st.dataframe(
        show.style.format({
            'Clicks':'{:,.0f}','Regs':'{:,.0f}','FTD':'{:,.0f}',
            'Click→Reg':'{:.1%}','Reg→FTD':'{:.1%}','Approval':'{:.1%}',
            'OneClick%':'{:.1%}','Organic%':'{:.1%}','Affiliate%':'{:.1%}',
            'FTD Amt $':'${:,.0f}','ROI':'{:.1%}'
        })
        .background_gradient(subset=['Reg→FTD'], cmap='RdYlGn', vmin=0, vmax=0.20)
        .background_gradient(subset=['Approval'], cmap='RdYlGn', vmin=0.60, vmax=0.95),
        use_container_width=True, hide_index=True
    )

    st.markdown('<div class="sec-label">Drop Detection (Reg→FTD vs Previous Period)</div>', unsafe_allow_html=True)
    a_prev = df_prev.copy()

    cur_r = a.groupby('agent', as_index=False).agg(Regs=('registrations','sum'), FTD=('ftd_count','sum'))
    prev_r = a_prev.groupby('agent', as_index=False).agg(Regs_prev=('registrations','sum'), FTD_prev=('ftd_count','sum'))
    dd = cur_r.merge(prev_r, on='agent', how='left').fillna(0)
    dd['Reg→FTD'] = dd['FTD'] / dd['Regs'].replace(0, np.nan)
    dd['Prev Reg→FTD'] = dd['FTD_prev'] / dd['Regs_prev'].replace(0, np.nan)
    dd['Δ (pp)'] = (dd['Reg→FTD'] - dd['Prev Reg→FTD']) * 100.0
    dd = dd.sort_values('Δ (pp)')

    st.dataframe(
        dd[['agent','Regs','FTD','Reg→FTD','Prev Reg→FTD','Δ (pp)']]
        .rename(columns={'agent':'Agent'})
        .style.format({'Regs':'{:,.0f}','FTD':'{:,.0f}','Reg→FTD':'{:.1%}','Prev Reg→FTD':'{:.1%}','Δ (pp)':'{:+.1f}'})
        .background_gradient(subset=['Δ (pp)'], cmap='RdYlGn', vmin=-10, vmax=10),
        use_container_width=True, hide_index=True
    )

    if sel_agents:
        st.markdown('<div class="sec-label">Deep Dive (Selected Agents)</div>', unsafe_allow_html=True)

        ad = a[a['agent'].isin(sel_agents)].groupby(['date','agent'], as_index=False).agg(
            Clicks=('clicks','sum'),
            Regs=('registrations','sum'),
            FTD=('ftd_count','sum'),
            Attempts=('payment_attempts','sum'),
            Approved=('payment_approved','sum'),
        )
        ad['Reg→FTD'] = ad['FTD'] / ad['Regs'].replace(0, np.nan)
        ad['Click→Reg'] = ad['Regs'] / ad['Clicks'].replace(0, np.nan)
        ad['Approval'] = ad['Approved'] / ad['Attempts'].replace(0, np.nan)

        fig1 = px.line(ad, x='date', y='Reg→FTD', color='agent', markers=True)
        apply_layout(fig1, MODE, title='Reg→FTD Trend (Selected Agents)', yaxis_tickformat='.0%')
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

        fig2 = px.line(ad, x='date', y='Approval', color='agent', markers=True)
        fig2.add_hline(y=_t_appr, line_dash="dot", line_color=COLORS['green'], annotation_text=f"Target {int(_t_appr*100)}%")
        apply_layout(fig2, MODE, title='Approval Rate Trend (Selected Agents)', yaxis_tickformat='.0%')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        fig3 = px.line(ad, x='date', y='Click→Reg', color='agent', markers=True)
        apply_layout(fig3, MODE, title='Click→Reg Trend (Selected Agents)', yaxis_tickformat='.0%')
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
