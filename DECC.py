import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ PCS Data (Texas vs. Germany) ------------------------ #
SPENDING_DATA = {
    "Texas": {"Rent": 1500, "Groceries": 600, "Entertainment": 200, "Transportation": 300, "Utilities": 200},
    "Germany": {"Rent": 1800, "Groceries": 700, "Entertainment": 150, "Transportation": 250, "Utilities": 250}
}

AI_RESPONSES = {
    "Plan my PCS move": {
        "Germany": "Your highest expense in Germany will be rent. Consider securing on-base housing for cost savings. Also, expect higher grocery costs.",
    },
    "Compare my current vs. future costs": {
        "Germany": "Rent is typically higher in Germany, but utility costs may be lower. Consider fuel-efficient vehicles or public transit to save on transportation."
    },
    "Set my PCS budget": {
        "Germany": "Set aside extra funds for move-in costs such as deposits, furniture, and unexpected international fees."
    },
    "Optimize my overseas banking": {
        "Germany": "Avoid high exchange fees by using a multi-currency account like Wise or Revolut for better conversion rates."
    }
}

# ------------------------ Helper Functions ------------------------ #
@st.cache_data
def get_spending_data():
    """Returns the PCS spending data dictionary."""
    return SPENDING_DATA

@st.cache_data
def get_ai_responses():
    """Returns the AI responses dictionary."""
    return AI_RESPONSES

def plot_spending_comparison(spending_data):
    """Generate a side-by-side cost comparison (Texas vs. Germany)."""
    df = pd.DataFrame(spending_data).T  # Transpose for better visualization

    fig, ax = plt.subplots(figsize=(7, 4))
    df.plot(kind="bar", ax=ax)
    ax.set_title("Cost Comparison: Texas vs. Germany")
    ax.set_ylabel("Monthly Expense ($)")
    ax.legend(title="Category")
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    return fig

def display_budget_tracking(budget_goal: int, spending: dict):
    """Tracks PCS budget usage and gives feedback."""
    total_spent = sum(spending.values())
    remaining_budget = budget_goal - total_spent
    percentage_used = min(total_spent / budget_goal, 1.0)

    st.write("### 📊 PCS Budget Tracking")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Budget Overview")
        st.metric(
            label="Total Spent", 
            value=f"${total_spent:.2f}", 
            delta=f"${remaining_budget:.2f}"
        )
        st.progress(percentage_used)

        if total_spent > budget_goal:
            st.error(f"🚨 You've exceeded your PCS budget by ${total_spent - budget_goal:.2f}.")
        elif total_spent < budget_goal * 0.5:
            st.info(f"👍 You're managing well—only {total_spent / budget_goal * 100:.1f}% of your budget used.")
        else:
            st.warning(f"⚠️ Be cautious—you're at {total_spent / budget_goal * 100:.1f}% of your budget.")

# ------------------------ Streamlit App Config ------------------------ #
st.set_page_config(page_title="PCS Financial Planner", layout="wide")

# ------------------------ Sidebar Inputs ------------------------ #
st.sidebar.header("✈️ PCS Financial Planning")
ai_responses = get_ai_responses()
project_type = st.sidebar.selectbox("Select a PCS-related goal:", list(ai_responses.keys()))

st.sidebar.header("🌍 Compare Costs: Texas vs. Germany")
spending_data = get_spending_data()
selected_region = "Germany"  # Always comparing Texas to Germany for this PCS case

st.sidebar.header("💰 Set Your PCS Budget")
budget_goal = st.sidebar.slider("Set your transition budget ($)", min_value=1000, max_value=10000, step=500)

# ------------------------ Main Layout ------------------------ #
st.title("🇺🇸 ➡️ 🇩🇪 Military PCS Financial Planner")
st.subheader(f"📍 Texas vs. {selected_region} - {project_type}")

# Layout with two columns: one for the spending breakdown and one for AI insights.
col_chart, col_insights = st.columns([2, 1])

with col_chart:
    st.write("### 📊 Cost Comparison: Texas vs. Germany")
    fig = plot_spending_comparison(spending_data)
    st.pyplot(fig, use_container_width=True)

with col_insights:
    st.write("### 🤖 AI-Powered PCS Tips")
    ai_message = ai_responses.get(project_type, {}).get(selected_region, "No insights available for this selection.")
    st.info(ai_message)
