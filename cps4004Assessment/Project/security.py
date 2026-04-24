import hashlib
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect('northshore.db')
    cur = conn.cursor()
    cur.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    conn.close()

    if result:
        stored_hash = result[0]
        role = result[1]

        if stored_hash == hash_password(password):
            return role

    return None

def log_login_attempt(username, action):
    conn = sqlite3.connect('northshore.db')
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    if result:
        user_id = result[0]
    else:
        user_id = 0

    cur.execute("INSERT INTO audit_log(user_id, action, table_name, record_id) VALUES (?, ?, ?, ?)", (user_id, action, "users", 0))
    conn.commit()
    conn.close()
