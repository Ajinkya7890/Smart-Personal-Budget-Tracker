
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

CATEGORIES = ['Food', 'Rent', 'Utilities', 'Entertainment', 'Transport', 'Health']

DEFAULT_BUDGET_LIMITS = {
    'Food': 40000,
    'Rent': 70000,
    'Utilities': 25000,
    'Entertainment': 20000,
    'Transport': 15000,
    'Health': 10000,
}


# ---------------------------------------------------------------------------
# Data generation (mirrors notebook cells 22-25: seed(42), 365 days mock data)
# ---------------------------------------------------------------------------
def generate_mock_expense_data():
    """Exact reproduction of the notebook's mock expense dataset."""
    np.random.seed(42)
    data = {
        'date': pd.date_range(start='2023-01-01', periods=365, freq='D'),
        'category': np.random.choice(CATEGORIES, 365),
        'amount': np.random.randint(50, 1000, 365),
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days
    return df


def generate_mock_income_data():
    """Exact reproduction of the notebook's income dataset."""
    income_data = {
        'date': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
        'source': ['Salary'] * 12,
        'amount': [50000, 50000, 52000, 52000, 55000, 55000,
                   55000, 58000, 58000, 60000, 60000, 60000],
    }
    return pd.DataFrame(income_data)


def add_manual_transactions(df):
    """Notebook's manual transaction entry module merged into main df."""
    manual_transactions = [
        ['2024-01-05', 'Food', 1200],
        ['2024-01-08', 'Transport', 500],
        ['2024-01-12', 'Entertainment', 2000],
        ['2024-01-15', 'Health', 1500],
    ]
    manual_df = pd.DataFrame(manual_transactions, columns=['date', 'category', 'amount'])
    manual_df['date'] = pd.to_datetime(manual_df['date'])
    df = pd.concat([df, manual_df], ignore_index=True)
    df['days'] = (df['date'] - df['date'].min()).dt.days
    return df


# ---------------------------------------------------------------------------
# Financial summary (notebook Step 1B)
# ---------------------------------------------------------------------------
def calculate_financial_summary(income_df, expense_df):
    total_income = income_df['amount'].sum()
    total_expense = expense_df['amount'].sum()
    savings = total_income - total_expense
    savings_rate = (savings / total_income) * 100 if total_income else 0
    return {
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'savings': float(savings),
        'savings_rate': float(savings_rate),
    }


# ---------------------------------------------------------------------------
# Budget monitoring (notebook Step 2B)
# ---------------------------------------------------------------------------
def calculate_budget_monitoring(expense_df, budget_limits: dict):
    category_spending = expense_df.groupby('category')['amount'].sum().reset_index()
    category_spending.columns = ['Category', 'Spent']

    budget_df = pd.DataFrame(list(budget_limits.items()), columns=['Category', 'Budget Limit'])

    budget_monitor = pd.merge(budget_df, category_spending, on='Category', how='left')
    budget_monitor['Spent'] = budget_monitor['Spent'].fillna(0)

    budget_monitor['Remaining'] = budget_monitor['Budget Limit'] - budget_monitor['Spent']
    budget_monitor['Status'] = budget_monitor['Remaining'].apply(
        lambda x: 'Over Budget ⚠️' if x < 0 else 'Within Budget ✅'
    )
    budget_monitor['Utilization %'] = (
        budget_monitor['Spent'] / budget_monitor['Budget Limit'] * 100
    ).round(1)
    return budget_monitor


# ---------------------------------------------------------------------------
# Budget alerts (notebook Step 3)
# ---------------------------------------------------------------------------
def generate_budget_alerts(budget_monitor: pd.DataFrame):
    alerts = []
    for _, row in budget_monitor.iterrows():
        if row['Remaining'] < 0:
            alerts.append({
                'category': row['Category'],
                'level': 'Over Budget',
                'message': f"{row['Category']} exceeded budget by ₹{abs(row['Remaining']):,.0f}",
                'icon': '⚠️',
            })
        elif row['Remaining'] <= row['Budget Limit'] * 0.10:
            alerts.append({
                'category': row['Category'],
                'level': 'Near Budget',
                'message': f"{row['Category']} has less than 10% budget remaining",
                'icon': '⚠️',
            })
        else:
            alerts.append({
                'category': row['Category'],
                'level': 'Within Budget',
                'message': f"{row['Category']} is within budget",
                'icon': '✅',
            })
    return alerts


# ---------------------------------------------------------------------------
# Budget Health Score (notebook Step 5)
# ---------------------------------------------------------------------------
def calculate_budget_health_score(budget_monitor: pd.DataFrame):
    total_categories = len(budget_monitor)
    within_budget = len(budget_monitor[budget_monitor['Status'].str.contains('Within Budget')])
    health_score = (within_budget / total_categories) * 100 if total_categories else 0

    if health_score >= 80:
        label, color = 'Excellent', '#22c55e'
    elif health_score >= 60:
        label, color = 'Good', '#eab308'
    elif health_score >= 40:
        label, color = 'Fair', '#f97316'
    else:
        label, color = 'Poor', '#ef4444'

    return {'score': round(health_score), 'label': label, 'color': color}


# ---------------------------------------------------------------------------
# Linear Regression Spending Forecast (notebook Step 2 / cells 26-29)
# ---------------------------------------------------------------------------
def forecast_spending(expense_df: pd.DataFrame, days_ahead: int = 30):
    """Fits Linear Regression on (days -> amount) exactly like the notebook
    and predicts the next `days_ahead` days of spending."""
    X = expense_df[['days']]
    y = expense_df['amount']

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(
        expense_df['days'].max() + 1, expense_df['days'].max() + 1 + days_ahead
    ).reshape(-1, 1)
    future_predictions = model.predict(future_days)

    future_dates = [
        expense_df['date'].max() + pd.Timedelta(days=int(x)) for x in future_days.flatten()
    ]

    future_df = pd.DataFrame({
        'date': future_dates,
        'amount': future_predictions,
        'category': 'Predicted',
    })

    total_predicted_spending = float(np.sum(future_predictions))

    return {
        'model': model,
        'future_df': future_df,
        'total_predicted_spending': total_predicted_spending,
        'slope': float(model.coef_[0]),
        'intercept': float(model.intercept_),
    }


# ---------------------------------------------------------------------------
# Analytics helpers (notebook visualizations 1-6)
# ---------------------------------------------------------------------------
def category_wise_spending(expense_df: pd.DataFrame):
    return expense_df.groupby('category')['amount'].sum().reset_index().rename(
        columns={'amount': 'Total Spent', 'category': 'Category'}
    )


def monthly_spending_trend(expense_df: pd.DataFrame):
    df = expense_df.copy()
    df['month'] = df['date'].dt.to_period('M').astype(str)
    return df.groupby('month')['amount'].sum().reset_index()


def spending_heatmap_data(expense_df: pd.DataFrame):
    df = expense_df.copy()
    df['day_of_week'] = df['date'].dt.day_name()
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = df.pivot_table(index='day_of_week', columns='category', values='amount', aggfunc='sum').fillna(0)
    pivot = pivot.reindex(order)
    return pivot


def top_spending_days(expense_df: pd.DataFrame, n: int = 10):
    return expense_df.nlargest(n, 'amount')[['date', 'category', 'amount']]


def financial_recommendations(summary: dict, budget_monitor: pd.DataFrame, health: dict):
    """Generate plain-language recommendations -- derived directly from the
    same numbers the notebook computes (savings rate, over-budget categories)."""
    recs = []
    if summary['savings_rate'] < 20:
        recs.append("Your savings rate is below 20%. Consider trimming discretionary spending.")
    else:
        recs.append("Great job — your savings rate is healthy. Keep maintaining this habit.")

    over_budget = budget_monitor[budget_monitor['Remaining'] < 0]
    if not over_budget.empty:
        cats = ', '.join(over_budget['Category'].tolist())
        recs.append(f"You are over budget in: {cats}. Review these categories first.")

    near_budget = budget_monitor[
        (budget_monitor['Remaining'] >= 0) &
        (budget_monitor['Remaining'] <= budget_monitor['Budget Limit'] * 0.10)
    ]
    if not near_budget.empty:
        cats = ', '.join(near_budget['Category'].tolist())
        recs.append(f"You are close to your limit in: {cats}. Slow down spending here.")

    if health['label'] in ('Fair', 'Poor'):
        recs.append("Your overall budget health needs attention — set stricter limits or increase income.")
    else:
        recs.append("Your overall budget health looks solid — keep tracking consistently.")

    return recs
