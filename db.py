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
            raise e
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
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
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
            """
        ]
        cursor = self.connection.cursor()
        for table in tables:
            cursor.execute(table)
        self.connection.commit()
        cursor.close()

    def insert_users(self, users):
        insert_sql = """
            INSERT INTO users (name, email, password) VALUES (?, ?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(insert_sql, [(user['name'], user['email'], user['password']) for user in users])
            self.connection.commit()
        except Error as e:
            raise e
        finally:
            cursor.close()
    
    def insert_accounts(self, accounts):
        insert_sql = """
            INSERT INTO accounts (user_id, account_number, iban, bic, sort_code, balance) VALUES (?, ?, ?, ?, ?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(insert_sql, [(account['user_id'], account['account_number'], account['iban'], account['bic'], account['sort_code'], account['balance']) for account in accounts])
            self.connection.commit()
        except Error as e:
            raise e
        finally:
            cursor.close()
    
    def insert_statements(self, statements):
        insert_sql = """
            INSERT INTO statements(account_id, start_date, end_date, opening_balance, closing_balance, money_out, money_in) VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(insert_sql, [(statement['account_id'], statement['start_date'], statement['end_date'], statement['opening_balance'], statement['closing_balance'], statement['money_out'], statement['money_in']) for statement in statements])
            self.connection.commit()
        except Error as e:
            raise e
        finally:
            cursor.close()

    def insert_categories(self, categories):
        insert_sql = """
            INSERT INTO categories (name, description) VALUES (?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(insert_sql, [(category['name'], category['description']) for category in categories])
            self.connection.commit()
        except Error as e:
            raise e
        finally:
            cursor.close()

    def insert_transactions(self, transactions):
        insert_sql = """
            INSERT INTO transactions (account_id, transaction_date, description, money_out, money_in, balance, category_id) VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(insert_sql, [(transaction['account_id'], transaction['date'], transaction['description'], transaction['money_out'], transaction['money_in'], transaction['balance'], transaction['category_id']) for transaction in transactions])
            self.connection.commit()
        except Error as e:
            raise e
        finally:
            cursor.close()