import os

import matplotlib.pyplot as plt

from .data_helper import prepare_expense_data, prepare_income_data
from .plot_helper import plot_bar_chart


def generate_report(transactions_by_category, output_dir="../static/reports/bank_of_scotland",
                    output_file="report.pdf", export_format="graphical"):
    expense_df = prepare_expense_data(transactions_by_category)
    income_df = prepare_income_data(transactions_by_category)

    if export_format in ["csv", "json"]:
        os.makedirs(output_dir, exist_ok=True)

    if export_format == "csv":
        expense_csv_path = os.path.join(output_dir, "expenses.csv")
        income_csv_path = os.path.join(output_dir, "incomes.csv")
        expense_df.to_csv(expense_csv_path, index=False)
        income_df.to_csv(income_csv_path, index=False)
        print(f"Expenses and incomes exported to {output_dir} as CSV files.")

    if export_format == "json":
        expense_json_path = os.path.join(output_dir, "expenses.json")
        income_json_path = os.path.join(output_dir, "incomes.json")
        expense_df.to_json(expense_json_path, orient="records", date_format="iso")
        income_df.to_json(income_json_path, orient="records", date_format="iso")
        print(f"Expenses and incomes exported to {output_dir} as JSON files.")

    if export_format == "console":
        print("Categorized Transactions:")
        for category, transactions in transactions_by_category.items():
            print(f"\nCategory: {category}")
            for transaction in transactions:
                print(f"  Date: {transaction['date']}, "
                      f"Money In: {transaction.get('money_in', 0)}, Money Out: {transaction.get('money_out', 0)}, "
                      f"Balance: {transaction['balance']}")

    if export_format == "graphical":
        fig, axs = plt.subplots(1, 2, figsize=(36, 24))

        plot_bar_chart(axs[0], expense_df, "money_out", "Expenses by Category")
        plot_bar_chart(axs[1], income_df, "money_in", "Income by Category")

        plt.suptitle("Financial Report", fontsize=20)

        output_path = os.path.join(output_dir, output_file)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close(fig)
        print(f"Report generated and saved to {output_path}")
