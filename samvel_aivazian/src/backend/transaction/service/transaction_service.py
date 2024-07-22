transactions_db = {}


def add_transaction(user, date, description, money_in, money_out, type_, balance):
    if user not in transactions_db:
        transactions_db[user] = []

    transactions_db[user].append({
        "date": date,
        "description": description,
        "type": type_,
        "money_in": money_in,
        "money_out": money_out,
        "balance": balance
    })


def get_transactions(user, start_date=None, end_date=None):
    if user not in transactions_db:
        return []

    user_transactions = transactions_db[user]

    # If no date filters are provided, return all transactions
    if not start_date and not end_date:
        return user_transactions

    # Filter transactions by date range
    filtered_transactions = [
        t for t in user_transactions
        if (not start_date or t["date"] >= start_date) and
           (not end_date or t["date"] <= end_date)
    ]

    return filtered_transactions


def get_transactions_grouped_by_category(user, start_date=None, end_date=None):
    transactions = get_transactions(user, start_date, end_date)
    categorized_transactions = {}

    for transaction in transactions:
        category = transaction["description"]  # Simplified categorization logic

        if category not in categorized_transactions:
            categorized_transactions[category] = []

        categorized_transactions[category].append(transaction)

    return categorized_transactions
