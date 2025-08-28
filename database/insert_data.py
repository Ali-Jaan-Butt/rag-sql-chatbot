from database.tables import Create_tables
import pandas as pd


class Insert_data:
    def __init__(self):
        obj = Create_tables()
        self.conn, self.cursor = obj.create_table_user()

    def insert_user_data(self):
        self.df = pd.read_sql("SELECT * FROM Users", self.conn)
        if self.df.empty:
            self.insert_query = """
            INSERT INTO Users
            (first_name, last_name, email, password, phone, address, city, country, zip_code, bank_name, account_number, iban, swift_code, card_number, expiry_date, cvv, amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            self.data = [
                ('Ali', 'Jaan', 'ali.jaan@example.com', 'abc123', '+923001234567', 'Street 123', 'Karachi', 'Pakistan', '74000',
                'HBL', '1234567890', 'PK36SCBL0000001123456702', 'HABBPKKA', '4111111111111111', '12/2026', '123', '3434123'),
                ('Sara', 'Khan', 'sara.khan@example.com', 'abcd1234', '+923004567890', 'Street 45', 'Lahore', 'Pakistan', '54000',
                'UBL', '9876543210', 'PK36SCBL0000001123456789', 'UNILPKKA', '4222222222222222', '07/2027', '456', '324544')
            ]

            self.cursor.executemany(self.insert_query, self.data)
            self.conn.commit()
            print('Data Inserted Successfully')
        self.conn.close()
        self.cursor.close()