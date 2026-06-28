"""Page 6: Expense Analytics — pie, histogram, monthly trend, heatmap, top days."""

import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

st.set_page_config(page_title="Expense Analytics", page_icon="📈", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("📈 Expense Analytics")
st.caption("Deep dive into your spending patterns")

expense_df = st.session_state.expense_df.copy()

# --- Filters -----------------------------------------------------------
st.markdown('<div class="section-title">Filters</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
with f1:
    date_range = st.date_input(
        "Date Range",
        value=(expense_df['date'].min().date(), expense_df['date'].max().date()),
    )
with f2:
    cats = st.multiselect("Categories", bl.CATEGORIES, default=bl.CATEGORIES)
with f3:
    search_term = st.text_input("🔎 Search Transactions (category contains...)")

filtered = expense_df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[(filtered['date'].dt.date >= start) & (filtered['date'].dt.date <= end)]
if cats:
    filtered = filtered[filtered['category'].isin(cats)]
if search_term:
    filtered = filtered[filtered['category'].str.contains(search_term, case=False)]

if filtered.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

# --- Pie + Histogram -----------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-title">Category-wise Spending</div>', unsafe_allow_html=True)
    cat_sum = bl.category_wise_spending(filtered)
    fig_pie = px.pie(cat_sum, names='Category', values='Total Spent', hole=0.35,
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig_pie.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">Spending Distribution</div>', unsafe_allow_html=True)
    fig_hist = px.histogram(filtered, x='amount', nbins=20, color_discrete_sequence=['#7c3aed'])
    fig_hist.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_title="Amount (₹)", yaxis_title="Frequency")
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Monthly Trend ---------------------------------------------------------
st.markdown('<div class="section-title">Monthly Spending Trend</div>', unsafe_allow_html=True)
monthly = bl.monthly_spending_trend(filtered)
fig_line = px.line(monthly, x='month', y='amount', markers=True, color_discrete_sequence=['#2563eb'])
fig_line.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_title="Month", yaxis_title="Total Amount (₹)")
st.plotly_chart(fig_line, use_container_width=True)

# --- Heatmap + Top Days -----------------------------------------------------
col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="section-title">Spending Heatmap (Day x Category)</div>', unsafe_allow_html=True)
    heatmap_data = bl.spending_heatmap_data(filtered)
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index,
        colorscale='Blues', text=heatmap_data.values, texttemplate="%{text:.0f}",
    ))
    fig_heat.update_layout(height=420, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)

with col4:
    st.markdown('<div class="section-title">Top 10 Spending Days</div>', unsafe_allow_html=True)
    top_days = bl.top_spending_days(filtered, 10)
    fig_top = px.bar(top_days, x=top_days['date'].dt.strftime('%Y-%m-%d'), y='amount', color='category',
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig_top.update_layout(height=420, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           xaxis_title="Date", yaxis_title="Amount (₹)")
    st.plotly_chart(fig_top, use_container_width=True)
