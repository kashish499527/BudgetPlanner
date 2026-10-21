import hashlib
import hmac
import os
from database.db import get_connection

def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 260_000).hex()

def create_user(username, password):
    salt = os.urandom(16).hex()
    password_hash = _hash_password(password, salt)
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO users(username, password_hash, password_salt) VALUES(?,?,?)",
                (username, password_hash, salt)
            )
            conn.execute("INSERT OR IGNORE INTO savings_goals(user_id, goal_name, target_amount) VALUES(?,?,?)",
                         (cur.lastrowid, "My savings goal", 0))
        return True, "Account created successfully."
    except Exception as exc:
        if "UNIQUE" in str(exc):
            return False, "That username is already taken."
        return False, "Could not create account. Please try again."

def authenticate_user(username, password):
    with get_connection() as conn:
        row = conn.execute("SELECT id, username, password_hash, password_salt FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        return None
    candidate = _hash_password(password, row["password_salt"])
    if hmac.compare_digest(candidate, row["password_hash"]):
        return {"id": row["id"], "username": row["username"]}
    return None
