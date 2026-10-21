import streamlit as st
from services.finance import get_goal, save_goal
from utils.helpers import money

def show_settings(user_id, username):
    st.markdown('<div class="eyebrow">PREFERENCES</div>', unsafe_allow_html=True)
    st.title("Settings")
    st.markdown('<div class="page-subtitle">Personalize your savings target and review account details.</div>', unsafe_allow_html=True)
    st.markdown("### Account")
    st.text_input("Username", value=username, disabled=True)
    st.caption("Your account and transactions are stored in the local SQLite database on this computer.")
    st.divider()
    st.markdown("### Savings goal")
    goal = get_goal(user_id)
    with st.form("goal_form"):
        name = st.text_input("Goal name", value=goal["goal_name"])
        target = st.number_input("Target amount (₹)", min_value=0.0, value=float(goal["target_amount"] or 0), step=500.0)
        saved = st.form_submit_button("Save savings goal", use_container_width=True)
    if saved:
        save_goal(user_id, name, target)
        st.success("Savings goal updated.")
        st.rerun()
    st.divider()
    st.markdown("### About")
    st.write("Budget Planner Pro is a local-first personal finance tracker built with Python, Streamlit and SQLite.")
    st.caption("Tip: Keep a backup of the budget_planner.db file to preserve your records.")
