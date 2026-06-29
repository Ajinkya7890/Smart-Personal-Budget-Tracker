 

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

# ---------------------------------------------------------------------------
# Page configuration 
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Budget Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

dm.init_session_state()
styling.inject_css() 

# ---------------------------------------------------------------------------
# Sidebar — branding, dark mode, CSV import/export
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 💰 Smart Budget Tracker")
    st.caption("Expense Forecasting Dashboard")
    st.divider()

    st.toggle("🌙 Dark Mode", key="dark_mode")

    st.divider()
    st.markdown("### 📁 Data Import / Export")

    uploaded = st.file_uploader("Upload Expense CSV", type=["csv"])
    if uploaded is not None:
        try:
            new_df = pd.read_csv(uploaded, parse_dates=['date'])
            required = {'date', 'category', 'amount'}
            if required.issubset(set(new_df.columns)):
                new_df = new_df[['date', 'category', 'amount']]
                new_df['days'] = (new_df['date'] - new_df['date'].min()).dt.days
                st.session_state.expense_df = new_df.sort_values('date').reset_index(drop=True)
                st.success("Expense data imported successfully.")
            else:
                st.error("CSV must contain columns: date, category, amount")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    csv_data = st.session_state.expense_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download Expense Data (CSV)",
        data=csv_data,
        file_name="expenses_export.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.divider()
    st.caption("Navigate using the **Pages** menu above ⬆️")

# ---------------------------------------------------------------------------
# Pull shared data
# ---------------------------------------------------------------------------
expense_df = st.session_state.expense_df
income_df = st.session_state.income_df
budget_limits = st.session_state.budget_limits

summary = bl.calculate_financial_summary(income_df, expense_df)
budget_monitor = bl.calculate_budget_monitoring(expense_df, budget_limits)
health = bl.calculate_budget_health_score(budget_monitor)
forecast = bl.forecast_spending(expense_df, days_ahead=30)

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("📊 Financial Dashboard")
st.caption("Overview of your income, expenses, savings and forecasted spending")

# ---------------------------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    styling.kpi_card("Total Income", f"₹{summary['total_income']:,.0f}", color="#16a34a")
with col2:
    styling.kpi_card("Total Expenses", f"₹{summary['total_expense']:,.0f}", color="#dc2626")
with col3:
    styling.kpi_card("Total Savings", f"₹{summary['savings']:,.0f}", color="#2563eb")
with col4:
    styling.kpi_card("Savings Rate", f"{summary['savings_rate']:.1f}%", color="#0891b2")
with col5:
    styling.kpi_card("Budget Health", f"{health['score']}/100", health['label'], color=health['color'])
with col6:
    styling.kpi_card("Next Month Forecast", f"₹{forecast['total_predicted_spending']:,.0f}", color="#7c3aed")

# ---------------------------------------------------------------------------
# Financial Overview Section
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Income vs Expense vs Savings</div>', unsafe_allow_html=True)

overview_df = pd.DataFrame({
    'Metric': ['Income', 'Expense', 'Savings'],
    'Amount': [summary['total_income'], summary['total_expense'], summary['savings']],
})

fig = go.Figure(go.Bar(
    x=overview_df['Metric'],
    y=overview_df['Amount'],
    marker_color=['#16a34a', '#dc2626', '#2563eb'],
    text=[f"₹{v:,.0f}" for v in overview_df['Amount']],
    textposition='outside',
))
fig.update_layout(
    height=420,
    yaxis_title="Amount (₹)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=20, b=20),
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Key Insights
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

insights = bl.financial_recommendations(summary, budget_monitor, health)
pills_html = "".join([f'<span class="insight-pill">💡 {i}</span>' for i in insights])
st.markdown(pills_html, unsafe_allow_html=True)

st.divider()
st.caption("Use the sidebar Pages menu to explore Transactions, Budgets, Alerts, Analytics, Forecasting and Financial Health.")
