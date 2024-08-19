import sqlite3
from typing import Optional, Tuple
from db import Database
from auth.hash_service import check_password, hash_password
from transactions.app_get_transactions_for_period import get_transactions_execute
from transactions.bos_parser_test_app import execute_upload
from visualisation.visualisation import Visualizer

class UserService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.db = Database(db_path)
        self.transactions = None
        self.visualisation_report = Visualizer('main/directory')

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

    def display_bank_menu(self, user_id):
        print("\n--- Bank Menu ---")
        print("Please choose an option:")
        print("1. Create Account")
        print("2. Upload Bank Statement")
        print("3. View Transactions")
        print("4. Generate Report by Grouped Transactions (by categories)")
        print("5. Create visualization report for statement")
        print("6. Logout")

        choice = input("Select an option (1-5): ")
        if choice == "1":
            self.create_account(user_id)
            pass
        elif choice == "2":
            account_id = self.get_account_by_userID(user_id)
            file_path = input("Enter the path to the bank statement file: ").strip('"')
            execute_upload(self.db, file_path, account_id)
        elif choice == "3":
            account_id = self.get_account_by_userID(user_id)
            self.transactions = get_transactions_execute(self.db, account_id)
            pass
        elif choice == "4":
            self.visualisation_report.visualize_income_vs_expense(self.transactions)
        elif choice == "5":
            print("Logging out...")
            return False
        else:
            print("Invalid option. Please try again.")
            return True

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option (1-3): ")

            if choice == "1":
                print("\n--- Register ---")
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                self.register_user(name, email, password)

            elif choice == "2":
                print("\n--- Login ---")
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                user_id = self.login_user(email, password)
                if user_id:
                    running = True
                    while running:
                        running = self.display_bank_menu(user_id)
            elif choice == "3":
                print("Exiting...")
                self.conn.close()
                break

            else:
                print("Invalid option. Please try again.")

