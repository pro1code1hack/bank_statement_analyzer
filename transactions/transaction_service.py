import sqlite3

from typing import TypedDict


class Transaction(TypedDict):
    """
    A TypedDict for representing a transaction.

    Attributes:
        date (str): The date of the transaction in YYYY-MM-DD format.
        description (str): A brief description of the transaction.
        money_in (float): The amount of money credited in the transaction.
        money_out (float): The amount of money debited in the transaction.
        balance (float): The account balance after the transaction.
        type (str): The type of transaction (e.g., 'DEBIT', 'CREDIT').
    """
    date: str
    description: str
    money_in: float
    money_out: float
    balance: float
    type: str


class TransactionService:
    """
    Service class for handling transaction-related operations.
    """

    def __init__(self, db: sqlite3.Connection) -> None:
        """
        Initialize the TransactionService with a database connection.

        Args:
            db (sqlite3.Connection): Database connection object.
        """
        self.db = db

    def get_transactions_by_account(self, account_id: int) -> dict:
        """
        Retrieve transactions by account ID and group them by category.

        Args:
            account_id (int): The ID of the account to retrieve transactions for.

        Returns:
            dict: A dictionary with categories as keys and lists of transactions as values.
        """
        cursor = self.db.connection.cursor()
        cursor.execute("""
            SELECT * FROM transactions WHERE account_id = ?
        """, (account_id,))
        rows = cursor.fetchall()
        cursor.close()

        transactions_by_category = {}
        for row in rows:
            category = row["description"]

            if category not in transactions_by_category:
                transactions_by_category[category] = []

            transactions_by_category[category].append({
                "date": row["transaction_date"],
                "description": row["description"],
                "money_in": row["money_in"],
                "money_out": row["money_out"],
                "balance": row["balance"]
            })
        return transactions_by_category

    def add_transaction(self, account_id: int, date: str, description: str, money_in: float, money_out: float,
                        balance: float, category_id: int = 1) -> None:
        """
        Add a transaction to the database.

        Args:
            account_id (int): The account ID associated with the transaction.
            date (str): The date of the transaction.
            description (str): The description of the transaction.
            money_in (float): The amount of money in for the transaction.
            money_out (float): The amount of money out for the transaction.
            balance (float): The balance after the transaction.
            category_id (int, optional): The category ID of the transaction. Defaults to 1.
        """
        cursor = self.db.connection.cursor()
        cursor.execute("""
            INSERT INTO transactions (account_id, transaction_date, description, money_out, money_in, balance, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (account_id, date, description, money_out, money_in, balance, category_id))
        self.db.connection.commit()
        cursor.close()
