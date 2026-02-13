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
    background: #F9FAFB;
    font-family: 'Outfit', sans-serif;
    color: #111827;
}

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

.main-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
    border: 1px solid #D1D5DB;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.score-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 18px 20px 16px;
    height: 100%;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    transition: all .3s;
}

.score-card:hover {
    border-color: #D1D5DB;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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

.sc-compare.up { color: #059669; }
.sc-compare.down { color: #DC2626; }

.sec-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6B7280;
    font-weight: 800;
    margin: 24px 0 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #E5E7EB;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

div[data-testid="stMetric"] label {
    color: #6B7280 !important;
    font-size: 11px !important;
    font-weight: 600;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    color: #111827;
    font-size: 20px;
    font-weight: 700;
}

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
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    
    # Agent filter
    all_agents = sorted([x for x in df_traffic['agent'].dropna().unique().tolist() if str(x).strip() != ""])
    selected_agents = st.multiselect("👤 Агенти", all_agents, default=all_agents)

apply_theme_css(st.session_state.theme_mode)
MODE = st.session_state.theme_mode

# ══════════════════════════════════════════════
# FILTER DATA
# ══════════════════════════════════════════════
def filter_traffic(df, start, end, geos, brands, platforms, sources, agents):
    mask = (
        (df['date'].dt.date >= start) & (df['date'].dt.date <= end) &
        (df['geo'].isin(geos)) & (df['brand'].isin(brands)) &
        (df['platform'].isin(platforms)) & (df['traffic_source'].isin(sources)) &
        (df['agent'].isin(agents))
    )
    return df[mask].copy()

df = filter_traffic(df_traffic, start_date, end_date, selected_geos, selected_brands, selected_platforms, selected_sources, selected_agents)
period_days = (end_date - start_date).days + 1
prev_start = start_date - timedelta(days=period_days)
prev_end = start_date - timedelta(days=1)
df_prev = filter_traffic(df_traffic, prev_start, prev_end, selected_geos, selected_brands, selected_platforms, selected_sources, selected_agents)

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
    
    # Alert 1: Reg2Dep Drop (Conversion Optimization Opportunity)
    reg2dep_drop = kpi['reg2dep'] - kpi_prev['reg2dep']
    if reg2dep_drop < -0.02:  # Drop more than 2pp
        lost_ftd = abs(reg2dep_drop) * kpi['registrations']
        revenue_impact = lost_ftd * kpi['avg_ftd_check']
        alerts.append({
            'type': 'critical',
            'icon': '📊',
            'title': 'Conversion Rate Needs Attention',
            'message': f"Reg2Dep знизився з **{kpi_prev['reg2dep']*100:.1f}%** до **{kpi['reg2dep']*100:.1f}%** (−{abs(reg2dep_drop)*100:.1f}pp)",
            'impact': f"Потенціал для покращення: **~{int(lost_ftd)} FTD** • Revenue opportunity: **{fmt_money(revenue_impact)}**",
            'recommendation': 'Рекомендації: перевірте user journey, payment flow stability, та якість incoming traffic'
        })
    
    # Alert 2: Approval Rate Drop (Payment Optimization)
    approval_drop = kpi['approval_rate'] - kpi_prev['approval_rate']
    if approval_drop < -0.05:  # Drop more than 5pp
        lost_approvals = abs(approval_drop) * kpi['registrations'] * kpi_prev['reg2dep']
        revenue_impact = lost_approvals * kpi['avg_ftd_check']
        alerts.append({
            'type': 'warning',
            'icon': '💳',
            'title': 'Payment Success Rate Declined',
            'message': f"Approval rate змінився: **{kpi_prev['approval_rate']*100:.1f}%** → **{kpi['approval_rate']*100:.1f}%** (−{abs(approval_drop)*100:.1f}pp)",
            'impact': f"Можлива оптимізація: **~{int(lost_approvals)}** deposits • Potential gain: **{fmt_money(revenue_impact)}**",
            'recommendation': 'Варто перевірити: PSP performance, fraud rules configuration, та declined transaction patterns'
        })
    
    # Alert 3: CPA Efficiency (Cost Optimization Opportunity)
    cpa_increase = (kpi['effective_cpa'] - kpi_prev['effective_cpa']) / kpi_prev['effective_cpa'] if kpi_prev['effective_cpa'] > 0 else 0
    if cpa_increase > 0.20:  # 20% increase
        extra_cost = (kpi['effective_cpa'] - kpi_prev['effective_cpa']) * kpi['ftd_count']
        alerts.append({
            'type': 'warning',
            'icon': '💡',
            'title': 'Media Buying Efficiency Opportunity',
            'message': f"eCPA збільшився: **{fmt_money(kpi_prev['effective_cpa'])}** → **{fmt_money(kpi['effective_cpa'])}** (+{cpa_increase*100:.1f}%)",
            'impact': f"Потенціал економії: **{fmt_money(extra_cost)}** за період",
            'recommendation': 'Можливі дії: оптимізація bid strategy, review campaign performance, A/B test креативів'
        })
    
    # Alert 4: ROI Below Target (Profitability Focus)
    if kpi['roi'] < -0.20:  # ROI below -20%
        total_loss = kpi['margin']
        break_even_needed = abs(total_loss) / (kpi['ftd_count'] if kpi['ftd_count'] > 0 else 1)
        alerts.append({
            'type': 'critical',
            'icon': '📈',
            'title': 'ROI Below Target - Action Plan Needed',
            'message': f"Поточний ROI: **{kpi['roi']*100:.1f}%** — є простір для оптимізації",
            'impact': f"Gap to break-even: **{fmt_money(abs(total_loss))}** • Need ~**{fmt_money(break_even_needed)}** more per FTD",
            'recommendation': 'Фокус на: retention programs, reduce bonus abuse, optimize traffic mix, improve LTV'
        })
    
    # Alert 5: Registration Volume Drop (Growth Opportunity)
    reg_drop = (kpi['registrations'] - kpi_prev['registrations']) / kpi_prev['registrations'] if kpi_prev['registrations'] > 0 else 0
    if reg_drop < -0.15:  # 15% drop
        lost_regs = abs(kpi['registrations'] - kpi_prev['registrations'])
        potential_ftd = lost_regs * kpi_prev['reg2dep']
        revenue_impact = potential_ftd * kpi['avg_ftd_check']
        alerts.append({
            'type': 'warning',
            'icon': '🎯',
            'title': 'Traffic Volume Growth Opportunity',
            'message': f"Реєстрації: **{fmt_num(kpi_prev['registrations'])}** → **{fmt_num(kpi['registrations'])}** (−{abs(reg_drop)*100:.1f}%)",
            'impact': f"Opportunity: **~{int(potential_ftd)} FTD** • Revenue potential: **{fmt_money(revenue_impact)}**",
            'recommendation': 'Розгляньте: збільшення media spend, нові traffic sources, seasonal adjustments, competitor analysis'
        })
    
    # Alert 6: Positive Alert - Performance Win
    if reg2dep_drop > 0.02 and kpi['reg2dep'] > 0.15:
        extra_ftd = reg2dep_drop * kpi['registrations']
        revenue_gain = extra_ftd * kpi['avg_ftd_check']
        alerts.append({
            'type': 'success',
            'icon': '✨',
            'title': 'Great Performance - Conversion Improving',
            'message': f"Reg2Dep покращився: **{kpi_prev['reg2dep']*100:.1f}%** → **{kpi['reg2dep']*100:.1f}%** (+{reg2dep_drop*100:.1f}pp)",
            'impact': f"Додатковий результат: **~{int(extra_ftd)} FTD** • Extra revenue: **{fmt_money(revenue_gain)}**",
            'recommendation': 'Наступні кроки: документуйте що спрацювало, масштабуйте успішні кампанії та креативи'
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
    
    # ════════════════════════════════════════════════════════════
    # ADVANCED BREAKDOWNS
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">🎯 Traffic Quality & Performance Analysis</div>', unsafe_allow_html=True)
    
    adv_col1, adv_col2 = st.columns(2)
    
    with adv_col1:
        # Traffic Source Performance with Reg2Dep
        src_perf = df.groupby('traffic_source').agg(
            Regs=('registrations', 'sum'),
            FTD=('ftd_count', 'sum'),
            Revenue=('net_revenue_usd', 'sum'),
            CPA=('cpa_cost_usd', 'sum'),
        ).reset_index()
        src_perf['Reg2Dep'] = src_perf['FTD'] / src_perf['Regs'].replace(0, np.nan)
        src_perf['ROI'] = ((src_perf['Revenue'] - src_perf['CPA']) / src_perf['CPA'].replace(0, np.nan))
        src_perf = src_perf.sort_values('Revenue', ascending=True)
        
        fig_src = go.Figure()
        fig_src.add_trace(go.Bar(
            y=src_perf['traffic_source'], x=src_perf['Revenue'],
            name='Net Revenue', orientation='h', marker_color=COLORS['green'],
            text=src_perf['Reg2Dep'].apply(lambda x: f"{x:.1%}"),
            textposition='inside', textfont=dict(color='white', size=11),
        ))
        
        apply_layout(fig_src, MODE, title='📡 Traffic Source Performance (Revenue & Reg2Dep %)')
        st.plotly_chart(fig_src, use_container_width=True, config={'displayModeBar': False})
    
    with adv_col2:
        # Platform + Brand Matrix
        plat_brand = df.groupby(['platform', 'brand']).agg(
            FTD=('ftd_count', 'sum'),
        ).reset_index()
        
        fig_pb = px.sunburst(
            plat_brand, path=['platform', 'brand'], values='FTD',
            color='FTD', color_continuous_scale='Viridis',
        )
        apply_layout(fig_pb, MODE, title='📱🏷️ Platform × Brand Distribution')
        fig_pb.update_traces(textinfo='label+percent parent')
        st.plotly_chart(fig_pb, use_container_width=True, config={'displayModeBar': False})
    
    # ════════════════════════════════════════════════════════════
    # CONVERSION FUNNEL SANKEY
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">🎯 Full Conversion Funnel</div>', unsafe_allow_html=True)
    
    total_impressions = int(kpi['impressions'])
    total_clicks = int(kpi['clicks'])
    total_regs = int(kpi['registrations'])
    total_attempts = int(df['payment_attempts'].sum())
    total_approved = int(df['payment_approved'].sum())
    total_ftd = int(kpi['ftd_count'])
    
    # Sankey diagram for funnel
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["Impressions", "Clicks", "Registrations", "Payment Attempts", "Approved", "FTD"],
            color=[COLORS['cyan'], COLORS['blue'], COLORS['purple'], COLORS['amber'], COLORS['green'], COLORS['green']],
        ),
        link=dict(
            source=[0, 1, 2, 3, 4],
            target=[1, 2, 3, 4, 5],
            value=[total_clicks, total_regs, total_attempts, total_approved, total_ftd],
            color=['rgba(91,141,239,0.3)', 'rgba(155,122,239,0.3)', 'rgba(240,176,90,0.3)', 
                   'rgba(61,223,160,0.3)', 'rgba(61,223,160,0.5)'],
        )
    )])
    
    apply_layout(fig_sankey, MODE, title='Conversion Funnel Flow', height=400)
    st.plotly_chart(fig_sankey, use_container_width=True, config={'displayModeBar': False})
    
    # Add funnel metrics below
    funnel_cols = st.columns(6)
    funnel_stages = [
        ("Impressions", fmt_num(total_impressions), fmt_pct(safe_div(total_clicks, total_impressions))),
        ("Clicks", fmt_num(total_clicks), fmt_pct(safe_div(total_regs, total_clicks))),
        ("Regs", fmt_num(total_regs), fmt_pct(safe_div(total_attempts, total_regs))),
        ("Attempts", fmt_num(total_attempts), fmt_pct(safe_div(total_approved, total_attempts))),
        ("Approved", fmt_num(total_approved), fmt_pct(safe_div(total_ftd, total_approved))),
        ("FTD", fmt_num(total_ftd), fmt_pct(safe_div(total_ftd, total_regs))),
    ]
    
    for i, (stage, value, rate) in enumerate(funnel_stages):
        with funnel_cols[i]:
            st.metric(stage, value, rate)

# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# TAB 2: DAILY OPERATIONS
# ═══════════════════════════════════════════════════
with tab_daily:
    # ════════════════════════════════════════════════════════════
    # TODAY vs YESTERDAY KPI COMPARISON (FIRST!)
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">Daily Change Analysis (vs Previous Day)</div>', unsafe_allow_html=True)
    
    today_date = df['date'].max()
    yesterday_date = today_date - timedelta(days=1)
    
    today_data = df[df['date'] == today_date]
    yesterday_data = df[df['date'] == yesterday_date]
    
    today_kpi = compute_kpis(today_data)
    yesterday_kpi = compute_kpis(yesterday_data)
    
    st.markdown(f"**Today ({today_date.strftime('%Y-%m-%d')})** vs **Yesterday ({yesterday_date.strftime('%Y-%m-%d')})**")
    
    kpi_cols = st.columns(6)
    
    kpi_comparisons = [
        ("Registrations", today_kpi['registrations'], yesterday_kpi['registrations'], "num"),
        ("FTD Count", today_kpi['ftd_count'], yesterday_kpi['ftd_count'], "num"),
        ("Reg2Dep", today_kpi['reg2dep'], yesterday_kpi['reg2dep'], "pct"),
        ("Approval Rate", today_kpi['approval_rate'], yesterday_kpi['approval_rate'], "pct"),
        ("Avg Check", today_kpi['avg_ftd_check'], yesterday_kpi['avg_ftd_check'], "money"),
        ("Net Revenue", today_kpi['net_revenue'], yesterday_kpi['net_revenue'], "money"),
    ]
    
    for i, (label, today_val, yesterday_val, fmt_type) in enumerate(kpi_comparisons):
        with kpi_cols[i]:
            if fmt_type == "pct":
                display_val = fmt_pct(today_val)
                delta_val = (today_val - yesterday_val) * 100
                delta_str = f"{delta_val:+.1f}pp"
            elif fmt_type == "money":
                display_val = fmt_money(today_val)
                if yesterday_val != 0:
                    delta_pct = ((today_val - yesterday_val) / yesterday_val) * 100
                    delta_str = f"{delta_pct:+.1f}%"
                else:
                    delta_str = "N/A"
            else:  # num
                display_val = fmt_num(today_val)
                if yesterday_val != 0:
                    delta_pct = ((today_val - yesterday_val) / yesterday_val) * 100
                    delta_str = f"{delta_pct:+.1f}%"
                else:
                    delta_str = "N/A"
            
            st.metric(label, display_val, delta_str)
    
    # ════════════════════════════════════════════════════════════
    # PLATFORM COMPARISON
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">📱 Platform Comparison</div>', unsafe_allow_html=True)
    
    platform_col1, platform_col2 = st.columns(2)
    
    with platform_col1:
        # Platform - Regs vs FTD
        plat_agg = df.groupby('platform').agg(
            Regs=('registrations', 'sum'),
            FTD=('ftd_count', 'sum'),
        ).reset_index().sort_values('Regs', ascending=False)
        
        fig_plat = go.Figure()
        fig_plat.add_trace(go.Bar(
            x=plat_agg['platform'], y=plat_agg['Regs'],
            name='Regs', marker_color=COLORS['blue'], opacity=0.8
        ))
        fig_plat.add_trace(go.Bar(
            x=plat_agg['platform'], y=plat_agg['FTD'],
            name='FTD', marker_color=COLORS['green']
        ))
        
        apply_layout(fig_plat, MODE, title='Regs vs FTD', barmode='group')
        st.plotly_chart(fig_plat, use_container_width=True, config={'displayModeBar': False})
    
    with platform_col2:
        # Platform - Reg2Dep Conversion Rate
        plat_agg['Reg2Dep'] = plat_agg['FTD'] / plat_agg['Regs'].replace(0, np.nan)
        
        fig_plat_conv = go.Figure()
        fig_plat_conv.add_trace(go.Bar(
            x=plat_agg['platform'], y=plat_agg['Reg2Dep'],
            marker_color=COLORS['purple'],
            text=plat_agg['Reg2Dep'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else ""),
            textposition='outside',
        ))
        
        apply_layout(fig_plat_conv, MODE, title='Conversion Rate by Platform', yaxis_tickformat='.0%')
        st.plotly_chart(fig_plat_conv, use_container_width=True, config={'displayModeBar': False})
    
    # ════════════════════════════════════════════════════════════
    # REG METHODS
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">📝 Reg Methods</div>', unsafe_allow_html=True)
    
    reg_col1, reg_col2 = st.columns(2)
    
    with reg_col1:
        # Registration Methods - By Method (Horizontal bars)
        reg_method_agg = df.groupby('reg_method').agg(
            Regs=('registrations', 'sum'),
            FTD=('ftd_count', 'sum'),
        ).reset_index().sort_values('Regs', ascending=True)
        
        fig_rm = go.Figure()
        fig_rm.add_trace(go.Bar(
            y=reg_method_agg['reg_method'], x=reg_method_agg['Regs'],
            name='Regs', orientation='h', marker_color=COLORS['blue'], opacity=0.8
        ))
        fig_rm.add_trace(go.Bar(
            y=reg_method_agg['reg_method'], x=reg_method_agg['FTD'],
            name='FTD', orientation='h', marker_color=COLORS['green']
        ))
        
        apply_layout(fig_rm, MODE, title='By Method', barmode='group')
        st.plotly_chart(fig_rm, use_container_width=True, config={'displayModeBar': False})
    
    with reg_col2:
        # Registration Methods - Conversion Rate
        reg_method_agg['Reg2Dep'] = reg_method_agg['FTD'] / reg_method_agg['Regs'].replace(0, np.nan)
        
        fig_rm_conv = go.Figure()
        fig_rm_conv.add_trace(go.Bar(
            y=reg_method_agg['reg_method'], x=reg_method_agg['Reg2Dep'],
            orientation='h', marker_color=COLORS['purple'],
            text=reg_method_agg['Reg2Dep'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else ""),
            textposition='outside',
        ))
        
        apply_layout(fig_rm_conv, MODE, title='Conversion Rate by Method', xaxis_tickformat='.0%')
        st.plotly_chart(fig_rm_conv, use_container_width=True, config={'displayModeBar': False})
    
    # ════════════════════════════════════════════════════════════
    # ADDITIONAL INSIGHTS
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">💡 Additional Insights</div>', unsafe_allow_html=True)
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        # Traffic Source Performance
        traffic_agg = df.groupby('traffic_source').agg(
            Regs=('registrations', 'sum'),
            FTD=('ftd_count', 'sum'),
            Revenue=('net_revenue_usd', 'sum'),
        ).reset_index()
        traffic_agg['Reg2Dep'] = traffic_agg['FTD'] / traffic_agg['Regs'].replace(0, np.nan)
        traffic_agg = traffic_agg.sort_values('Revenue', ascending=True)
        
        fig_traffic = go.Figure()
        fig_traffic.add_trace(go.Bar(
            y=traffic_agg['traffic_source'], x=traffic_agg['Revenue'],
            orientation='h', marker_color=COLORS['cyan'],
            text=traffic_agg['Reg2Dep'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else ""),
            textposition='inside', textfont=dict(color='white', size=11),
        ))
        
        apply_layout(fig_traffic, MODE, title='📡 Traffic Source Revenue & Conversion')
        st.plotly_chart(fig_traffic, use_container_width=True, config={'displayModeBar': False})
    
    with insight_col2:
        # Top GEO Performance
        geo_agg = df.groupby('geo').agg(
            FTD=('ftd_count', 'sum'),
            Revenue=('net_revenue_usd', 'sum'),
        ).reset_index().sort_values('Revenue', ascending=False).head(10)
        
        fig_geo = go.Figure()
        fig_geo.add_trace(go.Bar(
            x=geo_agg['geo'], y=geo_agg['Revenue'],
            marker_color=COLORS['green'],
            text=geo_agg['FTD'].apply(lambda x: f"{int(x)} FTD"),
            textposition='outside',
        ))
        
        apply_layout(fig_geo, MODE, title='🌍 Top 10 GEO by Revenue')
        st.plotly_chart(fig_geo, use_container_width=True, config={'displayModeBar': False})
    
    # ════════════════════════════════════════════════════════════
    # DAILY OPERATIONS TABLE (AT THE END!)
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">Daily Operations — Performance Table</div>', unsafe_allow_html=True)
    
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
    daily_tbl['Day'] = daily_tbl['date'].dt.strftime('%a')
    
    display_daily = daily_tbl[['date', 'Day', 'Regs', 'FTD', 'Reg2Dep', 'FTD_Amt', 'Approval', 'Net_Rev']].head(30)
    display_daily.columns = ['Date', 'Day', 'Regs', 'FTD', 'Reg2Dep %', 'FTD Amt $', 'Approval %', 'Net Rev $']

    st.dataframe(
        display_daily.style.format({
            'Date': lambda x: x.strftime('%Y-%m-%d'), 
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}',
            'Reg2Dep %': '{:.1f}%', 'FTD Amt $': '${:,.0f}', 
            'Approval %': '{:.1f}%', 'Net Rev $': '${:,.0f}'
        }).background_gradient(subset=['Reg2Dep %'], cmap='RdYlGn', vmin=0, vmax=25)
         .background_gradient(subset=['Approval %'], cmap='RdYlGn', vmin=50, vmax=95),
        use_container_width=True, hide_index=True, height=500,
    )

