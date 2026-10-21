import streamlit as st
from datetime import date
from services.finance import get_budgets, save_budget, delete_budget, get_transactions
from utils.helpers import CATEGORIES, money, transactions_frame

def show_budgets(user_id):
    st.markdown('<div class="eyebrow">SPENDING GUARDRAILS</div>', unsafe_allow_html=True)
    st.title("Budget limits")
    st.markdown('<div class="page-subtitle">Set category-wise limits and keep an eye on your spending.</div>', unsafe_allow_html=True)
    month = st.date_input("Choose month", value=date.today().replace(day=1), key="budget_month").strftime("%Y-%m")
    with st.form("budget_limit_form"):
        c1, c2 = st.columns(2)
        category = c1.selectbox("Expense category", CATEGORIES["Expense"])
        amount = c2.number_input("Monthly limit (₹)", min_value=1.0, step=500.0)
        saved = st.form_submit_button("Save budget limit", use_container_width=True)
    if saved:
        save_budget(user_id, month, category, amount)
        st.success("Budget limit saved.")
        st.rerun()
    budgets = get_budgets(user_id, month)
    rows = get_transactions(user_id, start=f"{month}-01", end=f"{month}-31", kind="Expense")
    df = transactions_frame(rows)
    spent = df.groupby("category")["amount"].sum().to_dict() if not df.empty else {}
    st.markdown("### Your limits")
    if not budgets:
        st.info("No limits for this month yet.")
    for b in budgets:
        limit = float(b["amount"])
        used = float(spent.get(b["category"], 0))
        ratio = used / limit if limit else 0
        st.markdown(f"**{b['category']}**")
        st.progress(min(ratio, 1), text=f"{money(used)} spent of {money(limit)} ({ratio*100:.0f}%)")
        if ratio >= 1:
            st.error("Limit reached or exceeded.")
        elif ratio >= .8:
            st.warning("You have used 80% or more of this limit.")
        c1, c2 = st.columns([5,1])
        c1.caption(f"Remaining: {money(max(limit-used, 0))}")
        if c2.button("Remove", key=f"remove_budget_{b['id']}"):
            delete_budget(user_id, b["id"])
            st.rerun()
