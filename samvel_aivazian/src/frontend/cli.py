import os

from samvel_aivazian.src.backend.auth.service.auth_service import register, login, logout, get_current_user
from samvel_aivazian.src.backend.bank_statement.parser.bank_of_scotland_parser import BankOfScotlandParser
from samvel_aivazian.src.backend.report.service.report_service import generate_report
from samvel_aivazian.src.backend.transaction.service.transaction_service import get_transactions, add_transaction, \
    get_transactions_grouped_by_category


def display_not_logged_in_menu():
    print("Please choose an option:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")


def display_logged_in_menu(current_user):
    print(f"Welcome, {current_user}! Please choose an option:")
    print("1. Upload Bank Statement")
    print("2. View Transactions")
    print("3. Generate Report by grouped Transactions (by categories)")
    print("4. Logout")


def register_handler():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        register(email, password)
    except ValueError as e:
        print(e)

    return True


def login_handler():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    login(email, password)

    return True


def exit_handler():
    print("Exiting...")
    return False


def upload_bank_statement_handler(current_user):
    file_path = input("Enter the path to the bank statement file: ").strip('"')
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return True

    parser = BankOfScotlandParser()
    transactions = parser.parse(file_path)

    for transaction in transactions:
        add_transaction(
            current_user,
            transaction["date"],
            transaction["description"],
            transaction["money_in"],
            transaction["money_out"],
            transaction["type"],
            transaction["balance"]
        )

    print("Bank statement uploaded and transactions added.")
    return True


def view_transactions_handler(current_user):
    start_date = input("Enter the start date (YYYY-MM-DD) or leave blank for no start date: ")
    end_date = input("Enter the end date (YYYY-MM-DD) or leave blank for no end date: ")

    transactions = get_transactions(current_user, start_date, end_date)

    if transactions:
        print(f"Transactions for {current_user}:")

        for transaction in transactions:
            print(
                f"Date: {transaction['date']}, "
                f"Description: {transaction['description']}, "
                f"Money In: {transaction['money_in']}, "
                f"Money Out: {transaction['money_out']}, "
                f"Type: {transaction['type']}, "
                f"Balance: {transaction['balance']}"
            )
    else:
        print("No transactions found for the given period.")
    return True


def generate_report_by_category_handler(current_user):
    start_date = input("Enter the start date (YYYY-MM-DD) or leave blank for no start date: ")
    end_date = input("Enter the end date (YYYY-MM-DD) or leave blank for no end date: ")
    export_format = input("Enter export format (console/graphical/csv/json): ").strip().lower()

    transactions_by_category = get_transactions_grouped_by_category(current_user, start_date, end_date)
    generate_report(transactions_by_category, export_format=export_format)
    return True


def logout_handler():
    logout()
    return True


not_logged_in_handlers = {
    '1': register_handler,
    '2': login_handler,
    '3': exit_handler,
}

logged_in_handlers = {
    '1': upload_bank_statement_handler,
    '2': view_transactions_handler,
    '3': generate_report_by_category_handler,
    '4': logout_handler,
}


def handle_not_logged_in_choice(choice):
    handler = not_logged_in_handlers.get(choice)
    if handler:
        return handler()
    else:
        print("Invalid choice, please try again.")
        return True


def handle_logged_in_choice(choice, current_user):
    handler = logged_in_handlers.get(choice)
    if handler:
        return handler(current_user)
    else:
        print("Invalid choice, please try again.")
        return True


def main_menu():
    while True:
        current_user = get_current_user()
        if current_user is None:
            display_not_logged_in_menu()
            choice = input("> ")
            if not handle_not_logged_in_choice(choice):
                break
        else:
            display_logged_in_menu(current_user)
            choice = input("> ")
            if not handle_logged_in_choice(choice, current_user):
                break


if __name__ == '__main__':
    main_menu()
