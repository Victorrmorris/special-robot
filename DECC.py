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

# **User Input: Number of Accounts & Fintech Usage**
num_accounts = st.sidebar.slider("How many bank accounts do you manage?", 1, 10, 4)
num_fintech_apps = st.sidebar.slider("How many fintech apps do you use?", 0, 10, 3)

# ---------------------- Forecast Parameters ---------------------- #
savings_rate = savings_target / monthly_income  # % of income saved
fintech_boost = num_fintech_apps * 0.02  # 2% savings boost per fintech app
high_yield_savings_rate = 0.045  # 4.5% APY for HYSAs
low_interest_rate = 0.01  # 1% APY for standard savings
expense_reduction = 0.10  # 10% discretionary spending reduction

# ---------------------- Forecast Function ---------------------- #
def calculate_savings_projection(months):
    """Simulates savings growth over a given period considering income, savings, interest rates, and fintech boosts."""
    
    # Initial balance (assumed from current savings)
    initial_savings = 10000  # Hypothetical current savings
    balance = initial_savings
    projections = []
    
    for month in range(1, months + 1):
        # Monthly savings contribution (base + fintech boost)
        monthly_savings = (monthly_income * savings_rate) + (monthly_income * fintech_boost)
        
        # Apply interest (assuming part is in HYSA, part in regular savings)
        balance += monthly_savings
        balance += (balance * high_yield_savings_rate / 12)  # High-yield account growth
        
        projections.append((month, balance))
    
    return projections

# ---------------------- Generate Forecasts ---------------------- #
savings_6_months = calculate_savings_projection(6)
savings_12_months = calculate_savings_projection(12)
savings_24_months = calculate_savings_projection(24)

# ---------------------- Chart Function ---------------------- #
def plot_savings_forecast():
    """Line chart for detailed savings growth forecast."""
    months_6, balance_6 = zip(*savings_6_months)
    months_12, balance_12 = zip(*savings_12_months)
    months_24, balance_24 = zip(*savings_24_months)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months_6, balance_6, marker="o", linestyle="-", label="6-Month Projection", color="#4A90E2")
    ax.plot(months_12, balance_12, marker="s", linestyle="--", label="12-Month Projection", color="#F5A623")
    ax.plot(months_24, balance_24, marker="^", linestyle=":", label="24-Month Projection", color="#50E3C2")

    ax.set_xlabel("Months", fontsize=12)
    ax.set_ylabel("Total Savings ($)", fontsize=12)
    ax.set_title("Projected Savings Growth Over Time", fontsize=14, fontweight="bold")
    ax.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    
    return fig

# ---------------------- Display Section ---------------------- #
st.title("💰 DECC Automated Savings Forecast")
st.subheader("📊 Detailed Savings Growth Projections")

# Display Chart
st.pyplot(plot_savings_forecast())

# Display projected balances
future_balances_6 = savings_6_months[-1][1]
future_balances_12 = savings_12_months[-1][1]
future_balances_24 = savings_24_months[-1][1]

st.markdown(f"""
### 📌 Future Savings Estimates:
- **💰 Current Total Savings:** **$10,000.00** _(hypothetical starting balance)_
- **📈 6-Month Projection:** **${future_balances_6:,.2f}**  
- **🚀 12-Month Projection:** **${future_balances_12:,.2f}**  
- **🌍 24-Month Projection:** **${future_balances_24:,.2f}**  
""")

# ---------------------- AI Insights ---------------------- #
if future_balances_12 >= 20000:
    ai_insight = "📌 Excellent progress! You are on track to double your savings within a year. Consider diversifying investments."
elif future_balances_12 >= 15000:
    ai_insight = "📌 Good job! You're on track for solid financial growth. Automating more savings could further boost results."
else:
    ai_insight = "📌 Your savings growth is steady, but consider increasing contributions or exploring higher-yield accounts."

st.write("### 🤖 AI Savings Insights")
st.info(ai_insight)

# ---------------------- Footer ---------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
