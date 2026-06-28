"""Page 5: Alerts Center — over-budget / near-budget alert cards."""

import streamlit as st
from utils import business_logic as bl
from utils import data_manager as dm 
from utils import styling

st.set_page_config(page_title="Alerts Center", page_icon="🚨", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("🚨 Alerts Center")
st.caption("Stay on top of budget breaches and near-limit warnings")

expense_df = st.session_state.expense_df
budget_limits = st.session_state.budget_limits
budget_monitor = bl.calculate_budget_monitoring(expense_df, budget_limits)
alerts = bl.generate_budget_alerts(budget_monitor)

over_count = sum(1 for a in alerts if a['level'] == 'Over Budget')
near_count = sum(1 for a in alerts if a['level'] == 'Near Budget')
ok_count = sum(1 for a in alerts if a['level'] == 'Within Budget')

c1, c2, c3 = st.columns(3)
with c1:
    styling.kpi_card("Over Budget Alerts", str(over_count), color="#dc2626")
with c2:
    styling.kpi_card("Near Budget Alerts", str(near_count), color="#f59e0b")
with c3:
    styling.kpi_card("Within Budget", str(ok_count), color="#16a34a")

st.markdown('<div class="section-title">Alert Details</div>', unsafe_allow_html=True)

for alert in alerts:
    css_class = {
        'Over Budget': 'alert-card-over',
        'Near Budget': 'alert-card-near',
        'Within Budget': 'alert-card-ok',
    }[alert['level']]

    st.markdown(
        f"""
        <div class="{css_class}">
            <b>{alert['icon']} {alert['level']}</b> — {alert['message']}
        </div>
        """,
        unsafe_allow_html=True,
    )

if over_count == 0 and near_count == 0:
    st.success("✅ All categories are comfortably within budget. No alerts.")
