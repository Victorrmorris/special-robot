import streamlit as st
import matplotlib.pyplot as plt

def display_budget_tracking(budget_goal: int, spending: dict):
    """
    Displays a streamlined budget tracking section using:
      - A metric showing total spent and remaining budget.
      - A progress bar visualizing budget usage.
      - A donut chart for a clear budget distribution.
      - Conditional messaging based on the spending level.
    """
    total_spent = sum(spending.values())
    remaining_budget = budget_goal - total_spent
    # Calculate percentage used (capped at 100% for display)
    percentage_used = min(total_spent / budget_goal, 1.0)

    st.write("### 📊 Budget Tracking")

    # Layout the numeric info and visual feedback in columns
    col_left, col_right = st.columns(2)

    # Left column: Metric and progress bar
    with col_left:
        st.subheader("Budget Overview")
        # Display the total spent as a metric. The delta shows remaining or over-budget amount.
        st.metric(
            label="Total Spent", 
            value=f"${total_spent:.2f}", 
            delta=f"${remaining_budget:.2f}"
        )
        # Progress bar (0 to 1 scale)
        st.progress(percentage_used)

        # Conditional messaging
        if total_spent > budget_goal:
            st.error(f"🚨 You've exceeded your budget by ${total_spent - budget_goal:.2f}.")
        elif total_spent < budget_goal * 0.5:
            st.info(f"👍 Great job! You've only used {total_spent / budget_goal * 100:.1f}% of your budget.")
        else:
            st.warning(f"⚠️ You're nearing your budget limit with {total_spent / budget_goal * 100:.1f}% spent.")

    # Right column: Donut chart visualization
    with col_right:
        st.subheader("Budget Distribution")
        plot_budget_donut(budget_goal, total_spent)

def plot_budget_donut(budget_goal: int, total_spent: float):
    """
    Plots a donut chart showing the split between the amount spent and the remaining budget.
    """
    remaining = max(budget_goal - total_spent, 0)
    sizes = [total_spent, remaining]
    labels = ["Spent", "Remaining"]
    colors = ["#FF6B6B", "#4ECDC4"]
    
    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        counterclock=False,
        colors=colors,
        wedgeprops=dict(width=0.3)  # This creates a donut chart
    )
    ax.set(aspect="equal")
    ax.set_title("Budget Distribution")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Example usage within your Streamlit app
# (Assuming 'spending_data' and 'spending_region' are already defined in your app)
region_spending = spending_data.get(spending_region, {})
display_budget_tracking(budget_goal, region_spending)
