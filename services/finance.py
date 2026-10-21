from database.db import get_connection

def add_transaction(user_id, kind, amount, category, description, date):
    with get_connection() as conn:
        conn.execute("INSERT INTO transactions(user_id,kind,amount,category,description,transaction_date) VALUES(?,?,?,?,?,?)",
                     (user_id, kind, float(amount), category, description.strip(), str(date)))

def get_transactions(user_id, start=None, end=None, kind=None, search=None):
    sql = "SELECT id, user_id, kind, amount, category, description, transaction_date FROM transactions WHERE user_id=?"
    params = [user_id]
    if start:
        sql += " AND transaction_date >= ?"; params.append(str(start))
    if end:
        sql += " AND transaction_date <= ?"; params.append(str(end))
    if kind and kind != "All":
        sql += " AND kind=?"; params.append(kind)
    if search:
        sql += " AND (category LIKE ? OR description LIKE ?)"; params.extend([f"%{search}%", f"%{search}%"])
    sql += " ORDER BY transaction_date DESC, id DESC"
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()

def update_transaction(user_id, tx_id, kind, amount, category, description, date):
    with get_connection() as conn:
        conn.execute("UPDATE transactions SET kind=?, amount=?, category=?, description=?, transaction_date=? WHERE id=? AND user_id=?",
                     (kind, float(amount), category, description.strip(), str(date), int(tx_id), user_id))

def delete_transaction(user_id, tx_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (int(tx_id), user_id))

def get_budgets(user_id, month):
    with get_connection() as conn:
        return conn.execute("SELECT id, category, amount FROM budgets WHERE user_id=? AND month=? ORDER BY category", (user_id, month)).fetchall()

def save_budget(user_id, month, category, amount):
    with get_connection() as conn:
        conn.execute("""INSERT INTO budgets(user_id,month,category,amount) VALUES(?,?,?,?)
        ON CONFLICT(user_id,month,category) DO UPDATE SET amount=excluded.amount""",
        (user_id, month, category, float(amount)))

def delete_budget(user_id, budget_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM budgets WHERE id=? AND user_id=?", (int(budget_id), user_id))

def get_goal(user_id):
    with get_connection() as conn:
        row = conn.execute("SELECT goal_name,target_amount FROM savings_goals WHERE user_id=?", (user_id,)).fetchone()
        return dict(row) if row else {"goal_name":"My savings goal","target_amount":0}

def save_goal(user_id, name, amount):
    with get_connection() as conn:
        conn.execute("""INSERT INTO savings_goals(user_id,goal_name,target_amount) VALUES(?,?,?)
        ON CONFLICT(user_id) DO UPDATE SET goal_name=excluded.goal_name,target_amount=excluded.target_amount""",
        (user_id, name.strip() or "My savings goal", float(amount)))
