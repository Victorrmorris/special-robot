import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- Page Configuration ---------------------- #
st.set_page_config(page_title="DECC Savings Forecast", layout="wide")

# ---------------------- User's Account Balances ---------------------- #
account_balances = {
    "USAA Checking": 4500.13,
    "AMEX Savings": 20348.05,
    "SCU Checking (Local)": 233.81,
    "Wise (Multi-currency)": 198.76,
    "Greenlight (Kids)": 300.00
}

# ---------------------- Assumptions ---------------------- #
monthly_income = 4000  # User's estimated monthly income ($)
savings_rate = 0.15  # 15% of income is saved each month
expense_reduction = 0.10  # 10% reduction in discretionary spending
fintech_savings_boost = 0.05  # Additional 5% savings boost
interest_rates = {
    "AMEX Savings": 0.045,  # 4.5% APY
    "Wise (Multi-currency)": 0.02  # 2.0% APY
}

# ---------------------- Savings Forecast Function ---------------------- #
def calculate_savings_projection(months):
    """Simulates savings growth over a given number of months."""
    
    # Initialize balances
    projected_balances = account_balances.copy()
    savings_growth = []

    for month in range(1, months + 1):
        # Monthly savings contribution
        monthly_savings = monthly_income * savings_rate
        fintech_boost = monthly_savings * fintech_savings_boost
        total_monthly_savings = monthly_savings + fintech_boost

        # Distribute savings
        projected_balances["AMEX Savings"] += total_monthly_savings
        projected_balances["USAA Checking"] += (monthly_income * expense_reduction)  # Extra savings

        # Apply interest growth
        for account, rate in interest_rates.items():
            projected_balances[account] += projected_balances[account] * (rate / 12)  # Monthly interest

        # Store for visualization
        total_balance = sum(projected_balances.values())
        savings_growth.append((month, total_balance))

    return savings_growth

# Generate savings projections for 6 and 12 months
savings_6_months = calculate_savings_projection(6)
savings_12_months = calculate_savings_projection(12)

# ---------------------- Chart Function ---------------------- #
def plot_savings_forecast():
    """Line chart visualizing savings growth over time."""
    months_6, balance_6 = zip(*savings_6_months)
    months_12, balance_12 = zip(*savings_12_months)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months_6, balance_6, marker="o", linestyle="-", label="6-Month Projection", color="#4A90E2")
    ax.plot(months_12, balance_12, marker="s", linestyle="--", label="12-Month Projection", color="#F5A623")

    ax.set_xlabel("Months", fontsize=12)
    ax.set_ylabel("Total Savings ($)", fontsize=12)
    ax.set_title("Projected Savings Growth Over Time", fontsize=14, fontweight="bold")
    ax.legend()

    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    return fig

# ---------------------- Display Section ---------------------- #
st.title("💰 DECC Automated Savings Forecast")
st.subheader("📊 Projected Savings Growth Over 6 & 12 Months")

# Display Chart
st.pyplot(plot_savings_forecast())

# Display projected balances
st.write("### 📌 Estimated Future Savings Balances")
future_balances_6 = savings_6_months[-1][1]
future_balances_12 = savings_12_months[-1][1]

st.markdown(f"""
- **💰 Total Balance Now:** **${sum(account_balances.values()):,.2f}**
- **📈 6-Month Projection:** **${future_balances_6:,.2f}**  
- **🚀 12-Month Projection:** **${future_balances_12:,.2f}**  
""")

# Display AI-driven insights
st.write("### 🤖 AI Insights")
st.info("📌 Automating your savings with fintech apps and high-yield accounts could increase your savings by 20% over the next year.")

# ---------------------- Footer ---------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
