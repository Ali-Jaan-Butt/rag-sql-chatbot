import pandas as pd
from database import mysql_conn


def verify_credentials(email, password):
    conn, cursor = mysql_conn.sql_connection()
    query = f"SELECT * FROM Users WHERE email='{email}' AND password='{password}' LIMIT 1;"
    try:
        user_data = pd.read_sql(query, conn)
        if not user_data.empty:
            return True, user_data.to_dict(orient="records")[0]
        return False, None
    except Exception as e:
        print("Login verification error:", e)
        return False, None