

import streamlit as st
import pandas as pd
from utils import business_logic as bl


def init_session_state():
    """Initialise all shared data the first time the app runs."""
    if 'expense_df' not in st.session_state:
        expense_df = bl.generate_mock_expense_data()
        expense_df = bl.add_manual_transactions(expense_df)
        expense_df = expense_df.sort_values('date').reset_index(drop=True)
        st.session_state.expense_df = expense_df

    if 'income_df' not in st.session_state:
        st.session_state.income_df = bl.generate_mock_income_data()

    if 'budget_limits' not in st.session_state:
        st.session_state.budget_limits = dict(bl.DEFAULT_BUDGET_LIMITS)

    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False


def add_transaction(date, category, amount, txn_type):
    """Append a new manual transaction to the right dataframe (Income/Expense)."""
    if txn_type == 'Expense':
        new_row = pd.DataFrame([{
            'date': pd.to_datetime(date),
            'category': category,
            'amount': amount,
        }])
        df = pd.concat([st.session_state.expense_df, new_row], ignore_index=True)
        df['days'] = (df['date'] - df['date'].min()).dt.days
        st.session_state.expense_df = df.sort_values('date').reset_index(drop=True)
    else:  # Income
        new_row = pd.DataFrame([{
            'date': pd.to_datetime(date),
            'source': category,
            'amount': amount,
        }])
        df = pd.concat([st.session_state.income_df, new_row], ignore_index=True)
        st.session_state.income_df = df.sort_values('date').reset_index(drop=True)


def get_recent_transactions(n: int = 15):
    """Combine income + expense into one table of recent transactions."""
    exp = st.session_state.expense_df[['date', 'category', 'amount']].copy()
    exp['type'] = 'Expense'

    inc = st.session_state.income_df[['date', 'source', 'amount']].copy()
    inc = inc.rename(columns={'source': 'category'})
    inc['type'] = 'Income'

    combined = pd.concat([exp, inc], ignore_index=True)
    combined = combined.sort_values('date', ascending=False).reset_index(drop=True)
    return combined.head(n)
