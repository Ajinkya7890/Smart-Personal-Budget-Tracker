"""Page 7: Spending Forecast — Linear Regression forecast from the notebook."""

import streamlit as st
import plotly.graph_objects as go
from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

st.set_page_config(page_title="Spending Forecast", page_icon="🔮", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("🔮 Spending Forecast")
st.caption("Linear Regression based future spending prediction (same model as the notebook)")

expense_df = st.session_state.expense_df
forecast = bl.forecast_spending(expense_df, days_ahead=30)

c1, c2, c3 = st.columns(3)
with c1:
    styling.kpi_card("Predicted Next 30 Days", f"₹{forecast['total_predicted_spending']:,.0f}", color="#7c3aed")
with c2:
    styling.kpi_card("Daily Trend (Slope)", f"₹{forecast['slope']:,.2f}/day", color="#2563eb")
with c3:
    styling.kpi_card("Baseline Intercept", f"₹{forecast['intercept']:,.2f}", color="#0891b2")

st.markdown('<div class="section-title">Historical vs Predicted Spending</div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=expense_df['date'], y=expense_df['amount'],
    mode='lines+markers', name='Actual Spending',
    line=dict(color='#2563eb'), marker=dict(size=4), opacity=0.7,
))
fig.add_trace(go.Scatter(
    x=forecast['future_df']['date'], y=forecast['future_df']['amount'],
    mode='lines', name='Predicted Spending',
    line=dict(color='#dc2626', dash='dash'),
))
fig.update_layout(
    height=480, xaxis_title="Date", yaxis_title="Amount (₹)",
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", y=1.08),
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-title">Forecast Insights</div>', unsafe_allow_html=True)

trend_word = "increasing 📈" if forecast['slope'] > 0 else "decreasing 📉"
insights = [
    f"Your spending trend is **{trend_word}** at roughly ₹{abs(forecast['slope']):,.2f} per day.",
    f"Based on this trend, total predicted spending for the next 30 days is **₹{forecast['total_predicted_spending']:,.0f}**.",
    "Forecast is generated using a Linear Regression model fit on historical days vs. amount, exactly as in the original notebook.",
]
for i in insights:
    st.markdown(f'<span class="insight-pill">💡 {i}</span>', unsafe_allow_html=True)

with st.expander("📄 View Predicted Daily Values"):
    st.dataframe(
        forecast['future_df'][['date', 'amount']].rename(columns={'date': 'Date', 'amount': 'Predicted Amount'}),
        use_container_width=True, hide_index=True,
    )
