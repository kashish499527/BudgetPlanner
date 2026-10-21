import streamlit as st
import pandas as pd
from datetime import date
from services.finance import get_transactions
from utils.helpers import transactions_frame, money

def show_reports(user_id):
    st.markdown('<div class="eyebrow">INSIGHTS & TRENDS</div>', unsafe_allow_html=True)
    st.title("Reports")
    st.markdown('<div class="page-subtitle">Understand where your money comes from and where it goes.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    start = c1.date_input("Start date", value=date.today().replace(day=1), key="report_start")
    end = c2.date_input("End date", value=date.today(), key="report_end")
    df = transactions_frame(get_transactions(user_id, start, end))
    if df.empty:
        st.info("No transactions found in this date range.")
        return
    income = float(df.loc[df.kind=="Income","amount"].sum())
    expense = float(df.loc[df.kind=="Expense","amount"].sum())
    a,b,c = st.columns(3)
    a.metric("Income", money(income))
    b.metric("Expenses", money(expense))
    c.metric("Net", money(income-expense))
    left, right = st.columns(2)
    with left:
        st.markdown("### Expense by category")
        expenses = df[df.kind=="Expense"].groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
        if not expenses.empty:
            st.bar_chart(expenses.set_index("category"), color="#6558e8")
        else:
            st.caption("No expenses in this period.")
    with right:
        st.markdown("### Income vs expenses")
        summary = pd.DataFrame({"Type":["Income","Expense"],"Amount":[income,expense]})
        st.bar_chart(summary.set_index("Type"), color="#6558e8")
    st.markdown("### Monthly breakdown")
    df["month"] = pd.to_datetime(df["transaction_date"]).dt.to_period("M").astype(str)
    monthly = df.pivot_table(index="month", columns="kind", values="amount", aggfunc="sum", fill_value=0)
    st.line_chart(monthly)
    st.download_button("Export report as CSV", data=df.drop(columns=["user_id"], errors="ignore").to_csv(index=False).encode("utf-8"),
                       file_name="budget_report.csv", mime="text/csv")
