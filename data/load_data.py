from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
import pandas as pd
from database import mysql_conn


def load_data():
    conn, cursor = mysql_conn.sql_connection()
    loader = PyPDFLoader("/Users/hassanazhar/Downloads/payment_method.pdf")
    docs = loader.load()
    df = pd.read_sql("SELECT * FROM Users", conn)
    db_docs = []
    for _, row in df.iterrows():
        cols = df.columns.tolist()
        if len(cols) >= 2:
            question = str(row[cols[0]])
            answer = str(row[cols[1]])
            if question.strip() and answer.strip():
                content = f"Q: {question}\nA: {answer}"
                db_docs.append(Document(page_content=content, metadata={"source": "database"}))
    conn.close()
    cursor.close()
    return docs, db_docs