import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- Page Configuration ---------------------- #
st.set_page_config(page_title="DECC Financial Dashboard", layout="wide")

# ---------------------- Sidebar Navigation ---------------------- #
st.sidebar.header("📊 Financial Activities")
financial_activity = st.sidebar.radio(
    "Select a financial activity:",
    [
        "Manage my bills",
        "Create and manage budgets",
        "View my savings or investments",
        "View and manage my credit score",
        "Categorize my expenses",
        "Track and manage my subscriptions",
    ]
)

# ---------------------- Hardcoded Data ---------------------- #
AI_INSIGHTS = {
    "Manage my bills": "📌 Your total outstanding bills this month are **$4,874.31**. Ensure timely payments to avoid late fees.",
    "Create and manage budgets": "📌 You have **$231.84 remaining** across your household budgets. Consider adjusting discretionary spending.",
    "View my savings or investments": "📌 Your current investment portfolio is valued at **$53,926.44**. Consider diversifying further for stability.",
    "View and manage my credit score": "📌 Your credit utilization is **36.13%**, slightly over the recommended 30%. Paying down **$1,020** can improve your score.",
    "Categorize my expenses": "📌 Your top expense category this month is **Rent ($1,800)**. Look for savings opportunities in discretionary spending.",
    "Track and manage my subscriptions": "📌 You have **recurring payments** for Internet ($39.99) and Utilities ($30). Review and optimize your subscriptions."
}

# ---------------------- Chart Functions ---------------------- #
def plot_bills_chart():
    """Bar chart showing upcoming bill payments."""
    categories = ["Rent", "Internet", "Utilities"]
    amounts = [1800, 39.99, 30]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categories, amounts, color=["#4A90E2", "#50E3C2", "#F5A623"])
    ax.set_title("Upcoming Bill Payments")
    ax.set_ylabel("Amount ($)")
    
    plt.tight_layout()
    return fig

def plot_budget_chart():
    """Donut chart for budget allocation."""
    categories = ["Needs", "Wants", "Savings"]
    values = [50, 30, 20]
    colors = ["#F5A623", "#4A90E2", "#50E3C2"]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(values, labels=categories, autopct="%1.1f%%", colors=colors, startangle=90, wedgeprops={"edgecolor": "black"})
    ax.set_title("Budget Allocation")
    
    plt.tight_layout()
    return fig

def plot_investments_chart():
    """Bar chart for investment portfolio."""
    accounts = ["Schwab", "Fidelity", "Thrift Savings Plan"]
    balances = [7890.32, 12487.23, 33548.89]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(accounts, balances, color=["#4A90E2", "#50E3C2", "#F5A623"])
    ax.set_title("Investment Portfolio")
    ax.set_ylabel("Balance ($)")
    
    plt.tight_layout()
    return fig

def plot_credit_chart():
    """Line chart for credit utilization trend."""
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    utilization = [34, 35, 36, 36.5, 36.13]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(months, utilization, marker="o", linestyle="-", color="#F5A623")
    ax.set_title("Credit Utilization Over Time")
    ax.set_ylabel("Utilization (%)")
    ax.axhline(y=30, color="red", linestyle="--", label="Recommended 30%")
    ax.legend()
    
    plt.tight_layout()
    return fig

def plot_expenses_chart():
    """Pie chart for expense categorization."""
    categories = ["Rent", "Groceries", "Utilities", "Entertainment", "Education"]
    amounts = [1800, 845.98, 179.20, 154.67, 123.54]
    colors = ["#F5A623", "#4A90E2", "#50E3C2", "#9013FE", "#D0021B"]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", colors=colors, startangle=90, wedgeprops={"edgecolor": "black"})
    ax.set_title("Expense Categorization")
    
    plt.tight_layout()
    return fig

def plot_subscriptions_chart():
    """Bar chart for subscription management."""
    services = ["Internet", "Utilities", "Streaming"]
    costs = [39.99, 30, 14.99]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(services, costs, color=["#4A90E2", "#50E3C2", "#F5A623"])
    ax.set_title("Monthly Subscription Costs")
    ax.set_ylabel("Cost ($)")
    
    plt.tight_layout()
    return fig

# ---------------------- Display Section ---------------------- #
st.title("💰 DECC Financial Dashboard")
st.subheader(f"📍 {financial_activity}")

# Display relevant chart based on the selected financial activity
st.write("### 📊 Financial Analysis")

chart_mapping = {
    "Manage my bills": plot_bills_chart,
    "Create and manage budgets": plot_budget_chart,
    "View my savings or investments": plot_investments_chart,
    "View and manage my credit score": plot_credit_chart,
    "Categorize my expenses": plot_expenses_chart,
    "Track and manage my subscriptions": plot_subscriptions_chart,
}

if financial_activity in chart_mapping:
    st.pyplot(chart_mapping[financial_activity]())

# Display AI-driven insights
st.write("### 🤖 AI Insights")
st.info(AI_INSIGHTS.get(financial_activity, "No insights available for this selection."))

# ---------------------- Footer ---------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
