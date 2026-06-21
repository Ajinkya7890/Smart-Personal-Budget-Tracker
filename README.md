# Smart Personal Budget Tracker & Expense Forecasting

A comprehensive personal finance management tool built with Python in Jupyter Notebook. This project demonstrates income tracking, expense categorization, budget monitoring, financial analysis, and spending forecasts using machine learning.

## 📋 Project Overview

The Smart Personal Budget Tracker provides users with:

- **Transaction Management**: Manual entry of income and expense transactions
- **Budget Planning**: Set and monitor budget limits across multiple spending categories
- **Financial Summary**: Calculate total income, expenses, savings, and savings rate
- **Budget Monitoring**: Track spending against budget limits with real-time status
- **Alert System**: Automatic alerts when budgets are exceeded or running low
- **Expense Analytics**: Visual insights into spending patterns and trends
- **Spending Forecast**: Machine learning-based predictions for future spending
- **Financial Health Scoring**: Automated health score assessment based on budget adherence

## 📁 Project Structure

```
Smart-Personal-Budget-Tracker/
├── README.md
├── Ipynb file/
│   └── PersonalBudgetTracker.ipynb    # Main Jupyter notebook
└── [Other supporting files]
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Jupyter Notebook or JupyterLab
- Required Python packages

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ajinkya7890/Smart-Personal-Budget-Tracker.git
cd Smart-Personal-Budget-Tracker
```

2. Install required dependencies:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

3. Launch Jupyter Notebook:
```bash
jupyter notebook
```

4. Open `Ipynb file/PersonalBudgetTracker.ipynb` and run the cells

## 📊 Key Features

### 1. **Transaction Management**
- Manual transaction entry with date, category, and amount
- Support for multiple spending categories:
  - Food
  - Rent
  - Utilities
  - Entertainment
  - Transport
  - Health

### 2. **Financial Summary Dashboard**
Displays key metrics:
- **Total Income**: ₹665,000
- **Total Expenses**: ₹196,140
- **Total Savings**: ₹468,860
- **Savings Rate**: 70.51%

### 3. **Budget Management**
- Pre-defined budget limits per category
- Easily customizable spending caps
- Comprehensive budget tracking table

### 4. **Budget Monitoring & Alerts**
- Real-time tracking of spent vs. budget limit
- Automatic status indicators:
  - ✅ Within Budget
  - ⚠️ Over Budget
- Alert system for:
  - Over-budget categories
  - Low budget warnings (< 10% remaining)

### 5. **Expense Analytics**
Visual representations including:
- Income vs. Expense vs. Savings bar charts
- Budget Limit vs. Actual Spending comparison
- Category-wise spending breakdown
- Trend analysis over time

### 6. **Spending Forecast**
- Linear Regression-based predictive model
- Forecasts next month's spending patterns
- Helps with future budget planning

### 7. **Financial Health Score**
Automated scoring system:
- **Score Range**: 0-100
- **Rating Levels**:
  - 🟢 Excellent (80+): Strong budget adherence
  - 🟡 Good (60-79): Healthy financial habits
  - 🟠 Fair (40-59): Needs attention
  - 🔴 Poor (<40): Requires immediate action

## 📈 Technology Stack

- **Language**: Python (96.3% Jupyter Notebook, 3.7% Python)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (Linear Regression)
- **Visualization**: Matplotlib, Seaborn

## 📖 How It Works

1. **Data Input**: Manually enter transactions with date, category, and amount
2. **Data Processing**: Aggregate transactions by category and date
3. **Financial Calculations**: Compute income, expenses, savings, and rates
4. **Budget Comparison**: Compare actual spending against budget limits
5. **Analysis & Visualization**: Generate charts and insights
6. **Forecasting**: Predict future spending using Linear Regression
7. **Health Assessment**: Calculate financial health score

## 🎯 Sample Output

### Budget Monitoring Report
| Category | Spent | Budget Limit | Remaining | Status |
|---|---|---|---|---|
| Entertainment | 4,206 | 20,000 | 15,794 | ✅ Within Budget |
| Food | 2,950 | 40,000 | 37,050 | ✅ Within Budget |
| Health | 1,500 | 10,000 | 8,500 | ✅ Within Budget |
| Rent | 2,376 | 70,000 | 67,624 | ✅ Within Budget |
| Transport | 500 | 15,000 | 14,500 | ✅ Within Budget |
| Utilities | 2,204 | 25,000 | 22,796 | ✅ Within Budget |

## 💡 Use Cases

- Personal expense tracking and budgeting
- Financial goal planning and savings targets
- Spending pattern analysis
- Budget rebalancing recommendations
- Financial health monitoring
- Future cash flow predictions

## 📝 License

This project is open source and available for educational and personal use.

## 👨‍💻 Author

**Ajinkya7890**

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork this repository and submit pull requests.

## 📧 Feedback

For questions, suggestions, or feedback, please open an issue on the GitHub repository.

---

**Note**: This is a demonstration project showcasing financial analysis techniques in Python. For production financial applications, additional security and compliance measures would be necessary.
