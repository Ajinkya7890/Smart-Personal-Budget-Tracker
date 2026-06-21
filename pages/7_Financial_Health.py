"""Page 8: Financial Health — budget health score gauge + recommendations."""

import streamlit as st
import plotly.graph_objects as go
from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

st.set_page_config(page_title="Financial Health", page_icon="🩺", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("🩺 Financial Health")
st.caption("An overall snapshot of how healthy your budgeting habits are")

expense_df = st.session_state.expense_df
income_df = st.session_state.income_df
budget_limits = st.session_state.budget_limits

summary = bl.calculate_financial_summary(income_df, expense_df)
budget_monitor = bl.calculate_budget_monitoring(expense_df, budget_limits)
health = bl.calculate_budget_health_score(budget_monitor)

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown('<div class="section-title">Budget Health Score</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health['score'],
        number={'suffix': "/100"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': health['color']},
            'steps': [
                {'range': [0, 40], 'color': '#fee2e2'},
                {'range': [40, 60], 'color': '#ffedd5'},
                {'range': [60, 80], 'color': '#fef9c3'},
                {'range': [80, 100], 'color': '#dcfce7'},
            ],
        },
    ))
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        f"<h3 style='text-align:center;color:{health['color']};'>Status: {health['label']}</h3>",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown('<div class="section-title">Financial Recommendations</div>', unsafe_allow_html=True)
    recs = bl.financial_recommendations(summary, budget_monitor, health)
    for r in recs:
        st.markdown(
            f"""<div class="kpi-card">💡 {r}</div>""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-title">Export Dashboard Summary</div>', unsafe_allow_html=True)

import pandas as pd
summary_export = pd.DataFrame({
    'Metric': ['Total Income', 'Total Expenses', 'Total Savings', 'Savings Rate (%)',
               'Budget Health Score', 'Financial Health Status'],
    'Value': [summary['total_income'], summary['total_expense'], summary['savings'],
              round(summary['savings_rate'], 2), health['score'], health['label']],
})
st.dataframe(summary_export, use_container_width=True, hide_index=True)

csv_bytes = summary_export.to_csv(index=False).encode('utf-8')
st.download_button(
    "⬇️ Download Dashboard Summary (CSV)",
    data=csv_bytes,
    file_name="dashboard_summary.csv",
    mime="text/csv",
)
