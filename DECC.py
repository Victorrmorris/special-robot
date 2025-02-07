import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ Dummy Data ------------------------ #
SPENDING_DATA = {
    "Germany": {
        "Rent": 1800,
        "Groceries": 700,
        "Entertainment": 150,
        "Transportation": 200,
        "Utilities": 250
    },
    "Italy": {
        "Rent": 1600,
        "Groceries": 650,
        "Entertainment": 200,
        "Transportation": 180,
        "Utilities": 230
    },
    "UK": {
        "Rent": 1900,
        "Groceries": 750,
        "Entertainment": 250,
        "Transportation": 220,
        "Utilities": 300
    },
}

# ------------------------ AI Responses ------------------------ #
# Original four goals plus the new "Consolidate multi-currency accounts" goal.
AI_RESPONSES = {
    "Track and analyze my spending habits": {
        "Germany": "Your highest expense in Germany is rent, followed by groceries. Consider adjusting entertainment spending for better savings.",
        "Italy": ("Housing and groceries take up the majority of your spending in Italy. Look into local markets for better grocery savings. "
                  "Would you like a comparison of local markets in your area?"),
        "UK": "Rent in the UK is a significant portion of your budget. Public transport passes might help reduce overall travel expenses."
    },
    "Reduce my expenses": {
        "Germany": "To reduce expenses in Germany, consider switching to budget grocery stores like Aldi and Lidl and cutting back on dining out.",
        "Italy": "Reducing expenses in Italy? Minimize transportation costs by using regional train passes and buying groceries in bulk.",
        "UK": "In the UK, avoiding peak-hour transportation fares and seeking out rent-sharing opportunities could lower costs."
    },
    "Set a monthly budget": {
        "Germany": "Setting a budget? Try allocating 50% to needs, 30% to wants, and 20% to savings while tracking expenses weekly.",
        "Italy": "For Italy, make sure to budget for unexpected fees such as tourist taxes or annual home maintenance costs.",
        "UK": "UK budgeting tip: Track variable expenses like electricity, which fluctuates seasonally, to avoid overspending."
    },
    "Optimize currency exchange": {
        "Germany": "Frequent transactions in Germany? Use a multi-currency bank account like Wise to minimize conversion fees.",
        "Italy": "For Italy, avoid dynamic currency conversion when paying with foreign cards—it often leads to extra fees.",
        "UK": "Using Revolut or Monzo in the UK could help optimize currency exchange rates and reduce international withdrawal fees."
    },
    "Consolidate multi-currency accounts": {
        "Germany": "Consolidating your accounts in Germany has simplified tracking. Consider using automated tools for real-time currency conversion.",
        "Italy": "Your multi-currency accounts in Italy are well balanced. Regularly review exchange rates to optimize fund allocation.",
        "UK": "Consolidating UK accounts improves clarity. Monitor currency fluctuations to adjust your holdings accordingly."
    }
}

# ------------------------ Helper Functions ------------------------ #
@st.cache_data
def get_spending_data():
    """Returns the spending data dictionary."""
    return SPENDING_DATA

@st.cache_data
def get_ai_responses():
    """Returns the AI responses dictionary."""
    return AI_RESPONSES

# ------------------------ Chart Functions ------------------------ #
def plot_spending_breakdown(region: str, spending_data: dict) -> plt.Figure:
    """Bar chart for spending breakdown."""
    spending = spending_data.get(region, {})
    df = pd.DataFrame(list(spending.items()), columns=["Category", "Amount"])
    
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(df["Category"], df["Amount"], color="skyblue")
    ax.set_title(f"Spending Breakdown in {region}")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount ($)")
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{height}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom"
        )
    plt.tight_layout()
    return fig

def plot_expense_reduction_chart(spending: dict) -> plt.Figure:
    """Grouped bar chart comparing current spending vs. a 10% reduction."""
    categories = list(spending.keys())
    current_spending = [spending[cat] for cat in categories]
    reduced_spending = [amt * 0.9 for amt in current_spending]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    width = 0.35
    indices = range(len(categories))
    
    ax.bar([i - width/2 for i in indices], current_spending, width=width,
           label='Current', color='salmon')
    ax.bar([i + width/2 for i in indices], reduced_spending, width=width,
           label='Reduced (10%)', color='lightgreen')
    
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Expense Reduction Potential")
    ax.set_xticks(indices)
    ax.set_xticklabels(categories)
    ax.legend()
    
    plt.tight_layout()
    return fig

def plot_budget_donut_chart(budget_goal: int) -> plt.Figure:
    """
    Donut chart showing the AI-recommended allocations:
      - Needs: 50%
      - Wants: 30%
      - Savings: 20%
    Dollar amounts are calculated from the default budget target.
    """
    allocations = {"Needs": 50, "Wants": 30, "Savings": 20}
    amounts = [budget_goal * pct / 100 for pct in allocations.values()]
    labels = [f"{cat} ({pct}%)" for cat, pct in allocations.items()]
    colors = ["gold", "lightcoral", "lightskyblue"]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(
        amounts, 
        labels=labels, 
        autopct=lambda pct: f"${budget_goal * pct / 100:.0f}",
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.4)
    )
    ax.set_title("Budget Allocation (Needs: 50%, Wants: 30%, Savings: 20%)")
    ax.set(aspect="equal")
    plt.tight_layout()
    return fig

