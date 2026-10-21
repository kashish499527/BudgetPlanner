import streamlit as st
import pandas as pd
from datetime import date, timedelta
from services.finance import add_transaction, get_transactions, update_transaction, delete_transaction
from utils.helpers import CATEGORIES, money, transactions_frame

def show_transactions(user_id):
    st.markdown('<div class="eyebrow">MONEY MOVEMENT</div>', unsafe_allow_html=True)
    st.title("Transactions")
    st.markdown('<div class="page-subtitle">Record, search, edit and manage every transaction.</div>', unsafe_allow_html=True)
    add_tab, manage_tab = st.tabs(["＋ Add transaction", "Manage transactions"])
    with add_tab:
        with st.form("add_transaction_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            kind = c1.selectbox("Transaction type", ["Expense", "Income"])
            amount = c2.number_input("Amount (₹)", min_value=1.0, step=100.0, format="%.2f")
            category = st.selectbox("Category", CATEGORIES[kind])
            description = st.text_input("Description (optional)", placeholder="e.g. Monthly groceries")
            tx_date = st.date_input("Date", value=date.today())
            saved = st.form_submit_button("Save transaction", use_container_width=True)
        if saved:
            add_transaction(user_id, kind, amount, category, description, tx_date)
            st.success("Transaction saved.")
            st.rerun()
    with manage_tab:
        all_rows = get_transactions(user_id)
        df = transactions_frame(all_rows)
        if df.empty:
            st.info("No transactions yet.")
        else:
            c1, c2, c3 = st.columns([1,1,1.4])
            kind_filter = c1.selectbox("Type", ["All","Income","Expense"])
            start = c2.date_input("From", value=date.today()-timedelta(days=30), key="filter_start")
            end = c3.date_input("To", value=date.today(), key="filter_end")
            search = st.text_input("Search category or description", placeholder="Type to search...")
            filtered = transactions_frame(get_transactions(user_id, start, end, kind_filter, search))
            st.dataframe(filtered[["id","transaction_date","kind","category","description","amount"]], use_container_width=True, hide_index=True)
            ids = [int(x) for x in filtered["id"].tolist()]
            if ids:
                selected_id = st.selectbox("Choose a transaction to edit or delete", ids, format_func=lambda x: f"#{x} · {filtered.loc[filtered.id==x, 'transaction_date'].iloc[0]} · {filtered.loc[filtered.id==x, 'category'].iloc[0]}")
                current = filtered[filtered.id == selected_id].iloc[0]
                with st.expander("Edit selected transaction"):
                    with st.form(f"edit_{selected_id}"):
                        new_kind = st.selectbox("Type", ["Expense","Income"], index=["Expense","Income"].index(current.kind))
                        new_amount = st.number_input("Amount (₹)", min_value=1.0, value=float(current.amount), step=100.0)
                        new_category = st.selectbox("Category", CATEGORIES[new_kind], index=CATEGORIES[new_kind].index(current.category) if current.category in CATEGORIES[new_kind] else 0)
                        new_desc = st.text_input("Description", value=str(current.description or ""))
                        new_date = st.date_input("Date", value=date.fromisoformat(str(current.transaction_date)))
                        update = st.form_submit_button("Save changes", use_container_width=True)
                    if update:
                        update_transaction(user_id, selected_id, new_kind, new_amount, new_category, new_desc, new_date)
                        st.success("Transaction updated.")
                        st.rerun()
                if st.button("Delete selected transaction", type="secondary"):
                    st.session_state["confirm_delete_tx"] = selected_id
                if st.session_state.get("confirm_delete_tx") == selected_id:
                    st.warning("Delete this transaction permanently?")
                    a, b = st.columns(2)
                    if a.button("Yes, delete", type="primary"):
                        delete_transaction(user_id, selected_id)
                        st.session_state.pop("confirm_delete_tx", None)
                        st.rerun()
                    if b.button("Cancel"):
                        st.session_state.pop("confirm_delete_tx", None)
                        st.rerun()
            csv = df.drop(columns=["user_id"], errors="ignore").to_csv(index=False).encode("utf-8")
            st.download_button("Download all transactions as CSV", data=csv, file_name="transactions.csv", mime="text/csv")