# ═══════════════════════════════════════════════════
# TAB 3: WEEKLY TRENDS
# ═══════════════════════════════════════════════════
with tab_weekly:
    st.markdown('<div class="sec-label">Weekly Trends</div>', unsafe_allow_html=True)
    
    df_full = filter_traffic(df_traffic, min_date, max_date, selected_geos, selected_brands, selected_platforms, selected_sources, selected_agents)
    weekly = df_full.copy()
    weekly['week'] = weekly['date'].dt.isocalendar().week.astype(int)
    weekly['year'] = weekly['date'].dt.year
    
    wk = weekly.groupby(['year', 'week']).agg(
        regs=('registrations', 'sum'),
        ftd=('ftd_count', 'sum'),
        ftd_amt=('ftd_amount_usd', 'sum'),
        net_rev=('net_revenue_usd', 'sum'),
        cpa=('cpa_cost_usd', 'sum'),
        bonus=('bonus_cost_usd', 'sum'),
        attempts=('payment_attempts', 'sum'),
        approved=('payment_approved', 'sum'),
    ).reset_index()
    
    wk['reg2dep'] = wk['ftd'] / wk['regs'].replace(0, np.nan)
    wk['approval_rate'] = wk['approved'] / wk['attempts'].replace(0, np.nan)
    wk['ecpa'] = wk['cpa'] / wk['ftd'].replace(0, np.nan)
    wk['roi'] = ((wk['net_rev'] - wk['cpa'] - wk['bonus']) / (wk['cpa'] + wk['bonus']).replace(0, np.nan))
    wk['period'] = wk['year'].astype(str) + '-W' + wk['week'].astype(str).str.zfill(2)
    wk = wk.sort_values(['year', 'week'], ascending=False)
    
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        fig_wv = make_subplots(specs=[[{"secondary_y": True}]])
        fig_wv.add_trace(go.Bar(x=wk['period'][::-1], y=wk['regs'][::-1], name='Registrations',
                                marker_color=COLORS['blue'], opacity=0.5), secondary_y=False)
        fig_wv.add_trace(go.Scatter(x=wk['period'][::-1], y=wk['ftd'][::-1], name='FTD',
                                    line=dict(color=COLORS['green'], width=2.5)), secondary_y=True)
        apply_layout(fig_wv, MODE, title='Weekly Volume')
        fig_wv.update_yaxes(title_text="Registrations", secondary_y=False)
        fig_wv.update_yaxes(title_text="FTD", secondary_y=True)
        st.plotly_chart(fig_wv, use_container_width=True, config={'displayModeBar': False})
    
    with col_w2:
        fig_wr = go.Figure()
        fig_wr.add_trace(go.Bar(x=wk['period'][::-1], y=wk['net_rev'][::-1], name='Net Revenue',
                                marker_color=COLORS['green']))
        apply_layout(fig_wr, MODE, title='Weekly Revenue')
        st.plotly_chart(fig_wr, use_container_width=True, config={'displayModeBar': False})
    
    # ════════════════════════════════════════════════════════════
    # WEEKLY SUMMARY TABLE
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">📊 Weekly Summary</div>', unsafe_allow_html=True)
    
    wk_display = wk[['period', 'regs', 'ftd', 'reg2dep', 'ftd_amt', 'approval_rate', 'net_rev', 'ecpa', 'roi']].copy()
    wk_display.columns = ['Week', 'Regs', 'FTD', 'Reg2Dep', 'FTD Amt $', 'Approval %', 'Net Rev $', 'eCPA $', 'ROI']
    
    st.dataframe(
        wk_display.style.format({
            'Regs': '{:,.0f}', 'FTD': '{:,.0f}', 'Reg2Dep': '{:.1%}',
            'FTD Amt $': '${:,.0f}', 'Approval %': '{:.1%}',
            'Net Rev $': '${:,.0f}', 'eCPA $': '${:.0f}', 'ROI': '{:.1%}'
        }).background_gradient(subset=['Reg2Dep'], cmap='RdYlGn', vmin=0, vmax=0.25)
         .background_gradient(subset=['Approval %'], cmap='RdYlGn', vmin=0.5, vmax=0.95)
         .background_gradient(subset=['ROI'], cmap='RdYlGn', vmin=-0.5, vmax=0.5),
        use_container_width=True, hide_index=True, height=500,
    )

