import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.connection = self.connect()

    def connect(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            return conn
        except Error as e:
            print(e)
        return None

    def create_tables(self) -> None:
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                account_number TEXT NOT NULL,
                iban TEXT,
                bic TEXT,
                sort_code TEXT,
                balance REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS statements (
                statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                opening_balance REAL,
                closing_balance REAL,
                money_out REAL,
                money_in REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                transaction_date TEXT NOT NULL,
                description TEXT,
                money_out REAL,
                money_in REAL,
                balance REAL,
                category_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts (account_id),
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            );
            """
        ]
        cursor = self.connection.cursor()
        for table in tables:
            cursor.execute(table)
        self.connection.commit()
        cursor.close()
