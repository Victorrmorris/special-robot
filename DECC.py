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

# ---------------------- Free Text Prompt Box ---------------------- #
st.sidebar.markdown("---")
user_query = st.sidebar.text_area(
    "💬 Ask a financial question or request insights:",
    placeholder="e.g., How can I reduce my utility costs?"
)
if st.sidebar.button("Submit Query"):
    st.sidebar.write(f"📢 Response: This feature is under development. Your query: '{user_query}' has been recorded.")

# ---------------------- Hardcoded Data ---------------------- #
AI_INSIGHTS = {
    "Manage my bills": "📌 Your total outstanding bills this month are **$4,874.31**. Ensure timely payments to avoid late fees.",
    "Create and manage budgets": "📌 You have **$231.84 remaining** across your household budgets. Consider adjusting discretionary spending.",
    "View my savings or investments": "📌 Your current investment portfolio is valued at **$53,926.44**. Consider diversifying further for stability.",
    "View and manage my credit score": "📌 Your credit utilization is **36.13%**, slightly over the recommended 30%. Paying down **$1,020** can improve your score.",
    "Categorize my expenses": "📌 Your top expense category this month is **Rent ($1,800)**. Look for savings opportunities in discretionary spending.",
    "Track and manage my subscriptions": "📌 You have **recurring payments** for Internet ($39.99) and Utilities ($30). Review and optimize your subscriptions."
}

SUBSCRIPTION_DATA = {
    "Spotify": 10.99,
    "Netflix": 15.49,
    "Amazon Prime": 14.99,
    "YouTube TV": 72.99,
    "NBA League Pass": 14.99,
    "Hulu": 7.99,
    "Disney+": 7.99,
    "Apple Music": 10.99
}

# ---------------------- Chart Functions ---------------------- #
def plot_bills_chart():
    """Bar chart showing upcoming bill payments."""
    categories = ["Rent", "Internet", "Utilities"]
    amounts = [1800, 39.99, 30]
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(categories, amounts, color=["#4A90E2", "#50E3C2", "#F5A623"])
    ax.set_title("Upcoming Bill Payments", fontsize=14, fontweight="bold")
    ax.set_ylabel("Amount ($)", fontsize=12)
    
    for i, v in enumerate(amounts):
        ax.text(i, v + 50, f"${v:.2f}", ha='center', fontsize=12, fontweight="bold")

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    return fig

def plot_budget_chart():
    """Donut chart for budget allocation."""
    categories = ["Needs", "Wants", "Savings"]
    values = [50, 30, 20]
    colors = ["#F5A623", "#4A90E2", "#50E3C2"]
    
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        values, labels=categories, autopct="%1.1f%%", colors=colors, startangle=90,
        wedgeprops={"edgecolor": "black"}, textprops={'fontsize': 12}
    )
    for text in autotexts:
        text.set_fontsize(12)
        text.set_fontweight("bold")
    
    ax.set_title("Budget Allocation", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig

def plot_subscriptions_chart():
    """Bar chart for most common subscriptions."""
    services = list(SUBSCRIPTION_DATA.keys())
    costs = list(SUBSCRIPTION_DATA.values())
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(services, costs, color="#4A90E2")
    ax.set_title("Monthly Subscription Costs", fontsize=14, fontweight="bold")
    ax.set_xlabel("Cost ($)", fontsize=12)

    for i, v in enumerate(costs):
        ax.text(v + 1, i, f"${v:.2f}", fontsize=12, fontweight="bold")

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
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
