import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ Pre-Move PCS Expense Categories ------------------------ #
EXPENSE_CATEGORIES = {
    "Reimbursable Expenses": {
        "Flight Tickets": 1200,
        "Hotel Stays (Temporary Lodging)": 800,
        "Shipping Household Goods": 3000,
        "Per Diem (Meals & Incidentals)": 500,
        "Vehicle Shipment (If Approved)": 2500
    },
    "Non-Reimbursable Expenses": {
        "Initial Rent & Deposit": 2000,
        "Furniture & Appliances": 1500,
        "Car Rental or Public Transport": 600,
        "Cell Phone Setup": 150,
        "Miscellaneous Fees": 400
    }
}

AI_RESPONSES = {
    "Plan my PCS budget": "Consider separating reimbursable vs. non-reimbursable expenses. The military may cover flights, lodging, and per diem, but you will need to budget for housing deposits, furniture, and transportation.",
    "Estimate moving costs": "A safe estimate for a PCS move to Germany is $6,000-$10,000, depending on family size and lifestyle adjustments. Plan for initial rent deposits and setup costs.",
    "Track reimbursable expenses": "Keep all receipts and documentation for flights, lodging, and per diem. Submit your travel claim promptly to receive reimbursement faster.",
    "Reduce out-of-pocket expenses": "Consider furnished housing to save on furniture costs. Use on-base resources like loan closets to borrow temporary household goods."
}

# ------------------------ Helper Functions ------------------------ #
@st.cache_data
def get_expense_data():
    """Returns the PCS expense categories dictionary."""
    return EXPENSE_CATEGORIES

@st.cache_data
def get_ai_responses():
    """Returns the AI responses dictionary."""
    return AI_RESPONSES

def plot_expense_breakdown(expenses):
    """Generate a bar chart for PCS expense breakdown."""
    df = pd.DataFrame(expenses.items(), columns=["Category", "Amount"])
    
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(df["Category"], df["Amount"], color=["#4CAF50" if "Reimbursable" in expenses else "#FF5733" for _ in df["Category"]])
    ax.set_title("PCS Expense Breakdown")
    ax.set_xlabel("Category")
    ax.set_ylabel("Estimated Cost ($)")
    plt.xticks(rotation=45, ha="right")
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom")
    
    plt.tight_layout()
    return fig

def display_budget_summary(reimbursable, non_reimbursable, user_budget):
    """Summarizes the user's PCS budget, showing total estimates vs. user input."""
    total_reimbursable = sum(reimbursable.values())
    total_non_reimbursable = sum(non_reimbursable.values())
    total_estimated_cost = total_reimbursable + total_non_reimbursable
    
    st.write("### 📊 PCS Budget Summary")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.metric(label="Estimated Reimbursable Costs", value=f"${total_reimbursable}")
        st.metric(label="Estimated Non-Reimbursable Costs", value=f"${total_non_reimbursable}")
        st.metric(label="Total Estimated PCS Cost", value=f"${total_estimated_cost}")
    
    with col_right:
        remaining_budget = user_budget - total_non_reimbursable
        percentage_used = min(total_non_reimbursable / user_budget, 1.0)
        
        st.metric(label="Your PCS Budget", value=f"${user_budget}")
        st.metric(label="Remaining After Non-Reimbursable", value=f"${remaining_budget}")

        st.progress(percentage_used)

        if total_non_reimbursable > user_budget:
            st.error(f"🚨 Your budget is short by ${total_non_reimbursable - user_budget}. Consider adjusting your plan.")
        else:
            st.success(f"✅ You have ${remaining_budget} left in your budget after non-reimbursable costs.")

# ------------------------ Streamlit App Config ------------------------ #
st.set_page_config(page_title="PCS Budget Planner", layout="wide")

# ------------------------ Sidebar Inputs ------------------------ #
st.sidebar.header("✈️ Plan Your PCS Budget")
ai_responses = get_ai_responses()
budgeting_goal = st.sidebar.selectbox("Select a budgeting goal:", list(ai_responses.keys()))

st.sidebar.header("💰 Set Your PCS Budget")
user_budget = st.sidebar.slider("Enter your estimated PCS budget ($)", min_value=5000, max_value=15000, step=500)

# ------------------------ Main Layout ------------------------ #
st.title("🇺🇸 ➡️ 🇩🇪 Military PCS Budget Planner")
st.subheader(f"📍 {budgeting_goal}")

# Layout: Reimbursable vs. Non-Reimbursable Expenses
col_left, col_right = st.columns([1, 1])

expense_data = get_expense_data()
with col_left:
    st.write("### ✅ Reimbursable Expenses")
    fig_reimb = plot_expense_breakdown(expense_data["Reimbursable Expenses"])
    st.pyplot(fig_reimb, use_container_width=True)

with col_right:
    st.write("### ❌ Non-Reimbursable Expenses")
    fig_non_reimb = plot_expense_breakdown(expense_data["Non-Reimbursable Expenses"])
    st.pyplot(fig_non_reimb, use_container_width=True)

# ------------------------ Budget Summary ------------------------ #
display_budget_summary(expense_data["Reimbursable Expenses"], expense_data["Non-Reimbursable Expenses"], user_budget)

# ------------------------ AI-Powered PCS Insights ------------------------ #
st.write("### 🤖 AI-Generated PCS Budgeting Tips")
st.info(ai_responses.get(budgeting_goal, "No insights available for this selection."))

# ------------------------ Actionable Checklist ------------------------ #
st.write("### ✅ PCS Budget Planning Checklist")
st.markdown("""
- 📝 **Create a PCS budget plan** separating reimbursable vs. non-reimbursable expenses.
- 📄 **Keep all receipts** for travel claims to ensure timely reimbursements.
- 🏠 **Research housing options**—on-base vs. off-base to reduce rent costs.
- 🚗 **Plan for transportation**—will you ship a car or buy locally?
- 💳 **Open an overseas-friendly bank account** to avoid exchange fees.
- 📦 **Decide what to ship** and what to sell/store before moving.
""")

# ------------------------ Footer ------------------------ #
st.markdown("---")
st.markdown("🔒 **DECC provides financial intelligence for U.S. military and expats moving overseas.**")
