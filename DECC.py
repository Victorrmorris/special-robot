import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- Page Configuration ---------------------- #
st.set_page_config(page_title="DECC Automated Savings Optimizer", layout="wide")

# ---------------------- Sidebar ---------------------- #
st.sidebar.header("🌍 Automated Savings Optimizer")

# **User Selection: Financial Goal**
financial_goal = st.sidebar.selectbox(
    "Select your financial savings goal:",
    [
        "Automate my savings",
        "Augment my savings using fintech apps",
        "Optimize multi-currency savings",
        "Compare savings accounts and interest rates",
    ]
)

# **User Input: Monthly Income & Savings Target**
st.sidebar.markdown("### 🏦 Financial Profile")
monthly_income = st.sidebar.number_input("Enter your monthly income ($)", min_value=500, value=4000, step=100)
savings_target = st.sidebar.number_input("Desired monthly savings ($)", min_value=0, value=500, step=50)

# **User Input: Number of Accounts**
num_accounts = st.sidebar.slider("How many bank accounts do you manage?", 1, 10, 4)
num_fintech_apps = st.sidebar.slider("How many fintech apps do you use?", 0, 10, 3)

# **Submit Button**
if st.sidebar.button("Generate Insights"):
    st.sidebar.success("📊 Insights Updated Below ⬇️")

# ---------------------- Hardcoded Data ---------------------- #
AI_INSIGHTS = {
    "Automate my savings": "📌 Automating your savings can increase your long-term savings rate by up to 15%. Fintech apps like Acorns and Qapital help round up purchases to increase savings seamlessly.",
    "Augment my savings using fintech apps": "📌 Millennials and Gen Z users save over **$27 billion** beyond their regular accounts through automated savings tools. Explore options like Yotta and Chime to boost your savings effortlessly.",
    "Optimize multi-currency savings": "📌 Living in Europe? Use multi-currency fintech solutions like **Wise or Revolut** to store savings in multiple currencies and take advantage of the best exchange rates.",
    "Compare savings accounts and interest rates": "📌 Your interest earnings could **double** by switching to a high-yield savings account (HYSA). Top HYSAs currently offer rates above **4.5% APY**."
}

BANK_DATA = {
    "Bank": ["Schwab", "Fidelity", "Revolut", "Wise", "Monzo"],
    "Interest Rate (%)": [4.5, 3.9, 2.5, 1.8, 2.0],
    "Minimum Balance ($)": [0, 1000, 0, 0, 0]
}

FINTECH_APPS = {
    "Fintech App": ["Acorns", "Qapital", "Yotta", "Digit", "Chime"],
    "Savings Boost (%)": [10, 12, 8, 15, 11],
    "User Base (millions)": [9, 6, 5, 7, 12]
}

# ---------------------- Chart Functions ---------------------- #
def plot_savings_chart():
    """Bar chart for savings by fintech app usage."""
    apps = ["Acorns", "Qapital", "Yotta", "Digit", "Chime"]
    boosts = [10, 12, 8, 15, 11]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(apps, boosts, color=["#4A90E2", "#50E3C2", "#F5A623", "#9013FE", "#D0021B"])
    ax.set_xlabel("Savings Boost (%)", fontsize=12)
    ax.set_title("Fintech Apps & Savings Boost", fontsize=14, fontweight="bold")

    for i, v in enumerate(boosts):
        ax.text(v + 1, i, f"+{v}%", fontsize=12, fontweight="bold")

    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    return fig

def plot_multi_currency_savings():
    """Pie chart for savings split by currency."""
    currencies = ["USD", "EUR", "GBP"]
    allocations = [60, 30, 10]

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        allocations, labels=currencies, autopct="%1.1f%%", colors=["#F5A623", "#4A90E2", "#50E3C2"],
        startangle=90, wedgeprops={"edgecolor": "black"}, textprops={'fontsize': 12}
    )

    for text in autotexts:
        text.set_fontsize(12)
        text.set_fontweight("bold")

    ax.set_title("Multi-Currency Savings Distribution", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig

def plot_savings_vs_income():
    """Line chart comparing savings and income trends."""
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    savings = [500, 550, 600, 700, 750]
    income = [4000, 4200, 4300, 4400, 4500]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(months, savings, marker="o", linestyle="-", color="#50E3C2", label="Savings")
    ax.plot(months, income, marker="s", linestyle="--", color="#F5A623", label="Income")
    
    ax.set_ylabel("Amount ($)", fontsize=12)
    ax.set_title("Savings vs. Income Over Time", fontsize=14, fontweight="bold")
    ax.legend()

    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    return fig

# ---------------------- Display Section ---------------------- #
st.title("💰 DECC Automated Savings Optimizer")
st.subheader(f"📍 {financial_goal}")

# Display relevant chart based on the selected financial activity
st.write("### 📊 Financial Analysis")

chart_mapping = {
    "Automate my savings": plot_savings_vs_income,
    "Augment my savings using fintech apps": plot_savings_chart,
    "Optimize multi-currency savings": plot_multi_currency_savings,
}

if financial_goal in chart_mapping:
    st.pyplot(chart_mapping[financial_goal]())

# Display AI-driven insights
st.write("### 🤖 AI Insights")
st.info(AI_INSIGHTS.get(financial_goal, "No insights available for this selection."))

# Display Bank Account Comparisons
if financial_goal == "Compare savings accounts and interest rates":
    df_banks = pd.DataFrame(BANK_DATA)
    st.write("### 🏦 Bank Account Interest Rates")
    st.table(df_banks)

# Display Fintech Savings App Data
if financial_goal == "Augment my savings using fintech apps":
    df_apps = pd.DataFrame(FINTECH_APPS)
    st.write("### 📲 Fintech Savings Apps & Boost")
    st.table(df_apps)

# ---------------------- Footer ---------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
