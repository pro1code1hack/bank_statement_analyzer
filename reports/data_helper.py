import pandas as pd


def prepare_expense_data(transactions_by_category):
    expense_data = []
    for category, transactions in transactions_by_category.items():
        for transaction in transactions:
            if transaction["money_out"] > 0:
                expense_data.append({
                    "date": transaction["date"],
                    "category": category,
                    "money_out": transaction["money_out"],
                    "balance": transaction["balance"]
                })
    expense_df = pd.DataFrame(expense_data).sort_values(by="date", ascending=False)
    return expense_df


def prepare_income_data(transactions_by_category):
    income_data = []
    for category, transactions in transactions_by_category.items():
        for transaction in transactions:
            if transaction["money_in"] > 0:
                income_data.append({
                    "date": transaction["date"],
                    "category": category,
                    "money_in": transaction["money_in"],
                    "balance": transaction["balance"]
                })
    income_df = pd.DataFrame(income_data).sort_values(by="date", ascending=False)
    return income_df
