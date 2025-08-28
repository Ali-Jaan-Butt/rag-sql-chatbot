import pymysql
from dotenv import load_dotenv
import os

def sql_connection():
    load_dotenv()
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db = os.getenv("DB_NAME")

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db,
        connect_timeout=60,
    )
    cursor = conn.cursor()
    print("Connection created successfully")
    return conn, cursor
