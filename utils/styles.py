import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --ink:#172033; --muted:#7b8498; --accent:#6558e8; --line:#e9ecf4; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:#f6f7fb; color:var(--ink); }
    [data-testid="stSidebar"] { background:#141a2d; border-right:1px solid #222941; }
    [data-testid="stSidebar"] * { color:#e8ebf7 !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] small { color:#9ca6c2 !important; letter-spacing:1.2px; font-size:10px; }
    [data-testid="stSidebar"] .stRadio label { padding:7px 10px; border-radius:9px; }
    [data-testid="stSidebar"] .stRadio label:hover { background:#222a44; }
    [data-testid="stSidebar"] button { border-radius:10px; }
    h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.6px; }
    h1 { font-weight:800 !important; }
    .sidebar-brand { display:flex; align-items:center; gap:11px; padding:12px 0 24px; }
    .brand-icon,.brand-mark { display:inline-flex; align-items:center; justify-content:center; background:#6b5ce7; border-radius:13px; width:42px; height:42px; font-size:23px; }
    .sidebar-brand b { display:block; font-size:15px; color:#fff; }
    .user-chip { background:#202842; border:1px solid #303a58; border-radius:10px; padding:10px 12px; margin:0 0 24px; font-size:13px; }
    .eyebrow { color:#7166df; text-transform:uppercase; font-size:11px; font-weight:700; letter-spacing:1.5px; margin-bottom:5px; }
    .page-subtitle { color:#858da1; margin-top:-8px; margin-bottom:24px; }
    .metric-card { background:white; border:1px solid #edf0f6; border-radius:16px; padding:20px 21px; box-shadow:0 5px 18px rgba(30,40,80,.025); min-height:122px; }
    .metric-label { color:#81899c; font-size:12px; font-weight:600; margin-bottom:12px; }
    .metric-value { color:#172033; font-size:27px; font-weight:800; font-family:'Manrope',sans-serif; letter-spacing:-.8px; }
    .metric-note { color:#9aa1b1; font-size:11px; margin-top:7px; }
    .panel { background:white; border:1px solid #edf0f6; border-radius:16px; padding:20px; }
    .auth-wrap { max-width:500px; margin:4vh auto 0; padding:34px; background:#fff; border:1px solid #edf0f6; border-radius:22px; box-shadow:0 18px 60px rgba(29,36,72,.08); }
    .auth-wrap .brand-mark { margin-bottom:14px; }
    .auth-title { font-size:32px; margin:0 !important; }
    .auth-title span { color:#6558e8; }
    .auth-subtitle { color:#858da1; margin:4px 0 26px; }
    .auth-foot { color:#a0a6b5; font-size:11px; text-align:center; margin-top:20px; }
    div.stButton > button, div.stFormSubmitButton > button { border-radius:10px; font-weight:600; min-height:42px; }
    div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] { background:#6558e8; border-color:#6558e8; }
    [data-testid="stMetric"] { background:white; border:1px solid #edf0f6; border-radius:14px; padding:16px; }
    [data-testid="stDataFrame"] { border:1px solid #edf0f6; border-radius:12px; overflow:hidden; }
    .stTabs [data-baseweb="tab-list"] { gap:12px; }
    .stTabs [data-baseweb="tab"] { padding:10px 16px; }
    @media (max-width: 700px) { .auth-wrap { margin:0; padding:22px; } .metric-value { font-size:22px; } }
    </style>
    """, unsafe_allow_html=True)
