import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import importlib.util

HAS_MPL = importlib.util.find_spec("matplotlib") is not None

def bg(styler, *args, **kwargs):
    """Safe wrapper for pandas Styler.background_gradient.
    If matplotlib isn't installed (typical on Streamlit Cloud unless added), just return the Styler without gradient.
    """
    if not HAS_MPL:
        return styler
    try:
        return styler.pipe(bg, *args, **kwargs)
    except Exception:
        return styler


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
# DARK THEME CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
/* === GLOBAL === */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp {
    background: #06080F;
    font-family: 'Outfit', sans-serif;
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
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# PLOTLY THEME
# ══════════════════════════════════════════════
COLORS = {
    'blue': '#5B8DEF', 'green': '#3DDFA0', 'red': '#F06A6A',
    'amber': '#F0B05A', 'purple': '#9B7AEF', 'cyan': '#4FD1D9',
    'pink': '#F06A9B', 'orange': '#FB923C',
}
COLOR_SEQ = list(COLORS.values())
PLOTLY_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='#131730',
    plot_bgcolor='#131730',
    font=dict(family='Outfit, sans-serif', color='#8B90AD', size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor='rgba(30,34,64,0.25)', zerolinecolor='#1E2240'),
    yaxis=dict(gridcolor='rgba(30,34,64,0.25)', zerolinecolor='#1E2240'),
    legend=dict(
        bgcolor='rgba(0,0,0,0)', borderwidth=0,
        font=dict(size=11, color='#8B90AD'),
        orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0
    ),
    colorway=COLOR_SEQ,
    hoverlabel=dict(bgcolor='#1A1E3A', bordercolor='#2A2F55', font_size=12),
)

def apply_layout(fig, **kwargs):
    layout = {**PLOTLY_LAYOUT, **kwargs}
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
    
    return traffic, payments, agents, geo_dim


try:
    df_traffic, df_payments, df_agents, df_geo = load_data()
except FileNotFoundError:
    st.error("⚠️ Файл `TF_Dashboard_Dataset_v2.xlsx` не знайдено. Покладіть його в ту ж папку, що й `app.py`.")
    st.stop()


# ══════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 T&F Dashboard")
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
        "<div style='font-size:11px;color:#565B7A;text-align:center'>"
        "Traffic & Finance Dashboard v2.0<br>Powered by Streamlit + Plotly</div>",
        unsafe_allow_html=True
    )


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
    "💳 Payment Analytics",
    "👥 Agent Performance",
])


