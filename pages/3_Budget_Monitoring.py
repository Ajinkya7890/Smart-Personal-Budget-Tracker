"""Page 4: Budget Monitoring — table + budget vs actual chart."""

import streamlit as st
import plotly.graph_objects as go
from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

st.set_page_config(page_title="Budget Monitoring", page_icon="📋", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("📋 Budget Monitoring")
st.caption("Track actual spending against budget limits by category")

expense_df = st.session_state.expense_df
budget_limits = st.session_state.budget_limits
budget_monitor = bl.calculate_budget_monitoring(expense_df, budget_limits)

st.markdown('<div class="section-title">Budget Monitoring Table</div>', unsafe_allow_html=True)


def style_status(val):
    if "Over Budget" in val:
        return "background-color:#fee2e2;color:#b91c1c;font-weight:600;"
    return "background-color:#dcfce7;color:#15803d;font-weight:600;"


display_df = budget_monitor[['Category', 'Spent', 'Budget Limit', 'Remaining', 'Status']].copy()
styled = display_df.style.applymap(style_status, subset=['Status']).format({
    'Spent': '₹{:,.0f}', 'Budget Limit': '₹{:,.0f}', 'Remaining': '₹{:,.0f}'
})
st.dataframe(styled, use_container_width=True, hide_index=True)

st.markdown('<div class="section-title">Budget vs Actual Spending</div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Bar(name='Actual Spending', x=budget_monitor['Category'], y=budget_monitor['Spent'],
                      marker_color='#2563eb'))
fig.add_trace(go.Bar(name='Budget Limit', x=budget_monitor['Category'], y=budget_monitor['Budget Limit'],
                      marker_color='#16a34a'))
fig.update_layout(
    barmode='group', height=450,
    yaxis_title="Amount (₹)",
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", y=1.1),
)
st.plotly_chart(fig, use_container_width=True)
