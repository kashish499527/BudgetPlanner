# Budget Planner Pro

A modular, local-first personal finance tracker built with Python, Streamlit and SQLite.

## Features
- Register and login with salted PBKDF2 password hashing
- User-specific income and expense records
- Add, search, edit and delete transactions
- Monthly category budget limits with warning alerts
- Dashboard with financial summary and savings goal
- Date-filtered reports and CSV exports
- Separate modules for database, authentication, styling, business logic and screens

## Run in VS Code (Windows)
1. Extract this ZIP.
2. Open the `BudgetPlannerPro` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment (recommended):
   ```powershell
   py -3.13 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal or skip the virtual environment.
5. Install packages:
   ```powershell
   py -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   py -m streamlit run app.py
   ```
7. Open the local URL shown in the terminal, usually `http://localhost:8501`.

The SQLite database file `budget_planner.db` is created automatically the first time the app runs. Keep it private; it contains your local account and finance data.

## Project structure
```text
BudgetPlannerPro/
├── app.py
├── requirements.txt
├── README.md
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── auth.py
├── services/
│   ├── __init__.py
│   └── finance.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── styles.py
└── views/
    ├── __init__.py
    ├── dashboard.py
    ├── transactions.py
    ├── budgets.py
    ├── reports.py
    └── settings.py
```

## Notes
- This version is designed for local/offline use after the packages have been installed. Google Fonts may need internet access to load; the app works without them using fallback fonts.
- Passwords are not stored as plain text.
- This is a learning project, not a banking application. Back up the database file regularly.
