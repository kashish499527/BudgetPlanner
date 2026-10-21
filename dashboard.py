import streamlit as st
import pandas as pd
from datetime import date
from services.finance import get_transactions, get_budgets, get_goal
from utils.helpers import money, transactions_frame

def show_dashboard(user_id, username):
    today = date.today()
    st.markdown('<div class="eyebrow">PERSONAL FINANCE WORKSPACE</div>', unsafe_allow_html=True)
    st.title(f"Welcome back, {username} 👋")
    st.markdown('<div class="page-subtitle">Make every rupee count. Here is your financial snapshot.</div>', unsafe_allow_html=True)
    rows = get_transactions(user_id, start=today.replace(day=1), end=today)
    df = transactions_frame(rows)
    income = float(df.loc[df.kind == "Income", "amount"].sum()) if not df.empty else 0
    expenses = float(df.loc[df.kind == "Expense", "amount"].sum()) if not df.empty else 0
    balance = income - expenses
    cols = st.columns(3)
    metrics = [("TOTAL INCOME", money(income), "This month"), ("TOTAL EXPENSES", money(expenses), "This month"), ("NET BALANCE", money(balance), "Income minus expenses")]
    for col, (label, value, note) in zip(cols, metrics):
        col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.6, 1])
    with left:
        st.markdown("### Cash flow")
        if df.empty:
            st.info("No transactions for this month yet. Add your first transaction to see your cash flow.")
        else:
            chart = df.groupby("kind", as_index=False)["amount"].sum()
            st.bar_chart(chart.set_index("kind"), color="#6558e8", height=250)
    with right:
        st.markdown("### Savings goal")
        goal = get_goal(user_id)
        target = float(goal["target_amount"] or 0)
        st.markdown(f"**{goal['goal_name']}**")
        if target > 0:
            progress = min(max(balance / target, 0), 1)
            st.progress(progress, text=f"{progress*100:.0f}% of target")
            st.caption(f"{money(max(balance, 0))} current monthly net · {money(target)} target")
        else:
            st.caption("Set a target in Settings to start tracking your goal.")
        st.markdown("### Budget check")
        month = today.strftime("%Y-%m")
        budgets = get_budgets(user_id, month)
        if not budgets:
            st.caption("No monthly limits set yet.")
        else:
            expenses_by_cat = df[df.kind == "Expense"].groupby("category")["amount"].sum().to_dict() if not df.empty else {}
            for b in budgets[:4]:
                spent = float(expenses_by_cat.get(b["category"], 0))
                pct = min(spent / float(b["amount"]), 1) if float(b["amount"]) else 0
                st.caption(f"{b['category']} · {money(spent)} / {money(b['amount'])}")
                st.progress(pct)
    st.markdown("### Recent transactions")
    if df.empty:
        st.info("Your latest activity will appear here.")
    else:
        show = df.head(6)[["transaction_date","kind","category","description","amount"]].copy()
        show["amount"] = show.apply(lambda r: ("+" if r["kind"]=="Income" else "−") + money(r["amount"]), axis=1)
        show.columns = ["Date","Type","Category","Description","Amount"]
        st.dataframe(show, use_container_width=True, hide_index=True)
