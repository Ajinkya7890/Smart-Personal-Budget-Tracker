"""Page 3: Budget Management — set / update budget limits with progress bars."""

import streamlit as st
from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

st.set_page_config(page_title="Budget Management", page_icon="🎯", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("🎯 Budget Management")
st.caption("Set and update monthly budget limits for each category")

expense_df = st.session_state.expense_df
budget_limits = st.session_state.budget_limits

st.markdown('<div class="section-title">Update Budget Limits</div>', unsafe_allow_html=True)

with st.form("budget_form"):
    cols = st.columns(3)
    new_limits = {}
    for i, cat in enumerate(bl.CATEGORIES):
        with cols[i % 3]:
            new_limits[cat] = st.number_input(
                f"{cat} (₹)",
                min_value=0,
                value=int(budget_limits.get(cat, 0)),
                step=1000,
                key=f"budget_{cat}",
            )
    save = st.form_submit_button("💾 Save Budget Limits", use_container_width=True)
    if save:
        st.session_state.budget_limits = new_limits
        st.success("Budget limits updated successfully.")

budget_limits = st.session_state.budget_limits
budget_monitor = bl.calculate_budget_monitoring(expense_df, budget_limits)

st.markdown('<div class="section-title">Budget Utilization</div>', unsafe_allow_html=True)

for _, row in budget_monitor.iterrows():
    pct = min(row['Utilization %'] / 100, 1.0)
    over = row['Remaining'] < 0
    label = f"**{row['Category']}** — ₹{row['Spent']:,.0f} / ₹{row['Budget Limit']:,.0f} ({row['Utilization %']:.1f}%)"
    st.write(label)
    st.progress(pct, text="Over Budget" if over else None)
