from db import Database
from data.users import users
from data.accounts import accounts
from data.statements import statements
from data.categories import categories
from data.transactions import transactions
from transactions.transaction_service import TransactionService

db = Database('bankdb.sqlite')
db.create_tables()
db.insert_users(users)
db.insert_accounts(accounts)
db.insert_statements(statements)
db.insert_categories(categories)
db.insert_transactions(transactions)

ts = TransactionService(db)
start_date = input("Enter start date, example 2023-01-10: ")
end_date = input("Enter end date, example 2023-02-01: ")
transaction_in_period = ts.get_data_period(start_date, end_date)
framed_data = ts.convert_to_pd(transaction_in_period)
print(framed_data)
