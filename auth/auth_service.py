import sqlite3
from typing import Optional, Tuple
from db import Database
from auth.hash_service import check_password, hash_password
from transactions.app_get_transactions_for_period import get_transactions_execute
from transactions.bos_parser_test_app import execute_upload


class UserService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.db = Database(db_path)

    def display_menu(self):
        print("\nWelcome to Bank Statement Parser!")
        print("\nPlease choose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

    def register_user(self, name: str, email: str, password: str) -> bool:
        try:
            hashed_password = hash_password(password)
            query = """
            INSERT INTO users (name, email, password) VALUES (?, ?, ?);
            """
            self.conn.execute(query, (name, email, hashed_password))
            self.conn.commit()
            print("User registered successfully!")
            return True
        except sqlite3.IntegrityError:
            print("Error: Email already exists!")
            return False

    def login_user(self, email: str, password: str) -> Optional[int]:
        query = """
        SELECT user_id, password FROM users WHERE email = ?;
        """
        cursor = self.conn.execute(query, (email,)) 
        user = cursor.fetchone()

        if user:  
            hashed_password = user[1]  
            if check_password(hashed_password, password):
                print("Login successful!")
                cursor.close()
                return user[0]  
            else:
                print("Login failed: Incorrect email or password.")
                cursor.close()
                return None
        else:
            print("Login failed: User not found.")
            cursor.close()
            return None
        
    def find_existing_account(self, account_number: Optional[str] = None, iban: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Check if an account exists based on account number or IBAN and return the account details.

        :param account_number: The account number to check.
        :param iban: The IBAN to check.
        :return: A tuple (account_number, iban) if the account exists, None otherwise.
        """
        query_check = """
        SELECT account_number, iban FROM accounts WHERE account_number = ? OR iban = ?;
        """
        cursor = self.conn.cursor()
        cursor.execute(query_check, (account_number, iban))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result
        return None
    
    def get_account_by_userID(self, user_id: int) -> Optional[int]:
        get_id = """
        SELECT account_id FROM accounts WHERE user_id = ? ;
        """
        cursor = self.conn.cursor()
        cursor.execute(get_id, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        return None
    
    def create_account(self, user_id: int) -> bool:
        account_number = input("Account number: ")
        iban = input("IBAN: ")
        bic = input("BIC: ")
        sort_code = input("Sort code: ")
        balance = input("Balance: ")

        existing_account = self.find_existing_account(account_number=account_number, iban=iban)
        if existing_account:
            print(f"Error: Account with account_number {existing_account[0]} or IBAN {existing_account[1]} already exists!")
            return False
        try:
            query_insert = """
            INSERT INTO accounts (user_id, account_number, iban, bic, sort_code, balance) 
            VALUES (?, ?, ?, ?, ?, ?);
            """
            self.conn.execute(query_insert, (user_id, account_number, iban, bic, sort_code, balance))
            self.conn.commit()
            print("Account created successfully!")
            return True
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        
