from database import mysql_conn

try:
    conn, cursor = mysql_conn.sql_connection()
    print("DB connection successful")
except Exception as e:
    print("DB connection failed:", e)
