from db import Database

from transactions.transaction_service import TransactionService

def initialize_db():
    db = Database('bankdb.sqlite')
    return db

def get_transactions_for_period(db):
    transaction_service = TransactionService(db)
    start_date = input("Enter start date, example 2023-01-10: ")
    end_date = input("Enter end date, example 2023-02-01: ")
    list_transactions = transaction_service.get_transactions_for_period(start_date, end_date)
    return list_transactions

def convert_transactions_to_table(db, transactions):
    transaction_service = TransactionService(db)
    tabular_dataset = transaction_service.convert_to_pd(transactions)
    return tabular_dataset

db = initialize_db()

transaction = get_transactions_for_period(db)

if len(transaction) > 0:
    table = convert_transactions_to_table(db, transaction)
    print(table)
else: 
    print("No transactions found for the specified period")


def get_transactions_execute(db, account_id):
    transaction = get_transactions_for_period(db,account_id)
    if len(transaction) > 0:
        table = convert_transactions_to_table(db, transaction)
        print(table)
    else:
        print("No transactions found for the specified period")