# ═══════════════════════════════
# TAB 1: EXECUTIVE SUMMARY
# ═══════════════════════════════
with tab_exec:
    # Header
    st.markdown(f"""
    <div class="main-header">
        <div>
            <h1>Traffic & Finance Dashboard</h1>
            <div class="subtitle">Acquisition Focus · {start_date.strftime('%b %d')} — {end_date.strftime('%b %d, %Y')} vs Previous Period</div>
        </div>
        <div class="live-badge">LIVE</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Alert banner (if conversion dropped)
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
    
    # Scorecards
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
    
    # KPI pills
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
    
    # Trend charts
    st.markdown('<div class="sec-label">Acquisition Funnel Trends</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        daily = df.groupby('date').agg(
            registrations=('registrations', 'sum'),
            ftd_count=('ftd_count', 'sum'),
        ).reset_index()
        
        # Previous period overlay
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
        apply_layout(fig, title='Registrations & FTD', yaxis2=dict(overlaying='y', side='right', gridcolor='rgba(30,34,64,0.0)'))
        st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})
    
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
        apply_layout(fig2, title='Revenue vs Costs', barmode='group')
        st.plotly_chart(fig2, width="stretch", config={'displayModeBar': False})
    
    # Breakdown: 3 donuts
    st.markdown('<div class="sec-label">Split Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        plat_data = df.groupby('platform')['ftd_count'].sum().reset_index()
        fig_plat = px.pie(plat_data, values='ftd_count', names='platform', hole=0.65,
                          color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_plat, title='Platform Split (FTD)', showlegend=True)
        fig_plat.update_traces(textinfo='percent+label', textfont_size=11)
        st.plotly_chart(fig_plat, width="stretch", config={'displayModeBar': False})
    
    with c2:
        src_data = df.groupby('traffic_source')['registrations'].sum().reset_index().sort_values('registrations', ascending=False)
        fig_src = px.pie(src_data, values='registrations', names='traffic_source', hole=0.65,
                         color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_src, title='Traffic Source (Regs)', showlegend=True)
        fig_src.update_traces(textinfo='percent', textfont_size=11)
        st.plotly_chart(fig_src, width="stretch", config={'displayModeBar': False})
    
    with c3:
        geo_data = df.groupby('geo')['ftd_amount_usd'].sum().reset_index().sort_values('ftd_amount_usd', ascending=False)
        fig_geo = px.pie(geo_data, values='ftd_amount_usd', names='geo', hole=0.65,
                         color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_geo, title='GEO (FTD Amount)', showlegend=True)
        fig_geo.update_traces(textinfo='percent+label', textfont_size=11)
        st.plotly_chart(fig_geo, width="stretch", config={'displayModeBar': False})
    
    # Conversion by GEO
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
    apply_layout(fig_conv, title='Reg2Dep by GEO — Weekly', yaxis_tickformat='.0%')
    st.plotly_chart(fig_conv, width="stretch", config={'displayModeBar': False})
    
    # Country table
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
        .pipe(bg, subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25)
        .pipe(bg, subset=['Approval %'], cmap='RdYlGn', vmin=60, vmax=95)
        .pipe(bg, subset=['ROI %'], cmap='RdYlGn', vmin=-50, vmax=50),
        width="stretch",
        hide_index=True,
    )


# ═══════════════════════════════
# TAB 2: DAILY OPERATIONS
# ═══════════════════════════════
with tab_daily:
    st.markdown('<div class="sec-label">Daily Operations — Granular View</div>', unsafe_allow_html=True)
    
    # Daily scorecards
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
    
    # Daily table
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
        .pipe(bg, subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25)
        .pipe(bg, subset=['Approval %'], cmap='RdYlGn', vmin=60, vmax=95),
        width="stretch", hide_index=True, height=600,
    )
    
    # Registration methods breakdown
    st.markdown('<div class="sec-label">Registration Methods Breakdown</div>', unsafe_allow_html=True)
    reg_methods = df.groupby('reg_method').agg(
        Regs=('registrations', 'sum'), FTD=('ftd_count', 'sum')
    ).reset_index().sort_values('Regs', ascending=True)
    
    fig_rm = go.Figure()
    fig_rm.add_trace(go.Bar(y=reg_methods['reg_method'], x=reg_methods['Regs'], name='Registrations', orientation='h', marker_color=COLORS['blue'], opacity=0.7))
    fig_rm.add_trace(go.Bar(y=reg_methods['reg_method'], x=reg_methods['FTD'], name='FTD', orientation='h', marker_color=COLORS['green'], opacity=0.7))
    apply_layout(fig_rm, title='Registration Methods — Volume & Conversion', barmode='group')
    st.plotly_chart(fig_rm, width="stretch", config={'displayModeBar': False})


# ═══════════════════════════════
# TAB 3: WEEKLY TRENDS
# ═══════════════════════════════
with tab_weekly:
    st.markdown('<div class="sec-label">Weekly Trends — 30 Weeks</div>', unsafe_allow_html=True)
    
    # Use full data for weekly view
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
        apply_layout(fig_wv, title='Weekly Volume: Regs & FTD')
        fig_wv.update_yaxes(title_text="Registrations", secondary_y=False)
        fig_wv.update_yaxes(title_text="FTD", secondary_y=True, gridcolor='rgba(30,34,64,0.0)')
        st.plotly_chart(fig_wv, width="stretch", config={'displayModeBar': False})
    
    with col_w2:
        fig_wc = make_subplots(specs=[[{"secondary_y": True}]])
        fig_wc.add_trace(go.Scatter(x=wk['period'], y=wk['reg2dep'], name='Reg2Dep %', line=dict(color=COLORS['purple'], width=2.5), fill='tozeroy', fillcolor='rgba(155,122,239,0.08)', mode='lines'), secondary_y=False)
        fig_wc.add_trace(go.Scatter(x=wk['period'], y=wk['ecpa'], name='eCPA $', line=dict(color=COLORS['red'], width=2, dash='dot'), mode='lines'), secondary_y=True)
        apply_layout(fig_wc, title='Reg2Dep vs eCPA — Weekly')
        fig_wc.update_yaxes(title_text="Conversion %", tickformat='.0%', secondary_y=False)
        fig_wc.update_yaxes(title_text="eCPA $", tickprefix='$', secondary_y=True, gridcolor='rgba(30,34,64,0.0)')
        st.plotly_chart(fig_wc, width="stretch", config={'displayModeBar': False})
    
    # Weekly table
    wk_display = wk[['period', 'regs', 'ftd', 'reg2dep', 'ftd_amt', 'net_rev', 'ecpa']].copy()
    wk_display.columns = ['Week', 'Regs', 'FTD', 'Reg2Dep', 'FTD Amt $', 'Net Rev $', 'eCPA $']
    wk_display = wk_display.sort_values('Week', ascending=False)
    
    st.dataframe(
        wk_display.style.format({
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}', 'Reg2Dep': '{:.1%}',
            'FTD Amt $': '${:,.0f}', 'Net Rev $': '${:,.0f}', 'eCPA $': '${:,.0f}'
        }).pipe(bg, subset=['Reg2Dep'], cmap='RdYlGn', vmin=0, vmax=0.25),
        width="stretch", hide_index=True, height=500,
    )


# ═══════════════════════════════
# TAB 4: PAYMENT ANALYTICS
# ═══════════════════════════════
with tab_payments:
    st.markdown('<div class="sec-label">Payment Analytics</div>', unsafe_allow_html=True)
    
    # Filter payments
    pm = df_payments[
        (df_payments['date'].dt.date >= start_date) &
        (df_payments['date'].dt.date <= end_date) &
        (df_payments['geo'].isin(selected_geos))
    ].copy()
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        pm_method = pm.groupby('payment_method').agg(
            txn=('txn_count', 'sum'), approved=('approved_count', 'sum')
        ).reset_index()
        pm_method['approval_rate'] = pm_method['approved'] / pm_method['txn'].replace(0, np.nan)
        pm_method = pm_method.sort_values('approval_rate', ascending=True)
        
        colors_pm = [COLORS['green'] if r >= 0.85 else COLORS['amber'] if r >= 0.70 else COLORS['red'] for r in pm_method['approval_rate']]
        
        fig_pm = go.Figure(go.Bar(
            y=pm_method['payment_method'], x=pm_method['approval_rate'],
            orientation='h', marker_color=colors_pm, opacity=0.8,
            text=pm_method['approval_rate'].apply(lambda x: f'{x:.0%}'), textposition='auto',
        ))
        apply_layout(fig_pm, title='Approval Rate by Payment Method', xaxis_tickformat='.0%', xaxis_range=[0.5, 1.0])
        st.plotly_chart(fig_pm, width="stretch", config={'displayModeBar': False})
    
    with col_p2:
        pm_geo = pm.groupby('geo').agg(
            approved=('approved_count', 'sum'), declined=('declined_count', 'sum')
        ).reset_index()
        
        fig_pg = go.Figure()
        fig_pg.add_trace(go.Bar(x=pm_geo['geo'], y=pm_geo['approved'], name='Approved', marker_color=COLORS['green'], opacity=0.7))
        fig_pg.add_trace(go.Bar(x=pm_geo['geo'], y=pm_geo['declined'], name='Declined', marker_color=COLORS['red'], opacity=0.5))
        apply_layout(fig_pg, title='Approved vs Declined by GEO', barmode='stack')
        st.plotly_chart(fig_pg, width="stretch", config={'displayModeBar': False})
    
    # Trend
    pm_trend = pm.groupby(['date', 'geo']).agg(
        txn=('txn_count', 'sum'), approved=('approved_count', 'sum')
    ).reset_index()
    pm_trend['rate'] = pm_trend['approved'] / pm_trend['txn'].replace(0, np.nan)
    
    # 7d rolling average
    pm_trend_all = pm.groupby('date').agg(txn=('txn_count', 'sum'), approved=('approved_count', 'sum')).reset_index()
    pm_trend_all['rate'] = pm_trend_all['approved'] / pm_trend_all['txn']
    pm_trend_all['rate_7d'] = pm_trend_all['rate'].rolling(7, min_periods=1).mean()
    
    fig_pt = go.Figure()
    fig_pt.add_trace(go.Scatter(x=pm_trend_all['date'], y=pm_trend_all['rate'], name='Daily', line=dict(color=COLORS['blue'], width=1), opacity=0.3))
    fig_pt.add_trace(go.Scatter(x=pm_trend_all['date'], y=pm_trend_all['rate_7d'], name='7d MA', line=dict(color=COLORS['blue'], width=2.5)))
    fig_pt.add_hline(y=0.85, line_dash="dot", line_color=COLORS['green'], annotation_text="Target 85%")
    apply_layout(fig_pt, title='Overall Approval Rate Trend (7d MA)', yaxis_tickformat='.0%')
    st.plotly_chart(fig_pt, width="stretch", config={'displayModeBar': False})
    
    # Chargeback analysis
    st.markdown('<div class="sec-label">Chargeback Analysis</div>', unsafe_allow_html=True)
    cb = pm.groupby('payment_method').agg(
        approved=('approved_count', 'sum'), cb_count=('chargeback_count', 'sum'), cb_amt=('chargeback_amount_usd', 'sum')
    ).reset_index()
    cb['cb_rate'] = (cb['cb_count'] / cb['approved'].replace(0, np.nan) * 100).round(2)
    cb = cb.sort_values('cb_rate', ascending=False)
    
    st.dataframe(
        cb.rename(columns={'payment_method': 'Method', 'approved': 'Approved Txns', 'cb_count': 'Chargebacks', 'cb_amt': 'CB Amount $', 'cb_rate': 'CB Rate %'})
        .style.format({'Approved Txns': '{:,.0f}', 'Chargebacks': '{:,.0f}', 'CB Amount $': '${:,.0f}', 'CB Rate %': '{:.2f}%'})
        .pipe(bg, subset=['CB Rate %'], cmap='Reds', vmin=0, vmax=3),
        width="stretch", hide_index=True,
    )


# ═══════════════════════════════
# TAB 5: AGENT PERFORMANCE
# ═══════════════════════════════
with tab_agents:
    st.markdown('<div class="sec-label">Agent Performance</div>', unsafe_allow_html=True)
    
    # Filter agents
    ag = df_agents[
        (df_agents['week_start'].dt.date >= start_date) &
        (df_agents['week_start'].dt.date <= end_date) &
        (df_agents['geo'].isin(selected_geos))
    ].copy()
    
    # Agent leaderboard
    ag_summary = ag.groupby('agent').agg(
        GEOs=('geo', lambda x: ', '.join(sorted(x.unique()))),
        Regs=('registrations', 'sum'),
        FTD=('ftd_count', 'sum'),
        FTD_Amt=('ftd_amount_usd', 'sum'),
        Net_Rev=('net_revenue_usd', 'sum'),
        CPA=('cpa_cost_usd', 'sum'),
        Bonus=('bonus_cost_usd', 'sum'),
        Quality=('quality_score', 'mean'),
        Fraud=('fraud_flags', 'sum'),
    ).reset_index()
    
    ag_summary['Conv_%'] = (ag_summary['FTD'] / ag_summary['Regs'].replace(0, np.nan) * 100).round(1)
    ag_summary['ROI_%'] = ((ag_summary['Net_Rev'] - ag_summary['CPA'] - ag_summary['Bonus']) / (ag_summary['CPA'] + ag_summary['Bonus']).replace(0, np.nan) * 100).round(1)
    ag_summary['Quality'] = ag_summary['Quality'].round(1)
    
    ag_display = ag_summary[['agent', 'GEOs', 'Regs', 'FTD', 'Conv_%', 'FTD_Amt', 'Quality', 'Fraud', 'ROI_%']].sort_values('FTD_Amt', ascending=False).head(15)
    ag_display.columns = ['Agent', 'GEOs', 'Regs', 'FTD', 'Conv %', 'FTD Amt $', 'Quality', 'Fraud Flags', 'ROI %']
    
    st.dataframe(
        ag_display.style
        .format({'Regs': '{:,.0f}', 'FTD': '{:,.0f}', 'Conv %': '{:.1f}%', 'FTD Amt $': '${:,.0f}', 'Quality': '{:.1f}', 'Fraud Flags': '{:,.0f}', 'ROI %': '{:.1f}%'})
        .pipe(bg, subset=['Conv %'], cmap='RdYlGn', vmin=0, vmax=15)
        .pipe(bg, subset=['Quality'], cmap='RdYlGn', vmin=2, vmax=10)
        .pipe(bg, subset=['ROI %'], cmap='RdYlGn', vmin=-50, vmax=50),
        width="stretch", hide_index=True,
    )
    
    # Charts
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        ag_scatter = ag_summary.head(20)
        fig_as = px.scatter(
            ag_scatter, x='Regs', y='Conv_%', size='FTD_Amt',
            color='Quality', color_continuous_scale='RdYlGn',
            hover_name='agent', size_max=40,
        )
        apply_layout(fig_as, title='Agent Quality vs Volume', yaxis_title='Conversion %', xaxis_title='Registrations')
        st.plotly_chart(fig_as, width="stretch", config={'displayModeBar': False})
    
    with col_a2:
        # Agent FTD by GEO — top 5
        top5_agents = ag_summary.nlargest(5, 'FTD_Amt')['agent'].tolist()
        ag_geo = ag[ag['agent'].isin(top5_agents)].groupby(['agent', 'geo'])['ftd_count'].sum().reset_index()
        
        fig_ag = px.bar(ag_geo, x='agent', y='ftd_count', color='geo',
                        color_discrete_sequence=COLOR_SEQ, barmode='stack')
        apply_layout(fig_ag, title='Top 5 Agents — FTD by GEO')
        st.plotly_chart(fig_ag, width="stretch", config={'displayModeBar': False})
    
    # Fraud alert
    fraud_agents = ag_summary[ag_summary['Fraud'] > ag_summary['Fraud'].quantile(0.9)]
    if not fraud_agents.empty:
        st.markdown('<div class="sec-label">⚠️ Fraud Risk Agents</div>', unsafe_allow_html=True)
        fraud_display = fraud_agents[['agent', 'GEOs', 'Regs', 'Fraud', 'Quality']].sort_values('Fraud', ascending=False)
        fraud_display.columns = ['Agent', 'GEOs', 'Regs', 'Fraud Flags', 'Quality']
        st.dataframe(fraud_display.style.format({'Regs': '{:,.0f}', 'Fraud Flags': '{:,.0f}', 'Quality': '{:.1f}'}), width="stretch", hide_index=True)
