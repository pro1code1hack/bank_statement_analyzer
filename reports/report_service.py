import os

from reports.data_helper import prepare_expense_data, prepare_income_data


class ReportService:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def generate_report(transactions, output_dir="../static/reports/bank_of_scotland", export_format="csv"):
        expense_df = prepare_expense_data(transactions)
        income_df = prepare_income_data(transactions)

        if export_format in ["csv", "json"]:
            os.makedirs(output_dir, exist_ok=True)

        if export_format == "csv":
            expense_csv_path = os.path.join(output_dir, "expenses.csv")
            income_csv_path = os.path.join(output_dir, "incomes.csv")
            expense_df.to_csv(expense_csv_path, index=False)
            income_df.to_csv(income_csv_path, index=False)
            print(f"Expenses and incomes exported to {output_dir} as CSV files.")
            return

        if export_format == "json":
            expense_json_path = os.path.join(output_dir, "expenses.json")
            income_json_path = os.path.join(output_dir, "incomes.json")
            expense_df.to_json(expense_json_path, orient="records", date_format="iso")
            income_df.to_json(income_json_path, orient="records", date_format="iso")
            print(f"Expenses and incomes exported to {output_dir} as JSON files.")
