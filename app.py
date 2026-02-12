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
# THEME TOGGLE (Light / Dark)
# ══════════════════════════════════════════════
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# ══════════════════════════════════════════════
# THEME STYLES (CSS)
# ══════════════════════════════════════════════
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root { color-scheme: dark; }

.stApp {
    background: #06080F;
    font-family: 'Outfit', sans-serif;
    color: #E4E6F0;
}

section[data-testid="stSidebar"] {
    background: #0C0F1A;
    border-right: 1px solid #1E2240;
}

.main-header {
    background: linear-gradient(135deg, #0C0F1A 0%, #131730 100%);
    border: 1px solid #1E2240;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}

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
    margin-bottom: 8px;
}

.sc-compare {
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

div[data-testid="stMetric"] {
    background: #131730;
    border: 1px solid #1E2240;
    border-radius: 12px;
    padding: 12px 16px;
}

div[data-testid="stMetric"] label {
    color: #565B7A !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    color: #E4E6F0;
    font-size: 20px;
    font-weight: 600;
}

.stTabs [data-baseweb="tab-list"] {
    background: #111528;
    border-radius: 10px;
    padding: 3px;
}

.stTabs [aria-selected="true"] {
    background: #131730 !important;
    color: #E4E6F0 !important;
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root { color-scheme: light; }

.stApp {
    background: #FFFFFF;
    font-family: 'Outfit', sans-serif;
    color: #111827;
}

section[data-testid="stSidebar"] {
    background: #F6F7FB;
    border-right: 1px solid #E5E7EB;
}

.main-header {
    background: linear-gradient(135deg, #F6F7FB 0%, #FFFFFF 100%);
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}

.score-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 18px 20px 16px;
    height: 100%;
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
    margin-bottom: 8px;
}

.sc-compare.up { color: #0F7A52; }
.sc-compare.down { color: #B42318; }

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

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 12px 16px;
}

div[data-testid="stMetric"] label {
    color: #6B7280 !important;
    font-size: 11px !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    color: #111827;
    font-size: 20px;
    font-weight: 700;
}
</style>
"""

def apply_theme_css(mode: str):
    st.markdown(DARK_CSS if mode == "dark" else LIGHT_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# PLOTLY THEME
# ══════════════════════════════════════════════
COLORS = {
    'blue': '#5B8DEF', 'green': '#3DDFA0', 'red': '#F06A6A',
    'amber': '#F0B05A', 'purple': '#9B7AEF', 'cyan': '#4FD1D9',
    'pink': '#F06A9B', 'orange': '#FB923C',
}
COLOR_SEQ = list(COLORS.values())

def apply_layout(fig, mode: str, **kwargs):
    if mode == "dark":
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#131730',
            plot_bgcolor='#131730',
            font=dict(family='Outfit, sans-serif', color='#8B90AD', size=12),
            margin=dict(l=20, r=20, t=40, b=20),
            colorway=COLOR_SEQ,
            **kwargs
        )
    else:
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            font=dict(family='Outfit, sans-serif', color='#374151', size=12),
            margin=dict(l=20, r=20, t=40, b=20),
            colorway=COLOR_SEQ,
            **kwargs
        )
    return fig

# ══════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_data():
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
    st.error("⚠️ Файл `TF_Dashboard_Dataset_v2.xlsx` не знайдено.")
    st.stop()

# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 T&F Dashboard")
    st.markdown("---")
    st.markdown("### 🎨 Theme")
    _is_dark = st.toggle("Dark mode", value=(st.session_state.theme_mode == "dark"))
    st.session_state.theme_mode = "dark" if _is_dark else "light"
    st.markdown("---")

    min_date = df_traffic['date'].min().date()
    max_date = df_traffic['date'].max().date()
    date_range = st.date_input("📅 Період", value=(max_date - timedelta(days=30), max_date),
                                min_value=min_date, max_value=max_date)
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    st.markdown("---")
    all_geos = sorted(df_traffic['geo'].unique())
    selected_geos = st.multiselect("🌍 Країни", all_geos, default=all_geos)
    all_brands = sorted(df_traffic['brand'].unique())
    selected_brands = st.multiselect("🏷️ Бренди", all_brands, default=all_brands)
    all_platforms = sorted(df_traffic['platform'].unique())
    selected_platforms = st.multiselect("📱 Платформи", all_platforms, default=all_platforms)
    all_sources = sorted(df_traffic['traffic_source'].unique())
    selected_sources = st.multiselect("📡 Джерела трафіку", all_sources, default=all_sources)

apply_theme_css(st.session_state.theme_mode)
MODE = st.session_state.theme_mode

# ══════════════════════════════════════════════
# FILTER DATA
# ══════════════════════════════════════════════
def filter_traffic(df, start, end, geos, brands, platforms, sources):
    mask = (
        (df['date'].dt.date >= start) & (df['date'].dt.date <= end) &
        (df['geo'].isin(geos)) & (df['brand'].isin(brands)) &
        (df['platform'].isin(platforms)) & (df['traffic_source'].isin(sources))
    )
    return df[mask].copy()

df = filter_traffic(df_traffic, start_date, end_date, selected_geos, selected_brands, selected_platforms, selected_sources)
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

def scorecard_html(label, value, change_pct, sub_text="", accent_color="#5B8DEF"):
    direction = "up" if change_pct >= 0 else "down"
    symbol = "▲" if direction == "up" else "▼"
    return f"""
    <div class="score-card">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{accent_color}"></div>
        <div class="sc-label">{label}</div>
        <div class="sc-value">{value}</div>
        <div class="sc-compare {direction}">{symbol} {abs(change_pct)*100:.1f}%</div>
        <div class="sc-sub">{sub_text}</div>
    </div>
    """

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
        'registrations': regs, 'ftd_count': ftd_c, 'ftd_amount': ftd_a,
        'net_revenue': net_rev, 'ggr': ggr, 'bonus_cost': bonus, 'cpa_cost': cpa,
        'reg2dep': safe_div(ftd_c, regs),
        'approval_rate': safe_div(p_ok, p_att),
        'avg_ftd_check': safe_div(ftd_a, ftd_c),
        'effective_cpa': safe_div(cpa, ftd_c),
        'roi': safe_div(net_rev - cpa - bonus, cpa + bonus) if (cpa + bonus) > 0 else 0,
        'margin': net_rev - cpa - bonus,
        'ctr': safe_div(clk, imp),
        'ggr_margin': safe_div(ggr, dep_total),
        'active_players': active, 'sessions': sessions,
        'impressions': imp, 'clicks': clk, 'deposits_total': dep_total,
    }

kpi = compute_kpis(df)
kpi_prev = compute_kpis(df_prev)

# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab_exec, tab_daily, tab_weekly, tab_payments, tab_agents = st.tabs([
    "🏠 Executive Summary",
    "📊 Daily Operations",
    "📈 Weekly Trends",
    "💳 Payment & Conversion Health",
    "👥 Traffic & Agent Efficiency",
])

# ═══════════════════════════════════════════════════
# TAB 1: EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════
with tab_exec:
    st.markdown(f"""
    <div class="main-header">
        <h1>Traffic & Finance Dashboard</h1>
        <p style="font-size:13px;color:#565B7A;margin-top:4px">
            Acquisition Focus · {start_date.strftime('%b %d')} — {end_date.strftime('%b %d, %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main scorecards
    cols = st.columns(6)
    sc_data = [
        ("Registrations", fmt_num(kpi['registrations']), pct_change(kpi['registrations'], kpi_prev['registrations']), 
         f"vs prev: {fmt_num(kpi_prev['registrations'])}", COLORS['blue']),
        ("FTD Count", fmt_num(kpi['ftd_count']), pct_change(kpi['ftd_count'], kpi_prev['ftd_count']),
         f"vs prev: {fmt_num(kpi_prev['ftd_count'])}", COLORS['green']),
        ("Reg2Dep", fmt_pct(kpi['reg2dep']), pct_change(kpi['reg2dep'], kpi_prev['reg2dep']),
         "Target: 18%", COLORS['purple']),
        ("FTD Amount", fmt_money(kpi['ftd_amount']), pct_change(kpi['ftd_amount'], kpi_prev['ftd_amount']),
         f"Avg: {fmt_money(kpi['avg_ftd_check'])}", COLORS['cyan']),
        ("Approval Rate", fmt_pct(kpi['approval_rate']), pct_change(kpi['approval_rate'], kpi_prev['approval_rate']),
         "Target: 85%", COLORS['amber']),
        ("Net Revenue", fmt_money(kpi['net_revenue']), pct_change(kpi['net_revenue'], kpi_prev['net_revenue']),
         f"Margin: {fmt_money(kpi['margin'])}", COLORS['red']),
    ]
    for i, (label, value, change, sub, color) in enumerate(sc_data):
        with cols[i]:
            st.markdown(scorecard_html(label, value, change, sub, color), unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # INTELLIGENT ALERTS - Business Impact Analysis
    # ════════════════════════════════════════════════════════════
    alerts = []
    
    # Alert 1: Reg2Dep Drop (Conversion Crisis)
    reg2dep_drop = kpi['reg2dep'] - kpi_prev['reg2dep']
    if reg2dep_drop < -0.02:  # Drop more than 2pp
        lost_ftd = abs(reg2dep_drop) * kpi['registrations']
        revenue_impact = lost_ftd * kpi['avg_ftd_check']
        alerts.append({
            'type': 'critical',
            'icon': '🔴',
            'title': 'CRITICAL: Conversion Rate Collapse',
            'message': f"Reg2Dep упала з **{kpi_prev['reg2dep']*100:.1f}%** до **{kpi['reg2dep']*100:.1f}%** (−{abs(reg2dep_drop)*100:.1f}pp)",
            'impact': f"Втрачено **~{int(lost_ftd)} FTD** • Estimated revenue loss: **{fmt_money(revenue_impact)}**",
            'recommendation': '→ Перевірте payment gateway stability, оновлення на сайті, та якість трафіку'
        })
    
    # Alert 2: Approval Rate Drop (Payment Issues)
    approval_drop = kpi['approval_rate'] - kpi_prev['approval_rate']
    if approval_drop < -0.05:  # Drop more than 5pp
        lost_approvals = abs(approval_drop) * kpi['registrations'] * kpi_prev['reg2dep']
        revenue_impact = lost_approvals * kpi['avg_ftd_check']
        alerts.append({
            'type': 'warning',
            'icon': '⚠️',
            'title': 'WARNING: Payment Approval Rate Deteriorating',
            'message': f"Approval rate впав з **{kpi_prev['approval_rate']*100:.1f}%** до **{kpi['approval_rate']*100:.1f}%** (−{abs(approval_drop)*100:.1f}pp)",
            'impact': f"Estimated lost deposits: **~{int(lost_approvals)}** • Revenue impact: **{fmt_money(revenue_impact)}**",
            'recommendation': '→ Негайно перевірте PSP status, fraud filters, та declined transactions breakdown'
        })
    
    # Alert 3: CPA Efficiency (Cost Spike)
    cpa_increase = (kpi['effective_cpa'] - kpi_prev['effective_cpa']) / kpi_prev['effective_cpa'] if kpi_prev['effective_cpa'] > 0 else 0
    if cpa_increase > 0.20:  # 20% increase
        extra_cost = (kpi['effective_cpa'] - kpi_prev['effective_cpa']) * kpi['ftd_count']
        alerts.append({
            'type': 'warning',
            'icon': '💸',
            'title': 'WARNING: CPA Spike Detected',
            'message': f"eCPA зріс з **{fmt_money(kpi_prev['effective_cpa'])}** до **{fmt_money(kpi['effective_cpa'])}** (+{cpa_increase*100:.1f}%)",
            'impact': f"Додаткові витрати: **{fmt_money(extra_cost)}** за період",
            'recommendation': '→ Оптимізуйте bid strategy, pause underperforming campaigns, перевірте targeting quality'
        })
    
    # Alert 4: ROI Negative Territory
    if kpi['roi'] < -0.20:  # ROI below -20%
        total_loss = kpi['margin']
        alerts.append({
            'type': 'critical',
            'icon': '💀',
            'title': 'CRITICAL: Negative ROI Territory',
            'message': f"ROI на рівні **{kpi['roi']*100:.1f}%** — бізнес втрачає гроші",
            'impact': f"Загальний збиток за період: **{fmt_money(abs(total_loss))}**",
            'recommendation': '→ НЕГАЙНО: pause unprofitable traffic sources, підвищіть retention, зменшіть bonus abuse'
        })
    
    # Alert 5: Registration Volume Drop (Traffic Issues)
    reg_drop = (kpi['registrations'] - kpi_prev['registrations']) / kpi_prev['registrations'] if kpi_prev['registrations'] > 0 else 0
    if reg_drop < -0.15:  # 15% drop
        lost_regs = abs(kpi['registrations'] - kpi_prev['registrations'])
        potential_ftd = lost_regs * kpi_prev['reg2dep']
        revenue_impact = potential_ftd * kpi['avg_ftd_check']
        alerts.append({
            'type': 'warning',
            'icon': '📉',
            'title': 'WARNING: Registration Volume Decline',
            'message': f"Реєстрації впали на **{abs(reg_drop)*100:.1f}%** ({fmt_num(kpi_prev['registrations'])} → {fmt_num(kpi['registrations'])})",
            'impact': f"Втрачено **~{int(potential_ftd)} FTD** • Revenue opportunity loss: **{fmt_money(revenue_impact)}**",
            'recommendation': '→ Перевірте media buying budget, ad account status, сезонність, конкурентні акції'
        })
    
    # Alert 6: Positive Alert - Performance Improvement
    if reg2dep_drop > 0.02 and kpi['reg2dep'] > 0.15:
        extra_ftd = reg2dep_drop * kpi['registrations']
        revenue_gain = extra_ftd * kpi['avg_ftd_check']
        alerts.append({
            'type': 'success',
            'icon': '🎯',
            'title': 'SUCCESS: Conversion Rate Improving',
            'message': f"Reg2Dep зріс з **{kpi_prev['reg2dep']*100:.1f}%** до **{kpi['reg2dep']*100:.1f}%** (+{reg2dep_drop*100:.1f}pp)",
            'impact': f"Додатково здобуто **~{int(extra_ftd)} FTD** • Extra revenue: **{fmt_money(revenue_gain)}**",
            'recommendation': '→ Проаналізуйте що спрацювало: масштабуйте успішні креативи, оффери, GEO'
        })
    
    # Display alerts if any exist
    if alerts:
        st.markdown('<div style="margin: 20px 0"></div>', unsafe_allow_html=True)
        
        # Sort: critical first, then warning, then success
        alert_priority = {'critical': 0, 'warning': 1, 'success': 2}
        alerts.sort(key=lambda x: alert_priority[x['type']])
        
        for alert in alerts:
            if alert['type'] == 'critical':
                bg_color = '#2D0E0E' if MODE == 'dark' else '#FEF2F2'
                border_color = '#F06A6A30' if MODE == 'dark' else '#FECACA'
                text_color = '#F06A6A' if MODE == 'dark' else '#B42318'
            elif alert['type'] == 'warning':
                bg_color = '#2D1F0E' if MODE == 'dark' else '#FFFBEB'
                border_color = '#F0B05A30' if MODE == 'dark' else '#FDE68A'
                text_color = '#F0B05A' if MODE == 'dark' else '#D97706'
            else:  # success
                bg_color = '#0E2D20' if MODE == 'dark' else '#F0FDF4'
                border_color = '#3DDFA030' if MODE == 'dark' else '#BBF7D0'
                text_color = '#3DDFA0' if MODE == 'dark' else '#15803D'
            
            st.markdown(f"""
            <div style="
                background: {bg_color};
                border: 1px solid {border_color};
                border-left: 4px solid {text_color};
                border-radius: 10px;
                padding: 16px 20px;
                margin-bottom: 12px;
                font-size: 13px;
            ">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px; line-height: 1;">{alert['icon']}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: {text_color}; margin-bottom: 6px; font-size: 14px;">
                            {alert['title']}
                        </div>
                        <div style="margin-bottom: 8px; line-height: 1.5;">
                            {alert['message']}
                        </div>
                        <div style="
                            font-family: 'JetBrains Mono', monospace;
                            font-weight: 600;
                            color: {text_color};
                            margin-bottom: 8px;
                            font-size: 13px;
                            padding: 8px 12px;
                            background: {'rgba(240,106,106,0.1)' if alert['type'] == 'critical' else 'rgba(240,176,90,0.1)' if alert['type'] == 'warning' else 'rgba(61,223,160,0.1)'};
                            border-radius: 6px;
                        ">
                            💰 {alert['impact']}
                        </div>
                        <div style="
                            font-size: 12px;
                            color: {'#8B90AD' if MODE == 'dark' else '#6B7280'};
                            font-style: italic;
                            padding-left: 12px;
                            border-left: 2px solid {border_color};
                        ">
                            {alert['recommendation']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Key Ratios</div>', unsafe_allow_html=True)
    
    # Using native Streamlit metrics
    metric_cols = st.columns(6)
    metrics_data = [
        ("CTR", fmt_pct(kpi['ctr'])),
        ("GGR Margin", fmt_pct(kpi['ggr_margin'])),
        ("eCPA", fmt_money(kpi['effective_cpa'])),
        ("ROI", fmt_pct(kpi['roi'])),
        ("Active Players", fmt_num(kpi['active_players'])),
        ("Sessions/Player", f"{safe_div(kpi['sessions'], kpi['active_players']):.1f}"),
    ]
    
    for i, (label, value) in enumerate(metrics_data):
        with metric_cols[i]:
            st.metric(label, value)

    st.markdown('<div class="sec-label">Acquisition Funnel Trends</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        daily = df.groupby('date').agg(
            registrations=('registrations', 'sum'),
            ftd_count=('ftd_count', 'sum'),
        ).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=daily['date'], y=daily['registrations'],
            name='Registrations', line=dict(color=COLORS['blue'], width=2),
            fill='tozeroy', fillcolor='rgba(91,141,239,0.05)',
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=daily['date'], y=daily['ftd_count'],
            name='FTD', line=dict(color=COLORS['green'], width=2),
        ), secondary_y=True)
        apply_layout(fig, MODE, title='Registrations & FTD')
        fig.update_yaxes(title_text="Registrations", secondary_y=False)
        fig.update_yaxes(title_text="FTD", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        daily_rev = df.groupby('date').agg(
            net_revenue=('net_revenue_usd', 'sum'),
            cpa_cost=('cpa_cost_usd', 'sum'),
            bonus_cost=('bonus_cost_usd', 'sum'),
        ).reset_index()

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=daily_rev['date'], y=daily_rev['net_revenue'], 
                              name='Net Revenue', marker_color=COLORS['green']))
        fig2.add_trace(go.Bar(x=daily_rev['date'], y=daily_rev['cpa_cost'],
                              name='CPA Cost', marker_color=COLORS['red']))
        apply_layout(fig2, MODE, title='Revenue vs Costs', barmode='group')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="sec-label">Split Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        plat_data = df.groupby('platform')['ftd_count'].sum().reset_index()
        fig_plat = px.pie(plat_data, values='ftd_count', names='platform', hole=0.65,
                          color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_plat, MODE, title='Platform Split (FTD)')
        st.plotly_chart(fig_plat, use_container_width=True, config={'displayModeBar': False})

    with c2:
        src_data = df.groupby('traffic_source')['registrations'].sum().reset_index()
        fig_src = px.pie(src_data, values='registrations', names='traffic_source', hole=0.65,
                         color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_src, MODE, title='Traffic Source (Regs)')
        st.plotly_chart(fig_src, use_container_width=True, config={'displayModeBar': False})

    with c3:
        geo_data = df.groupby('geo')['ftd_amount_usd'].sum().reset_index()
        fig_geo = px.pie(geo_data, values='ftd_amount_usd', names='geo', hole=0.65,
                         color_discrete_sequence=COLOR_SEQ)
        apply_layout(fig_geo, MODE, title='GEO (FTD Amount)')
        st.plotly_chart(fig_geo, use_container_width=True, config={'displayModeBar': False})

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
    geo_table['Approval_%'] = (geo_table['Payment_Approved'] / geo_table['Payment_Attempts'].replace(0, np.nan) * 100).round(1)
    geo_table['eCPA'] = (geo_table['CPA_Cost'] / geo_table['FTD'].replace(0, np.nan)).round(0)

    display_cols = ['geo', 'Registrations', 'FTD', 'Reg2Dep', 'FTD_Amount', 'Approval_%', 'Net_Revenue', 'eCPA']
    geo_display = geo_table[display_cols].sort_values('FTD_Amount', ascending=False)
    geo_display.columns = ['GEO', 'Regs', 'FTD', 'Reg2Dep %', 'FTD Amt $', 'Approval %', 'Net Rev $', 'eCPA $']

    st.dataframe(
        geo_display.style.format({
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}', 'Reg2Dep %': '{:.1f}%',
            'FTD Amt $': '${:,.0f}', 'Approval %': '{:.1f}%', 
            'Net Rev $': '${:,.0f}', 'eCPA $': '${:.0f}'
        }).background_gradient(subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25),
        use_container_width=True, hide_index=True,
    )

# ═══════════════════════════════════════════════════
# TAB 2: DAILY OPERATIONS
# ═══════════════════════════════════════════════════
with tab_daily:
    st.markdown('<div class="sec-label">Daily Operations</div>', unsafe_allow_html=True)
    
    daily_tbl = df.groupby('date').agg(
        Regs=('registrations', 'sum'),
        FTD=('ftd_count', 'sum'),
        FTD_Amt=('ftd_amount_usd', 'sum'),
        Net_Rev=('net_revenue_usd', 'sum'),
        P_Att=('payment_attempts', 'sum'),
        P_App=('payment_approved', 'sum'),
    ).reset_index().sort_values('date', ascending=False)

    daily_tbl['Reg2Dep'] = (daily_tbl['FTD'] / daily_tbl['Regs'].replace(0, np.nan) * 100).round(1)
    daily_tbl['Approval'] = (daily_tbl['P_App'] / daily_tbl['P_Att'].replace(0, np.nan) * 100).round(1)
    
    display_daily = daily_tbl[['date', 'Regs', 'FTD', 'Reg2Dep', 'FTD_Amt', 'Approval', 'Net_Rev']].head(30)
    display_daily.columns = ['Date', 'Regs', 'FTD', 'Reg2Dep %', 'FTD Amt $', 'Approval %', 'Net Rev $']

    st.dataframe(
        display_daily.style.format({
            'Date': lambda x: x.strftime('%Y-%m-%d'), 
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}',
            'Reg2Dep %': '{:.1f}%', 'FTD Amt $': '${:,.0f}', 
            'Approval %': '{:.1f}%', 'Net Rev $': '${:,.0f}'
        }).background_gradient(subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25),
        use_container_width=True, hide_index=True, height=600,
    )

# ═══════════════════════════════════════════════════
# TAB 3: WEEKLY TRENDS
# ═══════════════════════════════════════════════════
with tab_weekly:
    st.markdown('<div class="sec-label">Weekly Trends</div>', unsafe_allow_html=True)
    
    df_full = filter_traffic(df_traffic, min_date, max_date, selected_geos, selected_brands, selected_platforms, selected_sources)
    weekly = df_full.copy()
    weekly['week'] = weekly['date'].dt.isocalendar().week.astype(int)
    weekly['year'] = weekly['date'].dt.year
    
    wk = weekly.groupby(['year', 'week']).agg(
        regs=('registrations', 'sum'),
        ftd=('ftd_count', 'sum'),
        ftd_amt=('ftd_amount_usd', 'sum'),
        net_rev=('net_revenue_usd', 'sum'),
    ).reset_index()
    
    wk['reg2dep'] = wk['ftd'] / wk['regs'].replace(0, np.nan)
    wk['period'] = wk['year'].astype(str) + '-W' + wk['week'].astype(str).str.zfill(2)
    wk = wk.sort_values(['year', 'week'])
    
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        fig_wv = make_subplots(specs=[[{"secondary_y": True}]])
        fig_wv.add_trace(go.Bar(x=wk['period'], y=wk['regs'], name='Registrations',
                                marker_color=COLORS['blue'], opacity=0.5), secondary_y=False)
        fig_wv.add_trace(go.Scatter(x=wk['period'], y=wk['ftd'], name='FTD',
                                    line=dict(color=COLORS['green'], width=2.5)), secondary_y=True)
        apply_layout(fig_wv, MODE, title='Weekly Volume')
        fig_wv.update_yaxes(title_text="Registrations", secondary_y=False)
        fig_wv.update_yaxes(title_text="FTD", secondary_y=True)
        st.plotly_chart(fig_wv, use_container_width=True, config={'displayModeBar': False})
    
    with col_w2:
        fig_wr = go.Figure()
        fig_wr.add_trace(go.Bar(x=wk['period'], y=wk['net_rev'], name='Net Revenue',
                                marker_color=COLORS['green']))
        apply_layout(fig_wr, MODE, title='Weekly Revenue')
        st.plotly_chart(fig_wr, use_container_width=True, config={'displayModeBar': False})

# ═══════════════════════════════════════════════════
# TAB 4: PAYMENT & CONVERSION HEALTH
# ═══════════════════════════════════════════════════
with tab_payments:
    st.markdown('<div class="sec-label">Payment & Conversion Health</div>', unsafe_allow_html=True)
    
    st.markdown("#### Payment Funnel")
    funnel_cols = st.columns(6)
    
    clicks = int(df['clicks'].sum())
    regs = int(df['registrations'].sum())
    attempts = int(df['payment_attempts'].sum())
    approved = int(df['payment_approved'].sum())
    ftd = int(df['ftd_count'].sum())
    
    with funnel_cols[0]:
        st.metric("Clicks", fmt_num(clicks))
    with funnel_cols[1]:
        st.metric("Registrations", fmt_num(regs))
    with funnel_cols[2]:
        st.metric("Click→Reg", fmt_pct(safe_div(regs, clicks)))
    with funnel_cols[3]:
        st.metric("Attempts", fmt_num(attempts))
    with funnel_cols[4]:
        st.metric("Approved", fmt_num(approved))
    with funnel_cols[5]:
        st.metric("Reg→FTD", fmt_pct(safe_div(ftd, regs)))
    
    st.markdown('<div class="sec-label">Payment Approval Trend</div>', unsafe_allow_html=True)
    
    trend = df.groupby('date').agg(
        attempts=('payment_attempts', 'sum'),
        approved=('payment_approved', 'sum'),
    ).reset_index()
    trend['approval_rate'] = trend['approved'] / trend['attempts'].replace(0, np.nan)
    
    fig_ap = go.Figure()
    fig_ap.add_trace(go.Scatter(x=trend['date'], y=trend['approval_rate'],
                                name='Approval Rate', line=dict(color=COLORS['green'], width=2)))
    apply_layout(fig_ap, MODE, title='Daily Approval Rate', yaxis_tickformat='.0%')
    st.plotly_chart(fig_ap, use_container_width=True, config={'displayModeBar': False})

# ═══════════════════════════════════════════════════
# TAB 5: TRAFFIC & AGENT EFFICIENCY
# ═══════════════════════════════════════════════════
with tab_agents:
    st.markdown('<div class="sec-label">Traffic & Agent Efficiency</div>', unsafe_allow_html=True)
    
    a = df.copy()
    if a.empty:
        st.info("Немає даних за вибраними фільтрами.")
    else:
        agg = a.groupby('agent', as_index=False).agg(
            Clicks=('clicks','sum'),
            Regs=('registrations','sum'),
            FTD=('ftd_count','sum'),
            FTD_Amt=('ftd_amount_usd','sum'),
        )
        
        agg['Reg2FTD %'] = agg['FTD'] / agg['Regs'].replace(0, np.nan)
        agg['Click2Reg %'] = agg['Regs'] / agg['Clicks'].replace(0, np.nan)
        agg = agg.sort_values('FTD_Amt', ascending=False)
        
        st.dataframe(
            agg.style.format({
                'Clicks':'{:,.0f}','Regs':'{:,.0f}','FTD':'{:,.0f}',
                'Click2Reg %':'{:.1%}','Reg2FTD %':'{:.1%}',
                'FTD_Amt':'${:,.0f}'
            }).background_gradient(subset=['Reg2FTD %'], cmap='RdYlGn', vmin=0, vmax=0.20),
            use_container_width=True, hide_index=True
        )
