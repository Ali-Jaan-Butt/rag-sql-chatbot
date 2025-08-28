from data import load_data
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os


def save_data():
    docs, db_docs = load_data.load_data()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    documents = text_splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db_path = "faiss_db_payment_method"
    if os.path.exists(db_path):
        db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    else:
        db = FAISS.from_documents(documents, embeddings)
        db.save_local(db_path)

    db_path_sql = "faiss_db_sql"
    if os.path.exists(db_path_sql):
        db_sql = FAISS.load_local(db_path_sql, embeddings, allow_dangerous_deserialization=True)
    else:
        db_sql = FAISS.from_documents(db_docs, embeddings)
        db_sql.save_local(db_path_sql)
    return db, db_sql