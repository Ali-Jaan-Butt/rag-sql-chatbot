from database import mysql_conn


class Create_insert_table:
    def __init__(self):
        self.conn, self.cursor = mysql_conn.sql_connection()
    def create_table_sql(self):
        self.create_table_query = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(50),
            phone VARCHAR(20),
            address VARCHAR(255),
            city VARCHAR(50),
            country VARCHAR(50),
            zip_code VARCHAR(10),
            bank_name VARCHAR(100),
            account_number VARCHAR(30),
            iban VARCHAR(34),
            swift_code VARCHAR(15),
            card_number VARCHAR(20),
            expiry_date VARCHAR(7),
            cvv CHAR(3),
            amount VARCHAR(100)
        );
        """
        self.cursor.execute(self.create_table_query)
        self.conn.commit()