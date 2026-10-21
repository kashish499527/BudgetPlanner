import pandas as pd

CATEGORIES = {
    "Expense": ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Entertainment", "Rent", "Other"],
    "Income": ["Salary", "Freelance", "Business", "Scholarship", "Gift", "Other"],
}

def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"

def transactions_frame(rows):
    return pd.DataFrame([dict(r) for r in rows]) if rows else pd.DataFrame(
        columns=["id", "user_id", "kind", "amount", "category", "description", "transaction_date"]
    )
