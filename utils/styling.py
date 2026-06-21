

import streamlit as st

LIGHT_CSS = """
<style>
:root {
    --accent-blue: #2563eb;
    --accent-green: #16a34a;
    --bg-main: #ffffff;
    --bg-card: #f8fafc;
    --text-main: #0f172a;
    --border-color: #e2e8f0;
}

.stApp { background-color: var(--bg-main); color: var(--text-main); }

div[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 0.6rem;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent-blue);
    margin-top: 1.2rem;
    margin-bottom: 0.4rem;
    border-left: 4px solid var(--accent-green);
    padding-left: 0.6rem;
}

.alert-card-over {
    background: #fef2f2;
    border-left: 5px solid #ef4444;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.alert-card-near {
    background: #fffbeb;
    border-left: 5px solid #f59e0b;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.alert-card-ok {
    background: #f0fdf4;
    border-left: 5px solid #22c55e;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}

.insight-pill {
    display: inline-block;
    background: #eff6ff;
    color: var(--accent-blue);
    border-radius: 999px;
    padding: 0.4rem 0.9rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 0.85rem;
    font-weight: 600;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
section[data-testid="stSidebar"] * { color: #f1f5f9 !important; }
</style>
"""

DARK_CSS = """
<style>
:root {
    --accent-blue: #60a5fa;
    --accent-green: #4ade80;
    --bg-main: #0f172a;
    --bg-card: #1e293b;
    --text-main: #f1f5f9;
    --border-color: #334155;
}

.stApp { background-color: var(--bg-main); color: var(--text-main); }

div[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 1rem 1.2rem;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.6rem;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent-blue);
    margin-top: 1.2rem;
    margin-bottom: 0.4rem;
    border-left: 4px solid var(--accent-green);
    padding-left: 0.6rem;
}

.alert-card-over {
    background: #3f1d1d;
    border-left: 5px solid #ef4444;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.alert-card-near {
    background: #3f351a;
    border-left: 5px solid #f59e0b;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.alert-card-ok {
    background: #1a3322;
    border-left: 5px solid #22c55e;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}

.insight-pill {
    display: inline-block;
    background: #1e3a5f;
    color: var(--accent-blue);
    border-radius: 999px;
    padding: 0.4rem 0.9rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 0.85rem;
    font-weight: 600;
}
</style>
"""


def inject_css():
    if st.session_state.get('dark_mode'):
        st.markdown(DARK_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_CSS, unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", color: str = "#2563eb"):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div style="font-size:0.85rem;color:#64748b;font-weight:600;">{label}</div>
            <div style="font-size:1.6rem;font-weight:800;color:{color};">{value}</div>
            <div style="font-size:0.78rem;color:#94a3b8;">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