# ═══════════════════════════════════════════════════
# TAB 4: PAYMENT & CONVERSION HEALTH
# ═══════════════════════════════════════════════════
with tab_payments:
    st.markdown('<div class="sec-label">Payment & Conversion Health</div>', unsafe_allow_html=True)
    
    # ════════════════════════════════════════════════════════════
    # CURRENT HOUR APPROVAL RATE ALERT
    # ════════════════════════════════════════════════════════════
    try:
        # Get current hour data (using latest hour in dataset as "current")
        pm = df_payments[
            (df_payments['date'].dt.date >= start_date) &
            (df_payments['date'].dt.date <= end_date) &
            (df_payments['geo'].isin(selected_geos))
        ].copy()
        
        if not pm.empty:
            # Get latest hour
            latest_date = pm['date'].max()
            current_hour_data = pm[pm['date'] == latest_date]
            
            if not current_hour_data.empty:
                hour_attempts = current_hour_data['txn_count'].sum()
                hour_approved = current_hour_data['approved_count'].sum()
                hour_ar = safe_div(hour_approved, hour_attempts)
                
                # Determine status
                if hour_ar >= 0.85:
                    status = "🟢 HEALTHY"
                    alert_color = COLORS['green']
                    bg_color = '#0E2D20' if MODE == 'dark' else '#F0FDF4'
                elif hour_ar >= 0.75:
                    status = "🟡 WARNING"
                    alert_color = COLORS['amber']
                    bg_color = '#2D1F0E' if MODE == 'dark' else '#FFFBEB'
                else:
                    status = "🔴 CRITICAL"
                    alert_color = COLORS['red']
                    bg_color = '#2D0E0E' if MODE == 'dark' else '#FEF2F2'
                
                st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border: 2px solid {alert_color};
                    border-radius: 12px;
                    padding: 20px 24px;
                    margin-bottom: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 11px; color: #8B90AD; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                        Current Hour Approval Rate
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 48px; font-weight: 700; color: {alert_color}; margin-bottom: 8px;">
                        {hour_ar*100:.1f}%
                    </div>
                    <div style="font-size: 18px; font-weight: 600; color: {alert_color}; margin-bottom: 12px;">
                        {status}
                    </div>
                    <div style="font-size: 13px; color: #8B90AD;">
                        {int(hour_attempts)} attempts · {latest_date.strftime('%Y-%m-%d %H:00')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.info("Current hour data unavailable")
    
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
    
    # ════════════════════════════════════════════════════════════
    # APPROVAL RATE TRENDS
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">📈 Approval Rate Analysis</div>', unsafe_allow_html=True)
    
    ar_col1, ar_col2 = st.columns(2)
    
    with ar_col1:
        # Daily Approval Rate Trend
        trend = df.groupby('date').agg(
            attempts=('payment_attempts', 'sum'),
            approved=('payment_approved', 'sum'),
        ).reset_index()
        trend['approval_rate'] = trend['approved'] / trend['attempts'].replace(0, np.nan)
        trend['ma7'] = trend['approval_rate'].rolling(7, min_periods=1).mean()
        
        fig_ap = go.Figure()
        fig_ap.add_trace(go.Scatter(x=trend['date'], y=trend['approval_rate'],
                                    name='Daily AR', line=dict(color=COLORS['green'], width=1), opacity=0.4))
        fig_ap.add_trace(go.Scatter(x=trend['date'], y=trend['ma7'],
                                    name='7-day MA', line=dict(color=COLORS['green'], width=2.5)))
        fig_ap.add_hline(y=0.85, line_dash="dot", line_color=COLORS['amber'], 
                         annotation_text="Target 85%")
        apply_layout(fig_ap, MODE, title='Daily Approval Rate', yaxis_tickformat='.0%')
        st.plotly_chart(fig_ap, use_container_width=True, config={'displayModeBar': False})
    
    with ar_col2:
        # AR by Payment Method
        if not pm.empty:
            pm_method = pm.groupby('payment_method').agg(
                Attempts=('txn_count', 'sum'),
                Approved=('approved_count', 'sum'),
            ).reset_index()
            pm_method['AR'] = pm_method['Approved'] / pm_method['Attempts'].replace(0, np.nan)
            pm_method = pm_method.sort_values('AR', ascending=True)
            
            # Color by performance
            colors = pm_method['AR'].apply(lambda x: COLORS['green'] if x >= 0.85 
                                           else COLORS['amber'] if x >= 0.75 
                                           else COLORS['red']).tolist()
            
            fig_pm = go.Figure()
            fig_pm.add_trace(go.Bar(
                y=pm_method['payment_method'], x=pm_method['AR'],
                orientation='h', marker_color=colors,
                text=pm_method['AR'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else ""),
                textposition='outside',
            ))
            fig_pm.add_vline(x=0.85, line_dash="dot", line_color=COLORS['amber'],
                            annotation_text="Target")
            apply_layout(fig_pm, MODE, title='AR by Payment Method', xaxis_tickformat='.0%')
            st.plotly_chart(fig_pm, use_container_width=True, config={'displayModeBar': False})
    
    # ════════════════════════════════════════════════════════════
    # STATUS BREAKDOWN
    # ════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-label">📊 Payment Status Breakdown (Daily)</div>', unsafe_allow_html=True)
    
    if not pm.empty:
        # Daily status breakdown - check which columns exist
        available_cols = pm.columns.tolist()
        
        agg_dict = {
            'Approved': ('approved_count', 'sum'),
            'Declined': ('declined_count', 'sum'),
        }
        
        # Add pending if it exists
        if 'pending_count' in available_cols:
            agg_dict['Pending'] = ('pending_count', 'sum')
        
        status_daily = pm.groupby('date').agg(**agg_dict).reset_index()
        
        # Create figure
        fig_status = go.Figure()
        fig_status.add_trace(go.Bar(x=status_daily['date'], y=status_daily['Approved'],
                                   name='Approved', marker_color=COLORS['green']))
        fig_status.add_trace(go.Bar(x=status_daily['date'], y=status_daily['Declined'],
                                   name='Declined', marker_color=COLORS['red']))
        
        if 'Pending' in status_daily.columns:
            fig_status.add_trace(go.Bar(x=status_daily['date'], y=status_daily['Pending'],
                                       name='Pending', marker_color=COLORS['amber']))
        
        apply_layout(fig_status, MODE, title='Payment Status Breakdown', barmode='stack')
        st.plotly_chart(fig_status, use_container_width=True, config={'displayModeBar': False})
        
        # Status summary
        total_approved = int(status_daily['Approved'].sum())
        total_declined = int(status_daily['Declined'].sum())
        total_pending = int(status_daily['Pending'].sum()) if 'Pending' in status_daily.columns else 0
        total = total_approved + total_declined + total_pending
        
        status_cols = st.columns(3)
        with status_cols[0]:
            st.metric("✅ Approved", f"{fmt_num(total_approved)}", 
                     f"{(total_approved/total*100):.1f}%" if total > 0 else "0%")
        with status_cols[1]:
            st.metric("❌ Declined", f"{fmt_num(total_declined)}", 
                     f"{(total_declined/total*100):.1f}%" if total > 0 else "0%")
        with status_cols[2]:
            if total_pending > 0:
                st.metric("⏳ Pending", f"{fmt_num(total_pending)}", 
                         f"{(total_pending/total*100):.1f}%" if total > 0 else "0%")
            else:
                st.metric("⏳ Pending", "0", "0%")

# ═══════════════════════════════════════════════════
# TAB 5: TRAFFIC & AGENT EFFICIENCY
# ═══════════════════════════════════════════════════
with tab_agents:
    st.markdown('<div class="sec-label">Traffic & Agent Efficiency</div>', unsafe_allow_html=True)
    
    a = df.copy()
    if a.empty:
        st.info("Немає даних за вибраними фільтрами.")
    else:
        # ════════════════════════════════════════════════════════════
        # TOP PERFORMERS & KEY METRICS
        # ════════════════════════════════════════════════════════════
        agg = a.groupby('agent', as_index=False).agg(
            Clicks=('clicks','sum'),
            Regs=('registrations','sum'),
            FTD=('ftd_count','sum'),
            FTD_Amt=('ftd_amount_usd','sum'),
            Net_Rev=('net_revenue_usd','sum'),
            CPA=('cpa_cost_usd','sum'),
            Attempts=('payment_attempts','sum'),
            Approved=('payment_approved','sum'),
        )
        
        agg['Reg2FTD %'] = agg['FTD'] / agg['Regs'].replace(0, np.nan)
        agg['Click2Reg %'] = agg['Regs'] / agg['Clicks'].replace(0, np.nan)
        agg['Approval %'] = agg['Approved'] / agg['Attempts'].replace(0, np.nan)
        agg['ROI'] = ((agg['Net_Rev'] - agg['CPA']) / agg['CPA'].replace(0, np.nan))
        agg['eCPA'] = agg['CPA'] / agg['FTD'].replace(0, np.nan)
        agg = agg.sort_values('FTD_Amt', ascending=False)
        
        # Top 3 Performers
        st.markdown("### 🏆 Top Performers")
        top3_cols = st.columns(3)
        for idx, (i, row) in enumerate(agg.head(3).iterrows()):
            with top3_cols[idx]:
                medal = ["🥇", "🥈", "🥉"][idx]
                st.markdown(f"""
                <div style="
                    background: {'#131730' if MODE == 'dark' else '#FFFFFF'};
                    border: 2px solid {COLORS['green']};
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 16px;
                ">
                    <div style="font-size: 40px; margin-bottom: 12px;">{medal}</div>
                    <div style="font-size: 18px; font-weight: 700; margin-bottom: 8px; color: {'#E4E6F0' if MODE == 'dark' else '#111827'};">{row['agent']}</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: {COLORS['green']}; font-weight: 700; margin-bottom: 8px;">
                        {fmt_money(row['FTD_Amt'])}
                    </div>
                    <div style="font-size: 13px; color: {'#8B90AD' if MODE == 'dark' else '#6B7280'}; margin-top: 8px;">
                        {int(row['FTD'])} FTD · {row['Reg2FTD %']:.1%} CR
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # ════════════════════════════════════════════════════════════
        # AGENT PERFORMANCE CHARTS
        # ════════════════════════════════════════════════════════════
        st.markdown('<div class="sec-label">📊 Agent Performance Analysis</div>', unsafe_allow_html=True)
        
        # Top 10 by Revenue - full width
        top10_rev = agg.head(10).sort_values('Net_Rev', ascending=True)
        
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            y=top10_rev['agent'], x=top10_rev['Net_Rev'],
            orientation='h', marker_color=COLORS['green'],
            text=top10_rev['Net_Rev'].apply(lambda x: fmt_money(x)),
            textposition='outside',
        ))
        apply_layout(fig_rev, MODE, title='Top 10 Agents by Revenue')
        st.plotly_chart(fig_rev, use_container_width=True, config={'displayModeBar': False})
        
        # ════════════════════════════════════════════════════════════
        # TRAFFIC SOURCE BREAKDOWN BY AGENT
        # ════════════════════════════════════════════════════════════
        st.markdown('<div class="sec-label">📡 Traffic Mix by Top Agents</div>', unsafe_allow_html=True)
        
        # Get top 5 agents
        top5_agents = agg.head(5)['agent'].tolist()
        agent_source = a[a['agent'].isin(top5_agents)].groupby(['agent', 'traffic_source']).agg(
            Regs=('registrations', 'sum')
        ).reset_index()
        
        fig_mix = px.bar(
            agent_source, x='agent', y='Regs', color='traffic_source',
            color_discrete_sequence=COLOR_SEQ,
            barmode='stack'
        )
        apply_layout(fig_mix, MODE, title='Traffic Source Mix (Top 5 Agents)')
        st.plotly_chart(fig_mix, use_container_width=True, config={'displayModeBar': False})
        
        # ════════════════════════════════════════════════════════════
        # FULL AGENT TABLE
        # ════════════════════════════════════════════════════════════
        st.markdown('<div class="sec-label">📋 Complete Agent Leaderboard</div>', unsafe_allow_html=True)
        
        st.dataframe(
            agg.style.format({
                'Clicks':'{:,.0f}','Regs':'{:,.0f}','FTD':'{:,.0f}',
                'Click2Reg %':'{:.1%}','Reg2FTD %':'{:.1%}','Approval %':'{:.1%}',
                'FTD_Amt':'${:,.0f}','Net_Rev':'${:,.0f}','eCPA':'${:,.0f}','ROI':'{:.1%}'
            }).background_gradient(subset=['Reg2FTD %'], cmap='RdYlGn', vmin=0, vmax=0.20)
             .background_gradient(subset=['ROI'], cmap='RdYlGn', vmin=-0.5, vmax=0.5)
             .background_gradient(subset=['Approval %'], cmap='RdYlGn', vmin=0.6, vmax=0.95),
            use_container_width=True, hide_index=True, height=500
        )
        
        # ════════════════════════════════════════════════════════════
        # AGENT TRENDS (Optional Deep Dive)
        # ════════════════════════════════════════════════════════════
        st.markdown('<div class="sec-label">🔍 Agent Deep Dive (Optional)</div>', unsafe_allow_html=True)
        
        selected_agent = st.selectbox("Select agent for detailed analysis:", 
                                      [''] + sorted(a['agent'].dropna().unique().tolist()))
        
        if selected_agent:
            agent_data = a[a['agent'] == selected_agent].groupby('date').agg(
                Regs=('registrations', 'sum'),
                FTD=('ftd_count', 'sum'),
                Revenue=('net_revenue_usd', 'sum'),
            ).reset_index()
            agent_data['Reg2FTD'] = agent_data['FTD'] / agent_data['Regs'].replace(0, np.nan)
            
            deep_col1, deep_col2 = st.columns(2)
            
            with deep_col1:
                fig_agent_vol = go.Figure()
                fig_agent_vol.add_trace(go.Bar(x=agent_data['date'], y=agent_data['Regs'],
                                              name='Regs', marker_color=COLORS['blue']))
                fig_agent_vol.add_trace(go.Scatter(x=agent_data['date'], y=agent_data['FTD'],
                                                   name='FTD', line=dict(color=COLORS['green'], width=2),
                                                   yaxis='y2'))
                apply_layout(fig_agent_vol, MODE, title=f'{selected_agent} - Volume Trend')
                fig_agent_vol.update_layout(yaxis2=dict(overlaying='y', side='right'))
                st.plotly_chart(fig_agent_vol, use_container_width=True, config={'displayModeBar': False})
            
            with deep_col2:
                fig_agent_cr = go.Figure()
                fig_agent_cr.add_trace(go.Scatter(x=agent_data['date'], y=agent_data['Reg2FTD'],
                                                  line=dict(color=COLORS['purple'], width=2),
                                                  fill='tozeroy'))
                apply_layout(fig_agent_cr, MODE, title=f'{selected_agent} - Conversion Rate',
                            yaxis_tickformat='.0%')
                st.plotly_chart(fig_agent_cr, use_container_width=True, config={'displayModeBar': False})