def plot_currency_optimization_chart(region: str) -> plt.Figure:
    """
    Dummy bar chart for currency exchange optimization.
    Simulates current vs. optimized exchange rates for the selected region.
    """
    data = {
        "Germany": {"Current Rate": 1.00, "Optimized Rate": 0.98},
        "Italy": {"Current Rate": 1.00, "Optimized Rate": 0.97},
        "UK": {"Current Rate": 1.00, "Optimized Rate": 0.99}
    }
    region_data = data.get(region, {"Current Rate": 1.00, "Optimized Rate": 1.00})
    categories = list(region_data.keys())
    rates = list(region_data.values())
    
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(categories, rates, color=['skyblue', 'lightgreen'])
    ax.set_title(f"Currency Exchange Optimization for {region}")
    ax.set_ylabel("Exchange Rate")
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")
    plt.tight_layout()
    return fig

def plot_multi_currency_chart() -> plt.Figure:
    """Pie chart showing distribution across multi-currency accounts."""
    currencies = ["USD", "EUR", "GBP"]
    balances = [3000, 2500, 1500]
    colors = ["#ffcc99", "#c2c2f0", "#ffb3e6"]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(balances, labels=currencies, autopct=lambda pct: f"${pct:.0f}", colors=colors, startangle=90)
    ax.set_title("Multi-Currency Account Distribution")
    ax.set(aspect="equal")
    plt.tight_layout()
    return fig

# ------------------------ Financial Goal Chart Selector ------------------------ #
def get_financial_goal_chart(project_type: str, spending_data: dict,
                             spending_region: str, budget_goal: int) -> plt.Figure:
    """
    Returns the appropriate chart based on the selected financial goal.
    """
    spending = spending_data.get(spending_region, {})
    if project_type == "Track and analyze my spending habits":
        return plot_spending_breakdown(spending_region, spending_data)
    elif project_type == "Reduce my expenses":
        return plot_expense_reduction_chart(spending)
    elif project_type == "Set a monthly budget":
        return plot_budget_donut_chart(budget_goal)
    elif project_type == "Optimize currency exchange":
        return plot_currency_optimization_chart(spending_region)
    elif project_type == "Consolidate multi-currency accounts":
        return plot_multi_currency_chart()
    else:
        return plot_spending_breakdown(spending_region, spending_data)

# ------------------------ Streamlit App Config ------------------------ #
st.set_page_config(page_title="DECC Financial Insights", layout="wide")

# ------------------------ Sidebar Inputs ------------------------ #
st.sidebar.header("📊 Define Your Financial Project")
ai_responses = get_ai_responses()
project_type = st.sidebar.selectbox("Select a financial goal:", list(ai_responses.keys()))

st.sidebar.header("🌍 Select Spending Region")
spending_data = get_spending_data()
spending_region = st.sidebar.selectbox("Choose a region:", list(spending_data.keys()))

# A default budget target is used.
budget_goal = 2000  # Default budget target

# ------------------------ Live Query in Sidebar ------------------------ #
st.sidebar.header("💬 Live Query")
user_query = st.sidebar.text_area(
    "Enter your query", 
    "What are the best internet providers in Northern Italy?", 
    height=150
)
if st.sidebar.button("Get Live Insight"):
    if user_query.strip().lower() == "what are the best internet providers in northern italy?":
        live_insight = ("Based on our dummy data, Fastweb and Vodafone offer the best deals and fastest speeds in Northern Italy.")
    else:
        live_insight = "Dummy insight: This feature is under development. Please try again with a different query."
    st.sidebar.write(live_insight)

# ------------------------ Main Layout ------------------------ #
st.title("💰 DECC Financial Insights Dashboard")
st.subheader(f"📍 {spending_region} - {project_type}")

# Display the selected financial goal chart.
st.write("### 📊 Financial Goal Analysis")
fig_goal = get_financial_goal_chart(project_type, spending_data, spending_region, budget_goal)
st.pyplot(fig_goal, use_container_width=True)

# Display AI Insights.
st.write("### 🤖 AI Insights")
ai_message = ai_responses.get(project_type, {}).get(spending_region, "No insights available for this selection.")
st.info(ai_message)

# ------------------------ Additional Actionable Items ------------------------ #
if project_type == "Track and analyze my spending habits":
    if st.checkbox("Would you like to see a detailed table of your spending data?"):
        df_data = pd.DataFrame(
            list(spending_data.get(spending_region, {}).items()),
            columns=["Category", "Amount"]
        )
        st.table(df_data)

if project_type == "Reduce my expenses":
    if st.checkbox("Would you like to see potential cost-saving alternatives?"):
        cost_savings_data = {
            "Expense Category": ["Groceries", "Entertainment", "Transportation", "Utilities"],
            "Suggested Savings": [
                "Save $50 by buying in bulk",
                "Cut $20 by reducing subscriptions",
                "Save $30 with public transit",
                "Reduce $15 by conserving energy"
            ]
        }
        st.table(pd.DataFrame(cost_savings_data))

if project_type == "Set a monthly budget":
    if st.checkbox("Would you like to set a budget based on your monthly income?"):
        monthly_income = st.number_input("Enter your monthly income ($)", min_value=100, value=3000, key="income_input")
        recommended_budget = monthly_income * 0.7
        st.write(f"Based on your monthly income of ${monthly_income}, your recommended monthly budget is ${recommended_budget:.2f}.")

if project_type == "Optimize currency exchange":
    if st.checkbox("Would you like to see a comparison of exchange fees among popular providers?"):
        provider_data = {
            "Provider": ["Wise", "Revolut", "Monzo", "Local Bank"],
            "Fee": ["1.5%", "1.0%", "1.2%", "3.0%"]
        }
        st.table(pd.DataFrame(provider_data))

# ------------------------ Footer ------------------------ #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
