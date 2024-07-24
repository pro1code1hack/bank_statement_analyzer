from sqlite3 import Error
import pandas as pd

class TransactionService:

    def __init__(self, db):
        self.db = db

    def get_data_period(self, start_day, end_day):
        insert_sql = """
            SELECT 
                t.transaction_id,
                t.transaction_date,
                t.description,
                t.money_out,
                t.money_in,
                t.balance,
                a.account_number,
                c.name
            FROM 
                transactions t
            JOIN 
                accounts a ON t.account_id = a.account_id
            JOIN 
                categories c ON t.category_id = c.category_id
            WHERE t.transaction_date 
            BETWEEN ? AND ?;
        """
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(insert_sql, [start_day, end_day])
            result = cursor.fetchall()
            print(result)
            return result
        except Error as e:
            print(e)
        finally:
            cursor.close()

    def convert_to_pd(self, dataset):
        df = pd.DataFrame(dataset)
        df.columns = [
            "ID",
            "Date",
            "Description",
            "Money_out",
            "Money_in",
            "Balance",
            "Account number",
            "Category name"
        ]
        return df
  
