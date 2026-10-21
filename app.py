import streamlit as st
from database.db import init_db
from database.auth import authenticate_user, create_user
from utils.styles import load_css
from views.dashboard import show_dashboard
from views.transactions import show_transactions
from views.budgets import show_budgets
from views.reports import show_reports
from views.settings import show_settings

st.set_page_config(page_title="Budget Planner Pro", page_icon="💠", layout="wide", initial_sidebar_state="expanded")
init_db()
load_css()

def logout():
    for key in ("user_id", "username", "page"):
        st.session_state.pop(key, None)
    st.rerun()

def login_screen():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="brand-mark">💠</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">Budget Planner <span>Pro</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">A calmer way to manage your money.</p>', unsafe_allow_html=True)
    login_tab, signup_tab = st.tabs(["Sign in", "Create account"])
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            user = authenticate_user(username.strip(), password)
            if user:
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.rerun()
            else:
                st.error("Username or password is incorrect.")
    with signup_tab:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username", placeholder="At least 3 characters")
            new_password = st.text_input("Create password", type="password", placeholder="At least 8 characters")
            confirm = st.text_input("Confirm password", type="password")
            submitted_signup = st.form_submit_button("Create account", use_container_width=True)
        if submitted_signup:
            if len(new_username.strip()) < 3:
                st.error("Username must contain at least 3 characters.")
            elif len(new_password) < 8:
                st.error("Use a password with at least 8 characters.")
            elif new_password != confirm:
                st.error("Passwords do not match.")
            else:
                ok, message = create_user(new_username.strip(), new_password)
                if ok:
                    st.success(message + " You can now sign in.")
                else:
                    st.error(message)
    st.markdown('<p class="auth-foot">Your finances stay in your local database.</p></div>', unsafe_allow_html=True)

if "user_id" not in st.session_state:
    login_screen()
    st.stop()

with st.sidebar:
    st.markdown('<div class="sidebar-brand"><span class="brand-icon">💠</span><div><b>Budget Planner</b><small>PERSONAL FINANCE</small></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-chip">👤 &nbsp; {st.session_state.username}</div>', unsafe_allow_html=True)
    st.markdown("### Workspace")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Transactions", "Budget Limits", "Reports", "Settings"],
        label_visibility="collapsed",
        format_func=lambda x: {"Dashboard":"▦  Dashboard", "Transactions":"⇄  Transactions", "Budget Limits":"◎  Budget limits", "Reports":"▤  Reports", "Settings":"⚙  Settings"}[x],
    )
    st.divider()
    st.caption("LOCAL • PRIVATE • SIMPLE")
    if st.button("↪  Log out", use_container_width=True):
        logout()

if page == "Dashboard":
    show_dashboard(st.session_state.user_id, st.session_state.username)
elif page == "Transactions":
    show_transactions(st.session_state.user_id)
elif page == "Budget Limits":
    show_budgets(st.session_state.user_id)
elif page == "Reports":
    show_reports(st.session_state.user_id)
else:
    show_settings(st.session_state.user_id, st.session_state.username)
