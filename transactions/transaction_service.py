transactions_db = {}


class TransactionService:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def add_transaction(self, account_id, date, description, money_in, money_out, balance, category_id=1):
        cursor = self.db.connection.cursor()
        cursor.execute("""
            INSERT INTO transactions (account_id, transaction_date, description, money_out, money_in, balance, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (account_id, date, description, money_out, money_in, balance, category_id))
        self.db.connection.commit()
        cursor.close()
