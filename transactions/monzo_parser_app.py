import os

from db import Database
from transactions.parsers.bank_monzo_parser import MonzoBankParser
from transactions.transaction_service import TransactionService
from reports.data_helper import prepare_expense_data, prepare_income_data
from reports.report_service import ReportService


def initialize_db():
    db = Database('bankdb.sqlite')
    db.create_tables()
    return db

def parse_bank_statement(file_path, start_line):
    parser = MonzoBankParser()
    text = parser.parse_pdf(file_path, start_line)
    dates = parser.extract_dates(text)
    amounts_balances = parser.extract_amounts_balances(text)
    return parser.extract_transactions(text, dates, amounts_balances)

def insert_to_database(db, transactions, account_id):
    transaction_service = TransactionService(db)

    for transaction in transactions:
        transaction_service.add_transaction(
            account_id=account_id,
            date=transaction["date"],
            description=transaction["description"],
            money_in=transaction["money_in"],
            money_out=transaction["money_out"],
            balance=transaction["balance"],
            category_id=1
        )

def generate_and_print_report(db, account_id, output_dir="bank_monzo"):
    transaction_service = TransactionService(db)
    report_service = ReportService()

    trans = transaction_service.get_transactions_by_account(account_id)

    expense_df = prepare_expense_data(trans)
    income_df = prepare_income_data(trans)

    report_service.generate_report(trans, output_dir, "csv")

    report_service.generate_report(trans, output_dir, "json")

    print("Expenses:")
    print(expense_df.to_string(index=False))
    print("\nIncomes:")
    print(income_df.to_string(index=False))


if __name__ == "__main__":
    db = initialize_db()

    account_id = 1
    start_line ="Amount (GBP) Balance"
    output_dir = "monzo_bank"

    file_path = input("Enter the path to the Monzo bank statement file: ").strip('"')

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
    else:
        transactions = parse_bank_statement(file_path, start_line)

        insert_to_database(db, transactions, account_id)

        generate_and_print_report(db, account_id)
