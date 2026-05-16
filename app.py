import streamlit as st
from bakery_logic import calculate_results
from storage import save_entry, get_recent_entries

st.title("Bakery Pay & Profit Calculator")

# -------------------------
# Orders Section
# -------------------------
st.header("Order Info")

order_name = st.text_input("Order name (optional)", placeholder="e.g. Birthday cookies")

st.header("Orders")

orders = []

num_orders = st.number_input("Number of cookie types", min_value=1, max_value=10, value=1)

for i in range(num_orders):
    st.subheader(f"Cookie Type {i+1}")
    num = st.number_input(f"Quantity #{i+1}", min_value=0, step=1)
    price = st.number_input(f"Price per cookie #{i+1}", min_value=0.0)
    orders.append((num, price))

# -------------------------
# Work Info
# -------------------------
hours = st.number_input("Hours worked", min_value=0.0)

# -------------------------
# Costs
# -------------------------
st.header("Cost Settings")

# Default values
DEFAULT_BATCH_SIZE = 40
ICED_BATCH_COST = 15.15
NAKED_BATCH_COST = 6.80

# Choose cookie type
iced = st.checkbox("Cookies have icing?")

# Option to override
override = st.checkbox("Update batch cost or size?")

batch_size = DEFAULT_BATCH_SIZE

if iced:
    batch_cost = ICED_BATCH_COST
else:
    batch_cost = NAKED_BATCH_COST

# Custom override
if override:
    batch_size = st.number_input("Cookies per batch", min_value=1, value=DEFAULT_BATCH_SIZE)
    batch_cost = st.number_input("Cost per batch ($)", min_value=0.0, value=batch_cost)

# Calculate cost per cookie
cost_per_cookie = batch_cost / batch_size

# -------------------------
# Additional Costs
# -------------------------
st.header("Additional Costs")

add_extra = st.checkbox("Include additional costs (packaging, etc.)")

extra_cost = 0.0

if add_extra:
    extra_cost = st.number_input("Additional total cost ($)", min_value=0.0)

# -------------------------
# Target Wage
# -------------------------
target = st.number_input("Target hourly wage (optional)", min_value=0.0)

# -------------------------
# Calculate Button
# -------------------------
if st.button("Calculate"):
    results = calculate_results(orders, hours, cost_per_cookie, False, 0)
    # Add extra costs
    results["cost"] += extra_cost
    results["profit"] = results["revenue"] - results["cost"]

    # Recalculate hourly rate after extra costs
    results["hourly_rate"] = results["profit"] / hours if hours > 0 else 0

    st.header("Results")

    st.write(f"**Total cookies:** {results['cookies']}")
    st.write(f"**Revenue:** ${results['revenue']:.2f}")
    st.write(f"**Cost:** ${results['cost']:.2f}")
    st.write(f"**Profit:** ${results['profit']:.2f}")
    st.write(f"**Hourly rate:** ${results['hourly_rate']:.2f}/hr")
    if extra_cost > 0:
        st.write(f"**Additional costs:** ${extra_cost:.2f}")

    # ✅ Required price per cookie
    if target > 0 and results["cookies"] > 0:
        required_total = target * hours + results["cost"]
        required_price = required_total / results["cookies"]

        st.write("### 💡 Pricing Insight")
        st.write(f"To earn ${target:.2f}/hr, you should charge about:")
        st.success(f"${required_price:.2f} per cookie")

    # ✅ Target check
    if target > 0:
        if results['hourly_rate'] < target:
            st.error("⚠️ Below target hourly wage")
        else:
            st.success("✅ Meeting target hourly wage")

    # ✅ Save results with name + hours
    results["name"] = order_name if order_name else "Unnamed Order"
    results["hours"] = hours

    save_entry(results)

# -------------------------
# Summary Section
# -------------------------
st.header("📅 Last 14 Days Summary")

entries = get_recent_entries(14)

if entries:
    total_profit = sum(e["profit"] for e in entries)
    total_hours = sum(e.get("hours", 0) for e in entries)

    st.write(f"**Total profit:** ${total_profit:.2f}")
    st.write(f"**Total hours worked:** {total_hours:.2f}")

    # ✅ Bonus: actual hourly earned
    if total_hours > 0:
        avg_rate = total_profit / total_hours
        st.write(f"**Actual hourly earned:** ${avg_rate:.2f}/hr")

    # ✅ Paycheck based on hours
    if target > 0 and total_hours > 0:
        paycheck = target * total_hours
        remaining = total_profit - paycheck

        st.write(f"**Suggested paycheck:** ${paycheck:.2f}")
        st.write(f"**Remaining business profit:** ${remaining:.2f}")

        if remaining < 0:
            st.error("⚠️ Warning: Paying more than total profit!")

    st.subheader("History")

    for e in entries:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"**{e.get('name', 'Unnamed')}** "
                f"({e['date']}) — Profit: ${e['profit']:.2f}, "
                f"Hourly: ${e['hourly_rate']:.2f}/hr"
            )

        with col2:
            entry_id = e.get("id", None)

            if entry_id:
                if st.button("Delete", key=f"delete_{entry_id}"):
                    from storage import delete_entry
                    delete_entry(entry_id)
                    st.success("Entry deleted ✅")
                    st.rerun()
            else:
                st.write("(Old entry)")

else:
    st.write("No recent data yet.")
# python -m streamlit run app.py
# 
# After making changes:
# git add .
# git commit -m "Fix something"
# git push
