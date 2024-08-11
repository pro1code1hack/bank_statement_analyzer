import os

from db import Database
from reports.data_helper import prepare_expense_data, prepare_income_data
from reports.report_service import ReportService
from transactions.parsers.bank_of_scotland_parser import BankOfScotlandParser
from transactions.transaction_service import TransactionService


def initialize_db():
    db = Database('bankdb.sqlite')
    db.create_tables()
    return db


def upload_bank_statement(db, file_path, account_id):
    parser = BankOfScotlandParser()
    transactions = parser.parse(file_path)

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


def generate_and_print_report(db, account_id, output_dir="bank_of_scotland"):
    transaction_service = TransactionService(db)
    report_service = ReportService()

    transactions = transaction_service.get_transactions_by_account(account_id)

    expense_df = prepare_expense_data(transactions)
    income_df = prepare_income_data(transactions)

    report_service.generate_report(transactions, output_dir, "csv")

    report_service.generate_report(transactions, output_dir, "json")

    print("Expenses:")
    print(expense_df.to_string(index=False))
    print("\nIncomes:")
    print(income_df.to_string(index=False))


if __name__ == "__main__":
    db = initialize_db()

    account_id = 1

    file_path = input("Enter the path to the bank statement file: ").strip('"')
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
    else:
        upload_bank_statement(db, file_path, account_id)

        generate_and_print_report(db, account_id)
