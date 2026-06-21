"""Page 2: Add Transaction — manual income/expense entry."""

import streamlit as st
import datetime
from utils import business_logic as bl
from utils import data_manager as dm
from utils import styling

st.set_page_config(page_title="Add Transaction", page_icon="➕", layout="wide")
dm.init_session_state()
styling.inject_css()

st.title("➕ Add Transaction")
st.caption("Manually log an income or expense entry")

col_form, col_recent = st.columns([1, 1.3])

with col_form:
    st.markdown('<div class="section-title">New Transaction</div>', unsafe_allow_html=True)
    with st.form("add_txn_form", clear_on_submit=True):
        txn_type = st.radio("Transaction Type", ["Expense", "Income"], horizontal=True)
        date = st.date_input("Date", value=datetime.date.today())

        if txn_type == "Expense":
            category = st.selectbox("Category", bl.CATEGORIES)
        else:
            category = st.selectbox("Source", ["Salary", "Freelance", "Investment", "Other"])

        amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Save Transaction", use_container_width=True)

        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                dm.add_transaction(date, category, amount, txn_type)
                st.success(f"✅ {txn_type} of ₹{amount:,.0f} added under '{category}' on {date}.")

with col_recent:
    st.markdown('<div class="section-title">Recent Transactions</div>', unsafe_allow_html=True)
    recent = dm.get_recent_transactions(15)
    st.dataframe(
        recent.rename(columns={'date': 'Date', 'category': 'Category', 'amount': 'Amount', 'type': 'Type'}),
        use_container_width=True,
        hide_index=True,
    )
