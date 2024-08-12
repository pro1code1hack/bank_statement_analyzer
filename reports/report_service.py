from typing import Dict, List

from transactions.transaction_service import Transaction
from .data_helper import prepare_expense_data, prepare_income_data
from .serialisation import BankOfScotlandSerialiser


class ReportService:
    """
    Service class for handling report generation and export.
    """

    @staticmethod
    def generate_report(transactions_by_category: Dict[str, List['Transaction']],
                        output_dir: str = "default_bank",
                        export_format: str = "csv") -> None:
        """
        Generate a report from the categorized transactions.

        :param:
            transactions_by_category: Dictionary of categorized transactions.
            output_dir: Directory to save the report. Defaults to "../static/reports/default_bank".
            export_format: Format to export the report.
            Defaults to "csv".
        """
        formatted_output_dir = f"./static/reports/{output_dir}"
        expense_df = prepare_expense_data(transactions_by_category)
        income_df = prepare_income_data(transactions_by_category)

        BankOfScotlandSerialiser.serialise(expense_df, income_df, formatted_output_dir, export_format)
