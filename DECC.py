import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ Dummy Data ------------------------ #
SPENDING_DATA = {
    "Germany": {"Rent": 1800, "Groceries": 700, "Entertainment": 150, "Transportation": 200, "Utilities": 250},
    "Italy": {"Rent": 1600, "Groceries": 650, "Entertainment": 200, "Transportation": 180, "Utilities": 230},
    "UK": {"Rent": 1900, "Groceries": 750, "Entertainment": 250, "Transportation": 220, "Utilities": 300},
}

AI_RESPONSES = {
    "Track and analyze my spending habits": {
        "Germany": "Your highest expense in Germany is rent, followed by groceries. Consider adjusting entertainment spending for better savings.",
        "Italy": "Housing and groceries take up the majority of your spending in Italy. Look into local markets for better grocery savings.",
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
    }
}

# ------------------------ Helper Functions ------------------------ #
@st.cache_data
def get_spending_data():
    """Cache and return spending data."""
    return SPENDING_DATA

@st.cache_data
def get_ai_responses():
    """Cache and return AI responses."""
    return AI_RESPONSES

def plot_spending_breakdown(region: str, spending_data: dict) -> plt.Figure:
    """Generate a bar chart for the spending breakdown of the selected region."""
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

# ------------------------ Streamlit App Config ------------------------ #
st.set_page_config(page_title="DECC Financial Insights", layout="wide")

# ------------------------ Sidebar Inputs ------------------------ #
st.sidebar.header("📊 Define Your Financial Project")
ai_responses = get_ai_responses()
project_type = st.sidebar.selectbox("Select a financial goal:", list(ai_responses.keys()))

st.sidebar.header("🌍 Select Spending Region")
spending_data = get_spending_data()
spending_region = st.sidebar.selectbox("Choose a region:", list(spending_data.keys()))

st.sidebar.header("🎯 Set Spending Target")
budget_goal = st.sidebar.slider("Set a monthly budget limit ($)", min_value=500, max_value=3000, step=100)

# ------------------------ Main Layout ------------------------ #
st.title("💰 DECC Financial Insights Dashboard")
st.subheader(f"📍 {spending_region} - {project_type}")

# Layout with columns: 2/3 for the chart and 1/3 for AI insights
col_chart, col_insights = st.columns([2, 1])

with col_chart:
    st.write("### 📊 Spending Breakdown")
    fig = plot_spending_breakdown(spending_region, spending_data)
    st.pyplot(fig, use_container_width=True)

with col_insights:
    st.write("### 🤖 AI Insights")
    ai_message = ai_responses.get(project_type, {}).get(spending_region)
    if ai_message:
        st.info(ai_message)
    else:
        st.warning("No insights available for this selection.")

# ------------------------ Budget Tracking ------------------------ #
st.write("### 📊 Budget Tracking")
region_spending = spending_data.get(spending_region, {})
total_spent = sum(region_spending.values())

if total_spent > budget_goal:
    st.error(f"🚨 You've exceeded your budget of ${budget_goal} by ${total_spent - budget_goal}. Consider adjusting your expenses.")
else:
    st.success(f"✅ You are within your budget of ${budget_goal}! Keep it up.")

# ------------------------ Footer ------------------------ #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
