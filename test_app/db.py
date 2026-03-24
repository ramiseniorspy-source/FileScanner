import sqlite3

def execute_query(user_query):
    # This is a critical vulnerability: Raw SQL execution without parameterization
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{user_query}'")
    return cursor.fetchall()
