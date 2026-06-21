# Smart Personal Budget Tracker & Expense Forecasting Dashboard

A production-quality multi-page Streamlit web application converted from the
original Jupyter Notebook (`PersonalBudgetTracker.ipynb`). All business logic
(income/expense/savings calculations, budget monitoring, alerts, health
score, and the Linear Regression spending forecast) is preserved exactly as
implemented in the notebook — only the presentation layer changed.

## Project Structure

```
budget_app/
├── app.py                       # Entry point — Dashboard (Page 1) + sidebar
├── requirements.txt
├── pages/
│   ├── 1_Add_Transaction.py     # Page 2
│   ├── 2_Budget_Management.py   # Page 3
│   ├── 3_Budget_Monitoring.py   # Page 4
│   ├── 4_Alerts_Center.py       # Page 5
│   ├── 5_Expense_Analytics.py   # Page 6
│   ├── 6_Spending_Forecast.py   # Page 7
│   └── 7_Financial_Health.py    # Page 8
└── utils/
    ├── business_logic.py        # All notebook calculations (pure functions)
    ├── data_manager.py          # Streamlit session-state management
    └── styling.py                # Shared CSS / FinTech theme / dark mode
```

## How to Run Locally

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the app:
   ```bash
   streamlit run app.py
   ```

4. Open the URL Streamlit prints (default `http://localhost:8501`).

## Notebook → App Mapping

| Notebook Logic | App Location |
|---|---|
| Manual transaction entry | `Add Transaction` page |
| Income / Expense / Savings / Savings Rate | `business_logic.calculate_financial_summary` → Dashboard |
| Budget limits per category | `Budget Management` page |
| Budget monitoring (Spent/Remaining/Status) | `business_logic.calculate_budget_monitoring` → `Budget Monitoring` page |
| Budget alert system | `business_logic.generate_budget_alerts` → `Alerts Center` page |
| Budget Health Score | `business_logic.calculate_budget_health_score` → Dashboard & `Financial Health` page |
| Linear Regression spending forecast | `business_logic.forecast_spending` → `Spending Forecast` page |
| Pie / histogram / monthly trend / heatmap / top-10 days | `Expense Analytics` page |

## Notes

- All chart logic (Matplotlib/Seaborn in the notebook) was re-implemented
  with interactive **Plotly** charts for a modern dashboard feel, while
  keeping the **exact same underlying calculations**.
- CSV upload/download, search, date & category filters, and dark mode are
  additional features layered on top of the original notebook functionality.
- Data lives in `st.session_state` for the duration of a session — there is
  no external database; uploading a CSV on the sidebar replaces the working
  expense dataset.
